# UAF in PDFium due to incorrect ref count

| Field | Value |
|-------|-------|
| **Issue ID** | [40095638](https://issues.chromium.org/issues/40095638) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-07-08 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36

Steps to reproduce the problem:
1.
2.
3.

What is the expected behavior?

What went wrong?
...

Did this work before? N/A 

Chrome version: 75.0.3770.100  Channel: stable
OS Version: OS X 10.13.4
Flash Version:

## Timeline

### zh...@gmail.com (2019-07-08)

[Comment Deleted]

### li...@chromium.org (2019-07-08)

Thanks for your report! We'll need some more details to be able to investigate this bug. Could you please provide repro instructions and give us an idea of what's going wrong? Thanks!

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2019-07-08)

See https://crbug.com/chromium/835667 for a prior example where offered a reward for a bug in PDFium's Skia code.

### zh...@gmail.com (2019-07-09)

[Comment Deleted]

### sh...@chromium.org (2019-07-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2019-07-09)

Thanks for the report!

### pa...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-07-09)

I think https://crbug.com/chromium/981785#c4 just says ankk's commit is the version being tested. That particular commit has nothing to do with Skia.

### pa...@chromium.org (2019-07-09)

Do we think this bug is inside Skia, or due to how PDFium (possibly that patch) calls it?

### th...@chromium.org (2019-07-09)

CCing folks interested in PDFium + Skia. It looks like this regressed. I'm bisecting.

### th...@chromium.org (2019-07-09)

re: https://crbug.com/chromium/981785#c9 - probably a bug in PDFium's Skia usage. Flipping |m_debugDisable| in SkiaState (to disable a cache mechanism) makes the bug go away.

Bisected to https://pdfium-review.googlesource.com/53831, but it's not obvious if the CL has lifetime issues, or it's just triggering better rendering, which then allows this bug to manifest. Given the CL didn't cause any problem on the AGG side, I'm leaning towards the latter.

### th...@chromium.org (2019-07-09)

https://pdfium-review.googlesource.com/57491

### zh...@gmail.com (2019-07-10)

[Comment Deleted]

### zh...@gmail.com (2019-07-11)

[Comment Deleted]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/68fb145dca2b0d41acb00e9c16fc5032a1a980e0

commit 68fb145dca2b0d41acb00e9c16fc5032a1a980e0
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jul 16 20:22:55 2019

Use refcounting for |SkiaState::m_pTypeFace|.

Otherwise the CFX_TypeFace object SkiaState points to may get destroyed
to create a dangling pointer.

Bug: chromium:981785
Change-Id: I5ea2402d9d5320f266b7eb5b48b9eb16e5170278
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57491
Reviewed-by: Mike Reed <reed@google.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/68fb145dca2b0d41acb00e9c16fc5032a1a980e0/core/fxge/skia/fx_skia_device.cpp


### th...@chromium.org (2019-07-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/90c936c1a44917534bd275dffb94c01f450c44a0

commit 90c936c1a44917534bd275dffb94c01f450c44a0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jul 17 03:18:37 2019

Roll src/third_party/pdfium 22923602f40e..68fb145dca2b (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/22923602f40e..68fb145dca2b


git log 22923602f40e..68fb145dca2b --date=short --no-merges --format='%ad %ae %s'
2019-07-16 thestig@chromium.org Use refcounting for |SkiaState::m_pTypeFace|.
2019-07-16 thestig@chromium.org Roll third_party/skia/ 34d63e6b4..8590026db (479 commits; 75 trivial rolls)
2019-07-16 manojb@microsoft.com Add tests for FPDFLink_Enumerate() and friends
2019-07-16 thestig@chromium.org Include all SkSL sources when building Skia.
2019-07-16 thestig@chromium.org Remove dead code in CPDFSDK_ActionHandler.


Created with:
  gclient setdep -r src/third_party/pdfium@68fb145dca2b

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:981785
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I41fe746d057a10d2ce564ca0099dab264305082a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1705400
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#678109}

[modify] https://crrev.com/90c936c1a44917534bd275dffb94c01f450c44a0/DEPS


### sh...@chromium.org (2019-07-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $3,000 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### zh...@gmail.com (2019-07-31)

[Comment Deleted]

### ad...@chromium.org (2019-08-01)

Hi zhouat2017@, as this doesn't affect production code we wouldn't expect to mention this in the release notes.

### na...@google.com (2019-08-14)

Hi zhouat2017 - the Panel declined to reward this as a high quality report and would be more likely to believe that the exploitation was more likely if a pdf file were provided without requiring a patch 

### na...@google.com (2019-08-14)

Hi zhouat2017 - the Panel declined to reward this as a high quality report and would be more likely to believe that the exploitation was more likely if a pdf file were provided without requiring a patch 

### sh...@chromium.org (2019-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-23)

This issue was migrated from crbug.com/chromium/981785?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095638)*
