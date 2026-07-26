# Heap UAF in Blink OffscreenCanvas

| Field | Value |
|-------|-------|
| **Issue ID** | [494352590](https://issues.chromium.org/issues/494352590) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | jp...@chromium.org |
| **Created** | 2026-03-20 |
| **Bounty** | $7,000.00 |

## Description

## VULNERABILITY DETAILS

A heap-use-after-free vulnerability exists in Chromium's Blink engine, specifically within the `OffscreenCanvas` component (`core` and `modules`). The crash triggers at `mojo::Handle::is_valid()` via `blink::CanvasResourceDispatcher::OnBeginFrame`.

```
=================================================================
==2029962==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c80e0d45ef0 at pc 0x7f3104ff0f42 bp 0x7ffec54ac8a0 sp 0x7ffec54ac898
READ of size 8 at 0x7c80e0d45ef0 thread T0 (chrome)
    #0 0x7f3104ff0f41 in std::__Cr::unique_ptr<viz::mojom::blink::CompositorFrameSinkProxy, std::__Cr::default_delete<viz::mojom::blink::CompositorFrameSinkProxy>>::operator bool() const gen/third_party/libc++/src/include/__memory/unique_ptr.h:275:12
    #1 0x7f3104ff0f41 in mojo::internal::InterfacePtrState<viz::mojom::blink::CompositorFrameSink>::ConfigureProxyIfNecessary() mojo/public/cpp/bindings/lib/interface_ptr_state.h:261:9
    #2 0x7f310501bc44 in mojo::internal::InterfacePtrState<viz::mojom::blink::CompositorFrameSink>::instance() mojo/public/cpp/bindings/lib/interface_ptr_state.h:145:5
    #3 0x7f310501bc44 in mojo::Remote<viz::mojom::blink::CompositorFrameSink>::get() const mojo/public/cpp/bindings/remote.h:100:28
    #4 0x7f310501bc44 in mojo::Remote<viz::mojom::blink::CompositorFrameSink>::operator->() const mojo/public/cpp/bindings/remote.h:104:59
    #5 0x7f310501bc44 in blink::CanvasResourceDispatcher::OnBeginFrame(viz::BeginFrameArgs const&, blink::HashMap<unsigned int, viz::FrameTimingDetails, blink::HashTraits<unsigned int>, blink::HashTraits<viz::FrameTimingDetails>, blink::PartitionAllocator> const&, blink::Vector<viz::ReturnedResource, 0u, blink::PartitionAllocator>) third_party/blink/renderer/platform/graphics/canvas_resource_dispatcher.cc:416:5
    #6 0x7f310730b8d1 in viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept(viz::mojom::blink::CompositorFrameSinkClient*, mojo::Message*) gen/services/viz/public/mojom/compositing/compositor_frame_sink.mojom-blink.cc:1677:13
    #7 0x7f315fd743e2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x7f315fd8b78b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #9 0x7f315fd79c94 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x7f315fd9ad6e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #11 0x7f315fd9959d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #12 0x7f315fd8b78b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #13 0x7f315fd6002f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #14 0x7f315fd6187e in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #15 0x7f315fd627a4 in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>&&>::Invoke<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&>(void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&) base/functional/bind_internal.h:740:12
    #16 0x7f315fd627a4 in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, void, 0ul>::MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&) base/functional/bind_internal.h:956:5
    #17 0x7f315fd627a4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1069:14
    #18 0x7f315fd627a4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #19 0x7f315f5cbed2 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #20 0x7f315f5cbed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #21 0x7f315f64d3ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:112:5
    #22 0x7f315f64d3ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #23 0x7f315f64c3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x7f315f46dea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #25 0x7f315f64ea48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #26 0x7f315f536512 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #27 0x7f3155215bfe in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #28 0x7f31556480b7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #29 0x7f315564921f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #30 0x7f315564b80a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #31 0x7f3155645f53 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #32 0x7f31556462ea in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #33 0x556bdcd8f345 in ChromeMain chrome/app/chrome_main.cc:191:12
    #34 0x7f30ef8e7d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7c80e0d45ef0 is located 112 bytes inside of 472-byte region [0x7c80e0d45e80,0x7c80e0d46058)
freed by thread T0 (chrome) here:
    #0 0x556bdcd8e502 in operator delete(void*, unsigned long) (/mnt/lvm_data/chromium/src/out/asan_nodcheck/chrome+0x686f502) (BuildId: f667536c8ff65a4b)
    #1 0x7f30f6fc3e03 in blink::OffscreenCanvasRenderingContext2D::LoseContext(blink::CanvasRenderingContext::LostContextMode) third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc:445:11
    #2 0x7f30f6fc2e9b in blink::OffscreenCanvasRenderingContext2D::GetOrCreateResourceProvider() third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc:197:5
    #3 0x7f30f6fc2a03 in blink::OffscreenCanvasRenderingContext2D::FinalizeFrame(blink::FlushReason) third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc:136:8
    #4 0x7f30f6fc4d46 in blink::OffscreenCanvasRenderingContext2D::PushFrame() third_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen_canvas_rendering_context_2d.cc:322:3
    #5 0x7f310501bc36 in blink::CanvasResourceDispatcher::OnBeginFrame(viz::BeginFrameArgs const&, blink::HashMap<unsigned int, viz::FrameTimingDetails, blink::HashTraits<unsigned int>, blink::HashTraits<viz::FrameTimingDetails>, blink::PartitionAllocator> const&, blink::Vector<viz::ReturnedResource, 0u, blink::PartitionAllocator>) third_party/blink/renderer/platform/graphics/canvas_resource_dispatcher.cc:413:54
    #6 0x7f310730b8d1 in viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept(viz::mojom::blink::CompositorFrameSinkClient*, mojo::Message*) gen/services/viz/public/mojom/compositing/compositor_frame_sink.mojom-blink.cc:1677:13
    #7 0x7f315fd743e2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x7f315fd8b78b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #9 0x7f315fd79c94 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x7f315fd9ad6e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #11 0x7f315fd9959d in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #12 0x7f315fd8b78b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #13 0x7f315fd6002f in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #14 0x7f315fd6187e in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #15 0x7f315fd627a4 in void base::internal::DecayedFunctorTraits<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>&&>::Invoke<void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&>(void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> const&) base/functional/bind_internal.h:740:12
    #16 0x7f315fd627a4 in void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, void, 0ul>::MakeItSo<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&) base/functional/bind_internal.h:956:5
    #17 0x7f315fd627a4 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunImpl<void (mojo::Connector::*)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>, 0ul>(void (mojo::Connector::*&&)(), std::__Cr::tuple<base::WeakPtr<mojo::Connector>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1069:14
    #18 0x7f315fd627a4 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #19 0x7f315f5cbed2 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #20 0x7f315f5cbed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #21 0x7f315f64d3ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:112:5
    #22 0x7f315f64d3ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #23 0x7f315f64c3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #24 0x7f315f46dea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #25 0x7f315f64ea48 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #26 0x7f315f536512 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #27 0x7f3155215bfe in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #28 0x7f31556480b7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #29 0x7f315564921f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #30 0x7f315564b80a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #31 0x7f3155645f53 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #32 0x7f31556462ea in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #33 0x556bdcd8f345 in ChromeMain chrome/app/chrome_main.cc:191:12
    #34 0x7f30ef8e7d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

previously allocated by thread T0 (chrome) here:
    #0 0x556bdcd8d8fd in operator new(unsigned long) (/mnt/lvm_data/chromium/src/out/asan_nodcheck/chrome+0x686e8fd) (BuildId: f667536c8ff65a4b)
    #1 0x7f310f6f0ce2 in std::__Cr::unique_ptr<blink::CanvasResourceDispatcher, std::__Cr::default_delete<blink::CanvasResourceDispatcher>> std::__Cr::make_unique<blink::CanvasResourceDispatcher, blink::OffscreenCanvas*, scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<base::SingleThreadTaskRunner>, unsigned int&, unsigned int&, int&, gfx::Size, 0>(blink::OffscreenCanvas*&&, scoped_refptr<base::SingleThreadTaskRunner>&&, scoped_refptr<base::SingleThreadTaskRunner>&&, unsigned int&, unsigned int&, int&, gfx::Size&&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x7f310f6f0ce2 in blink::OffscreenCanvas::GetOrCreateResourceDispatcher() third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc:466:25
    #3 0x7f310f6f14a4 in blink::OffscreenCanvas::DidDraw(SkIRect const&) third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc:484:7
    #4 0x7f310f6f14a4 in non-virtual thunk to blink::OffscreenCanvas::DidDraw(SkIRect const&) third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc
    #5 0x7f310dfb28e3 in blink::CanvasRenderingContext::DidDraw(SkIRect const&, blink::CanvasPerformanceMonitor::DrawType) third_party/blink/renderer/core/html/canvas/canvas_rendering_context.cc:314:9
    #6 0x7f310f6eccf8 in blink::CanvasRenderingContext::DidDraw(blink::CanvasPerformanceMonitor::DrawType) third_party/blink/renderer/core/html/canvas/canvas_rendering_context.h:195:12
    #7 0x7f310f6eccf8 in blink::OffscreenCanvas::SetSize(gfx::Size) third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc:177:15
    #8 0x7f30f62aea08 in blink::(anonymous namespace)::v8_offscreen_canvas::WidthAttributeSetCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_offscreen_canvas.cc:96:17
    #9 0x7b30afdd06a3  (<unknown module>)
    #10 0x7b30afe2b528  (<unknown module>)
    #11 0x7b3090000843  (<unknown module>)
    #12 0x7b30afe1356d  (<unknown module>)
    #13 0x7b30aff01a29  (<unknown module>)
    #14 0x7b30afe01392  (<unknown module>)
    #15 0x7b30afdcb52a  (<unknown module>)
    #16 0x7f30fdf2748d in v8::internal::GeneratedCode<unsigned long, unsigned long, v8::internal::MicrotaskQueue*>::Call(unsigned long, v8::internal::MicrotaskQueue*) v8/src/execution/simulator.h:216:12
    #17 0x7f30fdf2748d in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:492:41
    #18 0x7f30fdf29689 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:534:18
    #19 0x7f30fdf29a8f in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) v8/src/execution/execution.cc:638:10
    #20 0x7f30fdfd21fc in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) v8/src/execution/microtask-queue.cc:185:22
    #21 0x7f30fdfd1c54 in v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) v8/src/execution/microtask-queue.cc:129:3
    #22 0x7f310c693c83 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:863:1
    #23 0x7f310c4e1b1b in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::CallInternal(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:126:12
    #24 0x7f310c4e1b1b in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0, (blink::bindings::CallbackReturnTypeIsPromise)0>::Call(int, v8::Local<v8::Value>*) third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:150:10
    #25 0x7f3110c9262b in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:73:13
    #26 0x7f3110c93a03 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::BasicHeapVector<(blink::internal::HeapCollectionType)1, blink::ScriptValue, 0u> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_function.cc:133:15
    #27 0x7f310fbc0669 in blink::ScheduledAction::Execute(blink::ExecutionContext*) third_party/blink/renderer/core/scheduler/scheduled_action.cc:145:18
    #28 0x7f310fbb8e57 in blink::DOMTimer::Fired() third_party/blink/renderer/core/scheduler/dom_timer.cc:446:11
    #29 0x7f3105590855 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:166:3
    #30 0x7f310ead069c in void base::internal::DecayedFunctorTraits<void (blink::TimerBase::*)(), blink::TimerBase*>::Invoke<void (blink::TimerBase::*)(), blink::TimerBase*>(void (blink::TimerBase::*)(), blink::TimerBase*&&) base/functional/bind_internal.h:740:12
    #31 0x7f310ead069c in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, void, 0ul>::MakeItSo<void (blink::TimerBase::*)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>>(void (blink::TimerBase::*&&)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>&&) base/functional/bind_internal.h:932:12
    #32 0x7f310ead069c in void base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunImpl<void (blink::TimerBase::*)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>, 0ul>(void (blink::TimerBase::*&&)(), std::__Cr::tuple<blink::UnretainedWrapper<blink::TimerBase>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/bind_internal.h:1069:14
    #33 0x7f310ead069c in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:982:12
    #34 0x7f315f5cbed2 in base::OnceCallback<void ()>::Run() && base/functional/callback.h:155:12
    #35 0x7f315f5cbed2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:229:34
    #36 0x7f315f64d3ce in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) base/task/common/task_annotator.h:112:5
    #37 0x7f315f64d3ce in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #38 0x7f315f64c3a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #39 0x7f315f46dea1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__memory/unique_ptr.h:275:12 in std::__Cr::unique_ptr<viz::mojom::blink::CompositorFrameSinkProxy, std::__Cr::default_delete<viz::mojom::blink::CompositorFrameSinkProxy>>::operator bool() const
Shadow bytes around the buggy address:
  0x7c80e0d45c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c80e0d45c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c80e0d45d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7c80e0d45d80: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x7c80e0d45e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x7c80e0d45e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
  0x7c80e0d45f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c80e0d45f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7c80e0d46000: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x7c80e0d46080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7c80e0d46100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==2029962==ADDITIONAL INFO

==2029962==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7f315fd62336 in mojo::Connector::PostDispatchNextMessageFromPipe() mojo/public/cpp/bindings/lib/connector.cc:589:7
    #1 0x7f315fd62336 in mojo::Connector::ScheduleDispatchOfPendingMessagesOrWaitForMore(unsigned long) mojo/public/cpp/bindings/lib/connector.cc:612:5
    #2 0x7f315e08b9ea in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=2029916 --enable-crash-reporter=, --noerrdialogs --user-data-dir=/tmp/org.chromium.Chromium.scoped_dir.8w1ili --change-stack-guard-on-fork=enable --no-sandbox --ozone-platform=headless --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1772947841576980 --launch-time-ticks=1025574931179 --shared-files=v8_context_snapshot_data:100 --field-trial-handle=3,i,7742491733228300046,8070823627392218987,262144 --disable-features=PaintHolding --variations-seed-version --pseudonymization-salt-handle=7,i,2791269340090131867,8337486435613622678,4 --trace-process-track-uuid=3190708990997080739`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2029962==END OF ADDITIONAL INFO

```
## VERSION

Chrome Version: Chromium 147.0.7703.0 and Chromium 148.0.7729.0 dev ASAN builds  

Operating System: Linux x86\_64 on the two provided repro hosts (Ubuntu 22.04.3 LTS class and Ubuntu 25.04 class)

## REPRODUCTION CASE

Primary HTML artifact: `poc_standalone.html`

Required flags (for PoC, not related to the vulnerability): `--no-first-run --no-default-browser-check --disable-background-networking`

```
chrome file:///path/to/poc_standalone.html --no-first-run --no-default-browser-check --disable-background-networking

```

Note: due to requiring race condition to reach this vulnerability, the PoC is a bit flaky and can take longer time (~1min) to crash on a slower machine. Also, please retry if it doesn't crash.

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer process crash

## CREDIT INFORMATION

Reporter credit: heapracer

## Attachments

- [poc_standalone.html](attachments/poc_standalone.html) (text/html, 8.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5183787826708480.

### 24...@project.gserviceaccount.com (2026-03-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-21)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/91a2a43f5a22baed132542a516c8ff069b47bdfb (Add a new kCanvasDisposed context loss type

When the canvas is being disposed, we can never restore the context.
This is already taken care of by setting context_restorable_ to true.
Using kSyntheticLostContext however is misleading because
BaseRenderingContext2D::DispatchContextLostEvent suggests that
kSyntheticLostContext are restored via TryRestoreContextLost [1].
Using dedicated context loss type clarifies the confusion. With this
CL, the only canvas 2d use of kSyntheticContextLost is in web tests.
These should probably be migrated to using real context losses, making
sure that we test with the same code that we run in production.

[1]: https://crsrc.org/c/third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc;l=238;drc=36c452f564b4fffe54d66e773758b87a7c930119

Bug: 404257881
Change-Id: I6ab06476bd7bddeb6915fb707fd4ccca2819fb09
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6414172
Reviewed-by: Colin Blundell <blundell@chromium.org>
Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1441267}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5183787826708480

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x79e7e2fef8f0
Crash State:
  viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept
  mojo::InterfaceEndpointClient::HandleValidatedMessage
  mojo::MessageDispatcher::Accept
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1441266:1441277

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5183787826708480

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-03-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-22)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### aw...@google.com (2026-04-01)

(pardon the noise, mouse-o!)

### dx...@google.com (2026-04-15)

Project: chromium/src  

Branch:  main  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7760835>

Don't honor transient canvas size restoration

---


Expand for full commit details
```
     
    When giving an invalid size to a 2D canvas, a contextlost event is 
    fired. If a valid size is later given, contextrestored will fire. 
    Things get complicated if the page changes the size again while 
    the contextlost and contextrestore state transitions happen. The 
    current implementation was trying to honor all state transitions 
    in scenarios where, for instance, the canvas is given a valid size 
    and an invalid size again, before contextlost fires. A unit test 
    for instance cycled the size as "good => bad => good => bad" in the 
    same task and expected events contextlost, contextrestored, 
    contextlost [1]. 
     
    This approach however doesn't really make sense. We cannot possibly 
    generalize to honoring any chain of same-task transitions. What if 
    we did one more "=> good => bad"? Really, doing "bad => good => bad" 
    in the same task is just the same as "bad => bad". Moreover, if the 
    canvas is restored while the size is invalid (even temporarily), the 
    CanvasResourceDispatcher of an OffscreenCanvas with a placeholder 
    would try to push a new frame, but since the size is invalid, the 
    context would get lost again, destroying the dispatcher while it's 
    being used. 
     
    This CL simplifies the logic by getting rid of the boolean 
    dispatch_context_restored_event_timer_ and instead just checking the 
    actual canvas size when it's time to move forward in the state machine. 
     
    This change is validated by adding web tests to validate more state 
    transition. There are lots of possible transitions to consider, given 
    that the page can change size before, during and after each events 
    forcing the canvas to bounce between lost and restored states. 
     
    [1] https://crsrc.org/c/third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html;l=146-165;drc=eb6fbdafc5a54fd4fd6f81bdc83e66b50891b682 
     
    Fixed: 494352590 
    Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760835 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1615474}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc`
- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.h`
- M `third_party/blink/web_tests/external/wpt/html/canvas/resources/canvas-promise-test.js`
- M `third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html`

