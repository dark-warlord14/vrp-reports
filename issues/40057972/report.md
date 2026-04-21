# Security:  Wild read with renderbuffers

| Field | Value |
|-------|-------|
| **Issue ID** | [40057972](https://issues.chromium.org/issues/40057972) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Internals, Internals>GPU>SwiftShader |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-11-19 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan spots a wild high read when the attached page is opened. The crash state points to ASan itself, but this could also be a weird way to fail e.g. in a double free condition. Reporting as a Chromium issue to be on the safe side.

**VERSION**  

Chrome Version: 98.0.4711.0  

Operating System: Linux, Debian 11.1

**REPRODUCTION CASE**  

Open the attached page. Issue should reproduce reliably in about a second.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: GPU process Crash State:

==1136444==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x561d1632cb04 bp 0x000000000000 sp 0x7ffcc3326360 T0)  

==1136444==The signal is caused by a READ memory access.  

==1136444==Hint: this fault was caused by a dereference of a high value address (see register values below). Disassemble the provided pc to learn which register was used.  

SCARINESS: 20 (wild-addr-read)  

#0 0x561d1632cb04 in atomic\_compare\_exchange\_strong<\_\_sanitizer::atomic\_uint8\_t> /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_atomic\_clang.h:80:10  

#1 0x561d1632cb04 in AtomicallySetQuarantineFlagIfAllocated /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_allocator.cpp:621:10  

#2 0x561d1632cb04 in \_\_asan::Allocator::Deallocate(void\*, unsigned long, unsigned long, \_\_sanitizer::BufferedStackTrace\*, \_\_asan::AllocType) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_allocator.cpp:697:10

**CREDIT INFORMATION**  

Reporter credit: Aki Helin, Solita

## Attachments

- [chrome-wild-read-renderbuffer.html](attachments/chrome-wild-read-renderbuffer.html) (text/plain, 3.3 KB)

## Timeline

### [Deleted User] (2021-11-19)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-20)

I get this stack trace:

   #0 0x55a2521da7eb in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4264:13
    #1 0x55a264714379 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:872:39
    #2 0x55a2643ee973 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:200:12
    #3 0x55a2643ee973 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:197:28
    #4 0x55a264712d7b in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:369:3
    #5 0x7fa4fb6a18e0 in __funlockfile :?
    #6 0x7fa4fb6a18e0 in ?? ??:0
    #7 0x55a2521a1714 in atomic_compare_exchange_strong<__sanitizer::atomic_uint8_t> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_atomic_clang.h:80:10
    #8 0x55a2521a1714 in AtomicallySetQuarantineFlagIfAllocated /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:621:10
    #9 0x55a2521a1714 in __asan::Allocator::Deallocate(void*, unsigned long, unsigned long, __sanitizer::BufferedStackTrace*, __asan::AllocType) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:697:10
    #10 0x55a252220d56 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:112:3
#7 0x7fa4ee513b16 <unknown>
#8 0x7fa4ee5138d4 <unknown>
#9 0x7fa4ee55dc3f <unknown>
#10 0x7fa4f1d43035 <unknown>
#11 0x7fa4f1b45e3b <unknown>
#12 0x7fa4f1b100ae <unknown>
#13 0x7fa4f19c26a5 <unknown>
#14 0x7fa4f19b6771 <unknown>
#15 0x7fa4f1b2e2b1 <unknown>
#16 0x7fa4f1a02e04 <unknown>
#17 0x7fa4f1a37800 <unknown>
#18 0x7fa4f19f0c65 <unknown>
#19 0x7fa4f0b403b4 <unknown>
    #11 0x55a26ad25bfd in gpu::gles2::GLES2DecoderPassthroughImpl::DoFlush() ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1297:10
    #12 0x55a26ace573f in gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) ./../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858:20
    #13 0x55a26b307209 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) ./../../gpu/command_buffer/service/command_buffer_service.cc:70:18
    #14 0x55a26b2f6ac0 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&) ./../../gpu/ipc/service/command_buffer_stub.cc:499:22
    #15 0x55a26b2f5af5 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) ./../../gpu/ipc/service/command_buffer_stub.cc:151:7
    #16 0x55a26b310b1c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) ./../../gpu/ipc/service/gpu_channel.cc:666:13
    #17 0x55a26b31ef2b in void base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) ./../../base/bind_internal.h:548:12
    #18 0x55a269763aa1 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:142:12
    #19 0x55a269763aa1 in gpu::Scheduler::RunNextTask() ./../../gpu/command_buffer/service/scheduler.cc:685:26
    #20 0x55a2645b8d97 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:142:12
    #21 0x55a2645b8d97 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:135:32
    #22 0x55a264627a6e in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0&&) ./../../base/task/common/task_annotator.h:73:5
    #23 0x55a264627a6e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #24 0x55a264626699 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #25 0x55a264628b92 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x55a26447a15a in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:375:46
    #27 0x55a26447a15a in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:125:43
    #28 0x7fa4fb53bd0b in g_main_context_dispatch ??:0:0
    #29 0x7fa4fb53bfb8 in g_main_context_dispatch ??:?
    #30 0x7fa4fb53bfb8 in ?? ??:0
    #31 0x7fa4fb53c06f in g_main_context_iteration ??:0:0
    #32 0x55a264478fd0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:401:30
    #33 0x55a264629986 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #34 0x55a26452afec in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140:14
    #35 0x55a2729a337d in content::GpuMain(content::MainFunctionParams) ./../../content/gpu/gpu_main.cc:401:14
    #36 0x55a262eb0c6f in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:615:14
    #37 0x55a262eb4a9f in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:687:12
    #38 0x55a262eb71c8 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1028:10
    #39 0x55a262eade17 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:398:36
    #40 0x55a262eafc05 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:426:10
    #41 0x55a25225195d in ChromeMain ./../../chrome/app/chrome_main.cc:172:12
    #42 0x7fa4f9aa0e4a in __libc_start_main ./csu/../csu/libc-start.c:314:16
    #43 0x55a2521a08aa in _start ??:0:0
  r8: 00007ffe72e75be0  r9: 0000000000000001 r10: 0000603000169240 r11: 000060800005bad8
 r12: 0000000000000001 r13: 0000000000000000 r14: 00007ffe72e75be0 r15: 000055a281ea4488
  di: ff0000ffff0000ff  si: ff0000ffff0000ff  bp: 0000000000000000  bx: ff0000ffff0000ff
  dx: 0000000000000000  ax: 0000000000000002  cx: 0000000000000003  sp: 00007ffe72e75ba0
  ip: 000055a2521a1714 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 000000000000000d msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
