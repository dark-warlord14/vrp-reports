# bad free in gpu ~PackedEnumMap

| Field | Value |
|-------|-------|
| **Issue ID** | [40059319](https://issues.chromium.org/issues/40059319) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU, Internals>GPU>ANGLE, Internals>GPU>SwiftShader, Internals>GPU>Vulkan |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-04-07 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1.open webserver  

python3.8 -m http.server 8000  

2.just run chrome with crash.html  

chrome <http://localhost:8000/crash.html>  

3.

**Problem Description:**  

tested version:  

Version 102.0.4972.0 (Official Build) dev (64-bit)  

Chromium 101.0.4929.5  

Ran the PoC in ASAN build, ASAN instrumentation could not catch the memory corruption. Rather, the internal state of the asan allocator itself was corrupted. And the ASAN build always crashes with the following check failure:  

AddressSanitizer: CHECK failed: asan\_allocator.cpp:188 "((old)) == ((kAllocBegMagic))" (0x0, 0xcc6e96b9cc6e96b9) (tid=4108016)  

#0 0x5602c9fb44c1 in \_\_asan::CheckUnwind() *asan\_rtl*:3  

#1 0x5602c9fc6944 in \_\_sanitizer::CheckFailed(char const\*, int, char const\*, unsigned long long, unsigned long long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/sanitizer\_common/sanitizer\_termination.cpp:86:5  

#2 0x5602c9f2e657 in Set *asan\_rtl*:7  

#3 0x5602c9f2e657 in \_\_asan::QuarantineCallback::Recycle(\_\_asan::AsanChunk\*) *asan\_rtl*:48  

#4 0x5602c9f2e3bc in \_\_sanitizer::Quarantine<\_\_asan::QuarantineCallback, \_\_asan::AsanChunk>::DoRecycle(\_\_sanitizer::QuarantineCache<\_\_asan::QuarantineCallback>\*, \_\_asan::QuarantineCallback) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_quarantine.h:193:12  

#5 0x5602c9f2df41 in \_\_sanitizer::Quarantine<\_\_asan::QuarantineCallback, \_\_asan::AsanChunk>::Recycle(unsigned long, \_\_asan::QuarantineCallback) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_quarantine.h:181:5  

#6 0x5602c9f301f7 in Put /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_quarantine.h:112:7  

#7 0x5602c9f301f7 in \_\_asan::Allocator::QuarantineChunk(\_\_asan::AsanChunk\*, void\*, \_\_sanitizer::BufferedStackTrace\*) *asan\_rtl*:18  

#8 0x5602c9faad95 in free *asan\_rtl*:3  

#9 0x7fac1e231e7d in vk::DeviceMemory::freeBuffer() ./../../third\_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:340:2  

#10 0x7fac1e231c4e in vk::DeviceMemory::destroy(VkAllocationCallbacks const\*) ./../../third\_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:157:3  

#11 0x7fac1e27f567 in destroy<VkNonDispatchableHandle<VkDeviceMemory\_T \*> > ./../../third\_party/swiftshader/src/Vulkan/VkDestroy.hpp:60:11  

#12 0x7fac1e27f567 in vkFreeMemory ./../../third\_party/swiftshader/src/Vulkan/libVulkan.cpp:1173:2  

#13 0x7fac20b01d6f in destroy ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_wrapper.h:1315:9  

#14 0x7fac20b01d6f in rx::vk::BufferBlock::destroy(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_utils.cpp:1607:19  

#15 0x7fac20aa30c5 in rx::vk::BufferPool::destroy(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:2760:16  

#16 0x7fac2092b3fc in rx::ShareGroupVk::onDestroy(egl::Display const\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/DisplayVk.cpp:423:19  

#17 0x7fac202f3005 in egl::ShareGroup::release(egl::Display const\*) ./../../third\_party/angle/src/libANGLE/Display.cpp:629:30  

#18 0x7fac2026aff6 in gl::Context::onDestroy(egl::Display const\*) ./../../third\_party/angle/src/libANGLE/Context.cpp:760:25  

#19 0x7fac202febda in egl::Display::releaseContext(gl::Context\*, egl::Thread\*) ./../../third\_party/angle/src/libANGLE/Display.cpp:1653:5  

#20 0x7fac203037ba in egl::Display::makeCurrent(egl::Thread\*, gl::Context\*, egl::Surface\*, egl::Surface\*, gl::Context\*) ./../../third\_party/angle/src/libANGLE/Display.cpp:1518:13  

#21 0x7fac203042c0 in egl::Display::destroyContext(egl::Thread\*, gl::Context\*) ./../../third\_party/angle/src/libANGLE/Display.cpp:1689:9  

#22 0x7fac201c2442 in egl::DestroyContext(egl::Thread\*, egl::Display\*, gl::Context\*) ./../../third\_party/angle/src/libGLESv2/egl\_stubs.cpp:284:5  

#23 0x7fac201cb9c0 in EGL\_DestroyContext ./../../third\_party/angle/src/libGLESv2/entry\_points\_egl\_autogen.cpp:182:12  

#24 0x7fac1f8bbaf3 in eglDestroyContext ./../../third\_party/angle/src/libEGL/libEGL\_autogen.cpp:117:12  

#25 0x5602dcd8b71d in gl::GLContextEGL::Destroy() ./../../ui/gl/gl\_context\_egl.cc:363:10  

#26 0x5602dcd8dad6 in ~GLContextEGL ./../../ui/gl/gl\_context\_egl.cc:558:3  

#27 0x5602dcd8dad6 in gl::GLContextEGL::~GLContextEGL() ./../../ui/gl/gl\_context\_egl.cc:557:31  

#28 0x5602dee3b980 in DeleteInternal[gl::GLContext](javascript:void(0);) ./../../base/memory/ref\_counted.h:355:5  

#29 0x5602dee3b980 in Destruct ./../../base/memory/ref\_counted.h:318:5  

#30 0x5602dee3b980 in Release ./../../base/memory/ref\_counted.h:344:7  

#31 0x5602dee3b980 in Release ./../../base/memory/scoped\_refptr.h:321:8  

#32 0x5602dee3b980 in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:223:7  

#33 0x5602dee3b980 in reset ./../../base/memory/scoped\_refptr.h:253:18  

#34 0x5602dee3b980 in operator= ./../../base/memory/scoped\_refptr.h:239:5  

#35 0x5602dee3b980 in gpu::gles2::GLES2DecoderPassthroughImpl::Destroy(bool) ./../../gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough.cc:1408:14  

#36 0x5602df2df5bc in gpu::CommandBufferStub::Destroy() ./../../gpu/ip

**Additional Comments:**

\*\*Chrome version: \*\* Chromium 101.0.4929.5 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.7 KB)
- [bug-1314383.txt](attachments/bug-1314383.txt) (text/plain, 30.4 KB)

