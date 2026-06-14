# Security: SEGV in blink::DOMWindowV8Internal::blurMethodCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40084766](https://issues.chromium.org/issues/40084766) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Input, Blink>JavaScript |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2016-07-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The following testcase crashes the latest asan build of chrome. Often with a null pointer, however I see SEGV's on other addresses during fuzzing which is likely due to the same root cause. Other global functions (close, focus, etc.) are also affected.

ASAN null pointer:

# ASAN:DEADLYSIGNAL

==19627==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x7f8b2a0e44fe bp 0x7fff0ca636d0 sp 0x7fff0ca636c0 T0)  

==19627==The signal is caused by a READ memory access.  

==19627==Hint: address points to the zero page.  

#0 0x7f8b2a0e44fd in blurMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4207:11  

#1 0x7f8b2a0e44fd in blink::DOMWindowV8Internal::blurMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4212  

#2 0x7f8b24efef11 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#3 0x7f8b23c96105 in HandleApiCallHelper<true> v8/src/builtins.cc:5311:36  

#4 0x7f8b23c96105 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins.cc:5337  

#5 0x7f8962206146 (<unknown module>)  

#6 0x7f8962242147 (<unknown module>)  

#7 0x7f896226c668 (<unknown module>)  

#8 0x7f8962242262 (<unknown module>)  

#9 0x7f8962225d6e (<unknown module>)  

#10 0x7f8b242b8892 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#11 0x7f8b242b826c in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:155:10  

#12 0x7f8b23b00d4d in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1871:23  

#13 0x7f8b29a1f8d0 in blink::V8ScriptRunner::runCompiledScript(v8::Isolate\*, v8::Local[v8::Script](javascript:void(0);), blink::ExecutionContext\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:414:26  

#14 0x7f8b29931474 in blink::ScriptController::executeScriptAndReturnValue(v8::Local[v8::Context](javascript:void(0);), blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:164:21  

#15 0x7f8b29937708 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:410:35  

#16 0x7f8b29937e0c in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double\*) third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:388:5  

#17 0x7f8b3309091c in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double\*) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:427:21  

#18 0x7f8b33088395 in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third\_party/WebKit/Source/core/dom/ScriptLoader.cpp:273:14  

#19 0x7f8b279244d1 in blink::HTMLScriptRunner::runScript(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:423:23  

#20 0x7f8b27923a82 in blink::HTMLScriptRunner::execute(blink::Element\*, WTF::TextPosition const&) third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:276:5  

#21 0x7f8b278d8153 in runScriptsForPausedTreeBuilder third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:267:25  

#22 0x7f8b278d8153 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::ParsedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);) >) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:483  

#23 0x7f8b278d0d48 in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:540:36  

#24 0x7f8b2790130e in Invoke<blink::WeakPersistent[blink::HTMLParserScheduler](javascript:void(0);)> base/bind\_internal.h:137:12  

#25 0x7f8b2790130e in MakeItSo<void (blink::HTMLParserScheduler::\*const &)(), blink::WeakPersistent[blink::HTMLParserScheduler](javascript:void(0);)> base/bind\_internal.h:224  

#26 0x7f8b2790130e in RunImpl<void (blink::HTMLParserScheduler::\*const &)(), const std::\_\_1::tuple<blink::WeakPersistent[blink::HTMLParserScheduler](javascript:void(0);) > &, 0> base/bind\_internal.h:267  

#27 0x7f8b2790130e in base::internal::Invoker<base::internal::BindState<void (blink::HTMLParserScheduler::\*)(), blink::WeakPersistent[blink::HTMLParserScheduler](javascript:void(0);) >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#28 0x7f8b33e767f5 in Invoke<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:90:12  

#29 0x7f8b33e767f5 in MakeItSo<void (\*const &)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > base/bind\_internal.h:204  

#30 0x7f8b33e767f5 in RunImpl<void (\*const &)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), const std::\_\_1::tuple<base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > > &, 0> base/bind\_internal.h:267  

#31 0x7f8b33e767f5 in base::internal::Invoker<base::internal::BindState<void (\*)(std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#32 0x7f8b1fcf9c21 in Run base/callback.h:389:12  

#33 0x7f8b1fcf9c21 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#34 0x7f8b33e91cfc in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:291:19  

#35 0x7f8b33e8da73 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:203:13  

#36 0x7f8b33e94127 in Invoke<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:137:12  

