# Heap-use-after-free in WebCore::FrameLoader::checkCompleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40076998](https://issues.chromium.org/issues/40076998) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2013-02-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Attached test case crashes with use after free in WebCore::FrameLoader::checkCompleted().

**VERSION**  

Chrome Version: [27.0.1417.0 (183117)] + [trunk]  

[24.0.1312.70] + [stable]  

[25.0.1364.84] + [beta]  

[26.0.1410.5] + [dev]  

I got asan output from trunk build. Even though this test case crashes on stable, beta and dev I was unable to verify wether they crash due a use after free or the same reason that trunk build crashes.

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

1. Download parent.html, test.html and out.ogv and host in a web server.
2. Open chrome and open parent.html.
3. Web page will display an alert box. Click ok or press escape.  
   
   Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: Address sanitizer output

==18881== ERROR: AddressSanitizer: heap-use-after-free on address 0x60580000b4f0 at pc 0x7f57438f70d2 bp 0x7fffb1e17a70 sp 0x7fffb1e17a68  

READ of size 8 at 0x60580000b4f0 thread T0 (chrome)  

#0 0x7f57438f70d1 in WebCore::FrameLoader::checkCompleted() out/Release/../../third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:777  

#1 0x7f5743965df5 in WebCore::CachedResourceLoader::loadDone(WebCore::CachedResource\*) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:748  

#2 0x7f5743932b56 in WebCore::SubresourceLoader::releaseResources() out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:322  

#3 0x7f5743932598 in WebCore::SubresourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:280  

#4 0x7f57462a9ed8 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../webkit/glue/weburlloader\_impl.cc:679  

#5 0x7f57443bec92 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../content/common/resource\_dispatcher.cc:489  

#6 0x7f57443c055e in bool ResourceMsg\_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) out/Release/../../content/common/resource\_messages.h:255  

#7 0x7f57443bbfcc in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:582  

#8 0x7f57443bb3d0 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:281  

#9 0x7f57442c9f00 in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child\_thread.cc:243  

#10 0x7f5741641874 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc\_channel\_proxy.cc:261  

#11 0x7f5741648708 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) out/Release/../../base/bind\_internal.h:899  

#12 0x7f5742073bc4 in MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:476  

#13 0x7f57420743bb in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:488  

#14 0x7f57420745e1 in MessageLoop::DoWork() out/Release/../../base/message\_loop.cc:671  

#15 0x7f57420808ec in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) out/Release/../../base/message\_pump\_default.cc:29  

#16 0x7f5742073317 in MessageLoop::RunInternal() out/Release/../../base/message\_loop.cc:433  

#17 0x7f57420ac4c9 in base::RunLoop::Run() out/Release/../../base/run\_loop.cc:45  

#18 0x7f5742072081 in MessageLoop::Run() out/Release/../../base/message\_loop.cc:313  

#19 0x7f5744d61c02 in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer\_main.cc:226  

#20 0x7f5744cc7ad3 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:402  

#21 0x7f5744cc83d3 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:458  

#22 0x7f5744cc909a in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content\_main\_runner.cc:754  

#23 0x7f5744cc720b in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main.cc:35  

#24 0x7f5740581f4a in ChromeMain out/Release/../../chrome/app/chrome\_main.cc:32  

#25 0x7f5740581e9a in main out/Release/../../chrome/app/chrome\_exe\_main\_gtk.cc:31  

#26 0x7f5738d0c76c in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226  

#27 0x7f5740581dc4 in \_start ??:0  

0x60580000b4f0 is located 112 bytes inside of 2744-byte region [0x60580000b480,0x60580000bf38)  

freed by thread T0 (chrome) here:  

#0 0x7f5740576942 in free ??:0  

#1 0x7f57439f956c in void WTF::derefIfNotNull[WebCore::Frame](javascript:void(0);)(WebCore::Frame\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53  

#2 0x7f57439f924d in ~FrameView out/Release/../../third\_party/WebKit/Source/WebCore/page/FrameView.cpp:229  

#3 0x7f57440cca10 in void WTF::derefIfNotNull[WebCore::FrameView](javascript:void(0);)(WebCore::FrameView\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53  

