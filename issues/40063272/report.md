# Security: PDFium UAF vulns

| Field | Value |
|-------|-------|
| **Issue ID** | [40063272](https://issues.chromium.org/issues/40063272) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@ncsc.gov.uk |
| **Assignee** | ts...@chromium.org |
| **Created** | 2023-02-27 |
| **Bounty** | $7,000.00 |

## Description

Please find attached report.

Please acknowledge receipt.

Thank you.

## Attachments

- [23011101-disclosure-report.pdf](attachments/23011101-disclosure-report.pdf) (application/pdf, 583.9 KB)
- [bug_1419831.in](attachments/bug_1419831.in) (application/octet-stream, 678 B)
- [bug_1419831.evt](attachments/bug_1419831.evt) (application/octet-stream, 62 B)

## Timeline

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-27)

Thanks for the report, do you also have test cases to trigger the issues?

I'm setting the labels based on the report for now, but since there's no reproducer, I couldn't verify if it's correct.

tsepez@, I saw you handled lots of pdfium vulnerabilities in the past. Would you be a good owner for this?

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-02-27)

FYI, XFA support is enabled at build time, but not enabled by default at runtime.

### ts...@chromium.org (2023-03-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/63e3719f1ec20ee6db804b2b2d4b00680db18d9c

commit 63e3719f1ec20ee6db804b2b2d4b00680db18d9c
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 07 16:04:24 2023

Observe CPWL_* object destruction across CPDFSDK_Widget methods

This is a simple fix to stop the symptoms while we investigate
how to avoid mutations at these points in the first place.

-- fix some nearby braces and annoying blank lines while at it.

Bug: chromium:1419831
Change-Id: I20c38806b91c7c0c9016bb1b567a04ce319243d8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104397
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/63e3719f1ec20ee6db804b2b2d4b00680db18d9c/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/63e3719f1ec20ee6db804b2b2d4b00680db18d9c/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/63e3719f1ec20ee6db804b2b2d4b00680db18d9c/fpdfsdk/formfiller/cffl_checkbox.cpp


### ts...@chromium.org (2023-03-07)

+Amy - We'll want to merge this but I want to keep the bug open a bit to do variants, test cases, etc. 

### ts...@chromium.org (2023-03-07)

Here's a test case -- while it doesn't trigger the UaF, it shows the mis-interpreation of ()s when used as an XFA name when the PDF widget is clicked upon.

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3567e644c70c1e2b67c142ad6f1f3d480da14781

commit 3567e644c70c1e2b67c142ad6f1f3d480da14781
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Mar 07 22:13:53 2023

Roll PDFium from 168173ce12c6 to fbd5dcdc49cc (12 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/168173ce12c6..fbd5dcdc49cc

2023-03-07 andyphan@chromium.org Support indirect objects for /Filter arrays
2023-03-07 szager@chromium.org Make CXFA_FFPageWidgetIterator CPPGC_STACK_ALLOCATED
2023-03-07 thestig@chromium.org Simplify CPDF_StreamContentParser::Handle_SetFont()
2023-03-07 thestig@chromium.org Roll buildtools/third_party/libc++abi/trunk/ b74d77161..cff1f2def (9 commits)
2023-03-07 thestig@chromium.org Roll buildtools and libc++
2023-03-07 tsepez@chromium.org Observe CPWL_* object destruction across CPDFSDK_Widget methods
2023-03-07 thestig@chromium.org Roll buildtools/third_party/libunwind/trunk/ e95b94b74..7b03cc568 (10 commits)
2023-03-07 thestig@chromium.org Update resultdb_version to git_revision:ebc74d10fa0d64057daa6f128e89f3672eeeec95
2023-03-07 kmoon@chromium.org [Skia] Eagerly flush text
2023-03-07 kmoon@chromium.org [Skia] Eagerly flush paths
2023-03-06 szager@chromium.org Move CXFA_EventParam::m_pTarget into CFXJSE_Engine
2023-03-06 kmoon@chromium.org Regenerate Skia expectation for bug_1963.in

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1419831,chromium:1421576
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I97339c1feeef9969f0f9c17b333aef95bdac2828
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4317168
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1114213}

