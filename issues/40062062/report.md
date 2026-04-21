# Security: CVE-2022-3970 was fixed in libtiff and published but not propagated to Pdfium yet

| Field | Value |
|-------|-------|
| **Issue ID** | [40062062](https://issues.chromium.org/issues/40062062) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-3970 |
| **Reporter** | ri...@sap.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-12-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

An integer overflow was reported in Chromium Bug report 53137 and fixed in libtiff on Nov 8, 2023.  

Bug Report: <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=53137>  

Fix: <https://gitlab.com/libtiff/libtiff/-/commit/a05860a0872d323e3fbf4390187ce934dd2b165e>.  

The Chromium bug report got closed and CVE-2022-3970 made public, but the fix did not land in Pdfium libtiff main branch so far, see: <https://pdfium.googlesource.com/pdfium/+/refs/heads/main/third_party/libtiff/tif_getimage.c>

**VERSION**  

The correction is not in Pdfium main branch yet.

**CREDIT INFORMATION**  

Credit information goes to the people involved in <https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=53137>. I (Richard Lorenz from SAP) just noticed it in our open source scans, because we integrated Chromium Embedded Framework within SAP Business Client.

Best regards,  

Richard

## Timeline

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-06)

Thanks. It appears that there's a problem with how our libtiff metadata was tracked, so it seems that indeed this fix hasn't been aborbed. The impact of this CVE on ChromeOS is tracked in https://crbug.com/chromium/1386095 but there is no such tracking issue for Chrome browser.

As this is publicly disclosed, I feel this needs to be Pri-0 and we should distribute a fix within 7 days. Tom, could you take care of this?

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-12-06)

The code is behind chrome://flag entry which isn't on by default, so is this still a P0?

Looking at the libtiff metadata, we have "CPEPrefix: cpe:/a:libtiff:libtiff:4.2.0" in PDFium's third_party/libtiff/README.pdfium. Are PDFium's sources being scanned? I landed cl/471011910 a while back to help with that process.

### [Deleted User] (2022-12-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-12-06)

I can also just do the cherry-pick.

### th...@chromium.org (2022-12-06)

https://pdfium-review.googlesource.com/102171

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0a2b8101b153e1574a09fcdbaebc16bea9544d3c

commit 0a2b8101b153e1574a09fcdbaebc16bea9544d3c
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Dec 06 21:26:24 2022

Cherry-pick libtiff TIFFReadRGBATileExt() fix.

Fixes https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=53137

Bug: chromium:1396254
Change-Id: I23bb1b4ab2cf3e89e93f1208bb2c6e8ea348ae04
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/102171
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/0a2b8101b153e1574a09fcdbaebc16bea9544d3c/third_party/libtiff/tif_getimage.c
[add] https://pdfium.googlesource.com/pdfium/+/0a2b8101b153e1574a09fcdbaebc16bea9544d3c/third_party/libtiff/0037-tiff-read-rgba-tile-ext.patch
[modify] https://pdfium.googlesource.com/pdfium/+/0a2b8101b153e1574a09fcdbaebc16bea9544d3c/third_party/libtiff/README.pdfium


### am...@chromium.org (2022-12-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-06)

Updating as fixed since the CP has been performed and to get this in the merge review queue. 
If not already done, please get this rolled and onto Canary at soonest. We should get this fix into the next week's M108 stable refresh release, so the merge deadline will is going to be 10am Pacific on Friday in order to do that. Thanks! 

### th...@chromium.org (2022-12-06)

DEPS roll is in progress in https://crrev.com/c/4083633

### th...@chromium.org (2022-12-06)

We should be able to get this in before the Friday merge deadline. We probably also have a M109 merge to do.

### am...@chromium.org (2022-12-06)

yep - thank you !The bot should add the merge review labels for both M109 and M108 by tomorrow am. 

### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/402fc8888793781c137a3592b6d08b3a983d5bbe

commit 402fc8888793781c137a3592b6d08b3a983d5bbe
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Dec 07 00:11:44 2022

Roll PDFium from 1aa642da9036 to 69d11eaac7e4 (10 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/1aa642da9036..69d11eaac7e4

2022-12-06 thestig@chromium.org Remove pdf_use_cxx20_override.
2022-12-06 thestig@chromium.org Cherry-pick libtiff TIFFReadRGBATileExt() fix.
2022-12-06 thestig@chromium.org Roll v8/ 248e6317f..24bde5401 (131 commits)
2022-12-06 thestig@chromium.org Roll third_party/instrumented_libraries/ a8992bf8a..87467200f (3 commits)
2022-12-06 nigi@chromium.org [Skia] Add a pixel test of 1-bpp and 8-bpp images
2022-12-06 thestig@chromium.org Roll DEPS for buildtools and libc++.
2022-12-05 thestig@chromium.org Roll base/allocator/partition_allocator/ 9f2740129..d84273fde (17 commits)
2022-12-05 thestig@chromium.org Add option for building with C++20 and roll DEPS for Abseil.
2022-12-05 thestig@chromium.org Roll tools/clang/ 2991b63fa..65848dccd (15 commits)
2022-12-05 thestig@chromium.org Roll build/ 4b87ced7d..2748ef76c (115 commits)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1383708,chromium:1396254
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I500f5b86de976b1b1a07f819778982056cac4dae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4083633
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1080066}

[modify] https://crrev.com/402fc8888793781c137a3592b6d08b3a983d5bbe/DEPS


### ad...@google.com (2022-12-07)

thestig@ thanks for jumping on this!

> The code is behind chrome://flag entry which isn't on by default, so is this still a P0?

No, it isn't then. I've reclassified as Security_Impact-None and there's no huge urgency. Unfortunately I didn't see your comment until this morning by which time you'd done all this frantic activity.

> Looking at the libtiff metadata, we have "CPEPrefix: cpe:/a:libtiff:libtiff:4.2.0" in PDFium's third_party/libtiff/README.pdfium. Are PDFium's sources being scanned? I landed cl/471011910 a while back to help with that process.

I don't know why Vomit didn't tell us about this. I started an email thread yesterday with the Vomit scanner folks, but I hadn't realized you'd done this CL, I've added you to the thread.

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Thank you for this report, Richard! The VRP Panel has decided to award you $1,000 as a thank you for the heads-up so we could get these libtiff fixes into Chromium. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### ri...@sap.com (2022-12-18)

Hi Amy,
Thank you very much. It was just our OSS scan, which gave the alert.
Best regards,
Richard

### [Deleted User] (2023-03-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1396254?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062062)*
