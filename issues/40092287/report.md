# Crash in gpu::gles2::Texture::ClearRenderableLevels

| Field | Value |
|-------|-------|
| **Issue ID** | [40092287](https://issues.chromium.org/issues/40092287) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-08-27 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

Steps to reproduce the problem:
Version 70.0.3515.0 (Developer Build) (64-bit)(ubuntu)
68.0.3440.106(release)(32bit)(windows)

1.build new chrome with asan.
2. ./chrome ./poc.html

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_ACCERR 61ad053a6b28
    #0 0x55e77b3b5741 in __interceptor_backtrace /b/swarming/w/ir/kitchen-workdir/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4024:13
    #1 0x55e78333318e in base::debug::StackTrace::StackTrace(unsigned long) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:808:41
    #2 0x55e7833320dd in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/stack_trace_posix.cc:334:3
    #3 0x7fd20bc6f890 in __funlockfile ??:?
    #4 0x7fd20bc6f890 in ?? ??:0
    #5 0x55e786bc749c in gpu::gles2::Texture::ClearRenderableLevels(gpu::DecoderContext*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/texture_manager.cc:1596:16
    #6 0x55e7877180b7 in gpu::gles2::GLES2DecoderImpl::ClearUnclearedTextures() /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/gles2_cmd_decoder.cc:10282:37
    #7 0x55e78771c083 in gpu::gles2::GLES2DecoderImpl::DoDrawArrays(char const*, bool, unsigned int, int, int, int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/gles2_cmd_decoder.cc:10738:10
    #8 0x55e78767125e in gpu::gles2::GLES2DecoderImpl::HandleDrawArrays(unsigned int, void const volatile*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/gles2_cmd_decoder.cc:10787:10
    #9 0x55e7876f3f7f in gpu::error::Error gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/gles2_cmd_decoder.cc:5654:18
    #10 0x55e787619e55 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/command_buffer_service.cc:69:18
    #11 0x55e78760ae5d in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/ipc/service/command_buffer_stub.cc:619:22
    #12 0x55e78760a6b2 in DispatchToMethodImpl<gpu::CommandBufferStub *, void (gpu::CommandBufferStub::*)(int, unsigned int), std::__1::tuple<int, unsigned int>, 0, 1> /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/tuple.h:52:3
    #13 0x55e78760a6b2 in DispatchToMethod<gpu::CommandBufferStub *, void (gpu::CommandBufferStub::*)(int, unsigned int), std::__1::tuple<int, unsigned int> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/tuple.h:60:0
    #14 0x55e78760a6b2 in DispatchToMethod<gpu::CommandBufferStub, void (gpu::CommandBufferStub::*)(int, unsigned int), void, std::__1::tuple<int, unsigned int> > /home/cowboy/chromium/src/out/chrome_asan_shared/../../ipc/ipc_message_templates.h:51:0
    #15 0x55e78760a6b2 in bool IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta, std::__1::tuple<int, unsigned int>, void>::Dispatch<gpu::CommandBufferStub, gpu::CommandBufferStub, void, void (gpu::CommandBufferStub::*)(int, unsigned int)>(IPC::Message const*, gpu::CommandBufferStub*, gpu::CommandBufferStub*, void*, void (gpu::CommandBufferStub::*)(int, unsigned int)) /home/cowboy/chromium/src/out/chrome_asan_shared/../../ipc/ipc_message_templates.h:146:0
    #16 0x55e787606cb7 in gpu::CommandBufferStub::OnMessageReceived(IPC::Message const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/ipc/service/command_buffer_stub.cc:280:5
    #17 0x55e7875e9813 in gpu::GpuChannel::HandleMessageHelper(IPC::Message const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/ipc/service/gpu_channel.cc:540:23
    #18 0x55e7875e3ade in gpu::GpuChannel::HandleMessage(IPC::Message const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/ipc/service/gpu_channel.cc:516:3
    #19 0x55e787829e3d in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #20 0x55e787829e3d in gpu::Scheduler::RunNextTask() /home/cowboy/chromium/src/out/chrome_asan_shared/../../gpu/command_buffer/service/scheduler.cc:526:0
    #21 0x55e78316b5c1 in Run /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/callback.h:99:12
    #22 0x55e78316b5c1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/debug/task_annotator.cc:101:0
    #23 0x55e7831668ee in base::MessageLoop::RunTask(base::PendingTask*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:431:46
    #24 0x55e783167b79 in DeferOrRunPendingTask /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:442:5
    #25 0x55e783167b79 in base::MessageLoop::DoWork() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_loop.cc:514:0
    #26 0x55e783170df6 in HandleDispatch /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:263:25
    #27 0x55e783170df6 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:109:0
    #28 0x7fd209986287 in g_main_context_dispatch ??:0:0
    #29 0x7fd2099864c0 in g_main_context_dispatch ??:?
    #30 0x7fd2099864c0 in ?? ??:0
    #31 0x7fd20998654c in g_main_context_iteration ??:0:0
    #32 0x55e7831705f8 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/message_loop/message_pump_glib.cc:305:30
    #33 0x55e7831e0c71 in base::RunLoop::Run() /home/cowboy/chromium/src/out/chrome_asan_shared/../../base/run_loop.cc:102:14
    #34 0x55e7900b59db in content::GpuMain(content::MainFunctionParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/gpu/gpu_main.cc:347:21
    #35 0x55e7825009a7 in content::ContentMainRunnerImpl::Run(bool) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main_runner_impl.cc:891:10
    #36 0x55e78262ed25 in service_manager::Main(service_manager::MainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../services/service_manager/embedder/main.cc:472:29
    #37 0x55e7824fbe7f in content::ContentMain(content::ContentMainParams const&) /home/cowboy/chromium/src/out/chrome_asan_shared/../../content/app/content_main.cc:19:10
    #38 0x55e77b43fe60 in ChromeMain /home/cowboy/chromium/src/out/chrome_asan_shared/../../chrome/app/chrome_main.cc:101:12
    #39 0x7fd204bccb97 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0
    #40 0x55e77b36802a in _start ??:0:0
  r8: 0000611000b7fc60  r9: 0000000000000001 r10: 0000000000000000 r11: 00006080004e4068
 r12: 00000000546bdc59 r13: 0000001d0513bea8 r14: 00000c0600034970 r15: 00006030001a4b88
  di: 000061ad053a6b28  si: 0000611000b7fc58  bp: 00007fff721a88a0  bx: 00006030001a4b80
  dx: 0000611000b7fcd0  ax: 0000000000000000  cx: 0000000000000000  sp: 00007fff721a8820
  ip: 000055e786bc749c efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000061ad053a6b28
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Version 70.0.3515.0 (Developer Build) (64-bit)(ubuntu)  Channel: beta
OS Version: Ubuntu18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [minimised.html](attachments/minimised.html) (text/plain, 2.1 KB)

## Timeline

### cl...@chromium.org (2018-08-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6276171617271808.

### cd...@gmail.com (2018-08-27)

After a little in-depth analysis I found this issue and my another issue may be caused by same root.If right, please merge it to one issue.
https://bugs.chromium.org/p/chromium/issues/detail?id=877876

this line repor sig 11:
__cass__5__.texParameteri(__cass__5__.TEXTURE_3D, __cass__5__.TEXTURE_BASE_LEVEL, 1416354905);

this line repor heap-buffer-oveflow:
__cass__5__.texParameteri(__cass__5__.TEXTURE_3D, __cass__5__.TEXTURE_BASE_LEVEL, 500);

attachment is minimised poc.

### cl...@chromium.org (2018-08-27)

Detailed report: <https://clusterfuzz.com/testcase?key=6276171617271808>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: UNKNOWN READ  

Crash Address: 0x61bd05169b28  

Crash State:  

gpu::gles2::Texture::ClearRenderableLevels  

gpu::gles2::GLES2DecoderImpl::ClearUnclearedTextures  

gpu::gles2::GLES2DecoderImpl::DoDrawArrays

Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=6276171617271808>

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Internals]