[3556069:1:1120/005042.934981:ERROR:command_buffer_proxy_impl.cc(328)] GPU state invalid after WaitForGetOffsetInRange.
[3555968:3555968:1120/005042.935775:ERROR:gpu_process_host.cc(962)] GPU process exited unexpectedly: exit_code=11


Assigning to an OWNER of the gpu/command_buffer. I'm not sure whether this is an ASAN bug or something else.

### mp...@chromium.org (2021-11-20)

GDB gives a more helpful stack trace:
#0  0x0000563e05640714 in atomic_compare_exchange_strong<__sanitizer::atomic_uint8_t> () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_atomic_clang.h:80
#1  AtomicallySetQuarantineFlagIfAllocated () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:621
#2  Deallocate() () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_allocator.cpp:697
#3  0x0000563e056bfd56 in __interceptor_free() () at /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:112
#4  0x00007f5736010b16 in vk::DeviceMemory::freeBuffer() (this=<optimized out>) at ../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:335
#5  0x00007f57360108d4 in vk::DeviceMemory::destroy(VkAllocationCallbacks const*) (this=0xff0000ffff0000ff, pAllocator=0xff0000ffff0000ff) at ../../third_party/swiftshader/src/Vulkan/VkDeviceMemory.cpp:152
#6  0x00007f573605ac3f in vk::destroy<VkNonDispatchableHandle<VkDeviceMemory_T*> >(VkNonDispatchableHandle<VkDeviceMemory_T*>, VkAllocationCallbacks const*) (vkObject=..., pAllocator=0x0)
    at ../../third_party/swiftshader/src/Vulkan/VkDestroy.hpp:60
#7  vkFreeMemory(VkDevice, VkDeviceMemory, VkAllocationCallbacks const*) (device=<optimized out>, memory=..., pAllocator=0x0) at ../../third_party/swiftshader/src/Vulkan/libVulkan.cpp:1107
#8  0x00007f5739840035 in rx::vk::GarbageObject::destroy(rx::RendererVk*) (this=<optimized out>, renderer=<optimized out>) at ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_utils.cpp:862
#9  0x00007f5739642e3b in rx::vk::SharedGarbage::destroyIfComplete(rx::RendererVk*, rx::Serial) (this=0x611000086140, renderer=<optimized out>, completedSerial=...)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/ResourceVk.cpp:147
#10 0x00007f573960d0ae in rx::RendererVk::cleanupGarbage(rx::Serial) (this=0x62e00000c400, lastCompletedQueueSerial=...) at ../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3183
#11 0x00007f57394bf6a5 in rx::vk::CommandQueue::queueSubmit(rx::vk::Context*, egl::ContextPriority, VkSubmitInfo const&, rx::vk::Fence const*, rx::Serial)
    (this=<optimized out>, context=<optimized out>, contextPriority=<optimized out>, submitInfo=<optimized out>, fence=<optimized out>, submitQueueSerial=...)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:1249
#12 0x00007f57394b3771 in rx::vk::CommandQueue::submitFrame(rx::vk::Context*, bool, egl::ContextPriority, std::__1::vector<VkSemaphore_T*, std::__1::allocator<VkSemaphore_T*> > const&, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> > const&, rx::vk::Semaphore const*, std::__1::vector<rx::vk::GarbageObject, std::__1::allocator<rx::vk::GarbageObject> >&&, std::__1::vector<rx::vk::priv::SecondaryCommandBuffer, std::__1::allocator<rx::vk::priv::SecondaryCommandBuffer> >&&, rx::vk::CommandPool*, rx::Serial) (this=
    0x62e000015400, context=<optimized out>, hasProtectedContent=false, priority=<optimized out>, waitSemaphores=<optimized out>, waitSemaphoreStageMasks=<optimized out>, signalSemaphore=<optimized out>, currentGarbage=<optimized out>, commandBuffersToReset=<optimized out>, commandPool=<optimized out>, submitQueueSerial=...) at ../../third_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:1067