## Timeline

### dt...@chromium.org (2022-04-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU]

### [Deleted User] (2022-04-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5386293286338560.

### rs...@chromium.org (2022-04-08)

I was able to reproduce this on Linux 102.0.4991.0 but not 101.0.4951.0. When I reproed it, ASan was able to get a full report rather than internal corruption (attached).

[Monorail components: Internals>GPU>ANGLE Internals>GPU>Vulkan]

### [Deleted User] (2022-04-08)

[Empty comment from Monorail migration]

### ad...@google.com (2022-04-08)

(auto-cc on security bug)

### [Deleted User] (2022-04-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2022-04-11)

Peng - can you help figure out if this is another issue with partition alloc? I don't have access to Linux ATM.

### pb...@google.com (2022-04-11)

We are cutting stable RC for M101 on April-19th-2022 which is 1 week away and this bug has been marked as M101 Stable blocker hence please request to review this bug and assess if this is indeed a M101 Stable blocker or not. If not, please remove the RBS label. If Blocker, please make sure to land the fix and request a merge to M101 release branch(http://go/chromebranches) ASAP. Thank you.

### pe...@chromium.org (2022-04-11)

[Comment Deleted]

[Monorail components: Internals>GPU>SwiftShader]

### pe...@chromium.org (2022-04-11)

I reproduced the original crash, but it is not the same crash in https://crbug.com/chromium/1314383#c4. Seems it is because swiftshader is freeing corrupted buffer.

BTW, I also saw some validation errors, not sure if it is related.


The reproduce command line is:
out/Release/chrome  --user-data-dir=/tmp/penghuang-chromium --enable-logging --disable-partial-raster \
	--enable-features=Vulkan,VulkanFromANGLE \
	--use-angle=swiftshader \
	--force-device-scale-factor=1 \
	--disable-vulkan-fallback-to-gl-for-testing \
	--enable-unsafe-webgpu \
	--use-webgpu-adapter=swiftshader \
	--ignore-gpu-blocklist  \
	--force-color-profile=scrgb-linear \
	--no-sandbox \
        crash.html



Validation errors:
[4090992:4090992:0411/123712.719741:ERROR:gpu_memory_buffer_support_x11.cc(44)] dri3 extension not supported.
ERR: RendererVk.cpp:774 (DebugUtilsMessenger): [ VUID-VkFramebufferCreateInfo-flags-04533 ] Validation Error: [ VUID-VkFramebufferCreateInfo-flags-04533 ] Object 0: handle = 0x560f0edfa640, type = VK_OBJECT_TYPE_DEVICE; | MessageID = 0xfe6b2428 | vkCreateFramebuffer(): VkFramebufferCreateInfo attachment #2 mip level 0 has width (32) smaller than the corresponding framebuffer width (40). The Vulkan spec states: If flags does not include VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT, each element of pAttachments that is used as an input, color, resolve, or depth/stencil attachment by renderPass must have been created with a VkImageCreateInfo::width greater than or equal to width (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-VkFramebufferCreateInfo-flags-04533)
                            Object: 0x560f0edfa640 (type = Device(3))

ERR: RendererVk.cpp:774 (DebugUtilsMessenger): [ VUID-VkFramebufferCreateInfo-flags-04533 ] Validation Error: [ VUID-VkFramebufferCreateInfo-flags-04533 ] Object 0: handle = 0x560f0edfa640, type = VK_OBJECT_TYPE_DEVICE; | MessageID = 0xfe6b2428 | vkCreateFramebuffer(): VkFramebufferCreateInfo attachment #2 mip level 0 has width (32) smaller than the corresponding framebuffer width (40). The Vulkan spec states: If flags does not include VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT, each element of pAttachments that is used as an input, color, resolve, or depth/stencil attachment by renderPass must have been created with a VkImageCreateInfo::width greater than or equal to width (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-VkFramebufferCreateInfo-flags-04533)
                            Object: 0x560f0edfa640 (type = Device(3))

ERR: RendererVk.cpp:774 (DebugUtilsMessenger): [ VUID-VkFramebufferCreateInfo-flags-04534 ] Validation Error: [ VUID-VkFramebufferCreateInfo-flags-04534 ] Object 0: handle = 0x560f0edfa640, type = VK_OBJECT_TYPE_DEVICE; | MessageID = 0x77e9b3aa | vkCreateFramebuffer(): VkFramebufferCreateInfo attachment #2 mip level 0 has height (32) smaller than the corresponding framebuffer height (40). The Vulkan spec states: If flags does not include VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT, each element of pAttachments that is used as an input, color, resolve, or depth/stencil attachment by renderPass must have been created with a VkImageCreateInfo::height greater than or equal to height (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-VkFramebufferCreateInfo-flags-04534)
                            Object: 0x560f0edfa640 (type = Device(3))

ERR: RendererVk.cpp:774 (DebugUtilsMessenger): [ VUID-VkFramebufferCreateInfo-flags-04534 ] Validation Error: [ VUID-VkFramebufferCreateInfo-flags-04534 ] Object 0: handle = 0x560f0edfa640, type = VK_OBJECT_TYPE_DEVICE; | MessageID = 0x77e9b3aa | vkCreateFramebuffer(): VkFramebufferCreateInfo attachment #2 mip level 0 has height (32) smaller than the corresponding framebuffer height (40). The Vulkan spec states: If flags does not include VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT, each element of pAttachments that is used as an input, color, resolve, or depth/stencil attachment by renderPass must have been created with a VkImageCreateInfo::height greater than or equal to height (https://www.khronos.org/registry/vulkan/specs/1.3-extensions/html/vkspec.html#VUID-VkFramebufferCreateInfo-flags-04534)
                            Object: 0x560f0edfa640 (type = Device(3))

### pe...@chromium.org (2022-04-11)

Hi sugoi@ could you please take a look? Thanks.

### su...@chromium.org (2022-04-11)

Actually, syoussefi@, these validation errors look legit and could lead to memory corruption in SwiftShader. Could you fix them? I'll have a look if this issue still reproduces after the validation errors are gone.

### sy...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a0b5299b6e9dc56f02d8765912e4cd47f3d6b91e

commit a0b5299b6e9dc56f02d8765912e4cd47f3d6b91e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Apr 12 04:38:50 2022

Vulkan: Fix resolve with subpass into smaller framebuffer

The condition to optimize resolve with subpass did not take into account
that the resolve area must match the render pass are, neither did it
disallow flipping and rotation.

Bug: angleproject:7196
Bug: chromium:1314383
Change-Id: I57e50da4d6e04dfebcce3c0a5061015e5ee8773b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3581055
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/a0b5299b6e9dc56f02d8765912e4cd47f3d6b91e/src/tests/gl_tests/BlitFramebufferANGLETest.cpp
[modify] https://crrev.com/a0b5299b6e9dc56f02d8765912e4cd47f3d6b91e/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/a0b5299b6e9dc56f02d8765912e4cd47f3d6b91e/src/tests/angle_end2end_tests_expectations.txt


### sy...@chromium.org (2022-04-13)

While I never got this crash, I did fix the validation errors with the change in https://crbug.com/chromium/1314383#c16, which were pointing to a real bug.

### sy...@chromium.org (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M101. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-13)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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

### gi...@appspot.gserviceaccount.com (2022-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b16a9fb56bf7f776727d87f3c402985c79d91fc

commit 6b16a9fb56bf7f776727d87f3c402985c79d91fc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 13 20:36:32 2022

Roll ANGLE from 19582d1201aa to 01c0bc215f4a (18 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/19582d1201aa..01c0bc215f4a

2022-04-13 jonahr@google.com Revert "Vulkan: Support Wayland"
2022-04-13 syoussefi@chromium.org Vulkan: Enum class instead of bool didRespecify
2022-04-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 345e2a278e69 to c9be322642fb (74 revisions)
2022-04-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 620982155d55 to 011bba68c819 (4 revisions)
2022-04-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from f961a0d4732b to 61150a1970a3 (431 revisions)
2022-04-13 gman@chromium.org Metal:Speed up BGRA8 to RGBA8 copy for readPixels
2022-04-13 syoussefi@chromium.org Remove feature override platform methods
2022-04-13 syoussefi@chromium.org Vulkan: Fix resolve with subpass into smaller framebuffer
2022-04-12 yuxinhu@google.com Fix Geometry Shader Conformance Test Failure on Pixel6
2022-04-12 penghuang@chromium.org Use the real max vertex attrib index instead of MAX_VERTEX_ATTRIBS
2022-04-12 sunnyps@chromium.org vulkan: Mark external memory textures as preinitialized
2022-04-12 ynovikov@chromium.org Suppress multisample_interpolation dEQP failures on Pixel 6 Vulkan
2022-04-12 senorblanco@chromium.org D3D: Remove a pass-through function.
2022-04-12 cclao@google.com Vulkan: Change ContextVk to Context for BufferPool APIs
2022-04-12 antonio.caggiano@collabora.com Vulkan: Support Wayland
2022-04-12 ynovikov@chromium.org Roll chromium_revision f89964bd5b..f961a0d473 (990903:991486)
2022-04-12 steven@valvesoftware.com egl_angle_ext: add more missing extension enum values
2022-04-12 ynovikov@chromium.org Update ANGLE's docs regarding Windows 10 SDK version to use

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
Bug: chromium:1258869,chromium:1292528,chromium:1314383
Tbr: jonahr@google.com
Change-Id: Ia3a5408f945c1a0439fd81932b3f5f1a20bb3a73
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3585833
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#992209}

[modify] https://crrev.com/6b16a9fb56bf7f776727d87f3c402985c79d91fc/DEPS


### sy...@chromium.org (2022-04-15)

1. Security issue
2. https://chromium-review.googlesource.com/c/angle/angle/+/3581055
3. Change is live in Chrome since "Apr 13, 2022, 4:37 PM EDT"
4. No
5. N/A
6. N/A

### am...@chromium.org (2022-04-16)

m101 merge approved, please merge this fix to branch 4951 NLT 10am PDT, Tuesday 19 April so this fix can be included in M101 stable cut 

### sy...@chromium.org (2022-04-19)

Done

### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0a684b5a44348b54498f009c232e2591f16a0c87

commit 0a684b5a44348b54498f009c232e2591f16a0c87
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Apr 12 04:38:50 2022

M101: Vulkan: Fix resolve with subpass into smaller framebuffer

The condition to optimize resolve with subpass did not take into account
that the resolve area must match the render pass are, neither did it
disallow flipping and rotation.

Bug: angleproject:7196
Bug: chromium:1314383
Change-Id: I63e4a032d0b717b0550c0319186c5563fd076d88
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3594101
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/0a684b5a44348b54498f009c232e2591f16a0c87/src/tests/gl_tests/BlitFramebufferANGLETest.cpp
[modify] https://crrev.com/0a684b5a44348b54498f009c232e2591f16a0c87/src/libANGLE/renderer/vulkan/FramebufferVk.cpp
[modify] https://crrev.com/0a684b5a44348b54498f009c232e2591f16a0c87/src/tests/angle_end2end_tests_expectations.txt


### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in hunting for GPU process memory corruption bugs and nice work! 

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1314383?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU, Internals>GPU>ANGLE, Internals>GPU>SwiftShader, Internals>GPU>Vulkan]
[Monorail blocked-on: crbug.com/angleproject/7196]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059319)*