#4 0x7f57440ca53c in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:56  

#5 0x7f5744046aa4 in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/Node.cpp:2324  

#6 0x7f5743f91574 in WebCore::Document::setReadyState(WebCore::Document::ReadyState) out/Release/../../third\_party/WebKit/Source/WebCore/dom/Document.cpp:1196  

#7 0x7f57438f6fdc in WebCore::FrameLoader::checkCompleted() out/Release/../../third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:775  

#8 0x7f5743965df5 in WebCore::CachedResourceLoader::loadDone(WebCore::CachedResource\*) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:748  

#9 0x7f5743932b56 in WebCore::SubresourceLoader::releaseResources() out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:322  

#10 0x7f5743932598 in WebCore::SubresourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:280  

#11 0x7f57462a9ed8 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../webkit/glue/weburlloader\_impl.cc:679  

#12 0x7f57443bec92 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../content/common/resource\_dispatcher.cc:489  

#13 0x7f57443c055e in bool ResourceMsg\_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) out/Release/../../content/common/resource\_messages.h:255  

#14 0x7f57443bbfcc in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:582  

#15 0x7f57443bb3d0 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:281  

#16 0x7f57442c9f00 in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child\_thread.cc:243  

#17 0x7f5741641874 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc\_channel\_proxy.cc:261  

#18 0x7f5741648708 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) out/Release/../../base/bind\_internal.h:899  

#19 0x7f5742073bc4 in MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:476  

#20 0x7f57420743bb in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:488  

#21 0x7f57420745e1 in MessageLoop::DoWork() out/Release/../../base/message\_loop.cc:671  

#22 0x7f57420808ec in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) out/Release/../../base/message\_pump\_default.cc:29  

#23 0x7f5742073317 in MessageLoop::RunInternal() out/Release/../../base/message\_loop.cc:433  

#24 0x7f57420ac4c9 in base::RunLoop::Run() out/Release/../../base/run\_loop.cc:45  

#25 0x7f5742072081 in MessageLoop::Run() out/Release/../../base/message\_loop.cc:313  

#26 0x7f5744d61c02 in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer\_main.cc:226  

#27 0x7f5744cc7ad3 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:402  

#28 0x7f5744cc83d3 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:458  

#29 0x7f5744cc909a in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content\_main\_runner.cc:754  

previously allocated by thread T0 (chrome) here:  

#0 0x7f5740576a22 in malloc ??:0  

#1 0x7f5746332a18 in WTF::fastMalloc(unsigned long) out/Release/../../third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:285  

#2 0x7f57439ecc3a in WebCore::Frame::create(WebCore::Page\*, WebCore::HTMLFrameOwnerElement\*, WebCore::FrameLoaderClient\*) out/Release/../../third\_party/WebKit/Source/WebCore/page/Frame.cpp:202  

#3 0x7f5741b3f971 in WebKit::WebFrameImpl::createChildFrame(WebCore::FrameLoadRequest const&, WebCore::HTMLFrameOwnerElement\*) out/Release/../../third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2211  

#4 0x7f5741bd62c4 in WebKit::FrameLoaderClientImpl::createFrame(WebCore::KURL const&, WTF::String const&, WebCore::HTMLFrameOwnerElement\*, WTF::String const&, bool, int, int) out/Release/../../third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1473  

#5 0x7f574392ff20 in WebCore::SubframeLoader::loadSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::String const&, WTF::String const&) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:367  

#6 0x7f574392dddf in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:341  

#7 0x7f574392db0e in WebCore::SubframeLoader::requestFrame(WebCore::HTMLFrameOwnerElement\*, WTF::String const&, WTF::AtomicString const&, bool, bool) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:87  

#8 0x7f5746c8c73f in WebCore::HTMLFrameElementBase::openURL(bool, bool) out/Release/../../third\_party/WebKit/Source/WebCore/html/HTMLFrameElementBase.cpp:88  

#9 0x7f5743f77df3 in WebCore::ChildNodeInsertionNotifier::notify(WebCore::Node\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:231  

#10 0x7f5743f7694e in WebCore::ContainerNode::parserAppendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:737  