#13 0x00007f573962b2b1 in rx::RendererVk::submitFrame(rx::vk::Context*, bool, egl::ContextPriority, std::__1::vector<VkSemaphore_T*, std::__1::allocator<VkSemaphore_T*> >&&, std::__1::vector<unsigned int, std::__1::allocator<unsigned int> >&&, rx::vk::Semaphore const*, std::__1::vector<rx::vk::ResourceUseList, std::__1::allocator<rx::vk::ResourceUseList> >&&, std::__1::vector<rx::vk::GarbageObject, std::__1::allocator<rx::vk::GarbageObject> >&&, rx::vk::CommandPool*, rx::Serial*)
    (this=<optimized out>, context=<optimized out>, hasProtectedContent=false, contextPriority=egl::ContextPriority::Medium, waitSemaphores=..., waitSemaphoreStageMasks=..., signalSemaphore=0x0, resourceUseLists=..., currentGarbage=..., commandPool=0x62e000056658, submitSerialOut=0x7f573ec25b20) at ../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3348
#14 0x00007f57394ffe04 in rx::ContextVk::submitFrame(rx::vk::Semaphore const*, rx::Serial*) (this=this@entry=
    0x62e000054400, signalSemaphore=signalSemaphore@entry=0x0, submitSerialOut=submitSerialOut@entry=0x7f573ec25b20) at ../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:2266
#15 0x00007f5739534800 in rx::ContextVk::flushAndGetSerial(rx::vk::Semaphore const*, rx::Serial*, rx::RenderPassClosureReason)
    (this=<optimized out>, signalSemaphore=<optimized out>, submitSerialOut=<optimized out>, renderPassClosureReason=<optimized out>) at ../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:5460
#16 0x00007f57394edc65 in rx::ContextVk::flushImpl(rx::vk::Semaphore const*, rx::RenderPassClosureReason) (this=0x62e000054400, signalSemaphore=0x0, renderPassClosureReason=rx::RenderPassClosureReason::GLFlush)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:5397
#17 rx::ContextVk::flush(gl::Context const*) (this=0x62e000054400, context=<optimized out>) at ../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:914
#18 0x00007f573863d3b4 in GL_Flush() () at ../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1227
#19 0x0000563e1e1c4bfd in gpu::gles2::GLES2DecoderPassthroughImpl::DoFlush() (this=0x625000717100) at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1297
#20 0x0000563e1e18473f in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)
    (this=<optimized out>, num_commands=<optimized out>, buffer=<optimized out>, num_entries=27, entries_processed=0x7f573ef08510) at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858
#21 0x0000563e1e7a6209 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) (this=<optimized out>, put_offset=<optimized out>, handler=0x625000717138)
    at ../../gpu/command_buffer/service/command_buffer_service.cc:70
#22 0x0000563e1e795ac0 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__1::vector<gpu::SyncToken, std::__1::allocator<gpu::SyncToken> > const&)
    (this=<optimized out>, put_offset=578, flush_id=<optimized out>, sync_token_fences=<optimized out>) at ../../gpu/ipc/service/command_buffer_stub.cc:499
#23 0x0000563e1e794af5 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) (this=<optimized out>, params=<optimized out>)
    at ../../gpu/ipc/service/command_buffer_stub.cc:151
#24 0x0000563e1e7afb1c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) (this=<optimized out>, params=...) at ../../gpu/ipc/service/gpu_channel.cc:666
#25 0x0000563e1e7bdf2b in base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>--Type <RET> for more, q to quit, c to continue without paging--
&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) (method=<optimized out>, receiver_ptr=<optimized out>, args=<optimized out>) at ../../base/bind_internal.h:548
#26 0x0000563e1cc02aa1 in base::OnceCallback<void ()>::Run() && (this=0x7f573f107ba0) at ../../base/callback.h:142
#27 gpu::Scheduler::RunNextTask() (this=0x60c00003b5c0) at ../../gpu/command_buffer/service/scheduler.cc:685
#28 0x0000563e17a57d97 in base::OnceCallback<void ()>::Run() && (this=<optimized out>) at ../../base/callback.h:142
#29 base::TaskAnnotator::RunTaskImpl(base::PendingTask&) (this=<optimized out>, pending_task=...) at ../../base/task/common/task_annotator.cc:135
#30 0x0000563e17ac6a6e in base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0&&)
    (this=0x616000000e40, pending_task=<optimized out>, event_name=..., args=<optimized out>) at ../../base/task/common/task_annotator.h:73