---

Hash: [4d94eaa23143776dd5b66e9a79b50dd5be3c5773](https://chromiumdash.appspot.com/commit/4d94eaa23143776dd5b66e9a79b50dd5be3c5773)  

Date: Wed Apr 15 23:10:17 2026


---

### ch...@google.com (2026-04-16)

Requesting merge to M146 because latest trunk commit (1615474) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1615474) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1615474) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-16)

**M146** merge request created. **Please update [crbug/503210921](https://crbug.com/503210921) to have this merge reviewed.**

### ch...@google.com (2026-04-16)

**M147** merge request created. **Please update [crbug/503210447](https://crbug.com/503210447) to have this merge reviewed.**

### ch...@google.com (2026-04-16)

**M148** merge request created. **Please update [crbug/503211153](https://crbug.com/503211153) to have this merge reviewed.**

### 24...@project.gserviceaccount.com (2026-04-16)

ClusterFuzz testcase 5183787826708480 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1615470:1615479

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### aj...@google.com (2026-04-21)

S1 as renderer memory corruption

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-04-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7791805>

[M146] Don't honor transient canvas size restoration

---


Expand for full commit details
```
     
    Original change's description: 
    > Don't honor transient canvas size restoration 
    > 
    > When giving an invalid size to a 2D canvas, a contextlost event is 
    > fired. If a valid size is later given, contextrestored will fire. 
    > Things get complicated if the page changes the size again while 
    > the contextlost and contextrestore state transitions happen. The 
    > current implementation was trying to honor all state transitions 
    > in scenarios where, for instance, the canvas is given a valid size 
    > and an invalid size again, before contextlost fires. A unit test 
    > for instance cycled the size as "good => bad => good => bad" in the 
    > same task and expected events contextlost, contextrestored, 
    > contextlost [1]. 
    > 
    > This approach however doesn't really make sense. We cannot possibly 
    > generalize to honoring any chain of same-task transitions. What if 
    > we did one more "=> good => bad"? Really, doing "bad => good => bad" 
    > in the same task is just the same as "bad => bad". Moreover, if the 
    > canvas is restored while the size is invalid (even temporarily), the 
    > CanvasResourceDispatcher of an OffscreenCanvas with a placeholder 
    > would try to push a new frame, but since the size is invalid, the 
    > context would get lost again, destroying the dispatcher while it's 
    > being used. 
    > 
    > This CL simplifies the logic by getting rid of the boolean 
    > dispatch_context_restored_event_timer_ and instead just checking the 
    > actual canvas size when it's time to move forward in the state machine. 
    > 
    > This change is validated by adding web tests to validate more state 
    > transition. There are lots of possible transitions to consider, given 
    > that the page can change size before, during and after each events 
    > forcing the canvas to bounce between lost and restored states. 
    > 
    > [1] https://crsrc.org/c/third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html;l=146-165;drc=eb6fbdafc5a54fd4fd6f81bdc83e66b50891b682 
    > 
    > Fixed: 494352590 
    > Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760835 
    > Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    > Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1615474} 
     
    (cherry picked from commit 4d94eaa23143776dd5b66e9a79b50dd5be3c5773) 
     
    Bug: 503210921,494352590 
    Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791805 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#4007} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc`
- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.h`
- M `third_party/blink/web_tests/external/wpt/html/canvas/resources/canvas-promise-test.js`
- M `third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html`

---

Hash: [f7f989b28ccc00c66808f6acd1dabd946eb4f233](https://chromiumdash.appspot.com/commit/f7f989b28ccc00c66808f6acd1dabd946eb4f233)  

Date: Fri Apr 24 16:00:51 2026


---

### pe...@google.com (2026-04-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-24)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7791159>

[M148] Don't honor transient canvas size restoration

---


Expand for full commit details
```
     
    Original change's description: 
    > Don't honor transient canvas size restoration 
    > 
    > When giving an invalid size to a 2D canvas, a contextlost event is 
    > fired. If a valid size is later given, contextrestored will fire. 
    > Things get complicated if the page changes the size again while 
    > the contextlost and contextrestore state transitions happen. The 
    > current implementation was trying to honor all state transitions 
    > in scenarios where, for instance, the canvas is given a valid size 
    > and an invalid size again, before contextlost fires. A unit test 
    > for instance cycled the size as "good => bad => good => bad" in the 
    > same task and expected events contextlost, contextrestored, 
    > contextlost [1]. 
    > 
    > This approach however doesn't really make sense. We cannot possibly 
    > generalize to honoring any chain of same-task transitions. What if 
    > we did one more "=> good => bad"? Really, doing "bad => good => bad" 
    > in the same task is just the same as "bad => bad". Moreover, if the 
    > canvas is restored while the size is invalid (even temporarily), the 
    > CanvasResourceDispatcher of an OffscreenCanvas with a placeholder 
    > would try to push a new frame, but since the size is invalid, the 
    > context would get lost again, destroying the dispatcher while it's 
    > being used. 
    > 
    > This CL simplifies the logic by getting rid of the boolean 
    > dispatch_context_restored_event_timer_ and instead just checking the 
    > actual canvas size when it's time to move forward in the state machine. 
    > 
    > This change is validated by adding web tests to validate more state 
    > transition. There are lots of possible transitions to consider, given 
    > that the page can change size before, during and after each events 
    > forcing the canvas to bounce between lost and restored states. 
    > 
    > [1] https://crsrc.org/c/third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html;l=146-165;drc=eb6fbdafc5a54fd4fd6f81bdc83e66b50891b682 
    > 
    > Fixed: 494352590 
    > Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760835 
    > Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    > Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1615474} 
     
    (cherry picked from commit 4d94eaa23143776dd5b66e9a79b50dd5be3c5773) 
     
    Bug: 503211153,494352590 
    Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791159 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#1565} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc`
- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.h`
- M `third_party/blink/web_tests/external/wpt/html/canvas/resources/canvas-promise-test.js`
- M `third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html`

---

Hash: [4658795b7a8a599a8be111491c62c3c2374d4961](https://chromiumdash.appspot.com/commit/4658795b7a8a599a8be111491c62c3c2374d4961)  

Date: Fri Apr 24 16:34:16 2026


---

### dx...@google.com (2026-04-24)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7791948>

[M147] Don't honor transient canvas size restoration

---


Expand for full commit details
```
     
    Original change's description: 
    > Don't honor transient canvas size restoration 
    > 
    > When giving an invalid size to a 2D canvas, a contextlost event is 
    > fired. If a valid size is later given, contextrestored will fire. 
    > Things get complicated if the page changes the size again while 
    > the contextlost and contextrestore state transitions happen. The 
    > current implementation was trying to honor all state transitions 
    > in scenarios where, for instance, the canvas is given a valid size 
    > and an invalid size again, before contextlost fires. A unit test 
    > for instance cycled the size as "good => bad => good => bad" in the 
    > same task and expected events contextlost, contextrestored, 
    > contextlost [1]. 
    > 
    > This approach however doesn't really make sense. We cannot possibly 
    > generalize to honoring any chain of same-task transitions. What if 
    > we did one more "=> good => bad"? Really, doing "bad => good => bad" 
    > in the same task is just the same as "bad => bad". Moreover, if the 
    > canvas is restored while the size is invalid (even temporarily), the 
    > CanvasResourceDispatcher of an OffscreenCanvas with a placeholder 
    > would try to push a new frame, but since the size is invalid, the 
    > context would get lost again, destroying the dispatcher while it's 
    > being used. 
    > 
    > This CL simplifies the logic by getting rid of the boolean 
    > dispatch_context_restored_event_timer_ and instead just checking the 
    > actual canvas size when it's time to move forward in the state machine. 
    > 
    > This change is validated by adding web tests to validate more state 
    > transition. There are lots of possible transitions to consider, given 
    > that the page can change size before, during and after each events 
    > forcing the canvas to bounce between lost and restored states. 
    > 
    > [1] https://crsrc.org/c/third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html;l=146-165;drc=eb6fbdafc5a54fd4fd6f81bdc83e66b50891b682 
    > 
    > Fixed: 494352590 
    > Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760835 
    > Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    > Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1615474} 
     
    (cherry picked from commit 4d94eaa23143776dd5b66e9a79b50dd5be3c5773) 
     
    Bug: 503210447,494352590 
    Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791948 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3620} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc`
- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.h`
- M `third_party/blink/web_tests/external/wpt/html/canvas/resources/canvas-promise-test.js`
- M `third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html`