### va...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-08-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5714186823532544.

### va...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-27)

M-68 per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#medium-severity

### cl...@chromium.org (2018-08-28)

Detailed report: https://clusterfuzz.com/testcase?key=5714186823532544

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x61bd0518d528
Crash State:
  gpu::gles2::Texture::ClearRenderableLevels
  gpu::gles2::GLES2DecoderImpl::ClearUnclearedTextures
  gpu::gles2::GLES2DecoderImpl::DoDrawArrays
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495501:495712

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5714186823532544

See https://github.com/google/clusterfuzz-tools for more information.

### va...@chromium.org (2018-08-28)

Possibly related to https://chromium-review.googlesource.com/612443

### zm...@chromium.org (2018-08-28)

I'll take a look at this.

### zm...@chromium.org (2018-08-28)

I don't have access to crbug.com/877876

If you want me to evaluate if these two are the same root cause, please add me to that bug.

I can repro the crash locally and understand the issue. I'll upload a fix shortly after.

### zm...@chromium.org (2018-08-28)

Olli, there seems to be a NVidia driver, where the test example (poc.zip) will trigger a segment fault in NVidia driver. The workaround in Chrome is to always clamp TEXTURE_BASE_LEVEL and TEXTURE_MAX_LEVEL through glTexParameteri() before glTexStorage*().

