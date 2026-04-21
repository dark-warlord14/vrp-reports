# Security: webgl heap-use-after-free in BitSetT

| Field | Value |
|-------|-------|
| **Issue ID** | [40057825](https://issues.chromium.org/issues/40057825) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-11-04 |
| **Bounty** | $5,000.00 |

## Description

Version 95.0.4638.69
On Windows 10 - Chrome Stable Version 95.0.4638.69
has to be launched using --no-sandbox --disable-gpu-sandbox --disable-gpu

2:037> r
rax=feeefeeefeeefeee rbx=feeefeeefeeefeee rcx=000000850bffdce0
rdx=0000000000000000 rsi=00000205dbc47ff0 rdi=00000205db39b938
rip=00007ffbb1d26b42 rsp=000000850bffdba0 rbp=000000850bffde20
 r8=0000000000000000  r9=0000000000000000 r10=0000000000000003
r11=000000850bffdc40 r12=0000000000000000 r13=0000000000000000
r14=0000000000000001 r15=00000205db39b6b0
iopl=0         nv up ei pl zr na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
libglesv2!angle::BitSetT<8,unsigned char,unsigned long long>::BitSetT [inlined in libglesv2!rx::FramebufferVk::startNewRenderPass+0xb2]:
00007ffb`b1d26b42 448aa0a0000000  mov     r12b,byte ptr [rax+0A0h] ds:feeefeee`feeeff8e=??
2:037> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     libglesv2!angle::BitSetT<8,unsigned char,unsigned long long>::BitSetT [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\common\bitset_utils.h @ 194] 
01 (Inline Function) --------`--------     libglesv2!gl::FramebufferState::getColorAttachmentsMask [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.h @ 93] 
02 00000085`0bffdba0 00007ffb`b1d12243     libglesv2!rx::FramebufferVk::startNewRenderPass+0xb2 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 2430] 
03 00000085`0bffdd90 00007ffb`b1d21072     libglesv2!rx::ContextVk::startRenderPass+0x33 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 5566] 
04 (Inline Function) --------`--------     libglesv2!rx::FramebufferVk::flushDeferredClears+0x64 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 2821] 
05 00000085`0bffddf0 00007ffb`b1d20eb3     libglesv2!rx::FramebufferVk::invalidateImpl+0x192 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 1557] 
06 00000085`0bffdea0 00007ffb`b192d26f     libglesv2!rx::FramebufferVk::invalidate+0x93 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\FramebufferVk.cpp @ 376] 
07 00000085`0bffdf40 00007ffb`a1218260     libglesv2!GL_InvalidateFramebuffer+0x8f [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp @ 1657] 
08 00000085`0bffdfa0 00007ffb`9affa692     chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3e394b0
09 00000085`0bffe010 00007ffb`9a851c05     chrome!ChromeMain+0x449e82
0a 00000085`0bffe080 00007ffb`9a850cf9     chrome!Ordinal0+0x5b1c05
0b 00000085`0bffe190 00007ffb`9a8509fc     chrome!Ordinal0+0x5b0cf9
0c 00000085`0bffe2d0 00007ffb`9aefaaa9     chrome!Ordinal0+0x5b09fc
0d 00000085`0bffe370 00007ffb`9c382513     chrome!ChromeMain+0x34a299
0e 00000085`0bffe3c0 00007ffb`9ca3dd2d     chrome!GetHandleVerifier+0xc40d63
0f 00000085`0bffe500 00007ffb`9ca3ce43     chrome!GetHandleVerifier+0x12fc57d
10 00000085`0bffe650 00007ffb`9b73fbe9     chrome!GetHandleVerifier+0x12fb693
11 00000085`0bffe7d0 00007ffb`9abf2726     chrome!ChromeMain+0xb8f3d9
12 00000085`0bffe880 00007ffb`9acd7326     chrome!ChromeMain+0x41f16
13 00000085`0bffe8f0 00007ffb`9d337fae     chrome!ChromeMain+0x126b16
14 00000085`0bffea00 00007ffb`9ab9a8b9     chrome!IsSandboxedProcess+0x6920e
15 00000085`0bffed80 00007ffb`9abb1962     chrome!Ordinal0+0x8fa8b9
16 00000085`0bffee50 00007ffb`9abb099f     chrome!ChromeMain+0x1152
17 00000085`0bfff040 00007ff7`74535742     chrome!ChromeMain+0x18f
18 00000085`0bfff150 00007ff7`745352dc     chrome_exe!MainDllLoader::Launch+0x302 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169] 
19 00000085`0bfff3d0 00007ff7`7457ca92     chrome_exe!wWinMain+0xc1c [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382] 
1a (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
1b 00000085`0bfff800 00007ffc`4cd17034     chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
1c 00000085`0bfff840 00007ffc`4cf02651     KERNEL32!BaseThreadInitThunk+0x14
1d 00000085`0bfff870 00000000`00000000     ntdll!RtlUserThreadStart+0x21

Also attached ASAN log from asan-linux-release-936833.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 17.0 KB)
- [BitSetT.html](attachments/BitSetT.html) (text/plain, 2.5 KB)

