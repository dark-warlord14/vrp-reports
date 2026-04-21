# Heap-use-after-free in blink::BoxPainterBase::PaintFillLayer

| Field | Value |
|-------|-------|
| **Issue ID** | [40059000](https://issues.chromium.org/issues/40059000) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | fl...@chromium.org |
| **Created** | 2022-03-07 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; Ubuntu 20.04 x64
gs://chromium-browser-asan/linux-release/asan-linux-release-978054.zip
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-978062.zip

#Reproduce

1. unzip poc.zip
2. cd poc; sudo python -m http.server 80 (Do not change the port as the address is hardcoded in the POC sample)
3. ./chrome --js-flags='--expose-gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --disable-extensions --use-gl=angle --use-angle=swiftshader --user-data-dir=test --enable-logging=stderr http://localhost/fuzz-00015.html
4. Wait for a minute, if there is no recurrence, try again, the local test recurrence rate is nearly 100%, but the ASAN log has several different situations.

ClusterFuzz cannot test this sample because many paths and ports are hard-coded.

What is the expected behavior?

What went wrong?

Type of crash
render tab

#Analysis
"-----------------registerPaint<int>--------------------" in the asan log is the key. If the problem reproduced, the last line of the log must be it.

#Patch
Not yet

#asan
[7816:7828:0307/223413.491:INFO:CONSOLE(7)] "-----------------registerPaint<int>--------------------", source: blob:http://localhost/99c2bc92-2556-41ab-a08a-4c092b905fc1 (7)
[7816:7828:0307/223413.491:INFO:CONSOLE(8)] "---cb---idx-> 3", source: blob:http://localhost/99c2bc92-2556-41ab-a08a-4c092b905fc1 (8)
=================================================================
==9252==ERROR: AddressSanitizer: heap-use-after-free on address 0x126949208dec at pc 0x7ff89339741d bp 0x00ff1a1fcba0 sp 0x00ff1a1fcbe8
READ of size 4 at 0x126949208dec thread T0
==9252==WARNING: Failed to use and restart external symbolizer!
==9252==*** WARNING: Failed to initialize DbgHelp!              ***
==9252==*** Most likely this means that the app is already      ***
==9252==*** using DbgHelp, possibly with incompatible flags.    ***
==9252==*** Due to technical reasons, symbolization might crash ***
==9252==*** or produce wrong results.                           ***
    #0 0x7ff89339741c in blink::BoxPainterBase::PaintFillLayer C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\box_painter_base.cc:970
    #1 0x7ff89339408a in blink::BoxPainterBase::PaintFillLayers C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\box_painter_base.cc:56
    #2 0x7ff892bded6b in blink::NGBoxFragmentPainter::PaintBackground C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:1364
    #3 0x7ff892bdd9c0 in blink::NGBoxFragmentPainter::PaintBoxDecorationBackgroundWithRectImpl C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:1176
    #4 0x7ff892bdbf7d in blink::NGBoxFragmentPainter::PaintBoxDecorationBackgroundWithRect C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:1115
    #5 0x7ff892bd313d in blink::NGBoxFragmentPainter::PaintBoxDecorationBackground C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:1037
    #6 0x7ff892bd0093 in blink::NGBoxFragmentPainter::PaintObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:550
    #7 0x7ff892bcd15f in blink::NGBoxFragmentPainter::PaintInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:439
    #8 0x7ff892bd81db in blink::NGBoxFragmentPainter::PaintBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:787
    #9 0x7ff892bd6cfc in blink::NGBoxFragmentPainter::PaintBlockChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:745
    #10 0x7ff892bd0994 in blink::NGBoxFragmentPainter::PaintObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:612
    #11 0x7ff892bcd7d0 in blink::NGBoxFragmentPainter::PaintInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:462
    #12 0x7ff892bd81db in blink::NGBoxFragmentPainter::PaintBlockChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:787
    #13 0x7ff892bd6cfc in blink::NGBoxFragmentPainter::PaintBlockChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:745
    #14 0x7ff892bd0994 in blink::NGBoxFragmentPainter::PaintObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:612
    #15 0x7ff892bcd7d0 in blink::NGBoxFragmentPainter::PaintInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\ng\ng_box_fragment_painter.cc:462
    #16 0x7ff88f436de7 in blink::PaintLayerPainter::PaintFragmentWithPhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:488
    #17 0x7ff88f435b3b in blink::PaintLayerPainter::PaintWithPhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:514
    #18 0x7ff88f4362bb in blink::PaintLayerPainter::PaintForegroundPhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:521
    #19 0x7ff88f43411d in blink::PaintLayerPainter::PaintLayerContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:365
    #20 0x7ff88f435ed5 in blink::PaintLayerPainter::PaintChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:428
    #21 0x7ff88f434297 in blink::PaintLayerPainter::PaintLayerContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\paint_layer_painter.cc:377
    #22 0x7ff88f437856 in blink::FramePainter::Paint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\frame_painter.cc:93
    #23 0x7ff88c12f2fd in blink::LocalFrameView::PaintTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2929
    #24 0x7ff88c12a2b9 in blink::LocalFrameView::RunPaintLifecyclePhase C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2742
    #25 0x7ff88c126aaa in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2513
    #26 0x7ff88c123b8e in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2350
    #27 0x7ff88c12370e in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2097
    #28 0x7ff88efebc98 in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:153
    #29 0x7ff88c0dbfba in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1295
    #30 0x7ff88f185a63 in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:812
    #31 0x7ff889b8b63a in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:379
    #32 0x7ff88cc2e837 in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:256
    #33 0x7ff890b679f2 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:748
    #34 0x7ff8870ad1f4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #35 0x7ff889f26f15 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:385
    #36 0x7ff889f264e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:290
    #37 0x7ff889efec07 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #38 0x7ff889f28640 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497
    #39 0x7ff88702d023 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #40 0x7ff889a14da2 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:290
    #41 0x7ff886c61b1b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:684
    #42 0x7ff886c63757 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1044
    #43 0x7ff886c6014b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:401
    #44 0x7ff886c608d4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:429
    #45 0x7ff87bdb14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #46 0x7ff7a3215b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #47 0x7ff7a3212b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #48 0x7ff7a360dbc3 in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #49 0x7ff9091f7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #50 0x7ff909702650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x126949208dec is located 76 bytes inside of 88-byte region [0x126949208da0,0x126949208df8)
freed by thread T9 here:
    #0 0x7ff7a32bdc7b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff890b51562 in gfx::TransformAnimationCurve::Tick C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\keyframe\animation_curve.cc:44
    #2 0x7ff890b434fa in gfx::KeyframeEffect::TickKeyframeModel C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\keyframe\keyframe_effect.cc:212
    #3 0x7ff88cbf99d7 in cc::KeyframeEffect::Tick C:\b\s\w\ir\cache\builder\src\cc\animation\keyframe_effect.cc:115
    #4 0x7ff889bbecc3 in cc::AnimationTimeline::TickTimeLinkedAnimations C:\b\s\w\ir\cache\builder\src\cc\animation\animation_timeline.cc:97
    #5 0x7ff889b7f97d in cc::AnimationHost::TickAnimations C:\b\s\w\ir\cache\builder\src\cc\animation\animation_host.cc:520
    #6 0x7ff88cc7506f in cc::LayerTreeHostImpl::AnimateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:4274
    #7 0x7ff88cc4e80a in cc::LayerTreeHostImpl::AnimateInternal C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:989
    #8 0x7ff88cc68252 in cc::LayerTreeHostImpl::WillBeginImplFrame C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:2992
    #9 0x7ff890b78005 in cc::Scheduler::BeginImplFrame C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:677
    #10 0x7ff890b76fc8 in cc::Scheduler::BeginImplFrameWithDeadline C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:564
    #11 0x7ff890b75bfe in cc::Scheduler::OnBeginFrameDerivedImpl C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:432
    #12 0x7ff88b3ebdd9 in viz::BeginFrameObserverBase::OnBeginFrame C:\b\s\w\ir\cache\builder\src\components\viz\common\frame_sinks\begin_frame_source.cc:91
    #13 0x7ff88b3f2b45 in viz::ExternalBeginFrameSource::OnBeginFrame C:\b\s\w\ir\cache\builder\src\components\viz\common\frame_sinks\begin_frame_source.cc:553
    #14 0x7ff888843bc1 in cc::mojo_embedder::AsyncLayerTreeFrameSink::OnBeginFrame C:\b\s\w\ir\cache\builder\src\cc\mojo_embedder\async_layer_tree_frame_sink.cc:279
    #15 0x7ff87edb8c29 in viz::mojom::CompositorFrameSinkClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\services\viz\public\mojom\compositing\compositor_frame_sink.mojom.cc:1550
    #16 0x7ff8873e35a8 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:921
    #17 0x7ff88a068892 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #18 0x7ff8873e71ca in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:663
    #19 0x7ff8873fb451 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096
    #20 0x7ff8873fa1e3 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:716
    #21 0x7ff88a068892 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #22 0x7ff8873de28c in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561
    #23 0x7ff8873dfac7 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618
    #24 0x7ff887432e4a in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:278
    #25 0x7ff8870ad1f4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #26 0x7ff889f26f15 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:385
    #27 0x7ff889f264e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:290

previously allocated by thread T9 here:
    #0 0x7ff7a32bdd7b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff89991ba9e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff87bf4d66a in std::__1::__split_buffer<perfetto::trace_processor::RawMemoryGraphNode::MemoryNodeEntry,std::__1::allocator<perfetto::trace_processor::RawMemoryGraphNode::MemoryNodeEntry> &>::__split_buffer C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__split_buffer:314
    #3 0x7ff88a7ebf93 in std::__1::vector<gfx::TransformOperation,std::__1::allocator<gfx::TransformOperation> >::push_back C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:1642
    #4 0x7ff88a7eadb0 in gfx::TransformOperations::BlendInternal C:\b\s\w\ir\cache\builder\src\ui\gfx\geometry\transform_operations.cc:359
    #5 0x7ff88a7ea88d in gfx::TransformOperations::Blend C:\b\s\w\ir\cache\builder\src\ui\gfx\geometry\transform_operations.cc:50
    #6 0x7ff89271741e in gfx::KeyframedTransformAnimationCurve::GetValue C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\keyframe\keyframed_animation_curve.cc:407
    #7 0x7ff890b51517 in gfx::TransformAnimationCurve::Tick C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\keyframe\animation_curve.cc:44
    #8 0x7ff890b434fa in gfx::KeyframeEffect::TickKeyframeModel C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\keyframe\keyframe_effect.cc:212
    #9 0x7ff88cbf99d7 in cc::KeyframeEffect::Tick C:\b\s\w\ir\cache\builder\src\cc\animation\keyframe_effect.cc:115
    #10 0x7ff889bbecc3 in cc::AnimationTimeline::TickTimeLinkedAnimations C:\b\s\w\ir\cache\builder\src\cc\animation\animation_timeline.cc:97
    #11 0x7ff889b7f97d in cc::AnimationHost::TickAnimations C:\b\s\w\ir\cache\builder\src\cc\animation\animation_host.cc:520
    #12 0x7ff88cc7506f in cc::LayerTreeHostImpl::AnimateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:4274
    #13 0x7ff88cc4e80a in cc::LayerTreeHostImpl::AnimateInternal C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:989
    #14 0x7ff88cc68252 in cc::LayerTreeHostImpl::WillBeginImplFrame C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host_impl.cc:2992
    #15 0x7ff890b78005 in cc::Scheduler::BeginImplFrame C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:677
    #16 0x7ff890b76fc8 in cc::Scheduler::BeginImplFrameWithDeadline C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:564
    #17 0x7ff890b75bfe in cc::Scheduler::OnBeginFrameDerivedImpl C:\b\s\w\ir\cache\builder\src\cc\scheduler\scheduler.cc:432
    #18 0x7ff88b3ebdd9 in viz::BeginFrameObserverBase::OnBeginFrame C:\b\s\w\ir\cache\builder\src\components\viz\common\frame_sinks\begin_frame_source.cc:91
    #19 0x7ff88b3f2b45 in viz::ExternalBeginFrameSource::OnBeginFrame C:\b\s\w\ir\cache\builder\src\components\viz\common\frame_sinks\begin_frame_source.cc:553
    #20 0x7ff888843bc1 in cc::mojo_embedder::AsyncLayerTreeFrameSink::OnBeginFrame C:\b\s\w\ir\cache\builder\src\cc\mojo_embedder\async_layer_tree_frame_sink.cc:279
    #21 0x7ff87edb8c29 in viz::mojom::CompositorFrameSinkClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\services\viz\public\mojom\compositing\compositor_frame_sink.mojom.cc:1550
    #22 0x7ff8873e35a8 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:921
    #23 0x7ff88a068892 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #24 0x7ff8873e71ca in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:663
    #25 0x7ff8873fb451 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096
    #26 0x7ff8873fa1e3 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:716
    #27 0x7ff88a068892 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43

Thread T9 created by T0 here:
    #0 0x7ff7a32c90e2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ff88717d8ee in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:184
    #2 0x7ff8870f6340 in base::SimpleThread::StartAsync C:\b\s\w\ir\cache\builder\src\base\threading\simple_thread.cc:51
    #3 0x7ff885809b80 in blink::Thread::CreateAndSetCompositorThread C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\scheduler\common\thread.cc:100
    #4 0x7ff88ca27e35 in content::RenderThreadImpl::InitializeCompositorThread C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:892
    #5 0x7ff88ca24cfe in content::RenderThreadImpl::InitializeWebKit C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:952
    #6 0x7ff88ca21e03 in content::RenderThreadImpl::Init C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:647
    #7 0x7ff88ca2432c in content::RenderThreadImpl::RenderThreadImpl C:\b\s\w\ir\cache\builder\src\content\renderer\render_thread_impl.cc:580
    #8 0x7ff889a149ba in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:237
    #9 0x7ff886c61b1b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:684
    #10 0x7ff886c63757 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1044
    #11 0x7ff886c6014b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:401
    #12 0x7ff886c608d4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:429
    #13 0x7ff87bdb14ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #14 0x7ff7a3215b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #15 0x7ff7a3212b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #16 0x7ff7a360dbc3 in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #17 0x7ff9091f7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #18 0x7ff909702650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\paint\box_painter_base.cc:970 in blink::BoxPainterBase::PaintFillLayer
Shadow bytes around the buggy address:
  0x04a672341160: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x04a672341170: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04a672341180: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x04a672341190: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04a6723411a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x04a6723411b0: fa fa fa fa fd fd fd fd fd fd fd fd fd[fd]fd fa
  0x04a6723411c0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x04a6723411d0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x04a6723411e0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x04a6723411f0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x04a672341200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==9252==ABORTING

Did this work before? N/A 

Chrome version: 99.0.4844.0  Channel: n/a
OS Version: 10.0

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 137.9 KB)
- [asan1.txt](attachments/asan1.txt) (text/plain, 29.0 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 19.5 KB)
- [asan3.txt](attachments/asan3.txt) (text/plain, 24.3 KB)
- [repro.zip](attachments/repro.zip) (application/octet-stream, 143.4 KB)
- [clusterfuzz-testcase-5735980887900160.zip](attachments/clusterfuzz-testcase-5735980887900160.zip) (application/octet-stream, 148.6 KB)

