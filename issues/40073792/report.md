# UAF in vk::Buffer::getOffsetPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40073792](https://issues.chromium.org/issues/40073792) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2023-09-29 |
| **Bounty** | $11,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:

- ubuntu 22.04

tested chrome version:

- Chromium 119.0.6034.6(build with asan)
- Chromium 119.0.6039.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1203313.zip)

Repro Steps:  

./chrome --disable-gpu --user-data-dir=/tmp/xx7 <http://localhost:8000/poc.html>

Bisect:  

This problem is introduced in this commit:<https://chromium.googlesource.com/angle/angle/+/1b450b92c561735d4ed6c24b7b0fdfa529de2bbc>  

<https://chromium-review.googlesource.com/c/angle/angle/+/4864003>  

According to the chromiumdash, this proble affects DEV version after 119.0.6034.6.

**Problem Description:**  

==3039323==ERROR: AddressSanitizer: heap-use-after-free on address 0x50700009bbb8 at pc 0x7f6a7e29884d bp 0x7f6a6bd5fed0 sp 0x7f6a6bd5fec8  

READ of size 8 at 0x50700009bbb8 thread T17  

#0 0x7f6a7e29884c in vk::Buffer::getOffsetPointer(unsigned long) const ./../../third\_party/swiftshader/src/Vulkan/VkBuffer.cpp:151:37  

#1 0x7f6a7e3b2041 in vk::Inputs::bindVertexInputs(int, bool) ./../../third\_party/swiftshader/src/Device/Context.cpp:337:61  

#2 0x7f6a7e2a8fd2 in (anonymous namespace)::CmdDrawBase::draw(vk::CommandBuffer::ExecutionState&, bool, unsigned int, unsigned int, unsigned int, int, unsigned int) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:933:10  

#3 0x7f6a7e2a8dc9 in (anonymous namespace)::CmdDraw::execute(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:985:3  

#4 0x7f6a7e2a2bc3 in vk::CommandBuffer::submit(vk::CommandBuffer::ExecutionState&) ./../../third\_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:2330:12  

#5 0x7f6a7e2fcc08 in vk::Queue::submitQueue(vk::Queue::Task const&) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:104:42  

#6 0x7f6a7e2fbbd0 in vk::Queue::taskLoop(marl::Scheduler\*) ./../../third\_party/swiftshader/src/Vulkan/VkQueue.cpp:156:4  

#7 0x7f6a7e2ff4e1 in \_\_invoke<void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, void> ./../../third\_party/libc++/src/include/\_\_type\_traits/invoke.h:312:25  

#8 0x7f6a7e2ff4e1 in \_\_thread\_execute<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);) >, void (vk::Queue::\*)(marl::Scheduler \*), vk::Queue \*, marl::Scheduler \*, 2UL, 3UL> ./../../third\_party/libc++/src/include/\_\_thread/thread.h:221:5  

#9 0x7f6a7e2ff4e1 in void\* std::\_\_Cr::\_\_thread\_proxy<std::\_\_Cr::tuple<std::\_\_Cr::unique\_ptr<std::\_\_Cr::\_\_thread\_struct, std::\_\_Cr::default\_delete[std::\_\_Cr::\_\_thread\_struct](javascript:void(0);)>, void (vk::Queue::\*)(marl::Scheduler\*), vk::Queue\*, marl::Scheduler\*>>(void\*) ./../../third\_party/libc++/src/include/\_\_thread/thread.h:232:5  

#10 0x5602f5d95148 in asan\_thread\_start(void\*) *asan\_rtl*:28

0x50700009bbb8 is located 8 bytes inside of 80-byte region [0x50700009bbb0,0x50700009bc00)  

freed by thread T0 (chrome) here:  

#0 0x5602f5d97116 in \_\_interceptor\_free *asan\_rtl*:3  

#1 0x7f6aa02ff47f in destroy ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_wrapper.h:1645:9  

#2 0x7f6aa02ff47f in rx::RendererVk::collectSuballocationGarbage(rx::vk::ResourceUse const&, rx::vk::BufferSuballocation&&, rx::vk::Buffer&&) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/RendererVk.h:386:20  

#3 0x7f6aa02ff202 in rx::vk::BufferHelper::onBufferUserSizeChange(rx::RendererVk\*) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/vk\_helpers.cpp:5011:19  

#4 0x7f6aa0029540 in rx::BufferVk::setDataWithMemoryType(gl::Context const\*, gl::BufferBinding, void const\*, unsigned long, unsigned int, gl::BufferUsage) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:440:17  

