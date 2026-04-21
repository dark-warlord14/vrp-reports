# UNKNOWN in blink::EventTarget::getEventListeners

| Field | Value |
|-------|-------|
| **Issue ID** | [40082399](https://issues.chromium.org/issues/40082399) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings, Blink>DOM |
| **Reporter** | [Deleted User] |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-06-29 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: [43.0.2357.130 m] 
Operating System: [win7]

## Attachments

- [poc.html](attachments/poc.html) (text/html, 56.7 KB)
- [uaf.txt](attachments/uaf.txt) (text/plain, 7.3 KB)
- [505374.txt](attachments/505374.txt) (text/plain, 16.2 KB)
- [505745_no_uaf.txt](attachments/505745_no_uaf.txt) (text/plain, 7.7 KB)
- [505745_uaf.txt](attachments/505745_uaf.txt) (text/plain, 7.3 KB)
- [505745.html](attachments/505745.html) (text/html, 7.5 KB)
- [505745_min.html](attachments/505745_min.html) (text/html, 1.1 KB)

## Timeline

### cl...@chromium.org (2015-06-29)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6059616771768320

### jw...@chromium.org (2015-06-29)

sigbjornf@opera.com, would you mind triaging this appropriately? Thanks.

### jw...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-06-29)

Clusterfuzz actually produced a slightly more useful stack track from the dup https://crbug.com/chromium/505361: https://cluster-fuzz.appspot.com/testcase?key=6457536163610624

### jw...@chromium.org (2015-06-29)

Just as a clarification, null pointer segvs are not security bugs, so I'm removing the labels and restrictions.

### [Deleted User] (2015-06-29)

I can't access #5, but stack trace:

 	blink_web.dll!blink::reportFatalErrorInMainThread(const char * location, const char * message)  Line 95	C++
 	v8.dll!v8::Utils::ReportApiFailure(const char * location, const char * message)  Line 291 + 0x2 bytes	C++
 	v8.dll!v8::Object::SlowGetAlignedPointerFromInternalField(int index)  Line 5397 + 0x47 bytes	C++
 	blink_web.dll!blink::getInternalField<blink::ScriptWrappable,1>(v8::Local<v8::Object> wrapper)  Line 207 + 0x14 bytes	C++
 	blink_web.dll!blink::toScriptWrappable(v8::Local<v8::Object> wrapper)  Line 222 + 0x9 bytes	C++
 	blink_web.dll!blink::V8HTMLElement::toImpl(v8::Local<v8::Object> object)  Line 29 + 0x9 bytes	C++
 	blink_web.dll!blink::HTMLElementV8Internal::onchangeAttributeGetter(const v8::FunctionCallbackInfo<v8::Value> & info)  Line 896 + 0x9 bytes	C++
 	blink_web.dll!blink::HTMLElementV8Internal::onchangeAttributeGetterCallback(const v8::FunctionCallbackInfo<v8::Value> & info)  Line 904 + 0x9 bytes	C++
 	33c0b0d4()	
 	33c17bfd()	
 	3660cf83()	
 	33c18d1d()	
 	3660cf83()	
 	33c18d1d()	
 	3660cf83()	
 	33c18d1d()	
 	3660cf83()	
 	33c16e9e()	
 	3662be41()	
 	36617fff()	
 	v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args)  Line 128 + 0x10 bytes	C++
 	v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool convert_receiver)  Line 179 + 0x19 bytes	C++
 	v8.dll!v8::Function::Call(v8::Local<v8::Context> context, v8::Local<v8::Value> recv, int argc, v8::Local<v8::Value> * argv)  Line 4501 + 0x1b bytes	C++
 	blink_web.dll!blink::V8ScriptRunner::callFunction(v8::Local<v8::Function> function, blink::ExecutionContext * context, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * args, v8::Isolate * isolate)  Line 437 + 0x3b bytes	C++
 	blink_web.dll!blink::ScriptController::callFunction(blink::ExecutionContext * context, v8::Local<v8::Function> function, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * info, v8::Isolate * isolate)  Line 154 + 0x21 bytes	C++
 	blink_web.dll!blink::ScriptController::callFunction(v8::Local<v8::Function> function, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * info)  Line 148 + 0x52 bytes	C++
 	blink_web.dll!blink::V8EventListener::callListenerFunction(blink::ScriptState * scriptState, v8::Local<v8::Value> jsEvent, blink::Event * event)  Line 96 + 0x2d bytes	C++
