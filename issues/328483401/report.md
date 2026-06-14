# Crash in gpu::gles2::GLES2Implementation::BufferDataHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [328483401](https://issues.chromium.org/issues/328483401) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | pe...@tencent.com |
| **Created** | 2024-03-07 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5125651647889408

Fuzzer: nesk_webgldomav2
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x78600000beff
Crash State:
  gpu::gles2::GLES2Implementation::BufferDataHelper
  gpu::gles2::GLES2Implementation::BufferData
  blink::v8_webgl2_rendering_context::BufferDataOperationOverload4
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1269370:1269374

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5125651647889408

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### ad...@google.com (2024-03-07)

Security shepherd here. I love it when ClusterFuzz successfully minimizes, bisects and labels everything.

Based on the regression range, sending to kbr@ as someone who knows about [this commit](https://chromium-review.googlesource.com/c/chromium/src/+/5344450).

### pe...@google.com (2024-03-07)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-07)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@tencent.com (2024-03-08)

This crash caused by invalid offset in bufferData causing memory out of bounds. I upload a CL to fix this issue:
<https://chromium-review.googlesource.com/c/chromium/src/+/5353870>

kbr@, please take a look. Thanks you very much.

### kb...@chromium.org (2024-03-11)

Thank you Perry for following up on this. Had a comment on your CL above.

### ap...@google.com (2024-03-13)

Project: chromium/src
Branch: main

commit 31e88b9d3d21986637252aed7f0aba9416950daf
Author: perryuwang <perryuwang@tencent.com>
Date:   Wed Mar 13 04:49:24 2024

    Fix crash caused by invalid offset in bufferData
    
    Invalid offset value causes memory out of bounds. This CL constrains
    that offset must be a non-negative value.
    
    Bug: 328483401
    Change-Id: I7c8bf7df88dd4038ad1ea52b8b40337be3bf81b4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5353870
    Reviewed-by: Kenneth Russell <kbr@chromium.org>
    Commit-Queue: Perry <perryuwang@tencent.com>
    Cr-Commit-Position: refs/heads/main@{#1271980}

M       third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc

https://chromium-review.googlesource.com/5353870


### 24...@project.gserviceaccount.com (2024-03-13)

ClusterFuzz testcase 5125651647889408 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1271979:1271980

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-03-20)

Not requesting merge to dev (M124) because latest trunk commit (1271980) appears to be prior to dev branch point (1274542). If this is incorrect please remove NA-124 from the 'Merge' field and add 124 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations n3sk! The Chrome VRP Panel has decided to award you $7,000 for this fuzzer report of renderer process memory corruption + $2,000 fuzzer bonus. Thank you for your fuzzing contributions to Chromium -- nice work!

### pe...@google.com (2024-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328483401)*
