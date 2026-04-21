# stack over flow in swiftshader

| Field | Value |
|-------|-------|
| **Issue ID** | [40054943](https://issues.chromium.org/issues/40054943) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Mac |
| **Reporter** | ne...@gmail.com |
| **Assignee** | ni...@google.com |
| **Created** | 2021-02-22 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36

Steps to reproduce the problem:
OS:ubuntu 20.04
Chromium 89.0.4350.4
repro1:
./chrome --use-gl=swiftshader http://localhost:8605/crash.html
It's going to take a few minutes to repro stack overflow. 
It may take longer if the machine performance is poor.Because it need to run 67,108,864+(2^31/32) this code(|draw->primitive += batch|)to triger interger overflow. 

During this period, you can manually close the browser and continue to wait. Because the code is still executing in the background gpu-process.

What is the expected behavior?

What went wrong?
1 |draw->primitive| can be integer overflow and finaly causes stack overflow.
This issue should have existed for a long time.Because that code has not changed for more than a year.
...
primitiveProgress[unit].drawCall = currentDraw;
primitiveProgress[unit].firstPrimitive = primitive;
primitiveProgress[unit].primitiveCount = count - primitive >= batch ? batch : count - primitive;
printf("[mydebug]count:%d,primitive:%d,batch:%d\n",count,primitive,batch) //my debug code
draw->primitive += batch; // primitive can be integer overflow and finaly causes stack overflow

Task &task = taskQueue[qHead];
task.type = Task::PRIMITIVES;
task.primitiveUnit = unit;
...
third_party/swiftshader/src/Renderer/Renderer.cpp	
https://source.chromium.org/chromium/chromium/src/+/master:third_party/swiftshader/src/Renderer/Renderer.cpp;l=845;drc=190c406acc1d8f9db9bcf250abe4621c21ede702;bpv=1?q=Renderer.cpp&ss=chromium%2Fchromium%2Fsrc

2. The output of printf is below:
count:2147483647,primitive:2147483488,batch:32
count:2147483647,primitive:2147483520,batch:32
count:2147483647,primitive:2147483552,batch:32
count:2147483647,primitive:2147483584,batch:32
count:2147483647,primitive:2147483616,batch:32  //2147483616=0x7FFFFFE0
count:2147483647,primitive:-2147483648,batch:32 //integer overflow here
count:2147483647,primitive:-2147483616,batch:32 
count:2147483647,primitive:-2147483584,batch:32
count:2147483647,primitive:-2147483552,batch:32
count:2147483647,primitive:-2147483520,batch:32
count:2147483647,primitive:-2147483488,batch:32
count:2147483647,primitive:-2147483456,batch:32
count:2147483647,primitive:-2147483424,batch:32
count:2147483647,primitive:-2147483392,batch:32

=================================================================
==2696897==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fc1262a7620 at pc 0x7fc153ed6c29 bp 0x7fc126fa8630 sp 0x7fc126fa8628
WRITE of size 4 at 0x7fc1262a7620 thread T17
error: unknown argument '--demangle=True'
    #0 0x7fc153ed6c28 in sw::Renderer::processPrimitiveVertices(int, unsigned int, unsigned int, unsigned int, int) ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:1145
    #1 0x7fc153ed6c28 in ?? ??:0
    #2 0x7fc153ed37b8 in sw::Renderer::executeTask(int) ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:921
    #3 0x7fc153ed37b8 in ?? ??:0

Address 0x7fc1262a7620 is located in stack of thread T17 at offset 1568 in frame
    #0 0x7fc153ed458b in sw::Renderer::processPrimitiveVertices(int, unsigned int, unsigned int, unsigned int, int) ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:1119
    #1 0x7fc153ed458b in ?? ??:0

  This frame has 1 object(s):
    [32, 1568) 'batch' (line 1135) <== Memory access at offset 1568 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
Thread T17 created by T0 (chrome) here:
error: unknown argument '--demangle=True'
    #0 0x55b37183daec in __interceptor_pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:205
    #1 0x55b37183daec in ?? ??:0
    #2 0x7fc154127ac6 in sw::Thread::Thread(void (*)(void*), void*) ./../../third_party/swiftshader/src/Common/Thread.cpp:27
    #3 0x7fc154127ac6 in ?? ??:0
    #4 0x7fc153ed9ca2 in sw::Renderer::initializeThreads() ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:2158
    #5 0x7fc153ed9ca2 in ?? ??:0
    #6 0x7fc153ecbb3e in sw::Renderer::updateConfiguration(bool) ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:2973
    #7 0x7fc153ecbb3e in ?? ??:0
    #8 0x7fc153ecc8e6 in sw::Renderer::draw(sw::DrawType, unsigned int, unsigned int, bool) ./../../third_party/swiftshader/src/Renderer/Renderer.cpp:259
    #9 0x7fc153ecc8e6 in ?? ??:0
    #10 0x7fc1541d5f4f in es2::Context::drawArrays(unsigned int, int, int, int) ./../../third_party/swiftshader/src/OpenGL/libGLESv2/Context.cpp:3622
    #11 0x7fc1541d5f4f in ?? ??:0
    #12 0x7fc15422e350 in gl::DrawArrays(unsigned int, int, int) ./../../third_party/swiftshader/src/OpenGL/libGLESv2/libGLESv2.cpp:1496
    #13 0x7fc15422e350 in ?? ??:0
    #14 0x55b383c2773c in gpu::gles2::GLES2DecoderImpl::HandleDrawArrays(unsigned int, void const volatile*) ./../../gpu/command_buffer/service/gles2_cmd_decoder.cc:11394
    #15 0x55b383c2773c in HandleDrawArrays ./../../gpu/command_buffer/service/gles2_cmd_decoder.cc:11443
    #16 0x55b383c2773c in ?? ??:0
    #17 0x55b383cb2338 in gpu::error::Error gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder.cc:5983
    #18 0x55b383cb2338 in ?? ??:0
    #19 0x55b38495b294 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:69
    #20 0x55b38495b294 in ?? ??:0
    #21 0x55b38495231e in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:517
    #22 0x55b38495231e in ?? ??:0
    #23 0x55b384951c49 in bool IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta, std::__1::tuple<int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > >, void>::Dispatch<gpu::CommandBufferStub, gpu::CommandBufferStub, void, void (gpu::CommandBufferStub::*)(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)>(IPC::Message const*, gpu::CommandBufferStub*, gpu::CommandBufferStub*, void*, void (gpu::CommandBufferStub::*)(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)) ./../../base/tuple.h:52
    #24 0x55b384951c49 in DispatchToMethod<gpu::CommandBufferStub *, void (gpu::CommandBufferStub::*)(int, unsigned int, const std::vector<gpu::SyncToken> &), std::tuple<int, unsigned int, std::vector<gpu::SyncToken> > > ./../../base/tuple.h:60
    #25 0x55b384951c49 in DispatchToMethod<gpu::CommandBufferStub, void (gpu::CommandBufferStub::*)(int, unsigned int, const std::vector<gpu::SyncToken> &), void, std::tuple<int, unsigned int, std::vector<gpu::SyncToken> > > ./../../ipc/ipc_message_templates.h:52
    #26 0x55b384951c49 in Dispatch<gpu::CommandBufferStub, gpu::CommandBufferStub, void, void (gpu::CommandBufferStub::*)(int, unsigned int, const std::vector<gpu::SyncToken> &)> ./../../ipc/ipc_message_templates.h:140
    #27 0x55b384951c49 in ?? ??:0
    #28 0x55b38494f44d in gpu::CommandBufferStub::OnMessageReceived(IPC::Message const&) ./../../gpu/ipc/service/command_buffer_stub.cc:166
    #29 0x55b38494f44d in ?? ??:0
    #30 0x55b384963a78 in gpu::GpuChannel::HandleMessage(IPC::Message const&) ./../../gpu/ipc/service/gpu_channel.cc:630
    #31 0x55b384963a78 in HandleMessage ./../../gpu/ipc/service/gpu_channel.cc:588
    #32 0x55b384963a78 in ?? ??:0
    #33 0x55b38496e4a6 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(IPC::Message const&), base::WeakPtr<gpu::GpuChannel>, IPC::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #34 0x55b38496e4a6 in MakeItSo<void (gpu::GpuChannel::*)(const IPC::Message &), base::WeakPtr<gpu::GpuChannel>, IPC::Message> ./../../base/bind_internal.h:657
    #35 0x55b38496e4a6 in RunImpl<void (gpu::GpuChannel::*)(const IPC::Message &), std::tuple<base::WeakPtr<gpu::GpuChannel>, IPC::Message>, 0, 1> ./../../base/bind_internal.h:710
    #36 0x55b38496e4a6 in RunOnce ./../../base/bind_internal.h:679
    #37 0x55b38496e4a6 in ?? ??:0
    #38 0x55b382b58817 in gpu::Scheduler::RunNextTask() ./../../base/callback.h:101
    #39 0x55b382b58817 in RunNextTask ./../../gpu/command_buffer/service/scheduler.cc:577
    #40 0x55b382b58817 in ?? ??:0
    #41 0x55b382b60844 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::*)(), base::WeakPtr<gpu::Scheduler> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:498
    #42 0x55b382b60844 in MakeItSo<void (gpu::Scheduler::*)(), base::WeakPtr<gpu::Scheduler>> ./../../base/bind_internal.h:657
    #43 0x55b382b60844 in RunImpl<void (gpu::Scheduler::*)(), std::tuple<base::WeakPtr<gpu::Scheduler> >, 0> ./../../base/bind_internal.h:710
    #44 0x55b382b60844 in RunOnce ./../../base/bind_internal.h:679
    #45 0x55b382b60844 in ?? ??:0
    #46 0x55b37db1b53a in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:101
    #47 0x55b37db1b53a in RunTask ./../../base/task/common/task_annotator.cc:163
    #48 0x55b37db1b53a in ?? ??:0
    #49 0x55b37db57463 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351
    #50 0x55b37db57463 in ?? ??:0
    #51 0x55b37db56c24 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264
    #52 0x55b37db56c24 in ?? ??:0
    #53 0x55b37da1aa89 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:374
    #54 0x55b37da1aa89 in WorkSourceDispatch ./../../base/message_loop/message_pump_glib.cc:124
    #55 0x55b37da1aa89 in ?? ??:0
error: unknown argument '--demangle=True'
    #56 0x7fc15e04dfbc in g_main_context_dispatch ??:?
    #57 0x7fc15e04dfbc in ?? ??:0

SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/test/chromium/src/out/release/swiftshader/libGLESv2.so+0x5a2c28)
Shadow bytes around the buggy address:
  0x0ff8a4c4ce70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4ce80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4ce90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4cea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4ceb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0ff8a4c4cec0: 00 00 00 00[f3]f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3
  0x0ff8a4c4ced0: f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4cee0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4cef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ff8a4c4cf00: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0ff8a4c4cf10: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2696897==ABORTING
