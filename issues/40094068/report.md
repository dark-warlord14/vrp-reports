# pdfium XFA CXFA_FFDocView::RunValidate Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40094068](https://issues.chromium.org/issues/40094068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-02-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15

Steps to reproduce the problem:
1. pdfium with XFA enabled, ASAN enabled
2. ./pdfium_test e8d01dca9386e3b17078653bdd0c952e.pdf
3. 

What is the expected behavior?

What went wrong?
m_ValidateNodes can be reallocated after run validate event => use after free

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.14.3
Flash Version:

## Attachments

- [e8d01dca9386e3b17078653bdd0c952e.pdf](attachments/e8d01dca9386e3b17078653bdd0c952e.pdf) (application/pdf, 4.1 KB)
- [asan_e8d01dca9386e3b17078653bdd0c952e](attachments/asan_e8d01dca9386e3b17078653bdd0c952e) (text/plain, 18.3 KB)

## Timeline

### me...@chromium.org (2019-02-19)

Tom, can you please take a look? I'm assuming this impacts stable channel.

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-02-20)

XFA-only.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7f7405ec47e9ca045d6bf391a05a423e5f1338e9

commit 7f7405ec47e9ca045d6bf391a05a423e5f1338e9
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Apr 08 18:21:21 2019

Move |CXFA_FFDocView::m_ValidateNodes| before iterating over it.

Similar issue to the one fixed in commit 12eacc8a.

BUG=chromium:933163

Change-Id: I7e79dd27a5ebbaceaa0db0604c28520b24a8d7f6
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/52832
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/7f7405ec47e9ca045d6bf391a05a423e5f1338e9/xfa/fxfa/cxfa_ffdocview.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4ed059978e234029109bfd43eacb7fcafaff7eff

commit 4ed059978e234029109bfd43eacb7fcafaff7eff
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Apr 08 20:36:11 2019

Roll src/third_party/pdfium 3419af426bd5..7f7405ec47e9 (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/3419af426bd5..7f7405ec47e9


git log 3419af426bd5..7f7405ec47e9 --date=short --no-merges --format='%ad %ae %s'
2019-04-08 thestig@chromium.org Move |CXFA_FFDocView::m_ValidateNodes| before iterating over it.
2019-04-08 thestig@chromium.org Give buffers in experimental fpdf_annot.h APIs clearer types.
2019-04-08 thestig@chromium.org Introduce ScopedFPDFWideString for use in tests.
2019-04-08 thestig@chromium.org Fix nits in fpdf_annot_embeddertest.cpp.


Created with:
  gclient setdep -r src/third_party/pdfium@7f7405ec47e9

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:933163
TBR=dsinclair@chromium.org

Change-Id: I7420e66a573b31bbb45486b9181b4aa4c24852a0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1556344
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#648844}
[modify] https://crrev.com/4ed059978e234029109bfd43eacb7fcafaff7eff/DEPS


### th...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $3,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/933163?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094068)*
