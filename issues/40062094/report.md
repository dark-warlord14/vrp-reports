# UAF in DOMContentLoaded 

| Field | Value |
|-------|-------|
| **Issue ID** | [40062094](https://issues.chromium.org/issues/40062094) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2012-07-31 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

I used details in chrome <https://crbug.com/chromium/136840> to make this issue.

It is possible to cause webkit to fire a readystatechange event when pdf object is removed by removing the pdf object on DOMContentLoaded event. Then it is possible to append the removed pdf object back to document which causes a use after free later.

**VERSION**  

Chrome Version: [20.0.1132.57] + [stable]  

[22.0.1223.0 (149174)] + [trunk]  

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

1. Download test.html and test1.html and host on local web server.
2. Open test.html on chrome.
3. Wait for 2 seconds.
4. Page will display an alert box.
5. Click on ok button of alert box or press ESCAPE to remove the alert box.
6. Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: Asan output

==8939== ERROR: AddressSanitizer heap-use-after-free on address 0x7f6adabd9c9c at pc 0x7f6ae992e6aa bp 0x7fff44717bb0 sp 0x7fff44717ba8  

READ of size 4 at 0x7f6adabd9c9c thread T0  

#0 0x7f6ae992e6aa in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /third\_party/WebKit/Source/WebCore/dom/Node.h:716  

#1 0x7f6ae992e58e in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /third\_party/WebKit/Source/WebCore/dom/Element.cpp:1163  

#2 0x7f6ae98c2fa2 in WebCore::Node::nextSibling() const /third\_party/WebKit/Source/WebCore/dom/Node.h:168  

#3 0x7f6ae98c5098 in ~AnimationUpdateBlock /third\_party/WebKit/Source/WebCore/page/animation/AnimationController.h:100  

#4 0x7f6aead7eaa3 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /third\_party/WebKit/Source/WebCore/page/FrameView.cpp:3181  

#5 0x7f6aead51b1a in WebCore::FocusController::setActive(bool) /third\_party/WebKit/Source/WebCore/page/FocusController.cpp:669  

#6 0x7f6ae97a90ad in WebKit::WebViewImpl::setFocus(bool) /third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1874  

#7 0x7f6aed8044bd in RenderWidget::webwidget() const /./content/renderer/render\_widget.h:105  

#8 0x7f6aed817109 in void DispatchToMethod<RenderWidget, void (RenderWidget::\*)(bool), bool>(RenderWidget\*, void (RenderWidget::\*)(bool), Tuple1<bool> const&) /./base/tuple.h:546  

#9 0x7f6aed7bf85c in RenderViewImpl::OnMessageReceived(IPC::Message const&) /content/renderer/render\_view\_impl.cc:961  

#10 0x7f6ae91747d5 in MessageRouter::RouteMessage(IPC::Message const&) /content/common/message\_router.cc:47  

#11 0x7f6ae9174640 in MessageRouter::OnMessageReceived(IPC::Message const&) /content/common/message\_router.cc:40  

#12 0x7f6ae9071697 in ChildThread::OnMessageReceived(IPC::Message const&) /content/common/child\_thread.cc:257  

#13 0x7f6ae7b9fd46 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /ipc/ipc\_channel\_proxy.cc:257  

#14 0x7f6ae7a602f1 in base::Callback<void ()>::Run() const /./base/callback.h:388  

#15 0x7f6ae7a60aac in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /base/message\_loop.cc:472  

#16 0x7f6ae7a61d99 in MessageLoop::DoWork() /base/message\_loop.cc:648  

#17 0x7f6ae7a6c147 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /base/message\_pump\_default.cc:28  

#18 0x7f6ae7a5eefa in MessageLoop::RunInternal() /base/message\_loop.cc:420  

#19 0x7f6ae7aa7d82 in base::RunLoop::AfterRun() /base/run\_loop.cc:84  

#20 0x7f6ae7a5d397 in MessageLoop::Run() /base/message\_loop.cc:300  

#21 0x7f6aed83ebed in RendererMain(content::MainFunctionParams const&) /content/renderer/renderer\_main.cc:220  

#22 0x7f6ae790cab4 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:331  

#23 0x7f6ae790dd60 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:384  

#24 0x7f6ae790f480 in content::ContentMainRunnerImpl::Run() /content/app/content\_main\_runner.cc:634  

#25 0x7f6ae790c05a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /content/app/content\_main.cc:35  

#26 0x7f6ae6289f97 in ChromeMain /chrome/app/chrome\_main.cc:32  

#27 0x7f6ae6289efb in main /chrome/app/chrome\_exe\_main\_gtk.cc:18  

#28 0x7f6adf6ac76d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

0x7f6adabd9c9c is located 28 bytes inside of 192-byte region [0x7f6adabd9c80,0x7f6adabd9d40)  

freed by thread T0 here:  

#0 0x7f6aeee0e6c2 in operator delete(void\*) ??:0  

#1 0x7f6ae8673c3f in v8::internal::RuntimeProfiler::IsEnabled() /v8/src/runtime-profiler.h:50  

#2 0x7f6ae86735d2 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector) /v8/src/global-handles.cc:558  

#3 0x7f6ae8690e9d in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) /v8/src/heap.cc:923  

#4 0x7f6ae868ef42 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) /v8/src/heap.cc:588  

#5 0x7f6ae86c514e in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const\*) /v8/src/heap-inl.h:440  

#6 0x7f6ae8bd1b8f in v8::internal::V8::IdleNotification(int) /v8/src/v8.cc:194  

#7 0x7f6ae8521c85 in v8::V8::IdleNotification(int) /v8/src/api.cc:4309  

#8 0x7f6aea602b60 in WebCore::V8GCForContextDispose::pseudoIdleTimerFired(WebCore::Timer[WebCore::V8GCForContextDispose](javascript:void(0);)\*) /third\_party/WebKit/Source/WebCore/bindings/v8/V8GCForContextDispose.cpp:75  

#9 0x7f6aea1fa2c8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#10 0x7f6ae7af6d4e in ~Callback /./base/callback.h:359  

#11 0x7f6ae7a602f1 in base::Callback<void ()>::Run() const /./base/callback.h:388  

#12 0x7f6ae7a60aac in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /base/message\_loop.cc:472  

#13 0x7f6ae7a61d99 in MessageLoop::DoWork() /base/message\_loop.cc:648  

#14 0x7f6ae7a6c147 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /base/message\_pump\_default.cc:28  

#15 0x7f6ae7a5eefa in MessageLoop::RunInternal() /base/message\_loop.cc:420  

#16 0x7f6ae7aa7d82 in base::RunLoop::AfterRun() /base/run\_loop.cc:84  

#17 0x7f6ae7a5d397 in MessageLoop::Run() /base/message\_loop.cc:300  

#18 0x7f6aed83ebed in RendererMain(content::MainFunctionParams const&) /content/renderer/renderer\_main.cc:220  

#19 0x7f6ae790cab4 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:331  

#20 0x7f6ae790dd60 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:384  

#21 0x7f6ae790f480 in content::ContentMainRunnerImpl::Run() /content/app/content\_main\_runner.cc:634  

#22 0x7f6ae790c05a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /content/app/content\_main.cc:35  

#23 0x7f6ae6289f97 in ChromeMain /chrome/app/chrome\_main.cc:32  

#24 0x7f6ae6289efb in main /chrome/app/chrome\_exe\_main\_gtk.cc:18  

#25 0x7f6adf6ac76d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

previously allocated by thread T0 here:  

#0 0x7f6aeee0e542 in operator new(unsigned long) ??:0  

#1 0x7f6aee66a254 in WebCore::HTMLEmbedElement::create(WebCore::QualifiedName const&, WebCore::Document\*, bool) /third\_party/WebKit/Source/WebCore/html/HTMLEmbedElement.cpp:55  

#2 0x7f6aebf2aaaa in WTF::PassRefPtr[WebCore::HTMLEmbedElement](javascript:void(0);)::leakRef() const /third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:104  

#3 0x7f6aebf247bd in WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::operator WebCore::HTMLElement\* WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::\*() const /third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:82  

#4 0x7f6aea17c29e in WTF::PassRefPtr[WebCore::HTMLElement](javascript:void(0);)::leakRef() const /third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:104  

#5 0x7f6aea0b5006 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken\*) /third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:916  

#6 0x7f6aea0a55d5 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken\*) /third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1205  

#7 0x7f6aea0a472b in WebCore::HTMLTreeBuilder::processToken(WebCore::AtomicHTMLToken\*) /third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:497  

#8 0x7f6aea0a179c in WebCore::HTMLElementStack::stackDepth() const /third\_party/WebKit/Source/WebCore/html/parser/HTMLElementStack.h:79  

#9 0x7f6aea0a15d8 in WebCore::AtomicMarkupTokenBase[WebCore::HTMLToken](javascript:void(0);)::clearExternalCharacters() /third\_party/WebKit/Source/WebCore/xml/parser/MarkupTokenBase.h:497  

#10 0x7f6aea04eeeb in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) /third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:254  

#11 0x7f6aea05094a in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) /third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:363  

#12 0x7f6aee380a5c in ~Deque /third\_party/WebKit/Source/WTF/wtf/Deque.h:370  

#13 0x7f6aeabd27cb in WebCore::DocumentWriter::end() /third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:238  

#14 0x7f6aeabbd2e1 in WebCore::ResourceErrorBase::isNull() const /third\_party/WebKit/Source/WebCore/platform/network/ResourceErrorBase.h:42  

#15 0x7f6aeac37fe6 in WebCore::MainResourceLoader::didFinishLoading(double) /third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:521  

#16 0x7f6aec7a0387 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /webkit/glue/weburlloader\_impl.cc:672  

#17 0x7f6ae9187e5b in content::ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /content/common/resource\_dispatcher.cc:473  

#18 0x7f6ae9188e8b in void DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks>(content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /./base/tuple.h:565  

#19 0x7f6ae918571d in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) /content/common/resource\_dispatcher.cc:543  

#20 0x7f6ae9183621 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) /content/common/resource\_dispatcher.cc:310  

#21 0x7f6ae90711c7 in ChildThread::OnMessageReceived(IPC::Message const&) /content/common/child\_thread.cc:223  

#22 0x7f6ae7b9fd46 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /ipc/ipc\_channel\_proxy.cc:257

## Attachments

- [test.html](attachments/test.html) (text/html; charset=us-ascii, 196 B)
- [test1.html](attachments/test1.html) (text/html; charset=us-ascii, 564 B)
- [test2.html](attachments/test2.html) (text/html; charset=us-ascii, 662 B)
- [test3.html](attachments/test3.html) (text/html; charset=us-ascii, 662 B)
- [test4.html](attachments/test4.html) (text/html; charset=us-ascii, 707 B)
- [test4_arraybuffer.html](attachments/test4_arraybuffer.html) (text/html; charset=us-ascii, 870 B)
- [test5.html](attachments/test5.html) (text/html; charset=us-ascii, 790 B)
- deleted (application/octet-stream, 0 B)
- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 490 B)