#11 0x7f57423f57c1 in WebCore::executeTask(WebCore::HTMLConstructionSiteTask&) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:91  

#12 0x7f57423f55d2 in WebCore::HTMLConstructionSite::executeQueuedTasks() out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:137  

#13 0x7f5742369994 in WebCore::HTMLDocumentParser::constructTreeFromHTMLToken(WebCore::HTMLToken&) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:480  

#14 0x7f5742366cd7 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:437  

#15 0x7f574236aa5b in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) out/Release/../../third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:625  

#16 0x7f5743f869e1 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:60  

#17 0x7f57438eb23f in WebCore::DocumentWriter::end() out/Release/../../third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:240  

#18 0x7f57438d2ad6 in WebCore::DocumentLoader::finishedLoading() out/Release/../../third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:295  

#19 0x7f574391a0f5 in WebCore::MainResourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:563  

#20 0x7f57439549d7 in WebCore::CachedResource::checkNotify() out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:378  

#21 0x7f57439508de in WebCore::CachedRawResource::data(WTF::PassRefPtr[WebCore::ResourceBuffer](javascript:void(0);), bool) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:72  

#22 0x7f5743932543 in WebCore::SubresourceLoader::didFinishLoading(double) out/Release/../../third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:278  

#23 0x7f57462a9ed8 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../webkit/glue/weburlloader\_impl.cc:679  

#24 0x7f57443bec92 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../content/common/resource\_dispatcher.cc:489  

#25 0x7f57443c055e in bool ResourceMsg\_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, int, bool, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) out/Release/../../content/common/resource\_messages.h:255  

#26 0x7f57443bbfcc in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:582  

#27 0x7f57443bb3d0 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource\_dispatcher.cc:281  

#28 0x7f57442c9f00 in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child\_thread.cc:243  

#29 0x7f5741641874 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc\_channel\_proxy.cc:261

## Attachments

- [out.ogv](attachments/out.ogv) (application/ogg; charset=binary, 288.3 KB)
- [test.html](attachments/test.html) (text/html; charset=us-ascii, 437 B)
- [parent.html](attachments/parent.html) (text/plain; charset=us-ascii, 131 B)
- [out.ogv](attachments/out_53231443.ogv) (application/ogg; charset=binary, 288.3 KB)
- [test.html](attachments/test_53231444.html) (text/html; charset=us-ascii, 218 B)
- [parent.html](attachments/parent_53231445.html) (text/plain; charset=us-ascii, 131 B)
- [out.ogv](attachments/out_53231522.ogv) (application/ogg; charset=binary, 288.3 KB)
- [parent.html](attachments/parent_53231523.html) (text/plain; charset=us-ascii, 131 B)
- [test.html](attachments/test_53231524.html) (text/html; charset=us-ascii, 495 B)

## Timeline

### ch...@gmail.com (2013-02-19)

Reproduction steps for stable, beta and dev
===========================================
1. Download parent.html, test.html and out.ogv and copy them to a folder in web server.
2. Open chrome.
3. Open the web server folder which contains parent.html.
   ex. http://127.0.0.1/video_uaf
4. Now click on parent.html to open it on chrome
5. Web page will display an alert box. Click ok or press escape.
Chrome will display sad tab.

Step 3 is not necessary on trunk build. (Additional Note: My trunk build is built with ASAN.)



### ch...@gmail.com (2013-02-19)

Attaching a simplified test case which works only in trunk build.

Reproduction steps
------------------
1. Download parent.html, test.html and out.ogv and copy them to a folder in web server.
2. Open chrome.
3. Open parent.html
Chrome will display sad tab.

### sc...@gmail.com (2013-02-19)

Nice Chamal.
Out of interest, how did you find this one?

### ch...@gmail.com (2013-02-19)

@scarybeasts 
I reported a similar bug (139814) which happens because of pdf and ready state event last year. That bug happened because it was possible to fire a ready state event when loader was canceled when pdf element was removed.

So I decided this month to investigate similar areas when ready state is event if fired when loader is cancelled. This bug accidentally occurred to me while i was investigating similar scenario with video element.


### ts...@chromium.org (2013-02-19)