#31 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) (this=<optimized out>, continuation_lazy_now=<optimized out>)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
#32 0x0000563e17ac5699 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() (this=0x616000000c80)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
#33 0x0000563e17ac7b92 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ()
#34 0x0000563e1791915a in base::MessagePumpGlib::HandleDispatch() (this=<optimized out>) at ../../base/message_loop/message_pump_glib.cc:375
#35 base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) (source=<optimized out>, unused_func=<optimized out>, unused_data=<optimized out>)
    at ../../base/message_loop/message_pump_glib.cc:125
#36 0x00007f5743038d0b in g_main_context_dispatch () at /lib/x86_64-linux-gnu/libglib-2.0.so.0
#37 0x00007f5743038fb8 in  () at /lib/x86_64-linux-gnu/libglib-2.0.so.0
#38 0x00007f574303906f in g_main_context_iteration () at /lib/x86_64-linux-gnu/libglib-2.0.so.0
#39 0x0000563e17917fd0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) (this=<optimized out>, delegate=<optimized out>) at ../../base/message_loop/message_pump_glib.cc:401
#40 0x0000563e17ac8986 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) (this=0x616000000c80, application_tasks_allowed=<optimized out>, timeout=...)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468
#41 0x0000563e179c9fec in base::RunLoop::Run(base::Location const&) (this=<optimized out>, location=<optimized out>) at ../../base/run_loop.cc:140
#42 0x0000563e25e4237d in content::GpuMain(content::MainFunctionParams) (parameters=...) at ../../content/gpu/gpu_main.cc:401
#43 0x0000563e1634fc6f in content::RunZygote(content::ContentMainDelegate*) (delegate=0x7f573eeff020) at ../../content/app/content_main_runner_impl.cc:615
#44 0x0000563e16353a9f in content::RunOtherNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) (process_type=<optimized out>, main_function_params=..., delegate=<optimized out>) at ../../content/app/content_main_runner_impl.cc:687
#45 0x0000563e163561c8 in content::ContentMainRunnerImpl::Run() (this=<optimized out>) at ../../content/app/content_main_runner_impl.cc:1028
#46 0x0000563e1634ce17 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) (params=..., content_main_runner=<optimized out>) at ../../content/app/content_main.cc:398
#47 0x0000563e1634ec05 in content::ContentMain(content::ContentMainParams) (params=...) at ../../content/app/content_main.cc:426
#48 0x0000563e056f095d in ChromeMain(int, char const**) (argc=<optimized out>, argv=<optimized out>) at ../../chrome/app/chrome_main.cc:172
#49 0x00007f574159de4a in __libc_start_main (main=
    0x563e056f06c0 <main(int, char const**)>, argc=8, argv=0x7ffddc6a5de8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7ffddc6a5dd8) at ../csu/libc-start.c:314
#50 0x0000563e0563f8aa in _start (

### cl...@chromium.org (2021-11-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5716021287387136.

### mp...@chromium.org (2021-11-20)

And with a non-ASAN build:

#0  0x00007f960510da0d in std::__Cr::default_delete<vk::CommandBuffer::Command>::operator()(vk::CommandBuffer::Command*) const (this=0x55ca16b873f8, __ptr=0x55ca16b938e0)
    at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54
#1  std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >::reset(vk::CommandBuffer::Command*) (this=0x55ca16b873f8, __p=0x0)
    at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315
#2  std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >::~unique_ptr() (this=0x55ca16b873f8)
    at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269
#3  std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > >::destroy(std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >*) (this=0x55ca16c4d988, __p=0x55ca16b873f8) at ../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:133
#4  std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > > >::destroy<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >, void>(std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > >&, std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >*) (__a=..., __p=0x55ca16b873f8)
    at ../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:308
#5  std::__Cr::__vector_base<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >, std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > > >::__destruct_at_end(std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >*)
    (this=0x55ca16c4d978, __new_last=0x55ca16b87380) at ../../buildtools/third_party/libc++/trunk/include/vector:429
#6  std::__Cr::__vector_base<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >, std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > > >::clear() (this=0x55ca16c4d978) at ../../buildtools/third_party/libc++/trunk/include/vector:372
#7  std::__Cr::vector<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> >, std::__Cr::allocator<std::__Cr::unique_ptr<vk::CommandBuffer::Command, std::__Cr::default_delete<vk::CommandBuffer::Command> > > >::clear() (this=0x55ca16c4d978) at ../../buildtools/third_party/libc++/trunk/include/vector:775
#8  vk::CommandBuffer::resetState() (this=0x55ca16c4d968) at ../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1233
#9  vk::CommandBuffer::reset(unsigned int) (this=0x55ca16c4d968, flags=<optimized out>) at ../../third_party/swiftshader/src/Vulkan/VkCommandBuffer.cpp:1297
#10 0x00007f96044696c4 in DispatchResetCommandBuffer(VkCommandBuffer_T*, unsigned int) (commandBuffer=0x55ca16c4d960, flags=0)
    at ../../third_party/vulkan-deps/vulkan-validation-layers/src/layers/generated/layer_chassis_dispatch.cpp:2704
#11 0x00007f96043ae2ce in vulkan_layer_chassis::ResetCommandBuffer(VkCommandBuffer_T*, unsigned int) (commandBuffer=0x55ca16c4d960, flags=0)
    at ../../third_party/vulkan-deps/vulkan-validation-layers/src/layers/generated/chassis.cpp:2691
