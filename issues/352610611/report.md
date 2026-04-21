# UAF in dawn::wire::client::Device::HandleError

| Field | Value |
|-------|-------|
| **Issue ID** | [352610611](https://issues.chromium.org/issues/352610611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn, Dawn>Wire |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2024-07-12 |
| **Bounty** | $8,000.00 |

## Description

UAF in dawn::wire::client::Device::HandleError
tested OS:ubuntu 22.04
tested chrome:
Chromium 128.0.6591.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1326524.zip)
Chromium 128.0.6585.0

- Repro steps (on the real Machine)
./chrome --user-data-dir=/tmp/xx1 --enable-unsafe-webgpu --incognito http://localhost:8880/crash.html

Wait a few seconds to reproduce the UAF (Use-After-Free).

- Bisect:
This issue started reproducing from this change:
https://chromium-review.googlesource.com/c/chromium/src/+/5661562

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x5020001bf0f0 at pc 0x638b4e0a768c bp 0x7fff2d504250 sp 0x7fff2d504248
READ of size 8 at 0x5020001bf0f0 thread T0 (chrome)
    #0 0x638b4e0a768b in operator bool ./../../base/memory/scoped_refptr.h:311:43
    #1 0x638b4e0a768b in is_null ./../../base/functional/callback_internal.h:140:34
    #2 0x638b4e0a768b in base::RepeatingCallback<void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, char const*)>::Run(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, char const*) const & ./../../base/functional/callback.h:336:5
    #3 0x638b4e0a77aa in operator() ./gen/third_party/dawn/include/dawn/wire/client/webgpu_cpp.h:7342:9
    #4 0x638b4e0a77aa in void wgpu::dawn::wire::client::DeviceDescriptor::SetUncapturedErrorCallback<void (*)(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, char const*, void*), void*, void (wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, char const*, void*), void>(void (*)(wgpu::dawn::wire::client::Device const&, wgpu::ErrorType, char const*, void*), void*)::'lambda'(WGPUDeviceImpl* const*, WGPUErrorType, char const*, void*, void*)::__invoke(WGPUDeviceImpl* const*, WGPUErrorType, char const*, void*, void*) ./gen/third_party/dawn/include/dawn/wire/client/webgpu_cpp.h:7338:45
    #5 0x638b42de3135 in dawn::wire::client::Device::HandleError(WGPUErrorType, char const*) ./../../third_party/dawn/src/dawn/wire/client/Device.cpp:356:9
    #6 0x638b42de1e59 in dawn::wire::client::Client::DoDeviceUncapturedErrorCallback(dawn::wire::client::Device*, WGPUErrorType, char const*) ./../../third_party/dawn/src/dawn/wire/client/ClientDoers.cpp:54:13
    #7 0x638b42de1cb3 in HandleDeviceUncapturedErrorCallback ./gen/third_party/dawn/src/dawn/wire/client/ClientHandlers_autogen.cpp:72:16
    #8 0x638b42de1cb3 in dawn::wire::client::Client::HandleCommandsImpl(char const volatile*, unsigned long) ./gen/third_party/dawn/src/dawn/wire/client/ClientHandlers_autogen.cpp:137:30
    #9 0x638b3385bb0a in gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../gpu/command_buffer/client/webgpu_implementation.cc:320:7
    #10 0x638b29ed750d in gpu::mojom::CommandBufferClientStubDispatch::Accept(gpu::mojom::CommandBufferClient*, mojo::Message*) ./gen/gpu/ipc/common/gpu_channel.mojom.cc:6450:13
    #11 0x638b3bf000f7 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1036:54
    #12 0x638b3bf1c22a in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #13 0x638b3bf05105 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20
    #14 0x638b3cd3daee in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1216:24
    #15 0x638b3cd3f943 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:738:12
    #16 0x638b3cd3f943 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:930:12
    #17 0x638b3cd3f943 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1067:14
    #18 0x638b3cd3f943 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:980:12
    #19 0x638b3a71eb44 in Run ./../../base/functional/callback.h:156:12
    #20 0x638b3a71eb44 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #21 0x638b3a785f36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #22 0x638b3a785f36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #23 0x638b3a784e50 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x638b3a786c7a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #25 0x638b3a6064bd in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #26 0x638b3a7878e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #27 0x638b3a6a540f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #28 0x638b521fcfa8 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:359:16
    #29 0x638b37aa57d6 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:703:14
    #30 0x638b37aa6eba in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:807:12
    #31 0x638b37aa9991 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1175:10
    #32 0x638b37aa3970 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:333:36
    #33 0x638b37aa3ffb in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:346:10
    #34 0x638b270f948b in ChromeMain ./../../chrome/app/chrome_main.cc:228:12
    #35 0x7913afc29d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x5020001bf0f0 is located 0 bytes inside of 8-byte region [0x5020001bf0f0,0x5020001bf0f8)