>	blink_web.dll!blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState * scriptState, blink::Event * event, v8::Local<v8::Value> jsEvent)  Line 125 + 0x1f bytes	C++
 	blink_web.dll!blink::V8AbstractEventListener::handleEvent(blink::ScriptState * scriptState, blink::Event * event)  Line 101	C++
 	blink_web.dll!blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext * executionContext, blink::Event * event)  Line 85 + 0x17 bytes	C++
 	blink_web.dll!blink::EventTarget::fireEventListeners(blink::Event * event, blink::EventTargetData * d, WTF::Vector<blink::RegisteredEventListener,1,WTF::DefaultAllocator> & entry)  Line 359 + 0x2b bytes	C++
 	blink_web.dll!blink::EventTarget::fireEventListeners(blink::Event * event)  Line 292 + 0x14 bytes	C++
 	blink_web.dll!blink::Node::handleLocalEvents(blink::Event & event)  Line 2046	C++
 	blink_web.dll!blink::NodeEventContext::handleLocalEvents(blink::Event & event)  Line 67 + 0x21 bytes	C++
 	blink_web.dll!blink::EventDispatcher::dispatchEventAtTarget()  Line 172	C++
 	blink_web.dll!blink::EventDispatcher::dispatch()  Line 126 + 0x8 bytes	C++
 	blink_web.dll!blink::EventDispatchMediator::dispatchEvent(blink::EventDispatcher & dispatcher)  Line 58	C++
 	blink_web.dll!blink::EventDispatcher::dispatchEvent(blink::Node & node, WTF::RawPtr<blink::EventDispatchMediator> mediator)  Line 50 + 0x1e bytes	C++
 	blink_web.dll!blink::ScopedEventQueue::dispatchEvent(WTF::RawPtr<blink::EventDispatchMediator> mediator)  Line 83 + 0x15 bytes	C++
 	blink_web.dll!blink::ScopedEventQueue::enqueueEventDispatchMediator(WTF::RawPtr<blink::EventDispatchMediator> mediator)  Line 68	C++
 	blink_web.dll!blink::EventDispatcher::dispatchScopedEvent(blink::Node & node, WTF::RawPtr<blink::EventDispatchMediator> mediator)  Line 70	C++
 	blink_web.dll!blink::Node::dispatchScopedEventDispatchMediator(WTF::RawPtr<blink::EventDispatchMediator> eventDispatchMediator)  Line 2055 + 0x15 bytes	C++
 	blink_web.dll!blink::Node::dispatchScopedEvent(WTF::RawPtr<blink::Event> event)  Line 2051	C++
 	blink_web.dll!blink::dispatchChildRemovalEvents(blink::Node & child)  Line 1252 + 0x84 bytes	C++
 	blink_web.dll!blink::ContainerNode::willRemoveChild(blink::Node & child)  Line 444 + 0x9 bytes	C++
 	blink_web.dll!blink::ContainerNode::removeChild(WTF::RawPtr<blink::Node> oldChild, blink::ExceptionState & exceptionState)  Line 583	C++
 	blink_web.dll!blink::Node::removeChild(WTF::RawPtr<blink::Node> oldChild, blink::ExceptionState & exceptionState)  Line 480 + 0x27 bytes	C++
 	blink_web.dll!blink::NodeV8Internal::removeChildMethod(const v8::FunctionCallbackInfo<v8::Value> & info)  Line 862	C++
 	blink_web.dll!blink::NodeV8Internal::removeChildMethodCallback(const v8::FunctionCallbackInfo<v8::Value> & info)  Line 872 + 0x9 bytes	C++
 	v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &)* f)  Line 34	C++
 	v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::Isolate * isolate, v8::internal::`anonymous-namespace'::BuiltinArguments<1> & args)  Line 1094	C++
 	v8.dll!v8::internal::Builtin_Impl_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate)  Line 1116 + 0x10 bytes	C++
 	v8.dll!v8::internal::Builtin_HandleApiCall(int args_length, v8::internal::Object * * args_object, v8::internal::Isolate * isolate)  Line 1111 + 0x55 bytes	C++
 	v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args)  Line 128 + 0x10 bytes	C++
 	v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool convert_receiver)  Line 179 + 0x19 bytes	C++
 	v8.dll!v8::Function::Call(v8::Local<v8::Context> context, v8::Local<v8::Value> recv, int argc, v8::Local<v8::Value> * argv)  Line 4501 + 0x1b bytes	C++
 	blink_web.dll!blink::V8ScriptRunner::callFunction(v8::Local<v8::Function> function, blink::ExecutionContext * context, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * args, v8::Isolate * isolate)  Line 437 + 0x3b bytes	C++
 	blink_web.dll!blink::ScriptController::callFunction(blink::ExecutionContext * context, v8::Local<v8::Function> function, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * info, v8::Isolate * isolate)  Line 154 + 0x21 bytes	C++
 	blink_web.dll!blink::ScriptController::callFunction(v8::Local<v8::Function> function, v8::Local<v8::Value> receiver, int argc, v8::Local<v8::Value> * info)  Line 148 + 0x52 bytes	C++
 	blink_web.dll!blink::V8EventListener::callListenerFunction(blink::ScriptState * scriptState, v8::Local<v8::Value> jsEvent, blink::Event * event)  Line 96 + 0x2d bytes	C++
 	blink_web.dll!blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState * scriptState, blink::Event * event, v8::Local<v8::Value> jsEvent)  Line 125 + 0x1f bytes	C++
 	blink_web.dll!blink::V8AbstractEventListener::handleEvent(blink::ScriptState * scriptState, blink::Event * event)  Line 101	C++
 	blink_web.dll!blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext * executionContext, blink::Event * event)  Line 85 + 0x17 bytes	C++
 	blink_web.dll!blink::EventTarget::fireEventListeners(blink::Event * event, blink::EventTargetData * d, WTF::Vector<blink::RegisteredEventListener,1,WTF::DefaultAllocator> & entry)  Line 359 + 0x2b bytes	C++
 	blink_web.dll!blink::EventTarget::fireEventListeners(blink::Event * event)  Line 292 + 0x14 bytes	C++
 	blink_web.dll!blink::WindowEventContext::handleLocalEvents(blink::Event & event)  Line 58	C++
 	blink_web.dll!blink::EventDispatcher::dispatchEventAtCapturing()  Line 153 + 0x2c bytes	C++
 	blink_web.dll!blink::EventDispatcher::dispatch()  Line 125 + 0x8 bytes	C++
 	blink_web.dll!blink::EventDispatchMediator::dispatchEvent(blink::EventDispatcher & dispatcher)  Line 58	C++
 	blink_web.dll!blink::EventDispatcher::dispatchEvent(blink::Node & node, WTF::RawPtr<blink::EventDispatchMediator> mediator)  Line 50 + 0x1e bytes	C++
 	blink_web.dll!blink::Node::dispatchEvent(WTF::RawPtr<blink::Event> event)  Line 2067 + 0x21 bytes	C++
 	blink_web.dll!blink::Document::finishedParsing()  Line 4595	C++
 	blink_web.dll!blink::HTMLConstructionSite::finishedParsing()  Line 545	C++
 	blink_web.dll!blink::HTMLTreeBuilder::finished()  Line 2807	C++
 	blink_web.dll!blink::HTMLDocumentParser::end()  Line 861	C++
 	blink_web.dll!blink::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd()  Line 873	C++
 	blink_web.dll!blink::HTMLDocumentParser::prepareToStopParsing()  Line 273	C++
 	blink_web.dll!blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk> popChunk)  Line 511	C++
 	blink_web.dll!blink::HTMLDocumentParser::pumpPendingSpeculations()  Line 563 + 0x18 bytes	C++
 	blink_web.dll!blink::HTMLDocumentParser::resumeParsingAfterYield()  Line 308	C++
 	blink_web.dll!blink::HTMLParserScheduler::continueParsing()  Line 166	C++
 	blink_web.dll!WTF::FunctionWrapper<void (__thiscall blink::HTMLParserScheduler::*)(void)>::operator()(blink::HTMLParserScheduler * c)  Line 83 + 0xc bytes	C++
 	blink_web.dll!WTF::PartBoundFunctionImpl<1,WTF::FunctionWrapper<void (__thiscall blink::HTMLParserScheduler::*)(void)>,void __cdecl(blink::HTMLParserScheduler *)>::operator()()  Line 179	C++
 	blink_platform.dll!blink::CancellableTaskFactory::CancellableTask::run()  Line 34 + 0xf bytes	C++


### [Deleted User] (2015-06-29)

i.e. failing to find the wrapper on the object/holder for the onchange getter callback.

### [Deleted User] (2015-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2015-06-30)

5e21f233 ff5240          call    dword ptr [edx+40h]  ds:0023:a134c0c1=????????
thanks,It's not null pointer.

### cl...@chromium.org (2015-06-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6059616771768320

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  blink::EventTarget::getEventListeners
  blink::EventTarget::getAttributeEventListener
  blink::HTMLElementV8Internal::onchangeAttributeGetterCallback
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=320284:320470

Minimized Testcase (12.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94UW1pp1L5MrpJRjs-kvkC__7pypCb6nkvcfFosS5khDRlTx4QFJ_NxWC8wDjxAMLuerk9srFhGQ7xYXaw4vakwdG9C1lrqgrU9rtaU2mojdRrAEPj6z_T_Iodbo5_UwcC8kiZjDG136vaaEDqZhEt4ntM69g



### yu...@chromium.org (2015-07-01)

I guess https://crbug.com/chromium/505336 and https://crbug.com/chromium/505365 may be caused by the same cause of this issue.

I'm investigating https://crbug.com/chromium/505365 and found the followings.
- When Blink binding layer is called (e.g. innerHTMLAttributeGetter), info.Holder() does NOT point to an instance of the interface (e.g. HTMLElement).  The internal fields for WrapperTypeInfo and C++ instance are not correct.
- The object passed to Blink is created by
    Object.create(HTMLElement.prototype)

Usually the object above is not associated with any C++ object, but somehow it seems succeeding to call to C++ callback.  I don't understand how it's possible (it must be impossible)...


### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

Lets just use this as a master bug and see if its fix fixes  https://crbug.com/chromium/505336 and https://crbug.com/chromium/505365 as well.

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-02)

open https://crbug.com/chromium/505745 poc.html,will appear uaf.

use asan appear uaf.If don't triger uaf,refresh a few times.

asan-win32-release-336507>chrome --no-sandbox --js-flags="--expose-gc"
win7 64

### [Deleted User] (2015-07-02)

I feel 505374 and 505745 not same.

### in...@chromium.org (2015-07-02)

Why not same, looks like the same stack to me.

### [Deleted User] (2015-07-02)

I use asan-win32-release-336507 test's result is not same.

### [Deleted User] (2015-07-02)

please use asan-win32-release-336507.

### in...@chromium.org (2015-07-02)

I would let dev decide if this is same root cause, looks very likely from similar stack. If not, then we would remove the dup.

### cl...@chromium.org (2015-07-03)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-03)

It take a lot of time to reduce the 505745 poc.I hope to help you a little.If don't triger uaf,please refresh a few times.

### yu...@chromium.org (2015-07-03)

Thanks for the html.  It's a great help.

By the way, I cannot access to https://crbug.com/chromium/505745 probably because I'm not listed in cc list.  Could someone add me to the list?

### yu...@chromium.org (2015-07-03)

Based on liuyongnew@'s version, I minimized the html as attached.

### yu...@chromium.org (2015-07-03)

jochen@, could you triage this issue to a V8 expert?

liuyongnew@ and I minimized the repro case (see #29), and it seems V8's issue to me.  At least, I'd like to hear V8 expert's opinions about what the cause may be.

### yu...@chromium.org (2015-07-03)

Just in case, my repro environment is Goobuntu (GNU/Linux) and 
    Version 45.0.2438.3 dev (64-bit)
I can repro with ToT of both of Release and Debug builds.

### in...@chromium.org (2015-07-03)

yukishiino@chromium.org, cced you on 505745  

+cc more v8 folks, based on c#30.

### jo...@chromium.org (2015-07-03)

what happens is that the ic happily transitions to monomorphic, while it constantly thows the error. in the monomorphic state, however, we elide the security check...

guess we should either track whether or not the call succeeded and not elide the security check if it didn't, or just not transition to monomorphic if exceptions are thrown.

### jo...@chromium.org (2015-07-06)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### jo...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8c298c79c2eff50b1d3809a5f72ed7d3679c47a4

commit 8c298c79c2eff50b1d3809a5f72ed7d3679c47a4
Author: jochen <jochen@chromium.org>
Date: Tue Jul 07 11:02:15 2015

Move compatible receiver check from CompileHandler to UpdateCaches

We also need to do the check before using an existing handler from the
cache

BUG=chromium:505374
R=verwaest@chromium.org
LOG=y

Review URL: https://codereview.chromium.org/1221433010

Cr-Commit-Position: refs/heads/master@{#29511}

[modify] http://crrev.com/8c298c79c2eff50b1d3809a5f72ed7d3679c47a4/src/ic/ic.cc
[modify] http://crrev.com/8c298c79c2eff50b1d3809a5f72ed7d3679c47a4/test/cctest/test-api.cc


### jo...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-08)

use latest asan-win32-release-337698,all are still able to reproduce.

### in...@chromium.org (2015-07-08)

Are you sure that v8 roll has happened and that latest asan build has the fix.

### jo...@chromium.org (2015-07-08)

the fix hasn't yet rolled into chromium

### [Deleted User] (2015-07-08)

You may need my information after fixed it,my name is Liu Yongjun,from NSFOCUS Security Team.Thanks.

### jo...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-08)

Are you sure these are the same? But I saw these stacks not same.If you true,can you tell me the reason which lead to vulnerability?

### jo...@chromium.org (2015-07-08)

which one are you referring to?

### in...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-08)

ClusterFuzz has detected this issue as fixed in range 337759:337769.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6059616771768320

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  blink::EventTarget::getEventListeners
  blink::EventTarget::getAttributeEventListener
  blink::HTMLElementV8Internal::onchangeAttributeGetterCallback
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=320284:320470
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=337759:337769

Minimized Testcase (12.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94UW1pp1L5MrpJRjs-kvkC__7pypCb6nkvcfFosS5khDRlTx4QFJ_NxWC8wDjxAMLuerk9srFhGQ7xYXaw4vakwdG9C1lrqgrU9rtaU2mojdRrAEPj6z_T_Iodbo5_UwcC8kiZjDG136vaaEDqZhEt4ntM69g

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### bu...@chromium.org (2015-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3bf7258ec1f9806f59465aa9e0bf5c8760e98063

commit 3bf7258ec1f9806f59465aa9e0bf5c8760e98063
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 10 07:58:56 2015

Version 4.4.63.16 (cherry-pick)

Merged 8c298c79c2eff50b1d3809a5f72ed7d3679c47a4

Move compatible receiver check from CompileHandler to UpdateCaches

BUG=chromium:505374
LOG=N
TBR=hablich@chromium.org

Review URL: https://codereview.chromium.org/1233453004 .

Cr-Commit-Position: refs/branch-heads/4.4@{#20}
Cr-Branched-From: 2e4c5505e85d94b520e853dda3f0cc3f2769e5f0-refs/heads/4.4.63@{#1}
Cr-Branched-From: 0208b8e3a1d7ce393308866386ac8d94f85faa05-refs/heads/master@{#28333}

[modify] http://crrev.com/3bf7258ec1f9806f59465aa9e0bf5c8760e98063/include/v8-version.h
[modify] http://crrev.com/3bf7258ec1f9806f59465aa9e0bf5c8760e98063/src/ic/ic.cc
[modify] http://crrev.com/3bf7258ec1f9806f59465aa9e0bf5c8760e98063/test/cctest/test-api.cc


### bu...@chromium.org (2015-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6135556c6ae59796f572c54ab4fdcd533c992f9

commit d6135556c6ae59796f572c54ab4fdcd533c992f9
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri Jul 10 08:09:11 2015

Version 4.3.61.38 (cherry-pick)

Merged 8c298c79c2eff50b1d3809a5f72ed7d3679c47a4

Move compatible receiver check from CompileHandler to UpdateCaches

BUG=chromium:505374
LOG=N
TBR=hablich@chromium.org

Review URL: https://codereview.chromium.org/1233593002 .

Cr-Commit-Position: refs/branch-heads/4.3@{#43}
Cr-Branched-From: f5c0a23a505616796a628d64f4ffe377d1fc4bcf-refs/heads/4.3.61@{#1}
Cr-Branched-From: 0a7d4f496a554028de0ab5a963c3a004e693b4cb-refs/heads/master@{#27508}

[modify] http://crrev.com/d6135556c6ae59796f572c54ab4fdcd533c992f9/include/v8-version.h
[modify] http://crrev.com/d6135556c6ae59796f572c54ab4fdcd533c992f9/src/ic/ic.cc
[modify] http://crrev.com/d6135556c6ae59796f572c54ab4fdcd533c992f9/test/cctest/test-api.cc


### ha...@chromium.org (2015-07-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-23)

The security bug has fixed at Chrome 44.0.2403.89,but the credit have not the information about me.
It's my information:Yongjun Liu,from NSFOCUS Security Team.Thanks.

### jo...@chromium.org (2015-07-23)

Tim, can you look into this, please?

### aa...@google.com (2015-07-23)

Tim is OOO. Marty, can you please fix the release notes and inform RM.

### mb...@chromium.org (2015-07-24)

Sorry we missed this one. It's now listed at http://googlechromereleases.blogspot.ca/2015/07/stable-channel-update_21.html

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-30)

Can you tell me about the reward?thanks.

### [Deleted User] (2015-08-10)

Who can tell me about the reward? have or not. thanks.

### ti...@google.com (2015-08-31)

Sorry for the delay - we'll take a look at this for reward in the next few weeks and let you know what the decision is at that time.

### cl...@chromium.org (2015-10-13)

Bulk update: removing view restriction from closed bugs.

### [Deleted User] (2015-10-27)

timwil...@google.com,I guess you forget it.

### [Deleted User] (2015-11-13)

Several weeks have passed.How long it will take?Next year?

### yu...@chromium.org (2015-11-16)

timwillis@, could you take a look for reward?

### ti...@google.com (2015-11-20)

Yikes! I'll put this on the top of the next panel. I'll email you with some additional details as well.

### ti...@google.com (2015-12-01)

Our panel finally reviewed your report and decided on a reward of $1000. Congratulations!

Panel feedback: Report first filed incorrectly as functional bug, so please make sure to file as a security bug in the future. Hard to see if out of bounds write can be achieved or if just out of bounds reads due to bad wrappers. For future consideration at higher reward levels, please refer to the table at https://www.google.com/about/appsecurity/chrome-rewards/#rewards, specifically what meets the bar for a high quality report.

A member of our finance team should be in touch within a week to collect payment details. If that doesn't happen, please let me know via updating this bug or emailing me at timwillis@.

Thanks again for your report (and your patience with the delay!)

### ti...@google.com (2015-12-14)

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

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/505374?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bindings, Blink>DOM]
[Monorail mergedwith: crbug.com/chromium/504723, crbug.com/chromium/505336, crbug.com/chromium/505361, crbug.com/chromium/505365, crbug.com/chromium/505371, crbug.com/chromium/505375, crbug.com/chromium/505379, crbug.com/chromium/505745, crbug.com/chromium/507566]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082399)*