#5 0x7f6aa0028b3e in rx::BufferVk::setDataWithUsageFlags(gl::Context const\*, gl::BufferBinding, void\*, void const\*, unsigned long, gl::BufferUsage, unsigned int) ./../../third\_party/angle/src/libANGLE/renderer/vulkan/BufferVk.cpp:390:12  

#6 0x7f6aa0484975 in gl::Buffer::bufferDataImpl(gl::Context\*, gl::BufferBinding, void const\*, long, gl::BufferUsage, unsigned int) ./../../third\_party/angle/src/libANGLE/Buffer.cpp:143:16  

#7 0x7f6aa0484d63 in gl::Buffer::bufferData(gl::Context\*, gl::BufferBinding, void const\*, long, gl::BufferUsage) ./../../third\_party/angle/src/libANGLE/Buffer.cpp:107:12  

#8 0x560310876936 in gpu::gles2::GLES2DecoderPassthroughImpl::DoBufferData(unsigned int, long, void const\*, unsigned int) ./../../gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough\_doers.cc:667:10  

#9 0x56031079d9d5 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile\*, int, int\*) ./../../gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough.cc:736:20  

#10 0x560310c6bedb in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface\*) ./../../gpu/command\_buffer/service/command\_buffer\_service.cc:232:35  

#11 0x560310c5a6e9 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::\_\_Cr::vector<gpu::SyncToken, std::\_\_Cr::allocator[gpu::SyncToken](javascript:void(0);)> const&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:507:22  

#12 0x560310c598eb in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command\_buffer\_stub.cc:153:7  

#13 0x560310c783fe in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)) ./../../gpu/ipc/service/gpu\_channel.cc:752:13  

#14 0x560310c89b0a in void base::internal::FunctorTraits<void (gpu::GpuChannel::\*)(mojo::StructPtr[gpu::mojom::DeferredRequestParams](javascript:void(0);)), void>::Invoke<void (gpu::GpuChannel::\*)(mojo::StructPtr<gpu::m

**Additional Comments:**

\*\*Chrome version: \*\* 119.0.6034.6 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.4 KB)

## Timeline

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-09-29)

Thank you for the report!

sugoi@chromium.org, could you help further triage this issue? Thanks!

[Monorail components: Internals>GPU>SwiftShader]

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-09-29)

This looks like ANGLE's garbage collector disposing of a resource that SwiftShader is still currently using, which looks like a duplicate of 1223346.

### [Deleted User] (2023-09-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-30)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### cc...@google.com (2023-10-03)

This is ANGLE bug.  I can't reproduce the bug with the attached html file, (likely due to I just dont know how to use chrome). But based on my code reading and investigation, I believe I know what likely happening here. I also added my own end2end test to demonstrate the bug.

Basically when someone called glBufferData with different size, vulkan backend may decide to reuse the underline memory (if size is big enough etc). When this happens, if robust access is enabled (which chomium does), we will still recreate a VkBuffer object with the new size and bind to the same memory, so that vulkan driver can use the size to do bounds check. The bug here is that if this buffer is bound to two VAOs, we also has to notify VAOs so that VAOs will pick up the buffer change. That "notification" was missing in previous CL. We also needs to bump the buffer's unique serial so that when others check the serial to see if it needs to update, it will detect the change and update accordingly. 



### gi...@appspot.gserviceaccount.com (2023-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7f5143c292457e1f91cdd9679d329990c6beae1d

commit 7f5143c292457e1f91cdd9679d329990c6beae1d
Author: Charlie Lao <cclao@google.com>
Date: Mon Oct 02 22:38:15 2023

Vulkan: Notify VAO when VBO's mBufferWithUserSize changed.

When buffer robust access is enabled, and bufferData is called with
different size and we end up reusing the underline storage, we will have
to recreate VkBuffer with user's size, and driver is relying on
VkBuffer's size to implement robust access. The bug here is that we
notify VAO when storage changes. But when storage is reused and we have
dedicated VkBufer with user size and that VkBuffer changed, we were not
notifying the VAO. This CL adds that notification so that VAO gets
notified and dirty bits processed and its cache of VkBuffer gets updated

Bug: chromium:1488055
Bug: b/303138134
Change-Id: Ie693c92c2edde9a22a41a25f5bde493397550d95
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4906568
Reviewed-by: Yuxin Hu <yuxinhu@google.com>
Commit-Queue: Charlie Lao <cclao@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/7f5143c292457e1f91cdd9679d329990c6beae1d/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/7f5143c292457e1f91cdd9679d329990c6beae1d/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp
[modify] https://crrev.com/7f5143c292457e1f91cdd9679d329990c6beae1d/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/7f5143c292457e1f91cdd9679d329990c6beae1d/src/libANGLE/renderer/vulkan/BufferVk.cpp


