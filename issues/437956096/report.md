# Debug check failed: allow_empty_handle || !i::ValueHelper::IsEmpty(that)

| Field | Value |
|-------|-------|
| **Issue ID** | [437956096](https://issues.chromium.org/issues/437956096) |
| **Status** | Verified |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2025-08-12 |
| **Bounty** | Confirmed (amount unknown) |

## Description

```


#
# Fatal error in ../../src/api/api-inl.h, line 147
# Debug check failed: allow_empty_handle || !i::ValueHelper::IsEmpty(that).
#
#
#
#FailureMessage Object: 0x7fff864572c8
==== C stack trace ===============================

    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fb9eebc849e]
    /home/user/v8/v8/out/x64.debug/libv8_libplatform.so(+0x4abbd) [0x7fb9eeb33bbd]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x7fb9eeba0e65]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(+0x4e81c) [0x7fb9eeba081c]
    /home/user/v8/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x7fb9eeba0f3d]
    ./x64.debug/d8(v8::Utils::OpenHandle(v8::String const*, bool)+0x54) [0x55759e652324]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::String::Concat(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>)+0x3d) [0x7fb9f675717d]
    ./x64.debug/d8(v8::Shell::FunctionAndArgumentsToString(v8::Local<v8::Function>, v8::Local<v8::Value>, v8::Local<v8::String>*, v8::Isolate*)+0x25e) [0x55759e62cd8e]
    ./x64.debug/d8(v8::Shell::ReadSource(v8::FunctionCallbackInfo<v8::Value> const&, int, v8::Shell::CodeType)+0x120) [0x55759e628de0]
    ./x64.debug/d8(v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&)+0x148) [0x55759e62d188]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::FunctionCallbackArguments::CallOrConstruct(v8::internal::Tagged<v8::internal::FunctionTemplateInfo>, bool)+0x1e0) [0x7fb9f68a3200]
    /home/user/v8/v8/out/x64.debug/libv8.so(+0x7cc6c6c) [0x7fb9f68a0c6c]
    /home/user/v8/v8/out/x64.debug/libv8.so(+0x7cc6012) [0x7fb9f68a0012]
    /home/user/v8/v8/out/x64.debug/libv8.so(v8::internal::Builtin_HandleApiConstruct(int, unsigned long*, v8::internal::Isolate*)+0xfb) [0x7fb9f689fb8b]
    [0x7fb9736aacfd]
Trace/breakpoint trap (core dumped)

```
#### VERSION

V8 version 14.0.0 (candidate)

#### REPRODUCTION CASE

Build: `python3 tools/dev/gm.py x64.debug`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 211 B)

## Timeline

### fa...@gmail.com (2025-08-12)

