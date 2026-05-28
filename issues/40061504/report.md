# Security: Stack-buffer-overflow in WebGL vulkan backend

| Field | Value |
|-------|-------|
| **Issue ID** | [40061504](https://issues.chromium.org/issues/40061504) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux |
| **Reporter** | et...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-10-28 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=333885>.

The commit id that introduced this vulnerability is 8ed5c89d533d74d57824eab7b05e4fe778e4a532, this chromium commit rolls the angle code forward.  

<https://chromium.googlesource.com/angle/angle.git/+log/493bab09b564..ba3b4515954d>

\*\*So the angle commit that actually introduced this vulnerability is: \*\* <https://chromium.googlesource.com/angle/angle.git/+/ba3b4515954d90f9242c4da165b064544e08d394>

Here, it implements a new OPCODE `GL_ANGLE_logic_op`, and destroys the original processing logic, causing the parameters passed to libvulkan\_intel.so to not be configured correctly.

This will lead to a stack overflow vulnerability that is stably reproduced in the chromium GPU process, it will crash on the canary check function stack\_chk\_fail of libvulkan\_intel.so loaded into the chromium GPU process, since it overwrites the stack canary.

It cannot be ruled out that for performance reasons, canary is turned off on some Linux distributions and rip is hijacked directly via stack overflow.

After some reverse analysis, I initially restored the stack overflow call path from Chromium to libvulkan:  

[0] SecondaryCommandBuffer::executeCommands  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/vulkan/SecondaryCommandBuffer.cpp;l=390?q=SecondaryCommandBuffer::executeCommands>

[1] CmdDraw  

<https://gitlab.freedesktop.org/mesa/mesa/-/blob/mesa-21.2.6/src/intel/vulkan/genX_cmd_buffer.c#L3909>

[2] cmd\_buffer\_flush\_state  

<https://gitlab.freedesktop.org/mesa/mesa/-/blob/mesa-21.2.6/src/intel/vulkan/genX_cmd_buffer.c#L3763>

[3] cmd\_buffer\_flush\_dynamic\_state end trigger canary check  

<https://gitlab.freedesktop.org/mesa/mesa/-/blob/mesa-21.2.6/src/intel/vulkan/gfx8_cmd_buffer.c#L418>

```
#4  0x00007fffa8e22a86 in __stack_chk_fail () at stack_chk_fail.c:24  
#5  0x00007fff8dc9569c in  () at /usr/lib/x86_64-linux-gnu/libvulkan_intel.so // gfx8（maybe 7?）_cmd_buffer_flush_dynamic_state  
#6  0x00007fff8dc7d159 in  () at /usr/lib/x86_64-linux-gnu/libvulkan_intel.so // gfx9_cmd_buffer_flush_state  
#7  0x00007fff8dc7ff1e in  () at /usr/lib/x86_64-linux-gnu/libvulkan_intel.so // gfx9_cmdDraw   
#8  0x00007fff97a556bf in rx::vk::priv::SecondaryCommandBuffer::executeCommands(rx::vk::priv::CommandBuffer\*) ()  
    at /home/pkf/Chrome_study/chromium/src/out/Default/libGLESv2.so  

```

**VERSION**  

Chrome Version: stable, beta, and dev  

Operating System: Only Linux

**REPRODUCTION CASE**

\*\*Note: not Trigger in a Linux virtual machine.\*\*

1. Since this is a GPU vulnerability, and it relies on the improper configuration of the parameters that Chromium passes into the mesa driver on Linux (that is, the source code of libvulkan\_intel.so), so it can only be triggered on a real Linux machine, not trigger in a Linux virtual machine.\*\*
2. I can trigger this vulnerability stably on different machines and different systems (ubuntu20.04 and 22.04). Please check if the GL\_RENDER field of your chrome://gpu shows that the current chromium Angle uses Vulkan and Mesa driver.  
   
   This is my GL RENDER for ubuntu20.04, since I don't have a linux machine with amd, I just tried intel, but I think it should be generic.

```
ANGLE (Intel, Vulkan 1.2.182 (Intel(R) UHD Graphics 630 (CFL GT2) (0x00003E92)), Intel open-source Mesa driver-21.2.6)  

```

3. Download Chromium asan from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1062998.zip?generation=1666648914528355&alt> =media
4. Run ./chrome-wrapper poc.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State: see crash log

**CREDIT INFORMATION**  

Reporter credit:  

Nan Wang(@eternalsakura13) and Yong Liu of 360 Vulnerability Research Institute

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.8 KB)
- repro.mp4 (video/mp4, 600.5 KB)
- [crash.log](attachments/crash.log) (text/plain, 9.7 KB)
- [chrome_gpu.config](attachments/chrome_gpu.config) (application/octet-stream, 54.7 KB)
- [libvulkan_intel.zip](attachments/libvulkan_intel.zip) (application/octet-stream, 3.5 MB)
- [crash.log](attachments/crash.log) (text/plain, 10.2 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 35.7 KB)

