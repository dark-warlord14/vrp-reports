# WebGLOnWebGPU: draw allowed with invalid vertex / index buffer state

| Field | Value |
|-------|-------|
| **Issue ID** | [472376568](https://issues.chromium.org/issues/472376568) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2025-12-30 |
| **Bounty** | $8,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

Note: This behavior is specific to the WebGLOnWebGPU path. It requires a Chromium build with WebGLOnWebGPU support enabled and then it can be triggered by launching Chromium with the flag `--enable-blink-features=WebGLOnWebGPU`. The feature is not enabled by default in standard Chromium builds.

---

In the WebGLOnWebGPU path, it is possible to call draw APIs (drawArrays / drawElements) with invalid vertex or index state:

- enabled vertex attributes configured via vertexAttribPointer() while no ARRAY\_BUFFER is bound
- drawElements() called while no valid ELEMENT\_ARRAY\_BUFFER is bound

In these cases, the invalid state reaches ANGLE, which falls back to its client-side attribute handling and interprets the attribute offset with pointer semantics, resulting in a renderer crash due to invalid memory read access. The address range is constrained to non-negative 32-bit values.

This is filed using the security bug template due to potential security relevance. A fix will be provided separately.

VERSION
Chrome Version: Locally built Chromium (WebGLOnWebGPU enabled)
Operating System: Windows 11 x64

REPRODUCTION CASE
Please see 01\_minimize.html and 02\_minimize.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

Crash stack for vertexAttribPointer (01-minimize.html):

```
=================================================================
==13424==ERROR: AddressSanitizer: access-violation on unknown address 0x000041414141 (pc 0x7ffb882ddc7d bp 0x0045ca1fcf50 sp 0x0045ca1fcec8 T0)
==13424==The signal is caused by a READ memory access.
==13424==*** WARNING: Failed to initialize DbgHelp!              ***
==13424==*** Most likely this means that the app is already      ***
==13424==*** using DbgHelp, possibly with incompatible flags.    ***
==13424==*** Due to technical reasons, symbolization might crash ***
==13424==*** or produce wrong results.                           ***
    #0 0x7ffb882ddc7c  (C:\Windows\System32\ucrtbase.dll+0x1800edc7c)
    #1 0x7ffac746b422  (C:\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b422)
    #2 0x7ffa8c03d13d in rx::CopyNativeVertexData<float, 3, 3, 0>(unsigned char const *, unsigned __int64, unsigned __int64, unsigned char *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h:69:9
    #3 0x7ffa8c988aa3 in rx::VertexArrayWgpu::syncClientArrays(class gl::Context const *, class angle::BitSetT<16, unsigned __int64, unsigned __int64> const &, enum gl::PrimitiveMode, int, int, int, enum gl::DrawElementsType, void const *, int, bool, void const **, unsigned int *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\VertexArrayWgpu.cpp:377:9
    #4 0x7ffa8c951f1c in rx::ContextWgpu::setupDraw(class gl::Context const *, enum gl::PrimitiveMode, int, int, int, enum gl::DrawElementsType, void const *, int, unsigned int *, unsigned int *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\ContextWgpu.cpp:1205:36
    #5 0x7ffa8c951b19 in rx::ContextWgpu::drawArrays(class gl::Context const *, enum gl::PrimitiveMode, int, int) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\ContextWgpu.cpp:288:15
    #6 0x7ffab46256d0 in gl::Context::drawArrays C:\src\chromium\src\third_party\angle\src\libANGLE\Context.inl.h:168
    #7 0x7ffab46256d0 in GL_DrawArrays C:\src\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:1794:22
    #8 0x7ffab1e21c3e in blink::`anonymous namespace'::v8_webgl2_rendering_context_webgpu::DrawArraysOperationCallback C:\src\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context_webgpu.cc:3308:17
    #9 0x7ffab67e81aa in Builtins_CallApiCallbackGeneric (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0381aa)
    #10 0x7ffab67e63a9 in Builtins_InterpreterEntryTrampoline (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0363a9)
    #11 0x7ffab68280ed in Builtins_AsyncFunctionAwaitResolveClosure (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0780ed)
    #12 0x7ffab6912ea9 in Builtins_PromiseFulfillReactionJob (C:\src\chromium\src\out\asan\chrome.dll+0x1ad162ea9)
    #13 0x7ffab6816706 in Builtins_RunMicrotasks (C:\src\chromium\src\out\asan\chrome.dll+0x1ad066706)
    #14 0x7ffab67e303e in Builtins_JSRunMicrotasksEntry (C:\src\chromium\src\out\asan\chrome.dll+0x1ad03303e)
    #15 0x7ffa8f47b037 in v8::internal::GeneratedCode<unsigned long long,unsigned long long,v8::internal::MicrotaskQueue *>::Call C:\src\chromium\src\v8\src\execution\simulator.h:216
    #16 0x7ffa8f47b037 in v8::internal::`anonymous namespace'::Invoke C:\src\chromium\src\v8\src\execution\execution.cc:460:41
    #17 0x7ffa8f47e659 in v8::internal::`anonymous namespace'::InvokeWithTryCatch C:\src\chromium\src\v8\src\execution\execution.cc:502:18
    #18 0x7ffa8f47eb1b in v8::internal::Execution::TryRunMicrotasks(class v8::internal::Isolate *, class v8::internal::MicrotaskQueue *) C:\src\chromium\src\v8\src\execution\execution.cc:606:10
    #19 0x7ffa8f51ef39 in v8::internal::MicrotaskQueue::RunMicrotasks(class v8::internal::Isolate *) C:\src\chromium\src\v8\src\execution\microtask-queue.cc:185:22
    #20 0x7ffa8f520ca7 in v8::internal::MicrotaskQueue::PerformCheckpointInternal C:\src\chromium\src\v8\src\execution\microtask-queue.cc:129
    #21 0x7ffa8f520ca7 in v8::internal::MicrotaskQueue::PerformCheckpoint(class v8::Isolate *) C:\src\chromium\src\v8\src\execution\microtask-queue.h:48:5
    #22 0x7ffa9764c1af in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\common\event_loop.cc:80:21
    #23 0x7ffa9767d19e in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\agent_group_scheduler_impl.cc:118:12
    #24 0x7ffa976bd816 in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:1180:28
    #25 0x7ffa976cec81 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(class base::WeakPtr<class blink::scheduler::MainThreadTaskQueue>, struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:2510:3
    #26 0x7ffa976ec324 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_task_queue.cc:140:29
    #27 0x7ffa976efc6b in base::internal::DecayedFunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>::Invoke C:\src\chromium\src\base\functional\bind_internal.h:730
    #28 0x7ffa976efc6b in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,void,0>::MakeItSo C:\src\chromium\src\base\functional\bind_internal.h:922
    #29 0x7ffa976efc6b in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0> >,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::RunImpl C:\src\chromium\src\base\functional\bind_internal.h:1059
    #30 0x7ffa976efc6b in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::scheduler::MainThreadTaskQueue::*const &)(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *), class blink::scheduler::MainThreadTaskQueue *>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::scheduler::MainThreadTaskQueue::*)(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *), class base::internal::UnretainedWrapper<class blink::scheduler::MainThreadTaskQueue, struct base::unretained_traits::MayNotDangle, 0>>, (struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *)>::Run(class base::internal::BindStateBase *, struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\base\functional\bind_internal.h:979:12
    #31 0x7ffaa29019ea in base::RepeatingCallback<void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run C:\src\chromium\src\base\functional\callback.h:343
    #32 0x7ffaa29019ea in base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\task_queue_impl.cc:1354:50
    #33 0x7ffa9d25c9bb in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(struct base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask *, class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:915:35
    #34 0x7ffa9d25c5d8 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(class base::LazyNow &) C:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:665:3
    #35 0x7ffaa291b5b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:488:37
    #36 0x7ffaa291a2b3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #37 0x7ffaa2962b7e in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\src\chromium\src\base\message_loop\message_pump_default.cc:42:55
    #38 0x7ffaa291d12f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647:12
    #39 0x7ffa9d2eb0fc in base::RunLoop::Run(class base::Location const &) C:\src\chromium\src\base\run_loop.cc:135:14
    #40 0x7ffaa075605d in content::RendererMain(struct content::MainFunctionParams) C:\src\chromium\src\content\renderer\renderer_main.cc:360:16
    #41 0x7ffa99df6c01 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\src\chromium\src\content\app\content_main_runner_impl.cc:771:14
    #42 0x7ffa99df9092 in content::ContentMainRunnerImpl::Run(void) C:\src\chromium\src\content\app\content_main_runner_impl.cc:1137:10
    #43 0x7ffa99ded17f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\src\chromium\src\content\app\content_main.cc:358:36
    #44 0x7ffa99ded922 in content::ContentMain(struct content::ContentMainParams) C:\src\chromium\src\content\app\content_main.cc:371:10
    #45 0x7ffa897b2b06 in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:191:12
    #46 0x7ff668544807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:201:12
    #47 0x7ff668542074 in main C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351:20
    #48 0x7ff668a23a1f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #49 0x7ff668a23a1f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #50 0x7ffb8890e8d6  (C:\Windows\System32\KERNEL32.DLL+0x18002e8d6)
    #51 0x7ffb8a62c53b  (C:\Windows\SYSTEM32\ntdll.dll+0x18008c53b)

==13424==Register values:
rax = 129400050000  rbx = 129400050000  rcx = 129400050000  rdx = 41414141
rdi = 41414141  rsi = 24  rbp = 45ca1fcf50  rsp = 45ca1fcec8
r8  = 24  r9  = 41414165  r10 = 7ffb881f0000  r11 = 0
r12 = 0  r13 = 129400050000  r14 = 41414141  r15 = ffffffffffffffe3
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\Windows\System32\ucrtbase.dll+0x1800edc7c)

