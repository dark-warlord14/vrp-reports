# Security: swiftshader heap-use-after-free in getOffsetPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40057980](https://issues.chromium.org/issues/40057980) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-11-21 |
| **Bounty** | $5,000.00 |

## Description

Tested on Version 96.0.4664.45 (Official Build) (64-bit) on Windows 11 and asan-win32-release_x64-936776.


2:146> r
rax=00000000feeefeee rbx=0000000000000001 rcx=feeefeeefeeefeee
rdx=00007ffd8a15b608 rsi=000000df2d9fec08 rdi=feeefeeefeeefeee
rip=00007ffd89dc5597 rsp=000000df2d9feb80 rbp=0000000000000000
 r8=000000df2d9fec08  r9=0000000000000000 r10=0000022386884440
r11=000002238659e0b0 r12=00000223872083b8 r13=000002238659c268
r14=0000022386884150 r15=000002238659c268
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
vk_swiftshader!vk::Image::getTexelPointer+0x17:
00007ffd`89dc5597 4c8b31          mov     r14,qword ptr [rcx] ds:feeefeee`feeefeee=????????????????
2:146> k
 # Child-SP          RetAddr               Call Site
00 000000df`2d9feb80 00007ffd`89dc8982     vk_swiftshader!vk::Image::getTexelPointer+0x17 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkImage.cpp @ 662] 
01 000000df`2d9febe0 00007ffd`89e14c76     vk_swiftshader!vk::ImageView::getOffsetPointer+0x82 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkImageView.cpp @ 381] 
02 000000df`2d9fec30 00007ffd`89db696b     vk_swiftshader!sw::Renderer::draw+0xdc6 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Device\Renderer.cpp @ 391] 
03 000000df`2d9ff120 00007ffd`89db66ef     vk_swiftshader!`anonymous namespace'::CmdDrawBase::draw+0x24b [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp @ 508] 
04 000000df`2d9ff230 00007ffd`89db55be     vk_swiftshader!`anonymous namespace'::CmdDraw::execute+0x2f [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp @ 534] 
05 000000df`2d9ff270 00007ffd`89dce902     vk_swiftshader!vk::CommandBuffer::submit+0x2e [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkCommandBuffer.cpp @ 1731] 
06 000000df`2d9ff2c0 00007ffd`89dcdfb1     vk_swiftshader!vk::Queue::submitQueue+0x262 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 220] 
07 000000df`2d9ff690 00007ffd`89dcf29a     vk_swiftshader!vk::Queue::taskLoop+0xb1 [C:\b\s\w\ir\cache\builder\src\third_party\swiftshader\src\Vulkan\VkQueue.cpp @ 281] 
08 (Inline Function) --------`--------     vk_swiftshader!std::__1::__invoke+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\type_traits @ 3897] 
09 (Inline Function) --------`--------     vk_swiftshader!std::__1::__thread_execute+0xb [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 280] 
0a 000000df`2d9ff730 00007ffd`8a0715e0     vk_swiftshader!std::__1::__thread_proxy<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct,std::__1::default_delete<std::__1::__thread_struct> >,void (vk::Queue::*)(marl::Scheduler *),vk::Queue *,marl::Scheduler *> >+0x2a [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\thread @ 293] 
0b 000000df`2d9ff770 00007ffe`3a1054e0     vk_swiftshader!thread_start<unsigned int (__cdecl*)(void *),1>+0x50 [C:\b\s\w\ir\cache\builder\src\out\Release_x64\minkernel\crts\ucrt\src\appcrt\startup\thread.cpp @ 97] 
0c 000000df`2d9ff7a0 00007ffe`3afa485b     KERNEL32!BaseThreadInitThunk+0x10
0d 000000df`2d9ff7d0 00000000`00000000     ntdll!RtlUserThreadStart+0x2b


## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.1 KB)
- [getOffsetPointer.html](attachments/getOffsetPointer.html) (text/plain, 2.8 KB)

## Timeline

### [Deleted User] (2021-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-21)

Chrome needs to be run with the following flags  .\chrome.exe --no-sandbox --disable-gpu