## Timeline

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-10-28)

Attach libvulkan_intel.so on ubuntu20.04


### et...@gmail.com (2022-10-28)

This bug should be fixed in chrome and because it is widely available on linux distributions, it can be triggered from the browser. I think this is a high vulnerability that should be fixed.

We can roll back some of the code to before we introduced this GL_ANGLE_logic_op commit.
https://chromium.googlesource.com/angle/angle.git/+/ba3b4515954d90f9242c4da165b064544e08d394

- asan-linux-release-1049155 is the first downloadable version of Chromium Asan that can reproduce.
https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1049155.zip?generation=1663695127955449&alt=media

- asan-linux-release-1049138 cannot reproduce
https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1049138.zip?generation=1663692824366982&alt=media

### me...@chromium.org (2022-10-28)

syoussefi, could you PTAL? I don't have access to a real Linux machine, so could you please help assign FoundIn- label as well? Thanks.

[Monorail components: Internals>GPU>ANGLE]

### sy...@chromium.org (2022-10-29)

Will do.

@reporter, I don't quite understand what you mean by this:

> Here, it implements a new OPCODE `GL_ANGLE_logic_op`, and destroys the original processing logic, causing the parameters passed to libvulkan_intel.so to not be configured correctly.

What the change does is to implement logicOp, a feature of GLES1 and desktop GL in GLES2+. There are no users at that point (though ANGLE's GLES1 implementation will use it in a later commit). However, it _does_ take advantage of dynamic state for logic op. We currently set all dynamic state on render pass start, even if ineffective (like the logic op when logic op is disabled).

So the behavior change you might see is ANGLE calling `vkCmdSetLogicOpEXT`, which should be a no-op because all pipelines have `VkPipelineColorBlendStateCreateInfo::logicOpEnable` equal to false. If that's causing mesa to trip up, it's a bug in mesa. You can verify this by applying the following diff:

     ANGLE_FEATURE_CONDITION(&mFeatures, supportsLogicOpDynamicState,
-                            mExtendedDynamicState2Features.extendedDynamicState2LogicOp == VK_TRUE);
+                            false);

If that fixes your issue, we can simply disable this dynamic state on Intel/Linux as a workaround, and you can report this issue to mesa to be fixed.

### et...@gmail.com (2022-10-29)

re https://crbug.com/chromium/1379201#c5
Thanks for your reply, but in fact I can't quite confirm this:
> Here, it implements a new OPCODE `GL_ANGLE_logic_op`, and destroys the original processing logic, causing the parameters passed to libvulkan_intel.so to not be configured correctly.

I don't fully understand the code here, I'm just speculating based on the phenomenon that caused this vulnerability to occur after the commit was introduced.

### et...@gmail.com (2022-10-29)

re https://crbug.com/chromium/1379201#c5:
Can you try to reproduce it and confirm?


### et...@gmail.com (2022-10-29)

I verified it in https://crbug.com/chromium/1379201#c5.

When I modify mExtendedDynamicState2Features.extendedDynamicState2LogicOp == VK_TRUE to false, it will work normally,  when set it to true, it will trigger stack overflow.