## Timeline

### ch...@gmail.com (2012-08-02)

Does this issue reproduce for you?

### ke...@chromium.org (2012-08-02)

I have reproduced a crash which looks like a NULL pointer deref, but I've only been able to try it on Windows so far. Someone will have to try this manually under ASAN still.

### ch...@gmail.com (2012-08-02)

kenrb, I also get a null pointer error. But I get null pointer error only when I open test1.html only.

When I open test.html and wait 2 seconds for test.html to redirect to test1.html, I get heap use after free error.

### ch...@gmail.com (2012-08-03)

Attaching another test case which needs only one html page.

Steps
=====
1. Download and host test2.html on local web server.
2. Open test2.html on chrome.
3. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
4. Page will reload itself after 5 seconds.
5. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
   Chrome will display sad tab due to heap use after free.

* Do not click anywhere on the document. Then chrome will crash due to null pointer deref.

### ch...@gmail.com (2012-08-03)

Shockwave flash plugin also has the same issue .Shall I report a new issue for it?

### sc...@gmail.com (2012-08-03)

No, it sounds like a generic issue with Chrome.

### ke...@chromium.org (2012-08-03)

We've tried this on different platforms and with ASAN now, following your instructions, and we can't recreate the crash stack you posted above. It's still true that all I can get is a NULL pointer crash.