## Timeline

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-08)

In the future, please try to clean up the POC so that it doesn't require running python as root. I edited the repro locally to convince it to work and was able to reproduce, so let's see what Clusterfuzz says.

### cl...@chromium.org (2022-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6207230910988288.

### cl...@chromium.org (2022-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5750538515578880.

### m....@gmail.com (2022-03-08)

re https://crbug.com/chromium/1303597#c02 You can give cf more timeout and try.

I have a custom sample minimization tool, but this sample will cause the reproduction to be unstable during the process, so I directly submitted the original sample, but your modified version can be reproduced by my local test.

### dc...@chromium.org (2022-03-08)

I can't get Clusterfuzz to repro this, though I think there's an issue with where the subresources are located. I'll work with the sheriffs to try to get that resolved. Hopefully, once the Clusterfuzz issue is sorted out, that will help with the FoundIn-X label as well as the minimization.

For future repros, I suggest teaching the fuzzer not to use absolute paths. It makes things a lot harder to move around, and no one should be running python as root :)

I've also attached repro with the paths fixed so they work with relative paths. The following Chrome command should be sufficient to repro (assuming http server running on port 8000):
$ out/asan/chrome --js-flags='--expose-gc --allow-natives-syntax' --enable-blink-test-features --disable-extensions --use-gl=angle --use-angle=swiftshader --enable-logging=stderr   http://127.0.0.1:8000/fuzzer-testcases/fuzz-00015.html