Maybe it's an issue with mesa, but since it will trigger a stack overflow in Chrome's GPU process, possibly causing a sandbox escape, this would be a high-severity vulnerability.

Should we disable it on Chrome's side to fix the bug?

For example, patch it to false as you said. Thanks :)

### ad...@google.com (2022-10-29)

(auto-cc on security bug)

### et...@gmail.com (2022-10-31)

I continued to run my fuzzer for 2 days. It hits a stack overflow with a different call stack.
I didn't have time to analyze it this week, but I'm attaching a poc sample of it here, I'm assuming the same cause for both of them.

** I recommend fixing this bug in chrome, as this is a stack overflow of a GPU process that could lead to a sandbox escape. **
Even assuming this is a mesa issue, linux distributions (eg ubuntu) are not up to date with the latest to mesa, and we don't know when it will be fixed.

Let me know if you have any problems reproducing :)

- stack trace
Received signal 6
    #0 0x562524335797 in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4434:13
    #1 0x5625347457f2 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:879:7
    #2 0x5625344f6103 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x5625344f6103 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x5625347442bb in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:372:3
    #5 0x7f8f71bfe420 in __funlockfile :?
    #6 0x7f8f701ad00b in __libc_signal_restore_set /build/glibc-SzIz7B/glibc-2.31/signal/../sysdeps/unix/sysv/linux/internal-signals.h:86:3
    #7 0x7f8f701ad00b in raise /build/glibc-SzIz7B/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:48:3
    #8 0x7f8f7018c859 in abort /build/glibc-SzIz7B/glibc-2.31/stdlib/abort.c:79:7
    #9 0x7f8f701f726e in __libc_message /build/glibc-SzIz7B/glibc-2.31/libio/../sysdeps/posix/libc_fatal.c:155:5
    #10 0x7f8f70299aba in __fortify_fail /build/glibc-SzIz7B/glibc-2.31/debug/fortify_fail.c:26:5
    #11 0x7f8f70299a86 in __stack_chk_fail /build/glibc-SzIz7B/glibc-2.31/debug/stack_chk_fail.c:24:3
#10 0x7f8f5e3fac0f <unknown>
#11 0x7f8f5e3e0399 <unknown>
#12 0x7f8f5e3e3aac <unknown>
#13 0x7f8f68482d6f <unknown>
#14 0x7f8f6859c220 <unknown>
#15 0x7f8f68467899 <unknown>
#16 0x7f8f683b3dfc <unknown>
#17 0x7f8f68374c0b <unknown>
#18 0x7f8f6838b30f <unknown>
#19 0x7f8f6839712f <unknown>
#20 0x7f8f67c34647 <unknown>
    #12 0x5625386a8d13 in gl::RealGLApi::glDrawArraysFn(unsigned int, int, int) ./../../ui/gl/gl_gl_api_implementation.cc:451:16
    #13 0x56253af12bbb in gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1221:10
    #14 0x56253aeced46 in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:895:20
    #15 0x56253b2f9618 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:226:35
    #16 0x56253b2ec62a in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::Cr::vector<gpu::SyncToken, std::Cr::allocator<gpu::SyncToken>> const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499:22
    #17 0x56253b2eb8d8 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:154:7
    #18 0x56253b30113a in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:706:13
    #19 0x56253b30e1e7 in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/functional/bind_internal.h:646:12
    #20 0x56253b30df9a in MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> > > ./../../base/functional/bind_internal.h:847:5
    #21 0x56253b30df9a in RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:919:12
    #22 0x56253b30df9a in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:870:12
    #23 0x5625395fa603 in Run ./../../base/functional/callback.h:173:12
    #24 0x5625395fa603 in gpu::Scheduler::RunNextTask() ./../../gpu/command_buffer/service/scheduler.cc:726:26
    #25 0x562539605b90 in Invoke<void (gpu::Scheduler::*)(), gpu::Scheduler *> ./../../base/functional/bind_internal.h:646:12
    #26 0x562539605b90 in MakeItSo<void (gpu::Scheduler::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::RawPtrBanDanglingIfSupported> > > ./../../base/functional/bind_internal.h:825:12
    #27 0x562539605b90 in RunImpl<void (gpu::Scheduler::*)(), std::Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler, base::RawPtrBanDanglingIfSupported> >, 0UL> ./../../base/functional/bind_internal.h:919:12
    #28 0x562539605b90 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::RawPtrBanDanglingIfSupported>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:870:12
    #29 0x56253465713a in Run ./../../base/functional/callback.h:173:12
    #30 0x56253465713a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:133:32
    #31 0x56253469d27e in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:443:29)> ./../../base/task/common/task_annotator.h:72:5
    #32 0x56253469d27e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:441:21
    #33 0x56253469c2fb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:297:30
    #34 0x56253469e585 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #35 0x562534561f69 in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:374:46
    #36 0x562534561f69 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:127:43
    #37 0x7f8f71a9c17d in g_main_context_dispatch ??:0:0
    #38 0x7f8f71a9c400 in g_main_context_dispatch ??:?
    #39 0x7f8f71a9c4a3 in g_main_context_iteration ??:0:0
    #40 0x562534560f3c in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:400:30
    #41 0x56253469f0b1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:600:12
    #42 0x5625345e644f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141:14
    #43 0x5625468cf61e in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:398:14
    #44 0x56253339f474 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:679:14
    #45 0x5625333a1521 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:761:12
    #46 0x5625333a36e9 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1104:10
    #47 0x56253339bf9d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:342:36
    #48 0x56253339c5aa in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:370:10
    #49 0x5625243bbb48 in ChromeMain ./../../chrome/app/chrome_main.cc:175:12
    #50 0x7f8f7018e083 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