freed by thread T0 (chrome) here:
    #0 0x638b270f74ad in operator delete(void*) _asan_rtl_:3
    #1 0x638b2edf1b79 in operator() ./../../v8/src/heap/cppgc/sweeper.cc:500:15
    #2 0x638b2edf1b79 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizePage(cppgc::internal::(anonymous namespace)::SweepingState::SweptPageState*) ./../../v8/src/heap/cppgc/sweeper.cc:514:7
    #3 0x638b2edf3de2 in cppgc::internal::(anonymous namespace)::SweepFinalizer::FinalizeWithDeadlineAndSize(cppgc::internal::(anonymous namespace)::SweepingState&, v8::base::TimeTicks, unsigned long) ./../../v8/src/heap/cppgc/sweeper.cc:459:7
    #4 0x638b2ede38bb in cppgc::internal::Sweeper::SweeperImpl::SweepForAllocationIfRunning(cppgc::internal::NormalPageSpace*, unsigned long, v8::base::TimeDelta) ./../../v8/src/heap/cppgc/sweeper.cc:1079:19
    #5 0x638b2edcebc9 in cppgc::internal::ObjectAllocator::TryRefillLinearAllocationBuffer(cppgc::internal::NormalPageSpace&, unsigned long) ./../../v8/src/heap/cppgc/object-allocator.cc:235:15
    #6 0x638b2edcdb77 in cppgc::internal::ObjectAllocator::OutOfLineAllocateImpl(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:182:8
    #7 0x638b2edcd656 in cppgc::internal::ObjectAllocator::OutOfLineAllocateGCSafePoint(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short, void**) ./../../v8/src/heap/cppgc/object-allocator.cc:121:13
    #8 0x638b2ed9be2c in OutOfLineAllocate ./../../v8/src/heap/cppgc/object-allocator.h:183:3
    #9 0x638b2ed9be2c in AllocateObjectOnSpace ./../../v8/src/heap/cppgc/object-allocator.h:242:12
    #10 0x638b2ed9be2c in AllocateObject ./../../v8/src/heap/cppgc/object-allocator.h:121:10
    #11 0x638b2ed9be2c in cppgc::internal::MakeGarbageCollectedTraitInternal::Allocate(cppgc::AllocationHandle&, unsigned long, unsigned short) ./../../v8/src/heap/cppgc/allocation.cc:38:48
    #12 0x638b4a21bfbe in Invoke ./../../v8/include/cppgc/allocation.h:94:14
    #13 0x638b4a21bfbe in Allocate ./../../v8/include/cppgc/allocation.h:179:12
    #14 0x638b4a21bfbe in Call<> ./../../v8/include/cppgc/allocation.h:240:9
    #15 0x638b4a21bfbe in MakeGarbageCollected<blink::HeapVector<cppgc::internal::BasicMember<const blink::DisplayItemClient, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0U> > ./../../v8/include/cppgc/allocation.h:279:7
    #16 0x638b4a21bfbe in MakeGarbageCollected<blink::HeapVector<cppgc::internal::BasicMember<const blink::DisplayItemClient, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0U> > ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #17 0x638b4a21bfbe in blink::PaintController::StartCycle(bool) ./../../third_party/blink/renderer/platform/graphics/paint/paint_controller.cc:810:7
    #18 0x638b47965df0 in blink::LocalFrameView::RunPaintLifecyclePhase(blink::PaintBenchmarkMode) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2643:31
    #19 0x638b47963dba in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2362:3
    #20 0x638b47960f70 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2166:3
    #21 0x638b479606dd in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1902:54
    #22 0x638b49219b8d in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/page/page_animator.cc:397:9
    #23 0x638b47aab9db in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1587:14
    #24 0x638b4a42ca95 in UpdateVisualState ./../../third_party/blink/renderer/platform/widget/widget_base.cc:1025:12
    #25 0x638b4a42ca95 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() ./../../third_party/blink/renderer/platform/widget/widget_base.cc:0:0
    #26 0x638b3f6c0d9c in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer_tree_host.cc:379:12
    #27 0x638b3f996c72 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) ./../../cc/trees/proxy_main.cc:284:21
    #28 0x638b3f9bd5b9 in Invoke<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), const base::WeakPtr<cc::ProxyMain> &, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > ./../../base/functional/bind_internal.h:738:12
    #29 0x638b3f9bd5b9 in MakeItSo<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > > ./../../base/functional/bind_internal.h:954:5
    #30 0x638b3f9bd5b9 in void base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>&&, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>&&>, base::internal::BindState<true, true, false, void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunImpl<void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, 0ul, 1ul>(void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind_internal.h:1067:14
    #31 0x638b3a71eb44 in Run ./../../base/functional/callback.h:156:12
    #32 0x638b3a71eb44 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #33 0x638b3a785f36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #34 0x638b3a785f36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #35 0x638b3a784e50 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #36 0x638b3a786c7a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #37 0x638b3a6064bd in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #38 0x638b3a7878e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #39 0x638b3a6a540f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #40 0x638b521fcfa8 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:359:16
    #41 0x638b37aa57d6 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:703:14
    #42 0x638b37aa6eba in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:807:12
    #43 0x638b37aa9991 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1175:10

