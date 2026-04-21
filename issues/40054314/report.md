# Security: heap-use-after-free in IsBox

| Field | Value |
|-------|-------|
| **Issue ID** | [40054314](https://issues.chromium.org/issues/40054314) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | vm...@chromium.org |
| **Created** | 2020-12-28 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version:  

Chromium 89.0.4356.6 (Developer Build) (64-bit)  

Revision: 8689d5f68d3ce081fb0b81230a4f316c03221418-refs/branch-heads/4356@{#11}  

Operating System: Linux-4.15.0-126-generic-x86\_64-with-Ubuntu-18.04-bionic

**REPRODUCTION CASE**

<meter></meter>

<iframe></iframe>
<style>
\\* {
all: initial;
content-visibility: hidden;
}
</style>
<script> window.addEventListener("load", () => {
document.caretRangeFromPoint();
})
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==26026==ERROR: AddressSanitizer: heap-use-after-free on address 0x613000128518 at pc 0x563e4327b4bf bp 0x7ffd103f0570 sp 0x7ffd103f0568  

READ of size 11 at 0x613000128518 thread T0  

#0 0x563e4327b4be in IsBox third\_party/blink/renderer/core/layout/layout\_object.h:3894  

#1 0x563e4327b4be in IsBox third\_party/blink/renderer/core/layout/layout\_object.h:1387  

#2 0x563e4327b4be in AllowFrom third\_party/blink/renderer/core/layout/layout\_box.h:2367  

#3 0x563e4327b4be in IsA<blink::LayoutBox, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:70  

#4 0x563e4327b4be in IsA<blink::LayoutBox, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:80  

#5 0x563e4327b4be in To<blink::LayoutBox, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:104  

#6 0x563e4327b4be in To<blink::LayoutBox, blink::LayoutObject> third\_party/blink/renderer/platform/wtf/casting.h:109  

#7 0x563e4327b4be in EndsOfNodeAreVisuallyDistinctPositions third\_party/blink/renderer/core/editing/visible\_units.cc:593  

#8 0x563e4327da7c in blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > blink::MostForwardCaretPosition<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) >(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule) third\_party/blink/renderer/core/editing/visible\_units.cc:873  

#9 0x563e4327b795 in blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > blink::MostBackwardOrForwardCaretPosition<blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > (\*)(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule)>(blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule, blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > (\*)(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule)) third\_party/blink/renderer/core/editing/visible\_units.cc:630  

#10 0x563e4327d254 in blink::MostForwardCaretPosition(blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule) third\_party/blink/renderer/core/editing/visible\_units.cc:936  

#11 0x563e430ae8a7 in blink::AdjustForEditingBoundary(blink::PositionWithAffinityTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&) third\_party/blink/renderer/core/editing/editing\_utilities.cc:1391  

#12 0x563e443c693c in CreatePositionWithAffinity third\_party/blink/renderer/core/layout/layout\_object.cc:4205  

#13 0x563e443c693c in CreatePositionWithAffinity third\_party/blink/renderer/core/layout/layout\_object.cc:4279  

#14 0x563e447a725e in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:234  

#15 0x563e441f0f90 in blink::LayoutBox::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/layout\_box.cc:6589  

#16 0x563e4408aed1 in blink::LayoutBlock::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/layout\_block.cc:1484  

#17 0x563e447a7204 in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:230  

#18 0x563e44060bd4 in blink::HitTestResult::GetPosition() const third\_party/blink/renderer/core/layout/hit\_test\_result.cc:193  

#19 0x563e42addeeb in blink::Document::caretRangeFromPoint(int, int) third\_party/blink/renderer/core/dom/document.cc:1712  

#20 0x563e4769d715 in blink::(anonymous namespace)::CaretRangeFromPointOperationCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/modules/v8/v8\_document.cc:4969  

#21 0x563e33e214ef in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158  

#22 0x563e33e1d708 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111  

#23 0x563e33e19e48 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141  

#24 0x563e33e18eec in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:129  

#25 0x563e36c8d8de in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit setup-isolate-deserialize.cc:?  

#26 0x563e369fe9ce in Builtins\_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?  

#27 0x563e369f517a in Builtins\_JSEntryTrampoline setup-isolate-deserialize.cc:?  

#28 0x563e369f4f57 in Builtins\_JSEntry setup-isolate-deserialize.cc:?  

#29 0x563e3419f583 in Call v8/src/execution/simulator.h:142  

#30 0x563e3419f583 in Invoke v8/src/execution/execution.cc:368  

#31 0x563e3419e355 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:462  

#32 0x563e33c1ae01 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:5118  

#33 0x563e45bb9216 in blink::V8ScriptRunner::CallFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/blink/renderer/bindings/core/v8/v8\_script\_runner.cc:632  

#34 0x563e45a7baf7 in blink::bindings::CallbackInvokeHelper<blink::CallbackInterfaceBase, (blink::bindings::CallbackInvokeHelperMode)0>::Call(int, v8::Local[v8::Value](javascript:void(0);)\*) third\_party/blink/renderer/bindings/core/v8/callback\_invoke\_helper.cc:129  

#35 0x563e46c7d30a in blink::V8EventListener::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::Event\*) gen/third\_party/blink/renderer/bindings/core/v8/v8\_event\_listener.cc:126  

#36 0x563e45a860bd in blink::JSBasedEventListener::Invoke(blink::ExecutionContext\*, blink::Event\*) third\_party/blink/renderer/bindings/core/v8/js\_based\_event\_listener.cc:150  

#37 0x563e42d1c9b5 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1u>&) third\_party/blink/renderer/core/dom/events/event\_target.cc:935  

#38 0x563e42d1ad5e in blink::EventTarget::FireEventListeners(blink::Event&) third\_party/blink/renderer/core/dom/events/event\_target.cc:849  

#39 0x563e4345eb7d in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget\*) third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1861  

#40 0x563e4345de46 in blink::LocalDOMWindow::DispatchLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:1823  

#41 0x563e4345d62d in blink::LocalDOMWindow::DispatchWindowLoadEvent() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:664  

#42 0x563e4345e2ce in blink::LocalDOMWindow::DocumentWasClosed() third\_party/blink/renderer/core/frame/local\_dom\_window.cc:668  

#43 0x563e42afdd58 in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3845  

#44 0x563e42afef06 in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3958  

#45 0x563e42b2e297 in CheckCompleted third\_party/blink/renderer/core/dom/document.cc:3932  

#46 0x563e42b2e297 in DecrementLoadEventDelayCountAndCheckLoadEvent third\_party/blink/renderer/core/dom/document.cc:7465  

#47 0x563e42e1a3ad in blink::IncrementLoadEventDelayCount::ClearAndCheckLoadEvent() third\_party/blink/renderer/core/dom/increment\_load\_event\_delay\_count.cc:26  

#48 0x563e43bf1663 in Invoke<void (blink::HTMLStyleElement::\*)(std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);), bool), blink::Persistent[blink::HTMLStyleElement](javascript:void(0);), std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);), bool> base/bind\_internal.h:498  

#49 0x563e43bf1663 in MakeItSo<void (blink::HTMLStyleElement::\*)(std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);), bool), blink::Persistent[blink::HTMLStyleElement](javascript:void(0);), std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);), bool> base/bind\_internal.h:637  

#50 0x563e43bf1663 in RunImpl<void (blink::HTMLStyleElement::\*)(std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);), bool), std::tuple<blink::Persistent[blink::HTMLStyleElement](javascript:void(0);), WTF::PassedWrapper<std::unique\_ptr[blink::IncrementLoadEventDelayCount](javascript:void(0);) >, bool>, 0, 1, 2> base/bind\_internal.h:710  

#51 0x563e43bf1663 in RunOnce base/bind\_internal.h:679  

#52 0x563e3720a11d in Run base/callback.h:101  

#53 0x563e3720a11d in RunInternal third\_party/blink/renderer/platform/wtf/functional.h:256  

#54 0x563e3720a11d in Run third\_party/blink/renderer/platform/wtf/functional.h:241  

#55 0x563e3af1c9f0 in Run base/callback.h:101  

#56 0x563e3af1c9f0 in RunTask base/task/common/task\_annotator.cc:163  

#57 0x563e3af712a0 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:199  

#58 0x563e3af75607 in Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:498  

#59 0x563e3af75607 in MakeItSo<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:657  

#60 0x563e3af75607 in RunImpl<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const std::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> &, 0, 1> base/bind\_internal.h:710  

#61 0x563e3af75607 in Run base/bind\_internal.h:692  

#62 0x563e3af1c9f0 in Run base/callback.h:101  

#63 0x563e3af1c9f0 in RunTask base/task/common/task\_annotator.cc:163  

#64 0x563e3af7d6c6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351  

#65 0x563e3af7cdcf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:264  

#66 0x563e3ae1dd03 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39  

#67 0x563e3af7f37c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:460  

#68 0x563e3aeb8dda in base::RunLoop::Run() base/run\_loop.cc:131  

#69 0x563e4bcfe77e in content::RenderViewTest::LoadHTMLWithUrlOverride(char const\*, char const\*) content/public/test/render\_view\_test.cc:381  

#70 0x563e2e271589 in LoadHTML content/test/fuzzer/fuzzer\_support.h:27  

#71 0x563e2e271589 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:22  

#72 0x563e2e272b18 in main testing/libfuzzer/unittest\_main.cc:57  

#73 0x7f893d7a8bf6 in \_\_libc\_start\_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310

0x613000128518 is located 24 bytes inside of 336-byte region [0x613000128500,0x613000128650)  

freed by thread T0 here:  

#0 0x563e2e2448e2 in \_\_interceptor\_free /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:127  

#1 0x563e4438c880 in Free base/allocator/partition\_allocator/partition\_root.h:673  

#2 0x563e4438c880 in operator delete third\_party/blink/renderer/core/layout/layout\_object.cc:240  

#3 0x563e443c643f in blink::LayoutObject::Destroy() third\_party/blink/renderer/core/layout/layout\_object.cc:3826  

#4 0x563e443c6169 in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers() layout\_object.cc:?  

#5 0x563e42da53d3 in blink::Node::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/node.cc:1714  

#6 0x563e42c3b542 in blink::Element::DetachLayoutTree(bool) element.cc:?  

#7 0x563e42a818bd in blink::ContainerNode::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/container\_node.cc:1014  

#8 0x563e42c3b534 in blink::Element::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/element.cc:2807  

#9 0x563e42a818bd in blink::ContainerNode::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/container\_node.cc:1014  

#10 0x563e42c3b534 in blink::Element::DetachLayoutTree(bool) third\_party/blink/renderer/core/dom/element.cc:2807  

#11 0x563e42da4968 in blink::Node::ReattachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/node.cc:1679  

#12 0x563e42c43106 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:3163  

#13 0x563e42a8660a in blink::ContainerNode::RebuildLayoutTreeForChild(blink::Node\*, blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1378  

#14 0x563e42a869ca in blink::ContainerNode::RebuildChildrenLayoutTrees(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/container\_node.cc:1403  

#15 0x563e42c43428 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:3192  

#16 0x563e4293af00 in blink::StyleEngine::RebuildLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:2071  

#17 0x563e4293c4d7 in blink::StyleEngine::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:2110  

#18 0x563e42aee703 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2540  

#19 0x563e42ade9f6 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2493  

#20 0x563e42af049b in blink::Document::UpdateStyleAndLayoutTreeForNode(blink::Node const\*) third\_party/blink/renderer/core/dom/document.cc:2646  

#21 0x563e45e24d28 in blink::HTMLMeterElement::CanContainRangeEndPoint() const third\_party/blink/renderer/core/html/html\_meter\_element.cc:223  

#22 0x563e4327b29f in CanHaveChildrenForEditing third\_party/blink/renderer/core/editing/editing\_utilities.h:155  

#23 0x563e4327b29f in EndsOfNodeAreVisuallyDistinctPositions third\_party/blink/renderer/core/editing/visible\_units.cc:592  

#24 0x563e4327da7c in blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > blink::MostForwardCaretPosition<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) >(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule) third\_party/blink/renderer/core/editing/visible\_units.cc:873  

#25 0x563e4327b795 in blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > blink::MostBackwardOrForwardCaretPosition<blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > (\*)(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule)>(blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule, blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > (\*)(blink::PositionTemplate<blink::EditingAlgorithm[blink::FlatTreeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule)) third\_party/blink/renderer/core/editing/visible\_units.cc:630  

#26 0x563e4327d254 in blink::MostForwardCaretPosition(blink::PositionTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&, blink::EditingBoundaryCrossingRule) third\_party/blink/renderer/core/editing/visible\_units.cc:936  

#27 0x563e430ae8a7 in blink::AdjustForEditingBoundary(blink::PositionWithAffinityTemplate<blink::EditingAlgorithm[blink::NodeTraversal](javascript:void(0);) > const&) third\_party/blink/renderer/core/editing/editing\_utilities.cc:1391  

#28 0x563e443c693c in CreatePositionWithAffinity third\_party/blink/renderer/core/layout/layout\_object.cc:4205  

#29 0x563e443c693c in CreatePositionWithAffinity third\_party/blink/renderer/core/layout/layout\_object.cc:4279  

#30 0x563e447a725e in blink::LayoutNGBlockFlowMixin[blink::LayoutBlockFlow](javascript:void(0);)::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/ng/layout\_ng\_block\_flow\_mixin.cc:234  

#31 0x563e441f0f90 in blink::LayoutBox::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/layout\_box.cc:6589  

#32 0x563e4408aed1 in blink::LayoutBlock::PositionForPoint(blink::PhysicalOffset const&) const third\_party/blink/renderer/core/layout/layout\_block.cc:1484

previously allocated by thread T0 here:  

#0 0x563e2e244b4d in \_\_interceptor\_malloc /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:145  

#1 0x563e4438c5e8 in AllocFlags base/allocator/partition\_allocator/partition\_root.h:947  

#2 0x563e4438c5e8 in Alloc base/allocator/partition\_allocator/partition\_root.h:1178  

#3 0x563e4438c5e8 in operator new third\_party/blink/renderer/core/layout/layout\_object.cc:234  

#4 0x563e443f8420 in CreateObject<blink::LayoutBlockFlow, blink::LayoutNGBlockFlow, blink::LayoutBlockFlow> third\_party/blink/renderer/core/layout/layout\_object\_factory.cc:93  

#5 0x563e443f8420 in CreateBlockFlow third\_party/blink/renderer/core/layout/layout\_object\_factory.cc:114  

#6 0x563e4438ce71 in blink::LayoutObject::CreateObject(blink::Element\*, blink::ComputedStyle const&, blink::LegacyLayout) third\_party/blink/renderer/core/layout/layout\_object.cc:285  

#7 0x563e42d4ce43 in blink::LayoutTreeBuilderForElement::CreateLayoutObject() third\_party/blink/renderer/core/dom/layout\_tree\_builder.cc:86  

#8 0x563e42c3917c in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2718  

#9 0x563e42a81706 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007  

#10 0x563e42c39563 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2752  

#11 0x563e42a81706 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007  

#12 0x563e42c39563 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2752  

#13 0x563e42a81706 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/container\_node.cc:1007  

#14 0x563e42c39563 in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/element.cc:2752  

#15 0x563e43b85158 in blink::HTMLHtmlElement::AttachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/html/html\_html\_element.cc:173  

#16 0x563e42da499c in blink::Node::ReattachLayoutTree(blink::Node::AttachContext&) third\_party/blink/renderer/core/dom/node.cc:1680  

#17 0x563e42c43106 in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) third\_party/blink/renderer/core/dom/element.cc:3163  

#18 0x563e4293af00 in blink::StyleEngine::RebuildLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:2071  

#19 0x563e4293c4d7 in blink::StyleEngine::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/css/style\_engine.cc:2110  

#20 0x563e42aee703 in blink::Document::UpdateStyle() third\_party/blink/renderer/core/dom/document.cc:2540  

#21 0x563e42ade9f6 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2493  

#22 0x563e42ade3d9 in blink::Document::UpdateStyleAndLayoutTree() third\_party/blink/renderer/core/dom/document.cc:2427  

#23 0x563e42b25cac in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:7010  

#24 0x563e46b0e113 in blink::HTMLConstructionSite::FinishedParsing() third\_party/blink/renderer/core/html/parser/html\_construction\_site.cc:631  

#25 0x563e46c459dc in blink::HTMLTreeBuilder::Finished() third\_party/blink/renderer/core/html/parser/html\_tree\_builder.cc:2958  

#26 0x563e46aceed8 in blink::HTMLDocumentParser::end() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1289  

#27 0x563e46abc3de in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1304  

#28 0x563e46abb4ee in blink::HTMLDocumentParser::PrepareToStopParsing() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:516  

#29 0x563e46acf580 in blink::HTMLDocumentParser::AttemptToEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1322  

#30 0x563e46ad0037 in blink::HTMLDocumentParser::Finish() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1384  

#31 0x563e44badfe6 in blink::DocumentLoader::FinishedLoading(base::TimeTicks) third\_party/blink/renderer/core/loader/document\_loader.cc:759  

#32 0x563e44bb61c5 in blink::DocumentLoader::StartLoadingResponse() document\_loader.cc:?

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/blink/renderer/core/layout/layout\_object.h:3894 in IsBox  

Shadow bytes around the buggy address:  

0x0c268001d050: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c268001d060: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c268001d070: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268001d080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268001d090: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c268001d0a0: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268001d0b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268001d0c0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c268001d0d0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c268001d0e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c268001d0f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==26026==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Renata Hodovan  

This issue was found by the Grammarinator fuzzer.

## Attachments

- [uaf_isbox.html](attachments/uaf_isbox.html) (text/plain, 200 B)
- [windows.asan](attachments/windows.asan) (application/octet-stream, 19.7 KB)

## Timeline

### [Deleted User] (2020-12-28)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-28)

Thanks. This repros immediately on Windows.

CC'ing some layout owners. I will attempt to bisect but assigning impact=stable for now.

[Monorail components: Blink>Layout]

### wa...@chromium.org (2020-12-28)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Layout Blink>Editing]

### aj...@google.com (2020-12-29)

(I do not have time to bisect, sorry!) It would be great for this bug to have an owner!

### wa...@chromium.org (2020-12-29)

I guess the bug will go through Blink>Editing triage process when the owners come back to work.


### at...@chromium.org (2020-12-29)

Looks like an editing edge case.
Several things are unusual when you run this in gdb:
It hits a DCHECK. 
PositionTemplate<Strategy> MostBackwardCaretPosition
   Check failed: !NeedsLayoutTreeUpdate(position). BODY@offsetInAnchor[0]

BODY is LayoutInline.

### [Deleted User] (2020-12-29)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2020-12-29)

Adding pcupp@ for Editing triage.

### pc...@microsoft.com (2021-01-05)

Anupam, can you take a look?  This is a security issue.  I'm assigning you as the owner.

### pc...@microsoft.com (2021-01-05)

[Empty comment from Monorail migration]

### sn...@microsoft.com (2021-01-05)

I'm not able to repro this on 87.0.4280.88 (Official Build) (64-bit) (cohort: Stable)
The page loads successfully and when I query for document.caretRangeFromPoint() after the page loads, I get Range {startContainer: body, startOffset: 2, endContainer: body, endOffset: 2, collapsed: true, …}. 
However, I'm able to hit the DCHECK as mentioned in https://crbug.com/chromium/1162131#c6 when I run it in a debug build. Can someone please confirm if this is still an issue on 87 stable?




### sn...@microsoft.com (2021-01-05)

Also tried on 89.0.4379.0 (Official Build) canary (64-bit) (cohort: Clang-64) Windows 10 OS Version 2009 (Build 19042.685) and not able to repro, but it does repro on debug builds so I guess I'll debug that..

### sn...@microsoft.com (2021-01-05)

OK so I was able to get callstacks for this UAF bug in a Win ASAN build and I think I have a pretty good idea why the crash happens, but I'm not familiar enough with style recalc and layout object lifetimes, so I'm adding few layout folks that have made changes in this area who might be able to suggest something here.

In |EndsOfNodeAreVisuallyDistinctPositions|, we get the LayoutObject (just a raw pointer) from the Node that was passed into this function. In this sample repro page, the node that was passed into |EndsOfNodeAreVisuallyDistinctPositions| is a <meter> element. In this function we call |CanHaveChildrenForEditing| and for <meter> element we check for |node->CanContainRangeEndPoint| in |CanHaveChildrenForEditing| which in turn invokes |Document::UpdateStyleAndLayoutTreeForNode| that eventually destroys the LayoutObject because of content-visibility set to hidden. When this call returns, we check whether the LayoutObject's box size is empty or not and in this call UAF happens.

### sc...@chromium.org (2021-01-06)

Can you re-order the calls to get the box size before calling CanHaveChildrenForEditing? It might be a stale box, but that's better than this.

Or can you refresh the LayoutObject pointer from the node after CanHaveChildrenForEditing returns?

### vm...@chromium.org (2021-01-06)

I think we have to early out the hit testing algorithm earlier, since we seem to be returning items in a content-visibility: hidden subtree which can be in a layout-dirty state. We have an early out when we hit test children, but that doesn't seem to be sufficient. I'm investigating and will update this bug

### sn...@microsoft.com (2021-01-06)

Re https://crbug.com/chromium/1162131#c14 yes, I did try that solution to verify my analysis and it worked, but that doesn't fix the underlying problem of Positions ending up in an "invalid" node after a style recalc. Also this issue is not just a problem in the hit testing algorithm. This can occur anytime we run layout and there is a cache object that relies on the positions to be somewhat immutable. e.g. in editing commands (backspace, InsertParagraphSeparator etc) we operate on "visible" positions and it could be stale after a style recalc, but the commands are not resilient to this kind of operation. I guess this is more of a philosophical question, but I have never found a clean solution to this problem so we ended up checking for dirty positions and bail out from the algorithm if it doesn't meet a certain criteria (in the editing commands we check if the nodes are still connected to the tree or are invalid etc). I'll discuss with yosin@ offline regarding this issue, but fixing the hit testing logic should fix this bug too.

### vm...@chromium.org (2021-01-06)

For the particular case here, I think the solution is something like this: https://chromium-review.googlesource.com/c/chromium/src/+/2611453

However, for #14 and #16, I'm not sure how to improve the robustness of editing while in content visibility. We have added a lot of early out conditions in editing, but the general principle is that if we're trying to do something with a node for which DisplayLockUtilities::NearestLockedExclusiveAncestor(*node) turns non-null, then we're in a locked subtree and we shouldn't do anything with this node as its style and layout information can be out of date. This node would not be visible and should not be hit-testable. Any code that _does_ need to access it (e.g. getComputedStyle) needs to ensure to update the state first, via something like UpdateStyleAndLayoutTreeForNode, which updates the state even if it is in a locked subtree.


### vm...@chromium.org (2021-01-06)

The CL in https://crbug.com/chromium/1162131#c17 addresses the DCHECK (which is the only thing I could reproduce), it would be awesome if someone could verify that it also addresses the UaF

### sn...@microsoft.com (2021-01-06)

vmpstr@ Thank you for the clarification. I built your changes in https://crbug.com/chromium/1162131#c17 and verified in Win ASAN build that it did fix this UaF issue!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8483cf6944e38203c3b247163c54cfa105e89c56

commit 8483cf6944e38203c3b247163c54cfa105e89c56
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Wed Jan 06 19:56:20 2021

content-visibility: Don't adjust position of a locked hittest result node.

This patch ensures that if we have a hittest result that has a locked
node, we don't try to recurse into its subtree. This can happen when we
do a PositionWithAffinity check.

R=chrishtr@chromium.org

Bug: 1162131
Change-Id: I357bd7032c6c2b6c9405bf26c49a36bda22d6a0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2611453
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: vmpstr <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#840727}

[add] https://crrev.com/8483cf6944e38203c3b247163c54cfa105e89c56/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/content-visibility-080.html
[modify] https://crrev.com/8483cf6944e38203c3b247163c54cfa105e89c56/third_party/blink/renderer/core/layout/hit_test_result.cc


### vm...@chromium.org (2021-01-06)

I think we need to merge this to 88, but I'll wait until we can verify the fix in Canary

### sc...@chromium.org (2021-01-06)

Just FYI the cut-off for the next M-88 Beta is this afternoon. Consider whether this is a serious enough issue to delay the release. I personally don't think so but we're only 12 days before Stable so you might not get a chance for any Beta testing if you miss this one.

+srinivassista@ (M88 Release TPM)

### vm...@chromium.org (2021-01-06)

That's a good point. Unfortunately, I'm not in a good position to make an assessment of whether this is severe enough or not. FWIW, I think the patch is fairly safe.

### vm...@chromium.org (2021-01-06)

Requesting a merge to 88 for patch in https://crbug.com/chromium/1162131#c20. For context, this is fixing a UaF bug. As I mentioned in https://crbug.com/chromium/1162131#c23, I think the patch is safe but I think security team should make an assessment whether this is severe enough for the merge.

### [Deleted User] (2021-01-06)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@chromium.org (2021-01-06)

1. Unsure, I think the security team should make the assessment if this bug is severe enough.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2611453
3. The change has landed and has been verified on ToT. It has _not_ been verified in Canary yet.
4. No
5. UaF bug fix
6. No
7. No

### go...@chromium.org (2021-01-06)

+adetaylor@ (Security TPM) for M88 merge review.  CL: https://chromium-review.googlesource.com/c/chromium/src/+/2611453  landed 1 hr back not in canary yet. 

### ho...@gmail.com (2021-01-06)

Not sure whether this is useful information at this point, but my local release ASAN build of the official stable version just finished and that chrome binary reproduces the UAF (with the default runtime settings), too.

Chromium	87.0.4280.88 (Developer Build) (64-bit)
Revision	89e2380a3e36c3464b5dd1302349b1382549290d-refs/branch-heads/4280@{#1761}
OS	Linux (Ubuntu 20.04.1, x86_64)

Build setup: 

gn gen out/FuzzerRelease --args="is_debug=false is_asan=true dcheck_always_on=false symbol_level=1 blink_symbol_level=1 enable_nacl=false"
ninja -C out/FuzzerRelease chrome



### ad...@chromium.org (2021-01-06)

I'd like to wait for at least a day of canary data before approving merge to M88, but yes, we'll merge to M88 - thanks for the answers in https://crbug.com/chromium/1162131#c26. We just missed the last M87 refresh today.

### ho...@gmail.com (2021-01-07)

In the meantime I checked the stable release with version 87.0.4280.141 from yesterday with the build setup in #28 and it reproduces for me.

### vm...@chromium.org (2021-01-07)

I've verified the latest Canary seems to have fixed the issue. Specifically, the return of document.caretRangeFromPoint() call returns the expected new value instead of recursing into structures that caused the initial problem.

### ad...@chromium.org (2021-01-07)

OK. I'm approving merge to M88, branch 4324, but please wait until the fix has been out in Canary for 24 hours in case of any unforeseen problems that may be reported.

Please also mark this as Fixed - for security bugs, we normally mark them as Fixed before merges occur.

### vm...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### vm...@chromium.org (2021-01-08)

I have the merge here: https://chromium-review.googlesource.com/c/chromium/src/+/2618603 waiting for the trybots to turn green. Also if someone could rubberstamp it, I'd appreciate it

### go...@chromium.org (2021-01-08)

+1ed M88 merge CL - https://chromium-review.googlesource.com/c/chromium/src/+/2618603

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3f7b67374a1121b6756ccfd2e4e414987f167489

commit 3f7b67374a1121b6756ccfd2e4e414987f167489
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Sat Jan 09 01:26:39 2021

content-visibility: Don't adjust position of a locked hittest result node.

This patch ensures that if we have a hittest result that has a locked
node, we don't try to recurse into its subtree. This can happen when we
do a PositionWithAffinity check.

R=chrishtr@chromium.org

(cherry picked from commit 8483cf6944e38203c3b247163c54cfa105e89c56)

Bug: 1162131
Change-Id: I357bd7032c6c2b6c9405bf26c49a36bda22d6a0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2611453
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: vmpstr <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#840727}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618603
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1566}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[add] https://crrev.com/3f7b67374a1121b6756ccfd2e4e414987f167489/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/content-visibility-080.html
[modify] https://crrev.com/3f7b67374a1121b6756ccfd2e4e414987f167489/third_party/blink/renderer/core/layout/hit_test_result.cc


### ac...@chromium.org (2021-01-10)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d74ba931c4b75858b36b0e97b6853579a6f7c510

commit d74ba931c4b75858b36b0e97b6853579a6f7c510
Author: Achuith Bhandarkar <achuith@chromium.org>
Date: Wed Jan 13 21:27:05 2021

content-visibility: Don't adjust position of a locked hittest result node.

This patch ensures that if we have a hittest result that has a locked
node, we don't try to recurse into its subtree. This can happen when we
do a PositionWithAffinity check.

R=chrishtr@chromium.org

(cherry picked from commit 8483cf6944e38203c3b247163c54cfa105e89c56)

(cherry picked from commit 3f7b67374a1121b6756ccfd2e4e414987f167489)

Bug: 1162131
Change-Id: I357bd7032c6c2b6c9405bf26c49a36bda22d6a0d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2611453
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: vmpstr <vmpstr@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#840727}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618603
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4324@{#1566}
Cr-Original-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618982
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1520}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[add] https://crrev.com/d74ba931c4b75858b36b0e97b6853579a6f7c510/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/content-visibility-080.html
[modify] https://crrev.com/d74ba931c4b75858b36b0e97b6853579a6f7c510/third_party/blink/renderer/core/layout/hit_test_result.cc


### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to reward you $5000 for this report. Thank you and nice job!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2021-01-19)

I see M-89, M-88 and M-86 commits, but nothing for M-87. Is that expected? https://crbug.com/chromium/1162131#c30 seem to imply its necessary, although there's only a couple of days before we start shipping M-88 so it's probably not worth it.

### ad...@chromium.org (2021-01-19)

It was a bit too late for the final M87 security refresh. The first M88 release comes out tomorrow.

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1162131?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054314)*