### sy...@chromium.org (2022-10-31)

https://chromium-review.googlesource.com/c/angle/angle/+/3993360

I'd appreciate it if you would confirm this indeed fixes the issue.

### gi...@appspot.gserviceaccount.com (2022-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7b102c1800c2a2448613c106f18ed3c9e63af054

commit 7b102c1800c2a2448613c106f18ed3c9e63af054
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Oct 31 14:29:45 2022

Vulkan: Disable logicOp dynamic state on Intel/Mesa

Hits a stack overflow inside the driver.

Bug: chromium:1379201
Change-Id: I52e5254b37688a027cbcf5ee5752de36b9b2a3aa
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3993360
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/7b102c1800c2a2448613c106f18ed3c9e63af054/src/libANGLE/renderer/vulkan/RendererVk.cpp


### et...@gmail.com (2022-11-01)

Thanks for the fix.
I have verified multiple poc and confirmed that this vulnerability has been fixed. :)

Since this issue was introduced in this commit of 2022.09.20
https://chromium.googlesource.com/chromium/src/+/8ed5c89d533d74d57824eab7b05e4fe778e4a532

So please mark it as FoundIn-108, and Fixed, Thanks :)

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2bf78bdb0542fc6720c29391932b988793172ff3

commit 2bf78bdb0542fc6720c29391932b988793172ff3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Nov 01 02:26:49 2022

Roll ANGLE from 9d9b8b07ba82 to 67ee49768691 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/9d9b8b07ba82..67ee49768691

2022-10-31 syoussefi@chromium.org Vulkan: Skip BestPractices-ImageBarrierAccessLayout
2022-10-31 lexa.knyazev@gmail.com D3D11: Add clip and cull distance support
2022-10-31 syoussefi@chromium.org Vulkan: Disable logicOp dynamic state on Intel/Mesa

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC syoussefi@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1379201
Tbr: syoussefi@google.com
Change-Id: I1b6e170d2da18169f03e7c7ec79d2f5ecb9f7d01
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3994355
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1065793}

[modify] https://crrev.com/2bf78bdb0542fc6720c29391932b988793172ff3/DEPS


### sy...@chromium.org (2022-11-01)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-11-01)

Thanks for the confirmation

### sy...@chromium.org (2022-11-01)