### cl...@chromium.org (2021-11-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5688492090523648.

### mp...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-11-23)

This looks like a duplicate of 1270658, but I'll try to double check this week.

### rs...@chromium.org (2021-11-23)

Thanks, matching flags of https://crbug.com/chromium/1270658 for now. If it is the same, go ahead and dupe.

Clusterfuzz puts the regression range at https://chromium.googlesource.com/chromium/src/+log/800bc54659eebae7ff28a0480c95ef40919e5afd..0294f38c6ffc5749b35e11794b8187bb59ed7b35?pretty=fuller&n=10000.

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5688492090523648

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60e000110fcc
Crash State:
  vk::ImageView::getOffsetPointer
  sw::Renderer::draw
  CmdDrawBase::draw
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=921184:921189

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5688492090523648

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5688492090523648 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-11-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2021-11-25)

For some reason, I can't repro this locally (but I can reproduce https://crbug.com/chromium/1270658, which looks very similar, just fine). I'm using ToT Chrome.
I'm not sure what I'm doing wrong. Nicolas, could you just tell me if you manage to reproduce this locally?

### ni...@google.com (2021-11-25)

This doesn't reproduce on my system either. It could be affected by core count or available memory, since it appears to involve asynchronous garbage collection in ANGLE (the asan.log in the first message is very helpful).

### sy...@chromium.org (2021-12-02)

I reran clusterfuzz to see if the issue still reproduces https://crbug.com/chromium/1270658 is fixed now.

### cl...@chromium.org (2021-12-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5688492090523648

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60e000110fcc
Crash State:
  vk::ImageView::getOffsetPointer
  sw::Renderer::draw
  CmdDrawBase::draw
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=921184:921189

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5688492090523648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sy...@chromium.org (2021-12-03)

Ok looks like this is still reproducible somehow, I'll see if I can repro. @Nicolas, FYI there's no async garbage collection happening here, ANGLE is deleting the object in its main thread, but it should have deferred it (it has missed that the object is in use)

### sy...@chromium.org (2021-12-03)

I can't seem to be able to reproduce this either. I highly suspect the issue is with the way the page continuously refreshes itself.

### sy...@chromium.org (2021-12-03)

I took the minimalized case produced by the fuzzer and modified it such that the webgl rendering code is not async, but the page is still reloaded. Will see if the fuzzer can reproduce the crash with that: https://clusterfuzz.com/testcase-detail/6303958538452992

### sy...@chromium.org (2021-12-03)

Removing async seems to have fixed the issue according to clusterfuzz.

In the meantime, I managed to get a repro, but not just by running the page. I can reproduce the issue by opening the page, then opening a new tab and entering chrome://gpu. Depending on timing, this can either get Chrome to freeze or ASAN to throw a the same error as this issue.

### sy...@chromium.org (2021-12-03)

I can reproduce this now very reliably with --disable-gpu-compositing

### sy...@chromium.org (2021-12-03)

The rendering function being async is unrelated, I can repro without it too. However, removing the fenceSync() call fixes the issue, and so does changing the second texture1 to texture2. Presumably that leads to the first texture1 to be freed early when the var name is redefined?

### sy...@chromium.org (2021-12-03)

Replacing the fenceSync with flush also reproduces the issue, so not a bug with sync

### sy...@chromium.org (2021-12-04)

Figured it out. The problem is that TextureVk::copySubImageImplWithDraw takes a view to pass to UtilsVk to perform the copy. The view is retain()ed at the time it's acquired in TextureVk, but UtilsVk closes the render pass, issues a flush (due to the flush after draw, which is deffered), and opens a new one to perform the draw. As such, the view ends up being used in the next command buffer and isn't retained on that.

A similar problem probably affects all the draw-based UtilsVk tools.

### gi...@appspot.gserviceaccount.com (2021-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/55840e902470f95fe0f7d81fcf485abf16bf71a4

commit 55840e902470f95fe0f7d81fcf485abf16bf71a4
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Dec 03 20:24:00 2021