Can you work on a better repro? I'm marking WontFix for now but if you can give us something reproduces on our end then I can reopen.

### ch...@gmail.com (2012-08-04)

kenrb, Can you post the Asan or gdb backtrace you get please? That will help me to find out why you are getting null pointer crash and produce a better repro.

Also do you get eventDispatchForbidden assert failiure on debug build?

### ch...@gmail.com (2012-08-04)

Generated crash reports on chrome stable version 20.0.1132.57. Here are the crash ids.

Crash ID 3e8edddcbd65d1a7
Crash ID e6b49fd784854dac

Is it possible to check this issue using these crash ids (Use after free or null deref)?

### ch...@gmail.com (2012-08-07)

Attached a slightly modified reproduction case. Please check this reproduction case.

Steps
=====
1. Download and host test3.html on local web server.
2. Open test3.html on chrome.
3. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
4. Page will display an alert box again.
   Press escape to dismiss alert box or click ok button of alert box.
5. Page will display an alert box again for third time.
   Press escape to dismiss alert box or click ok button of alert box.
   Chrome will display sad tab due to heap use after free.

### ke...@chromium.org (2012-08-07)


One of those crash reports does look like a use after free:
http://crash.corp.google.com/reportdetail?reportid=3e8edddcbd65d1a7

The other is a NULL pointer:
http://crash.corp.google.com/reportdetail?reportid=e6b49fd784854dac

And I also managed to get this crash on my own system:
http://crash.corp.google.com/reportdetail?reportid=94307d660f18be87

I can't make this happen in debug, and we haven't seen it under ASAN yet either, so it's hard to see what is happening, but it seems to warrant more looking into.

### ch...@gmail.com (2012-08-07)

kentb, Does the reproduction case I attached on https://crbug.com/chromium/139814#c10 crash with use after free?

### ch...@gmail.com (2012-08-09)

Analysis of this issue
======================
1. Web page has embed tag which embeds a pdf file.
2. This embed element is removed on DOMContentLoaded event of document.
3. This causes a readystatechange event to fire prematurely.
   This is the stacktrace that demonstrates how readystatechange event is fired on plugin removal. This is also the stacktrace that debug build crashes due to event dispatchForbidden assert failiure.
   Program received signal SIGSEGV, Segmentation fault.
0x0000555568080da3 in WebCore::EventDispatcher::dispatchEvent (
    node=<error reading variable: Unhandled dwarf expression opcode 0x1>, 
    mediator=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:125
125         ASSERT(!eventDispatchForbidden());
(gdb) bt
#0  0x0000555568080da3 in WebCore::EventDispatcher::dispatchEvent (
    node=<error reading variable: Unhandled dwarf expression opcode 0x1>, 
    mediator=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:125
#1  0x0000555567d0a793 in WebCore::Node::dispatchEvent (
    this=<error reading variable: Unhandled dwarf expression opcode 0x0>, 
    event=...) at third_party/WebKit/Source/WebCore/dom/Node.cpp:2581
#2  0x00005555678ad132 in WebCore::Document::setReadyState (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>, 
    readyState=<error reading variable: Unhandled dwarf expression opcode 0x0>)
    at third_party/WebKit/Source/WebCore/dom/Document.cpp:122
#3  0x000055556c3164d5 in WebCore::FrameLoader::checkCompleted (
    this=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:706
#4  0x000055556c316b83 in WebCore::FrameLoader::loadDone (this=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:655
#5  0x000055556c57854f in WebCore::CachedResourceLoader::loadDone (
    this=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:663
#6  0x000055556c46b48e in WebCore::SubresourceLoader::releaseResources (
    this=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:319
#7  0x000055556c44a0cc in WebCore::ResourceLoader::cancel (
    this=<optimized out>, 
    error=<error reading variable: Unhandled dwarf expression opcode 0xff>)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:390
#8  0x000055556c445808 in WebCore::ResourceLoader::cancel (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:339
#9  0x000055556c465f6b in WebCore::SubresourceLoader::cancelIfNotFinishing (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:129
#10 0x000055556d9aed1c in WebCore::CachedRawResource::allClientsRemoved (
    this=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:94
#11 0x000055556c515e15 in WebCore::CachedResource::removeClient (
    this=<optimized out>, client=<optimized out>)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:443
#12 0x000055556c28eb91 in WebCore::DocumentThreadableLoader::clearResource (
    this=<error reading variable: Unhandled dwarf expression opcode 0xa1>)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:175
#13 0x000055556c28e531 in WebCore::DocumentThreadableLoader::cancel (
    this=<error reading variable: Unhandled dwarf expression opcode 0x9a>)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:157
#14 0x000055556746114e in WebKit::AssociatedURLLoader::cancel (
    this=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:366
#15 0x000055556745f511 in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:305
#16 0x000055556745f35b in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:304
#17 0x00005555727753de in scoped_ptr<WebKit::WebURLLoader>::~scoped_ptr (
    this=<error reading variable: Unhandled dwarf expression opcode 0xd0>)
    at ./base/memory/scoped_ptr.h:166
#18 0x0000555572770bb3 in scoped_ptr<WebKit::WebURLLoader>::~scoped_ptr (
    this=<optimized out>) at ./base/memory/scoped_ptr.h:164
#19 0x000055557c636e7d in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl (this=<optimized out>) at webkit/plugins/ppapi/ppb_url_loader_impl.cc:87
#20 0x000055557c636bfb in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl (this=<optimized out>) at webkit/plugins/ppapi/ppb_url_loader_impl.cc:86
#21 0x000055555d91cc1b in base::RefCounted<ppapi::Resource>::Release ( this=<optimized out>) at ./base/memory/ref_counted.h:91
#22 0x0000555567020cee in ppapi::ResourceTracker::ReleaseResource (
    this=<optimized out>, res=<optimized out>)
    at ppapi/shared_impl/resource_tracker.cc:71