Reproduced on chrome 27.0.1414, linux 64 ASAN.




### js...@chromium.org (2013-02-19)

@japhet - Mind taking a look?

### ts...@chromium.org (2013-02-19)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=110237

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### ch...@gmail.com (2013-02-20)

This issue does not reproduce for me on a release build without asan.

Other thing is when I build with asan i build with linux_use_tcmalloc=0 flag as instructed in http://www.chromium.org/developers/testing/addresssanitizer.

Does this issue has anything to do with asan or tcmalloc?

### js...@chromium.org (2013-02-20)

@japhet - Hate to press, but if this doesn't get fixed in the next week it rolls into the Pwnium build. And then we all feel sad.

### ja...@chromium.org (2013-02-20)

My patch is approved and I plan on landing today, barring commit-queue brokenness. :)

### in...@chromium.org (2013-02-20)

http://trac.webkit.org/changeset/143514

Chris, very low risk fix, lets merge this to m25 in next batch :)

### sc...@gmail.com (2013-02-20)

M26: http://trac.webkit.org/changeset/143521
M25: http://trac.webkit.org/changeset/143522

### ch...@gmail.com (2013-02-21)

Attached similar test case which reproduces after the fix. 

Steps
-----
1. Download parent.html, test.html and out.ogv and copy them to a folder in web server.
2. Open chrome with --js-flags="--expose-gc"
3. Open parent.html
4. Chrome will display an alert box. Press escape.
5. Chrome will display another alert box. Press escape.
Tab will crash.

Address sanitizer output
-----------------------
==19512== ERROR: AddressSanitizer: heap-use-after-free on address 0x600c000d2b08 at pc 0x7f591f287dcd bp 0x7fffbec831a0 sp 0x7fffbec83198
READ of size 4 at 0x600c000d2b08 thread T0 (chrome)
    #0 0x7f591f287dcc in WTF::RefCountedBase::derefBase() out/Release/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:148
    #1 0x7f591fa392fd in WTF::RefCounted<WebCore::PODArena>::deref() out/Release/../../third_party/WebKit/Source/WTF/wtf/RefCounted.h:201
    #2 0x7f591fa11070 in ~HTMLMediaElement out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:357
    #3 0x7f591fa10cdd in ~HTMLMediaElement out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:329
    #4 0x7f5921189550 in void WTF::derefIfNotNull<WebCore::EventTarget>(WebCore::EventTarget*) out/Release/../../third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53
    #5 0x7f59217bbbea in WebCore::Event::setTarget(WTF::PassRefPtr<WebCore::EventTarget>) out/Release/../../third_party/WebKit/Source/WebCore/dom/Event.cpp:183
    #6 0x7f59217c2b4d in WebCore::GenericEventQueue::enqueueEvent(WTF::PassRefPtr<WebCore::Event>) out/Release/../../third_party/WebKit/Source/WebCore/dom/GenericEventQueue.cpp:57
    #7 0x7f591fa145bd in WebCore::HTMLMediaElement::scheduleEvent(WTF::AtomicString const&) out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:655
    #8 0x7f591fa273d4 in WebCore::HTMLMediaElement::userCancelledLoad() out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:3862
    #9 0x7f591fa27619 in WebCore::HTMLMediaElement::stop() out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:3932
    #10 0x7f592182b3e1 in WebCore::ScriptExecutionContext::stopActiveDOMObjects() out/Release/../../third_party/WebKit/Source/WebCore/dom/ScriptExecutionContext.cpp:239
    #11 0x7f59210a946a in WebCore::FrameLoader::frameDetached() out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2379
    #12 0x7f591fadfada in WebCore::HTMLFrameOwnerElement::disconnectContentFrame() out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLFrameOwnerElement.cpp:84
    #13 0x7f5921728a10 in WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners() out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:316
    #14 0x7f59217230f8 in WebCore::willRemoveChild(WebCore::Node*) out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:455
    #15 0x7f5921722bba in WebCore::ContainerNode::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:520
    #16 0x7f59217e8ad1 in WebCore::Node::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/WebCore/dom/Node.cpp:568
    #17 0x7f5920d56b40 in WebCore::V8Node::removeChildCallbackCustom(v8::Arguments const&) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:101
    #18 0x7f5923141ca3 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) out/Release/../../v8/src/builtins.cc:1335
    #19 0x2e474e0062ed in
