# [ANGLE] Vulkan Use After Free in onBeginTransformFeedback

| Field | Value |
|-------|-------|
| **Issue ID** | [40059047](https://issues.chromium.org/issues/40059047) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sj...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-03-10 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4934.0 Safari/537.36

Steps to reproduce the problem:
1. run with ./chrome --no-sandbox http://localhost:8000/poc1.html
2.
3.

What is the expected behavior?

What went wrong?
## Title
- [ANGLE] Vulkan Use After Free in onBeginTransformFeedback

## Test Environment
- OS : Ubuntu 20.04 64 bit
- Chromium Version : 101.0.4934.0 (Developer Build) (64-bit)
- Revision : 281980ccda2381e557cf502d101d1be3a0d76352-refs/heads/main@{#979210}
- run option :
    ./chrome --no-sandbox http://localhost:8000/poc1.html

## Analysis

* third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:4815
```c++
angle::Result ContextVk::onBeginTransformFeedback(
    size_t bufferCount,
    const gl::TransformFeedbackBuffersArray<vk::BufferHelper *> &buffers,
    const gl::TransformFeedbackBuffersArray<vk::BufferHelper> &counterBuffers)
{
    onTransformFeedbackStateChanged();

    bool shouldEndRenderPass = false;

    // If any of the buffers were previously used in the render pass, break the render pass as a
    // barrier is needed.
    for (size_t bufferIndex = 0; bufferIndex < bufferCount; ++bufferIndex)
    {
        const vk::BufferHelper *buffer = buffers[bufferIndex];
        if (mRenderPassCommands->usesBuffer(*buffer)) //[*] Here, refers to the already freed buffer.
        {
            shouldEndRenderPass = true;
            break;
        }
    }
//...
```

In above [*], reference to already freed Buffer Object.

## Credits
- Jeonghoon Shin at Theori

## PoC
- attached poc1.html
## ASAN Log
- attached poc1_asan.txt

Did this work before? N/A 

Chrome version: 101.0.4934.0  Channel: dev
OS Version: Ubuntu 20.04

## Attachments

- [report1.md](attachments/report1.md) (text/plain, 1.3 KB)
- [poc1.html](attachments/poc1.html) (text/plain, 2.2 KB)
- [poc1_asan.txt](attachments/poc1_asan.txt) (text/plain, 17.2 KB)

## Timeline

### [Deleted User] (2022-03-10)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-03-11)

Thanks for the report!

Successful repro on Linux ASAN build from tip of tree. I only tested a Linux build, but based on the build rules for this file this code is present everywhere except iOS. 

Assigning Severity High because UAF in sandbox process can be assumed to lead to RCE. 

[Monorail components: Internals>GPU>ANGLE Internals>GPU>Vulkan]

### [Deleted User] (2022-03-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5760301630554112.

### [Deleted User] (2022-03-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-03-14)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-03-14)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-03-14)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-03-14)

[Empty comment from Monorail migration]

[Monorail components: -Internals>GPU>Vulkan]

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/708ce9cfd63bc8eab7c48987612a2dedce78c69a

commit 708ce9cfd63bc8eab7c48987612a2dedce78c69a
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Mar 14 14:37:31 2022

Fix crash when pausing XFB then deleting a buffer.

Fix is to validate XFB buffer bindings even if we're paused.
This is undefined behaviour so we can use any non-crashing solution.

Bug: chromium:1305190
Change-Id: Ib95404cdb13adbde7f34d6cc77473a8b3cbf1de7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3522283
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/708ce9cfd63bc8eab7c48987612a2dedce78c69a/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/708ce9cfd63bc8eab7c48987612a2dedce78c69a/src/libANGLE/validationES.cpp


### gi...@appspot.gserviceaccount.com (2022-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b1219a869bd9b469bac758bc9f8463b1361b52e

commit 9b1219a869bd9b469bac758bc9f8463b1361b52e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 17 00:45:04 2022

Roll ANGLE from 3739a195c2df to d867ddbbb1b8 (26 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/3739a195c2df..d867ddbbb1b8

2022-03-16 m.maiya@samsung.com Doc: Update supported EGL minor version
2022-03-16 yuxinhu@google.com Revert "Flush the texture staged updates when destroying context share group"
2022-03-16 lubosz.sarnecki@collabora.com FrameCapture: Add override for Glsizei* types.
2022-03-16 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-16 romanl@google.com angle_system_info_test also exports androidSdkLevel
2022-03-16 romanl@google.com angle_system_info_test passes json via file
2022-03-16 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a11411926c31 to 51988dcdccbf (9 revisions)
2022-03-16 yahan@google.com Do not copy parent layer frame position
2022-03-15 cclao@google.com Vulkan: Update mCurrentElementArrayBuffersync based on dirty bit
2022-03-15 yuxinhu@google.com Flush the texture staged updates when destroying context share group
2022-03-15 b.schade@samsung.com Remove invalid validation check on compressed texture formats
2022-03-15 cclao@google.com Vulkan: Handle the case where the bound buffer is empty
2022-03-15 lubosz.sarnecki@collabora.com FrameCapture: Skip invalid VertexAttribPointer calls in MEC.
2022-03-15 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-15 jmadill@chromium.org Vulkan: Temporarily suppress 3 perf counter tests on P6.
2022-03-15 jmadill@chromium.org Revert "Vulkan: VkFormat/DrmFourCC"
2022-03-15 lexa.knyazev@gmail.com Skip no-op base instance draw calls
2022-03-15 lexa.knyazev@gmail.com Fix typo in DrawElementsInstancedBaseVertexBaseInstanceANGLE
2022-03-15 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from ffa866a5ae9e to 45902868a797 (562 revisions)
2022-03-15 b.schade@samsung.com Add usage of Spirv through glslang build flag
2022-03-14 kkinnunen@apple.com Add device id as a part of the key in EGLDisplay cache
2022-03-14 antonio.caggiano@collabora.com Vulkan: VkFormat/DrmFourCC
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 2d9abfbddc1b to a11411926c31 (18 revisions)
2022-03-14 jmadill@chromium.org Fix crash when pausing XFB then deleting a buffer.
2022-03-14 cclao@google.com Vulkan: Fix another corner case of mCurrentElementArrayBuffer
2022-03-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from f7e842466e0a to 8252a3d3cdd3 (8 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1296467,chromium:1299211,chromium:1299261,chromium:1305190
Tbr: jmadill@google.com
Test: Test: angle_end2end_tests --gtest_filter="VertexAttributeTestES3.InvalidAttribPointer/*"
Test: Test: capture_replay_tests.py --gtest_filter=FenceSyncTest.NullLength/*
Test: Test: gtest_filter=*DXT1CompressedTextureTest.NonBlockSizesMipLevels*
Test: Test: when using ANGLE (with metal or swiftshader backend) with
Change-Id: I52ffe787d20dd083af8efe1bdef05616ac611f55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3530116
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#981945}

[modify] https://crrev.com/9b1219a869bd9b469bac758bc9f8463b1361b52e/DEPS


### ad...@google.com (2022-03-21)

(auto-cc on security bug)

### sj...@gmail.com (2022-03-29)

Hi.

Is this issue already fixed?

Thanks

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-03-30)

Yes, it's fixed, thanks for the ping.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-04-11)

Should this fix be merged?

### jm...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-11)

ClusterFuzz testcase 6205249010073600 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Congratulations, Jeonghoon! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and nice work! 

### gi...@appspot.gserviceaccount.com (2022-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5c85fd4e11a3835a0719223a7cedb978d309da21

commit 5c85fd4e11a3835a0719223a7cedb978d309da21
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Apr 11 16:29:00 2022

Add error check on resuming XFB with deleted buffer.

Bug: chromium:1305190
Change-Id: I22c6f6400b05ca32c922fba9a3b9d4b5841ca8b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3578378
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/5c85fd4e11a3835a0719223a7cedb978d309da21/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/5c85fd4e11a3835a0719223a7cedb978d309da21/src/libANGLE/validationES3.cpp


### sj...@gmail.com (2022-04-11)

thanks for the reward!

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12e39e60c7b15f677b8f6776d9922b52d4a98ca6

commit 12e39e60c7b15f677b8f6776d9922b52d4a98ca6
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 12 04:42:05 2022

Roll ANGLE from a947c5f56cf7 to eeb396535317 (6 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/a947c5f56cf7..eeb396535317

2022-04-12 syoussefi@chromium.org Autogenerate features
2022-04-12 gman@chromium.org Metal:remove TextureMtl::mIsPow2
2022-04-11 kkinnunen@apple.com Metal: Avoid leaking MTLDevice lists in DisplayMtl
2022-04-11 kkinnunen@apple.com Metal: Avoid leaking MTLFunctionConstantValues in ProgramMtl
2022-04-11 steven@valvesoftware.com egl_angle_ext.xml: add missing enums and typedefs
2022-04-11 jmadill@chromium.org Add error check on resuming XFB with deleted buffer.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1305190
Tbr: jonahr@google.com
Change-Id: Iccec53b895433a13ca65f021622de2ad666531d1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3583202
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#991364}

[modify] https://crrev.com/12e39e60c7b15f677b8f6776d9922b52d4a98ca6/DEPS


### cl...@chromium.org (2022-04-12)

ClusterFuzz testcase 6205249010073600 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=991358:991364

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-15)

Manually adding merge request labels so these go into merge review queue (we are also looking into why sheriffbot is sleeping on the job in this regard) 

### [Deleted User] (2022-04-15)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-15)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-04-16)

m101 merge approved, please merge this fix to branch 4951
m100 merge approved, please merge this fix to branch 4896
please complete both merges prior to 10am PDT, Tuesday 19 April so this fix can be included in the m101 and m100 stable and extended stable cuts 

### am...@chromium.org (2022-04-16)

I should have specified, both CLs  (https://chromium-review.googlesource.com/c/angle/angle/+/3578378 and https://chromium-review.googlesource.com/c/angle/angle/+/3522283) to M100 

https://chromium-review.googlesource.com/c/angle/angle/+/3522283 is already on M101, so please merge https://chromium-review.googlesource.com/c/angle/angle/+/3578378 to M101 

thanks! 

### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d24570fb658ef04f67c773989af6218ff8a3a7a6

commit d24570fb658ef04f67c773989af6218ff8a3a7a6
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Mar 14 14:37:31 2022

[M100] Fix crash when pausing XFB then deleting a buffer.

Fix is to validate XFB buffer bindings even if we're paused.
This is undefined behaviour so we can use any non-crashing solution.

Bug: chromium:1305190
Change-Id: Ib95404cdb13adbde7f34d6cc77473a8b3cbf1de7
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3522283
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 708ce9cfd63bc8eab7c48987612a2dedce78c69a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594105
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/d24570fb658ef04f67c773989af6218ff8a3a7a6/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/d24570fb658ef04f67c773989af6218ff8a3a7a6/src/libANGLE/validationES.cpp


### [Deleted User] (2022-04-19)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-04-19)

Based on offline chat we have all the Merged to M101 hence marking the merge labels manually

### rz...@google.com (2022-04-19)

Changed code is not present in M96.

### am...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1305190?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1305219, crbug.com/chromium/1313905]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059047)*