#37 0x7f8b33e94127 in MakeItSo<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:224  

#38 0x7f8b33e94127 in RunImpl<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), const std::\_\_1::tuple<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool> &, 0, 1, 2> base/bind\_internal.h:267  

#39 0x7f8b33e94127 in base::internal::Invoker<base::internal::BindState<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#40 0x7f8b1fcf9c21 in Run base/callback.h:389:12  

#41 0x7f8b1fcf9c21 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#42 0x7f8b1fb7c1e5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:493:19  

#43 0x7f8b1fb7cfdf in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:502:5  

#44 0x7f8b1fb7e4bc in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:624:13  

#45 0x7f8b1fb886cd in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:35:31  

#46 0x7f8b1fbeb7c9 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#47 0x7f8b1fb79758 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:295:12  

#48 0x7f8b2e210f1c in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:197:37  

#49 0x7f8b1fa2ab87 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:343:14  

#50 0x7f8b1fa2f235 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:785:12  

#51 0x7f8b1fa2991d in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#52 0x7f8b1e94d5e5 in ChromeMain chrome/app/chrome\_main.cc:84:12  

#53 0x7f8b13dfcf44 in \_\_libc\_start\_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4207:11 in blurMethod  

==19627==ABORTING

other SEGV:

=================================================================  

==26422==ERROR: AddressSanitizer: SEGV on unknown address 0x001072c77043 (pc 0x0000098813c8 bp 0x7fff6be2b190 sp 0x7fff6be2b180 T0)  

==26422==The signal is caused by a READ memory access.  

#0 0x98813c7 in blurMethod /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4207:11  

#1 0x98813c7 in blink::DOMWindowV8Internal::blurMethodCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4212  

#2 0x3f84311 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#3 0x2d1bb65 in HandleApiCallHelper<true> v8/src/builtins.cc:5311:36  

#4 0x2d1bb65 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins.cc:5337  

#5 0x7f9640306146 (<unknown module>)  

#6 0x7f9640342147 (<unknown module>)  

#7 0x7f9640635844 (<unknown module>)  

#8 0x7f9640307cb4 (<unknown module>)  

#9 0x7f96405dc0d1 (<unknown module>)  

#10 0x7f964053f68d (<unknown module>)  

#11 0x7f9640443ed8 (<unknown module>)  

#12 0x7f964054ec6d (<unknown module>)  

#13 0x7f964053d099 (<unknown module>)  

#14 0x7f96405120c1 (<unknown module>)  

#15 0x7f964052b8d2 (<unknown module>)  

#16 0x7f9640307cb4 (<unknown module>)  

#17 0x7f9640342262 (<unknown module>)  

#18 0x7f9640325d6e (<unknown module>)  

#19 0x333e332 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:98:13  

#20 0x333dd0c in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:155:10  

#21 0x2bc8ec4 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4553:7  

#22 0x91be74b in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:510:28  

#23 0x922f3c9 in blink::V8FrameRequestCallback::handleEvent(double) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8FrameRequestCallback.cpp:52:5  

#24 0x6740f8e in blink::FrameRequestCallbackCollection::executeCallbacks(double, double) third\_party/WebKit/Source/core/dom/FrameRequestCallbackCollection.cpp:70:27  

#25 0x6866563 in executeCallbacks third\_party/WebKit/Source/core/dom/ScriptedAnimationController.cpp:135:26  

#26 0x6866563 in blink::ScriptedAnimationController::serviceScriptedAnimations(double) third\_party/WebKit/Source/core/dom/ScriptedAnimationController.cpp:163  

#27 0x80c4f97 in blink::PageAnimator::serviceScriptedAnimations(double) third\_party/WebKit/Source/core/page/PageAnimator.cpp:70:19  

#28 0x49bff78 in blink::WebViewImpl::beginFrame(double) third\_party/WebKit/Source/web/WebViewImpl.cpp:1999:5  

#29 0xbd8b5e3 in BeginMainFrame content/renderer/gpu/render\_widget\_compositor.cc:1008:14  

#30 0xbd8b5e3 in non-virtual thunk to content::RenderWidgetCompositor::BeginMainFrame(cc::BeginFrameArgs const&) content/renderer/gpu/render\_widget\_compositor.cc:1005  

#31 0xd135fe7 in cc::ProxyMain::BeginMainFrame(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:190:21  

#32 0xd16ab13 in Invoke<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:137:12  