```
user@local:~/v8-all$ 11.4.99/d8 new.js


#
# Fatal error in ../v8/src/api/api-inl.h, line 121
# Debug check failed: allow_empty_handle || !v8::internal::ValueHelper::IsEmpty(that).
#
#
#
#FailureMessage Object: 0x7f7230300c60
==== C stack trace ===============================

    11.4.99/d8(__interceptor_backtrace+0x57) [0x55fb97c82a47]
    /home/user/v8-all/11.4.99/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f72334caec3]
    /home/user/v8-all/11.4.99/libv8_libplatform.so(+0x2dcfa) [0x7f7233415cfa]
    /home/user/v8-all/11.4.99/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x27f) [0x7f723348410f]
    /home/user/v8-all/11.4.99/libv8_libbase.so(+0x4e0af) [0x7f72334830af]
    /home/user/v8-all/11.4.99/libv8.so(v8::String::Concat(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>)+0x170) [0x7f72358988e0]
    11.4.99/d8(+0x1a9430) [0x55fb97d5e430]
    11.4.99/d8(+0x19fef8) [0x55fb97d54ef8]
    11.4.99/d8(+0x1a97d1) [0x55fb97d5e7d1]
    /home/user/v8-all/11.4.99/libv8.so(+0x25ae266) [0x7f7235a96266]
    /home/user/v8-all/11.4.99/libv8.so(+0x25a93bd) [0x7f7235a913bd]
    /home/user/v8-all/11.4.99/libv8.so(+0x25a74d0) [0x7f7235a8f4d0]
    /home/user/v8-all/11.4.99/libv8.so(+0x25a6141) [0x7f7235a8e141]
    /home/user/v8-all/11.4.99/libv8.so(+0x1c91ebd) [0x7f7235179ebd]
Trace/breakpoint trap (core dumped)


user@local:~/v8-all$ 10.9.99/d8 new.js


#
# Fatal error in ../v8/src/api/api-inl.h, line 130
# Debug check failed: allow_empty_handle || that != nullptr.
#
#
#
#FailureMessage Object: 0x7f63a5365460
==== C stack trace ===============================

    10.9.99/d8(backtrace+0x57) [0x55bb6a3bde67]
    /home/user/v8-all/10.9.99/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f63a8429bd3]
    /home/user/v8-all/10.9.99/libv8_libplatform.so(+0x2f12a) [0x7f63a837312a]
    /home/user/v8-all/10.9.99/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x26f) [0x7f63a83e329f]
    /home/user/v8-all/10.9.99/libv8_libbase.so(+0x4f21f) [0x7f63a83e221f]
    /home/user/v8-all/10.9.99/libv8.so(v8::String::Concat(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>)+0x256) [0x7f63aada0966]
    10.9.99/d8(v8::Shell::FunctionAndArgumentsToString(v8::Local<v8::Function>, v8::Local<v8::Value>, v8::Local<v8::String>*, v8::Isolate*)+0x24a) [0x55bb6a49c02a]
    10.9.99/d8(v8::Shell::ReadSource(v8::FunctionCallbackInfo<v8::Value> const&, int, v8::Shell::CodeType)+0x548) [0x55bb6a490cd8]
    10.9.99/d8(v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&)+0x21d) [0x55bb6a49c36d]
    /home/user/v8-all/10.9.99/libv8.so(v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo)+0x3a9) [0x7f63ab0197a9]
    /home/user/v8-all/10.9.99/libv8.so(+0x2bd18ff) [0x7f63ab0128ff]
    /home/user/v8-all/10.9.99/libv8.so(+0x2bcdf8e) [0x7f63ab00ef8e]
    /home/user/v8-all/10.9.99/libv8.so(v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*)+0x230) [0x7f63ab00d8b0]
    [0x7f633f9d99ff]
Trace/breakpoint trap (core dumped)


user@local:~/v8-all$ 10.4.99/d8 new.js


#
# Fatal error in ../v8/src/api/api-inl.h, line 132
# Debug check failed: allow_empty_handle || that != nullptr.
#
#
#
#FailureMessage Object: 0x7f1420c75060
==== C stack trace ===============================

    10.4.99/d8(backtrace+0x5b) [0x56257013143b]
    /home/user/v8-all/10.4.99/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f1423d94ca3]
    /home/user/v8-all/10.4.99/libv8_libplatform.so(+0x3c09a) [0x7f1423cca09a]
    /home/user/v8-all/10.4.99/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x26f) [0x7f1423d4c25f]
    /home/user/v8-all/10.4.99/libv8_libbase.so(+0x5d18f) [0x7f1423d4b18f]
    /home/user/v8-all/10.4.99/libv8.so(v8::String::Concat(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>)+0x168) [0x7f14267b77a8]
    10.4.99/d8(v8::Shell::FunctionAndArgumentsToString(v8::Local<v8::Function>, v8::Local<v8::Value>, v8::Local<v8::String>*, v8::Isolate*)+0x1d2) [0x5625701ff8e2]
    10.4.99/d8(v8::Shell::ReadSource(v8::FunctionCallbackInfo<v8::Value> const&, int, v8::Shell::CodeType)+0x541) [0x5625701f3d31]
    10.4.99/d8(v8::Shell::WorkerNew(v8::FunctionCallbackInfo<v8::Value> const&)+0x213) [0x5625701ffc03]
    /home/user/v8-all/10.4.99/libv8.so(v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo)+0x412) [0x7f1426a0dc02]
    /home/user/v8-all/10.4.99/libv8.so(+0x2c56981) [0x7f1426a05981]
    /home/user/v8-all/10.4.99/libv8.so(+0x2c513af) [0x7f1426a003af]
    /home/user/v8-all/10.4.99/libv8.so(v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*)+0x22e) [0x7f14269fed9e]
    [0x7f13bfa081bf]
Trace/breakpoint trap (core dumped)

```