Vulkan: Fix deferred flush vs UtilsVk

Take the following scenario:

1. Draw
2. Flush (this is deferred)
3. Get image view (this is retain()ed)
4. Pass view to a draw-based UtilsVk function
5. Flush
6. Delete image view

At step 4, UtilsVk may start a new render pass and use the image view
from step 3.  Since the flush at step 2 is deferred, it will be
performed at this step, and so the serial of the image view is set to
the previous submission.

When step 4 uses this view, it doesn't retain it.  Step 5 submits the
new command buffer using this image view.

At step 6, if the previous submission has finished, it will destroy the
view immediately even though it's in use by the new submission.

One solution could have been to make sure render pass closure
originating from UtilsVk doesn't incur a flush.  However, due to the
current design where the render pass is immediately recorded in
RendererVk's primary command buffer, it's possible that an unrelated
context would perform the flush anyway.

This change makes sure instead that the render pass is closed before any
views are allocated/retained to be used by UtilsVk.

Bug: chromium:1272266
Change-Id: I5bdefb34e03c368511c4c174cf7965fda158d2b8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3315976
Reviewed-by: Tim Van Patten <timvp@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/vk_utils.h
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/UtilsVk.cpp
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/55840e902470f95fe0f7d81fcf485abf16bf71a4/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/44b788a5992fca21ead0749fcfe39c294b5ca97c

commit 44b788a5992fca21ead0749fcfe39c294b5ca97c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 09 23:14:38 2021

Roll ANGLE from 0f09d378edb9 to 663831aa676c (14 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/0f09d378edb9..663831aa676c

2021-12-09 jmadill@chromium.org Revert "Reland "system_utils: Add memory protection functionality.""
2021-12-09 gman@chromium.org Metal: Fix Intel backend fails with tall texture
2021-12-09 cclao@google.com Vulkan: Append the actual buffer size when binding's size is 0
2021-12-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from a4232c15e287 to 4625f84e8d56 (5 revisions)
2021-12-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from bc087f672f16 to 38603b300bce (6 revisions)
2021-12-09 ynovikov@chromium.org Skip couple flaky end2end tests on Pixel 4
2021-12-08 jmadill@chromium.org Frame Capture: Fix client buffers in MEC.
2021-12-08 ynovikov@chromium.org Sync logdog with Chromium
2021-12-08 timvp@google.com Vulkan: Re-enable RGB8 for pbuffers.
2021-12-08 syoussefi@chromium.org Vulkan: Fix deferred flush vs UtilsVk
2021-12-08 lubosz.sarnecki@collabora.com Reland "system_utils: Add memory protection functionality."
2021-12-08 timvp@google.com Add more support for GL_RGBX8_ANGLE
2021-12-08 jmadill@chromium.org Frame Capture: Track written files in ReplayWriter.
2021-12-08 jmadill@chromium.org Add a multi-context sample.

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
Bug: chromium:1272266
Tbr: jonahr@google.com
Test: Test: BlitFramebufferTestES31.BlitMultisampledRGBX8ToRGB8
Test: Test: WebGL2CompatibilityTest.ReadPixelsRgbx8AngleUnsignedByte
Test: Test: angle_unittests --gtest_filter="SystemUtils.PageFaultHandler*"
Change-Id: I94bab439a346c73efe8d997985682be63fc71bf0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3328262
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#950323}

[modify] https://crrev.com/44b788a5992fca21ead0749fcfe39c294b5ca97c/DEPS


### cl...@chromium.org (2021-12-11)

ClusterFuzz testcase 5688492090523648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=950320:950323

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

Requesting merge to stable M96 because latest trunk commit (950323) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (950323) appears to be after beta branch point (938553).

Not requesting merge to dev (M98) because latest trunk commit (950323) appears to be prior to dev branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-11)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-11)

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

### pb...@google.com (2021-12-12)

+adetaylor@ and @amyressler@ security TPM's for merge decision

### ad...@google.com (2021-12-13)

syoussefi@chromium.org thanks for figuring this out and for the fix.