#33 0xd16ab13 in MakeItSo<void (cc::ProxyMain::\*const &)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:224  

#34 0xd16ab13 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::RunImpl<void (cc::ProxyMain::\* const&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > const&, 0ul, 1ul>(void (cc::ProxyMain::\* const&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > const&, base::IndexSequence<0ul, 1ul>) base/bind\_internal.h:267  

#35 0x830611 in Run base/callback.h:389:12  

#36 0x830611 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#37 0x100e5a7c in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:291:19  

#38 0x100e17f3 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:203:13  

#39 0x100e7ea7 in Invoke<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:137:12  

#40 0x100e7ea7 in MakeItSo<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:224  

#41 0x100e7ea7 in RunImpl<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), const std::\_\_1::tuple<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool> &, 0, 1, 2> base/bind\_internal.h:267  

#42 0x100e7ea7 in base::internal::Invoker<base::internal::BindState<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:245  

#43 0x830611 in Run base/callback.h:389:12  

#44 0x830611 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#45 0x6e43d5 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:493:19  

#46 0x6e51cf in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:502:5  

#47 0x6e6e02 in base::MessageLoop::DoDelayedWork(base::TimeTicks\*) base/message\_loop/message\_loop.cc:662:10  

#48 0x6f06e1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:27  

#49 0x73a869 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#50 0x6e1998 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:295:12  

#51 0xba33fac in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:197:37  

#52 0x6487b7 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:343:14  

#53 0x64cf25 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:785:12  

#54 0x64754d in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#55 0x50d1d2 in main content/shell/app/shell\_main.cc:48:10  

#56 0x7f97f1e7bf44 in \_\_libc\_start\_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8Window.cpp:4207:11 in blurMethod  

==26422==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-403751/  

Operating System: Linux

**REPRODUCTION CASE**

<script>
new blur();
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Timeline

### ca...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>Input Blink>JavaScript]

### aa...@google.com (2016-07-06)

Calamity@, how did you decide on impacts head label ? Upload repro to clusterfuzz to make sure it does not impact stable/beta branches.

### jo...@chromium.org (2016-07-06)

Ugh

Does the spec say which exception to throw on an construct call to a DOM method?

### jo...@chromium.org (2016-07-06)

Firefox throws: TypeError: blur is not a constructor

remains the question whether bindings code should do the check, or whether v8 should have a way to mark a function as "not a constructor"

### jo...@chromium.org (2016-07-06)

