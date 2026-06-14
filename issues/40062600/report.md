# Heap-use-after-free in WebCore::CachedResource::didAddClient

| Field | Value |
|-------|-------|
| **Issue ID** | [40062600](https://issues.chromium.org/issues/40062600) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2012-08-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-use-after-free happens when validating cached resources.

**VERSION**  

Version 22.0.1225.0 (149762), Ubuntu 10.10

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==2039== ERROR: AddressSanitizer heap-use-after-free on address 0x7fd69c24f8e0 at pc 0x7fd6ab64de7c bp 0x7fff70faa470 sp 0x7fff70faa468  

READ of size 8 at 0x7fd69c24f8e0 thread T0  

#0 0x7fd6ab64de7c in WebCore::CachedResource::didAddClient(WebCore::CachedResourceClient\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:393  

#1 0x7fd6ab645f77 in WebCore::CachedCSSStyleSheet::didAddClient(WebCore::CachedResourceClient\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedCSSStyleSheet.cpp:65  

#2 0x7fd6ab64f407 in WebCore::CachedResource::switchClientsToRevalidatedResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:627  

#3 0x7fd6ab663320 in WebCore::MemoryCache::revalidationSucceeded(WebCore::CachedResource\*, WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/MemoryCache.cpp:139  

#4 0x7fd6ab6324fd in WebCore::SubresourceLoader::didReceiveResponse(WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:179  

#5 0x7fd6ac7868fb in webkit\_glue::WebURLLoaderImpl::Context::OnReceivedResponse(webkit\_glue::ResourceResponseInfo const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:561  

#6 0x7fd6aa2a3075 in content::ResourceDispatcher::OnReceivedResponse(int, content::ResourceResponseHead const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:355  

#7 0x7fd6aa2a5bf2 in bool ResourceMsg\_ReceivedResponse::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, content::ResourceResponseHead const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, content::ResourceResponseHead const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:133  

#8 0x7fd6aa2a29b5 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:537  

#9 0x7fd6aa2a1ea7 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:310  

#10 0x7fd6aa198a6e in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:223  

#11 0x7fd6a9425253 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:257  

#12 0x7fd6a942bd38 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:899  

#13 0x7fd6a9322de3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:461  

#14 0x7fd6a932357d in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:472  

#15 0x7fd6a9323892 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:648  

#16 0x7fd6a932f908 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#17 0x7fd6a93225dc in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:420  

#18 0x7fd6a9359893 in base::RunLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/run\_loop.cc:46  

#19 0x7fd6a93212d7 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:300  

#20 0x7fd6ad635954 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:220  

#21 0x7fd6a92069fb in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:331  

#22 0x7fd6a92074a3 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:384  

#23 0x7fd6a92081e0 in content::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:634  

#24 0x7fd6a920616f in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#25 0x7fd6a7e59ea7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#26 0x7fd6a7e59e0b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#27 0x7fd6a0de3d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7fd69c24f8e0 is located 96 bytes inside of 440-byte region [0x7fd69c24f880,0x7fd69c24fa38)  

freed by thread T0 here:  

#0 0x7fd6ae7d3592 in \_\_interceptor\_free ??:0  

#1 0x7fd6aad59da2 in WebCore::HTMLLinkElement::setCSSStyleSheet(WTF::String const&, WebCore::KURL const&, WTF::String const&, WebCore::CachedCSSStyleSheet const\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLLinkElement.cpp:336  

#2 0x7fd6ab645f44 in ~RefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:56  

#3 0x7fd6ab64f407 in WebCore::CachedResource::switchClientsToRevalidatedResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:627  

#4 0x7fd6ab663320 in WebCore::MemoryCache::revalidationSucceeded(WebCore::CachedResource\*, WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/MemoryCache.cpp:139  

#5 0x7fd6ab6324fd in WebCore::SubresourceLoader::didReceiveResponse(WebCore::ResourceResponse const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:179  

#6 0x7fd6ac7868fb in webkit\_glue::WebURLLoaderImpl::Context::OnReceivedResponse(webkit\_glue::ResourceResponseInfo const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:561  

#7 0x7fd6aa2a3075 in content::ResourceDispatcher::OnReceivedResponse(int, content::ResourceResponseHead const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:355  

#8 0x7fd6aa2a5bf2 in bool ResourceMsg\_ReceivedResponse::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, content::ResourceResponseHead const&)>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(int, content::ResourceResponseHead const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:133  

#9 0x7fd6aa2a29b5 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:537  

#10 0x7fd6aa2a1ea7 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:310  

#11 0x7fd6aa198a6e in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:223  

#12 0x7fd6a9425253 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:257  

#13 0x7fd6a942bd38 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context\* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::\*)(IPC::Message const&)>, IPC::ChannelProxy::Context\* const&, IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:899  

#14 0x7fd6a9322de3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:461  

#15 0x7fd6a932357d in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:472  

#16 0x7fd6a9323892 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:648  

#17 0x7fd6a932f908 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#18 0x7fd6a93225dc in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:420  

#19 0x7fd6a9359893 in base::RunLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/run\_loop.cc:46  

#20 0x7fd6a93212d7 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:300  

#21 0x7fd6ad635954 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:220  

#22 0x7fd6a92069fb in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:331  

#23 0x7fd6a92074a3 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:384  

#24 0x7fd6a92081e0 in content::ContentMainRunnerImpl::Run() /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:634  

#25 0x7fd6a920616f in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#26 0x7fd6a7e59ea7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#27 0x7fd6a7e59e0b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#28 0x7fd6a0de3d8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

previously allocated by thread T0 here:  

#0 0x7fd6ae7d3652 in \_\_interceptor\_malloc ??:0  

#1 0x7fd6aaa235a9 in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:268  

#2 0x7fd6aad57414 in WebCore::HTMLLinkElement::create(WebCore::QualifiedName const&, WebCore::Document\*, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLLinkElement.cpp:78  

#3 0x7fd6ac1b9daa in WebCore::linkConstructor(WebCore::QualifiedName const&, WebCore::Document\*, WebCore::HTMLFormElement\*, bool) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webkit/HTMLElementFactory.cpp:391  

#4 0x7fd6ac1b69f6 in WebCore::HTMLElementFactory::createHTMLElement(WebCore::QualifiedName const&, WebCore::Document\*, WebCore::HTMLFormElement\*, bool) /media/Chromium/chromium/depot\_tools/src/out/Release/obj/gen/webkit/HTMLElementFactory.cpp:780  

#5 0x7fd6aaebf0ca in WebCore::HTMLConstructionSite::createHTMLElement(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:412  

#6 0x7fd6aaebff77 in WebCore::HTMLConstructionSite::insertSelfClosingHTMLElement(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:316  

#7 0x7fd6aae4a52f in WebCore::HTMLTreeBuilder::processStartTagForInHead(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:2582  

#8 0x7fd6aae492e2 in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:749  

#9 0x7fd6aae46b5b in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1453  

#10 0x7fd6aae44b02 in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken(WebCore::AtomicHTMLToken\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:473  

#11 0x7fd6aae4494d in WTF::RefPtr[WebCore::AtomicHTMLToken](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/RefPtr.h:64  

#12 0x7fd6aae23565 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:254  

#13 0x7fd6aae247ca in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:363  

#14 0x7fd6adfce42e in WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter\*, char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/DecodedDataDocumentParser.cpp:50  

#15 0x7fd6ab5c7d87 in WebCore::DocumentLoader::commitData(char const\*, unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:356  

#16 0x7fd6aa85dc7a in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader\*, char const\*, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1124  

#17 0x7fd6ab5c7ecb in void WTF::derefIfNotNull[WebCore::DocumentLoader](javascript:void(0);)(WebCore::DocumentLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:52  

#18 0x7fd6ab62bcb2 in WebCore::ResourceLoader::didReceiveData(char const\*, int, long long, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:276  

#19 0x7fd6ab615ddc in void WTF::derefIfNotNull[WebCore::MainResourceLoader](javascript:void(0);)(WebCore::MainResourceLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:52  

#20 0x7fd6ab62ca44 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle\*, char const\*, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:431  

#21 0x7fd6aa2a45de in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:388  

#22 0x7fd6aa2a5fd6 in bool ResourceMsg\_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const\*, content::ResourceDispatcher\*, content::ResourceDispatcher\*, void (content::ResourceDispatcher::\*)(IPC::Message const&, int, base::FileDescriptor, int, int)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:158  

#23 0x7fd6aa2a2ade in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:541  

#24 0x7fd6aa2a1ea7 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:310  

==2039== ABORTING  

Stats: 10M malloced (12M for red zones) by 23170 calls  

Stats: 0M realloced by 247 calls  

Stats: 8M freed by 13529 calls  

Stats: 0M really freed by 0 calls  

Stats: 56M (14345 full pages) mmaped in 14 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:128; 17:32; 18:16; 19:8;  

mallocs by size class: 8:18115; 9:1729; 10:2626; 11:280; 12:72; 13:73; 14:112; 15:34; 16:114; 17:9; 18:3; 19:3;  

frees by size class: 8:9469; 9:1154; 10:2434; 11:133; 12:38; 13:54; 14:99; 15:27; 16:108; 17:7; 18:3; 19:3;  

rfrees by size class:  

Stats: malloc large: 15 small slow: 168  

Shadow byte and word:  

0x1ffad3849f1c: fd  

0x1ffad3849f18: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffad3849ef8: fa fa fa fa fa fa fa fa  

0x1ffad3849f00: fa fa fa fa fa fa fa fa  

0x1ffad3849f08: fa fa fa fa fa fa fa fa  

0x1ffad3849f10: fd fd fd fd fd fd fd fd  

=>0x1ffad3849f18: fd fd fd fd fd fd fd fd  

0x1ffad3849f20: fd fd fd fd fd fd fd fd  

0x1ffad3849f28: fd fd fd fd fd fd fd fd  

0x1ffad3849f30: fd fd fd fd fd fd fd fd  

0x1ffad3849f38: fd fd fd fd fd fd fd fd

## Attachments

- [04-08-uaf.zip](attachments/04-08-uaf.zip) (application/zip; charset=binary, 395 B)

## Timeline

### in...@chromium.org (2012-08-04)

It does not reproduce on trunk LKGR. Ax330d, can you please try with trunk and see if it reproduces for you.

I think it might have regressed in http://trac.webkit.org/changeset/124032 ? Vseivik@, can you please help to triage.

### ax...@gmail.com (2012-08-04)

It works for me on version 22.0.1227.0 (150032) with Ubuntu, but on Windows canary 22.0.1226.0 does not.

### ax...@gmail.com (2012-08-06)

Checked also on Version 22.0.1227.0 (150041) - crashes too, no extra flags are required, test-case should be run from web-server, won't crash when launched from file.

### vs...@chromium.org (2012-08-06)

Can you try with http://commondatastorage.googleapis.com/chromium-browser-continuous/index.html?path=Win/148913/
The place where it fails was introduced in trac.webkit.org/changeset/123848 and chromium revision r148913 is between this change and mine.

### ax...@gmail.com (2012-08-06)

@vsevik, it doesn't crash (seems that on Windows at all).

### vs...@chromium.org (2012-08-07)

I was able to reproduce it on ubuntu. I bisected it and it was indeed caused by http:// trac.webkit.org/changeset/123848.
Nate, could you please have a look since you were reviewing the original patch. 
I was not able to add change author to this issue.

### ja...@chromium.org (2012-08-08)

FYI, I'm not going to be able to look at this until next week. Hopefully that's soon enough.

Regardless, I can't imagine this is a P0.

### [Deleted User] (2012-08-09)

Filed upstream as:
https://bugs.webkit.org/show_bug.cgi?id=93632

Cluster fuzz URL:
https://cluster-fuzz.appspot.com/testcase?key=91668439

### [Deleted User] (2012-08-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-09)

This never reproduced for me locally or clusterfuzz. that is why, i am also not tracking this for code yellow. did it reproduce for you Cris ? i think we should drop the severity and secimpacts for this.

### vs...@chromium.org (2012-08-09)

I was able to reproduce it locally on Ubuntu consistently. 
the attached file must be served from the 
Web server for that as I understood.

### in...@chromium.org (2012-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-10)

I was going off of what vsevik said. I'll give it a shot on Linux.

### in...@chromium.org (2012-08-10)

i was confusing this with the other event bug. this didnt reproduce on ClusterFuzz, but does reproduce locally. so cced the regree upstream and added code yellow tags.

### in...@chromium.org (2012-08-10)

http://trac.webkit.org/changeset/125292

### ke...@google.com (2012-08-14)

Does this need to be merged still?

### sc...@gmail.com (2012-08-25)

M22: http://trac.webkit.org/changeset/126670

### sc...@gmail.com (2012-09-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

Thank you Arthur, $1000 for this regression catch.

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/140656?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062600)*
