# REGRESSION(wk109285): Heap-use-after-free in WebCore::Document::nodeChildrenWillBeRemoved

| Field | Value |
|-------|-------|
| **Issue ID** | [40054595](https://issues.chromium.org/issues/40054595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-03-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap-use-after-free when the attached page is viewed.

**VERSION**  

Chrome Version: 19.0.1061.0 (Developer Build 125107)  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

$ chrome-asan select.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==1166== ERROR: AddressSanitizer heap-use-after-free on address 0x7f4b82fa6bb8 at pc 0x7f4b91d3ea74 bp 0x7fff26693160 sp 0x7fff26693158  

READ of size 8 at 0x7f4b82fa6bb8 thread T0  

#0 0x7f4b91d3ea74 in WebCore::Document::nodeChildrenWillBeRemoved(WebCore::ContainerNode\*) ???:0  

#1 0x7f4b91cfced9 in WebCore::ContainerNode::removeChildren() ???:0  

#2 0x7f4b91ee599b in WebCore::HTMLElement::setInnerText(WTF::String const&, int&) ???:0  

#3 0x7f4b91fa2b71 in WebCore::HTMLTextFormControlElement::setInnerTextValue(WTF::String const&) ???:0  

#4 0x7f4b91f120a2 in WebCore::HTMLInputElement::updateInnerTextValue() ???:0  

#5 0x7f4b91fe049b in WebCore::TextFieldInputType::setValue(WTF::String const&, bool, WebCore::TextFieldEventBehavior) ???:0  

#6 0x7f4b91f17111 in WebCore::HTMLInputElement::setValue(WTF::String const&, WebCore::TextFieldEventBehavior) ???:0  

#7 0x7f4b9376dc6d in WebCore::HTMLInputElementInternal::valueAttrSetter(v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::AccessorInfo const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources13.cpp:0  

#8 0x7f4b90ba035c in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object\*, v8::internal::String\*, v8::internal::Object\*, v8::internal::JSObject\*, v8::internal::StrictModeFlag) ???:0  

#9 0x7f4b90ba8e20 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult\*, v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0  

#10 0x7f4b90b9f4a9 in v8::internal::JSReceiver::SetProperty(v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0  

#11 0x7f4b90fbd957 in v8::internal::StoreIC::Store(v8::internal::InlineCacheState, v8::internal::StrictModeFlag, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::String](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ???:0  

#12 0x7f4b90fc5dfb in v8::internal::StoreIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) ???:0  

#13 0x35618330614e  

#14 0x356183332785  

#15 0x356183322647  

#16 0x356183311137  

#17 0x7f4b908d45b8 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#18 0x7f4b90821619 in v8::Script::Run() ???:0  

#19 0x7f4b924f06c3 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#20 0x7f4b924ef8d5 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#21 0x7f4b924a2186 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#22 0x7f4b91e99efc in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#23 0x7f4b91e95aa5 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#24 0x7f4b92063074 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#25 0x7f4b92062b01 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#26 0x7f4b9205708d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#27 0x7f4b92057400 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#28 0x7f4b92056686 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#29 0x7f4b920581b4 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#30 0x7f4b957dc90c in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#31 0x7f4b92a16999 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#32 0x7f4b92a4d909 in WebCore::FrameLoader::finishedLoading() ???:0  

#33 0x7f4b92a746d1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#34 0x7f4b9414f602 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#35 0x7f4b912cd19a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#36 0x7f4b912ce37b in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#37 0x7f4b912ca97c in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#38 0x7f4b912c8c20 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#39 0x7f4b911c750f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#40 0x7f4b8ff2ace3 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#41 0x7f4b8fe15086 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#42 0x7f4b8fe158e6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#43 0x7f4b8fe16bcb in MessageLoop::DoWork() ???:0  

#44 0x7f4b8fe20fa7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#45 0x7f4b8fe13c7e in MessageLoop::RunInternal() ???:0  

#46 0x7f4b8fe11e6f in MessageLoop::Run() ???:0  

#47 0x7f4b94d03492 in RendererMain(content::MainFunctionParams const&) ???:0  

#48 0x7f4b8fd6f0e6 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#49 0x7f4b8fd6d78a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#50 0x7f4b8e56f657 in ChromeMain ??:0  

#51 0x7f4b8e56f5ab in main ???:0  

#52 0x7f4b87a3fc8d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.3/csu/libc-start.c:260  

0x7f4b82fa6bb8 is located 56 bytes inside of 80-byte region [0x7f4b82fa6b80,0x7f4b82fa6bd0)

freed by thread T0 here:  

#0 0x7f4b95eb1592 in operator delete(void\*) ??:0  

#1 0x7f4b91d3ed07 in WebCore::Document::nodeChildrenWillBeRemoved(WebCore::ContainerNode\*) ???:0  

#2 0x7f4b91cfced9 in WebCore::ContainerNode::removeChildren() ???:0  

#3 0x7f4b91ee599b in WebCore::HTMLElement::setInnerText(WTF::String const&, int&) ???:0  

#4 0x7f4b91fa2b71 in WebCore::HTMLTextFormControlElement::setInnerTextValue(WTF::String const&) ???:0  

#5 0x7f4b91f120a2 in WebCore::HTMLInputElement::updateInnerTextValue() ???:0  

#6 0x7f4b91fe049b in WebCore::TextFieldInputType::setValue(WTF::String const&, bool, WebCore::TextFieldEventBehavior) ???:0  

#7 0x7f4b91f17111 in WebCore::HTMLInputElement::setValue(WTF::String const&, WebCore::TextFieldEventBehavior) ???:0  

#8 0x7f4b9376dc6d in WebCore::HTMLInputElementInternal::valueAttrSetter(v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::AccessorInfo const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources13.cpp:0  

#9 0x7f4b90ba035c in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object\*, v8::internal::String\*, v8::internal::Object\*, v8::internal::JSObject\*, v8::internal::StrictModeFlag) ???:0  

#10 0x7f4b90ba8e20 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult\*, v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0  

#11 0x7f4b90b9f4a9 in v8::internal::JSReceiver::SetProperty(v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0  

#12 0x7f4b90fbd957 in v8::internal::StoreIC::Store(v8::internal::InlineCacheState, v8::internal::StrictModeFlag, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::String](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) ???:0  

#13 0x7f4b90fc5dfb in v8::internal::StoreIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) ???:0  

#14 0x35618330614e  

#15 0x356183332785  

#16 0x356183322647  

#17 0x356183311137  

#18 0x7f4b908d45b8 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#19 0x7f4b90821619 in v8::Script::Run() ???:0  

#20 0x7f4b924f06c3 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#21 0x7f4b924ef8d5 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#22 0x7f4b924a2186 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#23 0x7f4b91e99efc in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#24 0x7f4b91e95aa5 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#25 0x7f4b92063074 in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#26 0x7f4b92062b01 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#27 0x7f4b9205708d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#28 0x7f4b92057400 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

previously allocated by thread T0 here:  

#0 0x7f4b95eb1412 in operator new(unsigned long) ??:0  

#1 0x7f4b91e432d6 in WebCore::Text::create(WebCore::Document\*, WTF::String const&) ???:0  

#2 0x7f4b92896be6 in WebCore::replaceChildrenWithText(WebCore::ContainerNode\*, WTF::String const&, int&) ???:0  

#3 0x7f4b91ee59ab in WebCore::HTMLElement::setInnerText(WTF::String const&, int&) ???:0  

#4 0x7f4b91fa2b71 in WebCore::HTMLTextFormControlElement::setInnerTextValue(WTF::String const&) ???:0  

#5 0x7f4b91f120a2 in WebCore::HTMLInputElement::updateInnerTextValue() ???:0  

#6 0x7f4b91f1522d in WebCore::HTMLInputElement::parseAttribute(WebCore::Attribute\*) ???:0  

#7 0x7f4b957ec943 in WebCore::StyledElement::attributeChanged(WebCore::Attribute\*) ???:0  

#8 0x7f4b91d83d6a in WebCore::Element::parserSetAttributes(WTF::PassOwnPtr[WebCore::AttributeVector](javascript:void(0);), WebCore::FragmentScriptingPermission) ???:0  

#9 0x7f4b921538e9 in WebCore::HTMLConstructionSite::createHTMLElement(WebCore::AtomicHTMLToken&) ???:0  

#10 0x7f4b92154936 in WebCore::HTMLConstructionSite::insertSelfClosingHTMLElement(WebCore::AtomicHTMLToken&) ???:0  

#11 0x7f4b920b4fc4 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken&) ???:0  

#12 0x7f4b920a7195 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken&) ???:0  

#13 0x7f4b920a62ab in WebCore::HTMLTreeBuilder::processToken(WebCore::AtomicHTMLToken&) ???:0  

#14 0x7f4b920a37ef in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken(WebCore::AtomicHTMLToken&) ???:0  

#15 0x7f4b920a36cb in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&) ???:0  

#16 0x7f4b92056670 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#17 0x7f4b920581b4 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#18 0x7f4b957dc90c in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#19 0x7f4b92a16999 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#20 0x7f4b92a4d909 in WebCore::FrameLoader::finishedLoading() ???:0  

#21 0x7f4b92a746d1 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#22 0x7f4b9414f602 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0

==1166== ABORTING  

Stats: 8M malloced (11M for red zones) by 37736 calls  

Stats: 2M realloced by 1721 calls  

Stats: 6M freed by 28643 calls  

Stats: 0M really freed by 0 calls  

Stats: 56M (14344 full pages) mmaped in 14 calls  

mmaps by size class: 8:49149; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8;  

mallocs by size class: 8:31995; 9:3590; 10:1208; 11:455; 12:261; 13:65; 14:110; 15:28; 16:11; 17:8; 18:2; 19:3;  

frees by size class: 8:23648; 9:3163; 10:1102; 11:324; 12:226; 13:45; 14:98; 15:23; 16:4; 17:5; 18:2; 19:3;  

rfrees by size class:  

Stats: malloc large: 13 small slow: 147  

Shadow byte and word:  

0x1fe9705f4d77: fd  

0x1fe9705f4d70: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe9705f4d50: 00 00 00 00 fb fb fb fb  

0x1fe9705f4d58: fb fb fb fb fb fb fb fb  

0x1fe9705f4d60: fa fa fa fa fa fa fa fa  

0x1fe9705f4d68: fa fa fa fa fa fa fa fa  

=>0x1fe9705f4d70: fd fd fd fd fd fd fd fd  

0x1fe9705f4d78: fd fd fd fd fd fd fd fd  

0x1fe9705f4d80: fa fa fa fa fa fa fa fa  

0x1fe9705f4d88: fa fa fa fa fa fa fa fa  

0x1fe9705f4d90: fd fd fd fd fd fd fd fd

## Attachments

- [select.html](attachments/select.html) (text/plain; charset=us-ascii, 164 B)

## Timeline

### in...@chromium.org (2012-03-07)

quite relieved that does not affect stable, beta. CF report coming soon.

### in...@chromium.org (2012-03-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=24754573

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fc35d7869b8
Crash State:
  - crash stack -
  WebCore::Document::nodeChildrenWillBeRemoved
  WebCore::ContainerNode::removeChildren
  - free stack -
  WebCore::Document::nodeChildrenWillBeRemoved
  WebCore::ContainerNode::removeChildren
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124482:124537

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97Z63LflWmdLNTig4_u0ta-SU08jDmxYydC3T0BELU6qQ5iLll-Tx0saF-5OtefwS5tIHTX8XRO4iOkkAZEF6MFtuWQnETwtVkYpz8xFIoeNk43khonQLRCBWLi2jm2J6l7teBdllplH49kyFWLN-FFDuUzUg
<input id="foo" value="bar"> 
<script>
foo.select(31020435620660526591167694770, foo.value.length);
foo.style.fontStyle = "";
foo.value = "";
</script>

### in...@chromium.org (2012-03-07)

Shinyak@, can you please take a look. it might be coming from one of our patches in range https://trac.webkit.org/log/?verbose=on&stop_rev=109270&rev=109423&limit=1000

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2012-03-08)

I'll check it soon.

### sh...@chromium.org (2012-03-09)

upstream: https://bugs.webkit.org/show_bug.cgi?id=80578

The discussion is going on this thread.
https://bugs.webkit.org/show_bug.cgi?id=80659


### in...@chromium.org (2012-03-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-03-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-09)

Ryosuke has a r+ patch upstream.

### in...@chromium.org (2012-03-12)

http://trac.webkit.org/changeset/110449

### sc...@gmail.com (2012-03-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

Niiiiiiice regression catch. $1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ao...@gmail.com (2012-03-15)

@scarybeasts Sweet. One more test node paid itself back with this :)

### sc...@gmail.com (2012-05-10)

Payment in system (part of a $2000 batch)

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/117150?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/117388, crbug.com/chromium/117503]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054595)*