---

Hash: [30245b8234db76b50b3167fb57ee994ee22498c5](https://chromiumdash.appspot.com/commit/30245b8234db76b50b3167fb57ee994ee22498c5)  

Date: Fri Apr 24 16:45:27 2026


---

### pe...@google.com (2026-04-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-27)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7790540
2. Low - There was no conflict.
3. 146, 147, and 148
4. Yes, the suspected CL was merged in 2025.

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Jean-Philippe Gravel [jpgravel@chromium.org](mailto:jpgravel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7790540>

[M144-LTS] Don't honor transient canvas size restoration

---


Expand for full commit details
```
     
    When giving an invalid size to a 2D canvas, a contextlost event is 
    fired. If a valid size is later given, contextrestored will fire. 
    Things get complicated if the page changes the size again while 
    the contextlost and contextrestore state transitions happen. The 
    current implementation was trying to honor all state transitions 
    in scenarios where, for instance, the canvas is given a valid size 
    and an invalid size again, before contextlost fires. A unit test 
    for instance cycled the size as "good => bad => good => bad" in the 
    same task and expected events contextlost, contextrestored, 
    contextlost [1]. 
     
    This approach however doesn't really make sense. We cannot possibly 
    generalize to honoring any chain of same-task transitions. What if 
    we did one more "=> good => bad"? Really, doing "bad => good => bad" 
    in the same task is just the same as "bad => bad". Moreover, if the 
    canvas is restored while the size is invalid (even temporarily), the 
    CanvasResourceDispatcher of an OffscreenCanvas with a placeholder 
    would try to push a new frame, but since the size is invalid, the 
    context would get lost again, destroying the dispatcher while it's 
    being used. 
     
    This CL simplifies the logic by getting rid of the boolean 
    dispatch_context_restored_event_timer_ and instead just checking the 
    actual canvas size when it's time to move forward in the state machine. 
     
    This change is validated by adding web tests to validate more state 
    transition. There are lots of possible transitions to consider, given 
    that the page can change size before, during and after each events 
    forcing the canvas to bounce between lost and restored states. 
     
    [1] https://crsrc.org/c/third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html;l=146-165;drc=eb6fbdafc5a54fd4fd6f81bdc83e66b50891b682 
     
    (cherry picked from commit 4d94eaa23143776dd5b66e9a79b50dd5be3c5773) 
     
    Fixed: 494352590 
    Change-Id: Ib5ddab7bc51106ec04c361b3f9f8b63497f0847a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7760835 
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1615474} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7790540 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Auto-Submit: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4836} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc`
- M `third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.h`
- M `third_party/blink/web_tests/external/wpt/html/canvas/resources/canvas-promise-test.js`
- M `third_party/blink/web_tests/wpt_internal/html/canvas/context-lost/2d-invalid-size-context-lost.html`

---

Hash: [0e42e531d706a1d09fe92557e8935bce52778151](https://chromiumdash.appspot.com/commit/0e42e531d706a1d09fe92557e8935bce52778151)  

Date: Thu Apr 30 03:43:10 2026


---

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494352590)*