==13424==ADDITIONAL INFO

==13424==Note: Please include this section with the ASan report.
Task trace:


Command line: `"C:\src\chromium\src\out\asan\chrome.exe" --type=renderer --origin-trial-disabled-features=CanvasTextNg|WebAssemblyCustomDescriptors --no-pre-read-main-dll --start-stack-profiler --no-sandbox --enable-blink-features=WebGLOnWebGPU --video-capture-use-gpu-memory-buffer --lang=zh-CN --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=7 --time-ticks-at-unix-epoch=-1765398706846167 --launch-time-ticks=1591602904288 --metrics-shmem-handle=4944,i,11130632830184071275,4824128275539787136,2097152 --field-trial-handle=1900,i,1830540108335661940,10639675262829550042,262144 --variations-seed-version --trace-process-track-uuid=3190708992871164437 --enable-logging=stderr --mojo-platform-channel-handle=4312 /prefetch:1`

```

Crash stack for drawElements (02-minimize.html):

```
=================================================================
==19832==ERROR: AddressSanitizer: access-violation on unknown address 0x000042424242 (pc 0x7ffb882ddbf0 bp 0x00a8e9bfcda0 sp 0x00a8e9bfcd18 T0)
==19832==The signal is caused by a READ memory access.
==19832==*** WARNING: Failed to initialize DbgHelp!              ***
==19832==*** Most likely this means that the app is already      ***
==19832==*** using DbgHelp, possibly with incompatible flags.    ***
==19832==*** Due to technical reasons, symbolization might crash ***
==19832==*** or produce wrong results.                           ***
    #0 0x7ffb882ddbef  (C:\Windows\System32\ucrtbase.dll+0x1800edbef)
    #1 0x7ffac746b422  (C:\src\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b422)
    #2 0x7ffa8c98be88 in rx::`anonymous namespace'::CopyIndexData<unsigned short,unsigned short> C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\VertexArrayWgpu.cpp:63:9
    #3 0x7ffa8c98af69 in rx::VertexArrayWgpu::streamIndicesDefault(class rx::ContextWgpu *, enum gl::DrawElementsType, enum gl::DrawElementsType, enum gl::PrimitiveMode, int, void const *, unsigned char *, unsigned __int64, class rx::webgpu::BufferHelper *, class std::__Cr::vector<struct rx::VertexArrayWgpu::BufferCopy, class std::__Cr::allocator<struct rx::VertexArrayWgpu::BufferCopy>> *, unsigned __int64 *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\VertexArrayWgpu.cpp:777:5
    #4 0x7ffa8c989167 in rx::VertexArrayWgpu::syncClientArrays(class gl::Context const *, class angle::BitSetT<16, unsigned __int64, unsigned __int64> const &, enum gl::PrimitiveMode, int, int, int, enum gl::DrawElementsType, void const *, int, bool, void const **, unsigned int *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\VertexArrayWgpu.cpp:324:27
    #5 0x7ffa8c951f1c in rx::ContextWgpu::setupDraw(class gl::Context const *, enum gl::PrimitiveMode, int, int, int, enum gl::DrawElementsType, void const *, int, unsigned int *, unsigned int *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\ContextWgpu.cpp:1205:36
    #6 0x7ffa8c95305c in rx::ContextWgpu::drawElements(class gl::Context const *, enum gl::PrimitiveMode, int, enum gl::DrawElementsType, void const *) C:\src\chromium\src\third_party\angle\src\libANGLE\renderer\wgpu\ContextWgpu.cpp:374:15
    #7 0x7ffab462643b in gl::Context::drawElements C:\src\chromium\src\third_party\angle\src\libANGLE\Context.inl.h:185
    #8 0x7ffab462643b in GL_DrawElements C:\src\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:1836:22
    #9 0x7ffab1e224e3 in blink::`anonymous namespace'::v8_webgl2_rendering_context_webgpu::DrawElementsOperationCallback C:\src\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl2_rendering_context_webgpu.cc:3429:17
    #10 0x7ffab67e81aa in Builtins_CallApiCallbackGeneric (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0381aa)
    #11 0x7ffab67e63a9 in Builtins_InterpreterEntryTrampoline (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0363a9)
    #12 0x7ffab68280ed in Builtins_AsyncFunctionAwaitResolveClosure (C:\src\chromium\src\out\asan\chrome.dll+0x1ad0780ed)
    #13 0x7ffab6912ea9 in Builtins_PromiseFulfillReactionJob (C:\src\chromium\src\out\asan\chrome.dll+0x1ad162ea9)
    #14 0x7ffab6816706 in Builtins_RunMicrotasks (C:\src\chromium\src\out\asan\chrome.dll+0x1ad066706)
    #15 0x7ffab67e303e in Builtins_JSRunMicrotasksEntry (C:\src\chromium\src\out\asan\chrome.dll+0x1ad03303e)
    #16 0x7ffa8f47b037 in v8::internal::GeneratedCode<unsigned long long,unsigned long long,v8::internal::MicrotaskQueue *>::Call C:\src\chromium\src\v8\src\execution\simulator.h:216
    #17 0x7ffa8f47b037 in v8::internal::`anonymous namespace'::Invoke C:\src\chromium\src\v8\src\execution\execution.cc:460:41
    #18 0x7ffa8f47e659 in v8::internal::`anonymous namespace'::InvokeWithTryCatch C:\src\chromium\src\v8\src\execution\execution.cc:502:18
    #19 0x7ffa8f47eb1b in v8::internal::Execution::TryRunMicrotasks(class v8::internal::Isolate *, class v8::internal::MicrotaskQueue *) C:\src\chromium\src\v8\src\execution\execution.cc:606:10
    #20 0x7ffa8f51ef39 in v8::internal::MicrotaskQueue::RunMicrotasks(class v8::internal::Isolate *) C:\src\chromium\src\v8\src\execution\microtask-queue.cc:185:22
    #21 0x7ffa8f520ca7 in v8::internal::MicrotaskQueue::PerformCheckpointInternal C:\src\chromium\src\v8\src\execution\microtask-queue.cc:129
    #22 0x7ffa8f520ca7 in v8::internal::MicrotaskQueue::PerformCheckpoint(class v8::Isolate *) C:\src\chromium\src\v8\src\execution\microtask-queue.h:48:5
    #23 0x7ffa9764c1af in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\common\event_loop.cc:80:21
    #24 0x7ffa9767d19e in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\agent_group_scheduler_impl.cc:118:12
    #25 0x7ffa976bd816 in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint(void) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:1180:28
    #26 0x7ffa976cec81 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(class base::WeakPtr<class blink::scheduler::MainThreadTaskQueue>, struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_scheduler_impl.cc:2510:3
    #27 0x7ffa976ec324 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\third_party\blink\renderer\platform\scheduler\main_thread\main_thread_task_queue.cc:140:29
    #28 0x7ffa976efc6b in base::internal::DecayedFunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>::Invoke C:\src\chromium\src\base\functional\bind_internal.h:730
    #29 0x7ffa976efc6b in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,void,0>::MakeItSo C:\src\chromium\src\base\functional\bind_internal.h:922
    #30 0x7ffa976efc6b in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),blink::scheduler::MainThreadTaskQueue *>,base::internal::BindState<1,1,0,void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *),base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue,base::unretained_traits::MayNotDangle,0> >,void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::RunImpl C:\src\chromium\src\base\functional\bind_internal.h:1059
    #31 0x7ffa976efc6b in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::scheduler::MainThreadTaskQueue::*const &)(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *), class blink::scheduler::MainThreadTaskQueue *>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::scheduler::MainThreadTaskQueue::*)(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *), class base::internal::UnretainedWrapper<class blink::scheduler::MainThreadTaskQueue, struct base::unretained_traits::MayNotDangle, 0>>, (struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *)>::Run(class base::internal::BindStateBase *, struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\base\functional\bind_internal.h:979:12
    #32 0x7ffaa29019ea in base::RepeatingCallback<void (const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *)>::Run C:\src\chromium\src\base\functional\callback.h:343
    #33 0x7ffaa29019ea in base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(struct base::sequence_manager::Task const &, class base::sequence_manager::TaskQueue::TaskTiming *, class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\task_queue_impl.cc:1354:50
    #34 0x7ffa9d25c9bb in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(struct base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask *, class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:915:35
    #35 0x7ffa9d25c5d8 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(class base::LazyNow &) C:\src\chromium\src\base\task\sequence_manager\sequence_manager_impl.cc:665:3
    #36 0x7ffaa291b5b6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:488:37
    #37 0x7ffaa291a2b3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #38 0x7ffaa2962b7e in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\src\chromium\src\base\message_loop\message_pump_default.cc:42:55
    #39 0x7ffaa291d12f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647:12
    #40 0x7ffa9d2eb0fc in base::RunLoop::Run(class base::Location const &) C:\src\chromium\src\base\run_loop.cc:135:14
    #41 0x7ffaa075605d in content::RendererMain(struct content::MainFunctionParams) C:\src\chromium\src\content\renderer\renderer_main.cc:360:16
    #42 0x7ffa99df6c01 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\src\chromium\src\content\app\content_main_runner_impl.cc:771:14
    #43 0x7ffa99df9092 in content::ContentMainRunnerImpl::Run(void) C:\src\chromium\src\content\app\content_main_runner_impl.cc:1137:10
    #44 0x7ffa99ded17f in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\src\chromium\src\content\app\content_main.cc:358:36
    #45 0x7ffa99ded922 in content::ContentMain(struct content::ContentMainParams) C:\src\chromium\src\content\app\content_main.cc:371:10
    #46 0x7ffa897b2b06 in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:191:12
    #47 0x7ff668544807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:201:12
    #48 0x7ff668542074 in main C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:351:20
    #49 0x7ff668a23a1f in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #50 0x7ff668a23a1f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #51 0x7ffb8890e8d6  (C:\Windows\System32\KERNEL32.DLL+0x18002e8d6)
    #52 0x7ffb8a62c53b  (C:\Windows\SYSTEM32\ntdll.dll+0x18008c53b)