[modify] https://crrev.com/3567e644c70c1e2b67c142ad6f1f3d480da14781/DEPS


### ts...@chromium.org (2023-03-07)

Confirmed the example in c9 requires the XFA feature to be explicitly enabled.

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8a87da2cf76cdfd1539e30f43ff1add9163a2c1a

commit 8a87da2cf76cdfd1539e30f43ff1add9163a2c1a
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 07 22:42:23 2023

More tightly validate XML names in CXFA_FFDocView::GetWidgetByName()

Widget names must conform to XML name rules.

-- Beef up tests while at it.

Fixed: chromium:1419831
Change-Id: Id36b4a7b3d84aa0b74d54c91eed2f1a11da8298f
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104511
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/8a87da2cf76cdfd1539e30f43ff1add9163a2c1a/xfa/fxfa/cxfa_ffdocview.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8a87da2cf76cdfd1539e30f43ff1add9163a2c1a/core/fxcrt/xml/cfx_xmlparser_unittest.cpp


### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

Requesting merge to extended stable M110 because latest trunk commit (1114213) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1114213) appears to be after stable branch point (1097615).

Requesting merge to dev M112 because latest trunk commit (1114213) appears to be after dev branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-09)

Requesting merge to extended stable M110 because latest trunk commit (1114213) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1114213) appears to be after stable branch point (1097615).

Requesting merge to dev M112 because latest trunk commit (1114213) appears to be after dev branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-10)

Requesting merge to extended stable M110 because latest trunk commit (1114213) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1114213) appears to be after stable branch point (1097615).

Requesting merge to beta M112 because latest trunk commit (1114213) appears to be after beta branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-12)

Requesting merge to extended stable M110 because latest trunk commit (1114213) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1114213) appears to be after stable branch point (1097615).

Requesting merge to beta M112 because latest trunk commit (1114213) appears to be after beta branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-13)

Requesting merge to extended stable M110 because latest trunk commit (1114213) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1114213) appears to be after stable branch point (1097615).

Requesting merge to beta M112 because latest trunk commit (1114213) appears to be after beta branch point (1109224).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111, 112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-14)

Hi Tom, I reviewed the following individual CLs for merge: 
https://pdfium-review.googlesource.com/c/pdfium/+/104397
https://pdfium-review.googlesource.com/c/pdfium/+/104511

The gitwatcher did not tag the pdfium roll the second CL was part of, so please confirm there are no issues or concerns with that roll/group being backmerged. 
Otherwise, please go ahead and merge both fixes to branch 5615 as soon as possible so they can be included in the next M112/beta on Wednesday. 

Please merge to branches 5563 and 5481 so these fixes can be included in next M111/Stable and M110/Extended. 

### sr...@google.com (2023-03-14)

This issue has been approved for a merge to M112, I am cutting Beta RC build for M112 today afternoon around 3pm PST, please help complete all the merges to M112 today asap so the changes can be included into beta release and can get more beta channel coverage.

### ts...@chromium.org (2023-03-14)

To minimize disruption, I think we only need the first CL to be safe. The second one is a defense in depth.

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4090d4c0f9873f5f50b630c26c2439b5297a6e49

commit 4090d4c0f9873f5f50b630c26c2439b5297a6e49
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 14 20:07:27 2023

M112: Observe CPWL_* object destruction across CPDFSDK_Widget methods

This is a simple fix to stop the symptoms while we investigate
how to avoid mutations at these points in the first place.

-- fix some nearby braces and annoying blank lines while at it.

Bug: chromium:1419831
Change-Id: I20c38806b91c7c0c9016bb1b567a04ce319243d8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104397
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 63e3719f1ec20ee6db804b2b2d4b00680db18d9c)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104831
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/4090d4c0f9873f5f50b630c26c2439b5297a6e49/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/4090d4c0f9873f5f50b630c26c2439b5297a6e49/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/4090d4c0f9873f5f50b630c26c2439b5297a6e49/fpdfsdk/formfiller/cffl_checkbox.cpp


### [Deleted User] (2023-03-14)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/05a0a80e52ce088473e4998636b2f61a2cb35e41

