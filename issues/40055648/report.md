# Stack-use-after-return in SkRect::x

| Field | Value |
|-------|-------|
| **Issue ID** | [40055648](https://issues.chromium.org/issues/40055648) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Skia, Platform |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ju...@chromium.org |
| **Created** | 2021-04-23 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6341102773534720

Fuzzer: jesse_avalanche
Job Type: linux_debug_chrome
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0x7f90da7ac0a0
Crash State:
  SkRect::x
  blink::FloatRect::FloatRect
  blink::BaseRenderingContext2D::fillRect
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_debug_chrome&range=874736:874748

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6341102773534720

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6341102773534720 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-04-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Skia Platform]

### cl...@chromium.org (2021-04-23)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/fe0dba77d25752afcb453ed7446607504b6406e8 (Fix canvas filter crashes with fast API).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63cc0cbce5376c5c31c67f0242cea82eb0289f58

commit 63cc0cbce5376c5c31c67f0242cea82eb0289f58
Author: Justin Novosad <junov@chromium.org>
Date: Mon Apr 26 19:29:22 2021

Fix memory error in CanvasRenderingContext2D::fillRect

Lambda was capturing by reference a local variable that ended up getting
used after being popped off the stack due to the NoAlloc deferral
mechanism.

Bug: 1202119
Change-Id: Idac642ab74bafd79f1a83b538c683d05e59d648d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2849538
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Reviewed-by: Justin Novosad <junov@chromium.org>
Commit-Queue: Justin Novosad <junov@chromium.org>
Cr-Commit-Position: refs/heads/master@{#876267}

[modify] https://crrev.com/63cc0cbce5376c5c31c67f0242cea82eb0289f58/third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc


### ju...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-27)

ClusterFuzz testcase 6341102773534720 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_debug_chrome&range=876245:876268

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-28)

Congratulations! The VRP Panel has decided to award you $6000 for this report. Someone from our finance team will be in touch in the coming weeks to arrange payment (we are currently amid a finance systems transition). In the interim, please let me know (by what name/handle) you'd like to be credited for this issue. 
Thank you for your contributions to Chrome Fuzzing! 

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1202119?no_tracker_redirect=1

[Multiple monorail components: Internals>Skia, Platform]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055648)*