That said, please open an issue with mesa referencing this bug. The TL;DR of the bug would be that "Calling `vkCmdSetLogicOpEXT` with logic op disabled leads to stack overflow" :)

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

Requesting merge to beta M108 because latest trunk commit (1065793) appears to be after beta branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-11-02)

1. Avoids stack overflow inside a particular driver
2. https://chromium-review.googlesource.com/c/angle/angle/+/3993360
3. Landed on Oct 31
4. No
5. N/A
6. N/A

If this is going to merge for 108 (beta), it should also be merged for 109 (dev) and 110 (canary) in my opinion.

### am...@chromium.org (2022-11-03)

m108 merge approved, please merge this fix to branch 5359 at your earliest convenience 

Also, in reviewing this bug and fix, OP/Nan Wang/eternalsakura@ have you reported this issue to Intel/Mesa? I just want to confirm if you are doing that or if we need to on our side, but want to ensure you have the opportunity to get full credit / ack from them. 

Thanks! 

### et...@gmail.com (2022-11-03)

re https://crbug.com/chromium/1379201#c24:
Hi, I am planning this. But I ran into a problem. I haven't discussed it with you due to time reasons.

> That said, please open an issue with mesa referencing this bug. The TL;DR of the bug would be that "Calling `vkCmdSetLogicOpEXT` with logic op disabled leads to stack overflow" :)

I noticed you wanted me to open an issue with mesa referencing this bug.
I think this is a high-severity vulnerability in chromium, and I can't directly disclose the details in the issue with mesa.
But since this issue-1379201 is not yet public, I don't know how to add access to this issue-1379201 for them. 

>  I just want to confirm if you are doing that or if we need to on our side

If possible, please help me reach them and provide access to this issue, thanks.



### et...@gmail.com (2022-11-03)

Anyway, since this issue has been fixed in chrome, and I haven't found any other path to trigger it.
So even if you fail to contact them for some reason, when issue-1379201 becomes public after 14 weeks, I will  open an issue with mesa referencing this bug. thanks :)

### sy...@chromium.org (2022-11-04)

Good point, it's probably better if we notify intel right here.

### ji...@intel.com (2022-11-04)

Thanks for the notification.

### ji...@intel.com (2022-11-04)

I have reported this bug to the Intel mesa team. If any progress I will update it here. Thanks again for reporting and fixing!

### gi...@appspot.gserviceaccount.com (2022-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ceec659ac60b0c8ee9d9c602ca1a878ec1d3a88f

commit ceec659ac60b0c8ee9d9c602ca1a878ec1d3a88f
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Mon Oct 31 14:29:45 2022

M108: Vulkan: Disable logicOp dynamic state on Intel/Mesa

Hits a stack overflow inside the driver.

Bug: chromium:1379201
Change-Id: I790d7ef0333ba17eedbe91e4fc9c3a2b94563bff
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4004440
Reviewed-by: Yuxin Hu <yuxinhu@google.com>

[modify] https://crrev.com/ceec659ac60b0c8ee9d9c602ca1a878ec1d3a88f/src/libANGLE/renderer/vulkan/RendererVk.cpp


### ji...@intel.com (2022-11-08)

Hi reporter,
    I tried to reproduce the bug per the steps in your bug description on my Ubuntu20.04 and Ubuntu22.10, but failed to reproduce the bug. The mesa versions were 20, 22 respectively. Per your log, the mesa at your side was version 21. Could you please check with the latest mesa?  Thanks!

### et...@gmail.com (2022-11-08)

1. Hello, please download chromium here:
https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1062998.zip?generation=1666648914528355&alt=media

2. Open chrome://gpu and check if the GL_RENDERER field is intel mesa and angle vulkan.


Note that this vulnerability can only be reproduced on a real Linux machine, not a virtual machine.
I borrowed a new machine from a friend, here is its GL_RENDERER information，I can reproduce it on its machine too, hope this helps you :)

ANGLE (Intel, Vulkan 1.3.204 (Intel(R) Graphics (ADL-S GT1) (0x00004692)), Intel open-source Mesa driver-22.0.5)



