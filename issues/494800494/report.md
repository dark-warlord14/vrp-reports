# AreRequestHeadersSafe() missing Origin and Sec-* prefix blocking — compromised renderer forges Origin and Sec-Fetch-* headers via modified_headers in FollowRedirect

| Field | Value |
|-------|-------|
| **Issue ID** | [494800494](https://issues.chromium.org/issues/494800494) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2026-03-21 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

AreRequestHeadersSafe() missing Origin and Sec-\* prefix blocking — compromised renderer forges Origin and Sec-Fetch-\* headers via modified\_headers in FollowRedirect

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/header_util.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`IsRequestHeaderSafe()` in `header_util.cc` blocks `Host` and `Proxy-*` headers but omits `Origin` and has no `Sec-` prefix check. A compromised renderer forges `Origin` and `Sec-Fetch-*` headers via `modified_headers` in `FollowRedirect()`, overwriting values the network service sets on cross-origin redirects.

**Vulnerable file:** [header\_util.cc](https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/header_util.cc) — `IsRequestHeaderSafe()`

This violates `docs/security/compromised-renderers.md`: "Compromised renderers shouldn't be able to control security sensitive HTTP request headers like `Host`, `Origin`, or `Sec-Fetch-Site`."

On redirect: `redirect_util.cc:87` sets `Origin: null`, then `MergeFrom(modified_headers)` at line 93 overwrites it. `SetFetchMetadataHeaders` writes correct `Sec-Fetch-*` before `modified_headers` overwrite them.

Additionally, `SetSecFetchModeHeader` in `sec_header_helpers.cc:173` uses `SetHeaderIfMissing`, so a renderer-set `Sec-Fetch-Mode` persists on the initial request without any redirect.

**Steps to reproduce:**

1. Check out stable tag: `git checkout 146.0.7680.154`
2. `git apply poc_patch.diff`
3. `autoninja -C out/Default chrome`
4. Start PoC servers: `python3 serve.py`
5. Launch patched Chrome:
   - `out/Default/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/hdr1-test http://localhost:8080/`
6. Click "Run Both" — observe forged headers in the server terminal:
   - `Origin: http://127.0.0.1:8081` (should be `null` on cross-origin redirect)
   - `Sec-Fetch-Site: same-origin` (should be `cross-site`)

The renderer patch injects forged `Origin` and `Sec-Fetch-*` into `modified_headers` during `ResourceLoader::WillFollowRedirect()` on cross-origin redirects. No flags needed.

**Bisect:**

Introducing commit: `eb88b44f8e655` — Matt Menke, 2019-06-18, M77. Created `kUnsafeHeaders` blocklist without `Origin` or `Sec-` prefix. Parent commit has no blocklist. Moved to `header_util.cc` in `633e7e6277b64`.
Affected: M77 through M146 (current stable).

**Fix:** Add `Origin` to `kUnsafeHeaders` and add `Sec-` prefix check in `IsRequestHeaderSafe()`, matching the existing `Proxy-` prefix check. Also change `SetSecFetchModeHeader` to `overwrite=true`. Attached as `fix.diff`.

#### Impact analysis

The PoC demonstrates two concrete bypasses:

1. **CSRF bypass:** Victim server receives `Origin: http://127.0.0.1:8081` (forged to match victim) instead of `null` on a cross-origin POST redirect (307). Server-side CSRF validation that checks Origin is defeated.
2. **Fetch Metadata bypass:** Victim server receives `Sec-Fetch-Site: same-origin` instead of `cross-site`. Server-side resource isolation policies recommended by `compromised-renderers.md` (line 96) are defeated.

Variant analysis also found `Access-Control-Request-Private-Network` and `Cookie` (when 3P-blocked) are forgeable through the same gap.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.154 (Stable)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [fix.diff](attachments/fix.diff) (application/octet-stream, 903 B)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 1.3 KB)
- [index.html](attachments/index.html) (text/html, 4.6 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 4.1 KB)

## Timeline

### os...@gmail.com (2026-03-21)

CL with fix and unit test:

<https://chromium-review.googlesource.com/c/chromium/src/+/7690887>

### el...@google.com (2026-03-24)

Security shepherd: thanks for the report. I haven't run the PoC but your reasoning looks legit so I'm kicking this to mmenke@ for a further look. This is Sev-3 in our threat model I think, maybe Sev-2; I'll let mmenke figure that out too.

### mm...@chromium.org (2026-03-24)

HttpUtil::IsSafeHeader() is the method that returns false when it receives a header with the "Sec-" prefix or the Origin header. While the network service reports a bad message if AreRequestHeadersSafe() returns false, CorsUnsafeNotForbiddenRequestHeaderNames() checks using HttpUtil::IsSafeHeader().

I'm not an expert on the CORS code, so I defer to them on whether that's sufficient.

### mm...@chromium.org (2026-03-24)

I will note that the POC adds the "Sec-Fetch-Mode: no-cors" header.

### mm...@chromium.org (2026-03-24)

Worth noting kUnsafeHeaders were introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/1669431> (which was not landed on 2019-06-18, nor was written by me), at a point when CORS headers were still generated by the renderer process, so the bit about a regression in M77, when the network service was still run in the browser process, is bogus. It was, at the time, I believe the maximal set of headers we could CHECK on.