#23 0x00005555725a69c9 in webkit::ppapi::(anonymous namespace)::ReleaseResource
    (resource=<optimized out>) at webkit/plugins/ppapi/plugin_module.cc:165
#24 0x00007fffe9ee4209 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Debug/libpdf.so
#25 0x0000555576690d25 in ppapi::CallWhileUnlocked<void, int> (
    function=<optimized out>, p1=<optimized out>)
    at ./ppapi/shared_impl/proxy_lock.h:93
#26 0x000055557ac336f3 in ppapi::PPP_Instance_Combined::DidDestroy (
    this=<optimized out>, instance=<optimized out>)
    at ppapi/shared_impl/ppp_instance_combined.cc:55
#27 0x00005555725d64e6 in webkit::ppapi::PluginInstance::Delete (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at webkit/plugins/ppapi/ppapi_plugin_instance.cc:405
#28 0x000055557c626c80 in webkit::ppapi::WebPluginImpl::destroy (
    this=<optimized out>) at webkit/plugins/ppapi/ppapi_webplugin_impl.cc:118
#29 0x00005555672ca8f9 in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=<error reading variable: Unhandled dwarf expression opcode 0x0>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:632
#30 0x00005555672ca4db in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:626
#31 0x00005555672df66b in WTF::RefCounted<WebCore::Widget>::deref (
    this=<optimized out>) at third_party/WebKit/Source/WTF/wtf/RefCounted.h:190
#32 0x000055556998ae4e in WTF::derefIfNotNull<WebCore::Widget> (
    ptr=<error reading variable: Asked for position 0 of stack, stack only has 0 elements on it.>) at third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:52
#33 0x000055556998aced in WTF::RefPtr<WebCore::Widget>::~RefPtr (
    this=<optimized out>) at third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
#34 0x000055556998a653 in WTF::RefPtr<WebCore::Widget>::~RefPtr (
    this=<optimized out>) at third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
#35 0x000055556e7b3143 in WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>::~KeyValuePair (this=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/HashTraits.h:188
#36 0x000055556e7b3033 in WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>::~KeyValuePair (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at third_party/WebKit/Source/WTF/wtf/HashTraits.h:188
#37 0x000055556e7b2d55 in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::deallocateTable (
    table=<optimized out>, 
    size=<error reading variable: DWARF-2 expression error: DW_OP_reg operations must be used either alone or in conjunction with DW_OP_piece or DW_OP_bit_piece.>) at third_party/WebKit/Source/WTF/wtf/HashTable.h:1089
#38 0x000055556e7bd5fa in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::~HashTable (
    this=<optimized out>) at third_party/WebKit/Source/WTF/wtf/HashTable.h:371
#39 0x000055556e7bd443 in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::~HashTable (
    this=<optimized out>) at third_party/WebKit/Source/WTF/wtf/HashTable.h:368
#40 0x000055556e7bd333 in WTF::HashMap<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >::~HashMap (
    this=<error reading variable: Unhandled dwarf expression opcode 0x0>)
    at third_party/WebKit/Source/WTF/wtf/RefPtrHashMap.h:32
#41 0x000055556e796ac3 in WTF::HashMap<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >::~HashMap (
    this=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/RefPtrHashMap.h:32
#42 0x000055556e78d1c5 in WebCore::RenderWidget::resumeWidgetHierarchyUpdates
    () at third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:83
#43 0x0000555567b5aa8a in WebCore::Element::detach (this=<optimized out>)
    at third_party/WebKit/Source/WebCore/dom/Element.cpp:1005
#44 0x00005555699868c1 in WebCore::HTMLPlugInElement::detach (
    this=<optimized out>)
    at third_party/WebKit/Source/WebCore/html/HTMLPlugInElement.cpp:88
#45 0x000055556998fb5a in WebCore::HTMLPlugInImageElement::detach (
    this=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at third_party/WebKit/Source/WebCore/html/HTMLPlugInImageElement.cpp:183
#46 0x0000555567810dc9 in WebCore::ContainerNode::removeBetween (
    this=<optimized out>, previousChild=<optimized out>, 
    nextChild=<error reading variable: Unhandled dwarf expression opcode 0x0>, 
    oldChild=<error reading variable: Unhandled dwarf expression opcode 0x0>)
#47 0x000055556780fd8b in WebCore::ContainerNode::removeChild (
    this=<optimized out>, 
    oldChild=<error reading variable: Unhandled dwarf expression opcode 0x0>, 
    ec=<optimized out>)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:405
#48 0x0000555567cddd20 in WebCore::Node::removeChild (this=<optimized out>, 
    oldChild=<optimized out>, ec=<optimized out>)
    at third_party/WebKit/Source/WebCore/dom/Node.cpp:616
#49 0x000055556b138162 in WebCore::V8Node::removeChildCallback (args=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:105
#50 0x00005555619b77c7 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at v8/src/builtins.cc:1145
#51 0x00005555619b6536 in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
    isolate=<error reading variable: Unhandled dwarf expression opcode 0x1>)
    at v8/src/builtins.cc:1162
#52 0x000055556198c31b in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=<optimized out>) at v8/src/builtins.cc:1161

4. Then on readystatechange event removed embed element is attached to the document again. This is the cause of use after free.

### [Deleted User] (2012-08-09)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=93639

### ch...@gmail.com (2012-08-14)

Can I get permission to view the webkit bug please? My user name is chamalsl@yahoo.com.

### in...@chromium.org (2012-08-16)

Chamal, do you have a better testcase to help in reproducing this ?

### ch...@gmail.com (2012-08-17)

Inferno, What happens when you run test case attached in https://crbug.com/chromium/139814#c10?
If it crashes with a null pointer can you please give me the gdb or asan backtrace. It will help me to identify why this test case crash with nullpointer on your machines and produce a better reproduction case.