0x600c000d2b08 is located 8 bytes inside of 64-byte region [0x600c000d2b00,0x600c000d2b40)
freed by thread T0 (chrome) here:
    #0 0x7f591dcf64e2 in free ??:0
    #1 0x7f591fa11070 in ~HTMLMediaElement out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:357
    #2 0x7f59244afd0d in WebCore::HTMLVideoElement::~HTMLVideoElement() out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.h:36
    #3 0x7f59231c5751 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate*, v8::internal::GlobalHandles*) out/Release/../../v8/src/global-handles.cc:274
    #4 0x7f59231c51d4 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector, v8::internal::GCTracer*) out/Release/../../v8/src/global-handles.cc:656
    #5 0x7f59231db01c in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) out/Release/../../v8/src/heap.cc:989
    #6 0x7f59231da749 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) out/Release/../../v8/src/heap.cc:655
    #7 0x7f592319321d in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const*) out/Release/../../v8/src/heap-inl.h:461
    #8 0x7f59231da36e in v8::internal::Heap::CollectAllGarbage(int, char const*) out/Release/../../v8/src/heap.cc:565
    #9 0x7f5923193145 in v8::internal::GCExtension::GC(v8::Arguments const&) out/Release/../../v8/src/extensions/gc-extension.cc:46
    #10 0x7f5923141ca3 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) out/Release/../../v8/src/builtins.cc:1335
    #11 0x2e474e0062ed in
    #12 0x2e474e059ce6 in
    #13 0x2e474e00b353 in
    #14 0x2e474e025bdd in
    #15 0x2e474e007176 in
    #16 0x7f592318cf51 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) out/Release/../../v8/src/execution.cc:118
    #17 0x7f592310bd02 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../v8/src/api.cc:3723
    #18 0x7f5920cea6d7 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:234
    #19 0x7f5920cea3f2 in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:187
    #20 0x7f59215533b1 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext*, v8::Handle<v8::Value>, WebCore::Event*) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8EventListener.cpp:95
    #21 0x7f592133f6a6 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext*, WebCore::Event*, v8::Handle<v8::Value>) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:143
    #22 0x7f592133f40a in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*) out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:103
    #23 0x7f59217c00ce in WebCore::EventTarget::fireEventListeners(WebCore::Event*, WebCore::EventTargetData*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:256
    #24 0x7f59217bfaad in WebCore::EventTarget::fireEventListeners(WebCore::Event*) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:203
    #25 0x7f592187fce3 in WebCore::WindowEventContext::handleLocalEvents(WebCore::Event*) out/Release/../../third_party/WebKit/Source/WebCore/dom/WindowEventContext.cpp:60
    #26 0x7f5921877b85 in WebCore::EventDispatcher::dispatchEventAtBubbling(WebCore::WindowEventContext&) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:190
    #27 0x7f592187741c in WebCore::EventDispatcher::dispatch() out/Release/../../third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:123
    #28 0x7f592187610b in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher*) const out/Release/../../third_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:54
    #29 0x7f592187627d in WebCore::EventDispatcher::dispatchEvent(WebCore::Node*, WTF::PassRefPtr<WebCore::EventDispatchMediator>) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:56