Can you pass this to NVidia Linux driver team?

### zm...@chromium.org (2018-08-28)

+geofflang, +enne
One more driver bug workaround I am adding

### zm...@chromium.org (2018-08-28)

Actually we can just reuse the reset_base_mipmap_level_before_texstorage also works around the NVIDIA driver bug, although in theory we don't need to set it 0, but the clamped base_level, so we don't need to reset it again after TexStorage call, but the difference is trivia, and it's good to have one less workaround.

max_level seems not to matter.

### en...@chromium.org (2018-08-28)

If you're cc-ing me because of OOP-R, I think this doesn't apply to Skia.  Skia doesn't use TEXTURE_BASE_LEVEL as anything but zero except when building mipmaps.

### zm...@chromium.org (2018-08-28)

CL I am still working (missing tests): https://chromium-review.googlesource.com/c/chromium/src/+/1194994

### er...@chromium.org (2018-08-29)

+backer

### bu...@chromium.org (2018-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/385508dc888ef15d272cdd2705b17996abc519d6

commit 385508dc888ef15d272cdd2705b17996abc519d6
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Aug 29 20:03:50 2018

Implement immutable texture base/max level clamping

It seems some drivers fail to handle that gracefully, so let's always clamp
to be on the safe side.

BUG=877874
TEST=test case in the bug, gpu_unittests
R=kbr@chromium.org

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Change-Id: I6d93cb9389ea70525df4604112223604577582a2
Reviewed-on: https://chromium-review.googlesource.com/1194994
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#587264}
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/command_buffer/service/gles2_cmd_decoder.cc
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/command_buffer/service/gles2_cmd_decoder_unittest_textures.cc
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/command_buffer/service/texture_manager.cc
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/command_buffer/service/texture_manager.h
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/config/gpu_driver_bug_list.json
[modify] https://crrev.com/385508dc888ef15d272cdd2705b17996abc519d6/gpu/config/gpu_workaround_list.txt


### zm...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-29)

This bug requires manual review: We are only 5 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-29)

mbarbella@ & inferno@chromium.org for M69 merge review as awhalley@ is OOO.

Note: CL listed at #20 is not in canary yet and we're planning to cut M69 stable RC tomorrow.

### cl...@chromium.org (2018-08-30)