There's actually an old TODO about investigating expanding this list at <https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/header_util.cc;l=65>. I seem to remember at one point having histograms about expanding the list.

Possible we could be more restrictive on requests from renderers. I'm skeptical we could just expand the list without breaking some Android WebView consumers.

### os...@gmail.com (2026-03-25)

Thanks for the analysis. Apologies for the bisect error, the blocklist was correct at introduction when CORS was still renderer-side.

On whether `CorsUnsafeNotForbiddenRequestHeaderNames()` covers this: I don't think it does, for two reasons.

First, the function skips forbidden headers. `IsSafeHeader()` returns false for `Origin` and `Sec-*`, so they get `continue`'d past. They're invisible to `NeedsPreflight()` even when it runs during cors-mode redirects.

Second, for no-cors requests `NeedsPreflight()` returns nullopt immediately since the mode isn't CORS-enabled.

So `AreRequestHeadersSafe()` ends up being the only gate on `modified_headers` during redirect, and it doesn't block these. Each check seems to assume the other enforces them.

Impact-wise: `redirect_util.cc` sets `Origin: null` on cross-origin redirect, then `MergeFrom(modified_headers)` overwrites it. So the victim server sees a forged same-origin `Origin` and `Sec-Fetch-Site: same-origin` instead of `cross-site`, defeating CSRF and Fetch Metadata checks.

### to...@chromium.org (2026-03-27)

bashi, ricea:
someone from your team can take a look at this?

### to...@chromium.org (2026-04-13)

For the Origin modification, probably the best approach is to apply the existing origin lock check that was done on starting request today. I will try expanding this to redirect path.

Regarind the Set-\*, we still have some proper path where renderer sets such a headers in the Blink side. So, I need to exempt it, maybe Sec-CH-UA only?, from the forbidden header checks.

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  Takashi Toyoshima [toyoshim@chromium.org](mailto:toyoshim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7760107>

OOR-CORS: Block Origin header modification on redirect in CorsURLLoader

---


Expand for full commit details
```
     
    This change prevents a compromised renderer from spoofing the Origin 
    header during a cross-origin redirect by abusing the 
    CorsURLLoader::FollowRedirect API. 
     
    If the renderer attempts to modify the Origin header in FollowRedirect, 
    the request is rejected with net::ERR_INVALID_ARGUMENT. Ideally we 
    should use mojo::ReportBadMessage to kill the renderer, but it causes 
    the network service to crash in tests. We leave a TODO to change it to 
    ReportBadMessage once the testing infrastructure supports it. 
     
    This fix is protected by kBlockOriginHeaderModificationOnRedirect 
    feature, which is enabled by default. 
     
    Bug: 494800494 
    Change-Id: I6a86af4c4aa57fd671cebb5336337b45e3102552 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760107 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1616291}

```

---

Files:

- M `content/browser/loader/loader_browsertest.cc`
- M `services/network/cors/cors_url_loader.cc`
- M `services/network/public/cpp/features.cc`
- M `services/network/public/cpp/features.h`

---

Hash: [fd71efb820447671572c62544e3a93a78e8a6d7f](https://chromiumdash.appspot.com/commit/fd71efb820447671572c62544e3a93a78e8a6d7f)  

Date: Fri Apr 17 02:43:25 2026


---

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  Takashi Toyoshima [toyoshim@chromium.org](mailto:toyoshim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7760510>

OOR-CORS: Enforce extra forbidden Sec- header checks

---


Expand for full commit details
```
     
    This CL adds a new function ContainsForbiddenSecurityHeader in 
    header_util to check for unauthorized Sec- headers from renderer. 
     
    This function is used in both CorsURLLoaderFactory::IsValidRequest and 
    CorsURLLoader::FollowRedirect to prevent renderer from injecting or 
    modifying these headers, while permitting Client Hints and Sec-Purpose. 
     
    Change-Id: Ia2923ccbddddba2657d72916a03e657c1785cd85 
    Bug: 494800494 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760510 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619285}

```

---

Files:

- M `services/network/cors/cors_url_loader.cc`
- M `services/network/cors/cors_url_loader_factory.cc`
- M `services/network/cors/cors_url_loader_factory.h`
- M `services/network/public/cpp/features.cc`
- M `services/network/public/cpp/features.h`
- M `services/network/public/cpp/header_util.cc`
- M `services/network/public/cpp/header_util.h`
- M `services/network/public/cpp/header_util_unittest.cc`
- M `tools/metrics/histograms/metadata/network/histograms.xml`

---

Hash: [1917c17d0ad2fdc3e994a9aefd254b8db7bbe457](https://chromiumdash.appspot.com/commit/1917c17d0ad2fdc3e994a9aefd254b8db7bbe457)  

Date: Thu Apr 23 02:42:38 2026


---

### os...@gmail.com (2026-04-23)

Fixes landed in <https://chromium-review.googlesource.com/c/chromium/src/+/7760107> (Origin header) and <https://chromium-review.googlesource.com/c/chromium/src/+/7760510> (Sec-\* headers).

Added to Security-Fixed-Issue-Request hotlist per the rule update.

### ch...@google.com (2026-04-30)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
web platform bypass via compromised renderer


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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494800494)*