commit 05a0a80e52ce088473e4998636b2f61a2cb35e41
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 14 21:12:06 2023

M111: Observe CPWL_* object destruction across CPDFSDK_Widget methods

This is a simple fix to stop the symptoms while we investigate
how to avoid mutations at these points in the first place.

-- fix some nearby braces and annoying blank lines while at it.

Bug: chromium:1419831
Change-Id: I20c38806b91c7c0c9016bb1b567a04ce319243d8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104397
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 63e3719f1ec20ee6db804b2b2d4b00680db18d9c)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104832
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/05a0a80e52ce088473e4998636b2f61a2cb35e41/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/05a0a80e52ce088473e4998636b2f61a2cb35e41/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/05a0a80e52ce088473e4998636b2f61a2cb35e41/fpdfsdk/formfiller/cffl_checkbox.cpp


### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a0d16d18d072ce77e639a09ed211340a2ad9034e

commit a0d16d18d072ce77e639a09ed211340a2ad9034e
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 14 21:18:45 2023

M110: Observe CPWL_* object destruction across CPDFSDK_Widget methods

This is a simple fix to stop the symptoms while we investigate
how to avoid mutations at these points in the first place.

-- fix some nearby braces and annoying blank lines while at it.

Bug: chromium:1419831
Change-Id: I20c38806b91c7c0c9016bb1b567a04ce319243d8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104397
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 63e3719f1ec20ee6db804b2b2d4b00680db18d9c)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104833
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a0d16d18d072ce77e639a09ed211340a2ad9034e/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a0d16d18d072ce77e639a09ed211340a2ad9034e/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a0d16d18d072ce77e639a09ed211340a2ad9034e/fpdfsdk/formfiller/cffl_checkbox.cpp


### vo...@google.com (2023-03-16)

The report document mentions that the vulnerability was found in M-92, so I believe this applies to LTS-108.

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations NCSC! The VRP Panel has decided to award you $7,000 for this report, which at your request, will be donated on your behalf (after we double it based on our policies for donated VRP reward, of course). Thank you for your excellent report of this issue and reporting these issues to us! 

### am...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### se...@ncsc.gov.uk (2023-03-23)

Hello @amyressler@chromium.org,

Thank you for the award! Will this be issued as a Benevity giftcard that we can then use to donate?

Many thanks again,
NCSC

### am...@chromium.org (2023-03-23)

Hello, NCSC team! Yes, you'll be receiving a giftcard code so that you are able to directly donate the reward to the organization of your choosing through Benevity. 



### vo...@google.com (2023-03-27)

1. https://pdfium-review.googlesource.com/c/pdfium/+/104910
2. Low - small conflict
3. M110, M111, M112
4. Yes

### [Deleted User] (2023-03-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-28)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/2ae0976943abf567523989b2732d6d57a7ee03e1

commit 2ae0976943abf567523989b2732d6d57a7ee03e1
Author: Zakhar Voit <voit@google.com>
Date: Tue Mar 28 15:19:38 2023

[M108-LTS] Observe CPWL_* object destruction across CPDFSDK_Widget methods

This is a simple fix to stop the symptoms while we investigate
how to avoid mutations at these points in the first place.

-- fix some nearby braces and annoying blank lines while at it.

Bug: chromium:1419831
Change-Id: I20c38806b91c7c0c9016bb1b567a04ce319243d8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104397
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 63e3719f1ec20ee6db804b2b2d4b00680db18d9c)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104833
Auto-Submit: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit a0d16d18d072ce77e639a09ed211340a2ad9034e)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/104910

[modify] https://pdfium.googlesource.com/pdfium/+/2ae0976943abf567523989b2732d6d57a7ee03e1/fpdfsdk/formfiller/cffl_listbox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/2ae0976943abf567523989b2732d6d57a7ee03e1/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/2ae0976943abf567523989b2732d6d57a7ee03e1/fpdfsdk/formfiller/cffl_checkbox.cpp


### gm...@google.com (2023-03-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-03-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-06)

Reward processed for donation at the request of the reporters. As such, your reward amount has been doubled to $14,000 to be donated to a charitable organization or cause of your choosing! 

### [Deleted User] (2023-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1419831?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063272)*
