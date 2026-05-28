# Security: Security DCHECK failed in StringView

| Field | Value |
|-------|-------|
| **Issue ID** | [412265459](https://issues.chromium.org/issues/412265459) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ViewTransitions |
| **Platforms** | Linux |
| **Chrome Version** | asan-linux-release-1444497 |
| **Reporter** | su...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2025-04-21 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

I can only provide a rough POC at the moment, and I'm still trying to optimize it.

POC: see poc.html

1. fetch asan-linux-release-1444497
2. serve poc.html on port 8080
3. ./chrome --enable-experimental-web-platform-features <http://127.0.0.1:8080/poc.html>

# Problem Description

I am currently unable to determine the root cause of the bug, and I am in the process of analyzing it.

# Summary

Security: Security DCHECK failed in StringView

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
[585414:1:0421/145800.596171:FATAL:third_party/blink/renderer/platform/wtf/text/string_view.h:317] Security DCHECK failed: offset <= view.length().
    #0 0x5e415744bdc6 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4513:13
    #1 0x5e416cd3a768 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1058:7
    #2 0x5e416ccfb257 in StackTrace ./../../base/debug/stack_trace.cc:255:20
    #3 0x5e416ccfb257 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:250:28
    #4 0x5e416ca375e1 in logging::LogMessage::Flush() ./../../base/logging.cc:733:29
    #5 0x5e416ca394c9 in logging::LogMessageFatal::~LogMessageFatal() ./../../base/logging.cc:1077:3
    #6 0x5e41733aa1a3 in StringView ./../../third_party/blink/renderer/platform/wtf/text/string_view.h:0:0
    #7 0x5e41733aa1a3 in WTF::StringView::SubstringContainsOnlyWhitespaceOrEmpty(unsigned int, unsigned int) const ./../../third_party/blink/renderer/platform/wtf/text/string_view.cc:181:26
    #8 0x5e417c3c1e48 in blink::TextPainter::Paint(blink::TextFragmentPaintInfo const&, blink::TextPaintStyle const&, int, blink::AutoDarkMode const&, blink::TextPainter::ShadowMode) ./../../third_party/blink/renderer/core/paint/text_painter.cc:373:33
    #9 0x5e417c3bf6f2 in blink::TextFragmentPainter::Paint(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/text_fragment_painter.cc:494:20
    #10 0x5e417c181397 in blink::BoxFragmentPainter::PaintTextItem(blink::InlineCursor const&, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:2087:16
    #11 0x5e417c16b717 in blink::BoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::InlineCursor*) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:1908:11
    #12 0x5e417c165509 in blink::BoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, bool) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:721:9
    #13 0x5e417c25ecd8 in blink::InlineBoxFragmentPainter::Paint(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/inline_box_fragment_painter.cc:87:15
    #14 0x5e417c180b08 in blink::BoxFragmentPainter::PaintBoxItem(blink::FragmentItem const&, blink::PhysicalBoxFragment const&, blink::InlineCursor const&, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:2124:10
    #15 0x5e417c181965 in blink::BoxFragmentPainter::PaintBoxItem(blink::FragmentItem const&, blink::InlineCursor const&, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:2146:7
    #16 0x5e417c16b74d in blink::BoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::InlineCursor*) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:1913:11
    #17 0x5e417c171391 in blink::BoxFragmentPainter::PaintLineBoxChildItems(blink::InlineCursor*, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:2004:7
    #18 0x5e417c16c43b in blink::BoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:884:3
    #19 0x5e417c164e2c in blink::BoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, bool) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:726:9
    #20 0x5e417c16235b in blink::BoxFragmentPainter::PaintInternal(blink::PaintInfo const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:581:7
    #21 0x5e417c1611f0 in blink::BoxFragmentPainter::Paint(blink::PaintInfo const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:481:5
    #22 0x5e417c17218b in blink::BoxFragmentPainter::PaintBlockChild(blink::PhysicalFragmentLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>>) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:985:44
    #23 0x5e417c16e52a in blink::BoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>>) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:949:5
    #24 0x5e417c164f6e in blink::BoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, bool) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:730:9
    #25 0x5e417c16235b in blink::BoxFragmentPainter::PaintInternal(blink::PaintInfo const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:581:7
    #26 0x5e417c1611f0 in blink::BoxFragmentPainter::Paint(blink::PaintInfo const&) ./../../third_party/blink/renderer/core/paint/box_fragment_painter.cc:481:5
    #27 0x5e417c2d0da2 in blink::PaintLayerPainter::PaintFragmentWithPhase(blink::PaintPhase, blink::FragmentData const&, unsigned int, blink::PhysicalBoxFragment const*, blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:556:44
    #28 0x5e417c2cedac in blink::PaintLayerPainter::PaintWithPhase(blink::PaintPhase, blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:596:5
    #29 0x5e417c2cfc32 in blink::PaintLayerPainter::PaintForegroundPhases(blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:621:3
    #30 0x5e417c2cb30f in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:425:7
    #31 0x5e417c2cf2c4 in blink::PaintLayerPainter::PaintChildren(blink::PaintLayerIteration, blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:492:35
    #32 0x5e417c2cb423 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/paint_layer_painter.cc:437:7
    #33 0x5e417c21a9bd in blink::FramePainter::Paint(blink::GraphicsContext&, unsigned int) ./../../third_party/blink/renderer/core/paint/frame_painter.cc:67:17
    #34 0x5e417a5a6231 in PaintFrame ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3980:23
    #35 0x5e417a5a6231 in blink::LocalFrameView::PaintTree(blink::PaintBenchmarkMode, std::__Cr::optional<blink::PaintController>&) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2878:7
    #36 0x5e417a5aa61a in blink::LocalFrameView::RunPaintLifecyclePhase(blink::PaintBenchmarkMode) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2681:5
    #37 0x5e417a5a8ea1 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2386:3
    #38 0x5e417a5a49a1 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2171:3
    #39 0x5e417a5a410e in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1891:54
    #40 0x5e417c0e439e in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/page/page_animator.cc:397:9
    #41 0x5e417a70ea4c in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/web_frame_widget_impl.cc:1764:14
    #42 0x5e417d4af2ec in UpdateVisualState ./../../third_party/blink/renderer/platform/widget/widget_base.cc:1054:12
    #43 0x5e417d4af2ec in non-virtual thunk to blink::WidgetBase::UpdateVisualState() ./../../third_party/blink/renderer/platform/widget/widget_base.cc:0:0
    #44 0x5e4171f6898d in cc::LayerTreeHost::RequestMainFrameUpdate(bool) ./../../cc/trees/layer_tree_host.cc:402:12
    #45 0x5e417225f496 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) ./../../cc/trees/proxy_main.cc:297:21
    #46 0x5e4172288693 in Invoke<void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), const base::WeakPtr<cc::ProxyMain> &, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > ./../../base/functional/bind_internal.h:731:12
    #47 0x5e4172288693 in MakeItSo<void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > > > ./../../base/functional/bind_internal.h:947:5
    #48 0x5e4172288693 in RunImpl<void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >), std::__Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >, 0UL, 1UL> ./../../base/functional/bind_internal.h:1060:14
    #49 0x5e4172288693 in base::internal::Invoker<base::internal::FunctorTraits<void (cc::ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>&&, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>&&>, base::internal::BindState<true, true, false, void (cc::ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:973:12
    #50 0x5e416cb91da7 in Run ./../../base/functional/callback.h:156:12
    #51 0x5e416cb91da7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:209:34
    #52 0x5e416cc03769 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:458:11)> ./../../base/task/common/task_annotator.h:106:5
    #53 0x5e416cc03769 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:456:23
    #54 0x5e416cc0264d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330:40
    #55 0x5e416cc0449b in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #56 0x5e416ca5d274 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #57 0x5e416cc0504c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:629:12
    #58 0x5e416cb159b0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #59 0x5e4184986705 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #60 0x5e41698edb41 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:686:14
    #61 0x5e41698eeac0 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:790:12
    #62 0x5e41698f1346 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1155:10
    #63 0x5e41698eb90c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:359:36
    #64 0x5e41698ebe2c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:372:10
    #65 0x5e41574e0940 in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #66 0x73218182a1ca in __libc_init_first ??:?
    #67 0x73218182a28b in __libc_start_main ??:0:0
    #68 0x5e415740502a in _start ??:0:0
Task trace:
    #0 0x5e417227e8ee in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/proxy_impl.cc:767:7
    #1 0x5e4172260732 in cc::ProxyMain::BeginMainFrame(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState, std::__Cr::default_delete<cc::BeginMainFrameAndCommitState>>) ./../../cc/trees/proxy_main.cc:473:9
    #2 0x5e417227e8ee in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) ./../../cc/trees/proxy_impl.cc:767:7
    #3 0x5e4172297b9a in cc::Scheduler::PostPendingBeginFrameTask() ./../../cc/scheduler/scheduler.cc:367:28
    #4 0x5e417229bd34 in cc::Scheduler::ScheduleBeginImplFrameDeadline() ./../../cc/scheduler/scheduler.cc:799:9
Crash keys:
  "view-count" = "1"
  "loaded-origin-0" = "https://127.0.0.1:40923"
  "web-frame-count" = "2"
  "gpu-gl-renderer" = "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver-5.0.0)"
  "gpu-gl-vendor" = "Google Inc. (Google)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "1.00"
  "gpu-psver" = "1.00"
  "gpu-driver" = "5.0.0"
  "gpu_count" = "0"
  "gpu-devid" = "0xffff"
  "gpu-venid" = "0xffff"
  "extension-1" = "kkocnggiladfibcdnpfboflllbibdabf"
  "num-extensions" = "1"
  "renderer_foreground" = "true"
  "v8_ro_space_firstpage_address" = "0x6de000000000"
  "v8_isolate_address" = "0x723173499000"
  "variations" = "6f27bc8a-3f4a17df,c203d55b-3f4a17df,e32097a3-3f4a17df,102166ac-3f4a17df,b13ca3d9-84f6cff8,54baeba4-df787358,963667b1-3f4a17df,efb0dc7b-3f4a17df,2468d6e5-3f4a17df,dbc0becb-3f4a17df,f5a1eb9a-3f4a17df,66abf9c6-3f4a17df,d2526a3-3f4a17df,ac59e11a-3f4a17df,836f1ad3-3f4a17df,d6284ba0-9610fd4e,8382fe14-3f4a17df,47a0a3b2-3f4a17df,1b0dc97-3f4a17df,2c561bd6-3f4a17df,97063883-1f820d08,d4754f61-3f4a17df,13427e22-b33b80c0,af00e384-3f4a17df,83efc983-3f4a17df,314a19c6-3f4a17df,98e50d92-3f4a17df,6b7d4090-3f4a17df,601dc969-3f4a17df,ae727645-d13781e7,7fc96067-3f4a17df,dc738ae3-3f4a17df,d3aecf6a-3f4a17df,6deb1450-3f4a17df,5eb9e4fc-3f4a17df,cad2b12b-8ef57898,57d6085b-3f4a17df,85354e40-96f99e4a,2353d10c-3c966f10,a5ecfb95-3f4a17df,797fe373-3f4a17df,3843461e-3f4a17df,17a43872-3f4a17df,a88cddf3-3f4a17df,1ffefb1a-3f4a17df,17f5c3f5-3f4a17df,f45c108d-65bced95,f419bc72-3f4a17df,470d37ba-3f4a17df,f7d06457-e9d42fcd,bcb58f65-3f4a17df,d512da3a-513c429d,832b8234-3f4a17df,54d601a5-3f4a17df,29990ed3-3f4a17df,999e8980-6ec7edcb,7faa7be9-3f4a17df,4505a270-3f4a17df,46d7c84e-3f4a17df,2e235d6c-3f4a17df,5133eb43-307b98b1,f314f5b9-89ed2dc6,6e4a21fe-efc28565,820f17d2-e484eeec,40debc11-3f4a17df,12733ec4-3f4a17df,206d80d-3f4a17df,44666d99-3d47f4f4,2eb01e0a-d93a0620,62668b66-3f4a17df,7840af09-3d47f4f4,55ba4cfa-3f4a17df,a2db6721-3f4a17df,fd051c38-3f4a17df,a98def31-2a5a8f5d,fc1790de-3f4a17df,7627ad7c-3f4a17df,7dcaa2cd-3f4a17df,18324944-3f4a17df,3779be93-3f4a17df,f32b2e65-3f4a17df,8c6d6f42-3f4a17df,227f9fd6-3f4a17df,d7ce3099-d992c41f,caf19648-369d3741,3b02c079-3f4a17df,669a7db8-3f4a17df,14789165-3f4a17df,6d123c61-a13a8969,beae798-a5e2ac51,350559e5-3f4a17df,91cba98-b3b3bb94,87684b46-4af1dc7d,4620a8f0-3f4a17df,c75c6bbe-3f4a17df,73f1e332-8d04c5a1,4eb998ce-3f4a17df,a2d45efe-2319ef5a,88d5b984-e06be83e,ef3132a9-3f4a17df,7a74f189-d34b6670,3042ad4b-ad2fa222,2d3e25b-3f4a17df,7e6af697-3f4a17df,151258bf-3f4a17df,a716fea0-3f4a17df,3e672fd9-3dbe2353,ae1581ef-35f6ea04,893cc7a4-3f4a17df,3c978b59-3f4a17df,683a3aae-80f9a33e,255aa854-c5eb06b0,31ca1680-3f4a17df,42f684c2-3f4a17df,e41e244a-3f4a17df,8e0a63e8-3f4a17df,9b2353cc-3f4a17df,82730c70-3f4a17df,9982045c-3f4a17df,96d006a-c3a49e71,b33256c0-3f4a17df,71c14987-3f4a17df,2faf225b-3f4a17df,36d5ee52-3f4a17df,1fb31bc6-3f4a17df,864a51e5-aa32be6,1f70f502-3f4a17df,e9844d40-3f4a17df,2b68be8f-3f4a17df,ad9b71e2-3f4a17df,d1ae5bf4-3f4a17df,15d1b2d8-3f4a17df,289c0dda-19e41000,3dbad317-3f4a17df,cad46b80-3f4a17df,8bccc03b-3f4a17df,57e6ff6b-3f4a17df,70404afa-803f8fc4,b7ff085-3d47f4f4,e6ed801e-cf4f6ead,fc9ceed7-ee2a48b4,eb4e0c4a-3f4a17df,c823d1e9-3d47f4f4,b4c2bd17-23db2647,b86bee04-3f4a17df,9e5c75f1-30e1b12b,7f24847e-53f28a65,4d625646-3f4a17df,e5938e6b-3f4a17df,2394f90f-ecc8f8cf,d5f746a4-39aaf314,56aa5797-e5fec5a6,265c01cc-3f4a17df,e900a5ae-4c46d137,e2d38844-3f4a17df,eef5d69a-1dca273f,da493d3c-3f4a17df,72bafd3e-cdb4c186,f659c5ca-3f4a17df,98f58bfe-3f4a17df,f3ed486d-3f4a17df,b3c54bb3-88fcaf7d,4076100b-3f4a17df,8c162025-3d47f4f4,68fef0c-3f4a17df,868b8811-3f4a17df,aa21b99b-3f4a17df,6ad21bf6-727a1257,bb993abe-24c3f6ed,f5c6b1c4-3f4a17df,b446c562-3f4a17df,63831cab-3f4a17df,d2a642a0-3f4a17df,389951ae-3f4a17df,7ece8311-3f4a17df,7a32e64e-3f4a17df,8579ead7-3f4a17df,f108c955-3f4a17df,10713630-3f4a17df,b76b514f-3ac589b9,741e95d4-3f4a17df,f381b82f-3f4a17df,8f418b04-36b3300c,d3566fbd-c6f74b94,147e9ecd-3f4a17df,bcb143fe-3f4a17df,7289b217-3f4a17df,b9ffbd4a-35efc336,2ad820b5-7f92c82c,de028327-70abd7a5,2ca06d17-3f4a17df,5abe5347-3f4a17df,35a386c3-3f4a17df,45a2f2f-f9e1b5a8,c984ae3d-65bced95,89eb0046-3f4a17df,88e285c2-3f4a17df,7c0e4650-3f4a17df,2be5fc80-3f4a17df,f9664fa0-3f4a17df,66b7a83f-3f4a17df,d721a76b-3f4a17df,137f6fe-3f4a17df,4ea303a6-3f4a17df,79662520-3f4a17df,258151b3-3f4a17df,35144f3c-3f4a17df,19593c6e-3f4a17df,c92d2cc4-3f4a17df,7c0d937f-3f4a17df,5eb745a8-3f4a17df,2468be5e-5f6398dc,aa540f4f-3f4a17df,30cf4980-61673e6,9850104b-395bafa,19e446cd-3f4a17df,f613598-3f4a17df,f3b6291d-c4414d29,53e3be58-3f4a17df,977e3a5f-2f765f61,f112d133-3f4a17df,f9be514e-3f4a17df,cae19fc9-50fdd005,1aa5b0d5-fa79c490,663ec21b-3f4a17df,ee06384e-3f4a17df,ea0d881d-fd860968,3f752d-3f4a17df,2bac9a6a-3f4a17df,ced7ce3e-3f4a17df,444b9649-3f4a17df,d990c4ac-3f4a17df,23226e84-65aafa13,198413d6-3f4a17df,5870a003-3f4a17df,3797f84b-3f4a17df,fe28a636-3f4a17df,52a20523-3f4a17df,d0083347-3ec702d4,ef4764d7-88fcaf7d,2bac45ad-3f4a17df,ccc5f0aa-3f4a17df,613081e8-3f4a17df,5b364a35-3f4a17df,f9675edd-3f4a17df,c49d2b35-3f4a17df,377002b7-3f4a17df,935eb749-7a935877,e2d2a641-baec5b64,8782f1a1-3f4a17df,1fce7d57-3f4a17df,70e21b60-3f4a17df,e8c68789-49a20295,dd8dccfb-3f4a17df,8b679bb8-3f4a17df,b0f15b33-b0f15b33,739df952-739df952,3fc87288-3f4a17df,15607410-b6e8dbb7,49ad328f-3f4a17df,ad4acdda-3f4a17df,90860314-5ab828e2,7ec047c2-3f4a17df,ade3efeb-e1cc0f14,b1ceb06f-3f4a17df,db59f83a-3f4a17df,c1e0d32e-3f4a17df,bea4a9c2-94315184,db55e85b-ecb6e1a6,2f6246c2-3f4a17df,92c76c82-3f4a17df,d04818be-3f4a17df,cef95416-b1f74a2,a4506a93-3f4a17df,5910121-3f4a17df,f9a6f6e9-3f4a17df,595f5eb0-f23d1dea,d89640a1-2f213ed2,bef5c006-3f4a17df,b0ebc2b4-3f4a17df,54412203-573b100b,e0e211ad-e0e211ad,9a0df95c-3f4a17df,8abceefd-f7ec9f66,b53f3ef9-3f4a17df,c55491ea-156838e5,1caa3332-20af8ffe,169cac91-3f4a17df,e0041356-8a5e9319,f6264095-c3f8eab0,95a095bd-3f4a17df,186d6e2c-36c0e608,26016f9f-4df4f25e,ed2195eb-3f4a17df,e9fef5c2-3f4a17df,be9ac099-f9095748,f42905ff-3f4a17df,6d2935ee-3f4a17df,17196951-3f4a17df,5a474f9e-3f4a17df,a05c89eb-67c903d4,48a8d64c-3f4a17df,34e11aee-e0986b47,f48c01d3-6eb2bd2b,2e7369a1-4aceb943,45b76973-6f345330,f4f00e05-ca7d8d80,9481ce98-3d47f4f4,2a426c03-3d47f4f4,70678518-dee66fa8,be338734-dee66fa8,5f9907a9-dee66fa8,8eeccb9a-dee66fa8,2b465683-dee66fa8,52fc7926-dee66fa8,bc9b361d-dee66fa8,a41a7188-dee66fa8,ff71bfdc-dee66fa8,e7cc79d5-dee66fa8,4b935545-bb2d3403,9a38bae3-3d47f4f4,2d1e43a3-3d47f4f4,386dc267-3d47f4f4,d69d967d-3695c92e,a4406b35-1657e2d6,408da146-1657e2d6,6c377b0f-a744f381,"
  "num-experiments" = "327"
  "reentry_guard_tls_slot" = "unused"
  "switch-20" = "--variations-seed-version"
  "switch-19" = "--field-trial-handle=3,i,751390337600472044,13298727740046262939"
  "switch-18" = "--shared-files=v8_context_snapshot_data:100"
  "switch-17" = "--launch-time-ticks=31517906748"
  "switch-16" = "--time-ticks-at-unix-epoch=-1745215961980861"
  "switch-15" = "--renderer-client-id=8"
  "switch-14" = "--enable-main-frame-before-activation"
  "switch-13" = "--num-raster-threads=4"
  "switch-12" = "--lang=en-US"
  "switch-11" = "--disable-gpu-compositing"
  "commandline-disabled-feature-1" = "PaintHolding"
  "commandline-enabled-feature-17" = "ThirdPartyStoragePartitioning"
  "commandline-enabled-feature-16" = "StorageAccessHeaders"
  "commandline-enabled-feature-15" = "SchemefulSameSite"
  "commandline-enabled-feature-14" = "PrivateNetworkAccessRespectPreflightResults"
  "commandline-enabled-feature-13" = "PartitionedPopins"
  "commandline-enabled-feature-12" = "OriginIsolationHeader"
  "commandline-enabled-feature-11" = "ExperimentalContentSecurityPolicyFeatures"
  "commandline-enabled-feature-10" = "EnableCanvas2DLayers"
  "commandline-enabled-feature-9" = "DocumentPolicyNegotiation"
  "commandline-enabled-feature-8" = "DocumentPolicyIncludeJSCallStacksInCrashReports"
  "commandline-enabled-feature-7" = "DocumentPictureInPictureAPI"
  "commandline-enabled-feature-6" = "CriticalClientHint"
  "commandline-enabled-feature-5" = "CreateImageBitmapOrientationNone"
  "commandline-enabled-feature-4" = "CookieSameSiteConsidersRedirectChain"
  "commandline-enabled-feature-3" = "BlockInsecurePrivateNetworkRequestsFromUnknown"
  "commandline-enabled-feature-2" = "BlockInsecurePrivateNetworkRequestsFromPrivate"
  "commandline-enabled-feature-1" = "BlockInsecurePrivateNetworkRequests"
  "osarch" = "x86_64"
  "pid" = "1"
  "ptype" = "renderer"'

```
#### Reporter credit:

Reporter credit: Huang Xilin of Ant Group Light-Year Security Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [poc.html](attachments/poc.html) (text/html, 7.5 KB)
- [poc2.html](attachments/poc2.html) (text/html, 24.1 KB)
- [2025-04-23 17-10-09.mkv](attachments/2025-04-23 17-10-09.mkv) (video/x-matroska, 4.1 MB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4944859529936896.

### an...@chromium.org (2025-04-21)

[security shepherd]: Thanks for the report! Assigning to @ko...@chromium.org who have worked on StringView in the past. I uploaded the test case to clusterfuzz with provisional severity of S1 and Found In to 135.

### 24...@project.gserviceaccount.com (2025-04-21)

Testcase 4944859529936896 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4944859529936896.

### ch...@google.com (2025-04-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-22)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### su...@gmail.com (2025-04-22)

It seems that the CF was not successfully reproduced. I will try to construct a more stable POC.

### ko...@chromium.org (2025-04-23)

Tried with a debug content\_shell, I see a different crash. I'll try to see if linux-asan can reproduce, but cc who may be interested in seeing this.

A debug content\_shell without options works fine.

With the `--enable-experimental-web-platform-features` option, I get:

```
[FATAL:third_party\blink\renderer\core\css\style_traversal_root.cc:31] DCHECK failed: !document_element || (!root_node_ && root_type_ == RootType::kSingleRoot). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
...x4
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
...x4
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
...x2
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
...x3
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2232] DCHECK failed: !node.ChildNeedsReattachLayoutTree(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
...x4
[FATAL:third_party\blink\renderer\core\css\style_traversal_root.cc:38] DCHECK failed: root_node_. 
[FATAL:third_party\blink\renderer\core\css\style_engine.cc:3744] DCHECK failed: FlatTreeTraversal::ContainsIncludingPseudoElement( container, *layout_tree_rebuild_root_.GetRootNode()). 
[FATAL:third_party\blink\renderer\core\layout\inline\inline_node.h:188] DCHECK failed: !GetLayoutBlockFlow()->NeedsCollectInlines(). 
[FATAL:third_party\blink\renderer\core\layout\inline\inline_node.h:188] DCHECK failed: !GetLayoutBlockFlow()->NeedsCollectInlines(). 
[FATAL:third_party\blink\renderer\core\dom\document.cc:2231] DCHECK failed: !node.NeedsReattachLayoutTree(). 
...x5

```

Then crash at [`ViewTransitionStyleTracker::AddTransitionElementsFromCSS`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/view_transition/view_transition_style_tracker.cc;l=699?q=ViewTransitionStyleTracker::AddTransitionElementsFromCSS&ss=chromium%2Fchromium%2Fsrc)

```
      paint_layer = element_->GetLayoutObject()->EnclosingLayer();

```

It looks like `element_` is fine but `element_->GetLayoutObject()` is `nullptr`.

### su...@gmail.com (2025-04-23)

Here I provide a more complex but more stably reproducible POC. You can try to launch Chrome in Ubuntu to test this POC. If there is no crash, you can try to press F12 to open the console or adjust the window size, because this bug seems to be related to page layout.

### su...@gmail.com (2025-04-23)

This is a screen recording of my reproduction of this bug.

### ko...@chromium.org (2025-04-23)

The `poc2.html` in the [comment #9](https://issues.chromium.org/issues/412265459#comment9) with resizing reproduced locally. We're trying to paint offset 7-8 of a string of 4 ""\uFFFC\uFFFC\uFFFC\uFFFC".

By enabling the `DCHECK` in `StyleTraversalRoot::Update()`, it does hit, and right before that, the string has 17 characters, so failing to update layout is likely the root cause.

Style experts, can you take a look?

### fu...@chromium.org (2025-04-23)

Crashes only for `--enable-blink-features=ScopedViewTransitions`

Reduced case:

```
<!DOCTYPE html>
<meter><div id="node1"></div></meter>
<script>
  node1.startViewTransition();
</script>

```

### fu...@chromium.org (2025-04-23)

The meter element creates a shadow tree without a slot, making #node1 being outside the flat tree, which is the thing here.

This is also a repro:

```
<!DOCTYPE html>
<div>
  <template shadowrootmode="open"></template>
  <div id="node1"></div>
</div>
<script>
  node1.startViewTransition();
</script>

```

### fu...@chromium.org (2025-04-23)

... and display:none triggers a different CHECK failure:

```
<!DOCTYPE html>
<div style="display:none">
  <div id="node1"></div>
</div>
<script>
  node1.startViewTransition();
</script>

```

### fu...@chromium.org (2025-04-23)

I tried to check for Element::GetComputedStyle() not being null on the originating element before calling RecalcPseudoTreeStyle() from StyleEngine::RecalcTransitionPseudoStyle(), which, not surprisingly, got rid of the StyleTraversalRoot CHECK failures, but that triggered CHECK failures elsewhere:

```
#5 0x7fe5facba390 blink::LayoutObject::CheckIsNotDestroyed() [../../third_party/blink/renderer/core/layout/layout_object.h:305:0]
#6 0x7fe5fd9ddcd9 blink::LayoutObject::EnclosingLayer() [../../third_party/blink/renderer/core/layout/layout_object.cc:1180:3]
#7 0x7fe5fb8f4808 blink::ViewTransitionStyleTracker::AddTransitionElementsFromCSS() [../../third_party/blink/renderer/core/view_transition/view_transition_style_tracker.cc:699:50]
#8 0x7fe5fb8cc8e1 blink::ViewTransition::ProcessCurrentState() [../../third_party/blink/renderer/core/view_transition/view_transition.cc:458:25]
#9 0x7fe5fb8ddf82 blink::ViewTransition::RunViewTransitionStepsDuringMainFrame() [../../third_party/blink/renderer/core/view_transition/view_transition.cc:886:5]

```

There's something fundamentally problematic with how we do view transitions style updates, at least for non-rendered originating elements. We have to make sure the pseudo elements are traversed and bits cleared in the same way we do for normal elements.

### fu...@chromium.org (2025-04-23)

I would strongly encourage to fix this TODO and update the view transition pseudo element handling for style and box tree generation like we update other pseudo elements (assuming the view transition pseudo elements hang off of their originating elements?):

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_engine.cc;l=3850-3852>

### dx...@google.com (2025-05-05)

Project: chromium/src  

Branch: main  

Author: Steve Kobes [skobes@chromium.org](mailto:skobes@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6505605>

ScopedVT: Add checks for scope elements that are not rendered.

---


Expand for full commit details
```
     
    (1) If the scope element has no ComputedStyle, do not create a pseudo 
    element tree. This can happen if the scope element is inside the light 
    DOM of a shadow host, but does not appear in the flat tree. 
     
    (2) If the scope element has no LayoutObject, don't look for tagged 
    participants inside it. This happens if scope has display:none style. 
    Tag discovery uses paint order, so it requires a PaintLayer. 
     
    Bug: 412265459 
    Change-Id: I848cd438b043dbdba35a66177ba7ed6256e6cc44 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6505605 
    Reviewed-by: Kevin Ellis <kevers@chromium.org> 
    Commit-Queue: Steve Kobes <skobes@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1455654}