Bisection indicates the issue existed before `V8 version 10.4.99`.

### fa...@gmail.com (2025-08-12)

On release build `V8 version 14.0.0 (candidate)`:

```
user@local:~/v8/v8/out$ ./x64.release/d8 test.js
Received signal 11 SEGV_MAPERR 000000000000

==== C stack trace ===============================

./x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x13)[0x558a3d1014c3]
./x64.release/d8(+0x2c1041f)[0x558a3d10141f]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7face33ab330]
./x64.release/d8(_ZN2v86String6ConcatEPNS_7IsolateENS_5LocalIS0_EES4_+0x49)[0x558a3ba0f299]
./x64.release/d8(_ZN2v85Shell28FunctionAndArgumentsToStringENS_5LocalINS_8FunctionEEENS1_INS_5ValueEEEPNS1_INS_6StringEEEPNS_7IsolateE+0x19d)[0x558a3b97c12d]
./x64.release/d8(_ZN2v85Shell10ReadSourceERKNS_20FunctionCallbackInfoINS_5ValueEEEiNS0_8CodeTypeE+0x1a9)[0x558a3b978d99]
./x64.release/d8(_ZN2v85Shell9WorkerNewERKNS_20FunctionCallbackInfoINS_5ValueEEE+0x82)[0x558a3b97c282]
./x64.release/d8(_ZN2v88internal25FunctionCallbackArguments15CallOrConstructENS0_6TaggedINS0_20FunctionTemplateInfoEEEb+0x10f)[0x558a3ba4badf]
./x64.release/d8(+0x155a25e)[0x558a3ba4b25e]
./x64.release/d8(+0x155996b)[0x558a3ba4a96b]
./x64.release/d8(+0x2aadf76)[0x558a3cf9ef76]
[end of stack trace]
Segmentation fault (core dumped)

```

### cl...@appspot.gserviceaccount.com (2025-08-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6095532820725760.

### ch...@google.com (2025-08-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ta...@google.com (2025-08-14)

I can reproduce this locally, but I do not believe it is a security vulnerability. I am conservatively keeping the label until this is confirmed. Victor, could you please take a look at this, as Andreas is out of office?

### cl...@appspot.gserviceaccount.com (2025-08-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6376888075223040.

### th...@chromium.org (2025-08-14)

Marja, can you take this? We just seem to be missing some error handling here [1]. This concat fails (out of range) and returns an empty handle, and somewhere inside that other concat [2] there is the DCHECK that expects a non-empty handle.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/d8/d8.cc;drc=4de1c836b12a44f0b7702898909428458488e17e;l=3325>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/d8/d8.cc;drc=4de1c836b12a44f0b7702898909428458488e17e;l=3335>

### th...@chromium.org (2025-08-14)

Removing security labels, this looks harmless and this is a d8-only feature.

### 24...@project.gserviceaccount.com (2025-08-14)

Detailed Report: https://clusterfuzz.com/testcase?key=6376888075223040

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  allow_empty_handle || !i::ValueHelper::IsEmpty(that) in api-inl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=86689:86690

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6376888075223040

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2025-08-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### th...@chromium.org (2025-08-14)

CC Nikos because CF bisects it to your CL, but I suspect that it did not introduce the root cause. It looks like it just touches the failing DCHECK.

### ni...@chromium.org (2025-08-19)

This is a very old `DCHECK`.  