### cc...@google.com (2023-10-03)

Could someone verify the above CL actually fix the poc.html?

### gi...@appspot.gserviceaccount.com (2023-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5975d0b022dcdec3526d762ea8c5fc36aa929686

commit 5975d0b022dcdec3526d762ea8c5fc36aa929686
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Oct 03 22:43:54 2023

Roll ANGLE from 4ace4da1c446 to 1eccf863d302 (9 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/4ace4da1c446..1eccf863d302

2023-10-03 romanl@google.com Handle non-debuggable com.android.angle.test on device
2023-10-03 romanl@google.com Add missed include <atomic>
2023-10-03 abdolrashidi@google.com Revert "Add VMA version to logcat"
2023-10-03 cclao@google.com Vulkan: Notify VAO when VBO's mBufferWithUserSize changed.
2023-10-03 yuxinhu@google.com Enable multisample deqp tests on bots
2023-10-03 syoussefi@chromium.org Capture/Replay: Disable VK_EXT_host_image_copy during capture
2023-10-03 syoussefi@chromium.org Vulkan: Do host image copy without holding the share group lock
2023-10-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 7f4d495c89c2 to 5b6f768198ce (1 revision)
2023-10-03 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 8a3d372ccd3c to 07002c74826e (635 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,romanl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1488055
Tbr: romanl@google.com
Change-Id: I1fb68bb62c01c865ab4ea2f8c547212e6dc44f1b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4909426
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1204907}

[modify] https://crrev.com/5975d0b022dcdec3526d762ea8c5fc36aa929686/DEPS
[modify] https://crrev.com/5975d0b022dcdec3526d762ea8c5fc36aa929686/third_party/angle


### em...@gmail.com (2023-10-04)

#12
I have verified locally, and after applying the patch, the issue was not reproduced again.
- tested chrome version:
Chromium 119.0.6034.6

build options:
- args.gn
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false

### cc...@google.com (2023-10-04)

Thanks Emily for verifying, good to hear that it fixed the issue! 

### pb...@google.com (2023-10-04)

[BULK EDIT] M119 Stable RC cut date is just two weeks away i.e., Oct 24th, Please evaluate the releaseblocker and get the needed fix asap. Please consider this as a high priority issue as the Stable promotion is fast approaching.

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-10)

119 merge approved for https://crrev.com/c/4906568, please merge this fix to branch 6045 at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2023-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5cff2421ef225d14d3a4253b81073389fc840024

commit 5cff2421ef225d14d3a4253b81073389fc840024
Author: Charlie Lao <cclao@google.com>
Date: Mon Oct 02 22:38:15 2023

M119: Vulkan: Notify VAO when VBO's mBufferWithUserSize changed.

When buffer robust access is enabled, and bufferData is called with
different size and we end up reusing the underline storage, we will have
to recreate VkBuffer with user's size, and driver is relying on
VkBuffer's size to implement robust access. The bug here is that we
notify VAO when storage changes. But when storage is reused and we have
dedicated VkBufer with user size and that VkBuffer changed, we were not
notifying the VAO. This CL adds that notification so that VAO gets
notified and dirty bits processed and its cache of VkBuffer gets updated

Bug: chromium:1488055
Bug: b/303138134
Change-Id: I2ab92ed7b1f3e8646045733d118139d1e8da1b81
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4928408
Reviewed-by: Kenneth Russell <kbr@chromium.org>

[modify] https://crrev.com/5cff2421ef225d14d3a4253b81073389fc840024/src/libANGLE/renderer/vulkan/vk_helpers.h
[modify] https://crrev.com/5cff2421ef225d14d3a4253b81073389fc840024/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp
[modify] https://crrev.com/5cff2421ef225d14d3a4253b81073389fc840024/src/libANGLE/renderer/vulkan/vk_helpers.cpp
[modify] https://crrev.com/5cff2421ef225d14d3a4253b81073389fc840024/src/libANGLE/renderer/vulkan/BufferVk.cpp


### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-18)

Congratulations! The Chrome VRP Panel has decided to award you $10,000 for this report of a bug in the GPU process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 
This issue appears to only potentially allow for read from the buffer rather than demonstrating more severe memory corruption such as attacker control of a value or RCE. Please be aware that these types of issues / reports may be eligible for lower rewards in the future. Thank you! 


### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1488055?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073792)*