As a GPU process use-after-free, this is at the upper end of 'high' severity and we will certainly want to merge this back to M96 and M97 as soon as possible. (M97 will become stable just after the holidays; M96 will be the new 'extended stable').

This has had ~3 days in Canary so I'm going ahead and approving merge to M96 (branch 4664) and M97 (branch 4692). *However*, if you think this carries measurable risk of stability or performance regressions then please comment here instead of merging, and we'll discuss.

### pb...@google.com (2021-12-13)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this Wednesday's M97 Beta release.

### sy...@chromium.org (2021-12-13)

It's pretty low risk, going to merge it right now.

### gi...@appspot.gserviceaccount.com (2021-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64

commit f4e66c4ba6ae205f1460a4720ee09ad7d958dd64
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Dec 03 20:24:00 2021

M97: Vulkan: Fix deferred flush vs UtilsVk

Take the following scenario:

1. Draw
2. Flush (this is deferred)
3. Get image view (this is retain()ed)
4. Pass view to a draw-based UtilsVk function
5. Flush
6. Delete image view

At step 4, UtilsVk may start a new render pass and use the image view
from step 3.  Since the flush at step 2 is deferred, it will be
performed at this step, and so the serial of the image view is set to
the previous submission.

When step 4 uses this view, it doesn't retain it.  Step 5 submits the
new command buffer using this image view.

At step 6, if the previous submission has finished, it will destroy the
view immediately even though it's in use by the new submission.

One solution could have been to make sure render pass closure
originating from UtilsVk doesn't incur a flush.  However, due to the
current design where the render pass is immediately recorded in
RendererVk's primary command buffer, it's possible that an unrelated
context would perform the flush anyway.

This change makes sure instead that the render pass is closed before any
views are allocated/retained to be used by UtilsVk.

Bug: chromium:1272266
Change-Id: Ia939fa0cf939f2db91f24dc343d0e3eaf836aba6
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3335066
Reviewed-by: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64/src/libANGLE/renderer/vulkan/UtilsVk.cpp
[modify] https://crrev.com/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/f4e66c4ba6ae205f1460a4720ee09ad7d958dd64/src/libANGLE/renderer/vulkan/TextureVk.cpp


### gi...@appspot.gserviceaccount.com (2021-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1

commit 2094ca58abdce5f24d2b0b82ca10a54ed990f8b1
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Fri Dec 03 20:24:00 2021

M96: Vulkan: Fix deferred flush vs UtilsVk

Take the following scenario:

1. Draw
2. Flush (this is deferred)
3. Get image view (this is retain()ed)
4. Pass view to a draw-based UtilsVk function
5. Flush
6. Delete image view

At step 4, UtilsVk may start a new render pass and use the image view
from step 3.  Since the flush at step 2 is deferred, it will be
performed at this step, and so the serial of the image view is set to
the previous submission.

When step 4 uses this view, it doesn't retain it.  Step 5 submits the
new command buffer using this image view.

At step 6, if the previous submission has finished, it will destroy the
view immediately even though it's in use by the new submission.

One solution could have been to make sure render pass closure
originating from UtilsVk doesn't incur a flush.  However, due to the
current design where the render pass is immediately recorded in
RendererVk's primary command buffer, it's possible that an unrelated
context would perform the flush anyway.

This change makes sure instead that the render pass is closed before any
views are allocated/retained to be used by UtilsVk.

Bug: chromium:1272266
Change-Id: Ifdcdea5a8e73fa6d3cb113211c95d3a5f57c3906
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3335063
Reviewed-by: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1/src/libANGLE/renderer/vulkan/UtilsVk.cpp
[modify] https://crrev.com/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1/src/libANGLE/renderer/vulkan/ResourceVk.cpp
[modify] https://crrev.com/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/2094ca58abdce5f24d2b0b82ca10a54ed990f8b1/src/libANGLE/renderer/vulkan/TextureVk.cpp


### sy...@chromium.org (2021-12-13)

Done.

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations on another one, Omair! The VRP Panel has decided to award you $5,000 for this report. Thanks for your efforts and nice work! 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1272266?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057980)*
