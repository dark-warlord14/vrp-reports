# Security: Permission request UI spoof 

| Field | Value |
|-------|-------|
| **Issue ID** | [40090595](https://issues.chromium.org/issues/40090595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2018-02-24 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 66.0.3353.0 
Operating System: Only on Windows

I believe this is similar to https://crbug.com/chromium/774438.

1. Set up a local webserver to host poc.html
2. Click on "Click here" button 
3. Observe the permission request stays open after navigation to another origin (with http://localhost wants to...)

## Attachments

- [Screen Shot 2018-02-24 at 16.03.46.png](attachments/Screen Shot 2018-02-24 at 16.03.46.png) (image/png, 124.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 314 B)

## Timeline

### el...@chromium.org (2018-02-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Permissions>Prompts]

### ra...@chromium.org (2018-02-26)

This repros on stable M64 on linux for me.

It looks like 2 requests are being queued in the PermissionBubbleMediaAccessHandler and the second one is still being run even after the navigation happens. I know there is logic to cancel media requests after a navigation happens so there must be a missing case somewhere. To be safe we should check that the origin of the request matches the origin of the current frame. We could put this check in MediaStreamDevicesController::RequestPermissions but it seems like we should investigate why the request isn't being properly cancelled first. 

guidou: could you ptal? 

### gu...@chromium.org (2018-02-26)

I'll look into this.

### gu...@chromium.org (2018-02-26)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### gu...@chromium.org (2018-02-27)

The issue is that MediaStreamManager is sending a cancellation request using  NUM_MEDIA_TYPES as stream type, which gets ignored by PermissionBubbleMediaAccessHandler.

https://chromium-review.googlesource.com/c/chromium/src/+/939630 should fix it.

AFAICT, this has always been broken, dating back to when the code was first added in 2013.


### gu...@chromium.org (2018-02-27)

Should we request merge to M65 once the fix for this lands?

### bu...@chromium.org (2018-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/12c876ae82355de6285bf0879023f1d1f1822ecf

commit 12c876ae82355de6285bf0879023f1d1f1822ecf
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Mar 01 10:47:37 2018

Fix MediaObserver notifications in MediaStreamManager.

This CL fixes the stream type used to notify MediaObserver about
cancelled MediaStream requests.

Before this CL, NUM_MEDIA_TYPES was used as stream type to indicate
that all stream types should be cancelled.
However, the MediaObserver end does not interpret NUM_MEDIA_TYPES this
way and the request to update the UI is ignored.

This CL sends a separate notification for each stream type so that the
UI actually gets updated for all stream types in use.

Bug: 816033
Change-Id: Ib7d3b3046d1dd0976627f8ab38abf086eacc9405
Reviewed-on: https://chromium-review.googlesource.com/939630
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Raymes Khoury <raymes@chromium.org>
Cr-Commit-Position: refs/heads/master@{#540122}
[modify] https://crrev.com/12c876ae82355de6285bf0879023f1d1f1822ecf/content/browser/renderer_host/media/media_stream_manager.cc
[modify] https://crrev.com/12c876ae82355de6285bf0879023f1d1f1822ecf/content/browser/renderer_host/media/media_stream_manager_unittest.cc


### gu...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### gu...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-13)

Thanks! $500 for this one :-)

### ch...@gmail.com (2018-03-13)

Nice reward! Thanks Andrew as ever :-)

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2018-03-16)

Note that this fix landed originally in M66, so it does not need to be merged there. 

### ab...@google.com (2018-03-19)

Merge approved 66. branch3359

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### gu...@chromium.org (2018-03-20)

This landed originally in M66, so no merge is necessary.

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/816033?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090595)*