```

---

Files:

- M `third_party/blink/renderer/core/dom/element.cc`
- M `third_party/blink/renderer/core/view_transition/view_transition_style_tracker.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-view-transitions/scoped/crashtests/shadow-dom.html`
- D `third_party/blink/web_tests/flag-specific/highdpi/virtual/threaded/external/wpt/css/css-view-transitions/pseudo-element-animations-expected.txt`
- D `third_party/blink/web_tests/virtual/threaded/external/wpt/css/css-view-transitions/pseudo-element-animations-expected.txt`
- D `third_party/blink/web_tests/virtual/view-transition-mpa-serialization/external/wpt/css/css-view-transitions/pseudo-element-animations-expected.txt`
- D `third_party/blink/web_tests/virtual/view-transition-wide-gamut/external/wpt/css/css-view-transitions/pseudo-element-animations-expected.txt`

---

Hash: ab9790296508e35f810f38aab86f93bf4dce0b80  

Date:  Mon May 5 13:01:00 2025


---

### ch...@google.com (2025-05-06)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### sk...@chromium.org (2025-05-07)

1. security fix
2. https://chromium-review.googlesource.com/6505605
3. yes
4. behind --enable-experimental-web-platform-features, no active Finch exp
5. n/a
6. no

### am...@chromium.org (2025-05-07)

If this is behind --enable-experimental-web-platform-features and not enabled by default, this would be a SI-None issue and not eligible for a security merge.

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### vm...@chromium.org (2025-05-20)

#16, I assume you mean this TODO: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_engine.cc;l=3891-3893;drc=1a7cacf91d0c57328f7c2049efa74ee2c5df4916> (and I agree that we should fix that)

### fu...@chromium.org (2025-05-21)

> #16, I assume you mean this TODO: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_engine.cc;l=3891-3893;drc=1a7cacf91d0c57328f7c2049efa74ee2c5df4916> (and I agree that we should fix that)

Yes.

### ch...@google.com (2025-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/412265459)*