### et...@gmail.com (2022-11-08)

Sorry I can't provide an attempt to reproduce the latest mesa, this is the latest version I can find on ubuntu (mesa 22.0.5)
Please check your chrome://gpu and download the vulnerable chromium version to make sure it can be reproduced successfully.
If you have other questions, please let me know. :)
I tried it on many real linux machines to be sure this is not a special case problem.

### ji...@intel.com (2022-11-08)

Thanks, I am pretty sure my machines and steps of reproducing were as you described. Maye there is something else I missed.

@syoussefi, did you ever reproduce the bug?

### et...@gmail.com (2022-11-08)

Can you post your GL_Renderer? Thank you very much.

### et...@gmail.com (2022-11-08)

I have noticed that when using a non-Intel integrated graphics card, such as when we switched to nvida, it will not use mesa driver.


### sy...@chromium.org (2022-11-08)

@Jie, no the issue wouldn't reproduce for me with:

ANGLE (Intel, Vulkan 1.3.224 (Intel(R) HD Graphics 630 (KBL GT2) (0x0000591B)), Intel open-source Mesa driver-22.2.0)

Jie, did you by any chance make sure to re-enable the feature that is disabled when attempting to reproduce? You can do so by running Chrome with the following env var set:

ANGLE_FEATURE_OVERRIDES_ENABLED=SupportsLogicOpDynamicState

You can verify in chrome://gpu that this feature is enabled. If it's disabled, the workaround in #30 is in effect, so the mesa issue won't be triggered.

### ji...@intel.com (2022-11-09)

Thanks @Shahbaz. I was using the same chrome downloaded from the link. The feature shouldn't be the difference.
My GL_Renderer was:
ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) UHD Graphics 630 (CFL GT2), OpenGL 4.6 (Core Profile) Mesa 20.0.8)

Let's figure out how widely the bug could impact.

### et...@gmail.com (2022-11-09)

I noticed that there is no vulkan in your GL RENDERER, can you check if vulkan is enabled in chrome://gpu ?
such as: ANGLE (Intel, Vulkan 1.3.204 (Intel(R) Graphics (ADL-S GT1) (0x00004692)), Intel open-source Mesa driver-22.0.5)

### et...@gmail.com (2022-11-09)

In fact if someone can tell me how I can replace the native libvulkan_intel with a newer version, I'd be happy to help you test its reach.
I'm not familiar enough with gpu development. I tried compiling and replacing myself, but that didn't work.

### et...@gmail.com (2022-11-09)

[Comment Deleted]

### et...@gmail.com (2022-11-09)

Here is the GL_RENDER I tested on another 22.04, and its gpu feature:

GL_RENDERER
ANGLE (Intel, Vulkan 1.3.204 (Intel(R) UHD Graphics 630 (CFL GT2) (0x00003E98)), Intel open-source Mesa driver-22.0.5)
GL_VERSION
OpenGL ES 2.0.0 (ANGLE 2.1.19774 git hash: 7b4b56f0da0e)

Graphics Feature Status
Canvas: Hardware accelerated
Canvas out-of-process rasterization: Enabled
Direct Rendering Display Compositor: Disabled
Compositing: Hardware accelerated
Multiple Raster Threads: Enabled
OpenGL: Enabled
Rasterization: Hardware accelerated
Raw Draw: Disabled
Video Decode: Hardware accelerated
Video Encode: Software only. Hardware acceleration disabled
Vulkan: Enabled
WebGL: Hardware accelerated
WebGL2: Hardware accelerated
WebGPU: Disabled

### ji...@intel.com (2022-11-09)

I figured out the difference. It's specific to ANGLE on Vulkan. But chrome is still using ANGLE on GL by default on Linux. So I need to use the command line:
--enable-features=Vulkan --use-angle=vulkan

The bug was fixed in mesa 22.1.0(April, 2022). So this is why @Shahbaz couldn't reproduce it with mesa 22.2.0.

Things are clear now. Thank you all for the help.

### sy...@chromium.org (2022-11-09)