previously allocated by thread T0 (chrome) here:
    #0 0x638b270f6c4d in operator new(unsigned long) _asan_rtl_:3
    #1 0x638b4e0e11a0 in MakeWGPURepeatingCallback<base::RepeatingCallback<void (const wgpu::dawn::wire::client::Device &, wgpu::ErrorType, const char *)> > ./../../gpu/webgpu/callback.h:141:10
    #2 0x638b4e0e11a0 in blink::GPUDeviceProxy::GPUDeviceProxy() ./../../third_party/blink/renderer/modules/webgpu/gpu_device.cc:787:34
    #3 0x638b4e09f9c5 in Call<> ./../../v8/include/cppgc/allocation.h:241:32
    #4 0x638b4e09f9c5 in MakeGarbageCollected<blink::GPUDeviceProxy> ./../../v8/include/cppgc/allocation.h:279:7
    #5 0x638b4e09f9c5 in MakeGarbageCollected<blink::GPUDeviceProxy> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:37:10
    #6 0x638b4e09f9c5 in blink::GPUAdapter::requestDevice(blink::ScriptState*, blink::GPUDeviceDescriptor*) ./../../third_party/blink/renderer/modules/webgpu/gpu_adapter.cc:312:24
    #7 0x638b4c4ecb97 in blink::(anonymous namespace)::v8_gpu_adapter::RequestDeviceOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_gpu_adapter.cc:233:39
    #8 0x638b307b5b2d in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
    #9 0x638b307b38a6 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:0:0
    #10 0x638b307f40f5 in Builtins_AsyncFunctionAwaitResolveClosure setup-isolate-deserialize.cc:0:0
    #11 0x638b308d0e6d in Builtins_PromiseFulfillReactionJob setup-isolate-deserialize.cc:0:0
    #12 0x638b307e32ba in Builtins_RunMicrotasks setup-isolate-deserialize.cc:0:0
    #13 0x638b307b125e in Builtins_JSRunMicrotasksEntry setup-isolate-deserialize.cc:0:0
    #14 0x638b2ccb7faf in Call ./../../v8/src/execution/simulator.h:187:12
    #15 0x638b2ccb7faf in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:435:41
    #16 0x638b2ccbb76d in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:477:18
    #17 0x638b2ccbbba6 in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) ./../../v8/src/execution/execution.cc:578:10
    #18 0x638b2cd5470c in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) ./../../v8/src/execution/microtask-queue.cc:185:22
    #19 0x638b2cd5631d in PerformCheckpointInternal ./../../v8/src/execution/microtask-queue.cc:129:3
    #20 0x638b2cd5631d in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) ./../../v8/src/execution/microtask-queue.h:48:5
    #21 0x638b36b2d110 in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() ./../../third_party/blink/renderer/platform/scheduler/common/event_loop.cc:79:21
    #22 0x638b36b62646 in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() ./../../third_party/blink/renderer/platform/scheduler/main_thread/agent_group_scheduler_impl.cc:117:12
    #23 0x638b36ba8d7a in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:1137:28
    #24 0x638b36bbec03 in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2284:3
    #25 0x638b36be1226 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) ./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:174:29
    #26 0x638b36be494e in Invoke<void (blink::scheduler::MainThreadTaskQueue::*)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *), blink::scheduler::MainThreadTaskQueue *, const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *> ./../../base/functional/bind_internal.h:738:12
    #27 0x638b36be494e in MakeItSo<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *> ./../../base/functional/bind_internal.h:930:12
    #28 0x638b36be494e in RunImpl<void (blink::scheduler::MainThreadTaskQueue::*const &)(const base::sequence_manager::Task &, base::sequence_manager::TaskQueue::TaskTiming *, base::LazyNow *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #29 0x638b36be494e in base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) ./../../base/functional/bind_internal.h:987:12
    #30 0x638b3a762b3d in base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & ./../../base/functional/callback.h:344:12
    #31 0x638b3a736e6d in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) ./../../base/task/sequence_manager/sequence_manager_impl.cc:910:35
    #32 0x638b3a736a4f in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) ./../../base/task/sequence_manager/sequence_manager_impl.cc:679:3
    #33 0x638b3a7861da in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:500:37
    #34 0x638b3a784e50 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #35 0x638b3a786c7a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #36 0x638b3a6064bd in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #37 0x638b3a7878e6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #38 0x638b3a6a540f in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14

