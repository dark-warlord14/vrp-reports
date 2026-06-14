# Non-positive-vla-bound-value in blink::CanvasPath::roundRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40800189](https://issues.chromium.org/issues/40800189) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>Canvas, Blink>JavaScript>API |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2021-10-26 |
| **Bounty** | $1,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6010514792316928

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_ubsan_chrome
Platform Id: linux

Crash Type: Non-positive-vla-bound-value
Crash Address: 
Crash State:
  blink::CanvasPath::roundRect
  blink::v8_canvas_rendering_context_2d::RoundRectOperationCallback
  v8::internal::FunctionCallbackArguments::Call
  
Sanitizer: undefined (UBSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_ubsan_chrome&range=809305:809316

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6010514792316928

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6010514792316928 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Canvas Blink>JavaScript>API]

### cl...@chromium.org (2021-10-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/90c34dc0532b7e3733dd7f2249ea7726b5d01cc6 (Add roundRect to path).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2021-10-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

aaronhk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-11-24)

gentle ping - any updates on this one?

### aa...@chromium.org (2021-11-24)

I cannot repro, this is very strange. Looking at the minimized testcase (https://clusterfuzz.com/viewer?testcase_id=6010514792316928&key=a36b8e3a-aa84-4fba-ade0-d789484b39f1):

var v4217 = v3141.getLineDash(); 

Returns an empty array. This should throw an error on this line:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/canvas/canvas2d/canvas_path.cc;l=513?q=canvas_path.cc&sq=package:chromium&ct=os

But somehow the code is getting to this point:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/canvas/canvas2d/canvas_path.cc;l=532?q=canvas_path.cc&sq=package:chromium&ct=os

And THEN throwing an error because num_radii = 0. When I run the test locally, it fails on line 513, as expected. I cannot reproduce the behaviour of the fuzzer, nor do I have any idea how that's happening.

### aa...@chromium.org (2021-11-24)

Nevermind, my esteemed teammate junov@ immediately saw the issue. I'll have a fix up in a second.

### m....@gmail.com (2021-11-24)

Should this code return after ThrowRangeError？

### aa...@chromium.org (2021-11-24)

 m.cooolie@gmail.com, exactly. The error stop js execution, but not C++ execution. Why this is only a problem for UBSAN and not for release builds is totally beyond me.

Fix is here: https://chromium-review.googlesource.com/c/chromium/src/+/3299291

### m....@gmail.com (2021-11-25)

I see that there are some similar patterns in the next few lines of this function, but this CL did not deal with it, do you need to deal with it?

### aa...@chromium.org (2021-11-26)

Good point, I'll do that

### gi...@appspot.gserviceaccount.com (2021-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7732d063d755b2b03a7f55ed0de595caa0724a91

commit 7732d063d755b2b03a7f55ed0de595caa0724a91
Author: Aaron Krajeski <aaronhk@chromium.org>
Date: Sun Nov 28 12:51:15 2021

Return from roundrect error

The error stops javascript execution, but not necessarily C++ execution.
This can trip up fuzzers.

Bug: 1263417
Change-Id: Id145b4eaf24d558e7804a2d8fe9fef4c104c1a7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299291
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#945748}

[modify] https://crrev.com/7732d063d755b2b03a7f55ed0de595caa0724a91/third_party/blink/renderer/modules/canvas/canvas2d/path_2d.h
[modify] https://crrev.com/7732d063d755b2b03a7f55ed0de595caa0724a91/third_party/blink/renderer/modules/canvas/canvas2d/path_2d.cc
[modify] https://crrev.com/7732d063d755b2b03a7f55ed0de595caa0724a91/third_party/blink/renderer/modules/canvas/canvas2d/canvas_path.cc


### cl...@chromium.org (2021-11-29)

ClusterFuzz testcase 6010514792316928 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_ubsan_chrome&range=945747:945749

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Hello, while this issue did not appear to be exploitable, the VRP Panel did want to extend a $1,000 award for this fuzzer discovery and your analysis and prompt that did land a mitigation. Thank you for your efforts and your contributions to Chrome Fuzzing. 

### am...@chromium.org (2022-01-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

Updating to type=bug due to this not being an exploitable security issue 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1263417?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Canvas, Blink>JavaScript>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40800189)*