## Timeline

### [Deleted User] (2021-11-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5690983964278784.

### cl...@chromium.org (2021-11-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5162812240101376.

### va...@chromium.org (2021-11-05)

$ builds/asan-linux-release-936833/asan-linux-release-936833/chrome pocs/1267027/BitSetT.html

==2133773==ERROR: AddressSanitizer: heap-use-after-free on address 0x61700005de1e at pc 0x7f6a990277e1 bp 0x7ffe0dd006b0 sp 0x7ffe0dd006a8            [124/5841]
READ of size 1 at 0x61700005de1e thread T0 (chrome)                                                                                                             
    #0 0x7f6a990277e0 in BitSetT third_party/angle/src/common/bitset_utils.h:193:82                                                                             
    #1 0x7f6a990277e0 in getColorUnresolveAttachmentMask third_party/angle/src/libANGLE/renderer/vulkan/vk_cache_utils.h:179:16                                 
    #2 0x7f6a990277e0 in rx::FramebufferVk::startNewRenderPass(rx::ContextVk*, gl::Rectangle const&, rx::vk::priv::SecondaryCommandBuffer**, bool*) third_party/
angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:2416:25
    #3 0x7f6a98fe1e2d in rx::ContextVk::startRenderPass(gl::Rectangle, rx::vk::priv::SecondaryCommandBuffer**, bool*) third_party/angle/src/libANGLE/renderer/vu
lkan/ContextVk.cpp:5587:5
    #4 0x7f6a99013c1f in flushDeferredClears third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:2819:23
    #5 0x7f6a99013c1f in rx::FramebufferVk::invalidateImpl(rx::ContextVk*, unsigned long, unsigned int const*, bool, gl::Rectangle const&) third_party/angle/src
/libANGLE/renderer/vulkan/FramebufferVk.cpp:1557:5
    #6 0x7f6a99013624 in rx::FramebufferVk::invalidate(gl::Context const*, unsigned long, unsigned int const*) third_party/angle/src/libANGLE/renderer/vulkan/Fr
amebufferVk.cpp:376:5
    #7 0x7f6a98941a6f in GL_InvalidateFramebuffer third_party/angle/src/libGLESv2/entry_points_gles_3_0_autogen.cpp:1739:22
    #8 0x55ae1eef02f5 in gpu::gles2::GLES2DecoderPassthroughImpl::DoDiscardFramebufferEXT(unsigned int, int, unsigned int const volatile*) gpu/command_buffer/se
rvice/gles2_cmd_decoder_passthrough_doers.cc
    #9 0x55ae1ee877ef in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/com
mand_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #10 0x55ae1f2fd575 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:70:18
    #11 0x55ae1f2f106f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)
 gpu/ipc/service/command_buffer_stub.cc:500:22
    #12 0x55ae1f2f0619 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) gpu/ipc/service/command_buffer_stub.cc
:152:7
    #13 0x55ae1f304052 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) gpu/ipc/service/gpu_channel.cc:666:13
    #14 0x55ae1f31089e in Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<
gpu::mojom::DeferredRequestParams> > base/bind_internal.h:569:12
    #15 0x55ae1f31089e in void base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),
 base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestPar
ams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) base/bind_internal.h:769:5
    #16 0x55ae1dd0f7b7 in Run base/callback.h:142:12
    #17 0x55ae1dd0f7b7 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:685:26
    #18 0x55ae1970af03 in Run base/callback.h:142:12
    #19 0x55ae1970af03 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:157:32
    #20 0x55ae19746d98 in RunTask<> base/task/common/task_annotator.h:115:5
    #21 0x55ae19746d98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence
_manager/thread_controller_with_message_pump_impl.cc:354:21
    #22 0x55ae19746747 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_mess
age_pump_impl.cc:261:30
    #23 0x55ae197474d1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread
_controller_with_message_pump_impl.cc
    #24 0x55ae19602af9 in HandleDispatch base/message_loop/message_pump_glib.cc:375:46
    #25 0x55ae19602af9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:125:43
    #26 0x7f6aa1bd2d0a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x53d0a)

[Monorail components: Internals>GPU>ANGLE]

### va...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-05)

Can repro with 929513

### va...@chromium.org (2021-11-05)

Chromium	96.0.4664.0 (Developer Build) (64-bit)
Revision	85b0bd07c2597f03beeefb8b33fcfcee47dc6937-refs/heads/main@{#929513}
OS	Linux
JavaScript	V8 9.6.180

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-05)

Cannot repro with:
Chromium	95.0.4638.0 (Developer Build) (64-bit)
Revision	dc211eb1afdb62dd0152b9f1875d060b9e907e80-refs/heads/main@{#920005}


### [Deleted User] (2021-11-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-05)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/0e20c68092c68367c9b42c0e74ee592183d44c29

commit 0e20c68092c68367c9b42c0e74ee592183d44c29
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 20:24:09 2021

Sync framebuffer bindings in glInvalidateFramebuffer

If a framebuffer binding change is followed by glInvalidateFramebuffer,
ANGLE was not syncing the framebuffer binding.

- This means that invalidation was being done on the previous
  framebuffer.
- Paired with deferred clears, this was causing ContextVk to start a
  render pass on the previous, potentially deleted, framebuffer.

Bug: chromium:1267027
Change-Id: I092a0c8dd764db9e49258b694c970babb19cf24b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266175
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/libANGLE/angletypes.h
[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/libANGLE/Context.h
[modify] https://crrev.com/0e20c68092c68367c9b42c0e74ee592183d44c29/src/libANGLE/Context.cpp


### sy...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-11-09)

1. It's a security fix
2. https://chromium-review.googlesource.com/c/angle/angle/+/3266175
3. No. The ANGLE autoroller is currently blocked on another failure.
4. No
5. N/A
6. N/A

I'll make sure the ANGLE autoroller is fixed by tomorrow. If the release can afford waiting a few days for 3, that would be ideal. Note that I have a few other security bugs in queue that should land tomorrow and they would be in the same boat.

### am...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/944b0b14709dbedbb76d4633147662020e329bfa

commit 944b0b14709dbedbb76d4633147662020e329bfa
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 09 17:05:21 2021

Roll ANGLE from f16d7b9ceefb to 67a8cf07a740 (13 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/f16d7b9ceefb..67a8cf07a740

2021-11-09 jmadill@chromium.org Revert "Metal: Reintroduce GPU power preference selection code."
2021-11-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 4c6da56da96c to 7e9b8b317f16 (6 revisions)
2021-11-09 gert.wollny@collabora.com Capture/Replay: Don't force initialization of FS inout vars
2021-11-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from f1944afd4c24 to 76a46804f683 (1053 revisions)
2021-11-09 gert.wollny@collabora.com Capture/Replay: Limit the sleep time based on unfinished jobs
2021-11-09 msisov@igalia.com Reland "rename use_x11 to ozone_platform_x11"
2021-11-09 timvp@google.com Vulkan: Add flushCommandsAndEndRenderPassWithoutQueueSubmit()
2021-11-09 timvp@google.com Vulkan: Use optimalBufferCopyOffsetAlignment
2021-11-08 syoussefi@chromium.org Sync framebuffer bindings in glInvalidateFramebuffer
2021-11-08 jmadill@chromium.org infra: Switch ASAN to 64-bit on Windows.
2021-11-08 syoussefi@chromium.org Capture/Replay: Skip test of new failing tests
2021-11-08 jonahr@google.com Metal: Reintroduce GPU power preference selection code.
2021-11-08 syoussefi@chromium.org Vulkan: Fix spammy best practices message

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
Bug: chromium:1096425,chromium:1267027
Tbr: jmadill@google.com
Change-Id: Iaa1cd5ff9cbd6f4175080eb6a87753152ee393d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3270769
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#939881}

[modify] https://crrev.com/944b0b14709dbedbb76d4633147662020e329bfa/DEPS


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fa338f3bcf82d78f44517f9c7dffc90839229c8b

commit fa338f3bcf82d78f44517f9c7dffc90839229c8b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 20:24:09 2021

Canary: Sync framebuffer bindings in glInvalidateFramebuffer

If a framebuffer binding change is followed by glInvalidateFramebuffer,
ANGLE was not syncing the framebuffer binding.

- This means that invalidation was being done on the previous
  framebuffer.
- Paired with deferred clears, this was causing ContextVk to start a
  render pass on the previous, potentially deleted, framebuffer.

Bug: chromium:1267027
Change-Id: I092a0c8dd764db9e49258b694c970babb19cf24b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266175
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270994
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/libANGLE/angletypes.h
[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/libANGLE/Context.h
[modify] https://crrev.com/fa338f3bcf82d78f44517f9c7dffc90839229c8b/src/libANGLE/Context.cpp


### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### sr...@google.com (2021-11-10)

Merge approved for M96 branch:4664 pls merge asap

### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b

commit d61c6de21e1485754dbbb7ae4eb2e12f2cad231b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 20:24:09 2021

M96: Sync framebuffer bindings in glInvalidateFramebuffer

If a framebuffer binding change is followed by glInvalidateFramebuffer,
ANGLE was not syncing the framebuffer binding.

- This means that invalidation was being done on the previous
  framebuffer.
- Paired with deferred clears, this was causing ContextVk to start a
  render pass on the previous, potentially deleted, framebuffer.

Bug: chromium:1267027
Change-Id: I092a0c8dd764db9e49258b694c970babb19cf24b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266175
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270994
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271001

[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/libANGLE/angletypes.h
[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/libANGLE/Context.cpp
[modify] https://crrev.com/d61c6de21e1485754dbbb7ae4eb2e12f2cad231b/src/libANGLE/Context.h


### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fc379ea0f411050557a73626defd529cf17d6f52

commit fc379ea0f411050557a73626defd529cf17d6f52
Author: Geoff Lang <geofflang@google.com>
Date: Wed Nov 10 21:52:43 2021

M96: Fix compilation error in usage of Context::syncDirtyBits

Bug: chromium:1267027
Change-Id: Id18a6ab39b721e2212eb3f1eb48d33e6bec3bee5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270756
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/fc379ea0f411050557a73626defd529cf17d6f52/src/libANGLE/Context.cpp


### am...@chromium.org (2021-11-11)

Merge approved for M97; please go ahead and merge to branch 4692 as soon as possible. Thanks! 


### gi...@appspot.gserviceaccount.com (2021-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/b79b2b1d26041600954090182fa41cc829e20dbf

commit b79b2b1d26041600954090182fa41cc829e20dbf
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Nov 08 20:24:09 2021

M97: Sync framebuffer bindings in glInvalidateFramebuffer

If a framebuffer binding change is followed by glInvalidateFramebuffer,
ANGLE was not syncing the framebuffer binding.

- This means that invalidation was being done on the previous
  framebuffer.
- Paired with deferred clears, this was causing ContextVk to start a
  render pass on the previous, potentially deleted, framebuffer.

Bug: chromium:1267027
Change-Id: I092a0c8dd764db9e49258b694c970babb19cf24b
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3266175
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3270994
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3271001
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3276038

[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/libANGLE/angletypes.h
[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/libANGLE/Context.cpp
[modify] https://crrev.com/b79b2b1d26041600954090182fa41cc829e20dbf/src/libANGLE/Context.h


### sy...@chromium.org (2021-11-12)

Done

### pb...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-16)

ClusterFuzz testcase 5690983964278784 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for reporting this finding to us!! 

### sy...@chromium.org (2021-11-19)

The clusterfuzz failures seem completely different now. If there is a true failure here, it's a separate issue. I reran both https://clusterfuzz.com/testcase-detail/5162812240101376 and https://clusterfuzz.com/testcase-detail/5690983964278784 and will open a new bug if they continue to fail.

### sy...@chromium.org (2021-11-19)

I see the same failure in crbug.com/1267424, so I'm fairly certain it's an unrelated issue with ToT chrome itself.

### sy...@chromium.org (2021-11-20)

New failures are unrelated and are tracked in crbug.com/1267697

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267027?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057825)*