previously allocated by thread T0 (chrome) here:
    #0 0x7f591dcf65c2 in malloc ??:0
    #1 0x7f5923ae2ef8 in WTF::fastMalloc(unsigned long) out/Release/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:285
    #2 0x7f591fa39233 in WebCore::PODFreeListArena<WebCore::PODRedBlackTree<WebCore::PODInterval<double, WebCore::TextTrackCue*> >::Node>::create() out/Release/../../third_party/WebKit/Source/WebCore/platform/PODFreeListArena.h:40
    #3 0x7f591fa3875a in PODRedBlackTree out/Release/../../third_party/WebKit/Source/WebCore/platform/PODRedBlackTree.h:125
    #4 0x7f591fa3869d in PODIntervalTree out/Release/../../third_party/WebKit/Source/WebCore/platform/PODIntervalTree.h:89
    #5 0x7f591fa0fee2 in HTMLMediaElement out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:264
    #6 0x7f59244b0040 in HTMLVideoElement out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.cpp:50
    #7 0x7f59244aea63 in WebCore::HTMLVideoElement::create(WebCore::QualifiedName const&, WebCore::Document*, bool) out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.cpp:56
    #8 0x7f5922021c31 in WebCore::videoConstructor(WebCore::QualifiedName const&, WebCore::Document*, WebCore::HTMLFormElement*, bool) out/Release/gen/webkit/HTMLElementFactory.cpp:576
    #9 0x7f592201c632 in WebCore::HTMLElementFactory::createHTMLElement(WebCore::QualifiedName const&, WebCore::Document*, WebCore::HTMLFormElement*, bool) out/Release/gen/webkit/HTMLElementFactory.cpp:782
    #10 0x7f591fb838c2 in WebCore::HTMLConstructionSite::createHTMLElement(WebCore::AtomicHTMLToken*) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:538
    #11 0x7f591fb84307 in WebCore::HTMLConstructionSite::insertHTMLElement(WebCore::AtomicHTMLToken*) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:416
    #12 0x7f591fb3c5d3 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken*) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:947
    #13 0x7f591fb38db5 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken*) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1176
    #14 0x7f591fb36efe in WebCore::HTMLTreeBuilder::constructTree(WebCore::AtomicHTMLToken*) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:369
    #15 0x7f591faf47b4 in WebCore::HTMLDocumentParser::constructTreeFromHTMLToken(WebCore::HTMLToken&) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:482
    #16 0x7f591faf1af7 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:439
    #17 0x7f591faf587b in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:627
    #18 0x7f5921731161 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter*) out/Release/../../third_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:60
    #19 0x7f5921090aaf in WebCore::DocumentWriter::end() out/Release/../../third_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:240
    #20 0x7f5921078346 in WebCore::DocumentLoader::finishedLoading() out/Release/../../third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:295
    #21 0x7f59210bf9d5 in WebCore::MainResourceLoader::didFinishLoading(double) out/Release/../../third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:563
    #22 0x7f59210fa3b7 in WebCore::CachedResource::checkNotify() out/Release/../../third_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:378
    #23 0x7f59210f62be in WebCore::CachedRawResource::data(WTF::PassRefPtr<WebCore::ResourceBuffer>, bool) out/Release/../../third_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:72
    #24 0x7f59210d7e33 in WebCore::SubresourceLoader::didFinishLoading(double) out/Release/../../third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:278
    #25 0x7f5923a5a388 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../webkit/glue/weburlloader_impl.cc:713
    #26 0x7f5921b68a52 in content::ResourceDispatcher::OnRequestComplete(int, int, bool, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) out/Release/../../content/common/resource_dispatcher.cc:501
    #27 0x7f5921b6a47e in bool ResourceMsg_RequestComplete::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, int, bool, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(int, int, bool, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) out/Release/../../content/common/resource_messages.h:256
    #28 0x7f5921b65d8c in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:601
    #29 0x7f5921b65190 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:293


### in...@chromium.org (2013-02-21)

Chamal, please file a new bug for this last stacktrace, it looks like a new bug and unrelated to the fix.

### ch...@gmail.com (2013-02-22)

Reported 177620 for issue mentioned in https://crbug.com/chromium/176882#c15.

### ch...@gmail.com (2013-02-22)

I feel this issue might not affect stable, beta or dev. What actually reproduces in stable, beta and dev is new issue reported in 177620. That may be the reason why reproduction case attached in https://crbug.com/chromium/176882#c2 reproduces only in trunk build.

### sc...@gmail.com (2013-02-22)

@inferno: should this be unmerged?

Hopefully we can get to 177620 tomorrow :-/

### in...@chromium.org (2013-02-22)

ClusterFuzz is giving evidence that this did affect Stable m25. Two reports are coming. We should not unmerge this. The patch is generic and this is pretty clear that setReadyState can fire mutation event to destroy the frame.

