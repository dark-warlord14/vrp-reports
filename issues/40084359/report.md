# Security: heap-use-after-free in blink::LayoutBox::shapeOutsideInfo

| Field | Value |
|-------|-------|
| **Issue ID** | [40084359](https://issues.chromium.org/issues/40084359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-05-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest asan build of chrome as follows:

=================================================================  

==7258==ERROR: AddressSanitizer: heap-use-after-free on address 0x612000006050 at pc 0x000008b2a0f5 bp 0x7ffc6cbd88d0 sp 0x7ffc6cbd88c8  

READ of size 8 at 0x612000006050 thread T0 (content\_shell)  

#0 0x8b2a0f4 in get /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RefPtr.h:59  

#1 0x8728df6 in blink::LayoutBox::shapeOutsideInfo() const /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBox.cpp:4826  

#2 0x8bf3b73 in blink::ComputeFloatOffsetForLineLayoutAdapter<(blink::FloatingObject::Type)2>::updateOffsetIfNeeded(blink::FloatingObject const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/FloatingObjects.cpp:598 (discriminator 4)  

#3 0x8bf4184 in collectIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/FloatingObjects.cpp:570 (discriminator 1)  

#4 0x8be789d in allOverlapsWithAdapter<blink::ComputeFloatOffsetForLineLayoutAdapter[blink::FloatingObject::Type::FloatRight](javascript:void(0);) > /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/PODIntervalTree.h:126 (discriminator 1)  

#5 0x86e4ba6 in logicalRightOffsetForLine /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlockFlow.h:333 (discriminator 3)  

#6 0x86e45da in blink::LayoutBox::shrinkLogicalWidthToAvoidFloats(blink::LayoutUnit, blink::LayoutUnit, blink::LayoutBlockFlow const\*) const /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBox.cpp:1672 (discriminator 3)  

#7 0x86cef36 in blink::LayoutBox::computeLogicalWidthUsing(blink::SizeType, blink::Length const&, blink::LayoutUnit, blink::LayoutBlock const\*) const /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBox.cpp:2355 (discriminator 3)  

#8 0x86f055b in blink::LayoutBox::computeLogicalWidth(blink::LayoutBox::LogicalExtentComputedValues&) const /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBox.cpp:2262 (discriminator 3)  

#9 0x86ee1a8 in blink::LayoutBox::updateLogicalWidth() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBox.cpp:2164  

#10 0x86042ec in blink::LayoutBlock::updateLogicalWidthAndColumnWidth() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:464  

#11 0x863242f in blink::LayoutBlockFlow::updateLogicalWidthAndColumnWidth() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:225 (discriminator 1)  

#12 0x8635975 in blink::LayoutBlockFlow::layoutBlockFlow(bool, blink::LayoutUnit&, blink::SubtreeLayoutScope&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:426 (discriminator 1)  

#13 0x8634d00 in blink::LayoutBlockFlow::layoutBlock(bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:395  

#14 0x8603e1c in blink::LayoutBlock::layout() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/layout/LayoutBlock.cpp:433  

#15 0x795cd1e in blink::FrameView::layoutOrthogonalWritingModeRoots() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:1783 (discriminator 1)  

#16 0x795ba5b in blink::FrameView::performLayout(bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:872  

#17 0x795fd3e in blink::FrameView::layout() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/FrameView.cpp:1039  

#18 0x64a082e in blink::Document::implicitClose() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2672 (discriminator 1)  

#19 0x7d9694f in blink::FrameLoader::checkCompleted() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:616 (discriminator 2)  

#20 0x7d96385 in blink::FrameLoader::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:534  

#21 0x64d6328 in blink::Document::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4801 (discriminator 1)  

#22 0x6e94308 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:797 (discriminator 1)  

#23 0x6e9d690 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::OwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:445  

#24 0x6e963c3 in blink::HTMLDocumentParser::pumpPendingSpeculations() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:528 (discriminator 2)  

#25 0x6ec5d0e in operator()<> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:183 (discriminator 3)  

#26 0xfe91093 in Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:159 (discriminator 2)  

#27 0x820a91 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:397 (discriminator 1)  

#28 0xfeac54f in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/base/task\_queue\_manager.cc:289  

#29 0xfea82fc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/base/task\_queue\_manager.cc:201  

#30 0xfeaea64 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:186 (discriminator 6)  

#31 0x820a91 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:397 (discriminator 1)  

#32 0x6d8ed5 in base::MessageLoop::RunTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:478  

#33 0x6d9cef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:487  

#34 0x6db12c in base::MessageLoop::DoWork() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:604  

#35 0x6e53bd in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:33 (discriminator 1)  

#36 0x72e139 in base::RunLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:35  

#37 0x6d6648 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:294  

#38 0xb68e37d in content::RendererMain(content::MainFunctionParams const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:199 (discriminator 1)  

#39 0x637d72 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:345  

#40 0x63c52f in content::ContentMainRunnerImpl::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:787  

#41 0x636aed in content::ContentMain(content::ContentMainParams const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:20 (discriminator 1)  

#42 0x501db2 in main /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/shell/app/shell\_main.cc:48  

#43 0x7f3d30fda82f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

0x612000006050 is located 16 bytes inside of 264-byte region [0x612000006040,0x612000006148)  

freed by thread T0 (content\_shell) here:  

#0 0x4d61eb in \_\_interceptor\_free ??:?  

#1 0x66198bb in blink::Node::detach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:933 (discriminator 1)  

#2 0x64188ce in blink::ContainerNode::detach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:770  

#3 0x654fb2e in blink::Element::detach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1593  

#4 0x66194b9 in blink::Node::reattach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:910  

#5 0x65538f5 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1765  

#6 0x65525aa in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1705  

#7 0x6491aff in blink::Document::updateStyle() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1817  

#8 0x64800f3 in blink::Document::updateStyleAndLayoutTree() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1752  

#9 0x64a0686 in blink::Document::implicitClose() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2668  

#10 0x7d9694f in blink::FrameLoader::checkCompleted() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:616 (discriminator 2)  

#11 0x7d96385 in blink::FrameLoader::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:534  

#12 0x64d6328 in blink::Document::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4801 (discriminator 1)  

#13 0x6e94308 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:797 (discriminator 1)  

#14 0x6e9d690 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::OwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:445  

#15 0x6e963c3 in blink::HTMLDocumentParser::pumpPendingSpeculations() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:528 (discriminator 2)  

#16 0x6ec5d0e in operator()<> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:183 (discriminator 3)  

#17 0xfe91093 in Run<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:159 (discriminator 2)  

#18 0x820a91 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:397 (discriminator 1)  

#19 0xfeac54f in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/base/task\_queue\_manager.cc:289  

#20 0xfea82fc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/base/task\_queue\_manager.cc:201  

#21 0xfeaea64 in Run<scheduler::TaskQueueManager \*, const base::TimeTicks &, const bool &> /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:186 (discriminator 6)  

#22 0x820a91 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:397 (discriminator 1)  

#23 0x6d8ed5 in base::MessageLoop::RunTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:478  

#24 0x6d9cef in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:487  

#25 0x6db12c in base::MessageLoop::DoWork() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:604  

#26 0x6e53bd in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:33 (discriminator 1)  

#27 0x72e139 in base::RunLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:35  

#28 0x6d6648 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:294  

#29 0xb68e37d in content::RendererMain(content::MainFunctionParams const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:199 (discriminator 1)

previously allocated by thread T0 (content\_shell) here:  

#0 0x4d651d in \_\_interceptor\_malloc ??:?  

#1 0x8875b1c in partitionAlloc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:660 (discriminator 1)  

#2 0x65ca7a4 in blink::LayoutTreeBuilderForElement::createLayoutObject() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.cpp:119 (discriminator 2)  

#3 0x654db88 in createLayoutObjectIfNeeded /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/LayoutTreeBuilder.h:76  

#4 0x66194f1 in blink::Node::reattach(blink::Node::AttachContext const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:911  

#5 0x65538f5 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1765  

#6 0x65525aa in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1705  

#7 0x6491aff in blink::Document::updateStyle() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1817  

#8 0x64800f3 in blink::Document::updateStyleAndLayoutTree() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1752  

#9 0x6495566 in blink::Document::updateStyleAndLayoutTreeIgnorePendingStylesheets() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1999  

#10 0x64937a4 in updateStyleAndLayoutIgnorePendingStylesheets /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2004  

#11 0x653ce95 in blink::Element::getBoundingClientRect() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1021 (discriminator 1)  

#12 0x9144169 in getBoundingClientRectMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Element.cpp:1780  

#13 0x3ef9f60 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api-arguments.cc:16  

#14 0x2bf3d2d in v8::internal::(anonymous namespace)::HandleApiCallHelper(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)3>) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:4673 (discriminator 1)  

#15 0x2c9128e in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)3>, v8::internal::Isolate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/builtins.cc:4691 (discriminator 5)  

#16 0x7f3b7e708ba6 (<unknown module>)  

#17 0x7f3b7e7657f8 (<unknown module>)  

#18 0x7f3b7e764fa9 (<unknown module>)  

#19 0x7f3b7e745962 (<unknown module>)  

#20 0x7f3b7e72998e (<unknown module>)  

#16 0x32c18de in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:98  

#17 0x32c12e1 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:154 (discriminator 2)  

#18 0x2b204fc in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4468 (discriminator 3)  

#19 0x901125b in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:467 (discriminator 3)  

#20 0x8feaa6d in blink::V8LazyEventListener::callListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:100 (discriminator 4)  

#21 0x8fa62fa in blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:130 (discriminator 1)  

#22 0x8fa5dba in blink::V8AbstractEventListener::handleEvent(blink::ScriptState\*, blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:95 (discriminator 3)  

#23 0x8fa5992 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext\*, blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:84  

#24 0x67dd0de in blink::EventTarget::fireEventListeners(blink::Event\*, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:582 (discriminator 1)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/nils/MonkeyChrome/OpRealEstate/asan-linux-release-395131/content\_shell+0x8b2a0f4)  

Shadow bytes around the buggy address:  

0x0c247fff8bb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff8bc0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c247fff8bd0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c247fff8be0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff8bf0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

=>0x0c247fff8c00: fa fa fa fa fa fa fa fa fd fd[fd]fd fd fd fd fd  

0x0c247fff8c10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff8c20: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c247fff8c30: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c247fff8c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c247fff8c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

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

==7258==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-395131  

Operating System: linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o242=document.createElement('html');
o1084=(new DOMParser()).parseFromString(unescape('%3E'),'text/html');
o1087=o1084.all[2];
o242.innerHTML='x<style>\\*{ display: list-item} @keyframes key8 { from{ float: right}} .class2{} \\* { animation-name: key8; animation-duration: 0.001s;>';
o1140=o242.querySelectorAll('\\*')[1];
o1087.innerHTML="<style>@font-face{} \\*{ all: initial;>";
document.body=o1140;
document.head.getBoundingClientRect();
document.body=o1087;
o1087.style.writingMode='vertical-rl';
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2016-05-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6508315777695744

### cl...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-05-27)

robhogan: Can you please take a look? Thanks.

[Monorail components: Blink>Layout]

### me...@chromium.org (2016-05-27)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-05-28)

kojii: this looks like it's related to https://codereview.chromium.org/1549153002 (possibly same root cause as 604095).

Passing over to you!

### sh...@chromium.org (2016-05-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-28)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-05-29)

Thanks robhogan@.

m_floatingObjects.m_lowestFloatBottomCache[0] has nullptr and [1] has a detached LayoutObject. I suppose these must be cleared when LayoutObject was deleted/detached, but haven't figured out why yet.

### ro...@chromium.org (2016-05-29)

kojii: my guess is that you are accessing a float object that has been deleted but has not yet been removed from the float lists. Layout makes an assumption about floats: that if you are laying out an object any floats in the float list exist. If they were deleted then they would have been removed from the float lists when the object's ancestor was laid out.

layoutOrthogonalWritingModeRoots() violates this assumption because it lays out parts of the tree 'out of DOM order'. However it should be safe for layoutOrthogonalWritingModeRoots() to violate the assumption because floats do not intrude across formatting contexts and a writing mode root creates a new formatting context.

So what I suspect is happening here is that a writing mode root has become 'not a writing mode root' or vice versa. When laying out the root you are trying to access a float in the root's float lists that no longer belongs there (because no floats outside its own formatting context should be in its float lists). The fact that the float has been deleted is what causes the crash but it shouldn't be in your list anyway.

When changing writing mode on an object we should be clearing down its float lists before layout maybe? Or it could be that you need to skip subtree layout on this item and let it take part in normal layout?

Hopefully these suggestions help - I do suspect https://crbug.com/chromium/604095 is a dupe of this.


### ko...@chromium.org (2016-05-29)

Thanks for the info. Yeah, by looking into this, I think I started to understand how we layout floats. I'm sending a WIP patch, not sure if I do the right thing for floats but at least prevents the assert and use-after-free.

Though writing-mode roots create a new BFC, when it's an inline-block and it has floating siblings, its containing block keeping detached objects doesn't look good.

In this case, we can't exclude from the layoutOrthogonalWritingModeRoots() list because computing preferred width of the parent of orthogonal inline block requires its logical height. We can probably clear the float list before layoutOrthogonalWritingModeRoots() to pre-compute logical height (which is the logical width for its parent), if my understanding that ancestors re-create float list when it layouts is correct.

Appreciate for you to look at the WIP.

### ko...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-06-06)

Assigning to kojii@chromium.org as this is an issue with orthogonal layout.

### ro...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fac93418b4bcf2f8c7480696567db3e2d12d467b

commit fac93418b4bcf2f8c7480696567db3e2d12d467b
Author: kojii <kojii@chromium.org>
Date: Tue Jun 07 22:19:35 2016

Remove floats from LayoutView in removeFloatingOrPositionedChildFromBlockLists

This patch fixes removeFloatingOrPositionedChildFromBlockLists fails to
remove floats when their containing block is LayoutView.

BUG=613869

Review-Url: https://codereview.chromium.org/2042353002
Cr-Commit-Position: refs/heads/master@{#398399}

[add] https://crrev.com/fac93418b4bcf2f8c7480696567db3e2d12d467b/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats-expected.txt
[add] https://crrev.com/fac93418b4bcf2f8c7480696567db3e2d12d467b/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats.html
[modify] https://crrev.com/fac93418b4bcf2f8c7480696567db3e2d12d467b/third_party/WebKit/Source/core/layout/LayoutBox.cpp


### cl...@chromium.org (2016-06-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6508315777695744

Uploader: lgarron@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000047750
Crash State:
  blink::ShapeOutsideInfo::isEnabledFor
  blink::LayoutBox::shapeOutsideInfo
  blink::ComputeFloatOffsetForLineLayoutAdapter<
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=374097:374217

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97OP2PBVqNR0Hk5ckrvjihbyUfIiv7P8-rA27yb3ga1sbs0m4wMnUa5zqmrQEP9da0aZhuiPP5pl68J8VOJESzkjFurOEKv2_PUeIt5IjBbSX4O5Q7t_Xi2w60V_g_YNo-nLgIddlFRoVGCvbzxuvYs5RsJww

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-08)

ClusterFuzz has detected this issue as fixed in range 398351:398496.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6508315777695744

Uploader: lgarron@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000047750
Crash State:
  blink::ShapeOutsideInfo::isEnabledFor
  blink::LayoutBox::shapeOutsideInfo
  blink::ComputeFloatOffsetForLineLayoutAdapter<
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=374097:374217
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=398351:398496

Minimized Testcase (0.57 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97OP2PBVqNR0Hk5ckrvjihbyUfIiv7P8-rA27yb3ga1sbs0m4wMnUa5zqmrQEP9da0aZhuiPP5pl68J8VOJESzkjFurOEKv2_PUeIt5IjBbSX4O5Q7t_Xi2w60V_g_YNo-nLgIddlFRoVGCvbzxuvYs5RsJww

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ko...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-09)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-10)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### sh...@chromium.org (2016-06-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db32c89564e79897cb949d6d8fb714c5068341f9

