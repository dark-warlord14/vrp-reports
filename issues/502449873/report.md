# Integer truncation in `protectedAudience.decodeUtf8()` causes out-of-bounds read via `strlen` in auction worklet utility process

| Field | Value |
|-------|-------|
| **Issue ID** | [502449873](https://issues.chromium.org/issues/502449873) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>InterestGroups |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2026-04-14 |
| **Bounty** | $3,000.00 |

## Description

# Integer truncation in `protectedAudience.decodeUtf8()` causes out-of-bounds read via `strlen` in auction worklet utility process

## Summary

The `TextConversionHelpers::DecodeUtf8` function in the Protected Audience (FLEDGE) auction worklet service passes a `size_t` byte length to `v8::String::NewFromUtf8`, whose length parameter is `int`. When a worklet supplies a Uint8Array whose byte length exceeds `INT_MAX`, the implicit narrowing produces a negative value, causing V8 to fall back to `strlen` on the raw buffer pointer. This results in an unbounded out-of-bounds read past the allocated buffer. The crash occurs in the sandboxed auction worklet utility process. The vulnerability affects all platforms (Linux, macOS, Windows) on 64-bit builds. The feature flag `kFledgeTextConversionHelpers` is currently disabled by default but is compiled into every Chrome binary and can be remotely enabled through Finch field trials at any time.

## Bisect

Introducing Commit: `e013281fdbd7cbff5f745e7aaf7b8e80d0fd282e`

- Date: 2025-02-27
- Author: Maks Orlovich [morlovich@chromium.org](mailto:morlovich@chromium.org)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6269638>

## Root Cause

`TextConversionHelpers::DecodeUtf8` extracts the backing data and byte length from the caller-supplied Uint8Array and forwards them directly to `v8::String::NewFromUtf8`:

```
// content/services/auction_worklet/text_conversion_helpers.cc
v8::Local<v8::Uint8Array> array = args[0].As<v8::Uint8Array>();
args.GetReturnValue().Set(
    v8::String::NewFromUtf8(
        isolate,
        UNSAFE_BUFFERS(reinterpret_cast<char*>(array->Buffer()->Data()) +
                       array->ByteOffset()),
        v8::NewStringType::kNormal, array->ByteLength())
        .ToLocalChecked());

```

`Uint8Array::ByteLength()` returns `size_t`, but the fourth parameter of `NewFromUtf8` is declared as `int`:

```
// v8/include/v8-primitive.h
static V8_WARN_UNUSED_RESULT MaybeLocal<String> NewFromUtf8(
    Isolate* isolate, const char* data,
    NewStringType type = NewStringType::kNormal, int length = -1);

```

When `ByteLength()` is 0x80000000 (2 GB), the implicit conversion to `int` yields -2147483648. Inside V8, the `NEW_STRING` macro handles this negative value as though no length was provided:

```
// v8/src/api/api.cc
#define NEW_STRING(v8_isolate, class_name, function_name, Char, data, type, \
                   length)                                                  \
  ...                                                                       \
  } else {                                                                  \
    ...                                                                     \
    if (length < 0) length = StringLength(data);                            \
    ...                                                                     \
  }

```

`StringLength` is a thin wrapper around `strlen`:

```
// v8/src/api/api.cc
inline int StringLength(const char* string) {
  size_t len = strlen(string);
  CHECK_GE(String::kMaxLength, len);
  ...
}

```

Because the caller fills the entire 2 GB buffer with non-zero bytes, `strlen` scans the full extent of the allocation and then continues reading one byte at a time into unmapped memory beyond the buffer, producing an out-of-bounds read. No existing mitigation intercepts this path: the buffer is raw memory (MiraclePtr is inapplicable), there are no `CHECK` guards before the narrowing conversion, and `DCHECK` is absent in release builds.

The `decodeUtf8` function is gated behind the runtime feature flag `kFledgeTextConversionHelpers`, which is currently `FEATURE_DISABLED_BY_DEFAULT`. The code is compiled into every Chrome binary; only the runtime switch prevents exposure. Google can enable it remotely through a Finch experiment at any time, at which point every bidder and seller worklet script gains access to the vulnerable API.

The Protected Audience API requires calling origins to pass a Privacy Sandbox attestation check, meaning only sites enrolled in Google's Privacy Sandbox program can invoke the auction machinery. In practice this is not a meaningful barrier, as any advertising participant (DSP, SSP, or ad network) holds a valid enrollment and can serve a malicious worklet script. For local testing, the `--privacy-sandbox-enrollment-overrides` switch whitelists a given origin.

## Reproduce

Tested at commit `123ee915f2e08` on Linux x86\_64.

PoC directory layout:

```
issue_content013/
├── poc.html      main page: joins interest group and runs auction
├── bidder.js     bidder worklet: allocates 2 GB, calls decodeUtf8()
├── seller.js     seller worklet: trivial scoreAd
├── ad.html       placeholder ad render URL
└── server.py     HTTPS server with Ad-Auction-Allowed headers

```

Build configuration (`args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```

Build:

```
autoninja -C out/asan-release chrome

```

Start the PoC HTTPS server (generates a self-signed certificate automatically):

```
cd issue_content013 && python3 server.py

```

In a second terminal, launch Chrome:

```
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a ./out/asan-release/chrome \
  --enable-features=FledgeTextConversionHelpers,OverridePrivacySandboxSettingsLocalTesting \
  --privacy-sandbox-enrollment-overrides=https://localhost:8443 \
  --no-sandbox --disable-gpu --ignore-certificate-errors \
  --user-data-dir=/tmp/poc-$(date +%s) \
  --enable-logging=stderr \
  'https://localhost:8443/'

```

The page automatically joins an interest group and triggers a Protected Audience auction. The bidder worklet allocates a 2 GB WebAssembly memory, fills it with non-zero bytes, and calls `protectedAudience.decodeUtf8()` on the resulting Uint8Array. The auction worklet utility process crashes with SIGSEGV within a few seconds. The complete crash output is in `crash.log`; the symbolized portion follows:

```
Received signal 11 SEGV_ACCERR 7a2f80000000
#0 (chrome+0x6757235)    __interceptor_backtrace
#1 (libbase.so+0x766771) base::debug::CollectStackTrace()                    stack_trace_posix.cc:1050
#2 (libbase.so+0x70bf52) base::debug::StackTrace::StackTrace()               stack_trace.cc:280
#3 (libbase.so+0x765a0a) base::debug::StackDumpSignalHandler()               stack_trace_posix.cc:483
#4 (libc.so.6+0x4251f)   __GI___sigaction
#5 (libc.so.6+0x19d95f)  __strlen_avx2                                       strlen-avx2.S:276
#6 (chrome+0x6727bc3)    __interceptor_strlen
#7 (libv8.so+0x15401b6)  v8::String::NewFromUtf8()                           v8/src/api/api.cc:7511
#8 (libcontent.so+0x7acc8ce) auction_worklet::TextConversionHelpers::DecodeUtf8()  text_conversion_helpers.cc:137

  r12: 0000000080000000  r14: 00007a2f00000000
  cr2: 00007a2f80000000

cr2 = r14 + r12: the fault address is buffer base + 0x80000000, exactly one byte
past the end of the 2 GB allocation.

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [ad.html](attachments/ad.html) (text/html, 45 B)
- [seller.js](attachments/seller.js) (text/javascript, 180 B)
- [readme.md](attachments/readme.md) (text/markdown, 916 B)
- [crash.log](attachments/crash.log) (text/plain, 2.1 KB)
- [poc.html](attachments/poc.html) (text/html, 1.1 KB)
- [bidder.js](attachments/bidder.js) (text/javascript, 755 B)
- [server.py](attachments/server.py) (text/x-python, 2.0 KB)

## Timeline

### ma...@google.com (2026-04-16)

security shepherd: OOB read -> S1; disabled feature flag: SI-None. Did not yet attempt a repro.

morlovich, PTAL. Could you confirm that this feature has not been enabled for any part of the Chrome Stable population, including via Origin Trials?

### mo...@chromium.org (2026-04-16)

It went up to Beta, you can see the state of removal in cl/834806286.
Also in field trial config, but I suppose everything is.

### ma...@google.com (2026-04-16)

But it's currently not active by default in any release channel?

### je...@gmail.com (2026-04-17)

decodeUtf8() is a handwritten V8 C++ callback that directly reads the ByteLength() from a Uint8Array object, completely bypassing Blink's Web IDL bindings layer input validation checks (which enforce a maximum size of 2G-2M).

### mo...@chromium.org (2026-04-17)

It's a non-blink process, and this is one of the downsides of that decision.

> But it's currently not active by default in any release channel?

Right. Experiment removed, feature always has been FEATURE_DISABLED_BY_DEFAULT.  Actually not in field trial config either, I was confused by google-side code search including old branches. (Removed by Russ in https://chromium.googlesource.com/chromium/src/+/fea7c3b9092d232ac9292788c08bcb880b63c66f%5E%21/)

So I think the risk is only to whoever is somehow running old versions with --enable-field-trial-testing-config and... people stuck with old experiment config that turns it on, somehow? 
Not sure how much we can even do to help people in such circumstances.


### ma...@google.com (2026-04-17)

Yeah, we classify it as Security\_Impact-None then.

It's totally resolve this issue by fully removing the code if there's not plan to launch. If you have a bug for the removal, I'd recommend marking it as blocking this one.

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  main  

Author:  Paul Jensen [pauljensen@chromium.org](mailto:pauljensen@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7823020>

Remove FledgeTextConversionHelpers code

---


Expand for full commit details
```
     
    This feature didn't ship and given that the parent feature, Protected 
    Audience, is deprecated, it won't in the future, so remove the code. 
     
    Fixed: 502449873 
    Change-Id: I3b7f6bdd8b5f9c7afb6195fe0fc91bc3253f10ab 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7823020 
    Reviewed-by: Jeremy Roman <jbroman@chromium.org> 
    Commit-Queue: Paul Jensen <pauljensen@chromium.org> 
    Reviewed-by: Maks Orlovich <morlovich@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1626498}

```

---

Files:

- M `content/browser/interest_group/interest_group_browsertest.cc`
- M `content/services/auction_worklet/BUILD.gn`
- M `content/services/auction_worklet/bidder_worklet.cc`
- M `content/services/auction_worklet/bidder_worklet_unittest.cc`
- M `content/services/auction_worklet/context_recycler.cc`
- M `content/services/auction_worklet/context_recycler.h`
- M `content/services/auction_worklet/context_recycler_unittest.cc`
- M `content/services/auction_worklet/public/cpp/auction_worklet_features.cc`
- M `content/services/auction_worklet/public/cpp/auction_worklet_features.h`
- M `content/services/auction_worklet/seller_worklet.cc`
- M `content/services/auction_worklet/seller_worklet_unittest.cc`
- D `content/services/auction_worklet/text_conversion_helpers.cc`
- D `content/services/auction_worklet/text_conversion_helpers.h`
- M `gin/public/gin_embedders.h`

---

Hash: [c843cd5af63fd57bafa003d9ea294c7abdc78d57](https://chromiumdash.appspot.com/commit/c843cd5af63fd57bafa003d9ea294c7abdc78d57)  

Date: Wed May 6 22:19:31 2026


---

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502449873)*