(I'd also contest the "High" rating without a repro of a non-nullptr crash)

### ha...@chromium.org (2016-07-06)

The binding could do the check using the IsConstructor() API. Either is fine with me.



### cl...@chromium.org (2016-07-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


Filer: calamity

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### jo...@chromium.org (2016-07-06)

removing the prototype seems to be the way to go

### cl...@chromium.org (2016-07-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  
Regressed: V8: r37148:37158

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### bu...@chromium.org (2016-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/46428e45e9982a7490685ff1af6ffe680096c1a4

commit 46428e45e9982a7490685ff1af6ffe680096c1a4
Author: jochen <jochen@chromium.org>
Date: Wed Jul 06 11:41:37 2016

Make it possible to create a v8::Function directly w/o a prototype

BUG=chromium:625823
R=verwaest@chromium.org

Review-Url: https://codereview.chromium.org/2123143002
Cr-Commit-Position: refs/heads/master@{#37549}

[modify] https://crrev.com/46428e45e9982a7490685ff1af6ffe680096c1a4/include/v8.h
[modify] https://crrev.com/46428e45e9982a7490685ff1af6ffe680096c1a4/src/api.cc


### bu...@chromium.org (2016-07-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/c4dedf32b1f5c71740df5be2a9b1446a01df304c

commit c4dedf32b1f5c71740df5be2a9b1446a01df304c
Author: jochen <jochen@chromium.org>
Date: Wed Jul 06 12:26:23 2016

Remove prototypes from v8 functions that aren't constructors

BUG=chromium:625823
R=haraken@chromium.org,thestig@chromium.org

Review-Url: https://codereview.chromium.org/2123153002

[modify] https://crrev.com/c4dedf32b1f5c71740df5be2a9b1446a01df304c/fpdfsdk/jsapi/fxjs_v8.cpp
[modify] https://crrev.com/c4dedf32b1f5c71740df5be2a9b1446a01df304c/fxjse/class.cpp


### bu...@chromium.org (2016-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/596fd5ed32fdcce384a3a5f6453582919bef6528

commit 596fd5ed32fdcce384a3a5f6453582919bef6528
Author: jochen <jochen@chromium.org>
Date: Wed Jul 06 12:29:50 2016

Remove the prototype from all V8 functions that aren't constructors

BUG=625823
R=haraken@chromium.org
TBR=eroman@chromium.org,yzshen@chromium.org

Review-Url: https://codereview.chromium.org/2126763002
Cr-Commit-Position: refs/heads/master@{#403888}

[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/chrome/test/base/v8_unit_test.cc
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/extensions/renderer/console.cc
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/extensions/renderer/module_system.cc
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/gin/function_template.h
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/gin/modules/module_registry.cc
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/mojo/public/js/validation_unittests.js
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/net/proxy/proxy_resolver_v8.cc
[add] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/third_party/WebKit/LayoutTests/fast/dom/Window/window-methods-construct.html
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/third_party/WebKit/Source/bindings/core/v8/DocumentWriteEvaluator.cpp
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
[modify] https://crrev.com/596fd5ed32fdcce384a3a5f6453582919bef6528/third_party/WebKit/Source/bindings/core/v8/V8PerIsolateData.cpp


### sh...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-07-06)

> Does the spec say which exception to throw on an construct call to a DOM method?

This is an open Web IDL issue: https://github.com/heycam/webidl/issues/106

### cl...@gmail.com (2016-07-06)

I tried to get the non-null ptr SEGV more reliable. Pasting this in the developer console on an ASAN build leads to a non-null crash in ~10% of the attempts for me:

new Error(new blur(new Error(new Error(new Error()))))


Asan:

ASAN:DEADLYSIGNAL
=================================================================
==22073==ERROR: AddressSanitizer: SEGV on unknown address 0x7f6dc5804a41 (pc 0x7f6dc5804a41 bp 0x7fff54c3ed90 sp 0x7fff54c3ecb8 T0)
==22073==The signal is caused by a READ memory access.
    #0 0x7f6dc5804a40  (<unknown module>)
    #1 0x55b097afab45 in HandleApiCallHelper<true> v8/src/builtins.cc:5490:36
    #2 0x55b097afab45 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins.cc:5516
    #3 0x7f6dc63063a6  (<unknown module>)
    #4 0x7f6dc63441c7  (<unknown module>)
    #5 0x7f6dc641cee6  (<unknown module>)
    #6 0x7f6dc63442e2  (<unknown module>)
    #7 0x7f6dc6325e0e  (<unknown module>)
    #8 0x55b09811fe92 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:98:13
    #9 0x55b09811f86c in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:155:10
    #10 0x55b09796805d in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1881:23
    #11 0x55b0a6b18827 in blink::V8DebuggerImpl::runCompiledScript(v8::Local<v8::Context>, v8::Local<v8::Script>) third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.cpp:722:48
...


### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/95adc31201fd4d1f3b9ec96a62993e64d3273ed9

commit 95adc31201fd4d1f3b9ec96a62993e64d3273ed9
Author: ochang <ochang@chromium.org>
Date: Thu Jul 07 02:47:54 2016

Roll PDFium cfb31d6..2f6d148

https://pdfium.googlesource.com/pdfium.git/+log/cfb31d6..2f6d148

BUG=625541,625823

Review-Url: https://codereview.chromium.org/2128163002
Cr-Commit-Position: refs/heads/master@{#404047}

[modify] https://crrev.com/95adc31201fd4d1f3b9ec96a62993e64d3273ed9/DEPS


### cl...@chromium.org (2016-07-07)

ClusterFuzz has detected this issue as fixed in range 37544:37559.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  
Regressed: V8: r37148:37158
Fixed: V8: r37544:37559

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-07)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### jo...@chromium.org (2016-07-07)

I'll mark it as fixed once it's fixed, thank you

### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/3c27a84d15c06f85cc7f455f96dc124673f9f9d2

commit 3c27a84d15c06f85cc7f455f96dc124673f9f9d2
Author: jochen <jochen@chromium.org>
Date: Thu Jul 07 11:31:26 2016

Remove constructor from functions that aren't constructors

BUG=chromium:625823
R=haraken@chromium.org,thestig@chromium.org

Review-Url: https://codereview.chromium.org/2128793002

[modify] https://crrev.com/3c27a84d15c06f85cc7f455f96dc124673f9f9d2/DEPS
[modify] https://crrev.com/3c27a84d15c06f85cc7f455f96dc124673f9f9d2/fxjse/dynprop.cpp


### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/587b0b37724cdfc0eec5ed091b94eb8276bc05ce

commit 587b0b37724cdfc0eec5ed091b94eb8276bc05ce
Author: jochen <jochen@chromium.org>
Date: Thu Jul 07 12:33:36 2016

Remove constructor from remaining functions that aren't constructors

BUG=625823
R=haraken@chromium.org,pfeldman@chromium.org

Review-Url: https://codereview.chromium.org/2124183003
Cr-Commit-Position: refs/heads/master@{#404137}

[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/bindings/core/v8/V8Binding.h
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/core/inspector/InspectorDOMDebuggerAgent.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/core/inspector/ThreadDebugger.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.cpp
[modify] https://crrev.com/587b0b37724cdfc0eec5ed091b94eb8276bc05ce/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp


### ha...@chromium.org (2016-07-07)

Please merge 46428e45e9982a7490685ff1af6ffe680096c1a4.

### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96b3c35dbff379f682c3693734b2eab05c10bbf1

commit 96b3c35dbff379f682c3693734b2eab05c10bbf1
Author: jochen <jochen@chromium.org>
Date: Thu Jul 07 17:29:27 2016

Roll src/third_party/pdfium/ 2f6d1480a..3c27a84d1 (4 commits).

https://pdfium.googlesource.com/pdfium.git/+log/2f6d1480a1be..3c27a84d15c0

$ git log 2f6d1480a..3c27a84d1 --date=short --no-merges --format='%ad %ae %s'
2016-07-07 jochen Remove constructor from functions that aren't constructors
2016-07-07 jochen Mark win_xfa_clang as experimental
2016-07-07 agoode Fix compilation with strict format checking
2016-07-06 weili Change class member variables in raw pointer type into unique_ptr

TBR=thestig@chromium.org
BUG=625823

Review-Url: https://codereview.chromium.org/2131523003
Cr-Commit-Position: refs/heads/master@{#404166}

[modify] https://crrev.com/96b3c35dbff379f682c3693734b2eab05c10bbf1/DEPS


### jo...@chromium.org (2016-07-07)

re https://crbug.com/chromium/625823#c16 - it looks like there's no check on the path that reads out the DOMWindow* pointer, and we end up taking some value that happens to be on the heap behind one of the error objects.

I guess "high" is then correct.

### jo...@chromium.org (2016-07-07)

let's give this some bake time

### aw...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/6d3d40adcbebbde3b0d14dc283cab77956eabb06

commit 6d3d40adcbebbde3b0d14dc283cab77956eabb06
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 08 08:44:34 2016

Version 5.1.281.74 (cherry-pick)

Merged 46428e45e9982a7490685ff1af6ffe680096c1a4

Make it possible to create a v8::Function directly w/o a prototype

BUG=chromium:625823
LOG=N
TBR=hablich@chromium.org

Review URL: https://codereview.chromium.org/2133643002 .

Cr-Commit-Position: refs/branch-heads/5.1@{#88}
Cr-Branched-From: 167dc63b4c9a1d0f0fe1b19af93644ac9a561e83-refs/heads/5.1.281@{#1}
Cr-Branched-From: 03953f52bd4a184983a551927c406be6489ef89b-refs/heads/master@{#35282}

[modify] https://crrev.com/6d3d40adcbebbde3b0d14dc283cab77956eabb06/include/v8.h
[modify] https://crrev.com/6d3d40adcbebbde3b0d14dc283cab77956eabb06/src/api.cc


### bu...@chromium.org (2016-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e7ca25cb4806cca3b9fd81257db4380e321355d8

commit e7ca25cb4806cca3b9fd81257db4380e321355d8
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 08 10:51:28 2016

Version 5.3.332.12 (cherry-pick)

Merged 46428e45e9982a7490685ff1af6ffe680096c1a4

Make it possible to create a v8::Function directly w/o a prototype

BUG=chromium:625823
LOG=N
TBR=hablich@chromium.org

Review URL: https://codereview.chromium.org/2133133002 .

Cr-Commit-Position: refs/branch-heads/5.3@{#15}
Cr-Branched-From: 820a23aade5e74a92d794e05a0c2b3597f0da4b5-refs/heads/5.3.332@{#2}
Cr-Branched-From: 37538cb2c1b4d75c41af386cb4fedbe5566f5608-refs/heads/master@{#37308}

[modify] https://crrev.com/e7ca25cb4806cca3b9fd81257db4380e321355d8/include/v8-version.h
[modify] https://crrev.com/e7ca25cb4806cca3b9fd81257db4380e321355d8/include/v8.h
[modify] https://crrev.com/e7ca25cb4806cca3b9fd81257db4380e321355d8/src/api.cc


### bu...@chromium.org (2016-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0497584527d328b372405c419b9f586faf4b7c47

commit 0497584527d328b372405c419b9f586faf4b7c47
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 08 11:01:44 2016

Version 5.2.361.38 (cherry-pick)

Merged 46428e45e9982a7490685ff1af6ffe680096c1a4

Make it possible to create a v8::Function directly w/o a prototype

BUG=chromium:625823
LOG=N
TBR=hablich@chromium.org

Review URL: https://codereview.chromium.org/2133683002 .

Cr-Commit-Position: refs/branch-heads/5.2@{#44}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/0497584527d328b372405c419b9f586faf4b7c47/include/v8-version.h
[modify] https://crrev.com/0497584527d328b372405c419b9f586faf4b7c47/include/v8.h
[modify] https://crrev.com/0497584527d328b372405c419b9f586faf4b7c47/src/api.cc


### sh...@chromium.org (2016-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-08)

ClusterFuzz has detected this issue as fixed in range 37544:37559.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  
Fixed: V8: r37544:37559

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-08)

ClusterFuzz has detected this issue as fixed in range 37544:37559.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  
Fixed: V8: r37544:37559

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4857372564783104

Job Type: linux_asan_chrome_v8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::DOMWindowV8Internal::blurMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  v8::internal::Builtin_Impl_HandleApiCall
  
Regressed: V8: r37148:37158
Fixed: V8: r37544:37559

Minimized Testcase (0.03 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96yf0s42ZeBuJ1yerWAYTMLitNZyp5xSFikAjWpC3OGt576c4S6-14Q0wMkzJTVDQ9ntEPfRRTUjE11lcmG16U84915_1WRGBCVw0gx3FFnLMFxZNq1dyN_ChcYjh_4ye9fIC3N8_j0oxwH0Kt8TwuP7wV_-w?testcase_id=4857372564783104
<script>
new blur();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-07-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2016-07-11)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-07-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-07-13)

So, what shall we do here?

I'd say the changes are all quite safe, and to really be on the safe side, we should merge them all.

To fix only the case reported initially, it's enough to merge the one line in V8PerIsolateData::findOrCreateOperationTemplate

opinions?

### jo...@chromium.org (2016-07-13)

+cc inferno explicitly. Mind commenting on #38?

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

  hablich@, could you ptal https://crbug.com/chromium/625823#c38 and please approve the merges to M52 and M53 if you think it is ok to do so. 

### jo...@chromium.org (2016-07-14)

note that the V8 bits are trivial, and already merged to M51-M53.

It's the Blink, Chrome, and PDFium bits I ask about.

### go...@chromium.org (2016-07-14)

yeah, got it. 

inferno@ or awhalley@, could any one of you please reply to https://crbug.com/chromium/625823#c38.



### aw...@chromium.org (2016-07-14)

Yes, I think this is OK to merge.  It's had the requisite time on TOT for a merge to Beta for a Severity-High.

### go...@chromium.org (2016-07-14)

Blink, Chrome, and PDFium bits: Approving merge to M53 branch 2785 and M52 branch 2743 based on https://crbug.com/chromium/625823#c44 and after chatting with awhalley@. please merge ASAP. Thank you.

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6367b77ca60d720e4d791a404c858e583a756762

commit 6367b77ca60d720e4d791a404c858e583a756762
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 15 08:01:58 2016

Remove constructor from remaining functions that aren't constructors

BUG=625823
R=haraken@chromium.org,pfeldman@chromium.org

Review-Url: https://codereview.chromium.org/2124183003
Cr-Commit-Position: refs/heads/master@{#404137}
(cherry picked from commit 587b0b37724cdfc0eec5ed091b94eb8276bc05ce)

Review URL: https://codereview.chromium.org/2154683002 .

Cr-Commit-Position: refs/branch-heads/2785@{#144}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/bindings/core/v8/V8Binding.h
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/core/inspector/InspectorDOMDebuggerAgent.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/core/inspector/ThreadDebugger.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/platform/v8_inspector/V8Console.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/platform/v8_inspector/V8DebuggerImpl.cpp
[modify] https://crrev.com/6367b77ca60d720e4d791a404c858e583a756762/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp


### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf976b9ee471214c1fac69bef867b0ddda721256

commit bf976b9ee471214c1fac69bef867b0ddda721256
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 15 08:13:05 2016

Remove the prototype from all V8 functions that aren't constructors

BUG=625823
R=haraken@chromium.org
TBR=eroman@chromium.org,yzshen@chromium.org

Review-Url: https://codereview.chromium.org/2126763002
Cr-Commit-Position: refs/heads/master@{#403888}
(cherry picked from commit 596fd5ed32fdcce384a3a5f6453582919bef6528)

Review URL: https://codereview.chromium.org/2155503003 .

Cr-Commit-Position: refs/branch-heads/2785@{#145}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/chrome/test/base/v8_unit_test.cc
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/extensions/renderer/console.cc
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/extensions/renderer/module_system.cc
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/gin/function_template.h
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/gin/modules/module_registry.cc
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/mojo/public/js/validation_unittests.js
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/net/proxy/proxy_resolver_v8.cc
[add] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/third_party/WebKit/LayoutTests/fast/dom/Window/window-methods-construct.html
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/third_party/WebKit/Source/bindings/core/v8/DocumentWriteEvaluator.cpp
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
[modify] https://crrev.com/bf976b9ee471214c1fac69bef867b0ddda721256/third_party/WebKit/Source/bindings/core/v8/V8PerIsolateData.cpp


### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/50f1fc0e0601accaed1473a905273e76c8d281d4

commit 50f1fc0e0601accaed1473a905273e76c8d281d4
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 15 09:02:58 2016


### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ae2f62f9ec017f73c3e0e945bffd2135146539c

commit 0ae2f62f9ec017f73c3e0e945bffd2135146539c
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 15 11:29:55 2016

Remove the prototype from all V8 functions that aren't constructors

BUG=625823
R=haraken@chromium.org
TBR=eroman@chromium.org,yzshen@chromium.org

Review-Url: https://codereview.chromium.org/2126763002
Cr-Commit-Position: refs/heads/master@{#403888}
(cherry picked from commit 596fd5ed32fdcce384a3a5f6453582919bef6528)

Review URL: https://codereview.chromium.org/2150303002 .

Cr-Commit-Position: refs/branch-heads/2743@{#644}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/chrome/test/base/v8_unit_test.cc
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/extensions/renderer/console.cc
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/extensions/renderer/module_system.cc
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/extensions/renderer/object_backed_native_handler.cc
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/gin/function_template.h
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/gin/modules/module_registry.cc
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/mojo/public/js/validation_unittests.js
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/net/proxy/proxy_resolver_v8.cc
[add] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/third_party/WebKit/LayoutTests/fast/dom/Window/window-methods-construct.html
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/third_party/WebKit/Source/bindings/core/v8/DocumentWriteEvaluator.cpp
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/third_party/WebKit/Source/bindings/core/v8/PrivateScriptRunner.cpp
[modify] https://crrev.com/0ae2f62f9ec017f73c3e0e945bffd2135146539c/third_party/WebKit/Source/bindings/core/v8/V8PerIsolateData.cpp


### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/461182bf88597975d2aa8c5b64aaed4e90137956

commit 461182bf88597975d2aa8c5b64aaed4e90137956
Author: Oliver Chang <ochang@google.com>
Date: Fri Jul 15 16:32:20 2016


### of...@google.com (2016-08-15)

The V8 change 46428e45e9982a7490685ff1af6ffe680096c1a4 may also need to be floated on Node.js 6.x (for V8 5.0), but let us wait for closure on https://github.com/nodejs/node/pull/8054.

### of...@google.com (2016-09-01)

Node 6 has upgraded to V8 5.1, so a backport/float for 5.0 is no longer needed.

### ha...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations, the panel decided to award $1,000 for this bug!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-09-18)

We have made a bunch of changes on ClusterFuzz side, so resetting ClusterFuzz-Wrong label.

### is...@google.com (2017-09-18)

This issue was migrated from crbug.com/chromium/625823?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, Blink>JavaScript]
[Monorail blocking: crbug.com/chromium/601272]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084766)*
