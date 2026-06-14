# CSP bypass with blob URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40092664](https://issues.chromium.org/issues/40092664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-10-10 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36

Steps to reproduce the problem:
1. Go to https://vuln.shhnjk.com/iframer.php?url=https://test.shhnjk.com/blobCSP.html
2. Observe an alert

What is the expected behavior?
alert is blocked by CSP

What went wrong?
Patch of issues 799747 tries to see if there is any parent/opener where blob URL can inherit CSP from. Since they finds parent with no CSP, blob URL will happily inherit that and bypasses CSP.

Did this work before? N/A 

Chrome version: 69.0.3497.100  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### ct...@chromium.org (2018-10-11)

+andypaicu@ who is owner of the referenced bug.

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-10-15)

Keep in mind that this is according to spec. I think before we try to patch some more of these the spec itself needs fixing.

Also the related issue did not cause this issue, it's a fix for this same issue but it only works because that one was in a main frame, and this actually has a parent. This behavior would have been present before as well. I'm just saying this to avoid ambiguity because it's not clear.

There will be a TPAC CSP section and I think this should be discussed among other things.

### s....@gmail.com (2018-10-15)

LGTM :)

### sh...@chromium.org (2018-10-29)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-12)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### aw...@google.com (2018-12-04)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thanks for your report. The panel has decided to reward $1,000 :) 

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-02-14)

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

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/894228?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092664)*
