# Heap-buffer-overflow in angle::LoadToNative<signed char,1>

| Field | Value |
|-------|-------|
| **Issue ID** | [40091191](https://issues.chromium.org/issues/40091191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | w3...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2018-04-24 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5928207824715776

Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x12aac8231b84
Crash State:
  angle::LoadToNative<signed char,1>
  rx::Image11::loadData
  rx::TextureD3D::initializeContents
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=550440:550450

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5928207824715776

Issue filed automatically.

See https://github.com/google/clusterfuzz-tools for more information.

## Timeline

### el...@chromium.org (2018-04-24)

https://chromium.googlesource.com/angle/angle.git/+log/14f4817c4dad..56c8577b4dbf is the ANGLE roll in the regression range.

https://chromium.googlesource.com/angle/angle.git/+/56c8577b4dbf2239780e38090dadbeb06f4b8563 touched the initializeContents method of TextureD3D.

[Monorail components: Internals>GPU>ANGLE]

### sh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-04-24)

This is same as 834534, our gpu bots were not configured right, so it wont reproduce on gpu bots.

### in...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### ge...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### ge...@chromium.org (2018-04-24)

I'll take a look.

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f2807385cbc923d71677d43cf846cec630a42551

commit f2807385cbc923d71677d43cf846cec630a42551
Author: Geoff Lang <geofflang@chromium.org>
Date: Tue Apr 24 20:35:27 2018

D3D: Use an alignment of 1 when uploading zero data to initialize textures.

BUG=836131

Change-Id: I1206c8eda465da563e15cf43f2e5c9320bb65eae
Reviewed-on: https://chromium-review.googlesource.com/1026460
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/f2807385cbc923d71677d43cf846cec630a42551/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/f2807385cbc923d71677d43cf846cec630a42551/src/tests/gl_tests/RobustResourceInitTest.cpp


### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9dc7cc6f79e2fa73cf375ce3b64d0c4056d08425

commit 9dc7cc6f79e2fa73cf375ce3b64d0c4056d08425
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Apr 24 23:08:36 2018

Roll src/third_party/angle/ 33e05babb..f2807385c (2 commits)

https://chromium.googlesource.com/angle/angle.git/+log/33e05babbc69..f2807385cbc9

$ git log 33e05babb..f2807385c --date=short --no-merges --format='%ad %ae %s'
2018-04-24 geofflang D3D: Use an alignment of 1 when uploading zero data to initialize textures.
2018-04-24 jmadill Vulkan: Add GetColorComponentFlags.

Created with:
  roll-dep src/third_party/angle
BUG=chromium:836131


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
TBR=geofflang@chromium.org

Change-Id: I7201098909db555b302a67bd4108eda1b6f30eb8
Reviewed-on: https://chromium-review.googlesource.com/1026559
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#553341}
[modify] https://crrev.com/9dc7cc6f79e2fa73cf375ce3b64d0c4056d08425/DEPS


### go...@chromium.org (2018-04-25)

M67 Stable promotion is coming soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. Thank you.



### cl...@chromium.org (2018-04-25)

ClusterFuzz has detected this issue as fixed in range 553334:553344.

Detailed report: https://clusterfuzz.com/testcase?key=5928207824715776

Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x12aac8231b84
Crash State:
  angle::LoadToNative<signed char,1>
  rx::Image11::loadData
  rx::TextureD3D::initializeContents
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=550440:550450
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=553334:553344

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5928207824715776

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-04-25)

ClusterFuzz testcase 5928207824715776 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-04-25)

The older reward-topanel https://crbug.com/chromium/834534 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ge...@chromium.org (2018-04-25)

This is the same bug as https://crbug.com/chromium/834534 but it was not completely fixed the first time.

### sh...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ge...@chromium.org (2018-04-25)

Would like to merge this to M67 (CL in https://crbug.com/chromium/836131#c9), a one-line fix that covers some extra edge cases from cwallez's fix that was merged in https://crbug.com/chromium/827667

### in...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-25)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-04-25)

Re #17: Is CL listed at #9 still need a merge to M67 as this bugis marked as dupe of https://crbug.com/chromium/827667 at #18?

### ge...@chromium.org (2018-04-25)

Yes, both CLs partially fix the bug.  The dupe is incorrect.

### go...@chromium.org (2018-04-26)

Thank you geofflang@.
+awhalley@ for M67 merge review. PTAL comments #17, #20 and #21. Thank you.

### aw...@google.com (2018-04-26)

govind - good for 57

### go...@chromium.org (2018-04-26)

Approving merge for Cl listed at #9 to M67 branch 3396 based on https://crbug.com/chromium/836131#c23. Please merge ASAP. Thank you.

### bu...@chromium.org (2018-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f7d4f25ecb44e47cecea9f3685b5c03aa7a4f9d3

commit f7d4f25ecb44e47cecea9f3685b5c03aa7a4f9d3
Author: Geoff Lang <geofflang@chromium.org>
Date: Thu Apr 26 19:02:56 2018

D3D: Use an alignment of 1 when uploading zero data to initialize textures.

BUG=836131

Change-Id: I1206c8eda465da563e15cf43f2e5c9320bb65eae
Reviewed-on: https://chromium-review.googlesource.com/1026460
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit f2807385cbc923d71677d43cf846cec630a42551)
Reviewed-on: https://chromium-review.googlesource.com/1030890
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/f7d4f25ecb44e47cecea9f3685b5c03aa7a4f9d3/src/libANGLE/renderer/d3d/TextureD3D.cpp
[modify] https://crrev.com/f7d4f25ecb44e47cecea9f3685b5c03aa7a4f9d3/src/tests/gl_tests/RobustResourceInitTest.cpp


### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-05-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-03)

The older reward-topanel https://crbug.com/chromium/834599 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Nice one w3bd3vil! The VRP panel decided to award $1,000 + the $500 fuzzer bonus for this report.

### aw...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-01)

This issue was migrated from crbug.com/chromium/836131?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/834599]
[Monorail mergedinto: crbug.com/chromium/827667]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091191)*
