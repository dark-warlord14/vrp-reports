# Heap-use-after-free in WebCore::SVGStyledElement::buildPendingResourcesIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40055111](https://issues.chromium.org/issues/40055111) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | ax...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2012-03-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use after free happens when adding attribute to SVG element from imported and adopted node.

**VERSION**  

Version 19.0.1068.0 (126348), Developer Build on Ubuntu 10.10  

17.0.963.79 m, Win7 x64

**REPRODUCTION CASE**  

In attachment.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==3489== ERROR: AddressSanitizer heap-use-after-free on address 0x7f5ddf9d2c80 at pc 0x7f5e1948ed72 bp 0x7fffc0e1d7b0 sp 0x7fffc0e1d7a8  

READ of size 8 at 0x7f5ddf9d2c80 thread T0  

#0 0x7f5e1948ed72 in WebCore::SVGStyledElement::buildPendingResourcesIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.cpp:384  

#1 0x7f5e1948e33e in WebCore::SVGStyledElement::svgAttributeChanged(WebCore::QualifiedName const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGStyledElement.cpp:347  

#2 0x7f5e19467f31 in ~InvalidationGuard /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGElementInstance.h:81  

#3 0x7f5e16f8f770 in WebCore::Node::document() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:400  

#4 0x7f5e16f93e04 in WebCore::ElementAttributeData::addAttribute(WTF::PassRefPtr[WebCore::Attribute](javascript:void(0);), WebCore::Element\*, WebCore::EInUpdateStyleAttribute) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ElementAttributeData.cpp:108  

#5 0x7f5e16f7b788 in ~PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:67  

#6 0x7f5e17b4e651 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#7 0x7f5e161d2359 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

#8 0x7f5e161daf90 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult\*, v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) /media/Chromium/chromium/depot\_tools/src/v8/src/objects.cc:3010  

#9 0x7f5e161d1473 in v8::internal::JSReceiver::SetProperty(v8::internal::String\*, v8::internal::Object\*, PropertyAttributes, v8::internal::StrictModeFlag) /media/Chromium/chromium/depot\_tools/src/v8/src/objects.cc:2654  

#10 0x7f5e16601754 in v8::internal::StoreIC::Store(v8::internal::InlineCacheState, v8::internal::StrictModeFlag, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::String](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/v8/src/ic.cc:1391  

#11 0x7f5e16609c8b in v8::internal::StoreIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) /media/Chromium/chromium/depot\_tools/src/v8/src/ic.cc:2011  

#12 0x7f5de3f0614e  

#13 0x7f5de3f3658b  

#14 0x7f5de3f43b7b  

#15 0x7f5de3f22647  

#16 0x7f5de3f11137  

#17 0x7f5e15eff278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#18 0x7f5e15e636f2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3608  

#19 0x7f5e17b6f474 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:437  

#20 0x7f5e17b6ec67 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

#21 0x7f5e17b61e0b in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:98  

#22 0x7f5e183aabe4 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:160  

#23 0x7f5e183aa789 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3577  

#24 0x7f5e16fa0d0f in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:231  

#25 0x7f5e16fa0870 in WebCore::Event::defaultPrevented() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Event.h:133  

#26 0x7f5e16fcec42 in WebCore::Node::handleLocalEvents(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2755  

#27 0x7f5e170896f1 in WTF::PassRefPtr[WebCore::Event](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:76  

#28 0x7f5e170840d4 in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:51  

#29 0x7f5e17085e42 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:55  

#30 0x7f5e16fcf277 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2769  

#31 0x7f5e181e7afe in WebCore::DOMWindow::dispatchLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1548  

#32 0x7f5e16f1f418 in WebCore::Document::dispatchWindowLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3734  

#33 0x7f5e180f72e6 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:799  

#34 0x7f5e180f3ac8 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:680  

#35 0x7f5e16f4150a in WebCore::Frame::page() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.h:353  

#36 0x7f5e180d8bfc in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:249  

#37 0x7f5e18110399 in WebCore::ResourceErrorBase::isNull() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/network/ResourceErrorBase.h:42  

#38 0x7f5e18137701 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#39 0x7f5e198eaa3d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:662  

#40 0x7f5e1691c8aa in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#41 0x7f5e1691dacb in void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks>(ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /media/Chromium/chromium/depot\_tools/src/./base/tuple.h:566  

#42 0x7f5e1691a05c in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#43 0x7f5e16918290 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (85650897).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (57267916).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (85650897).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (57267916).  

BFD: Dwarf Error: Offset (1949266029) greater than or equal to .debug\_str size (85650897).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (57267916).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (85650897).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (57267916).  