[Monorail components: Blink>Paint]

### wa...@chromium.org (2022-03-08)

If --enable-bink-test-features is needed to reproduce, this bug won't affect normal users. Will try to find which test feature is causing this.

### m....@gmail.com (2022-03-08)

I guess it may be related to the registerPaint feature

### wa...@chromium.org (2022-03-11)

Minimized command line to reproduce:
out/asan/chrome --enable-blink-features=AccessibilityObjectModel http://127.0.0.1:8000/fuzzer-testcases/fuzz-00015.html

The "freed by" and "allocated by" stack traces seem random. The type of object allocated and freed is not related to the type of the used object after free. It seems that the address of |bg_layer| is random, which may indicate that reversed_paint_list [1] contains invalid pointers.

dmazzoni@, what's the status of the AccessibilityObjectModel feature? It has been there for several years. Do you have any idea why it causes the use-after-free in paint code?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/box_painter_base.cc;l=45

[Monorail components: Blink>Accessibility]

### wa...@chromium.org (2022-03-12)

The stack memory is corrupted (and the address of bg_layer is changed) during GetImage() here: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/box_painter_base.cc;drc=5a758a97032f0b656c3c36a3497560762495501a;l=964

Wondering why asan fails to detect what causes the the stack corruption, but blames the deref of the corrupted reference. 


### [Deleted User] (2022-03-12)

[Empty comment from Monorail migration]

### wa...@chromium.org (2022-03-12)

+people to access this bug for internal discussion.

[Monorail components: Blink>Canvas]

### wa...@chromium.org (2022-03-12)

With a DCHECK non-asan build, a DCHECK fails during StyleGeneratedImage::GetImage():
[632376:1:0312/105439.301042:FATAL:node.cc(1596)] Check failed: GetDocument().Lifecycle().StateAllowsDetach() || GetDocument().GetStyleEngine().InContainerQueryStyleRecalc(). 
#0 0x5609d764abd9 base::debug::CollectStackTrace()
#1 0x5609d756aff3 base::debug::StackTrace::StackTrace()
#2 0x5609d75830a0 logging::LogMessage::~LogMessage()
#3 0x5609d7583b5e logging::LogMessage::~LogMessage()
#4 0x5609db6202f1 blink::Node::DetachLayoutTree()
#5 0x5609db661e7f blink::ContainerNode::DetachLayoutTree()
#6 0x5609db63d96d blink::Element::DetachLayoutTree()
#7 0x5609db661e7f blink::ContainerNode::DetachLayoutTree()
#8 0x5609db748bac blink::ShadowRoot::DetachLayoutTree()
#9 0x5609db63d955 blink::Element::DetachLayoutTree()
#10 0x5609db660ff5 blink::ContainerNode::RemoveBetween()
#11 0x5609db65fda2 blink::ContainerNode::RemoveChild()
#12 0x5609dd706318 blink::(anonymous namespace)::v8_element::RemoveOperationCallback()
#13 0x5609d55bf870 v8::internal::FunctionCallbackArguments::Call()
#14 0x5609d55bde85 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#15 0x5609d55bb9eb v8::internal::Builtin_Impl_HandleApiCall()
#16 0x5609d55bb4a9 v8::internal::Builtin_HandleApiCall()
#17 0x560957edfa78 <unknown>


### [Deleted User] (2022-03-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-03-14)

[Comment Deleted]

### wa...@chromium.org (2022-03-15)

To reproduce:
1. Download repro.zip in https://crbug.com/chromium/1303597#c6 and unzip it
2. Run 'python -m http.server 8000' in the download directory
3. Build DCHECK+Release chrome, and run with --enable-blink-features=AccessibilityObjectModel http://127.0.0.1:8000/fuzzer-testcases/fuzz-00015.html

After some time, the renderer crashes at a DCHECK. Stack trace is in https://crbug.com/chromium/1303597#c13. The situation found by the DCHECK failure will cause use-after-free in an asan build.

The sequence of execution when before the DCHECK failure (or asan use-after-free/buffer-overflow): 
1. <body>'s onload event handler creates an image element. 
2. The image's onload event fires, and the event handler calls a huge async function trigger1().
3. After some document cycles, trigger1() reaches the following code and yields:
     var v3189 = await v2086.getComputedAccessibleNode(v1848);
4. In the next document cycle, an element with background:paint(paintlet1) paints its background.
5. The paint worklet class registered as paintlet1 is to be constructed. The code calls the JavaScript constructor of the paint worklet class.
6. The JavaScript code after 3 seems to execute in the paint worklet's context. The DCHECK fails before the constructor in #5 returns.
7. (In a non-DCHECK build): The constructor in #5 returns, but during #6, the stack of the current thread is corrupted, and a reference variable in the stack points to an invalid address.
8. (In a non-DCHECK asan build): Dereference of the reference variable in #7 causes use-after-free or buffer-overflow.

You can apply the patch https://paste.googleplex.com/5911055793389568 locally, and add console.log before and after the line shown in #3 in fuzz-00015.html, to show the above execution sequence with more details.

I'm not sure if this is an AccessibilityObjectModel bug or a V8 bug. Assigning to aleventhal@chromium.org who is an owner of third_party/blink/renderer/modules/accessibility. Please assign to V8 team if you believe this is a V8 bug.

BTW, what's the status of AccessibilityObjectModel which has been in experimental status for several years?

