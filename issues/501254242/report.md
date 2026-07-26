# HLS key redirect bypasses origin restriction

| Field | Value |
|-------|-------|
| **Issue ID** | [501254242](https://issues.chromium.org/issues/501254242) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Reporter** | oj...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2026-04-10 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

HLS key redirect bypasses origin restriction

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A relative key URI in an HLS manifest (e.g. `URI="key.bin"`) is classified `kSafeOrigin` at parse time. If the server responds with a 302 redirect to a different origin, the fetch follows it, but the origin check still sees `kSafeOrigin` and lets the cross-origin response through. Direct absolute cross-origin URIs are correctly blocked on Dev 149, confirming the restriction works for those, but not for redirected relative URIs.

Chrome Stable 147 has no key-origin restriction at all; any cross-origin key URI is accepted.

## Steps to reproduce

1. Save `poc.py` (attached).
2. Run it:

```
python3 poc.py

```

3. Open Chrome:

```
google-chrome-unstable --no-first-run --user-data-dir=/tmp/hls-poc http://evil.localhost:9000/

```

4. Check the `poc.py` terminal.

## What you will see

poc.py terminal output on Chrome 149 Dev:

```
attacker: http://evil.localhost:9000/
target:   http://target.localhost:9001/secret
Open the attacker URL in Chrome and watch this terminal.
[attacker :9000] "GET / HTTP/1.1" 200 -
[attacker :9000] "GET /manifest.m3u8 HTTP/1.1" 200 -
[attacker :9000] "GET /key.bin HTTP/1.1" 302 -
[!] Cross-origin hit: target.localhost:9001/secret
[target   :9001] "GET /secret HTTP/1.1" 200 -
[attacker :9000] "GET /segment.ts HTTP/1.1" 200 -

```

The `segment.ts` request after the key fetch means the key was imported. Compare with a direct cross-origin URI (`URI="http://target.localhost:9001/secret"`) on the same Chrome build, where the key is fetched but rejected and no `segment.ts` follows:

```
[attacker :9000] "GET /manifest.m3u8 HTTP/1.1" 200 -
[target   :9001] "GET /secret HTTP/1.1" 200 -
[attacker :9000] "GET /favicon.ico HTTP/1.1" 404 -

```
## Expected result

A key fetch that lands on a different origin after redirect should be rejected the same way a direct cross-origin URI is.

## Affected versions

| Channel | Version | Behavior |
| --- | --- | --- |
| Stable | 147.0.7727.55 | No key restriction, any cross-origin key accepted |
| Dev | 149.0.7779.3 | Has restriction, bypassed by redirect from relative URI |

## Root cause

At parse time (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/media/formats/hls/media_playlist.cc#255>), a relative URI gets `kSafeOrigin`:

```
} else if (!declared_uri_value.starts_with("//") &&
           !GURL(declared_uri_value).has_scheme()) {
  key_location =
      MediaSegment::EncryptionData::KeyLocation::kSafeOrigin;
}

```

At fetch time (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/media/filters/hls_network_access_impl.cc#58>), the check only rejects `kUnsafeOrigin`:

```
if (stream->would_taint_origin() &&
    enc_data->GetKeyLocation() ==
        hls::MediaSegment::EncryptionData::KeyLocation::kUnsafeOrigin) {
  std::move(cb).Run({..., "insecure key request"});
  return;
}

```

After a cross-origin redirect, `would_taint_origin()` is true but `GetKeyLocation()` is still `kSafeOrigin`. The `&&` fails and the key goes through.

The comment on line 61-62 says:

> // Do not accept keys which would taint the origin, unless it is on the same
> // origin as the manifest which includes the key.

But the code doesn't actually verify that post-redirect.

## Bisection

Bypass introduced with the restriction itself: commit [db46e35db7](https://chromium-review.googlesource.com/c/chromium/src/+/7722343) ("Restrict origins for HLS keys", April 2, 2026, `refs/heads/main@{#1609376}`). The `kSafeOrigin` path-only heuristic doesn't account for redirects.

The underlying problem (HLS key fetches ignore CORS) predates that commit and affects all Chrome builds with `ENABLE_HLS_DEMUXER` (on when `proprietary_codecs` is true, i.e. all Google Chrome releases).

## Suggested fix

Drop the `kSafeOrigin` exemption. A relative URI that stays same-origin won't set `would_taint_origin()`, so checking that flag alone is sufficient:

```
if (stream->would_taint_origin()) {
  std::move(cb).Run({HlsDataSourceProvider::ReadStatus::Codes::kError,
                     "insecure key request"});
  return;
}

```
#### Impact analysis

## Security impact

The page makes a no-CORS GET to any URL the attacker picks, via the media stack. The attacker controls the redirect target.

This is useful for SSRF: redirect `key.bin` to `http://192.168.1.1/admin/status` and observe whether `segment.ts` is fetched afterward. If it is, the internal endpoint returned exactly 16 bytes (valid AES-128 key size). If not, it returned something else or errored. That binary signal leaks whether private endpoints exist and what size their responses are.

Same trick works for login-state detection on public sites. An endpoint returning different response sizes for logged-in vs. logged-out users is distinguishable through the 16-byte oracle.

The page visitor doesn't need to click anything.

---

### The cause

#### What version of Chrome have you found the security issue in?

Google Chrome 149.0.7779.3 (Dev, Linux x86\_64) & Google Chrome 147.0.7727.55 (Stable, Linux x86\_64)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Information Leak

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.2 MB)
- [poc.py](attachments/poc.py) (text/x-python, 2.7 KB)
- [index.html](attachments/index.html) (text/html, 589 B)

## Timeline

### aj...@google.com (2026-04-10)

note: bisect seems unrelated to the report.

This might be a real bug, passing to the team to take a look.

### oj...@gmail.com (2026-04-10)

To clarify, the bisect commit db46e35db7 is CL <https://chromium-review.googlesource.com/c/chromium/src/+/7718533> ("Restrict origins for HLS keys"), which introduced the kSafeOrigin classification for path-only URIs. This is the commit that introduced the bypass, as the heuristic doesn't account for redirects changing the final origin.

### ch...@google.com (2026-04-11)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### tm...@chromium.org (2026-04-13)

Yeah, seems like an oversight. The proposed fix is wrong though, it's misunderstanding what `would_taint_origin` means in this context. I'll get out another fix for it.

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  Ted Meyer [tmathmeyer@chromium.org](mailto:tmathmeyer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7759073>

Check for redirection when determinging key safety

---


Expand for full commit details
```
     
    The old logic only considered whether the key was cross origin and 
    declared relative to the manifest, but that doesn't work, because a 
    relative key can still 203 to any other URI. Now we do the following: 
     
    Non-Tainted Key => accept in all cases 
    Tainted, Redirected Key => reject in all cases 
    Tainted, Relative, Non-Redirected key => accept 
     
    Fixed: 501254242 
    Change-Id: I9a1ca06648ecf4d8fed10fd6d7070d40b8a17598 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7759073 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1615571}

```

---

Files:

- M `media/base/data_source.cc`
- M `media/base/data_source.h`
- M `media/filters/hls_data_source_provider.h`
- M `media/filters/hls_data_source_provider_impl.cc`
- M `media/filters/hls_network_access_impl.cc`
- M `media/filters/hls_network_access_impl_unittest.cc`
- M `media/filters/hls_test_helpers.h`
- M `third_party/blink/renderer/platform/media/multi_buffer_data_source.cc`
- M `third_party/blink/renderer/platform/media/multi_buffer_data_source.h`

---

Hash: [a8db6f5f733cfec577972326fa249a8551dbc394](https://chromiumdash.appspot.com/commit/a8db6f5f733cfec577972326fa249a8551dbc394)  

Date: Thu Apr 16 01:59:33 2026


---

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Web platform bypass, lower impact


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/501254242)*