ClusterFuzz has detected this issue as fixed in range 587263:587267.

Detailed report: https://clusterfuzz.com/testcase?key=5714186823532544

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x61bd0518d528
Crash State:
  gpu::gles2::Texture::ClearRenderableLevels
  gpu::gles2::GLES2DecoderImpl::ClearUnclearedTextures
  gpu::gles2::GLES2DecoderImpl::DoDrawArrays
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=495501:495712
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=587263:587267

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5714186823532544

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-08-30)

ClusterFuzz testcase 5714186823532544 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-08-30)

Rejecting merge to M69 per internal mail thread "Requesting M69 merge review ASAP - crbug 877874".

### zm...@chromium.org (2018-08-30)

I don't see the internal mail thread mentioned in #27 in my email inbox. Could you please include me in that discussion?

Per offline talk with kbr, seg fault is not a huge risk - there are other ways to crash GPU process today, so we agree it's OK not to merge back to M69.

### zm...@chromium.org (2018-08-30)

sugoi@: it seems this fuzzer isn't running on top of SwiftShader. Can we switch it to SwiftShader instead?

### su...@chromium.org (2018-08-30)

zmo@: Which fuzzer are you referring to? The test in the clusterfuzz report does use "--use-gl=swiftshader".

### zm...@chromium.org (2018-08-30)

Thta doesn't make sense. If you look at the stack, it doesn't involve SwiftShader.

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-12)

Hi cdsrc2016@ - the VRP panel decided to award $1,000 for this report - thanks!

### aw...@google.com (2018-09-12)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-09-13)

@awhalley
Hi,Thank you for the rewawrd.:)

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-09)

Hi oetuaho@nvidia.com - Given the underlying bug is in nvidia driver, do you think the CVE should refer to that issue rather than our workaround?  Have you already issued a CVE for it?

### ka...@chromium.org (2018-11-09)

-oetuaho
+kkinnunen

### ka...@chromium.org (2018-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### jo...@google.com (2019-07-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f

commit 5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Sep 20 00:14:03 2023

Remove GPU workarounds and entries.

They no longer applies, either related codes are deleted,
or they only apply on validating command buffer which is
not used on the affected platforms.

The removed workarounds are:
* init_vertex_attributes
* needs_offscreen_buffer_workaround
* rebind_transform_feedback_before_resume
* regenerate_struct_names
* remove_invariant_and_centroid_for_essl3
* reset_base_mipmap_level_before_texstorage
* restore_scissor_on_fbo_change
* rewrite_do_while_loops
* rewrite_float_unary_minus_operator
* rewrite_texelfetchoffset_to_texelfetch
* set_zero_level_before_generating_mipmap
* simulate_out_of_memory_on_large_textures
* unpack_image_height_workaround_with_unpack_buffer
* use_unused_standard_shared_blocks

TEST=bots
R=kbr@chromium.org,geofflang@chromium.org

Bug: 1136972,89557,351528,403957,560499,563714,638514,640506,642605,618464,654258,639760,641129,672300,877874,709351,1090584
Change-Id: I12cfbee5e7060467a4f6abeab21bee9f91daeb37
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4876849
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1198703}

[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/vertex_attrib_manager.h
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/vertex_attrib_manager.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/gles2_cmd_decoder_unittest_drawing.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/texture_manager.h
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/gles2_cmd_decoder.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/gles2_cmd_decoder_unittest_base.h
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/vertex_attrib_manager_unittest.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/config/gpu_driver_bug_list_unittest.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/config/gpu_driver_bug_list.json
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/texture_manager.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/command_buffer/service/gles2_cmd_decoder_unittest_base.cc
[modify] https://crrev.com/5eec641267a4f6da4d92d4c3a315c2c3b12c8a2f/gpu/config/gpu_workaround_list.txt


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/877874?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/976283]
[Monorail mergedwith: crbug.com/chromium/877876]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092287)*
