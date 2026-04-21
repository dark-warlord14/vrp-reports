# Security: webgl global-buffer-overflow in getIncompleteTexture

| Field | Value |
|-------|-------|
| **Issue ID** | [40058015](https://issues.chromium.org/issues/40058015) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Vulkan |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | lf...@google.com |
| **Created** | 2021-11-25 |
| **Bounty** | $5,000.00 |

## Description

Tested on Version 96.0.4664.45 (Official Build) (64-bit) on Windows 11 and asan-win32-release_x64-936776.

Flags used --no-sandbox --disable-gpu

(6988.33b4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
00000000`00000000 ??              ???
2:037> k
 # Child-SP          RetAddr               Call Site
00 00000012`115fd778 00007ffe`aadb5270     0x0
01 (Inline Function) --------`--------     libglesv2!rx::vk::Format::getTextureLoadFunction+0x4f [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_format_utils.h @ 115] 
02 00000012`115fd780 00007ffe`aadb64b2     libglesv2!rx::vk::ImageHelper::stageSubresourceUpdateImpl+0xb0 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 5605] 
03 00000012`115fd9a0 00007ffe`aad7837c     libglesv2!rx::vk::ImageHelper::stageSubresourceUpdate+0x132 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 6055] 
04 00000012`115fda80 00007ffe`aad77edb     libglesv2!rx::TextureVk::setSubImageImpl+0x47c [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp @ 549] 
05 00000012`115fdbd0 00007ffe`aaa0de33     libglesv2!rx::TextureVk::setSubImage+0xab [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\TextureVk.cpp @ 339] 
06 00000012`115fdc80 00007ffe`aaa6a064     libglesv2!gl::Texture::setSubImage+0xf3 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Texture.cpp @ 1241] 
07 00000012`115fdd30 00007ffe`aad3ed09     libglesv2!rx::IncompleteTextureSet::getIncompleteTexture+0x264 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\renderer_utils.cpp @ 650] 
08 (Inline Function) --------`--------     libglesv2!rx::ContextVk::getIncompleteTexture+0x27 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 650] 
09 00000012`115fde50 00007ffe`aad3c3f8     libglesv2!rx::ContextVk::updateActiveTextures+0x239 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 5024] 
0a (Inline Function) --------`--------     libglesv2!rx::ContextVk::invalidateCurrentTextures+0x3c [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 4159] 
0b 00000012`115fe030 00007ffe`aa9640de     libglesv2!rx::ContextVk::syncState+0x998 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 3743] 
0c (Inline Function) --------`--------     libglesv2!gl::Context::syncDirtyBits+0x21 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.inl.h @ 90] 
0d (Inline Function) --------`--------     libglesv2!gl::Context::prepareForDraw+0xa9 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.inl.h @ 119] 
0e (Inline Function) --------`--------     libglesv2!gl::Context::drawArrays+0x188 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.inl.h @ 131] 
0f 00000012`115fe130 00007ffe`7fe5896b     libglesv2!GL_DrawArrays+0x20e [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp @ 1063] 
10 00000012`115fe1b0 00007ffe`7fea77f3     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays+0x3b [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc @ 1217] 
11 (Inline Function) --------`--------     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl+0xcc [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 858] 
12 00000012`115fe200 00007ffe`7ffba2b5     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands+0xf3 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 796] 
13 00000012`115fe280 00007ffe`7ffb96c4     chrome!gpu::CommandBufferService::Flush+0xe5 [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc @ 73] 
14 (Inline Function) --------`--------     chrome!gpu::CommandBufferStub::OnAsyncFlush+0xb0 [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 500] 
15 00000012`115fe390 00007ffe`835e9a4c     chrome!gpu::CommandBufferStub::ExecuteDeferredRequest+0x154 [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 152] 
16 00000012`115fe4d0 00007ffe`835e9960     chrome!gpu::GpuChannel::ExecuteDeferredRequest+0xcc [C:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc @ 669] 
17 (Inline Function) --------`--------     chrome!base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),void>::Invoke+0x56 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509] 
18 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x6d [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 668] 
19 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunImpl+0x6d [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721] 
1a 00000012`115fe570 00007ffe`8012e30c     chrome!base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunOnce+0x80 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 694] 
1b (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x7 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 142] 
1c 00000012`115fe5b0 00007ffe`82cb0775     chrome!gpu::Scheduler::RunNextTask+0x7bc [C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc @ 685] 
1d (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x10 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 142] 
1e 00000012`115fe6e0 00007ffe`82caee41     chrome!base::TaskAnnotator::RunTask+0x1c5 [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 178] 
1f (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x59d [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 357] 
20 00000012`115fe830 00007ffe`818e5739     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x631 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260] 
21 00000012`115feb90 00007ffe`80407eb3     chrome!base::MessagePumpDefault::Run+0xc9 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 40] 
22 00000012`115fec40 00007ffe`80634ee6     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x83 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 465] 
23 00000012`115fecb0 00007ffe`806a0d7c     chrome!base::RunLoop::Run+0x1c6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 142] 
24 00000012`115fede0 00007ffe`80690fc6     chrome!content::GpuMain+0x49c [C:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc @ 429] 
25 (Inline Function) --------`--------     chrome!content::RunOtherNamedProcessTypeMain+0xb4 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 649] 
26 00000012`115ff160 00007ffe`80337f82     chrome!content::ContentMainRunnerImpl::Run+0x1a6 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 986] 
27 (Inline Function) --------`--------     chrome!content::RunContentProcess+0x11d [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 390] 
28 00000012`115ff230 00007ffe`80336e4a     chrome!content::ContentMain+0x152 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 418] 
29 00000012`115ff420 00007ff7`17db6f30     chrome!ChromeMain+0x18a [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 175] 
2a 00000012`115ff530 00007ff7`17db6aca     chrome_exe!MainDllLoader::Launch+0x300 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169] 
2b 00000012`115ff7b0 00007ff7`17e1b9d2     chrome_exe!wWinMain+0xcca [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382] 
2c (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
2d 00000012`115ffbe0 00007fff`3b2854e0     chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
2e 00000012`115ffc20 00007fff`3c12485b     KERNEL32!BaseThreadInitThunk+0x10
2f 00000012`115ffc50 00000000`00000000     ntdll!RtlUserThreadStart+0x2b


2:037> ub
libglesv2!angle::Format::Get+0x1a [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 5596] [inlined in libglesv2!rx::vk::ImageHelper::stageSubresourceUpdateImpl+0x86 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\vk_helpers.cpp @ 5596]]:
00007ffe`aadb5246 beaaaaaaaa      mov     esi,0AAAAAAAAh
00007ffe`aadb524b 89b4244c010000  mov     dword ptr [rsp+14Ch],esi
00007ffe`aadb5252 89b42448010000  mov     dword ptr [rsp+148h],esi
00007ffe`aadb5259 0f2835e0191800  movaps  xmm6,xmmword ptr [libglesv2!_xmmaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (00007ffe`aaf36c40)]
00007ffe`aadb5260 488d8c2430010000 lea     rcx,[rsp+130h]
00007ffe`aadb5268 0f2931          movaps  xmmword ptr [rcx],xmm6
00007ffe`aadb526b 4489f2          mov     edx,r14d
00007ffe`aadb526e ff13            call    qword ptr [rbx]



## Attachments

- [getIncompleteTexture.html](attachments/getIncompleteTexture.html) (text/plain, 1.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 6.6 KB)

## Timeline

### [Deleted User] (2021-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5750802670747648.

### rs...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE Internals>GPU>Vulkan]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5750802670747648

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x7fbb984b8480
Crash State:
  rx::IncompleteTextureSet::getIncompleteTexture
  rx::ContextVk::updateActiveTextures
  rx::ContextVk::syncState
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=902741:902744

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5750802670747648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### lf...@google.com (2021-12-02)

[Empty comment from Monorail migration]

### lf...@google.com (2021-12-02)

This one looks like it's because SamplerFormat is just some value field it can initialize to anything it wants, including some value outside the range of the allowed 0, 1, 2, 3, 4, then reading past the end of kIncompleteTextureParameters

### lf...@google.com (2021-12-02)

Initialization-wise we actually properly fill the mActiveSamplerFormats array (of ProgramExecutable) with InvalidEnum, so we are initializing properly. However, the problem is that PackedEnumMap's array size depends on the EnumCount which is wrongly 4 for SamplerFormat (there are actually 5 SamplerFormats because we include the invalid enum).

### jm...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### jm...@chromium.org (2021-12-02)

Frank: I suggest we don't allow incomplete textures for an invalid sampler type. One solution would be to override invalid with 2D. I thought though we should generate invalid_operation when we try to draw with a sampler type conflict:

        if (executable)
        {
            if (!executable->validateSamplers(nullptr, context->getCaps()))
            {
                return kTextureTypeConflict;
            }

Maybe there's a way this code can bypass that check? Once you get the repro case into ANGLE I can help you debug & find the best fix.

### lf...@google.com (2021-12-02)

I can look into getting the repro case in. However, it seems fragile to rely on spec logic to avoid invalid---much better to make the current struct definition consistent first, right? We seem to rely in SamplerFormat::InvalidEnum in _many_ places.

### jm...@chromium.org (2021-12-02)

Sorry, I wasn't aware of us relying on SamplerFormat::InvalidEnum for incomplete textures. We rely on spec behaviour *everywhere*.. hence why disabling validation results in tons of crashes.

### gi...@appspot.gserviceaccount.com (2021-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6d3435fddd7abd67699c3f020d6b4fa21445d9b3

commit 6d3435fddd7abd67699c3f020d6b4fa21445d9b3
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 01:08:01 2021

Validate SamplerFormat

We weren't validating sampler formats in ProgramExecutable validation.

Bug: chromium:1273661
Change-Id: Ida0c67c0c7169ea3f47ceb2d433bee17012a7e5e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312717
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>

[modify] https://crrev.com/6d3435fddd7abd67699c3f020d6b4fa21445d9b3/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/6d3435fddd7abd67699c3f020d6b4fa21445d9b3/src/libANGLE/ProgramExecutable.cpp


### lf...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0bc38ea16ec75040921620619a23233b0f8f4b36

commit 0bc38ea16ec75040921620619a23233b0f8f4b36
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Dec 07 00:57:11 2021

Roll ANGLE from 929c8ed4e8c3 to 006c11d932fc (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/929c8ed4e8c3..006c11d932fc

2021-12-06 syoussefi@chromium.org Vulkan: Fix xfb query ASSERT on end
2021-12-06 lfy@google.com Validate SamplerFormat
2021-12-06 ianelliott@google.com Point to ANGLE Wrangler schedule website in document

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
Bug: chromium:1209285,chromium:1273661
Tbr: jonahr@google.com
Change-Id: I77070ac519287ab32fccc6b5b80e18f0b91dea0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3319199
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#948762}

[modify] https://crrev.com/0bc38ea16ec75040921620619a23233b0f8f4b36/DEPS


### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-07)

ClusterFuzz testcase 5750802670747648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=948756:948766

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

Requesting merge to stable M96 because latest trunk commit (948762) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (948762) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

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

### [Deleted User] (2021-12-08)

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

### lf...@google.com (2021-12-08)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It's a security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/angle/angle/+/3312717

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A

### ad...@google.com (2021-12-08)

Approving merge to M96 (branch 4664) and M97 (branch 4692).

### [Deleted User] (2021-12-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-12-13)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this Wednesday's M97 Beta release.

### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739

commit 7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 01:08:01 2021

M97: Validate SamplerFormat

We weren't validating sampler formats in ProgramExecutable validation.

Bug: chromium:1273661
Change-Id: Ida0c67c0c7169ea3f47ceb2d433bee17012a7e5e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312717
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 6d3435fddd7abd67699c3f020d6b4fa21445d9b3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3335174
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739/src/libANGLE/ProgramExecutable.cpp


### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ce8b70863980d84e103c8d5f3ab6e267ae90701a

commit ce8b70863980d84e103c8d5f3ab6e267ae90701a
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 01:08:01 2021

M96: Validate SamplerFormat

We weren't validating sampler formats in ProgramExecutable validation.

Bug: chromium:1273661
Change-Id: Ida0c67c0c7169ea3f47ceb2d433bee17012a7e5e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312717
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 6d3435fddd7abd67699c3f020d6b4fa21445d9b3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3335173
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/ce8b70863980d84e103c8d5f3ab6e267ae90701a/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/ce8b70863980d84e103c8d5f3ab6e267ae90701a/src/libANGLE/ProgramExecutable.cpp


### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739

commit 7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739
Author: Lingfeng Yang <lfy@google.com>
Date: Thu Dec 02 01:08:01 2021

M97: Validate SamplerFormat

We weren't validating sampler formats in ProgramExecutable validation.

Bug: chromium:1273661
Change-Id: Ida0c67c0c7169ea3f47ceb2d433bee17012a7e5e
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3312717
Reviewed-by: Charlie Lao <cclao@google.com>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Lingfeng Yang <lfy@google.com>
(cherry picked from commit 6d3435fddd7abd67699c3f020d6b4fa21445d9b3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3335174
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739/src/tests/gl_tests/TextureTest.cpp
[modify] https://crrev.com/7ccfe9ae7cb9648f4d1eabca14f8cb67fac55739/src/libANGLE/ProgramExecutable.cpp


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

And another one! Congratulations, Omair - the VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1273661?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>Vulkan]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058015)*
