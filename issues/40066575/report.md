# Security: Heap-buffer-overflow in CompositorFrameSinkSupport::DidPresentCompositorFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40066575](https://issues.chromium.org/issues/40066575) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU, Internals>Services>Viz |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ky...@chromium.org |
| **Created** | 2023-06-28 |
| **Bounty** | $15,000.00 |

## Description

reproduce:
1. apply change.diff and compile Chromium wiht ASAN
2. start a server at the folder of poc.html and video.html  `python2 -m SimpleHTTPServer 8080`
3. `./Chrome --no-sandbox --disable-popup-blocking http://127.0.0.1:8080/poc.html`

**This is a bug that affects GPU process with a compromised render. It DOES NOT need any user interactions.**


1. Analysis:

`CompositorFrameSinkSupport::DidPresentCompositorFrame` will find `frame_token` in flat_map `pending_received_frame_times_`[1], but it doesn't check whether the iterator is equal to end. The use of end->second will cause Heap overflow[2]. 

In order to ensure that the `frame_token` does not exist in the flat_map, we patched the render to send a `frame_token` with the same ID. In my poc, I use `video` HTMLElement to send a controllable `CompositorFrame` to the compositor service. 

```
void CompositorFrameSinkSupport::DidPresentCompositorFrame(
    uint32_t frame_token,
    base::TimeTicks draw_start_timestamp,
    const gfx::SwapTimings& swap_timings,
    const gfx::PresentationFeedback& feedback) {
  DCHECK(frame_token);
  DCHECK((feedback.flags & gfx::PresentationFeedback::kFailure) ||
         (!draw_start_timestamp.is_null() && !swap_timings.is_null()));

  DCHECK_LE(pending_received_frame_times_.size(), 25u);
  auto received_frame_timestamp =
      pending_received_frame_times_.find(frame_token);
  DCHECK(received_frame_timestamp != pending_received_frame_times_.end());

  FrameTimingDetails details;
  details.received_compositor_frame_timestamp =
      received_frame_timestamp->second;
      [...]
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/compositor_frame_sink_support.cc;l=799;drc=7f7d944b6a0014e202d36eb554d201d0ddea9092;bpv=1;bpt=0
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/compositor_frame_sink_support.cc;l=804;drc=7f7d944b6a0014e202d36eb554d201d0ddea9092;bpv=1;bpt=0


2. Bisect
17c336c1b501e62e376a5d55d7763f940c8624de
https://chromium-review.googlesource.com/c/chromium/src/+/1705158

Chrome Stabl 78.0.3904.70 introcuded this vulnerability pattern, wihich didn't check the result and maybe use `end->second` directly.

```
void CompositorFrameSinkSupport::DidPresentCompositorFrame(
    uint32_t presentation_token,
    const gfx::PresentationFeedback& feedback) {
  DCHECK(presentation_token);

  FrameTimingDetails details;
  details.presentation_feedback = feedback;

  DCHECK_LT(received_compositor_frame_times_.size(), 25u);
  auto received_compositor_frame_time =
      received_compositor_frame_times_.find(presentation_token);
  DCHECK(received_compositor_frame_time !=
         received_compositor_frame_times_.end());
  details.received_compositor_frame_timestamp =
      received_compositor_frame_time->second;
[...]
}
```


3. Suggested Patch：
Change the `DCHECK` to `CHECK` [3].

[3] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/compositor_frame_sink_support.cc;l=800;drc=7f7d944b6a0014e202d36eb554d201d0ddea9092;bpv=1;bpt=0

4. Reporter credit:
Guang and Weipeng Jiang of VRI 



## Attachments

- [poc.html](attachments/poc.html) (text/plain, 316 B)
- [video.html](attachments/video.html) (text/plain, 138 B)
- [change.diff](attachments/change.diff) (text/plain, 752 B)
- [flower.webm](attachments/flower.webm) (video/webm, 541.1 KB)

## Timeline

### [Deleted User] (2023-06-28)

[Empty comment from Monorail migration]

### hi...@gmail.com (2023-06-29)

append the asan log

=================================================================
==2964468==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x5020000426a8 at pc 0x563e61c2a383 bp 0x7f24a35a3790 sp 0x7f24a35a3788
READ of size 8 at 0x5020000426a8 thread T26 (VizCompositorTh)
[2964095:2964146:0620/223631.536151:ERROR:ssl_client_socket_impl.cc(980)] handshake failed; returned -1, SSL error code 1, net_error -101
    #0 0x563e61c2a382 in viz::CompositorFrameSinkSupport::DidPresentCompositorFrame(unsigned int, base::TimeTicks, gfx::SwapTimings const&, gfx::PresentationFeedback const&) components/viz/service/frame_sinks/compositor_frame_sink_support.cc:795:47
    #1 0x563e61e4df47 in viz::Surface::PresentationHelper::DidPresent(base::TimeTicks, gfx::SwapTimings const&, gfx::PresentationFeedback const&) components/viz/service/surfaces/surface.cc:74:22
    #2 0x563e61c6a647 in OnPresent components/viz/service/display/display.cc:311:26
    #3 0x563e61c6a647 in viz::Display::DidReceivePresentationFeedback(gfx::PresentationFeedback const&) components/viz/service/display/display.cc:1168:29
    #4 0x563e61bcf2f2 in viz::SoftwareOutputSurface::SwapBuffersCallback(base::TimeTicks, gfx::Size const&) components/viz/service/display_embedder/software_output_surface.cc:105:12
    #5 0x563e61bd25f3 in Invoke<void (viz::SoftwareOutputSurface::*)(base::TimeTicks, const gfx::Size &), const base::WeakPtr<viz::SoftwareOutputSurface> &, base::TimeTicks, const gfx::Size &> base/functional/bind_internal.h:746:12
    #6 0x563e61bd25f3 in MakeItSo<void (viz::SoftwareOutputSurface::*)(base::TimeTicks, const gfx::Size &), std::__Cr::tuple<base::WeakPtr<viz::SoftwareOutputSurface>, base::TimeTicks>, const gfx::Size &> base/functional/bind_internal.h:953:5
    #7 0x563e61bd25f3 in void base::internal::Invoker<base::internal::BindState<void (viz::SoftwareOutputSurface::*)(base::TimeTicks, gfx::Size const&), base::WeakPtr<viz::SoftwareOutputSurface>, base::TimeTicks>, void (gfx::Size const&)>::RunImpl<void (viz::SoftwareOutputSurface::*)(base::TimeTicks, gfx::Size const&), std::__Cr::tuple<base::WeakPtr<viz::SoftwareOutputSurface>, base::TimeTicks>, 0ul, 1ul>(void (viz::SoftwareOutputSurface::*&&)(base::TimeTicks, gfx::Size const&), std::__Cr::tuple<base::WeakPtr<viz::SoftwareOutputSurface>, base::TimeTicks>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, gfx::Size const&) base/functional/bind_internal.h:1025:12
    #8 0x563e355d1a9a in Run base/functional/callback.h:152:12
    #9 0x563e355d1a9a in Invoke<base::OnceCallback<void (const gfx::Size &)>, gfx::Size> base/functional/bind_internal.h:849:49
    #10 0x563e355d1a9a in MakeItSo<base::OnceCallback<void (const gfx::Size &)>, std::__Cr::tuple<gfx::Size> > base/functional/bind_internal.h:925:12
    #11 0x563e355d1a9a in RunImpl<base::OnceCallback<void (const gfx::Size &)>, std::__Cr::tuple<gfx::Size>, 0UL> base/functional/bind_internal.h:1025:12
    #12 0x563e355d1a9a in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (gfx::Size const&)>, gfx::Size>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:976:12
    #13 0x563e4c386f45 in Run base/functional/callback.h:152:12
    #14 0x563e4c386f45 in DispatchShmCompletionEvent ui/base/x/x11_shm_image_pool.cc:275:30
    #15 0x563e4c386f45 in ui::XShmImagePool::OnEvent(x11::Event const&) ui/base/x/x11_shm_image_pool.cc:288:5
    #16 0x563e343324c3 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14
    #17 0x563e34331cd8 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3
    #18 0x563e34330f63 in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #19 0x563e4c3f4426 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:57:15
    #20 0x7f24d187b04d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5204d) (BuildId: 5fdb313daf182a33a858ba2cc945211b11d34561)

0x5020000426a8 is located 8 bytes before 8-byte region [0x5020000426b0,0x5020000426b8)
allocated by thread T26 (VizCompositorTh) here:
    #0 0x563e328e58ad in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x563e61e8d5c3 in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:268:10
    #2 0x563e61e8d5c3 in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:294:10
    #3 0x563e61e8d5c3 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:114:38
    #4 0x563e61e8d5c3 in __allocate_at_least<std::__Cr::allocator<viz::SurfaceAllocationGroup *> > buildtools/third_party/libc++/trunk/include/__memory/allocate_at_least.h:55:19
    #5 0x563e61e8d5c3 in __split_buffer buildtools/third_party/libc++/trunk/include/__split_buffer:358:29
    #6 0x563e61e8d5c3 in void std::__Cr::vector<viz::SurfaceAllocationGroup*, std::__Cr::allocator<viz::SurfaceAllocationGroup*>>::__push_back_slow_path<viz::SurfaceAllocationGroup*>(viz::SurfaceAllocationGroup*&&) buildtools/third_party/libc++/trunk/include/vector:1540:49
    #7 0x563e61e7ee4c in push_back buildtools/third_party/libc++/trunk/include/vector:1572:9
    #8 0x563e61e7ee4c in viz::SurfaceManager::GetOrCreateAllocationGroupForSurfaceId(viz::SurfaceId const&) components/viz/service/surfaces/surface_manager.cc:577:69
    #9 0x563e61e7e854 in viz::SurfaceManager::CreateSurface(base::WeakPtr<viz::SurfaceClient>, viz::SurfaceInfo const&) components/viz/service/surfaces/surface_manager.cc:114:7
    #10 0x563e61c2e01d in viz::CompositorFrameSinkSupport::MaybeSubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, absl::optional<viz::HitTestRegionList>, unsigned long, base::OnceCallback<void (std::__Cr::vector<viz::ReturnedResource, std::__Cr::allocator<viz::ReturnedResource>>)>) components/viz/service/frame_sinks/compositor_frame_sink_support.cc:677:41
    #11 0x563e61c1d002 in viz::CompositorFrameSinkImpl::SubmitCompositorFrameInternal(viz::LocalSurfaceId const&, viz::CompositorFrame, absl::optional<viz::HitTestRegionList>, unsigned long, base::OnceCallback<void (std::__Cr::vector<viz::ReturnedResource, std::__Cr::allocator<viz::ReturnedResource>>)>) components/viz/service/frame_sinks/compositor_frame_sink_impl.cc:167:33
    #12 0x563e61c1cc25 in viz::CompositorFrameSinkImpl::SubmitCompositorFrame(viz::LocalSurfaceId const&, viz::CompositorFrame, absl::optional<viz::HitTestRegionList>, unsigned long) components/viz/service/frame_sinks/compositor_frame_sink_impl.cc:145:3
    #13 0x563e381872ef in viz::mojom::CompositorFrameSinkStubDispatch::Accept(viz::mojom::CompositorFrameSink*, mojo::Message*) gen/services/viz/public/mojom/compositing/compositor_frame_sink.mojom.cc:1175:13
    #14 0x563e4a65eb34 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54
    #15 0x563e4a680c16 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #16 0x563e4a664ca6 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
    #17 0x563e4a692600 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1096:42
    #18 0x563e4a68ff7e in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
    #19 0x563e4a680c16 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #20 0x563e4a653719 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:550:49
    #21 0x563e4a6556c2 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:607:14
    #22 0x563e4a658fef in Invoke<void (mojo::Connector::*)(unsigned int), mojo::Connector *, unsigned int> base/functional/bind_internal.h:746:12
    #23 0x563e4a658fef in MakeItSo<void (mojo::Connector::*const &)(unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> base/functional/bind_internal.h:925:12
    #24 0x563e4a658fef in RunImpl<void (mojo::Connector::*const &)(unsigned int), const std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> base/functional/bind_internal.h:1025:12
    #25 0x563e4a658fef in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:989:12
    #26 0x563e38392e95 in Run base/functional/callback.h:333:12
    #27 0x563e38392e95 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.h:192:14
    #28 0x563e38393134 in Invoke<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:636:12
    #29 0x563e38393134 in MakeItSo<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind_internal.h:925:12
    #30 0x563e38393134 in RunImpl<void (*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::__Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind_internal.h:1025:12
    #31 0x563e38393134 in base::internal::Invoker<base::internal::BindState<void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:989:12
    #32 0x563e4a6fd0cb in Run base/functional/callback.h:333:12
    #33 0x563e4a6fd0cb in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:278:14
    #34 0x563e4a6fe0f0 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> base/functional/bind_internal.h:746:12
    #35 0x563e4a6fe0f0 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > base/functional/bind_internal.h:953:5
    #36 0x563e4a6fe0f0 in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) base/functional/bind_internal.h:1025:12
    #37 0x563e474ff019 in Run base/functional/callback.h:152:12
    #38 0x563e474ff019 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:186:34
    #39 0x563e475796c8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:488:11)> base/task/common/task_annotator.h:89:5
    #40 0x563e475796c8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:23
    #41 0x563e4757824b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:41
    #42 0x563e4757a9ee in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #43 0x563e4772cf98 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:646:46
    #44 0x563e477307e6 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:274:43
    #45 0x7f24d187b17c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c) (BuildId: 5fdb313daf182a33a858ba2cc945211b11d34561)

Thread T26 (VizCompositorTh) created by T0 (chrome) here:
    #0 0x563e3289d5aa in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:208:3
    #1 0x563e4766f277 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:146:13
    #2 0x563e4760b394 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:215:26
    #3 0x563e43e342bd in CreateAndStartCompositorThread components/viz/service/main/viz_compositor_thread_runner_impl.cc:81:3
    #4 0x563e43e342bd in viz::VizCompositorThreadRunnerImpl::VizCompositorThreadRunnerImpl() components/viz/service/main/viz_compositor_thread_runner_impl.cc:90:15
    #5 0x563e43e3a1ff in make_unique<viz::VizCompositorThreadRunnerImpl> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:686:30
    #6 0x563e43e3a1ff in viz::VizMainImpl::VizMainImpl(viz::VizMainImpl::Delegate*, viz::VizMainImpl::ExternalDependencies, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>) components/viz/service/main/viz_main_impl.cc:85:9
    #7 0x563e61a964c7 in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, content::ChildThreadImpl::Options, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>) content/gpu/gpu_child_thread.cc:124:7
    #8 0x563e61a96142 in content::GpuChildThread::GpuChildThread(base::RepeatingCallback<void ()>, std::__Cr::unique_ptr<gpu::GpuInit, std::__Cr::default_delete<gpu::GpuInit>>) content/gpu/gpu_child_thread.cc:110:7
    #9 0x563e61a94637 in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:370:11
    #10 0x563e43ebd47d in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:676:14
    #11 0x563e43ebf884 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:776:12
    #12 0x563e43ec3a57 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1140:10
    #13 0x563e43eba867 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:326:36
    #14 0x563e43ebb09e in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:343:10
    #15 0x563e328e8447 in ChromeMain chrome/app/chrome_main.cc:187:12
    #16 0x7f24d018e082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-buffer-overflow components/viz/service/frame_sinks/compositor_frame_sink_support.cc:795:47 in viz::CompositorFrameSinkSupport::DidPresentCompositorFrame(unsigned int, base::TimeTicks, gfx::SwapTimings const&, gfx::PresentationFeedback const&)
Shadow bytes around the buggy address:
  0x502000042400: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042480: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fa
  0x502000042500: f7 fa fd fd f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042580: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042600: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
=>0x502000042680: f7 fa 00 00 f7[fa]00 fa f7 fa 00 fa f7 fa fd fa
  0x502000042700: f7 fa fd fd f7 fa 00 00 f7 fa 00 fa f7 fa fd fd
  0x502000042780: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042800: f7 fa 00 fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042880: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x502000042900: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
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

==2964468==ADDITIONAL INFO

==2964468==Note: Please include this section with the ASan report.
Task trace:


==2964468==END OF ADDITIONAL INFO
==2964468==ABORTING

### es...@chromium.org (2023-06-30)

Thanks for the report. I can't reproduce this. I see a lot of error messages:
'SetError: {code=4, message="MEDIA_ELEMENT_ERROR: Media load rejected by URL safety check"}'

Is there any other information you can provide to help reproduce?

### es...@chromium.org (2023-06-30)

[Comment Deleted]

### es...@chromium.org (2023-06-30)

Ah, ok, it looks like to reproduce you have to host the poc at exactly 127.0.0.1:8080 (e.g. localhost doesn't work), and disable DCHECKs.

components/viz owners, can you please take a look? Thanks!

[Monorail components: Internals>GPU Internals>Services>Viz]

### [Deleted User] (2023-06-30)

[Empty comment from Monorail migration]

### hi...@gmail.com (2023-06-30)

You have to build chromium with asan to reproduce the issue, my build configuration file args.gn is as follows:

use_libfuzzer = true
is_asan = true
is_debug = false
enable_nacl = false
dcheck_always_on = false
enable_ipc_fuzzer = true

enable_full_stack_frames_for_profiling = true
v8_enable_verify_heap = true

### vm...@chromium.org (2023-06-30)

Kyle, can you triage this please?

### [Deleted User] (2023-06-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hi...@gmail.com (2023-07-07)

[Comment Deleted]

### hi...@gmail.com (2023-07-11)

Hello, any update of this issue?

### ky...@chromium.org (2023-07-11)

Not verifying the uniqueness of frame_token from clients and then assuming they are unique seems like a legitimate problem from a malicous renderer. I will land a CL to convert DCHECKs into CHECKs in CompositorFrameSinkSupport::DidPresentCompositorFrame(). That fixes the immediate security concerns.

Although, maybe we should verify uniqueness of frame_token in CompositorFrameSinkSupport::MaybeSubmitCompositorFrame() too? It can reject CFs where the frame_token is not monotonically increasing. Wrap around after frame_token passes UINT32_MAX needs to be handled though.

### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b62ab5a88379b37dbc712171fdfd5530b99a7a9

commit 9b62ab5a88379b37dbc712171fdfd5530b99a7a9
Author: kylechar <kylechar@chromium.org>
Date: Wed Jul 12 13:35:46 2023

Ensure unique entries in frame_timing_details_

CompositorFrameSinkSupport::DidPresentCompositorFrame() keeps
|frame_timing_details_| map keyed on CompositorFrame frame_tokens. These
are supposed to be unique but a malicious renderer could violate that
assumption. Convert some DCHECKs into CHECKs to guard against problems
related to this.

Bug: 1458819
Change-Id: Ib0b9551d18ea421957e0dce49a2593043f4abb12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4673638
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1169287}

[modify] https://crrev.com/9b62ab5a88379b37dbc712171fdfd5530b99a7a9/components/viz/service/frame_sinks/compositor_frame_sink_support.cc


### ky...@chromium.org (2023-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74e09654430d9696d1d8710633e6781d21169a74

commit 74e09654430d9696d1d8710633e6781d21169a74
Author: kylechar <kylechar@chromium.org>
Date: Thu Jul 13 18:15:59 2023

Ensure unique entries in frame_timing_details_

CompositorFrameSinkSupport::DidPresentCompositorFrame() keeps
|frame_timing_details_| map keyed on CompositorFrame frame_tokens. These
are supposed to be unique but a malicious renderer could violate that
assumption. Convert some DCHECKs into CHECKs to guard against problems
related to this.

(cherry picked from commit 9b62ab5a88379b37dbc712171fdfd5530b99a7a9)

Bug: 1458819
Change-Id: Ib0b9551d18ea421957e0dce49a2593043f4abb12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4673638
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1169287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4682626
Cr-Commit-Position: refs/branch-heads/5845@{#469}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/74e09654430d9696d1d8710633e6781d21169a74/components/viz/service/frame_sinks/compositor_frame_sink_support.cc


### ky...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ky...@chromium.org (2023-07-14)

1. No.
2. No.

### am...@chromium.org (2023-07-15)

Hi kylechar@ -- in the future, please avoid manually requesting merge reviews for security bugs. All you need to do is closed the bug as Fixed and the friendly neighborhood sheriffbot will take care of adding merge labels and ensure the issue goes into our security merge review queue and can be evaluated for backmerge to all affected release branches as soon as possible. 
This is important to ensure we ship security fixes to affected channels in a timely fashion and reduce the risk for n-day exploitation security bugs whose fixes have not shipped to Beta and Stable. 

This is a high severity security fix for a security bug going back to at least 114, which is current Stable but will be promoted to Extended Stable on Tuesday, when Stable/115 is shipped at that time. 

I have added the merge review labels so I can revisit this issue for merge review for 115/Stable and 114/Extended a bit later. 


### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### rz...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-17)

M115 and M114 merges approved. 
Please merge this fix to M115 / branch 5790 and M114 / branch 5735 at your earliest convenience. Thank you! 

### va...@chromium.org (2023-07-17)

Kyle is on leave now, I can take care of merges 

### va...@chromium.org (2023-07-17)

https://chromium-review.googlesource.com/c/chromium/src/+/4690443 and https://chromium-review.googlesource.com/c/chromium/src/+/4689943

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33120ee46273cd7ab62a8e87ed509bad225eed16

commit 33120ee46273cd7ab62a8e87ed509bad225eed16
Author: kylechar <kylechar@chromium.org>
Date: Mon Jul 17 22:17:48 2023

Ensure unique entries in frame_timing_details_

CompositorFrameSinkSupport::DidPresentCompositorFrame() keeps
|frame_timing_details_| map keyed on CompositorFrame frame_tokens. These
are supposed to be unique but a malicious renderer could violate that
assumption. Convert some DCHECKs into CHECKs to guard against problems
related to this.

(cherry picked from commit 9b62ab5a88379b37dbc712171fdfd5530b99a7a9)

Bug: 1458819
Change-Id: Ib0b9551d18ea421957e0dce49a2593043f4abb12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4673638
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1169287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4690443
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#1740}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/33120ee46273cd7ab62a8e87ed509bad225eed16/components/viz/service/frame_sinks/compositor_frame_sink_support.cc


### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d0c1b8954a1be016b8a9725b818b750998fb842f

commit d0c1b8954a1be016b8a9725b818b750998fb842f
Author: kylechar <kylechar@chromium.org>
Date: Mon Jul 17 23:14:41 2023

Ensure unique entries in frame_timing_details_

CompositorFrameSinkSupport::DidPresentCompositorFrame() keeps
|frame_timing_details_| map keyed on CompositorFrame frame_tokens. These
are supposed to be unique but a malicious renderer could violate that
assumption. Convert some DCHECKs into CHECKs to guard against problems
related to this.

(cherry picked from commit 9b62ab5a88379b37dbc712171fdfd5530b99a7a9)

Bug: 1458819
Change-Id: Ib0b9551d18ea421957e0dce49a2593043f4abb12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4673638
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1169287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4689943
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1481}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/d0c1b8954a1be016b8a9725b818b750998fb842f/components/viz/service/frame_sinks/compositor_frame_sink_support.cc


### rz...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-07-18)

1. Just https://crrev.com/c/4689619
2. Low, no conflicts
3. 114, 115, 116
4. Yes

### gm...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations Guang and Weipeng Jiang! The VRP Panel has decided to award you $15,000 for this high quality report of a GPU process bug + $2,000 bonus for bisect and related information provided. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/536e3869ea425322cfadf2e847c80b373317620c

commit 536e3869ea425322cfadf2e847c80b373317620c
Author: kylechar <kylechar@chromium.org>
Date: Thu Jul 27 11:28:53 2023

[M108-LTS] Ensure unique entries in frame_timing_details_

CompositorFrameSinkSupport::DidPresentCompositorFrame() keeps
|frame_timing_details_| map keyed on CompositorFrame frame_tokens. These
are supposed to be unique but a malicious renderer could violate that
assumption. Convert some DCHECKs into CHECKs to guard against problems
related to this.

(cherry picked from commit 9b62ab5a88379b37dbc712171fdfd5530b99a7a9)

Bug: 1458819
Change-Id: Ib0b9551d18ea421957e0dce49a2593043f4abb12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4673638
Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1169287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4689619
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1495}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/536e3869ea425322cfadf2e847c80b373317620c/components/viz/service/frame_sinks/compositor_frame_sink_support.cc


### rz...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1458819?no_tracker_redirect=1

[Multiple monorail components: Internals>GPU, Internals>Services>Viz]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066575)*