#12 0x00007f96067f553e in rx::vk::priv::CommandBuffer::reset() (this=0x55ca16cc62d8) at ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_wrapper.h:712
#13 0x00007f96067f4bbc in rx::vk::PersistentCommandPool::collect(rx::vk::Context*, rx::vk::priv::CommandBuffer&&) (this=0x55ca16009780, context=0x55ca16c9aca8, buffer=...)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/PersistentCommandPool.cpp:90
#14 0x00007f96067681c5 in rx::vk::CommandQueue::retireFinishedCommands(rx::vk::Context*, unsigned long) (this=0x55ca16009740, context=0x55ca16c9aca8, finishedCount=1)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:886
#15 0x00007f9606763f1b in rx::vk::CommandQueue::finishToSerial(rx::vk::Context*, rx::Serial, unsigned long) (this=0x55ca16009740, context=0x55ca16c9aca8, finishSerial=..., timeout=120000000000)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:1006
#16 0x00007f9606765044 in rx::vk::CommandQueue::waitIdle(rx::vk::Context*, unsigned long) (this=0x55ca16009740, context=0x55ca16c9aca8, timeout=120000000000)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/CommandProcessor.cpp:1014
#17 0x00007f960683bf6c in rx::RendererVk::finish(rx::vk::Context*, bool) (this=0x55ca16000740, context=0x55ca16c9aca8, hasProtectedContent=false)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/RendererVk.cpp:3426
#18 0x00007f9606784c85 in rx::ContextVk::finishImpl(rx::RenderPassClosureReason) (this=0x55ca16c9ac80, renderPassClosureReason=rx::RenderPassClosureReason::GLReadPixels)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/ContextVk.cpp:5487
#19 0x00007f9606941ca9 in rx::vk::ImageHelper::readPixels(rx::ContextVk*, gl::RectangleImpl<int> const&, rx::PackPixelsParams const&, VkImageAspectFlagBits, gl::LevelIndexWrapper<int>, unsigned int, void*, rx::vk::DynamicBuffer*) (this=
    0x55ca169249e0, contextVk=0x55ca16c9ac80, area=..., packPixelsParams=..., copyAspectFlags=VK_IMAGE_ASPECT_COLOR_BIT, levelGL=..., layer=0, pixels=0x7f95ddefa040, stagingBuffer=0x55ca1691cfa8)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/vk_helpers.cpp:7373
#20 0x00007f96067d9f63 in rx::FramebufferVk::readPixelsImpl(rx::ContextVk*, gl::RectangleImpl<int> const&, rx::PackPixelsParams const&, VkImageAspectFlagBits, rx::RenderTargetVk*, void*)
    (this=0x55ca1691cf10, contextVk=0x55ca16c9ac80, area=..., packPixelsParams=..., copyAspectFlags=VK_IMAGE_ASPECT_COLOR_BIT, renderTarget=0x7f95a0029650, pixels=0x7f95ddefa040)
    at ../../third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:2734
#21 0x00007f96067d9d44 in rx::FramebufferVk::readPixels(gl::Context const*, gl::RectangleImpl<int> const&, unsigned int, unsigned int, gl::PixelPackState const&, gl::Buffer*, void*)
    (this=0x55ca1691cf10, context=0x55ca16c94f40, area=..., format=6408, type=5121, pack=..., packBuffer=0x0, pixels=0x7f95ddefa040) at ../../third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp:787
#22 0x00007f9606124ceb in gl::Framebuffer::readPixels(gl::Context const*, gl::RectangleImpl<int> const&, unsigned int, unsigned int, gl::PixelPackState const&, gl::Buffer*, void*)
    (this=0x55ca1691b950, context=0x55ca16c94f40, area=..., format=6408, type=5121, pack=..., packBuffer=0x0, pixels=0x7f95ddefa040) at ../../third_party/angle/src/libANGLE/Framebuffer.cpp:1681
#23 0x00007f96060669d8 in gl::Context::readPixels(int, int, int, int, unsigned int, unsigned int, void*) (this=0x55ca16c94f40, x=0, y=0, width=300, height=150, format=6408, type=5121, pixels=0x7f95ddefa040)
    at ../../third_party/angle/src/libANGLE/Context.cpp:4438
#24 0x00007f9606066ace in gl::Context::readPixelsRobust(int, int, int, int, unsigned int, unsigned int, int, int*, int*, int*, void*)
    (this=0x55ca16c94f40, x=0, y=0, width=300, height=150, format=6408, type=5121, bufSize=262080, length=0x7ffd3a52c5ac, columns=0x7ffd3a52c5a8, rows=0x7ffd3a52c5a4, pixels=0x7f95ddefa040)
    at ../../third_party/angle/src/libANGLE/Context.cpp:4453
#25 0x00007f9605fef8f3 in GL_ReadPixelsRobustANGLE(GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLsizei, GLsizei*, GLsizei*, GLsizei*, void*)
    (x=0, y=0, width=300, height=150, format=6408, type=5121, bufSize=262080, length=0x7ffd3a52c5ac, columns=0x7ffd3a52c5a8, rows=0x7ffd3a52c5a4, pixels=0x7f95ddefa040)
    at ../../third_party/angle/src/libGLESv2/entry_points_gles_ext_autogen.cpp:1625
