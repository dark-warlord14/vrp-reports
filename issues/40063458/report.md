# Heap-use-after-free in blink::NGTextDecorationPainter::UpdateDecorationInfo

| Field | Value |
|-------|-------|
| **Issue ID** | [40063458](https://issues.chromium.org/issues/40063458) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | da...@igalia.com |
| **Created** | 2023-03-08 |
| **Bounty** | $10,000.00 |

## Description

\*\*VULNERABILITY DETAILS\*\*
UAF in blink::NGTextDecorationPainter::UpdateDecorationInfo ng\_text\_decoration\_painter.cc:46:15
\*\*VERSION\*\*
Chromium: 1114386
\*\*REPRODUCTION CASE\*\*
The case was discovered by my fuzzer running on CF, but it cannot be reproduced stably, so I submitted the report manually
[https://clusterfuzz.com/testcase-detail/5878562507390976](https://www.google.com/url?q=https://clusterfuzz.com/testcase-detail/5878562507390976&sa=D&source=buganizer&usg=AOvVaw1BeOL8vzVKS8rjqFvVXuwY)
Type of crash: [tab]
#ASAN
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000128c30 at pc 0x5652c2a5ec0f bp 0x7ffca8adcb70 sp 0x7ffca8adcb68
READ of size 8 at 0x60b000128c30 thread T0 (chrome)
SCARINESS: 51 (8-byte-read-heap-use-after-free)
#0 0x5652c2a5ec0e in get base/memory/scoped\_refptr.h:283:27
#1 0x5652c2a5ec0e in Get third\_party/blink/renderer/core/style/data\_ref.h:37:39
#2 0x5652c2a5ec0e in operator-> third\_party/blink/renderer/core/style/data\_ref.h:40:40
#3 0x5652c2a5ec0e in GetTextDecorationLine gen/third\_party/blink/renderer/core/style/computed\_style\_base.h:3653:44
#4 0x5652c2a5ec0e in IsDecoratingBox third\_party/blink/renderer/core/style/computed\_style.h:1851:9
#5 0x5652c2a5ec0e in HasAppliedTextDecorations third\_party/blink/renderer/core/style/computed\_style.h:1862:9
#6 0x5652c2a5ec0e in blink::NGTextDecorationPainter::UpdateDecorationInfo(absl::optional<blink::TextDecorationInfo>&, blink::ComputedStyle const&, blink::TextPaintStyle const&, absl::optional<blink::PhysicalRect>, blink::AppliedTextDecoration const\\*) third\_party/blink/renderer/core/paint/ng/ng\_text\_decoration\_painter.cc:46:15
#7 0x5652c2a773b9 in blink::NGHighlightPainter::PaintDecorationsExceptLineThrough(blink::NGHighlightOverlay::HighlightPart const&, blink::TextDecorationLine) third\_party/blink/renderer/core/paint/ng/ng\_highlight\_painter.cc:1144:25
#8 0x5652c2a72346 in blink::NGHighlightPainter::PaintDecorationsExceptLineThrough(blink::NGHighlightOverlay::HighlightPart const&) third\_party/blink/renderer/core/paint/ng/ng\_highlight\_painter.cc:1102:3
#9 0x5652c2a7657e in blink::NGHighlightPainter::PaintHighlightOverlays(blink::TextPaintStyle const&, int, bool, absl::optional<blink::AffineTransform>) third\_party/blink/renderer/core/paint/ng/ng\_highlight\_painter.cc:1055:9
#10 0x5652c2a5a731 in blink::NGTextFragmentPainter::Paint(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_text\_fragment\_painter.cc:453:25
#11 0x5652c2a18bf6 in blink::NGBoxFragmentPainter::PaintTextItem(blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1678:16
#12 0x5652c2a0ae3c in blink::NGBoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&, blink::NGInlineCursor\\*) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1501:11
#13 0x5652c2a0f0b0 in blink::NGBoxFragmentPainter::PaintLineBoxChildItems(blink::NGInlineCursor\\*, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1596:7
#14 0x5652c2a0bb84 in blink::NGBoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:824:3
#15 0x5652c2a041a9 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:663:9
#16 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#17 0x5652c29ffb25 in blink::NGBoxFragmentPainter::PaintAllPhasesAtomically(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1476:3
#18 0x5652c29ff791 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:412:5
#19 0x5652c2a1014e in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:873:46
#20 0x5652c2a0c6fc in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:837:5
#21 0x5652c2a04356 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:665:9
#22 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#23 0x5652c29ffb25 in blink::NGBoxFragmentPainter::PaintAllPhasesAtomically(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1476:3
#24 0x5652c29ff791 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:412:5
#25 0x5652c2a11298 in blink::(anonymous namespace)::PaintFragment(blink::NGPhysicalBoxFragment const&, blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:364:36
#26 0x5652c2a18264 in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGPhysicalBoxFragment const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1702:5
#27 0x5652c2a194d8 in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1732:7
#28 0x5652c2a0ae65 in blink::NGBoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&, blink::NGInlineCursor\\*) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1506:11
#29 0x5652c2a0f0b0 in blink::NGBoxFragmentPainter::PaintLineBoxChildItems(blink::NGInlineCursor\\*, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1596:7
#30 0x5652c2a0bb84 in blink::NGBoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:824:3
#31 0x5652c2a041a9 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:663:9
#32 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#33 0x5652c29ff70e in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:418:5
#34 0x5652c2a1014e in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:873:46
#35 0x5652c2a0c6fc in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:837:5
#36 0x5652c2a04356 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:665:9
#37 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#38 0x5652c29ff70e in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:418:5
#39 0x5652c2a1014e in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:873:46
#40 0x5652c2a0c6fc in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:837:5
#41 0x5652c2a04356 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:665:9
#42 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#43 0x5652c29ff70e in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:418:5
#44 0x5652c2b02679 in blink::PaintLayerPainter::PaintFragmentWithPhase(blink::PaintPhase, blink::FragmentData const&, blink::NGPhysicalBoxFragment const\\*, blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:378:46
#45 0x5652c2b00cc1 in blink::PaintLayerPainter::PaintWithPhase(blink::PaintPhase, blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:412:5
#46 0x5652c2b019a6 in blink::PaintLayerPainter::PaintForegroundPhases(blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:435:3
#47 0x5652c2aff651 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:253:7
#48 0x5652c2b01163 in blink::PaintLayerPainter::PaintChildren(blink::PaintLayerIteration, blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:316:35
#49 0x5652c2aff829 in blink::PaintLayerPainter::Paint(blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/paint\_layer\_painter.cc:265:7
#50 0x5652c29b2fd9 in blink::FramePainter::Paint(blink::GraphicsContext&, unsigned int) third\_party/blink/renderer/core/paint/frame\_painter.cc:91:17
#51 0x5652c0cae05c in PaintFrame third\_party/blink/renderer/core/frame/local\_frame\_view.cc:4028:23
#52 0x5652c0cae05c in blink::LocalFrameView::PaintTree(blink::PaintBenchmarkMode) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2952:7
#53 0x5652c0caba29 in blink::LocalFrameView::RunPaintLifecyclePhase(blink::PaintBenchmarkMode) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2763:22
#54 0x5652c0ca9579 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2510:3
#55 0x5652c0ca696f in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2311:3
#56 0x5652c0ca61e7 in blink::LocalFrameView::UpdateAllLifecyclePhases(blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2074:54
#57 0x5652c28a5567 in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentUpdateReason) third\_party/blink/renderer/core/page/page\_animator.cc:315:9
#58 0x5652c0e034e5 in blink::WebFrameWidgetImpl::UpdateLifecycle(blink::WebLifecycleUpdate, blink::DocumentUpdateReason) third\_party/blink/renderer/core/frame/web\_frame\_widget\_impl.cc:1449:14
#59 0x5652c3ac6235 in UpdateVisualState third\_party/blink/renderer/platform/widget/widget\_base.cc:884:12
#60 0x5652c3ac6235 in non-virtual thunk to blink::WidgetBase::UpdateVisualState() third\_party/blink/renderer/platform/widget/widget\_base.cc:0
#61 0x5652b91cb5b6 in cc::LayerTreeHost::RequestMainFrameUpdate(bool) cc/trees/layer\_tree\_host.cc:376:12
#62 0x5652b945b775 in cc::ProxyMain::BeginMainFrame(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>) cc/trees/proxy\_main.cc:285:21
#63 0x5652b947c51f in Invoke<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > > base/functional/bind\_internal.h:760:12
#64 0x5652b947c51f in MakeItSo<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > > > base/functional/bind\_internal.h:962:5
#65 0x5652b947c51f in RunImpl<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > >, 0UL, 1UL> base/functional/bind\_internal.h:1034:12
#66 0x5652b947c51f in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunOnce(base::internal::BindStateBase\\*) base/functional/bind\_internal.h:985:12
#67 0x5652b3c3311a in Run base/functional/callback.h:152:12
#68 0x5652b3c3311a in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:162:32
#69 0x5652b3c8a5ab in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> base/task/common/task\_annotator.h:88:5
#70 0x5652b3c8a5ab in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#71 0x5652b3c89375 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:339:41
#72 0x5652b3c8bc44 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0
#73 0x5652b3b1acd3 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\\*) base/message\_loop/message\_pump\_default.cc:48:55
#74 0x5652b3c8c909 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:634:12
#75 0x5652b3bb566f in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:140:14
#76 0x5652cb17219e in content::RendererMain(content::MainFunctionParams) content/renderer/renderer\_main.cc:336:16
#77 0x5652b1162ab9 in content::RunZygote(content::ContentMainDelegate\\*) content/app/content\_main\_runner\_impl.cc:707:14
#78 0x5652b1164d40 in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\\*) content/app/content\_main\_runner\_impl.cc:792:12
#79 0x5652b116724a in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1154:10
#80 0x5652b115f445 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\\*) content/app/content\_main.cc:326:36
#81 0x5652b115f980 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:343:10
#82 0x5652a2840c76 in ChromeMain chrome/app/chrome\_main.cc:190:12
#83 0x7f7b0b33b082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/libc-start.c:308:16
0x60b000128c30 is located 16 bytes inside of 104-byte region [0x60b000128c20,0x60b000128c88)
freed by thread T0 (chrome) here:
#0 0x5652a280d246 in free third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:52:3
#1 0x5652c2a664da in operator delete third\_party/blink/renderer/core/style/computed\_style.h:332:7
#2 0x5652c2a664da in DeleteInternal<blink::ComputedStyle> third\_party/blink/renderer/platform/wtf/ref\_counted.h:54:5
#3 0x5652c2a664da in Destruct third\_party/blink/renderer/platform/wtf/ref\_counted.h:35:5
#4 0x5652c2a664da in Release base/memory/ref\_counted.h:356:7
#5 0x5652c2a664da in Release base/memory/scoped\_refptr.h:382:8
#6 0x5652c2a664da in ~scoped\_refptr base/memory/scoped\_refptr.h:280:7
#7 0x5652c2a664da in blink::NGHighlightPainter::NGHighlightPainter(blink::NGTextFragmentPaintInfo const&, blink::NGTextPainter&, blink::NGTextDecorationPainter&, blink::PaintInfo const&, blink::NGInlineCursor const&, blink::NGFragmentItem const&, absl::optional<blink::AffineTransform>, blink::PhysicalRect const&, blink::PhysicalOffset const&, blink::ComputedStyle const&, blink::TextPaintStyle const&, blink::NGHighlightPainter::SelectionPaintState\\*, bool) third\_party/blink/renderer/core/paint/ng/ng\_highlight\_painter.cc:563:9
#8 0x5652c2a59797 in blink::NGTextFragmentPainter::Paint(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_text\_fragment\_painter.cc:341:22
#9 0x5652c2a18bf6 in blink::NGBoxFragmentPainter::PaintTextItem(blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1678:16
#10 0x5652c2a0ae3c in blink::NGBoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&, blink::NGInlineCursor\\*) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1501:11
#11 0x5652c2a0f0b0 in blink::NGBoxFragmentPainter::PaintLineBoxChildItems(blink::NGInlineCursor\\*, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1596:7
#12 0x5652c2a0bb84 in blink::NGBoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:824:3
#13 0x5652c2a041a9 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:663:9
#14 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#15 0x5652c29ffb25 in blink::NGBoxFragmentPainter::PaintAllPhasesAtomically(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1476:3
#16 0x5652c29ff791 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:412:5
#17 0x5652c2a1014e in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:873:46
#18 0x5652c2a0c6fc in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:837:5
#19 0x5652c2a04356 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:665:9
#20 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#21 0x5652c29ffb25 in blink::NGBoxFragmentPainter::PaintAllPhasesAtomically(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1476:3
#22 0x5652c29ff791 in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:412:5
#23 0x5652c2a11298 in blink::(anonymous namespace)::PaintFragment(blink::NGPhysicalBoxFragment const&, blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:364:36
#24 0x5652c2a18264 in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGPhysicalBoxFragment const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1702:5
#25 0x5652c2a194d8 in blink::NGBoxFragmentPainter::PaintBoxItem(blink::NGFragmentItem const&, blink::NGInlineCursor const&, blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1732:7
#26 0x5652c2a0ae65 in blink::NGBoxFragmentPainter::PaintInlineItems(blink::PaintInfo const&, blink::PhysicalOffset const&, blink::PhysicalOffset const&, blink::NGInlineCursor\\*) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1506:11
#27 0x5652c2a0f0b0 in blink::NGBoxFragmentPainter::PaintLineBoxChildItems(blink::NGInlineCursor\\*, blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:1596:7
#28 0x5652c2a0bb84 in blink::NGBoxFragmentPainter::PaintLineBoxes(blink::PaintInfo const&, blink::PhysicalOffset const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:824:3
#29 0x5652c2a041a9 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:663:9
#30 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
#31 0x5652c29ff70e in blink::NGBoxFragmentPainter::Paint(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:418:5
#32 0x5652c2a1014e in blink::NGBoxFragmentPainter::PaintBlockChild(blink::NGLink const&, blink::PaintInfo const&, blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:873:46
#33 0x5652c2a0c6fc in blink::NGBoxFragmentPainter::PaintBlockChildren(blink::PaintInfo const&, blink::PhysicalOffset) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:837:5
#34 0x5652c2a04356 in blink::NGBoxFragmentPainter::PaintObject(blink::PaintInfo const&, blink::PhysicalOffset const&, bool) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:665:9
#35 0x5652c2a00e95 in blink::NGBoxFragmentPainter::PaintInternal(blink::PaintInfo const&) third\_party/blink/renderer/core/paint/ng/ng\_box\_fragment\_painter.cc:511:7
previously allocated by thread T0 (chrome) here:
#0 0x5652a280d4ee in malloc third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:69:3
#1 0x5652b1998d88 in AllocWithFlagsInternal base/allocator/partition\_allocator/partition\_root.h:1870:49
#2 0x5652b1998d88 in AllocWithFlags base/allocator/partition\_allocator/partition\_root.h:1847:10
#3 0x5652b1998d88 in partition\_alloc::PartitionRoot<true>::Alloc(unsigned long, char const\\*) base/allocator/partition\_allocator/partition\_root.h:2204:10
#4 0x5652c2e7f743 in operator new third\_party/blink/renderer/core/style/computed\_style.h:325:12
#5 0x5652c2e7f743 in blink::ComputedStyleBuilder::CloneStyle() const third\_party/blink/renderer/core/style/computed\_style.cc:2475:25
#6 0x5652c42d58ca in blink::StyleResolver::ApplyAnimatedStyle(blink::StyleResolverState&, blink::StyleCascade&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1878:30
#7 0x5652c42d2951 in blink::StyleResolver::ResolveStyle(blink::Element\\*, blink::StyleRecalcContext const&, blink::StyleRequest const&) third\_party/blink/renderer/core/css/resolver/style\_resolver.cc:1014:7
#8 0x5652c400295a in OriginalStyleForLayoutObject third\_party/blink/renderer/core/dom/element.cc:3150:43
#9 0x5652c400295a in blink::Element::StyleForLayoutObject(blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3099:13
#10 0x5652c4009288 in blink::Element::RecalcOwnStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3633:17
#11 0x5652c40062c5 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3288:20
#12 0x5652c3d3b568 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1396:26
#13 0x5652c4007064 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3393:7
#14 0x5652c3d3b568 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1396:26
#15 0x5652c4006ec7 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3385:13
#16 0x5652c3d3b568 in blink::ContainerNode::RecalcDescendantStyles(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:1396:26
#17 0x5652c4007064 in blink::Element::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/dom/element.cc:3393:7
#18 0x5652c00e52a5 in blink::StyleEngine::RecalcStyle(blink::StyleRecalcChange, blink::StyleRecalcContext const&) third\_party/blink/renderer/core/css/style\_engine.cc:3137:20
#19 0x5652c00e8267 in blink::StyleEngine::RecalcStyle() third\_party/blink/renderer/core/css/style\_engine.cc:3167:3
#20 0x5652c00e8c89 in blink::StyleEngine::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:3275:7
#21 0x5652c3d7410c in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2300:16
#22 0x5652c3d720df in blink::Document::UpdateStyleAndLayoutTreeForThisDocument() third\_party/blink/renderer/core/dom/document.cc:2243:3
#23 0x5652c0cb3736 in blink::LocalFrameView::UpdateStyleAndLayoutInternal() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3266:30
#24 0x5652c0c9d9a4 in blink::LocalFrameView::UpdateStyleAndLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:3214:18
#25 0x5652c3d72937 in blink::Document::UpdateStyleAndLayout(blink::DocumentUpdateReason) third\_party/blink/renderer/core/dom/document.cc:2608:17
#26 0x5652c07172ab in blink::FrameSelection::ComputeAbsoluteBounds(gfx::Rect&, gfx::Rect&) const third\_party/blink/renderer/core/editing/frame\_selection.cc:619:26
#27 0x5652c0e1c8a0 in blink::WebFrameWidgetImpl::CalculateSelectionBounds(gfx::Rect&, gfx::Rect&, gfx::Rect\\*) third\_party/blink/renderer/core/frame/web\_frame\_widget\_impl.cc:4036:18
#28 0x5652c0e1bcb3 in blink::WebFrameWidgetImpl::GetSelectionBoundsInWindow(gfx::Rect\\*, gfx::Rect\\*, gfx::Rect\\*, base::i18n::TextDirection\\*, base::i18n::TextDirection\\*, bool\\*) third\_party/blink/renderer/core/frame/web\_frame\_widget\_impl.cc:3363:3
#29 0x5652c3ac5a59 in blink::WidgetBase::UpdateSelectionBounds() third\_party/blink/renderer/platform/widget/widget\_base.cc:1284:23
#30 0x5652c3ac56d0 in blink::WidgetBase::WillBeginMainFrame() third\_party/blink/renderer/platform/widget/widget\_base.cc:851:3
#31 0x5652b91cb051 in cc::LayerTreeHost::WillBeginMainFrame() cc/trees/layer\_tree\_host.cc:346:12
#32 0x5652b945b610 in cc::ProxyMain::BeginMainFrame(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>) cc/trees/proxy\_main.cc:262:21
#33 0x5652b947c51f in Invoke<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > > base/functional/bind\_internal.h:760:12
#34 0x5652b947c51f in MakeItSo<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > > > base/functional/bind\_internal.h:962:5
#35 0x5652b947c51f in RunImpl<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> >), std::Cr::tuple<base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState> > >, 0UL, 1UL> base/functional/bind\_internal.h:1034:12
#36 0x5652b947c51f in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\\*)(std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>), base::WeakPtr<cc::ProxyMain>, std::Cr::unique\_ptr<cc::BeginMainFrameAndCommitState, std::Cr::default\_delete<cc::BeginMainFrameAndCommitState>>>, void ()>::RunOnce(base::internal::BindStateBase\\*) base/functional/bind\_internal.h:985:12
SUMMARY: AddressSanitizer: heap-use-after-free (/mnt/scratch0/clusterfuzz/bot/builds/chrome-test-builds\_media\_linux-release\_eb660d5ee526c9c1c1608a71fcbe7a713c490533/revisions/asan-linux-release-1114386/chrome+0x2ca8cc0e) (BuildId: 82ef17887df3d138)
Shadow bytes around the buggy address:
0x60b000128980: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
0x60b000128a00: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x60b000128a80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
0x60b000128b00: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fd fd
0x60b000128b80: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
=>0x60b000128c00: fa fa fa fa fd fd[fd]fd fd fd fd fd fd fd fd fd
0x60b000128c80: fd fa fa fa fa fa fa fa fa fa 00 00 00 00 00 00
0x60b000128d00: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa
0x60b000128d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa
0x60b000128e00: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
0x60b000128e80: 00 00 00 00 fa fa fa fa fa fa fa fa 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable:00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb
==1==ADDITIONAL INFO
==1==Note: Please include this section with the ASan report.
Task trace:
#0 0x5652b9474a3c in cc::ProxyImpl::ScheduledActionSendBeginMainFrame(viz::BeginFrameArgs const&) cc/trees/proxy\_impl.cc:770:7
#1 0x5652b6094218 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple\_watcher.cc:102:13

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 31.3 KB)

## Timeline

### m....@gmail.com (2023-03-08)

bisect
Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/4199618


### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-08)

Detailed Report: https://clusterfuzz.com/testcase?key=5878562507390976

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b000128c30
Crash State:
  blink::NGTextDecorationPainter::UpdateDecorationInfo
  blink::NGHighlightPainter::PaintDecorationsExceptLineThrough
  blink::NGHighlightPainter::PaintDecorationsExceptLineThrough
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&revision=1114386

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5878562507390976

Additional requirements: Requires Gestures

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-08)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Paint]