BFD: Dwarf Error: Offset (1848602733) greater than or equal to .debug\_str size (85650897).  

BFD: Dwarf Error: Offset (1949237248) greater than or equal to .debug\_line size (57267916).  

#44 0x7f5e1681275f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:172  

#45 0x7f5e15524e13 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:268  

#46 0x7f5e1540d256 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#47 0x7f5e1540dab8 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#48 0x7f5e1540eda9 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#49 0x7f5e15419277 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#50 0x7f5e1540be1e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#51 0x7f5e1540a00f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#52 0x7f5e1a7e5b5c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#53 0x7f5e153624b6 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:245  

#54 0x7f5e15360a2a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#55 0x7f5e13dc7c97 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#56 0x7f5e13dc7beb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#57 0x7f5e0d1d7d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f5ddf9d2c80 is located 0 bytes inside of 520-byte region [0x7f5ddf9d2c80,0x7f5ddf9d2e88)  

freed by thread T0 here:  

#0 0x7f5e1bb679d2 in operator delete(void\*) ??:0  

#1 0x7f5e16eed098 in WebCore::TreeShared[WebCore::ContainerNode](javascript:void(0);)::deref() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/TreeShared.h:79  

#2 0x7f5e17018550 in WebCore::Range::surroundContents(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Range.cpp:1559  

#3 0x7f5e18bb2d18 in WebCore::RangeInternal::surroundContentsCallback(v8::Arguments const&) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webcore/bindings/V8Range.cpp:372  

#4 0x7f5e15eb0da3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1136  

#5 0x7f5de3f0614e  

#6 0x7f5de3f36559  

#7 0x7f5de3f43b7b  

#8 0x7f5de3f22647  

#9 0x7f5de3f11137  

#10 0x7f5e15eff278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#11 0x7f5e15e636f2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3608  

#12 0x7f5e17b6f474 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:437  

#13 0x7f5e17b6ec67 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

#14 0x7f5e17b61e0b in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:98  

#15 0x7f5e183aabe4 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:160  

#16 0x7f5e183aa789 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3577  

#17 0x7f5e16fa0d0f in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:231  

#18 0x7f5e16fa0870 in WebCore::Event::defaultPrevented() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Event.h:133  

#19 0x7f5e16fcec42 in WebCore::Node::handleLocalEvents(WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2755  

#20 0x7f5e170896f1 in WTF::PassRefPtr[WebCore::Event](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:76  

#21 0x7f5e170840d4 in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:51  

#22 0x7f5e17085e42 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:55  

#23 0x7f5e16fcf277 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:2769  

#24 0x7f5e181e7afe in WebCore::DOMWindow::dispatchLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1548  

#25 0x7f5e16f1f418 in WebCore::Document::dispatchWindowLoadEvent() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:3734  

#26 0x7f5e180f72e6 in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:799  

#27 0x7f5e180f3ac8 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:680  

#28 0x7f5e16f4150a in WebCore::Frame::page() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.h:353  

#29 0x7f5e180d8bfc in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:249  

previously allocated by thread T0 here:  

#0 0x7f5e1bb67852 in operator new(unsigned long) ??:0  

#1 0x7f5e1949c649 in WebCore::SVGTRefElement::create(WebCore::QualifiedName const&, WebCore::Document\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/svg/SVGTRefElement.cpp:61  

#2 0x7f5e19221536 in WTF::PassRefPtr[WebCore::SVGTRefElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#3 0x7f5e1921a728 in WTF::PassRefPtr[WebCore::SVGElement](javascript:void(0);)::operator WebCore::SVGElement\* WTF::PassRefPtr[WebCore::SVGElement](javascript:void(0);)::\*() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:82  

#4 0x7f5e16f0f7c8 in WTF::PassRefPtr[WebCore::SVGElement](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#5 0x7f5e16f10a63 in WTF::PassRefPtr[WebCore::Element](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#6 0x7f5e16f10db3 in WTF::PassRefPtr[WebCore::Node](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#7 0x7f5e18fa0bea in WTF::PassRefPtr[WebCore::Node](javascript:void(0);)::leakRef() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161  

#8 0x7f5e15eb0da3 in HandleApiCallHelper /media/Chromium/chromium/depot\_tools/src/v8/src/builtins.cc:1136  

#9 0x7f5de3f0614e  

#10 0x7f5de3f36496  

#11 0x7f5de3f43b7b  

#12 0x7f5de3f22647  

#13 0x7f5de3f11137  