#26 0x00007f960601c827 in glReadPixelsRobustANGLE(GLint, GLint, GLsizei, GLsizei, GLenum, GLenum, GLsizei, GLsizei*, GLsizei*, GLsizei*, void*)
    (x=0, y=0, width=300, height=150, format=6408, type=5121, bufSize=262080, length=0x7ffd3a52c5ac, columns=0x7ffd3a52c5a8, rows=0x7ffd3a52c5a4, pixels=0x7f95ddefa040)
    at ../../third_party/angle/src/libGLESv2/libGLESv2_autogen.cpp:3174
#27 0x00007f964c913209 in gl::GLApiBase::glReadPixelsRobustANGLEFn(int, int, int, int, unsigned int, unsigned int, int, int*, int*, int*, void*) (this=
    0x55ca16cafba0, x=0, y=0, width=300, height=150, format=6408, type=5121, bufSize=262080, length=0x7ffd3a52c5ac, columns=0x7ffd3a52c5a8, rows=0x7ffd3a52c5a4, pixels=0x7f95ddefa040)
    at ../../ui/gl/gl_bindings_autogen_gl.cc:5517
#28 0x00007f961a3df681 in gpu::gles2::GLES2DecoderPassthroughImpl::DoReadPixels(int, int, int, int, unsigned int, unsigned int, int, int*, int*, int*, void*, int*) (this=
    0x55ca16c91f30, x=0, y=0, width=300, height=150, format=6408, type=5121, bufsize=262080, length=0x7ffd3a52c5ac, columns=0x7ffd3a52c5a8, rows=0x7ffd3a52c5a4, pixels=0x7f95ddefa040, success=0x7ffd3a52c5a0)
    at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:2480
#29 0x00007f961a4073cb in gpu::gles2::GLES2DecoderPassthroughImpl::HandleReadPixels(unsigned int, void const volatile*) (this=0x55ca16c91f30, immediate_data_size=0, cmd_data=0x7f95ddcfa86c)
    at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_handlers.cc:1104
#30 0x00007f961a3bac75 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)
    (this=0x55ca16c91f30, num_commands=20, buffer=0x7f95ddcfa86c, num_entries=12, entries_processed=0x7ffd3a52c7dc) at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:858
#31 0x00007f961a3ab795 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int, void const volatile*, int, int*)
    (this=0x55ca16c91f30, num_commands=20, buffer=0x7f95ddcfa86c, num_entries=12, entries_processed=0x7ffd3a52c7dc) at ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:796
#32 0x00007f964ce752c1 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) (this=0x55ca16c807d0, put_offset=551, handler=0x55ca16c91f68)
    at ../../gpu/command_buffer/service/command_buffer_service.cc:70
#33 0x00007f9619c8631f in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken> > const&) (this=
    0x55ca16c8dfc0, put_offset=551, flush_id=15, sync_token_fences=...) at ../../gpu/ipc/service/command_buffer_stub.cc:499
#34 0x00007f9619c85bd3 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&) (this=0x55ca16c8dfc0, params=...) at ../../gpu/ipc/service/command_buffer_stub.cc:151
#35 0x00007f9619ca7b73 in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>) (this=0x7f95a000cc20, params=...) at ../../gpu/ipc/service/gpu_channel.cc:666
#36 0x00007f9619cb5b14 in base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), void>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) (method=
    (void (gpu::GpuChannel::*)(gpu::GpuChannel * const, mojo::StructPtr<gpu::mojom::DeferredRequestParams>)) 0x7f9619ca79b0 <gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)>, receiver_ptr=..., args=...) at ../../base/bind_internal.h:548
#37 0x00007f9619cb597c in base::internal::InvokeHelper<true, void>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&) (functor=
    @0x7f95a0026000: (void (gpu::GpuChannel::*)(gpu::GpuChannel * const, mojo::StructPtr<gpu::mojom::DeferredRequestParams>)) 0x7f9619ca79b0 <gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)>, weak_ptr=..., args=...) at ../../base/bind_internal.h:732
#38 0x00007f9619cb58d3 in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) (functor=
    @0x7f95a0026000: (void (gpu::GpuChannel::*)(gpu::GpuChannel * const, mojo::StructPtr<gpu::mojom::DeferredRequestParams>)) 0x7f9619ca79b0 <gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>)>, bound=...) at ../../base/bind_internal.h:785
