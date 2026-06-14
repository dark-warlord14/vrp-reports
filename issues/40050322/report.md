# CXFA_FFPageView Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40050322](https://issues.chromium.org/issues/40050322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-10-03 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15

Steps to reproduce the problem:
1.build pdfium with XFA
2. ./pdfium_test poc.pdf
3.

What is the expected behavior?

What went wrong?
CXFA_FFPageView as freed in CXFA_Document::ClearLayoutData()
and later was used in CXFA_LayoutItem::GetFormNode

ASAN output is attached in this report

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.14.6
Flash Version:

## Attachments

- [asan_poc.txt](attachments/asan_poc.txt) (text/plain, 20.1 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 5.1 KB)

## Timeline

### fs...@chromium.org (2019-10-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### mp...@google.com (2019-10-03)

Thanks for the report! Looks like outside of ASAN mode this would be a double free. Assigning to thestig@.

### do...@google.com (2019-10-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-04)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-17)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-17)

XFA is not shipped to users.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e

commit 7b8eb884cfd6da446798014671be54bc2fed305e
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 31 19:50:35 2020

Make all CXFA_FFWidget observe their CXFA_FFPageview.

Although a very blunt technique, the cost shouldn't be terrible in
memory given the size of the CXFA_FFWidget itself, and shouldn't be
terrible in runtime give the rarity of the notification case. Ideally,
future memory work would improve this situation, but this safely
adding more test cases at present to guard against regressions.

Bug: chromium:1042915, chromium:1010844
Change-Id: Idd02967a8297d3bce7d35451db9ae05f79cdf3ac
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65870
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/xfa/fxfa/cxfa_ffwidget.h
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915.pdf
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915.evt


### ts...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df6fd718399c5a2860b543cfa55f3c60a230c752

commit df6fd718399c5a2860b543cfa55f3c60a230c752
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jan 31 21:28:03 2020

Roll src/third_party/pdfium 62c4aa446733..7b8eb884cfd6 (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/62c4aa446733..7b8eb884cfd6

git log 62c4aa446733..7b8eb884cfd6 --date=short --first-parent --format='%ad %ae %s'
2020-01-31 tsepez@chromium.org Make all CXFA_FFWidget observe their CXFA_FFPageview.
2020-01-31 thestig@chromium.org Fix various build/include_order lint errors.
2020-01-31 thestig@chromium.org Give some .in test files better formatting.
2020-01-31 tsepez@chromium.org Remove dwCoordinatesType arg from GetPageMatrix().
2020-01-31 thestig@chromium.org Reduce the number of calls to HasPermissions().
2020-01-31 thestig@chromium.org Move permission constants to constants/access_permissions.h.
2020-01-31 dhoss@chromium.org Run tests with --disable-xfa in coverage_report.py

Created with:
  gclient setdep -r src/third_party/pdfium@7b8eb884cfd6

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1010844,chromium:1042915
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I6415f31dfba3a5156486c3f53cb14e64d455c30a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2033586
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#737460}

[modify] https://crrev.com/df6fd718399c5a2860b543cfa55f3c60a230c752/DEPS


### sh...@chromium.org (2020-02-01)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### ho...@gmail.com (2020-02-05)

hi natashapabrai@google.com  if I got reward, could you help me to change bank account to receive the reward 

### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $5,000 for this report! 

Someone from finance will be in touch shortly so you can claim your reward. 

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-02-20)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-09)

This issue was migrated from crbug.com/chromium/1010844?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1011648]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050322)*