It exists roughly in this form since [my CL](https://chromium-review.googlesource.com/c/v8/v8/+/4296134) (March 2023, landed in 113.0.5626.0).  

Before that, you would get the `that != nullptr` version.  

Further back, this was converted to a `DCHECK` by [this CL](https://codereview.chromium.org/841083002) (January 2015).  

It originates in [an ancient CL](https://chromiumcodereview.appspot.com/10917088) by Jakob (September 2012).  

If one somehow manages to run an earlier version with this POC (assuming that workers and all would work), you'd still get the crash both in debug and release builds.  

I don't think that the result of CF's bisection makes any sense.

### th...@chromium.org (2025-08-19)

I don't think the bug goes that far back though. The empty handle comes from a failing `String::Concat` that happens during `FunctionAndArgumentsToString`, which was introduced [here](https://chromium-review.googlesource.com/c/v8/v8/+/2643381). So I think we just need to handle the error there, see [comment #9](https://issues.chromium.org/issues/437956096#comment9).

### ni...@chromium.org (2025-08-19)

The empty handle is produced [here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/api/api.cc;drc=280cd6cc9ad696c74313035a0bbaab8f4f8c4bf4;l=7682), because the string is too long.  

From what I can see, this changed with a quite [old CL](https://codereview.chromium.org/735763002/) (November 2014).  

This changed the behaviour of `v8::String::Concat` so that it does not throw if the length limit is reached.  

It seems, however, that a lot of calls do not expect an empty handle, e.g., the one crashing here, or [this one](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/d8/d8-posix.cc;drc=280cd6cc9ad696c74313035a0bbaab8f4f8c4bf4;l=325), or those [in here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/d8/d8.cc;drc=280cd6cc9ad696c74313035a0bbaab8f4f8c4bf4;l=3151).  

Fortunately, I have not found any such case probable to overflow outside d8.

I'll prepare a fix for this.

### dx...@google.com (2025-08-21)

Project: v8/v8  

Branch:  main  

Author:  Nikolaos Papaspyrou [nikolaos@chromium.org](mailto:nikolaos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6863276>

[d8] Expect limit exceeded in string concatenation

---


Expand for full commit details
```
     
    Method v8::String::Concat does not throw an exception in case the 
    length of the result exceeds the allowed limit. Instead, it returns 
    an empty local handle. This CL fixes a number of calls of this method 
    in d8, where the result can get arbitrarily big and this case was not 
    properly checked. 
     
    Bug: 437956096 
    Change-Id: Ie9f7127594fd1669b2e789340305ed2675d1ad3d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6863276 
    Commit-Queue: Nikolaos Papaspyrou <nikolaos@chromium.org> 
    Reviewed-by: Camillo Bruni <cbruni@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101968}

```

---

Files:

- M `src/d8/d8-posix.cc`
- M `src/d8/d8.cc`
- M `src/d8/d8.h`
- A `test/mjsunit/regress/regress-437956096.js`

---

Hash: [fb1a4f36e01bf56855affe861bae8ad5e84d805c](https://chromiumdash.appspot.com/commit/fb1a4f36e01bf56855affe861bae8ad5e84d805c)  

Date: Thu Aug 21 09:16:37 2025


---

### ni...@chromium.org (2025-08-21)

This should be fixed by the above.

### ni...@chromium.org (2025-08-21)

Thank you for reporting this, Fazim!

### fa...@gmail.com (2025-08-21)

ur welcome, and thank you for addressing this issue 😁.

### fa...@gmail.com (2025-08-21)

Hi, I think we can also close this issue: <https://issues.chromium.org/u/1/issues/425185698>. I believe it's the same issue.

### ni...@chromium.org (2025-08-21)

I'm afraid I don't have access to [issue 425185698](https://issues.chromium.org/issues/425185698).  

If it's d8-specific, it shouldn't been a vulnerability either.

### 24...@project.gserviceaccount.com (2025-08-22)

ClusterFuzz testcase 5996044118589440 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=101967:101968

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
While we appreciate the report, this appears to be a report of a functional issue, rather than an exploitable security bug. This report is, therefore, unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> While we appreciate the report, this appears to be a report of a functional issue, rather than an exploitable security bug. This report is, therefore, unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Securit

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/437956096)*