Also I am using pepper pdf plugin which comes with chrome developer version 22.0.1215.0. Are you using a newer version?

### ch...@gmail.com (2012-08-18)

I forgot to mention one reproduction step. Need to do this when reproducing in trunk build.

Copy libpdf.so (Pepper pdf plugin) to $SRC/out/Release folder.

### ch...@gmail.com (2012-08-19)

Added a new test case.

Steps
=====
1. If you are testing on trunk build copy libpdf.so (Pepper pdf plugin) to $SRC/out/Release folder.
2. Download and host test4.html on local web server.
3. Open test4.html on chrome.
4. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
5. Wait 30 seconds.
   This wait is necessary for garbage collector to fire.
   Is there a way to manually trigger garbage collector?
   During this wait do not click on document body or move mouse. Then chrome will crash due to null pointer.

Chrome will display sad tab due to use after free.


### [Deleted User] (2012-08-22)

It appears that this reproduction requires Adobe Acrobat NPAPI Plug-in. It doesn't reproduce on Safari or trunk build Chromium where the plugin is not available.

### pa...@google.com (2012-08-24)

rniwa: Sadly no, I can consistently repro it in an ASAN build on Linux with our PDF plugin.

### in...@chromium.org (2012-08-29)

[Comment Deleted]

### in...@chromium.org (2012-08-29)

Sorry wrong bug.

### in...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-09-04)

Attached a test case which allocates ArrayBufferContents object of a ArrayBuffer on the freed slot of HTMLEmbedElement. Then that memory is filled with "A" characters.

Steps
=====

1. If you are testing on trunk build copy libpdf.so (Pepper pdf plugin) to $SRC/out/Release folder.
2. Download and host test4_arraybuffer.html on local web server.
3. Run 
   out/Release/chrome --disable-seccomp-sandbox --renderer-cmd-prefix='xterm -title renderer -e gdb --args' http://127.0.0.1/test4_arraybuffer.html
4. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
5. Wait 30 seconds.
   This wait is necessary for garbage collector to fire.
   During this wait do not click on document body or move mouse. Then chrome will crash due to null pointer.
6. Then gdb will show this error message. Type p n on gdb to view the value of n.

Program received signal SIGSEGV, Segmentation fault.
WebCore::Element::recalcStyle (this=0x55555a83b840, 
    change=WebCore::Node::NoChange)
    at third_party/WebKit/Source/WebCore/dom/Element.cpp:1154
1154            if (n->isTextNode()) {
(gdb) p n
$1 = (WebCore::Node *) 0x4141414141414141





### sc...@gmail.com (2012-09-04)

Thanks Chamal, sounds interesting!

### sc...@gmail.com (2012-09-06)

I suppose I should look at this, since no-one else is :-)

### sc...@gmail.com (2012-09-06)

In debug:

ASSERT(!eventDispatchForbidden());
#0  0x00007f10620a02da in WebCore::EventDispatcher::dispatchEvent (
    node=0x7f1052378000, mediator=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:126
#1  0x00007f10620352d8 in WebCore::Node::dispatchEvent (this=0x7f1052378000, 
    event=...) at third_party/WebKit/Source/WebCore/dom/Node.cpp:2591
#2  0x00007f1061fa4994 in WebCore::Document::setReadyState (
    this=0x7f1052378000, readyState=WebCore::Document::Complete)
    at third_party/WebKit/Source/WebCore/dom/Document.cpp:1237
#3  0x00007f1062cdba4d in WebCore::FrameLoader::checkCompleted (
    this=0x7f105fc05c98)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:746
#4  0x00007f1062cdb856 in WebCore::FrameLoader::loadDone (this=0x7f105fc05c98)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:695
#5  0x00007f1062d32a23 in WebCore::CachedResourceLoader::loadDone (
    this=0x7f105fbd38c0)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:663
#6  0x00007f1062d1047c in WebCore::SubresourceLoader::releaseResources (
    this=0x7f105239ec00)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:339
#7  0x00007f1062d0b543 in WebCore::ResourceLoader::cancel (
    this=0x7f105239ec00, error=...)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:395
---Type <return> to continue, or q <return> to quit---
#8  0x00007f1062d0b2f3 in WebCore::ResourceLoader::cancel (this=0x7f105239ec00)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:344
#9  0x00007f1062d0f299 in WebCore::SubresourceLoader::cancelIfNotFinishing (
    this=0x7f105239ec00)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:135
#10 0x00007f1062fd93c3 in WebCore::CachedRawResource::allClientsRemoved (
    this=0x7f1051d90400)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:94
#11 0x00007f1062d268b8 in WebCore::CachedResource::removeClient (
    this=0x7f1051d90400, client=0x7f1051ddb388)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:443
#12 0x00007f1062ccc5cd in WebCore::DocumentThreadableLoader::clearResource (
    this=0x7f1051ddb360)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:175
#13 0x00007f1062ccc4e9 in WebCore::DocumentThreadableLoader::cancel (
    this=0x7f1051ddb360)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:157
#14 0x00007f1061f2102d in WebKit::AssociatedURLLoader::cancel (
    this=0x7f1051dd6d40)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:364
---Type <return> to continue, or q <return> to quit---
#15 0x00007f1061f20a2c in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x7f1051dd6d40, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:303
#16 0x00007f1061f20a9a in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x7f1051dd6d40, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:304
#17 0x00007f106392510d in scoped_ptr<WebKit::WebURLLoader>::~scoped_ptr (
    this=0x7f1051afd630, __in_chrg=<optimized out>)
    at ./base/memory/scoped_ptr.h:166
#18 0x00007f1064bea3b8 in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl (this=0x7f1051afd580, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppb_url_loader_impl.cc:86
#19 0x00007f1064bea432 in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl (this=0x7f1051afd580, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppb_url_loader_impl.cc:87
#20 0x00007f10611c2a82 in base::RefCounted<ppapi::Resource>::Release (
    this=0x7f1051afd588) at ./base/memory/ref_counted.h:92
