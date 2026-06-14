# UAF in blink::PaintLayer::CommonAncestor

| Field | Value |
|-------|-------|
| **Issue ID** | [40050970](https://issues.chromium.org/issues/40050970) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Compositing, Blink>Paint |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2019-12-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

==426180==ERROR: AddressSanitizer: heap-use-after-free on address 0x1218d6e37560 at pc 0x7ff951ca7e53 bp 0x00ebfd9f78e0 sp 0x00ebfd9f7928  

READ of size 8 at 0x1218d6e37560 thread T0  

#0 0x7ff951ca7e52 in blink::PaintLayer::CommonAncestor(class blink::PaintLayer const \*) const C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\paint\paint\_layer.cc:3551:1

**VERSION**  

Chrome Version: 80.0.3987.7 dev also tested on latest canary (78.0.3871.0) 64bit  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

Minimized test case together with ASAN logs attached.

**CREDIT INFORMATION**  

Reporter credit: Pawel Wylecial of REDTEAM.PL

## Attachments

- [cm_render.html](attachments/cm_render.html) (text/plain, 749 B)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 35.9 KB)

## Timeline

### pa...@blackowlsec.com (2019-12-13)

* small correction latest canary 81.0.3993.0 not 78.0.3871.0

### cl...@chromium.org (2019-12-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4803596122128384.

### cl...@chromium.org (2019-12-13)

Testcase 4803596122128384 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4803596122128384.

### pa...@blackowlsec.com (2019-12-14)

sorry, from what i see #enable-display-locking flag is required to trigger this

### cl...@chromium.org (2019-12-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4765287631093760.

### cl...@chromium.org (2019-12-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6381802155474944.

### cl...@chromium.org (2019-12-16)

Testcase 4765287631093760 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4765287631093760.

### cl...@chromium.org (2019-12-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Compositing Blink>Paint]

### cl...@chromium.org (2019-12-16)

ClusterFuzz testcase 6381802155474944 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2019-12-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6381802155474944

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000156118
Crash State:
  blink::PaintLayer::CommonAncestor
  blink::CompositingInputsRoot::Update
  blink::PaintLayer::RemoveChild
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=724986

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6381802155474944

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6381802155474944 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### oc...@google.com (2019-12-16)

chrishtr, could you please help with triaging this bug as an owner of third_party/blink/renderer/core/paint ? Thanks!

### oc...@google.com (2019-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-16)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-12-16)

rakina@, can you look at this with vmpstr@ OOO?

### ch...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-17)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-31)

chrishtr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8a2ded450fe5e95cd6174700c048ee6bd8afaf8a

commit 8a2ded450fe5e95cd6174700c048ee6bd8afaf8a
Author: Chris Harrelson <chrishtr@chromium.org>
Date: Thu Jan 02 22:41:35 2020

Clear a CompositingInputRoot that is being deleted.

This is probably only a problem with rendersubtree-locked subtrees,
because the compositing inputs dirty bits get left around for these
subtrees.

Bug: 1033795

Change-Id: I3dca73eed34b39c70c7609bdfb9d052dc1b6af2b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1977306
Reviewed-by: vmpstr <vmpstr@chromium.org>
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#728046}

[modify] https://crrev.com/8a2ded450fe5e95cd6174700c048ee6bd8afaf8a/third_party/blink/renderer/core/paint/compositing/compositing_inputs_updater.cc
[modify] https://crrev.com/8a2ded450fe5e95cd6174700c048ee6bd8afaf8a/third_party/blink/renderer/core/paint/paint_layer.cc
[add] https://crrev.com/8a2ded450fe5e95cd6174700c048ee6bd8afaf8a/third_party/blink/web_tests/wpt_internal/display-lock/rendersubtree/audio-element-crash.html


### ch...@chromium.org (2020-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-03)

Requesting merge to beta M80 because latest trunk commit (728046) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-03)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-03)

chrishtr@ pls answer the questions in https://crbug.com/chromium/1033795#c25 for merge review.

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-07)

friendly ping chrishtr@

### ch...@chromium.org (2020-01-07)

It is not necessary to merge this CL. The fix only applies to an unlaunched feature.

### sr...@google.com (2020-01-07)

removing merge review label per https://crbug.com/chromium/1033795#c29

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-14)

chrishtr@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-04-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wi...@gmail.com (2021-06-06)

To reproduce this bug, "Experimental Web Platform Features" flags should be enabled.

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1033795?no_tracker_redirect=1

[Multiple monorail components: Blink>Compositing, Blink>Paint]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050970)*
