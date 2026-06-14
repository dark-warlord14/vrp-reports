# pdfium XFA CXFA_FFDocView::RunSubformIndexChange Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40094055](https://issues.chromium.org/issues/40094055) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-02-16 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15

Steps to reproduce the problem:
1. pdfium with XFA build , ASAN enable
2. ./pdfium_test 5db68c09ecaba144679862bb220ba4ae.pdf
3. 

What is the expected behavior?

What went wrong?
Attacker can run script from indexChange event which make ** m_IndexChangedSubforms** vector reallocate => Use after free

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.14.3
Flash Version:

## Attachments

- [5db68c09ecaba144679862bb220ba4ae.pdf](attachments/5db68c09ecaba144679862bb220ba4ae.pdf) (application/pdf, 3.1 KB)
- [asan_5db68c09ecaba144679862bb220ba4ae](attachments/asan_5db68c09ecaba144679862bb220ba4ae) (text/plain, 18.8 KB)

## Timeline

### me...@chromium.org (2019-02-18)

Thanks for the report.

Tom,  can you PTAL?

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2019-02-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4898647483482112.

### cl...@chromium.org (2019-02-19)

Testcase 4898647483482112 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4898647483482112.

### sh...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-02-20)

Not RBS since it is XFA.

### th...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-10)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b9516868546eef446d961fed199f985c3aa923ec

commit b9516868546eef446d961fed199f985c3aa923ec
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Apr 10 20:48:49 2019

Convert |CXFA_FFDocView::m_IndexChangedSubforms| to a deque.

Pop off items one at a time to safely iterate through it. Add a set to
keep track of seen notes to prevent infinite loops.

BUG=chromium:932900

Change-Id: I74eb29262e8ba29097638f7103ef427799a06fc5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/52971
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/b9516868546eef446d961fed199f985c3aa923ec/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://crrev.com/b9516868546eef446d961fed199f985c3aa923ec/xfa/fxfa/cxfa_ffdocview.h


### th...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0fd07109ffd224c579307e686e263db4b127805

commit f0fd07109ffd224c579307e686e263db4b127805
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 10 22:04:41 2019

Roll src/third_party/pdfium 44034bca7d3e..b9516868546e (9 commits)

https://pdfium.googlesource.com/pdfium.git/+log/44034bca7d3e..b9516868546e


git log 44034bca7d3e..b9516868546e --date=short --no-merges --format='%ad %ae %s'
2019-04-10 thestig@chromium.org Convert |CXFA_FFDocView::m_IndexChangedSubforms| to a deque.
2019-04-10 thestig@chromium.org Add a test to exercise FPDF_FFLDraw() with FPDF_REVERSE_BYTE_ORDER.
2019-04-10 tsepez@chromium.org Separate CXFA_FFWidget from CXFA_ContentLayoutItem.
2019-04-10 thestig@chromium.org Use early returns in CXFA_Node.
2019-04-10 thestig@chromium.org Give CXFA_FFDocView* params proper names in CXFA_Node.
2019-04-10 thestig@chromium.org Return Optional<float> from CXFA_Node::FindSplitPos().
2019-04-10 thestig@chromium.org Add CXFA_LayoutPageMgr::ShouldGetNextPageArea().
2019-04-10 thestig@chromium.org Add CXFA_LayoutPageMgr::HasCurrentViewRecord().
2019-04-10 thestig@chromium.org Prevent an out of bound access in CXFA_TextLayout::DoLayout().


Created with:
  gclient setdep -r src/third_party/pdfium@b9516868546e

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:932900,chromium:925788
TBR=dsinclair@chromium.org

Change-Id: I368f5bf1b393923a8002ecab848b75b702eb16b3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1562493
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#649672}
[modify] https://crrev.com/f0fd07109ffd224c579307e686e263db4b127805/DEPS


### sh...@chromium.org (2019-04-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-04-18)

Congrats! The Panel decided to reward $3,000 for this report!

### aw...@google.com (2019-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/932900?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094055)*