commit db32c89564e79897cb949d6d8fb714c5068341f9
Author: Koji Ishii <kojii@chromium.org>
Date: Tue Jun 14 07:31:38 2016

Remove floats from LayoutView in removeFloatingOrPositionedChildFromBlockLists

This patch fixes removeFloatingOrPositionedChildFromBlockLists fails to
remove floats when their containing block is LayoutView.

BUG=613869

Review-Url: https://codereview.chromium.org/2042353002
Cr-Commit-Position: refs/heads/master@{#398399}
(cherry picked from commit fac93418b4bcf2f8c7480696567db3e2d12d467b)

Review URL: https://codereview.chromium.org/2064743003 .

Cr-Commit-Position: refs/branch-heads/2743@{#349}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats-expected.txt
[add] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats.html
[modify] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/Source/core/layout/LayoutBox.cpp


### ko...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/db32c89564e79897cb949d6d8fb714c5068341f9

commit db32c89564e79897cb949d6d8fb714c5068341f9
Author: Koji Ishii <kojii@chromium.org>
Date: Tue Jun 14 07:31:38 2016

Remove floats from LayoutView in removeFloatingOrPositionedChildFromBlockLists

This patch fixes removeFloatingOrPositionedChildFromBlockLists fails to
remove floats when their containing block is LayoutView.

BUG=613869

Review-Url: https://codereview.chromium.org/2042353002
Cr-Commit-Position: refs/heads/master@{#398399}
(cherry picked from commit fac93418b4bcf2f8c7480696567db3e2d12d467b)

Review URL: https://codereview.chromium.org/2064743003 .

Cr-Commit-Position: refs/branch-heads/2743@{#349}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats-expected.txt
[add] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/LayoutTests/fast/writing-mode/orthogonal-writing-modes-in-layoutview-with-floats.html
[modify] https://crrev.com/db32c89564e79897cb949d6d8fb714c5068341f9/third_party/WebKit/Source/core/layout/LayoutBox.cpp


### ti...@google.com (2016-06-15)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ko...@chromium.org (2016-06-16)

I don't know why https://crbug.com/chromium/613869#c25 was recorded; it's the same CL to M52 as #23, probably a bug in bugdroid. Fixed in trunk, merged to M52, requesting for M51.

This is quite rare to occur, can't reproduce without JS manipulating DOM, but the fix looks safe to me.

### aw...@chromium.org (2016-07-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

Congratulations - $3,000 for this one. Thanks as ever!

### sh...@chromium.org (2016-09-15)

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

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-03-25)

This issue was migrated from crbug.com/chromium/613869?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084359)*