### cl...@chromium.org (2023-03-08)

ClusterFuzz testcase 5878562507390976 appears to be flaky, updating reproducibility label.

### ma...@chromium.org (2023-03-08)

Setting foundin-113 based on the reported bisect (https://crbug.com/chromium/1422533#c1)

Setting high severity as it is a UAF in renderer.

Based on the stacktrace, does not appear to be platform specific.

### [Deleted User] (2023-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2023-03-15)

#RCA

HighlightPseudoStyle calls ComputedStyle-related functions and returns const ComputedStyle*[3].
HighlightPseudoStyle itself wraps const ComputedStyle* and returns a scoped_refptr<const ComputedStyle>[2].
LayerPaintState calls HighlightPseudoStyle to obtain a scoped_refptr<const ComputedStyle> temporary variable, but uses get()[1] to obtain the original pointer, which leads ComputedStyle get freed and results in UAF.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/ng/ng_highlight_painter.cc;drc=0e9a0b6e9bb6ec59521977eec805f5d0bca833e0;l=562
        layers_.push_back(LayerPaintState{
            layers[i],
            HighlightPaintingUtils::HighlightPseudoStyle(
                node_, originating_style_, layers[i].PseudoId(),
                layers[i].PseudoArgument())
                .get(),
            HighlightPaintingUtils::HighlightPaintingStyle(
                document, originating_style_, node_, layers[i].PseudoId(),
                layers_[i - 1].text_style, paint_info_,
                layers[i].PseudoArgument()),
        });
        

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/highlight_painting_utils.cc;drc=0e9a0b6e9bb6ec59521977eec805f5d0bca833e0;l=303
scoped_refptr<const ComputedStyle> HighlightPaintingUtils::HighlightPseudoStyle(
    Node* node,
    const ComputedStyle& style,
    PseudoId pseudo,
    const AtomicString& pseudo_argument) {
  if (!UsesHighlightPseudoInheritance(pseudo)) {
    return HighlightPseudoStyleWithOriginatingInheritance(node, pseudo,
                                                          pseudo_argument);
  }

  if (!style.HighlightData())
    return nullptr;

  switch (pseudo) {
    case kPseudoIdSelection:
      return style.HighlightData()->Selection();
    case kPseudoIdTargetText:
      return style.HighlightData()->TargetText();
    case kPseudoIdSpellingError:
      return style.HighlightData()->SpellingError();
    case kPseudoIdGrammarError:
      return style.HighlightData()->GrammarError();
    case kPseudoIdHighlight:
      return style.HighlightData()->CustomHighlight(pseudo_argument);
    default:
      NOTREACHED();
      return nullptr;
  }
}

[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/style/style_highlight_data.cc;drc=0e9a0b6e9bb6ec59521977eec805f5d0bca833e0;l=78
const ComputedStyle* StyleHighlightData::Selection() const {
  return selection_.get();
}

const ComputedStyle* StyleHighlightData::TargetText() const {
  return target_text_.get();
}

const ComputedStyle* StyleHighlightData::SpellingError() const {
  return spelling_error_.get();
}

const ComputedStyle* StyleHighlightData::GrammarError() const {
  return grammar_error_.get();
}

const ComputedStyle* StyleHighlightData::CustomHighlight(
    const AtomicString& highlight_name) const {
  if (highlight_name) {
    auto iter = custom_highlights_.find(highlight_name);
    if (iter != custom_highlights_.end()) {
      return iter->value.get();
    }
  }
  return nullptr;
}

### pd...@chromium.org (2023-03-15)

Delan: ping?

### da...@igalia.com (2023-03-16)

Looking into this.

### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94

commit ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94
Author: Delan Azabani <dazabani@igalia.com>
Date: Fri Mar 17 16:21:46 2023

CSS highlight painting: fix heap-use-after-free and NOTREACHED bugs

The ctor for NGHighlightPainter stores the ComputedStyle for each
highlight pseudo in a LayerPaintState field for use by later method
calls, but it unwraps the scoped_refptr<ComputedStyle> into a raw
pointer first, allowing the values to be freed before use. This patch
makes LayerPaintState hold the refcounted pointer itself.

ForcedForegroundColor and ForcedBackgroundColor lacked cases for the
::spelling-error and ::grammar-error pseudos, yielding a NOTREACHED()
crash when painting those highlights in forced colors mode. This patch
adds cases for those pseudos, fixing the crash.

Fixed: 1422533, 1423540
Change-Id: Ied7eaafea601a044b2c8e35889e0d36aa43ab791
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4350127
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Philip Rogers <pdr@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1118687}

[add] https://crrev.com/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94/third_party/blink/web_tests/wpt_internal/css/css-pseudo/spelling-error-007-crash.html
[modify] https://crrev.com/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94/third_party/blink/renderer/core/paint/ng/ng_highlight_painter.cc
[modify] https://crrev.com/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94/third_party/blink/renderer/core/paint/ng/ng_highlight_painter.h
[modify] https://crrev.com/ac6a56d8b7d742b83fa00aaa171bdc0f6ebd2e94/third_party/blink/renderer/core/paint/highlight_painting_utils.cc


### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### [Deleted User] (2023-03-24)

Not requesting merge to dev (M113) because latest trunk commit (1118687) appears to be prior to dev branch point (1121455). If this is incorrect, please replace the Merge-NA-113 label with Merge-Request-113. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-24)

fix landed on M113, no merge needed here 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1422533?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063458)*