[Monorail components: Blink>JavaScript]

### wa...@chromium.org (2022-03-15)

(Rephrasing the question at the end of https://crbug.com/chromium/1303597#c16: What's the plan of AccessibilityObjectModel which has been in experimental status for several years?)

This is the native stack where the JavaScript code after 'await getComputedAccessibleNode' is called when we construct a paint worklet:

#5 0x55c752be41b9 v8::internal::MicrotaskQueue::RunMicrotasks()
#6 0x55c752be3ce6 v8::internal::MicrotaskQueue::PerformCheckpointInternal()
#7 0x55c75295da6e v8::MicrotasksScope::~MicrotasksScope()
#8 0x55c758c59278 blink::V8ScriptRunner::CallAsConstructor()
#9 0x55c759cdf00e blink::bindings::CallbackInvokeHelper<>::Call()
#10 0x55c759ce50aa blink::V8NoArgumentConstructor::Construct()
#11 0x55c75a5cf69e blink::CSSPaintDefinition::MaybeCreatePaintInstance()
#12 0x55c75a5cf27b blink::CSSPaintDefinition::Paint()
#13 0x55c75a5ca492 blink::PaintWorklet::Paint()
#14 0x55c758e93ffb blink::CSSPaintValue::GetImage()
#15 0x55c758b4d579 blink::CSSImageGeneratorValue::GetImage()
#16 0x55c759698395 blink::BoxPainterBase::PaintFillLayer()
#17 0x55c759697fce blink::BoxPainterBase::PaintFillLayers()
...
(a normal document lifecycle update)

The MicrotaskQueue contains a microtask for the "then" of "await getComputedAccessibleNode". The microtask may be still in the right context, but it runs at wrong time (when we don't expect DOM mutations during paint).

This may not be a AccessibilityObjectModel problem. I need to investigate more to properly triage this.

### wa...@chromium.org (2022-03-16)

Turned out that AccessibillityObjectModel just triggers the problem. The root cause is that PaintWorklet doesn't have a separate microtask queue.

### wa...@chromium.org (2022-03-16)

I have tried every way to fix this, but they all failed. As I have never worked on csspaint, I'm unassigning myself so that someone more familiar with this area can pick this up.

[Monorail components: -Blink>Accessibility]

### wa...@chromium.org (2022-03-17)

Assigning to the the owner of third_party/blink/renderer/modules/csspaint. flackr@ can you take a look?

### pd...@chromium.org (2022-03-17)

Re-triaging to canvas who owns paint worklet.

### [Deleted User] (2022-03-21)

fserb: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-03-28)

Pinged fserb via email but no response :( - ccing everyone else on the GPU Canvas team in the hopes that someone can fix this (which apparently is to add a microtask queue to the PaintWorklet according to https://crbug.com/chromium/1303597#c18).

### ju...@chromium.org (2022-03-28)

 wangxianzhu@ have you tried what you mentioned in https://crbug.com/chromium/1303597#c18? 
According to https://crbug.com/chromium/1303597#c19 it seems that hasn't worked?

### wa...@chromium.org (2022-03-29)

juanmihd@ I added you in the internal discussion thread.

### fs...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### vm...@chromium.org (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### ju...@chromium.org (2022-04-01)

Jeremy, Hiroki,
I think you've both have worked on worklet architecture, could you please take a look at this to see if you have any ideas or suggestions on how to move forward?

There is a tentative CL to create a separate microtask queue, as suggested in https://crbug.com/chromium/1303597#c18, but it has some issues.
https://chromium-review.googlesource.com/c/chromium/src/+/3528337

### nh...@chromium.org (2022-04-04)

Does this issue happen only on the main thread paint worklets? IIRC the paint worklets could run on non-main threads depending on the feature flag (OffMainThreadCSSPaint), and it seems like the flag is now enabled by default[1]. If we no longer support the main thread paint worklets, could we simply remove them instead of fixing the issue?

[1]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/runtime_enabled_features.json5;l=1656-1657;drc=f29dae990982590742ca472957af4ace08c2909d

### wa...@chromium.org (2022-04-04)

According to https://crbug.com/chromium/1306778, this bug doesn't apply to off-main-thread paint worklets. For now OffMainThreadCSSPaint seems to only control whether off-main-thread csspaint worklet is supported. Is it easy to switch main-thread csspaint worklet to off-main-thread?

### nh...@chromium.org (2022-04-04)

Anyone knows the current status of OffMainThreadCSSPaint? The flag is flipped by xidachen@ (https://crbug.com/chromium/829967), but xidachen@ seems no longer active. 

### nh...@chromium.org (2022-04-04)

I'm also curious if the proposed fix on https://crbug.com/chromium/1303597#c31 that creates a separate microtask queue is compatible with the paint worklet spec.

### fl...@chromium.org (2022-04-04)

OffMainThreadCSSPaint is indeed fully stable and shipped, however, not all paint worklets can run off of the main thread. CSSPaintValue::GetImage[1] is where we make the decision, which is based on the inputs being used by the paint worklet. Specifically, PaintWorkletStylePropertyMap::BuildCrossThreadData will return null for paint worklet inputs which are not currently cloneable to the worklet thread (e.g. rich CSSOM types). Until we can support cloning all possible style inputs we can't require all paint worklets to run off the main thread.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_paint_value.cc?q=CSSPaintValue::GetImage%20file:css_paint_value%5C.cc&ss=chromium%2Fchromium%2Fsrc

### nh...@chromium.org (2022-04-05)

https://crbug.com/chromium/1303597#c35: Thanks for the clarification! I understand we still need to keep the OnMainThreadCSSPaint.

Regarding the spec compatibility (#c34), probably it's ok as OffMainThreadCSSPaint already has a separate microtask queue?

### ju...@chromium.org (2022-04-12)

I understand the discussion as that the proposed fix of adding the microtask queue will fix the issue and it makes sense to be used according to the spec.

I will now focus on the failing test of direct-import to see why it's failing and try to fix it.

### ju...@chromium.org (2022-04-12)

When I try to open the failing test (https://localhost:9000/css/css-paint-api/dynamic-import.https.html) locally with the fix, it is working properly, but when I try to run it on content shell and the test infrastructure the test is failing. 

So the fix seems to be good but the test with the fix is failing only with content_shell. 

### ju...@chromium.org (2022-04-12)

nhiroki@ or someone with more experience with microtasks, is there any special need for these tests to work on CQ with Content_shell? https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/css/css-paint-api/dynamic-import.https.html

### ju...@chromium.org (2022-04-14)

I need some help here from any cc'ed in this bug that has more experience writing tests with paint worklet and the microtask queue interaction.

I have tried dynamic-import.https.html test by opening the wptserve 
vpython third_party/blink/tools/run_blink_wptserve.py -t Release

And then opening it both with chrome or with content_shell and the test is working properly.

When I try to execute it with third_party/blink/tools/run_web_tests.py -t Release external/wpt/css/css-paint-api/dynamic-import.https.html the test is failing again.

Any ideas or suggestions on how to debug the run_web_tests.py way to run the content_shell wpt tests?

### ju...@chromium.org (2022-04-14)

It seems that the test was effectively working, but as it was written as a reference test, the screenshot taken was before the import threw. I've rewritten the test to effectively validate what it has to do, that doing a dynamic import inside a worklet should throw.

So the CL should be ready to review.

### ju...@chromium.org (2022-04-14)

I'm blocked with this and will stop to actively work on this. 

My findings so far is that the test dynamic-import with the fix seems to work (when I add a console.log("debug") here https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/css/css-paint-api/dynamic-import.https.html;l=26?q=external%2Fwpt%2Fcss%2Fcss-paint-api%2Fdynamic-import.https.html&ss=chromium it's logging that, so it is effectively throwing an error.

While testing on chrome and on context_shell this is properly working, but I'm unable to either write a non reference test to validate this throwing of the exception or to make this reference test work.

I would need some support from somoeone who understand better paintworklets and wpt infrastructure.

### ju...@chromium.org (2022-04-14)

[Empty comment from Monorail migration]

### wa...@chromium.org (2022-04-15)

Does increasing '2' to '3' or greater at https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/external/wpt/common/worklet-reftest.js;drc=3feb6ba9d962518e7aa982cbe59fc2448efba54d;l=30 work?

### bo...@chromium.org (2022-04-22)

This is your friendly security marshal checking in since this appears to be stuck.

Reassigning to @nhiroki to help @juanmihd get unstuck. @nhiroki, please redirect as appropriate if you're not in a position to provide assistance. 

Setting ImpactNone and reducing severity to Medium because a non-standard flag (--enable-blink-test-features) is required to expose the vulnerability. 

### bo...@chromium.org (2022-04-22)

A note for folks coming after me:

I'm am unable to repro the UAF crash using an ASAN build from tip of tree (103.0.5020.0) with the revised POC and invocation provided by @dcheng in https://crbug.com/chromium/1303597#c6 on Linux after >5 tries

### wa...@chromium.org (2022-04-23)

bookholt@ can you reproduce in the steps in https://crbug.com/chromium/1303597#c16?

### bo...@chromium.org (2022-04-25)

No, not with my ASAN build from Friday. For transparency, I'm using the following invocation via SSH

xvfb-run -a out/asan/chrome --enable-blink-features=AccessibilityObjectModel  --enable-logging=stderr https://..../fuzzer-testcases/fuzz-00015.html

### ju...@chromium.org (2022-04-25)

I just tried with Release and the steps in https://crbug.com/chromium/1303597#c16 and I get the same DCHECK as before,
[2327209:1:0425/201329.120008:FATAL:node.cc(1595)] Check failed: GetDocument().Lifecycle().StateAllowsDetach() || GetDocument().GetStyleEngine().InContainerQueryStyleRecalc(). 

There is a potential fix in https://chromium-review.googlesource.com/c/chromium/src/+/3528337 but it still has some issues. I haven't being able to make the suggested test in one of the CL's comments work.  

I am unsure if there is some issue with how the microtask is setted up. 

### pd...@chromium.org (2022-05-01)

Paint worklet is owned by canvas and the fix is outside paint code so I'm removing Blink>Paint for bug triaging purposes.

[Monorail components: -Blink>Paint]

### m....@gmail.com (2022-05-13)

[Comment Deleted]

### m....@gmail.com (2022-06-01)

any update on this?

### m....@gmail.com (2022-06-14)

ping@

### m....@gmail.com (2022-06-24)

My fuzzer running on CF reports a stable reproduction sample https://clusterfuzz.com/testcase-detail/5735980887900160

### nh...@chromium.org (2022-06-24)

Sorry, I didn't notice this is assigned to me. I'm not an expert of MicrotaskQueue and PaintWorklet APIs. Could someone in the component owners take this?

### bo...@chromium.org (2022-06-24)

@schenney, can you please help route this bug and shepherd toward resolution? It's a verified medium severity heap buffer overflow in the painter that's been lingering since early May. Help is most appreciated :)

### sc...@chromium.org (2022-06-24)

Assigning to flackr@ to move this forward. Based on the CL from https://crbug.com/chromium/1303597#c49 we're blocked on getting a test that works. Maybe re-assign to juanmihd@ once you've looked at the CL and test again.

### m....@gmail.com (2022-06-29)

Testcase found by fuzzer run on CF.
```
[Environment] ASAN_OPTIONS=alloc_dealloc_mismatch=0:allocator_may_return_null=1:allow_user_segv_handler=0:check_malloc_usable_size=0:detect_leaks=0:detect_odr_violation=0:detect_stack_use_after_return=1:fast_unwind_on_fatal=1:handle_abort=1:handle_segv=1:handle_sigbus=1:handle_sigfpe=1:handle_sigill=1:max_uar_stack_size_log=16:print_scariness=1:print_summary=1:print_suppressions=0:redzone=16:strict_memcmp=0:symbolize=0:use_sigaltstack=1
[Command line] /mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds_media_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-1018366/chrome --user-data-dir=/mnt/scratch0/tmp/user_profile_0 --enable-logging=stderr --v=1 --ignore-gpu-blacklist --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --dns-prefetch-disable --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --force-internal-pdf --js-flags="--expose-gc --verify-heap" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --use-gl=angle --use-angle=swiftshader --enable-shadow-dom --enable-media-stream --enable-mp3-stream-parser --disable-in-process-stack-traces --enable-experimental-web-platform-features /mnt/scratch0/clusterfuzz/bot/inputs/fuzzer-testcases/fuzz-00371.html
```

### m....@gmail.com (2022-07-25)

@ping CF still reproduce.
https://clusterfuzz.com/testcase-detail/6221344513654784

### am...@chromium.org (2022-08-08)

The clusterfuzz testcase in https://crbug.com/chromium/1303597#c54 (https://clusterfuzz.com/testcase-detail/5735980887900160) did actively reproduce; however, clusterfuzz has remarked that as fixed in revision range 1022978:1022984. Is this correct, and can someone confirm if this issue has been resolved? 

As this issue is SI-None, there is no SLO to resolve (until the code is enabled by default/no longer behind a command line flag), but adding a next action would be helpful to avoid future security pings if this issue is not yet resolved. Thanks! 

### wa...@chromium.org (2022-08-08)

Actually this bug didn't require --enable-blink-test-features to reproduce, so SI-None was incorrect. Please see https://crbug.com/chromium/1303597#c18. Now sure about the current status, but the root cause doesn't seem to have been fixed.

I can't access the https://crbug.com/chromium/1303597#c54 and https://crbug.com/chromium/1303597#c59 test cases.

### am...@chromium.org (2022-08-09)

Thank you for that update. I've removed SI-None. Original label for FoundIn-99 remains as that was oldest active release channel at the time this was reported. 
Because the test cases in https://crbug.com/chromium/1303597#c54 and https://crbug.com/chromium/1303597#c59 did not reliably reproduce, they have expired off clusterfuzz, so they are not accessible to any of us. 

OP, can you provide those test cases once again to assist? 

### am...@chromium.org (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

[Empty comment from Monorail migration]

### aa...@chromium.org (2022-08-09)

[Empty comment from Monorail migration]

### wa...@chromium.org (2022-08-09)

https://crbug.com/chromium/1303597#c16 contains steps to reliably reproduce the bug, but I'm not sure if it still works. The steps require --enable-blink-features=AccessibilityObjectModel, but the root cause of this bug is unrelated to the flag.

https://chromium-review.googlesource.com/c/chromium/src/+/3528337 contains a unit test that can reproduce the issue in a controlled environment.


### [Deleted User] (2022-08-10)

flackr: Uh oh! This issue still open and hasn't been updated in the last 127 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-09-30)

@ping owner Long time no update progress.

### m....@gmail.com (2022-10-17)

@ping OWNER

It's been too long without an update, not sure how the progress of this issue is.

But CF still has new crashes(https://clusterfuzz.com/testcase-detail/6237578485497856)

### am...@chromium.org (2022-10-17)

flaky repro in clusterfuzz, dumping the stack trace from clusterfuzz as the testcase will be deleted by clusterfuzz on 24 October if no longer seen
will also attempt to link this bug to the test case to attempt to make it more accessible 

=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60a0000e8c40 at pc 0x55f6f97f92aa bp 0x7fff693e16d0 sp 0x7fff693e16c8
READ of size 7 at 0x60a0000e8c40 thread T0 (chrome)
SCARINESS: 49 (7-byte-read-heap-use-after-free)
    #0 0x55f6f97f92a9 in GetType third_party/blink/renderer/core/style/fill_layer.h:215:71
    #1 0x55f6f97f92a9 in ShouldApplyBlendOperation third_party/blink/renderer/core/paint/box_painter_base.cc:1023:41
    #2 0x55f6f97f92a9 in blink::BoxPainterBase::PaintFillLayer(blink::PaintInfo const&, blink::Color const&, blink::FillLayer const&, blink::PhysicalRect const&, blink::BackgroundBleedAvoidance, blink::BackgroundImageGeometry&, bool, blink::PhysicalSize const&) third_party/blink/renderer/core/paint/box_painter_base.cc:1077:9
    #3 0x55f6f97f60bb in blink::BoxPainterBase::PaintFillLayers(blink::PaintInfo const&, blink::Color const&, blink::FillLayer const&, blink::PhysicalRect const&, blink::BackgroundImageGeometry&, blink::BackgroundBleedAvoidance) third_party/blink/renderer/core/paint/box_painter_base.cc:60:5
    #4 0x55f6f97e373e in PaintBackground third_party/blink/renderer/core/paint/box_painter.cc:221:21
    #5 0x55f6f97e373e in blink::BoxPainter::PaintBoxDecorationBackgroundWithRect(blink::PaintInfo const&, gfx::Rect const&, blink::PhysicalRect const&, blink::DisplayItemClient const&) third_party/blink/renderer/core/paint/box_painter.cc:174:7
    #6 0x55f6f97e1b2d in blink::BoxPainter::PaintBoxDecorationBackground(blink::PaintInfo const&, blink::PhysicalOffset const&) third_party/blink/renderer/core/paint/box_painter.cc:99:5
    #7 0x55f6f9a92bbb in blink::ReplacedPainter::Paint(blink::PaintInfo const&) third_party/blink/renderer/core/paint/replaced_painter.cc:155:12
    #8 0x55f6f8c6d2c2 in blink::LayoutReplaced::Paint(blink::PaintInfo const&) const third_party/blink/renderer/core/layout/layout_replaced.cc:158:26
    #9 0x55f6f9948a39 in blink::ObjectPainter::PaintAllPhasesAtomically(blink::PaintInfo const&) third_party/blink/renderer/core/paint/object_painter.cc:114:18
    #10 0x55f6f98bd02b in blink::(anonymous namespace)::PaintFragment(blink::NGPhysicalBoxFragment const&, blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:403:35
    #11 0x55f6f98c367c in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGPhysicalBoxFragment const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:1675:7
    #12 0x55f6f98c49a8 in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:1709:7
    #13 0x55f6f98b7bb2 in blink::NGBoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&, blink::NGInlineCursor*) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:1467:11
    #14 0x55f6f98bbc36 in blink::NGBoxFragmentPainter::PaintLineBoxChildItems(blink::NGInlineCursor*, blink::PaintInfo const&, blink::PhysicalOffset const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:1557:7
    #15 0x55f6f98b87e3 in blink::NGBoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalOffset const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:839:3
    #16 0x55f6f98b2200 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:687:9
    #17 0x55f6f98aef80 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:535:7
    #18 0x55f6f98ad821 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:441:5
    #19 0x55f6f98bc5df in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:888:46
    #20 0x55f6f98b915a in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:852:5
    #21 0x55f6f98b23b3 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:689:9
    #22 0x55f6f98aef80 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:535:7
    #23 0x55f6f98ad821 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:441:5
    #24 0x55f6f98bc5df in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:888:46
    #25 0x55f6f98b915a in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:852:5
    #26 0x55f6f98b23b3 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:689:9
    #27 0x55f6f98aef80 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:535:7
    #28 0x55f6f98ad821 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third_party/blink/renderer/core/paint/ng/ng_box_fragment_painter.cc:441:5
    #29 0x55f6f9997d0b in blink::PaintLayerPainter::PaintFragmentWithPhase(blink::PaintPhase, blink::FragmentData const&, blink::NGPhysicalBoxFragment const*, blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:378:46
    #30 0x55f6f9996741 in blink::PaintLayerPainter::PaintWithPhase(blink::PaintPhase, blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:412:5
    #31 0x55f6f9997436 in blink::PaintLayerPainter::PaintForegroundPhases(blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:435:3
    #32 0x55f6f9994e89 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:253:7
    #33 0x55f6f9996be3 in blink::PaintLayerPainter::PaintChildren(blink::PaintLayerIteration, blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:316:35
    #34 0x55f6f9994fe9 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/paint_layer_painter.cc:265:7
    #35 0x55f6f9854a09 in blink::FramePainter::Paint(blink::GraphicsContext&, unsigned int) third_party/blink/renderer/core/paint/frame_painter.cc:91:17
    #36 0x55f6f6eedd70 in PaintFrame third_party/blink/renderer/core/frame/local_frame_view.cc:4042:23
    #37 0x55f6f6eedd70 in blink::LocalFrameView::PaintTree(blink::PaintBenchmarkMode, blink::PaintControllerCycleScope&) third_party/blink/renderer/core/frame/local_frame_view.cc:2963:7
    #38 0x55f6f6eeb33b in blink::LocalFrameView::RunPaintLifecyclePhase(blink::PaintBenchmarkMode) third_party/blink/renderer/core/frame/local_frame_view.cc:2758:22
    #39 0x55f6f6ee8d20 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third_party/blink/renderer/core/frame/local_frame_view.cc:2513:3
    #40 0x55f6f6ee6209 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/local_frame_view.cc:2318:3
    #41 0x55f6f6ee5a97 in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/local_frame_view.cc:2080:54
    #42 0x55f6f9755627 in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) third_party/blink/renderer/core/page/page_animator.cc:159:9
    #43 0x55f6f7ef489e in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1376:14
    #44 0x55f6fa7d1c95 in UpdateVisualState third_party/blink/renderer/platform/widget/widget_base.cc:891:12
    #45 0x55f6fa7d1c95 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() third_party/blink/renderer/platform/widget/widget_base.cc:0
    #46 0x55f6f13a392c in cc::LayerTreeHost::RequestMainFrameUpdate(bool) cc/trees/layer_tree_host.cc:376:12
    #47 0x55f6f15e2b87 in cc::ProxyMain::BeginMainFrame(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>) cc/trees/proxy_main.cc:278:21
    #48 0x55f6f15fdff0 in Invoke<void (cc::ProxyMain::*)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState> >), base::WeakPtr<cc::ProxyMain>, std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState> > > base/functional/bind_internal.h:647:12
    #49 0x55f6f15fdff0 in MakeItSo<void (cc::ProxyMain::*)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState> > > > base/functional/bind_internal.h:848:5
    #50 0x55f6f15fdff0 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunImpl<void (cc::ProxyMain::*)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, 0ul, 1ul>(void (cc::ProxyMain::*&&)(std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default_delete<cc::BeginMainFrameAndCommitState>>>&&, std::Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/functional/bind_internal.h:920:12
    #51 0x55f6ec181049 in Run base/functional/callback.h:145:12
    #52 0x55f6ec181049 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:133:32
    #53 0x55f6ec1c718d in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:443:29)> base/task/common/task_annotator.h:72:5
    #54 0x55f6ec1c718d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:441:21
    #55 0x55f6ec1c620a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:297:30
    #56 0x55f6ec1c8494 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0
    #57 0x55f6ec08a1e7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:40:55
    #58 0x55f6ec1c8fc0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:600:12
    #59 0x55f6ec11035e in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #60 0x55f701ca9e32 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:313:16
    #61 0x55f6eaed66e3 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:679:14
    #62 0x55f6eaed8790 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:761:12
    #63 0x55f6eaeda958 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1104:10
    #64 0x55f6eaed320c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:342:36
    #65 0x55f6eaed3819 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:370:10
    #66 0x55f6dbe1eb37 in ChromeMain chrome/app/chrome_main.cc:175:12
    #67 0x7ff711ffb082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/libc-start.c:308:16
0x60a0000e8c40 is located 64 bytes inside of 96-byte region [0x60a0000e8c00,0x60a0000e8c60)
freed by thread T0 (chrome) here:
    #0 0x55f6dbdeb9a6 in free third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:52:3
    #1 0x55f6f6fc186a in operator delete third_party/blink/renderer/platform/wtf/ref_counted.h:44:3
    #2 0x55f6f6fc186a in DeleteInternal<blink::ComputedStyleBase::StyleBackgroundData> third_party/blink/renderer/platform/wtf/ref_counted.h:54:5
    #3 0x55f6f6fc186a in Destruct third_party/blink/renderer/platform/wtf/ref_counted.h:35:5
    #4 0x55f6f6fc186a in Release base/memory/ref_counted.h:353:7
    #5 0x55f6f6fc186a in Release base/memory/scoped_refptr.h:361:8
    #6 0x55f6f6fc186a in ~scoped_refptr base/memory/scoped_refptr.h:261:7
    #7 0x55f6f6fc186a in ~DataRef third_party/blink/renderer/core/style/data_ref.h:33:7
    #8 0x55f6f6fc186a in blink::ComputedStyleBase::~ComputedStyleBase() gen/third_party/blink/renderer/core/style/computed_style_base.h:12993:32
    #9 0x55f6faccedd0 in ~ComputedStyle third_party/blink/renderer/core/style/computed_style.h:211:7
    #10 0x55f6faccedd0 in DeleteInternal<blink::ComputedStyle> third_party/blink/renderer/platform/wtf/ref_counted.h:54:5
    #11 0x55f6faccedd0 in Destruct third_party/blink/renderer/platform/wtf/ref_counted.h:35:5
    #12 0x55f6faccedd0 in Release base/memory/ref_counted.h:353:7
    #13 0x55f6faccedd0 in Release base/memory/scoped_refptr.h:361:8
    #14 0x55f6faccedd0 in ~scoped_refptr base/memory/scoped_refptr.h:261:7
    #15 0x55f6faccedd0 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4541:1
    #16 0x55f6facc98f3 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:3970:20
    #17 0x55f6faa1a4a8 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/container_node.cc:1386:26
    #18 0x55f6facca74e in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4073:7
    #19 0x55f6faa1a4a8 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/container_node.cc:1386:26
    #20 0x55f6facca74e in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4073:7
    #21 0x55f6f7481d4c in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/css/style_engine.cc:2783:20
    #22 0x55f6f7484eef in blink::StyleEngine::RecalcStyle() third_party/blink/renderer/core/css/style_engine.cc:2811:3
    #23 0x55f6f74859ea in blink::StyleEngine::UpdateStyleAndLayoutTree() third_party/blink/renderer/core/css/style_engine.cc:2918:7
    #24 0x55f6faa49e4a in blink::Document::UpdateStyle() third_party/blink/renderer/core/dom/document.cc:2265:20
    #25 0x55f6faa478f0 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument() third_party/blink/renderer/core/dom/document.cc:2214:3
    #26 0x55f6f6ef2ae1 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3292:28
    #27 0x55f6f6edc623 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3243:18
    #28 0x55f6faa48413 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2564:17
    #29 0x55f6f82422d1 in blink::HTMLPlugInElement::LayoutEmbeddedContentForJSBindings() const third_party/blink/renderer/core/html/html_plugin_element.cc:483:17
    #30 0x55f6f82415c7 in PluginEmbeddedContentView third_party/blink/renderer/core/html/html_plugin_element.cc:409:11
    #31 0x55f6f82415c7 in blink::HTMLPlugInElement::PluginWrapper() third_party/blink/renderer/core/html/html_plugin_element.cc:385:16
    #32 0x55f6fb711d85 in GetScriptableObjectProperty<blink::V8HTMLEmbedElement> third_party/blink/renderer/bindings/core/v8/custom/v8_html_plugin_element_custom.cc:67:42
    #33 0x55f6fb711d85 in blink::V8HTMLEmbedElement::NamedPropertyGetterCustom(WTF::AtomicString const&, v8::PropertyCallbackInfo<v8::Value> const&) third_party/blink/renderer/bindings/core/v8/custom/v8_html_plugin_element_custom.cc:138:3
    #34 0x55f6fb70b9b4 in blink::V8HTMLEmbedElement::NamedPropertyGetterCallback(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_html_embed_element.cc:91:1
    #35 0x55f6e1721739 in BasicCallNamedGetterCallback v8/src/api/api-arguments-inl.h:201:3
    #36 0x55f6e1721739 in v8::internal::PropertyCallbackArguments::CallNamedGetter(v8::internal::Handle<v8::internal::InterceptorInfo>, v8::internal::Handle<v8::internal::Name>) v8/src/api/api-arguments-inl.h:181:10
    #37 0x55f6e1cd4bef in v8::internal::(anonymous namespace)::GetPropertyWithInterceptorInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::InterceptorInfo>, bool*) v8/src/objects/js-objects.cc:1241:19
    #38 0x55f6e1e86371 in v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool) v8/src/objects/objects.cc:1177:9
    #39 0x55f6e16d3806 in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool, v8::internal::Handle<v8::internal::Object>) v8/src/ic/ic.cc:507:5
    #40 0x55f6e16f8193 in __RT_impl_Runtime_LoadNoFeedbackIC_Miss v8/src/ic/ic.cc:2671:3
    #41 0x55f6e16f8193 in v8::internal::Runtime_LoadNoFeedbackIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2656:1
    #25 0x55f67ff15a37  (<unknown module>)
    #26 0x55f67ffd2cd2  (<unknown module>)
    #27 0x55f67fe8b82b  (<unknown module>)
    #28 0x55f67fec43b7  (<unknown module>)
    #29 0x55f67ff6f370  (<unknown module>)
previously allocated by thread T0 (chrome) here:
    #0 0x55f6dbdebc4e in malloc third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:69:3
    #1 0x55f6ec565817 in AllocWithFlagsInternal base/allocator/partition_allocator/partition_root.h:1789:49
    #2 0x55f6ec565817 in AllocWithFlags base/allocator/partition_allocator/partition_root.h:1766:10
    #3 0x55f6ec565817 in partition_alloc::PartitionRoot<true>::Alloc(unsigned long, char const*) base/allocator/partition_allocator/partition_root.h:2119:10
    #4 0x55f6fa0c5ebf in operator new third_party/blink/renderer/platform/wtf/ref_counted.h:44:3
    #5 0x55f6fa0c5ebf in Copy gen/third_party/blink/renderer/core/style/computed_style_base.h:8526:29
    #6 0x55f6fa0c5ebf in Access third_party/blink/renderer/core/style/data_ref.h:44:22
    #7 0x55f6fa0c5ebf in MutableBackgroundInternal gen/third_party/blink/renderer/core/style/computed_style_base.h:8823:29
    #8 0x55f6fa0c5ebf in AccessBackgroundLayers third_party/blink/renderer/core/style/computed_style.h:2662:48
    #9 0x55f6fa0c5ebf in blink::css_longhand::BackgroundAttachment::ApplyInitial(blink::StyleResolverState&) const gen/third_party/blink/renderer/core/css/properties/longhands.cc:1619:43
    #10 0x55f6fafcc669 in blink::StyleBuilder::ApplyProperty(blink::CSSProperty const&, blink::StyleResolverState&, blink::ScopedCSSValue const&) third_party/blink/renderer/core/css/resolver/style_builder.cc:0
    #11 0x55f6fafd66e8 in blink::StyleCascade::LookupAndApplyDeclaration(blink::CSSProperty const&, blink::CascadePriority*, blink::CascadeResolver&) third_party/blink/renderer/core/css/resolver/style_cascade.cc:677:3
    #12 0x55f6fafd0588 in blink::StyleCascade::ApplyMatchResult(blink::CascadeResolver&) third_party/blink/renderer/core/css/resolver/style_cascade.cc:528:5
    #13 0x55f6fafcd1a0 in blink::StyleCascade::Apply(blink::CascadeFilter) third_party/blink/renderer/core/css/resolver/style_cascade.cc:213:3
    #14 0x55f6fafa5518 in blink::StyleResolver::CascadeAndApplyMatchedProperties(blink::StyleResolverState&, blink::StyleCascade&) third_party/blink/renderer/core/css/resolver/style_resolver.cc:2133:3
    #15 0x55f6fafa46c7 in blink::StyleResolver::ApplyBaseStyleNoCache(blink::Element*, blink::StyleRecalcContext const&, blink::StyleRequest const&, blink::StyleResolverState&, blink::StyleCascade&) third_party/blink/renderer/core/css/resolver/style_resolver.cc:1318:3
    #16 0x55f6faf9e7b3 in blink::StyleResolver::ApplyBaseStyle(blink::Element*, blink::StyleRecalcContext const&, blink::StyleRequest const&, blink::StyleResolverState&, blink::StyleCascade&) third_party/blink/renderer/core/css/resolver/style_resolver.cc:1464:3
    #17 0x55f6faf9cd52 in blink::StyleResolver::ResolveStyle(blink::Element*, blink::StyleRecalcContext const&, blink::StyleRequest const&) third_party/blink/renderer/core/css/resolver/style_resolver.cc:944:3
    #18 0x55f6facc78d9 in blink::Element::OriginalStyleForLayoutObject(blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:3849:43
    #19 0x55f6facc6c74 in blink::Element::StyleForLayoutObject(blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:3811:13
    #20 0x55f6faccc554 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4294:17
    #21 0x55f6facc98f3 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:3970:20
    #22 0x55f6faa1a4a8 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/container_node.cc:1386:26
    #23 0x55f6facca74e in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4073:7
    #24 0x55f6faa1a4a8 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/container_node.cc:1386:26
    #25 0x55f6facca74e in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/dom/element.cc:4073:7
    #26 0x55f6f7481d4c in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third_party/blink/renderer/core/css/style_engine.cc:2783:20
    #27 0x55f6f7484eef in blink::StyleEngine::RecalcStyle() third_party/blink/renderer/core/css/style_engine.cc:2811:3
    #28 0x55f6f74859ea in blink::StyleEngine::UpdateStyleAndLayoutTree() third_party/blink/renderer/core/css/style_engine.cc:2918:7
    #29 0x55f6faa49e4a in blink::Document::UpdateStyle() third_party/blink/renderer/core/dom/document.cc:2265:20
    #30 0x55f6faa478f0 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument() third_party/blink/renderer/core/dom/document.cc:2214:3
    #31 0x55f6f6ef2ae1 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third_party/blink/renderer/core/frame/local_frame_view.cc:3292:28
    #32 0x55f6f6edc623 in blink::LocalFrameView::UpdateStyleAndLayout() third_party/blink/renderer/core/frame/local_frame_view.cc:3243:18
    #33 0x55f6faa48413 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2564:17
    #34 0x55f6faa4daf3 in blink::Document::EnsurePaintLocationDataValidForNode(blink::Node const*, blink::DocumentUpdateReason) third_party/blink/renderer/core/dom/document.cc:2664:3
    #35 0x55f6f81c63b4 in blink::HTMLElement::offsetTopForBinding() third_party/blink/renderer/core/html/html_element.cc:1800:17
    #36 0x55f700f12d23 in blink::(anonymous namespace)::v8_html_element::OffsetTopAttributeGetCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_html_element.cc:625:39
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds_media_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-1059803/chrome+0x2985f2a9) (BuildId: 39eba3b1f2cd00e5)
Shadow bytes around the buggy address:
  0x60a0000e8980: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x60a0000e8a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60a0000e8a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60a0000e8b00: fa fa fa fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x60a0000e8b80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
=>0x60a0000e8c00: fd fd fd fd fd fd fd fd[fd]fd fd fd fa fa fa fa
  0x60a0000e8c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60a0000e8d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x60a0000e8d80: fa fa fa fa fa fa fa fa fa fa fa fa 00 00 00 00
  0x60a0000e8e00: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
  0x60a0000e8e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
==1==ABORTING

### cl...@chromium.org (2022-10-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6237578485497856

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 7
Crash Address: 0x60a0000e8c40
Crash State:
  blink::BoxPainterBase::PaintFillLayer
  blink::BoxPainterBase::PaintFillLayers
  blink::BoxPainter::PaintBoxDecorationBackgroundWithRect
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=1059803

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6237578485497856

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### fl...@chromium.org (2022-10-17)

[Comment Deleted]

### fl...@chromium.org (2022-10-17)

Kevin, can you have a look at this?

### cl...@chromium.org (2022-10-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2022-10-17)

ClusterFuzz testcase 6237578485497856 appears to be flaky, updating reproducibility label.

### pd...@chromium.org (2022-10-19)

Paint worklet is owned by canvas and the fix is outside paint code so I'm removing Blink>Paint for bug triaging purposes.

[Monorail components: -Blink>Paint]

### cl...@chromium.org (2022-10-20)

ClusterFuzz testcase 6237578485497856 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1061042:1061049

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### fl...@chromium.org (2022-10-25)

[Empty comment from Monorail migration]

### fl...@chromium.org (2022-10-25)

I suspect this is (now) fixed by https://chromium-review.googlesource.com/c/chromium/src/+/3975449 . The previous detected fix may have closed the particular path but having a microtask queue for paintworklets should prevent the underlying issue.

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations on yet another one this week! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in providing updated test cases to help provide improved reproduction! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1303597?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Canvas, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059000)*