Received signal 6

Did this work before? N/A 

Chrome version: 89.0.4350.4  Channel: stable
OS Version: 20.04
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 902 B)
- [webgl-test-utils.js](attachments/webgl-test-utils.js) (text/plain, 103.8 KB)

## Timeline

### [Deleted User] (2021-02-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5650305514274816.

### jd...@chromium.org (2021-02-22)

sugoi@: can you take a look at this? ClusterFuzz probably won't be able to reproduce it because of the long time needed, but it seems at least plausible. If you think this bug is invalid, feel free to close it.

Also, is SwiftShader running for actual user? This is either Security_Severity-Medium (OOB write in the renderer, but mitigated because it's so expensive to do) or Security_Severity-None if it's not actually currently shipping.

[Monorail components: Internals>GPU>SwiftShader]

### su...@chromium.org (2021-02-22)

SwiftShader is currently shipping, but it is getting replaced with SwANGLE (ANGLE + SwiftShader Vulkan), so this code is on its way to being deprecated, hopefully this quarter, so we no longer actively fix non critical issues at the moment.

### [Deleted User] (2021-02-23)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2021-02-24)

Looking at this again, I don't think the mitigation is expensive enough to warrant a High->Medium downgrade, so updating severity accordingly.

Thanks for the context. As long as we're shipping vulnerable code to the client, we really should be prioritizing fixing them, especially high severity or higher bugs. Would you mind at least taking enough of a look at this to determine how hard of a fix it should be? Thanks!

### ca...@chromium.org (2021-02-24)

I'll have a closer look at the security severity this represents.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-23)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@google.com (2021-05-06)

Sorry, this fell off my radar. I don't think this poses a real threat. It can only access data at an index of about 2^31 into an small array located on the stack. This will practically always result in a segfault, and even if somehow it hits a valid page, I don't see how this can be used in a controlled manner to be part of any exploit.

Considering the age of this code and the little time left before it will be replaced by SwANGLE, I'm very hesitant to make any changes. Note we've already switched all testing over to use SwANGLE, so it's just WebGL fallback for end users that still uses legacy SwiftShader. More things can go wrong by touching this code than whatever unlikely scenario this overflow can be abused for, in my opinion.

Happy to reconsider if someone can point out something I haven't taken into account.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

Bumping to Low per https://crbug.com/chromium/1180745#c13.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ni...@google.com (2021-09-25)

Windows and Linux have been switched to using SwANGLE instead of legacy SwiftShader. macOS will follow. I don't think there's any value in keeping this open.

### [Deleted User] (2021-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-26)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-09-28)

This bug is not fixed, it's still shipping on macOS. This is a memory corruption in a sandboxed process so is P-1. Please land a fix for this bug as a matter of priority.

### [Deleted User] (2021-10-09)

nicolascapens: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-23)

nicolascapens: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-03-03)

[gpu-triage] Per https://crbug.com/chromium/1180745#c24 we were planning to switch MacOS to SwANGLE, has that been done? Otherwise per https://crbug.com/chromium/1180745#c27 this is a high priority bug.

### ni...@google.com (2022-03-03)

macOS is using SwANGLE now.

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations! The VRP Panel decided to award you $7500 for this report, despite the unusual circumstances that this issue was not actually fixed, but resolved by  SwANGLE being shipped in Mac OS. We greatly appreciate your efforts and reporting this issue to us. Apologies for the delay in getting this to resolution and thank you again for your efforts and nice work! 

### am...@google.com (2022-03-17)

sent to finance for processing 11 March 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

Adding a 'Release' label for the sake of various analyses. Per https://crbug.com/chromium/1180745#c33 this was fixed around March; that was (roughly) M99.

### pg...@google.com (2022-12-14)

Swangle replaced legacy swiftshader on all platforms with this last cl: https://bugs.chromium.org/p/chromium/issues/detail?id=1060139#c122

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1180745?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054943)*
