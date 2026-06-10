# Security: CSP does not propagate to blob: URIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40093065](https://issues.chromium.org/issues/40093065) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@googlemail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-11-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When setting a CSP that allows blob: URIs, creating a blob: of type "text/html" and then navigating to that blob removes the CSP restrictions.

**VERSION**  

Chromium Version: 70.0.3538.77 stable  

Operating System: ArchLinux x64, rolling release

**REPRODUCTION CASE**  

Serve index.html and script.js from a webserver setting a header of  

Content-Security-Policy "default-src 'self' blob:;

On index.html the embedded inline script does not get executed, because 'unsafe-inline' is not set. When navigating to the blob by clicking on the link, the inline script in the blob gets executed.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: sohalt

## Attachments

- [index.html](attachments/index.html) (text/plain, 243 B)
- [script.js](attachments/script.js) (text/plain, 358 B)

## Timeline

### pa...@googlemail.com (2018-11-14)

I forgot to include: Firefox propagates the CSP restrictions to the blob.

### dr...@chromium.org (2018-11-14)

andypaicu@: This looks very similar to http://crbug/799747, but I was able to reproduce this on Stable (70.0.3538.102). Is there a possible regression, or are they different bugs?

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### sh...@chromium.org (2018-11-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/108147dfd1ea159fd3632ef92ccc4ab8952980c7

commit 108147dfd1ea159fd3632ef92ccc4ab8952980c7
Author: Andy Paicu <andypaicu@chromium.org>
Date: Mon Nov 26 15:34:25 2018

Inherit the navigation initiator when navigating instead of the parent/opener

Spec PR: https://github.com/w3c/webappsec-csp/pull/358

Bug: 905301, 894228, 836148
Change-Id: I43ada2266d42d1cd56dbe3c6dd89d115e878a83a
Reviewed-on: https://chromium-review.googlesource.com/c/1314633
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610850}
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/frame_loader.h
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-main-window-self-navigate-inherits.sub.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### an...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d72a833dad8deabbf0e49ef16073542142db88a6

commit d72a833dad8deabbf0e49ef16073542142db88a6
Author: Mounir Lamouri <mlamouri@chromium.org>
Date: Mon Nov 26 20:19:56 2018

Revert "Inherit the navigation initiator when navigating instead of the parent/opener"

This reverts commit 108147dfd1ea159fd3632ef92ccc4ab8952980c7.

Reason for revert:
FindIt suggests a 74% chance that this is the cause of the following issues:
https://ci.chromium.org/buildbot/chromium.webkit/WebKit%20Linux%20Trusty%20Leak/26833

Original change's description:
> Inherit the navigation initiator when navigating instead of the parent/opener
> 
> Spec PR: https://github.com/w3c/webappsec-csp/pull/358
> 
> Bug: 905301, 894228, 836148
> Change-Id: I43ada2266d42d1cd56dbe3c6dd89d115e878a83a
> Reviewed-on: https://chromium-review.googlesource.com/c/1314633
> Commit-Queue: Andy Paicu <andypaicu@chromium.org>
> Reviewed-by: Mike West <mkwst@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#610850}

TBR=mkwst@chromium.org,andypaicu@chromium.org

Change-Id: If3ccf72cf8a4285926429f2855f32c1b0c606c5b
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 905301, 894228, 836148
Reviewed-on: https://chromium-review.googlesource.com/c/1351285
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: Mounir Lamouri <mlamouri@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610930}
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/frame_loader.h
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-self-navigate-inherits.sub.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-28)

(will re-add reward-topanel once it's marked as fixed again)

### bu...@chromium.org (2018-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29c42edb32d7e6825ea1d06a7d097668382dd91c

commit 29c42edb32d7e6825ea1d06a7d097668382dd91c
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Dec 04 12:29:42 2018

Rework of "inherit the navigation initiator when navigating"

Spec: https://w3c.github.io/webappsec-csp/#initialize-document-csp

This is a rework and reland of https://chromium-review.googlesource.com/c/chromium/src/+/1314633

The initial patch got reverted because it did not pass the trusty leak
build checks. The issue was that holding to the initiator document as a
member in FrameLoader was holding said document alive unreasonably long.
Instead this rework holds a copy of the initiator's CSP.

Bug: 905301, 894228, 836148
Change-Id: Ic12c28d20c53def5d6753449c3c4da7de5242ca2
Reviewed-on: https://chromium-review.googlesource.com/c/1353978
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#613521}
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/frame_loader.h
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-main-window-self-navigate-inherits.sub.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### an...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-13)

Thank you for submitting this report. The Panel has decided to reward you $1,000. Since you are a new reporter a member of our finance team will be in touch. 




### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-14)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-12-14)

How safe is this merge? Seems like a fairly large change. My preference is to target M73. 

### ab...@google.com (2019-01-08)

+awhalley@

### aw...@google.com (2019-01-08)

It's been out on dev for almost 4 weeks, so has good coverage, and doesn't seem too complex. andypaicu@, what do you think?

### ab...@google.com (2019-01-18)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/905301?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/990581]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093065)*
