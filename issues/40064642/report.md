# Security: Bypass Of 1342072

| Field | Value |
|-------|-------|
| **Issue ID** | [40064642](https://issues.chromium.org/issues/40064642) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>PresentationAPI, UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Mac, Windows |
| **Reporter** | ia...@gmail.com |
| **Assignee** | ah...@google.com |
| **Created** | 2023-05-18 |
| **Bounty** | $2,000.00 |

## Description

For me its a bypass of 1342072, please do let me know what you think about this.
Detailed information is attached.

Please let me know if or correct me If I am wrong somewhere.

Tested On Mac Ventura 13.1
Version 113.0.5672.126 (Official Build) (arm64)

I have also attached screenshot of Opera, Edge for information that how they behave from this vulnerability.

## Attachments

- [Bypass.txt](attachments/Bypass.txt) (text/plain, 3.3 KB)
- [chrome_cross.html.png](attachments/chrome_cross.html.png) (image/png, 492.3 KB)
- [chrome_cross2.html.png](attachments/chrome_cross2.html.png) (image/png, 506.3 KB)
- [opera_cross.html.png](attachments/opera_cross.html.png) (image/png, 523.4 KB)
- [opera_cross2.html.png](attachments/opera_cross2.html.png) (image/png, 537.6 KB)
- [edge_cross.html.png](attachments/edge_cross.html.png) (image/png, 473.7 KB)
- [Bypass.txt](attachments/Bypass.txt) (text/plain, 3.9 KB)

## Timeline

### ia...@gmail.com (2023-05-18)

Details available in Bypass.txt attached.

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>PresentationAPI]

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-19)

Hi creis@, I have not reproduced this on my local machine yet, but I am sending this bug to you and ahmedmoussa@ on this issue as the reporter looks to have found a bypass for the fix done in https://bugs.chromium.org/p/chromium/issues/detail?id=1342072. Please let me know if this report looks valid! Thank you.

### cr...@chromium.org (2023-05-19)

This looks like a URL eliding question at first glance, where long URLs aren't being displayed in a safe way.  I'm not sure if that's considered medium or low.  I believe the guide for that is here:
https://chromium.googlesource.com/chromium/src/+/main/docs/security/url_display_guidelines/url_display_guidelines.md#Eliding-URLs

ahmedmoussa@: Can you take a look?
meacer@: Can you help confirm the severity?

[Monorail components: UI>Security>UrlFormatting]

### an...@chromium.org (2023-05-20)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-05-20)

@creis - This report is regarding URL Eliding! If you the screenshots of Chrome and Opera, its doable for some one to spoof the URL and looks very convincing from user prospective.

### [Deleted User] (2023-05-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a

commit a01e3d760b3b51cdcfe56a327619a3bdcfb8811a
Author: ahmedmoussa <ahmedmoussa@google.com>
Date: Thu May 25 19:48:26 2023

Fix issues MirroringType::kOffscreenTab

1) Zenith dialog is not shown after cast session starts, in case of `MirroringType::kOffscreenTab`. The cause was that ShouldHideNotification() returns true.

2) Casting PresentationRequest (i.e. MirroringType::kOffscreenTab), cause chrome to crash upon trying to stop casting.

3) URL shown as title in Zenith is tailed elided which might cause url spoofing.

Bug: 1446754
Change-Id: I771434cbeed2a69b2f783546945ac7311ac81ea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4559072
Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1149311}

[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/components/media_message_center/media_notification_view_modern_impl.cc
[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/chrome/browser/media/cast_mirroring_service_host.h
[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/chrome/browser/ui/global_media_controls/cast_media_notification_producer_unittest.cc
[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/chrome/browser/ui/global_media_controls/cast_media_notification_producer.cc
[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/components/media_message_center/media_notification_view_ash_impl.cc
[modify] https://crrev.com/a01e3d760b3b51cdcfe56a327619a3bdcfb8811a/components/media_message_center/media_notification_view_impl.cc


### ia...@gmail.com (2023-05-27)

Can we also mark "Window" tag as well in affected component just for references.

### cr...@chromium.org (2023-05-30)

Adding Windows per https://crbug.com/chromium/1446754#c12.

ahmedmoussa@: Thanks for landing r1149311!  Should this be marked fixed now, or is another CL needed?

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ah...@google.com (2023-05-30)

It is fixed. But I am requesting for the fix to be merged into M115.

### [Deleted User] (2023-05-30)

Merge approved: your change passed merge requirements and is auto-approved for M115. Please go ahead and merge the CL to branch 5790 (refs/branch-heads/5790) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-05-30)

Please mark bugs as fixed (fixed=work completed on main, needs verification and merges (if applicable)) once a fix has landed. This allows our automation to come and take care of the merge request and other labels necessary for our processes :D

### am...@chromium.org (2023-05-30)

Also, please do not removed M- and Target- labels on security issues as these are relevant to security automation. TY 

### ah...@google.com (2023-05-30)

Got it, thanks.

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/128d8006c125f003a006bbe15b36b98e1a2eca26

commit 128d8006c125f003a006bbe15b36b98e1a2eca26
Author: ahmedmoussa <ahmedmoussa@google.com>
Date: Thu Jun 01 02:24:18 2023

Fix issues MirroringType::kOffscreenTab

1) Zenith dialog is not shown after cast session starts, in case of `MirroringType::kOffscreenTab`. The cause was that ShouldHideNotification() returns true.

2) Casting PresentationRequest (i.e. MirroringType::kOffscreenTab), cause chrome to crash upon trying to stop casting.

3) URL shown as title in Zenith is tailed elided which might cause url spoofing.

(cherry picked from commit a01e3d760b3b51cdcfe56a327619a3bdcfb8811a)

Bug: 1446754
Change-Id: I771434cbeed2a69b2f783546945ac7311ac81ea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4559072
Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1149311}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4575049
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#207}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/components/media_message_center/media_notification_view_modern_impl.cc
[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/chrome/browser/media/cast_mirroring_service_host.h
[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/chrome/browser/ui/global_media_controls/cast_media_notification_producer.cc
[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/chrome/browser/ui/global_media_controls/cast_media_notification_producer_unittest.cc
[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/components/media_message_center/media_notification_view_ash_impl.cc
[modify] https://crrev.com/128d8006c125f003a006bbe15b36b98e1a2eca26/components/media_message_center/media_notification_view_impl.cc


### ah...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of the URL elision issue. Thank you for your effort and reporting this issue to us! 

### ia...@gmail.com (2023-06-09)

Thank you team :)

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hello! We consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), so I've undeleted them. Thanks! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1446754?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PresentationAPI, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/1452056]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064642)*