#21 0x00007f1061e9a403 in ppapi::ResourceTracker::ReleaseResource (
    this=0x7f105fbd4710, res=190) at ppapi/shared_impl/resource_tracker.cc:71
#22 0x00007f10638edc95 in webkit::ppapi::(anonymous namespace)::ReleaseResource
    (resource=190) at webkit/plugins/ppapi/plugin_module.cc:165
---Type <return> to continue, or q <return> to quit---
#23 0x00007f105378ae9b in pp::Core::ReleaseResource (this=0x7f105fbad7a0, 
    resource=190) at ./ppapi/cpp/core.h:42
#24 0x00007f105384566a in pp::Resource::~Resource (this=0x7f105fbe6108, 
    __in_chrg=<optimized out>) at ppapi/cpp/resource.cc:24
#25 0x00007f105374f65a in pp::URLLoader::~URLLoader (this=0x7f105fbe6108, 
    __in_chrg=<optimized out>) at ./ppapi/cpp/url_loader.h:23
#26 0x00007f10537589ca in chrome_pdf::Instance::~Instance (
    this=0x7f105fbe6000, __in_chrg=<optimized out>) at pdf/instance.cc:284
#27 0x00007f1053758ad0 in chrome_pdf::Instance::~Instance (
    this=0x7f105fbe6000, __in_chrg=<optimized out>) at pdf/instance.cc:286
#28 0x00007f105384202b in pp::Instance_DidDestroy (instance=-2118424679)
    at ppapi/cpp/module.cc:89
#29 0x00007f10644453ff in ppapi::CallWhileUnlocked<void, int> (
    function=0x7f1053841f7d <pp::Instance_DidDestroy(int)>, 
    p1=@0x7fff6f3bb2a4: -2118424679) at ./ppapi/shared_impl/proxy_lock.h:93
#30 0x00007f1064924086 in ppapi::PPP_Instance_Combined::DidDestroy (
    this=0x7f10523a9740, instance=-2118424679)
    at ppapi/shared_impl/ppp_instance_combined.cc:55
#31 0x00007f10638f5c41 in webkit::ppapi::PluginInstance::Delete (
    this=0x7f105fc77380) at webkit/plugins/ppapi/ppapi_plugin_instance.cc:514
#32 0x00007f1064be8195 in webkit::ppapi::WebPluginImpl::destroy (
    this=0x7f10524075a0) at webkit/plugins/ppapi/ppapi_webplugin_impl.cc:118
#33 0x00007f1061eeae5f in WebKit::WebPluginContainerImpl::~WebPluginContainerImp---Type <return> to continue, or q <return> to quit---
l (this=0x7f1052408e40, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:655
#34 0x00007f1061eeaef4 in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=0x7f1052408e40, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:656
#35 0x00007f1061eed7aa in WTF::RefCounted<WebCore::Widget>::deref (
    this=0x7f1052408e48) at third_party/WebKit/Source/WTF/wtf/RefCounted.h:190
#36 0x00007f1062762381 in WTF::derefIfNotNull<WebCore::Widget> (
    ptr=0x7f1052408e40) at third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53
#37 0x00007f106276229f in WTF::RefPtr<WebCore::Widget>::~RefPtr (
    this=0x7f1051b4d800, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
#38 0x00007f10631f22f0 in WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>::~KeyValuePair (this=0x7f1051b4d800, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/HashTraits.h:188
#39 0x00007f10631f22b9 in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::deallocateTable (
---Type <return> to continue, or q <return> to quit---
    table=0x7f1051b4d480, size=64)
    at third_party/WebKit/Source/WTF/wtf/HashTable.h:1089
#40 0x00007f10631f1ae4 in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::~HashTable (
    this=0x7fff6f3bb490, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/HashTable.h:371
#41 0x00007f10631f1828 in WTF::HashMap<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >::~HashMap (
    this=0x7fff6f3bb490, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/RefPtrHashMap.h:32
#42 0x00007f10631efbaa in WebCore::RenderWidget::resumeWidgetHierarchyUpdates
    () at third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:82
#43 0x00007f1061ffaea4 in WebCore::Element::detach (this=0x7f105fbd3460)
    at third_party/WebKit/Source/WebCore/dom/Element.cpp:1043
#44 0x00007f1062761879 in WebCore::HTMLPlugInElement::detach (
    this=0x7f105fbd3460)
    at third_party/WebKit/Source/WebCore/html/HTMLPlugInElement.cpp:90
#45 0x00007f106276305a in WebCore::HTMLPlugInImageElement::detach (
---Type <return> to continue, or q <return> to quit---
    this=0x7f105fbd3460)
    at third_party/WebKit/Source/WebCore/html/HTMLPlugInImageElement.cpp:183
#46 0x00007f1061f8dcf0 in WebCore::ContainerNode::removeBetween (
    this=0x7f1052395b80, previousChild=0x7f10523c9060, 
    nextChild=0x7f10523c9120, oldChild=0x7f105fbd3460)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:442
#47 0x00007f1061f8db77 in WebCore::ContainerNode::removeChild (
    this=0x7f1052395b80, oldChild=0x7f105fbd3460, ec=@0x7fff6f3bb738: 0)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:423
#48 0x00007f106202dce9 in WebCore::Node::removeChild (this=0x7f1052395b80, 
    oldChild=0x7f105fbd3460, ec=@0x7fff6f3bb738: 0)
    at third_party/WebKit/Source/WebCore/dom/Node.cpp:617
#49 0x00007f1062a6bedb in WebCore::V8Node::removeChildCallback (args=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:104
#50 0x00007f106230c934 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=0x7f105fbae000) at v8/src/builtins.cc:1146
#51 0x00007f1062307754 in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
    isolate=0x7f105fbae000) at v8/src/builtins.cc:1163
#52 0x00007f1062307725 in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=0x7f105fbae000) at v8/src/builtins.cc:1162
#53 0x00002b129c00618e in ?? ()
...
#76 0x0000000000000000 in ?? ()
[The stack does not symbolize back out of v8]

Not sure if it's related, but there seems to be a high degree of re-entrancy here :-)

### sc...@gmail.com (2012-09-07)