SUMMARY: AddressSanitizer: heap-use-after-free (/home/pwn11/asan-linux-release/chrome+0x3626768b) (BuildId: e9c18dc7a7b058e2)
Shadow bytes around the buggy address:
  0x5020001bee00: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x5020001bee80: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x5020001bef00: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fd
  0x5020001bef80: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x5020001bf000: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fa
=>0x5020001bf080: f7 fa fd fd f7 fa 00 00 f7 fa 00 fa f7 fa[fd]fa
  0x5020001bf100: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x5020001bf180: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x5020001bf200: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd
  0x5020001bf280: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x5020001bf300: f7 fa fd fd f7 fa fd fa f7 fa fd fd f7 fa fd fd
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

==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x638b3cd2eef2 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1155:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=1722934 --enable-crash-reporter=, --user-data-dir=/tmp/xx1 --origin-trial-disabled-features=ElementCapture --no-subproc-heap-profiling --change-stack-guard-on-fork=enable --enable-unsafe-webgpu --file-url-path-alias=/gen=/home/pwn11/asan-linux-release/gen --disable-databases --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1720580726603173 --launch-time-ticks=178280437694 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,3904436244842492458,12268896500720107563,2097152 --field-trial-handle=3,i,9155494884536509254,15642038043340019442,262144 --variations-seed-version`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.






## Attachments

- [crash.html](attachments/crash.html) (text/html, 837 B)
- [asan.log](attachments/asan.log) (text/plain, 46.7 KB)
- [launcher.sh](attachments/launcher.sh) (text/x-sh, 502 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5736668986277888.

### ja...@chromium.org (2024-07-15)

I'm working on reproducing this. I was unable to reproduce with 126.0.6478.126 (Official Build) (64-bit) on Linux. I'm downloading the ASAN build to try with that like the bug reporter's instructions say.

### ja...@chromium.org (2024-07-15)

Adding components Dawn and Dawn>Wire pre-emptively.

### ja...@chromium.org (2024-07-15)

Retrying clusterfuzz using `--enable-unsafe-webgpu`

### cl...@appspot.gserviceaccount.com (2024-07-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6113431604101120.

### ja...@chromium.org (2024-07-15)

I also tried using 128.0.6585.0 (Developer Build) custom (64-bit) on Linux but I haven't been able to reproduce it. I'm going to guess that I'm doing something trivial incorrectly. I'll pass it to lokokung@ who authored [crrev.com/5661562](https://crrev.com/5661562) to take a look.

### ja...@chromium.org (2024-07-15)

Hi lokokung, could you please take a look at this issue? I wasn't able to reproduce it but it looks legitimate.

### ja...@chromium.org (2024-07-15)

Applying S1 [high] as it looks like use after free without miracle pointer protection (from the asan stack trace).

### ja...@chromium.org (2024-07-15)

Putting found-in as 128 since [crrev.com/5661562](https://crrev.com/5661562) is only in 128 so far.

### em...@gmail.com (2024-07-16)

Do you use a real PC? It should be quickly reproducible on a real device. I'm not sure if CF can reproduce the webgpu-dawn issue.

If it can't be reproduced on a real device, you can try the attached script and open multiple browsers at the same time.

Usage:：
./launcher.sh ~/asan-linux-release/chrome http://localhost:8880/crash.html 5 2>&1|grep -E 'heap-use'

tested version:
gs://chromium-browser-asan/linux-release/asan-linux-release-1327907.zip

### pe...@google.com (2024-07-16)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-07-16)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-07-19)

Project: chromium/src
Branch: main

commit 9d06182051758c3bc96e0b1bee050dfe95b7a90e
Author: Loko Kung <lokokung@google.com>
Date:   Fri Jul 19 00:42:06 2024

    Revert "[dawn] Use new device lost and uncaptured error callback types in Blink"
    
    This reverts commit b779ad49ce7582fcbddef3ccc2fe01f9278d5e31.
    
    Reason for revert: Could be causing UAF in crbug.com/352610611
    
    Bug: 352610611
    
    Original change's description:
    > [dawn] Use new device lost and uncaptured error callback types in Blink
    >
    > Bug: 42241461, 42241415
    > Change-Id: I891d6d7dec15624b4b46b7bb707b913b188a14c3
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5661562
    > Reviewed-by: Austin Eng <enga@chromium.org>
    > Commit-Queue: Loko Kung <lokokung@google.com>
    > Cr-Commit-Position: refs/heads/main@{#1320780}
    
    Bug: 42241461, 42241415
    Change-Id: I10595ae45e027d026272d3bbc2a6ce4ccc1652d5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5723289
    Commit-Queue: Loko Kung <lokokung@google.com>
    Auto-Submit: Loko Kung <lokokung@google.com>
    Reviewed-by: Austin Eng <enga@chromium.org>
    Commit-Queue: Austin Eng <enga@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1329916}

M       third_party/blink/renderer/modules/webgpu/gpu_adapter.cc
M       third_party/blink/renderer/modules/webgpu/gpu_adapter.h
M       third_party/blink/renderer/modules/webgpu/gpu_device.cc
M       third_party/blink/renderer/modules/webgpu/gpu_device.h

https://chromium-review.googlesource.com/5723289


### lo...@google.com (2024-07-23)

Offending change has been rolled back so the UAF should be gone now. Closing.

### pe...@google.com (2024-07-24)

Not requesting merge to dev (M128) because latest trunk commit (1320780) appears to be prior to dev branch point (1331488). If this is incorrect please remove NA-128 from the 'Merge' field and add 128 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us -- nice work!

### pe...@google.com (2024-10-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352610611)*