==19832==Register values:
rax = 12e700050000  rbx = 12e700050000  rcx = 12e700050000  rdx = 42424242
rdi = 42424242  rsi = 6  rbp = a8e9bfcda0  rsp = a8e9bfcd18
r8  = 6  r9  = 7ffb882ddbf0  r10 = 7ffb881f0000  r11 = 0
r12 = 4b902aaa80  r13 = 3  r14 = 12e700050000  r15 = ffffffffffffffc5
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (C:\Windows\System32\ucrtbase.dll+0x1800edbef)

==19832==ADDITIONAL INFO

==19832==Note: Please include this section with the ASan report.
Task trace:


Command line: `"C:\src\chromium\src\out\asan\chrome.exe" --type=renderer --origin-trial-disabled-features=CanvasTextNg|WebAssemblyCustomDescriptors --no-pre-read-main-dll --no-sandbox --enable-blink-features=WebGLOnWebGPU --video-capture-use-gpu-memory-buffer --lang=zh-CN --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=7 --time-ticks-at-unix-epoch=-1765398706846167 --launch-time-ticks=1592032542759 --metrics-shmem-handle=5956,i,7295815233934873813,11375185996430849483,2097152 --field-trial-handle=1900,i,1830540108335661940,10639675262829550042,262144 --variations-seed-version --trace-process-track-uuid=3190708992871164437 --enable-logging=stderr --mojo-platform-channel-handle=6012 /prefetch:1`