#39 0x00007f9619cb585c in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams> >, void ()>::RunOnce(base::internal::BindStateBase*) (base=0x7f95a0025fe0) at ../../base/bind_internal.h:754
#40 0x00007f964ce8aec1 in base::OnceCallback<void ()>::Run() && (this=0x7ffd3a52d200) at ../../base/callback.h:142
#41 0x00007f964ce87e5b in gpu::Scheduler::RunNextTask() (this=0x55ca16cf8db0) at ../../gpu/command_buffer/service/scheduler.cc:685
#42 0x00007f964cea05ea in base::internal::FunctorTraits<void (gpu::Scheduler::*)(), void>::Invoke<void (gpu::Scheduler::*)(), gpu::Scheduler*>(void (gpu::Scheduler::*)(), gpu::Scheduler*&&)
    (method=(void (gpu::Scheduler::*)(gpu::Scheduler * const)) 0x7f964ce872b0 <gpu::Scheduler::RunNextTask()>, receiver_ptr=@0x7ffd3a52d430: 0x55ca16cf8db0) at ../../base/bind_internal.h:548
#43 0x00007f964cea0531 in base::internal::InvokeHelper<false, void>::MakeItSo<void (gpu::Scheduler::*)(), gpu::Scheduler*>(void (gpu::Scheduler::*&&)(), gpu::Scheduler*&&)
    (functor=@0x55ca16ba13f0: (void (gpu::Scheduler::*)(gpu::Scheduler * const)) 0x7f964ce872b0 <gpu::Scheduler::RunNextTask()>, args=@0x7ffd3a52d430: 0x55ca16cf8db0) at ../../base/bind_internal.h:712
#44 0x00007f964cea04b7 in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler> >, void ()>::RunImpl<void (gpu::Scheduler::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler> >, 0ul>(void (gpu::Scheduler::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::Scheduler> >&&, std::__Cr::integer_sequence<unsigned long, 0ul>) (functor=@0x55ca16ba13f0: (void (gpu::Scheduler::*)(gpu::Scheduler * const)) 0x7f964ce872b0 <gpu::Scheduler::RunNextTask()>, bound=...) at ../../base/bind_internal.h:785
#45 0x00007f964cea045c in base::internal::Invoker<base::internal::BindState<void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler> >, void ()>::RunOnce(base::internal::BindStateBase*)
    (base=0x55ca16ba13d0) at ../../base/bind_internal.h:754
#46 0x00007f965a68f621 in base::OnceCallback<void ()>::Run() && (this=0x55ca16ccec40) at ../../base/callback.h:142
#47 0x00007f965a8742d6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) (this=0x55ca15f687c0, pending_task=...) at ../../base/task/common/task_annotator.cc:135
#48 0x00007f965a8becb0 in base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)::$_0&&) (this=0x55ca15f687c0, event_name=..., pending_task=..., args=...)
    at ../../base/task/common/task_annotator.h:73
#49 0x00007f965a8bea72 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) (this=0x55ca15f68600, continuation_lazy_now=0x7ffd3a52d810)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356
#50 0x00007f965a8be231 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() (this=0x55ca15f68600)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261
#51 0x00007f965a8bec30 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ()
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:389
#52 0x00007f965a756b71 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) (this=0x55ca15f20ab0, delegate=0x55ca15f68608) at ../../base/message_loop/message_pump_glib.cc:405
#53 0x00007f965a8bf1ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) (this=0x55ca15f68600, application_tasks_allowed=true, timeout=...)
    at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468
#54 0x00007f965a805437 in base::RunLoop::Run(base::Location const&) (this=0x7ffd3a52db88, location=...) at ../../base/run_loop.cc:140
#55 0x00007f964fe13a89 in content::GpuMain(content::MainFunctionParams) (parameters=...) at ../../content/gpu/gpu_main.cc:401
#56 0x00007f9653728bb9 in content::RunZygote(content::ContentMainDelegate*) (delegate=0x7ffd3a52e748) at ../../content/app/content_main_runner_impl.cc:615
#57 0x00007f9653729425 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) (process_type=..., main_function_params=..., delegate=0x7ffd3a52e748) at ../../content/app/content_main_runner_impl.cc:687
#58 0x00007f965372a5c7 in content::ContentMainRunnerImpl::Run() (this=0x55ca15ec2ef0) at ../../content/app/content_main_runner_impl.cc:1028
#59 0x00007f9653726f68 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) (params=..., content_main_runner=0x55ca15ec2ef0) at ../../content/app/content_main.cc:398
#60 0x00007f96537278ca in content::ContentMain(content::ContentMainParams) (params=...) at ../../content/app/content_main.cc:426
#61 0x000055ca0bea1f6a in ChromeMain(int, char const**) (argc=8, argv=0x7ffd3a52e8f8) at ../../chrome/app/chrome_main.cc:172
#62 0x000055ca0bea1d92 in main(int, char const**) (argc=8, argv=0x7ffd3a52e8f8) at ../../chrome/app/chrome_exe_main_aura.cc:17

### mp...@chromium.org (2021-11-20)

For now, marking as Security_Severity-High.

[Monorail components: Internals>GPU>ANGLE Internals>GPU>Internals Internals>GPU>SwiftShader]

### [Deleted User] (2021-11-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-20)

ClusterFuzz testcase 5716021287387136 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2021-11-20)

Detailed Report: https://clusterfuzz.com/testcase?key=5716021287387136

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000014
Crash State:
  sw::SpirvShader::SpirvShader
  vkCreateGraphicsPipelines
  rx::vk::GraphicsPipelineDesc::initializePipeline
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=943773

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5716021287387136

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5716021287387136 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### [Deleted User] (2021-11-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@chromium.org (2021-11-24)