Regarding the new 177620, we will definitely look into it next.

### in...@chromium.org (2013-02-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=166776838

Fuzzer: Inferno_twister

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6058000270f0
Crash State:
  - crash stack -
  WebCore::FrameLoader::checkCompleted
  WebCore::ThreadTimers::sharedTimerFiredInternal
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141366:141387

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94coqKh4BVXlao5Pmn1TJ2SqTBjqZBZC_96IoSv7O_baSVHdFRyLTKk3zbPGpSgXohzN-OM9VhavNxnlrTRK1PcS1yOieYf1nOJkUG6VKXmuQyVUsZAZkjrfEUPMZ1HhWrQA9cmno-mQHZtFZxbwGbqvQp8y-wfXqGyx_xGBrm2y2M8M68
<script>
if (window.testRunner) {
    testRunner.waitUntilDone();
}

function r()
{
    document.body.removeChild(document.getElementById("f"));
}
</script>
><iframe id=f src=resources/delete-frame-during-readystatechange-frame.html>

### in...@chromium.org (2013-02-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=166567528

Fuzzer: Inferno_twister

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6058000270f0
Crash State:
  - crash stack -
  WebCore::FrameLoader::checkCompleted
  WebCore::CachedResourceLoader::loadDone
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141366:141387

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97FrPITA9XHLETqRI1rv1RkqU-qoRaemq3kjyj8PYIuE2RHNvaAiXgkCKbLkGl9mddgpD0eVYTCNaK11Xlt3FSPudh02rwEOoccJ4RDcj4K-iiqwJ6p0-pTpF66515i2DDunfW2SIrRSTtaVxXMMqGXCusKotzb4pUR3Xwa2qLraayxuTk
<script>
if (window.testRunner) {
    testRunner.waitUntilDone();
}

function r()
{
    document.body.removeChild(document.getElementById("f"));
}
</script>
>>><iframe id=f src=resources/delete-frame-during-readystatechange-frame.html>

Additional requirements: Requires HTTP

### cl...@chromium.org (2013-02-24)

ClusterFuzz has detected this issue as fixed in range 183765:184307.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=166776838

Fuzzer: Inferno_twister

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6058000270f0
Crash State:
  - crash stack -
  WebCore::FrameLoader::checkCompleted
  WebCore::ThreadTimers::sharedTimerFiredInternal
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141366:141387
Fixed: https://cluster-fuzz.appspot.com/revisions?range=183765:184307

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94coqKh4BVXlao5Pmn1TJ2SqTBjqZBZC_96IoSv7O_baSVHdFRyLTKk3zbPGpSgXohzN-OM9VhavNxnlrTRK1PcS1yOieYf1nOJkUG6VKXmuQyVUsZAZkjrfEUPMZ1HhWrQA9cmno-mQHZtFZxbwGbqvQp8y-wfXqGyx_xGBrm2y2M8M68

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-02-24)

ClusterFuzz has detected this issue as fixed in range 183765:184307.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=166567528

Fuzzer: Inferno_twister

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6058000270f0
Crash State:
  - crash stack -
  WebCore::FrameLoader::checkCompleted
  WebCore::CachedResourceLoader::loadDone
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141366:141387
Fixed: https://cluster-fuzz.appspot.com/revisions?range=183765:184307

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97FrPITA9XHLETqRI1rv1RkqU-qoRaemq3kjyj8PYIuE2RHNvaAiXgkCKbLkGl9mddgpD0eVYTCNaK11Xlt3FSPudh02rwEOoccJ4RDcj4K-iiqwJ6p0-pTpF66515i2DDunfW2SIrRSTtaVxXMMqGXCusKotzb4pUR3Xwa2qLraayxuTk

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ch...@gmail.com (2013-03-01)

Is this issue eligible for reward?

### sc...@gmail.com (2013-03-01)

It seems plausible :) Added reward-topanel.

### sc...@gmail.com (2013-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-02)

Good find Chamal, $1000

### ch...@gmail.com (2013-03-02)

Thank you very much for the reward :)

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### tk...@chromium.org (2014-06-20)

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

This issue was migrated from crbug.com/chromium/176882?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076998)*