Sorry, Chamal, I see I just duplicated the ASSERT you mentioned in https://crbug.com/chromium/139814#c13

### sc...@gmail.com (2012-09-07)

Heya Chamal, if you wanted to fiddle with a more reliable repro, I have an exciting Chrome command-line flag for you!

--js-flags="--expose-gc"

It then enables your PoC to use the function "window.gc()" which can run GC in a more deterministic manner.

Anyway, I'm no expert here but I'm 99% sure that the problem here is re-entering Javascript whilst in the middle of a DOM mutation (removeChild). This happens because  the detach of the plug-in is canceling all its pending URL loads, which in return fires document readiness state change events -> oops.

I need to look into this more tomorrow, but it may be timing sensitive if the repro needs to hit the "URL load cancel" path whilst the load is still in-flight.

Chamal, were you successful ever in getting this to repro with the repro files hosted on the filesystem instead of HTTP ?

### sc...@gmail.com (2012-09-07)

Adding Adam Barth and Nate too, since it involves an event firing from within the loader machinery.

### ch...@gmail.com (2012-09-07)

[Comment Deleted]

### ch...@gmail.com (2012-09-07)

Scarybeasts, Thanks a lot for the flag --js-flags="--expose-gc". It's great. Managed to reduce the time of test case. Please see the attached test case.

Steps
=====
1. If you are testing on trunk build copy libpdf.so (Pepper pdf plugin) to $SRC/out/Release folder.
2. Download and host test5.html on local web server.
3. Run chrome with these flags.
   out/Release/chrome --js-flags="--expose-gc"
4. Open test5.html on chrome.
5. Page will display an alert box.
   Press escape to dismiss alert box or click ok button of alert box.
6. Wait 4 seconds. Do not click on document body or move mouse over embed element area.
7. Chrome will display sad tab due to heap use after free.

It is also possible to reproduce by repro files hosted on the filesystem instead of HTTP.

### sc...@gmail.com (2012-09-07)

Yeah, repro 5 is working good for me on the local filesystem now. Nice. I like the way "test.pdf" doesn't even have to exist.
I put back in the "buffer = new ArrayBuffer(177);" line etc. into the collectGarbage() function in test5.html. I do now see 0x4141414141 etc. in gdb, nice :)

### sc...@gmail.com (2012-09-07)

Ok 

### ts...@chromium.org (2012-09-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-10)

Tom volunteered to take a look.

### sc...@gmail.com (2012-09-10)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-09-10)

Heh.  I think npapi has the same problem with tripping the assert; here's the relevant snippet of it's stack(other portions are similar to ppapi case):
.
.
.
#14 0x00007f9c81aa1d89 in WebKit::AssociatedURLLoader::cancel (
    this=0x7f9c72179b40)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:364
#15 0x00007f9c84755a96 in webkit::npapi::WebPluginImpl::TearDownPluginInstance (
    this=0x7f9c7231e540, loader_to_ignore=0x0)
    at webkit/plugins/npapi/webplugin_impl.cc:1416
#16 0x00007f9c84754aaa in webkit::npapi::WebPluginImpl::SetContainer (
    this=0x7f9c7231e540, container=0x0)
    at webkit/plugins/npapi/webplugin_impl.cc:1110
#17 0x00007f9c8475054d in webkit::npapi::WebPluginImpl::destroy (
    this=0x7f9c7231e540) at webkit/plugins/npapi/webplugin_impl.cc:288
#18 0x00007f9c81a6bc63 in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=0x7f9c721b5d80, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:655
#19 0x00007f9c81a6bcf8 in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=0x7f9c721b5d80, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:656
#20 0x00007f9c81a6e5ae in WTF::RefCounted<WebCore::Widget>::deref (
.
.
.


### ts...@chromium.org (2012-09-10)

One change that avoids the assert:


Index: webkit/plugins/ppapi/ppapi_webplugin_impl.cc
===================================================================
--- webkit/plugins/ppapi/ppapi_webplugin_impl.cc	(revision 155002)
+++ webkit/plugins/ppapi/ppapi_webplugin_impl.cc	(working copy)
@@ -72,6 +72,12 @@
 }
 
 WebPluginImpl::~WebPluginImpl() {
+  if (instance_) {
+    ::ppapi::PpapiGlobals::Get()->GetVarTracker()->ReleaseVar(instance_object_);
+    instance_object_ = PP_MakeUndefined();
+    instance_->Delete();
+    instance_ = NULL;
+  }
 }
 
 WebKit::WebPluginContainer* WebPluginImpl::container() const {
@@ -112,13 +118,6 @@
 }
 
 void WebPluginImpl::destroy() {
-  if (instance_) {
-    ::ppapi::PpapiGlobals::Get()->GetVarTracker()->ReleaseVar(instance_object_);
-    instance_object_ = PP_MakeUndefined();
-    instance_->Delete();
-    instance_ = NULL;
-  }
-
   MessageLoop::current()->DeleteSoon(FROM_HERE, this);
 }
 

A similar change could be made to NPAPI

### ts...@chromium.org (2012-09-10)

But that can't work because it defers it too long and other things are gone. sigh.

### ts...@chromium.org (2012-09-11)

This is the only way out I can envision:

Index: third_party/WebKit/Source/WebCore/dom/Document.cpp
===================================================================
--- third_party/WebKit/Source/WebCore/dom/Document.cpp	(revision 127533)
+++ third_party/WebKit/Source/WebCore/dom/Document.cpp	(working copy)
@@ -1234,8 +1234,9 @@
     }
 
     m_readyState = readyState;
-    dispatchEvent(Event::create(eventNames().readystatechangeEvent, false, false));
-    
+    enqueueDocumentEvent(Event::create(eventNames().readystatechangeEvent,
+                                       false, false));
+
 

### sc...@gmail.com (2012-09-11)

I'd go for that. Does it pass tests? FWIW, I should imagine a lot of ready state change events are already asynchronous on account of network involvement.

### ts...@chromium.org (2012-09-11)