==19832==END OF ADDITIONAL INFO

```

## Attachments

- [01_minimize.html](attachments/01_minimize.html) (text/html, 892 B)
- [02_minimize.html](attachments/02_minimize.html) (text/html, 742 B)

## Timeline

### le...@gmail.com (2025-12-30)

A fix has been uploaded for review:
<https://chromium-review.googlesource.com/c/chromium/src/+/7317007>

### mp...@google.com (2025-12-31)

geofflang@ I'm not sure where validation should occur here, but presumably we should fix this in at least third\_party/angle/src/libANGLE/renderer/wgpu/VertexArrayWgpu.cpp right?

### mp...@google.com (2025-12-31)

FWIW this bug is in a feature that is not enabled anywhere is not really ready for fuzzing or security efforts.

### cw...@chromium.org (2026-01-05)

I commented on the CL, there's a missing option that should be passed on context creation to disallow client arrays.

### dx...@google.com (2026-01-07)

Project: chromium/src  

Branch:  main  

Author:  Wenxiang Qian [leonwxqian@gmail.com](mailto:leonwxqian@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7317007>

[WebGLOnWebGPU] Disable ANGLE client-side array handling

---


Expand for full commit details
```
     
    Configure the ANGLE context used by WebGLOnWebGPU to disable client-side 
    array handling. Also disable implicit buffer creation on bind and enable 
    robust resource initialization. 
     
    This prevents attribute offsets from being interpreted with client-side 
    pointer semantics. 
     
    Bug: 472376568 
    Change-Id: I381353dd1c2995702c276a258483d0f202947ecb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7317007 
    Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Corentin Wallez <cwallez@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1565487}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_webgpu_base.cc`

---

Hash: [b56c9d4512fc4a0ea800f7577cf77eff7680e0fc](https://chromiumdash.appspot.com/commit/b56c9d4512fc4a0ea800f7577cf77eff7680e0fc)  

Date: Wed Jan 7 09:16:39 2026


---

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
baseline memory corruption in sandboxed process with a patch bonus. Thank you for the patch!


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline memory corruption in sandboxed process with a patch bonus. Thank you for the patch!

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/472376568)*