Thanks Jie, I can limit the workaround to mesa up to 22.1.0. Any pointers on how to parse VkPhysicalDeviceProperties::driverVersion to get it in the X.Y.Z form?

### ji...@intel.com (2022-11-09)

I am not quite sure. We probably should do that in chrome rather angle like this:
https://source.chromium.org/chromium/chromium/src/+/main:gpu/config/gpu_driver_bug_list.json;drc=3d181f693ec651bae7ea2229d7bd285657ad406f;l=3171

### et...@gmail.com (2022-11-09)

Thanks for your investigation :)


### sy...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Nan Wang and Yong Liu! Nice work -- the VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-11-16)

@Jie, FWIW, I found out that mesa uses `VK_MAKE_VERSION` to put in mesa's version in `VkPhysicalDeviceProperties::driverVersion`.

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5ef24b269f6cd4df1a2eb82f10d1b4ddbb43c2d6

commit 5ef24b269f6cd4df1a2eb82f10d1b4ddbb43c2d6
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Nov 16 16:17:53 2022

Vulkan: Limit logicOp dynamic state workaround to old mesa

Bug: chromium:1379201
Change-Id: I618507b118b4420793ec172f3ed1f0dddbb2ae86
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4031492
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/5ef24b269f6cd4df1a2eb82f10d1b4ddbb43c2d6/src/libANGLE/renderer/vulkan/RendererVk.cpp
[modify] https://crrev.com/5ef24b269f6cd4df1a2eb82f10d1b4ddbb43c2d6/src/gpu_info_util/SystemInfo.h
[modify] https://crrev.com/5ef24b269f6cd4df1a2eb82f10d1b4ddbb43c2d6/src/gpu_info_util/SystemInfo.cpp


### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0082503930503bc86dd338f654215cc5e90946eb

commit 0082503930503bc86dd338f654215cc5e90946eb
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 16 22:23:15 2022

Roll ANGLE from 3f9223b265d5 to 2dde73576aa0 (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/3f9223b265d5..2dde73576aa0

2022-11-16 syoussefi@chromium.org Vulkan: `const` render passes
2022-11-16 syoussefi@chromium.org Vulkan: Limit logicOp dynamic state workaround to old mesa

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
Bug: chromium:1379201
Tbr: jonahr@google.com
Change-Id: Ib165b1b0e2b0a890f25df0374c72b96f8904bf80
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4032211
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1072482}

[modify] https://crrev.com/0082503930503bc86dd338f654215cc5e90946eb/DEPS


### gi...@appspot.gserviceaccount.com (2022-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/7e7a47dffca034c50bfc96225e6c910bacc55c0f

commit 7e7a47dffca034c50bfc96225e6c910bacc55c0f
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Nov 17 02:29:20 2022

Vulkan: Adjust logicOp dynamic state workaround

Bug: chromium:1379201
Change-Id: I355d0034de12e5aaf95c160efcace34ff7062337
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4031149
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jie A Chen <jie.a.chen@intel.com>

[modify] https://crrev.com/7e7a47dffca034c50bfc96225e6c910bacc55c0f/src/libANGLE/renderer/vulkan/RendererVk.cpp


### gi...@appspot.gserviceaccount.com (2022-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9e0643eb4d035ea99fc632a1144dd41d7ec41389

commit 9e0643eb4d035ea99fc632a1144dd41d7ec41389
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Nov 17 20:04:18 2022

Roll ANGLE from a6fae3fec809 to 7e7a47dffca0 (1 revision)

https://chromium.googlesource.com/angle/angle.git/+log/a6fae3fec809..7e7a47dffca0

2022-11-17 syoussefi@chromium.org Vulkan: Adjust logicOp dynamic state workaround

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
Bug: chromium:1379201
Tbr: jonahr@google.com
Change-Id: I3ddc643a1141a159c7aed418effeb9c295b5eff8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4032701
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1072994}

[modify] https://crrev.com/9e0643eb4d035ea99fc632a1144dd41d7ec41389/DEPS


### [Deleted User] (2023-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1379201?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061504)*