Haven't tried tests yet.  An alternative would be to have a flag in Document that either dispatches or deferrs, and set/clear that in ContainerNode::removeBetween().  Might catch other unknown cases.

### sc...@gmail.com (2012-09-12)

The simplicity of always going async seems preferable. Don't want WebKit to become even more of a proliferation of magic flags and states :)

### ts...@chromium.org (2012-09-12)

The fix in C42 wont work as it turns out, it just kicks the can a little further down the road until the possibility of another event arising from Document::dispatchWindowLoadEvent().

I'm left wondering if one can defer the resumeWidgetHierarchyUpdates by adding another set of macthing suspend/resume calls further down the stack.

### sc...@gmail.com (2012-09-13)

Should Document::dispatchWindowLoadEvent() be asynchronous too?

### ts...@chromium.org (2012-09-13)

Landed in http://trac.webkit.org/changeset/128524

### sc...@gmail.com (2012-09-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-17)

M22: http://trac.webkit.org/changeset/128807

### sc...@gmail.com (2012-09-25)

Hello Chamal!
So a $1000 base reward for the high severity UAF.
And a $1000 bonus top-up for the repro that demonstrated 0x4141414141414141 in the freed object slot! Congrats and nice work.

Total reward: $2000

### ch...@gmail.com (2012-09-25)

Wow. Thanks a lot for the higher reward :)

### sc...@gmail.com (2012-10-12)

Paid.

### ch...@gmail.com (2012-11-05)

It is possible to reproduce this issue in a different way.

Reproduction Case
-----------------
1. Open repro.html on chrome.

Address Sanitizer output
------------------------
==5595== ERROR: AddressSanitizer heap-use-after-free on address 0x7f3aa79d9270 at pc 0x7f3aba7bee43 bp 0x7fff8d02e7f0 sp 0x7fff8d02e7e8
READ of size 8 at 0x7f3aa79d9270 thread T0
    #0 0x7f3aba7bee42 in ~RefPtr third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
    #1 0x7f3aba7beb1d in ~AssociatedURLLoader third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:302
    #2 0x7f3ac152bfcb in ~scoped_ptr ./base/memory/scoped_ptr.h:163
    #3 0x7f3ac152bc9d in ~PPB_URLLoader_Impl webkit/plugins/ppapi/ppb_url_loader_impl.cc:87
    #4 0x7f3aba6e70b8 in base::RefCounted<ppapi::Resource>::Release() const ./base/memory/ref_counted.h:92
    #5 0x7f3aaa6561ac in ?? ??:0
    #6 0x7f3a000000d1
0x7f3aa79d9270 is located 48 bytes inside of 56-byte region [0x7f3aa79d9240,0x7f3aa79d9278)
freed by thread T0 here:
    #0 0x7f3ac1c52e70 in operator delete(void*) ??:0
    #1 0x7f3ac152c107 in scoped_ptr<WebKit::WebURLLoader>::reset(WebKit::WebURLLoader*) ./base/memory/scoped_ptr.h:186
    #2 0x7f3aba6e8b2d in ppapi::ResourceTracker::DidDeleteInstance(int) ppapi/shared_impl/resource_tracker.cc:144
    #3 0x7f3abe0ac3e6 in webkit::ppapi::HostGlobals::InstanceDeleted(int) webkit/plugins/ppapi/host_globals.cc:242
    #4 0x7f3abe0bd11e in ~PluginInstance webkit/plugins/ppapi/ppapi_plugin_instance.cc:653
    #5 0x7f3abe0bcabd in ~PluginInstance webkit/plugins/ppapi/ppapi_plugin_instance.cc:628
    #6 0x7f3ac15264bf in base::RefCounted<webkit::ppapi::PluginInstance>::Release() const ./base/memory/ref_counted.h:92
    #7 0x7f3aba767eb2 in ~WebPluginContainerImpl third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:661
    #8 0x7f3aba767bdd in ~WebPluginContainerImpl third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:648
    #9 0x7f3abd216048 in WTF::RefCounted<WebCore::Widget>::deref() third_party/WebKit/Source/WTF/wtf/RefCounted.h:202
    #10 0x7f3aba8f0c88 in ~WidgetHierarchyUpdatesSuspensionScope third_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41
    #11 0x7f3aba8ec0de in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node*, WTF::Vector<WTF::RefPtr<WebCore::Node>, 11ul>&, int&) third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:92
    #12 0x7f3aba8eb561 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, bool) third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:570
    #13 0x7f3aba9ed5ff in WebCore::Node::appendChild(WTF::PassRefPtr<WebCore::Node>, int&, bool) third_party/WebKit/Source/WebCore/dom/Node.cpp:630
    #14 0x7f3abc0724d7 in WebCore::V8Node::appendChildCallback(v8::Arguments const&) third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:120
previously allocated by thread T0 here:
    #0 0x7f3ac1c52cf0 in operator new(unsigned long) ??:0
    #1 0x7f3aba72bb7c in WebKit::WebFrameImpl::createAssociatedURLLoader(WebKit::WebURLLoaderOptions const&) third_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:1120
    #2 0x7f3ac152d7b5 in webkit::ppapi::PPB_URLLoader_Impl::Open(ppapi::URLRequestInfoData const&, int, scoped_refptr<ppapi::TrackedCallback>) webkit/plugins/ppapi/ppb_url_loader_impl.cc:175
    #3 0x7f3ac152c554 in webkit::ppapi::PPB_URLLoader_Impl::Open(int, scoped_refptr<ppapi::TrackedCallback>) webkit/plugins/ppapi/ppb_url_loader_impl.cc:109
    #4 0x7f3ac0f7088d in ppapi::thunk::(anonymous namespace)::Open(int, int, PP_CompletionCallback) ppapi/thunk/ppb_url_loader_thunk.cc:38
    #5 0x7f3aaa656709 in ?? ??:0


### ch...@gmail.com (2012-11-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-05)

Chamal, can you please file a new bug

### ch...@gmail.com (2012-11-05)

Reported https://crbug.com/chromium/159429.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2014-07-16)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/139814?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/136840]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062094)*
