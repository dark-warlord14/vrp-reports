# Security: Form field validation bubbles can appear over the wrong tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40087137](https://issues.chromium.org/issues/40087137) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Validation |
| **Platforms** | Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2017-03-23 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 59.0.3049.0 Canary + stable  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open the testcase
2. Click on the button and observe

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 988 B)
- [screenshot.png](attachments/screenshot.png) (image/png, 144.3 KB)

## Timeline

### ch...@gmail.com (2017-03-23)

[Comment Deleted]

### ch...@gmail.com (2017-03-23)

Spoofing.

### rs...@chromium.org (2017-03-23)

Confirmed. Labeling as Low, since I don't quite see how an attacker would be able to make this too useful.

[Monorail components: Blink>Forms>Validation]

### ch...@gmail.com (2017-03-23)

[Comment Deleted]

### ch...@gmail.com (2017-03-23)

From https://crbug.com/chromium/673163.

### ch...@gmail.com (2017-03-23)

Kent - shouldn't be higher than low severity as https://crbug.com/chromium/673163?

### rs...@chromium.org (2017-03-23)

Prior art says yes. Thanks.

### tk...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

### tk...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a896ff44a395a50ab18f5120f20b7eb5a9550247

commit a896ff44a395a50ab18f5120f20b7eb5a9550247
Author: tkent <tkent@chromium.org>
Date: Mon Mar 27 03:47:21 2017

Form validation: Validation bubble should be closed on document unload process.

This CL fixes a bug that a validation bubble is not closed by page navigation in
some cases.

We close a validation message on Page::documentDetached(). However it seems it was
too late to communicate with the browser process in some cases. So, this CL moves
it to Document unload timing.

 * Add ValidationMessage::willUnloadDocument(), which closes a validation bubble,
  and Document::dispatchUnloadEvents() calls it indirectly through Page.

 * HTMLFormControlElement prevents from showing a validation message after the
  unload processing.

BUG=704560

Review-Url: https://codereview.chromium.org/2771193002
Cr-Commit-Position: refs/heads/master@{#459701}

[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/dom/DocumentTest.cpp
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/html/HTMLFormControlElement.cpp
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/core/page/ValidationMessageClient.h
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/web/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/a896ff44a395a50ab18f5120f20b7eb5a9550247/third_party/WebKit/Source/web/ValidationMessageClientImpl.h


### ch...@gmail.com (2017-03-27)

Fixed on 59.0.3053.0 Canary.

### tk...@chromium.org (2017-03-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-03-27)

+awhalley@ for M57/M58 merge review.

Please note we already cut M57 Stable RC for release this week. 

### aw...@google.com (2017-03-28)

Not taking this for M57, but good for M58 once it's been out on canary for 48 hours+

### sh...@chromium.org (2017-03-28)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0

commit 2bf11fe64e121ef8c9603d1b56e972b4800cc3c0
Author: Kent Tamura <tkent@chromium.org>
Date: Wed Mar 29 07:54:14 2017

Merge "Form validation: Validation bubble should be closed on document unload process." to M58

This CL fixes a bug that a validation bubble is not closed by page navigation in
some cases.

We close a validation message on Page::documentDetached(). However it seems it was
too late to communicate with the browser process in some cases. So, this CL moves
it to Document unload timing.

 * Add ValidationMessage::willUnloadDocument(), which closes a validation bubble,
  and Document::dispatchUnloadEvents() calls it indirectly through Page.

 * HTMLFormControlElement prevents from showing a validation message after the
  unload processing.

BUG=704560

Review-Url: https://codereview.chromium.org/2771193002
Cr-Commit-Position: refs/heads/master@{#459701}
(cherry picked from commit a896ff44a395a50ab18f5120f20b7eb5a9550247)

Review-Url: https://codereview.chromium.org/2782093003 .
Cr-Commit-Position: refs/branch-heads/3029@{#472}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/dom/DocumentTest.cpp
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/html/HTMLFormControlElement.cpp
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/core/page/ValidationMessageClient.h
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/web/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/2bf11fe64e121ef8c9603d1b56e972b4800cc3c0/third_party/WebKit/Source/web/ValidationMessageClientImpl.h


### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Nice one! The panel has decided to award $500 for this bug.

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/704560?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087137)*