#14 0x7f5e15eff278 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /media/Chromium/chromium/depot\_tools/src/v8/src/execution.cc:118  

#15 0x7f5e15e636f2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/v8/src/api.cc:3608  

#16 0x7f5e17b6f474 in WebCore::V8Proxy::instrumentedCallFunction(WebCore::Frame\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:437  

#17 0x7f5e17b6ec67 in WebCore::V8Proxy::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:407  

#18 0x7f5e17b61e0b in WebCore::V8LazyEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8LazyEventListener.cpp:98  

#19 0x7f5e183aabe4 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:160  

#20 0x7f5e183aa789 in ~Scope /media/Chromium/chromium/depot\_tools/src/v8/include/v8.h:3577  

#21 0x7f5e16fa0d0f in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:231  

#22 0x7f5e16fa0870 in WebCore::Event::defaultPrevented() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Event.h:133  

==3489== ABORTING  

Stats: 41M malloced (37M for red zones) by 73344 calls  

Stats: 1M realloced by 1743 calls  

Stats: 37M freed by 57647 calls  

Stats: 0M really freed by 0 calls  

Stats: 104M (26641 full pages) mmaped in 26 calls  

mmaps by size class: 8:65532; 9:16382; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 22:5;  

mallocs by size class: 8:57656; 9:8033; 10:4430; 11:1212; 12:336; 13:1194; 14:138; 15:249; 16:27; 17:49; 18:8; 19:7; 22:5;  

frees by size class: 8:43288; 9:7433; 10:4108; 11:958; 12:254; 13:1169; 14:121; 15:242; 16:20; 17:34; 18:8; 19:7; 22:5;  

rfrees by size class:  

Stats: malloc large: 69 small slow: 391  

Shadow byte and word:  

0x1febbbf3a590: fd  

0x1febbbf3a590: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1febbbf3a570: fa fa fa fa fa fa fa fa  

0x1febbbf3a578: fa fa fa fa fa fa fa fa  

0x1febbbf3a580: fa fa fa fa fa fa fa fa  

0x1febbbf3a588: fa fa fa fa fa fa fa fa  

=>0x1febbbf3a590: fd fd fd fd fd fd fd fd  

0x1febbbf3a598: fd fd fd fd fd fd fd fd  

0x1febbbf3a5a0: fd fd fd fd fd fd fd fd  

0x1febbbf3a5a8: fd fd fd fd fd fd fd fd  

0x1febbbf3a5b0: fd fd fd fd fd fd fd fd

## Attachments

- [tc-16-03-12-uaf.zip](attachments/tc-16-03-12-uaf.zip) (application/zip; charset=binary, 574 B)
- [118593-2.zip](attachments/118593-2.zip) (application/zip; charset=binary, 4.5 KB)

## Timeline

### in...@chromium.org (2012-03-16)

ClusterFuzz report coming soon - https://cluster-fuzz.appspot.com/testcase?key=26885842. it will help to set the rest of the impact tags.

Stephen, can you please help to triage.

### sc...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26885842

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f09ab08ec80
Crash State:
  - crash stack -
  WebCore::SVGStyledElement::buildPendingResourcesIfNeeded
  WebCore::SVGStyledElement::svgAttributeChanged
  - free stack -
  WebCore::ContainerNode::removeChild
  WebCore::Range::surroundContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=109205:109251

Minimized Testcase (0.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94miwXdx7bP8latykdXkvaQjFAg9_SU_FvMeFOfDWI55QJBoZ2jf2hSgAM7dhFojwMfuI1kErlyg1j-ihZP6UlWwIyBU0G8IyUyEnwYg7JC87POwGs9fVjo0pyn5Pj6FPKI4BI8yvbSeJjiIEpATr2_1tghVg

### in...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### pd...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### pd...@chromium.org (2012-03-18)

https://bugs.webkit.org/show_bug.cgi?id=81473

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### ax...@gmail.com (2012-03-21)

Just another testcase triggering the same bug through different path.

### in...@chromium.org (2012-03-21)

http://trac.webkit.org/changeset/111556

### pd...@chromium.org (2012-03-21)

I believe this second triggering testcase goes through a different codepath and requires a separate patch. Confirming...

### in...@chromium.org (2012-03-21)

Yeah best to file a new bug, also allows us to merge this one in time.

### sc...@gmail.com (2012-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-29)

M18: http://trac.webkit.org/changeset/112610

### sc...@gmail.com (2012-04-04)

$1000, thank you Arthur.

### sc...@gmail.com (2012-05-10)

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

This issue was migrated from crbug.com/chromium/118593?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055111)*
