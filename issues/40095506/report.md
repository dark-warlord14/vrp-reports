# Security: PDFium (XFA) Use-after-free in CXFA_FFWidget::OnSetFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40095506](https://issues.chromium.org/issues/40095506) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-06-25 |
| **Bounty** | $3,000.00 |

## Description


Steps to reproduce the problem:
1. Compile the latest chromium with enabled XFA PDFium
2. Open file test.pdf with chrome
3. 

What is the expected behavior?

What went wrong?
xfa.host.setFocus() triggers use-after-free CXFA_FFExclGroup object in CXFA_FFWidget::OnSetFocus

Did this work before? N/A 

Chrome version: Lasted  Channel: n/a
OS Version: Windows 10 64bit
Flash Version:

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 226.2 KB)
- [crash_log.txt](attachments/crash_log.txt) (text/plain, 28.2 KB)

## Timeline

### cl...@chromium.org (2019-06-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5203150277050368.

### cl...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-26)

Testcase 5203150277050368 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5203150277050368.

### cl...@chromium.org (2019-06-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4826307564797952.

### cl...@chromium.org (2019-06-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-06-26)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/22ae151e6d0d72e178f616c986460efffa6b6a99 (Separate CXFA_FFWidget from CXFA_ContentLayoutItem.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-06-26)

Detailed report: https://clusterfuzz.com/testcase?key=4826307564797952

Fuzzer: libFuzzer_pdfium_xfa_fuzzer
Fuzz target binary: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000021c88
Crash State:
  fxcrt::UnownedPtr<CXFA_ContentLayoutItem>::Get
  CXFA_FFWidget::OnSetFocus
  CXFA_FFField::OnSetFocus
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=649670:649678

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4826307564797952

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7d6ec19df654383bcdf418b2d8fc8da47400ae38

commit 7d6ec19df654383bcdf418b2d8fc8da47400ae38
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 02 19:13:21 2019

Observe CXFA_FFWidgets across OnSetFocus() events.

Although ObservedPtrs are computationally expensive, the
distance between the free and the stale pointer includes a round
trip through JS and back to C++, so returning status through all
the intervening layers would be cumbersome.

Bug: chromium:978575
Change-Id: Id4dcb40fab3bddb9ede58b986569c7cfa91c4b87
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/57110
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/7d6ec19df654383bcdf418b2d8fc8da47400ae38/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://crrev.com/7d6ec19df654383bcdf418b2d8fc8da47400ae38/xfa/fxfa/cxfa_fffield.cpp
[modify] https://crrev.com/7d6ec19df654383bcdf418b2d8fc8da47400ae38/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://crrev.com/7d6ec19df654383bcdf418b2d8fc8da47400ae38/xfa/fxfa/cxfa_ffwidget.h


### ts...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/920ac098c39ed3d76e111c158f22f4cab56750ff

commit 920ac098c39ed3d76e111c158f22f4cab56750ff
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jul 02 20:58:16 2019

Roll src/third_party/pdfium 0088ed08355e..815726bc4c69 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/0088ed08355e..815726bc4c69


git log 0088ed08355e..815726bc4c69 --date=short --no-merges --format='%ad %ae %s'
2019-07-02 tsepez@chromium.org Fold CXFA_LayoutContext into CXFA_ContentLayoutProcessor.
2019-07-02 tsepez@chromium.org Observe CXFA_FFWidgets across OnSetFocus() events.
2019-07-02 tsepez@chromium.org Rename CXFA_LayoutPageMgr to CXFA_ViewLayoutProcessor


Created with:
  gclient setdep -r src/third_party/pdfium@815726bc4c69

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:978575
TBR=pdfium-deps-rolls@chromium.org

Change-Id: I2b8c15ee58a804a7af0d688d3f1d0c21d1b3c202
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1685426
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#674211}

[modify] https://crrev.com/920ac098c39ed3d76e111c158f22f4cab56750ff/DEPS


### sh...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-03)

ClusterFuzz testcase 4826307564797952 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=674195:674215

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report! Please let us know how you would like to be credited on our release notes

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### my...@gmail.com (2019-08-01)

Thank you for the reward, I would like to be credited as "tictactoe" if possible.

### sh...@chromium.org (2019-10-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/978575?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095506)*