Created end2end test:
https://chromium-review.googlesource.com/c/angle/angle/+/3301019
which throws VUID-VkFramebufferCreateInfo-pAttachments-00881 errors.

Sending to syoussefi@ for further investigation.

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1047af3816a5a8363efac358e013baa55db1a46e

commit 1047af3816a5a8363efac358e013baa55db1a46e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Dec 02 19:30:42 2021

Fix changing attached renderbuffer from MSRTT to non-MSRTT

FramebufferAttachment::mRenderToTextureSamples was never updated if the
renderbuffer storage was changed after attaching to framebuffer.

Bug: chromium:1272068
Change-Id: Ib0cfde53c3453c0df4b0aea32ab0a246aa2ade7f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313414
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/1047af3816a5a8363efac358e013baa55db1a46e/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/1047af3816a5a8363efac358e013baa55db1a46e/src/libANGLE/FramebufferAttachment.cpp
[modify] https://crrev.com/1047af3816a5a8363efac358e013baa55db1a46e/src/libANGLE/FramebufferAttachment.h


### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9df08d0fb9551aa2f175ab7f7741228a5279d70d

commit 9df08d0fb9551aa2f175ab7f7741228a5279d70d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Dec 03 22:43:32 2021

Roll ANGLE from c88a73c8b84f to 9408adceaeb9 (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/c88a73c8b84f..9408adceaeb9

2021-12-03 bsheedy@chromium.org Add Gold git main method
2021-12-03 cnorthrop@google.com Vulkan: Allow nonconformant EXT_gpu_shader5
2021-12-03 syoussefi@chromium.org Fix changing attached renderbuffer from MSRTT to non-MSRTT

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1272068,chromium:1276531
Tbr: ynovikov@google.com
Test: Test: ES 3.2 traces on SwiftShader (Asphalt 9, Fortnite, etc)
Change-Id: I029bf4148df4ca761951e35bda3ac8715b1df7de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3315432
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#948202}

[modify] https://crrev.com/9df08d0fb9551aa2f175ab7f7741228a5279d70d/DEPS


### [Deleted User] (2021-12-04)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-05)

Requesting merge to stable M96 because latest trunk commit (948202) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (948202) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-05)

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

### [Deleted User] (2021-12-05)

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

### sy...@chromium.org (2021-12-06)

1. Security bug
2. https://chromium-review.googlesource.com/c/angle/angle/+/3313414
3. For three days so far
4. No
5. N/A
6. N/A

### am...@chromium.org (2021-12-06)

merge approved for M97; please merge to branch 4692 by NLT 12pm PST tomorrow (Tuesday, 7 December) so this fix can be included in the m97 cut 

merge approved for M96, please merge to branch 4664 at your earliest convenience 

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations, Aki on another one! The VRP Panel has decided to award you $5,000 for this report. Thank you for this report and great work! 

### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/6b4be8ad99e9f9234cbb1a709798ade2fecd8b66

commit 6b4be8ad99e9f9234cbb1a709798ade2fecd8b66
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Dec 02 19:30:42 2021

M97: Fix changing attached renderbuffer from MSRTT to non-MSRTT

FramebufferAttachment::mRenderToTextureSamples was never updated if the
renderbuffer storage was changed after attaching to framebuffer.

Bug: chromium:1272068
Change-Id: I1a42314854f525dc85c297839665efd1531d38a1
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3320924
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/6b4be8ad99e9f9234cbb1a709798ade2fecd8b66/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/6b4be8ad99e9f9234cbb1a709798ade2fecd8b66/src/libANGLE/FramebufferAttachment.cpp
[modify] https://crrev.com/6b4be8ad99e9f9234cbb1a709798ade2fecd8b66/src/libANGLE/FramebufferAttachment.h


### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/bdffa0ea51488f8ffde80095934454e5a6476a1f

commit bdffa0ea51488f8ffde80095934454e5a6476a1f
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Thu Dec 02 19:30:42 2021

M96: Fix changing attached renderbuffer from MSRTT to non-MSRTT

FramebufferAttachment::mRenderToTextureSamples was never updated if the
renderbuffer storage was changed after attaching to framebuffer.

Bug: chromium:1272068
Change-Id: Icddbb5650354ea16d06c49532d6a8d0ae962ab5f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3320923
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/bdffa0ea51488f8ffde80095934454e5a6476a1f/src/tests/gl_tests/FramebufferTest.cpp
[modify] https://crrev.com/bdffa0ea51488f8ffde80095934454e5a6476a1f/src/libANGLE/FramebufferAttachment.cpp
[modify] https://crrev.com/bdffa0ea51488f8ffde80095934454e5a6476a1f/src/libANGLE/FramebufferAttachment.h


### sy...@chromium.org (2021-12-07)

Done

### ad...@google.com (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-10)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-06)

^^ info was already sent to finance for payment processing on 7 December, automation borked and did not update here accordingly and was discovered and fixed today

### [Deleted User] (2022-03-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1272068?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU>ANGLE, Internals>GPU>Internals, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057972)*
