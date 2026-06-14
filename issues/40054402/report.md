# Heap-use-after-free in WebCore::CSSCrossfadeValue::~CSSCrossfadeValue

| Field | Value |
|-------|-------|
| **Issue ID** | [40054402](https://issues.chromium.org/issues/40054402) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2012-03-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free can be triggered when using CSS function cross-fade() during page reload.

**VERSION**  

Version 19.0.1050.0 (123195) - Developer Build on Ubuntu 10.10  

17.0.963.56 m, Win7, x64

**REPRODUCTION CASE**  

In attachment.  

Note: it makes no sense which image is loaded, it just must be present. Also location.reload() is used only in purpose to automate test-case.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==2973== ERROR: AddressSanitizer heap-use-after-free on address 0x7fd99b49f080 at pc 0x4d569a0 bp 0x7fff86e81d40 sp 0x7fff86e81d38  

READ of size 8 at 0x7fd99b49f080 thread T0  

#0 0x4d569a0 in WebCore::CSSCrossfadeValue::~CSSCrossfadeValue() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSCrossfadeValue.cpp:80  

#1 0x46ed591 in WebCore::CSSValue::destroy() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSValue.cpp:205  

#2 0x4741aa3 in WTF::VectorDestructor<true, WebCore::CSSProperty>::destruct(WebCore::CSSProperty\*, WebCore::CSSProperty\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57  

#3 0x4674d3d in WTF::RefCounted[WebCore::StylePropertySet](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#4 0x465a932 in WebCore::CSSRule::destroy() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSRule.cpp:86  

#5 0x46e8293 in WTF::VectorDestructor<true, WTF::RefPtr[WebCore::CSSRule](javascript:void(0);) >::destruct(WTF::RefPtr[WebCore::CSSRule](javascript:void(0);)\*, WTF::RefPtr[WebCore::CSSRule](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57  

#6 0x46e7fbe in WTF::RefCounted[WebCore::StyleSheet](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#7 0x475736f in WTF::VectorDestructor<true, WTF::RefPtr[WebCore::StyleSheet](javascript:void(0);) >::destruct(WTF::RefPtr[WebCore::StyleSheet](javascript:void(0);)\*, WTF::RefPtr[WebCore::StyleSheet](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57  

#8 0x3d7ba38 in WTF::RefCounted[WebCore::StyleSheetList](javascript:void(0);)::operator delete(void\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:178  

#9 0x3f33562 in ~HTMLDocument /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceClient.h:35  

#10 0x2c6b589 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot\_tools/src/v8/src/runtime-profiler.h:50  

0x7fd99b49f080 is located 0 bytes inside of 1112-byte region [0x7fd99b49f080,0x7fd99b49f4d8)  

freed by thread T0 here:  

#0 0x8013722 in free ??:0  

#1 0x4b1befa in WebCore::CachedResource::unregisterHandle(WebCore::CachedResourceHandleBase\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:617  

#2 0x4af3551 in ~CachedResourceHandle /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceHandle.h:35  

#3 0x620173d in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:659  

#4 0x36c337a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#5 0x36c45ab in void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks>(ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /media/Chromium/chromium/depot\_tools/src/./base/tuple.h:566  

#6 0x36c0afc in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#7 0x36be9d0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

#8 0x35c121f in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/child\_thread.cc:171  

#9 0x3753853 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/ipc/ipc\_channel\_proxy.cc:268  

#10 0x1e98086 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot\_tools/src/./base/callback.h:272  

#11 0x1e988e8 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#12 0x1e99bd9 in MessageLoop::DoWork() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:660  

#13 0x1ea4027 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:28  

#14 0x1e96c4e in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#15 0x1e94e3f in ~AutoRunState /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:745  

#16 0x6dca60c in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#17 0x1dedc23 in RunZygote /media/Chromium/chromium/depot\_tools/src/content/app/content\_main\_runner.cc:234  

#18 0x1dec1da in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:35  

#19 0x5575a7 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#20 0x5574fb in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#21 0x7fd9a089fd8e in ?? ??:0  

previously allocated by thread T0 here:  

#0 0x80137e2 in malloc ??:0  

#1 0x38e1d7b in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x4b256b8 in WebCore::CachedResource::operator new(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.h:57  

#3 0x4b253b0 in WebCore::CachedResourceLoader::revalidateResource(WebCore::CachedResource\*, WebCore::ResourceLoadPriority, WebCore::ResourceLoaderOptions const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:458  

#4 0x4b21886 in WebCore::CachedResourceLoader::requestResource(WebCore::CachedResource::Type, WebCore::ResourceRequest&, WTF::String const&, WebCore::ResourceLoaderOptions const&, WebCore::ResourceLoadPriority, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:431  

#5 0x4b2075c in WebCore::CachedResourceLoader::requestImage(WebCore::ResourceRequest&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:160  

#6 0x45a63ec in WebCore::CSSImageValue::cachedImage(WebCore::CachedResourceLoader\*, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSImageValue.cpp:90  

#7 0x45a6003 in WebCore::CSSImageValue::cachedImage(WebCore::CachedResourceLoader\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSImageValue.cpp:79  

#8 0x4d57b80 in WTF::RefPtr[WebCore::CSSValue](javascript:void(0);)::get() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSCrossfadeValue.cpp:59  

#9 0x46d2ee8 in PassRefPtr /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:60  

#10 0x46aaf1b in WTF::RefPtr[WebCore::StyleImage](javascript:void(0);)::operator=(WTF::PassRefPtr[WebCore::StyleImage](javascript:void(0);) const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:141  

#11 0x46926ab in WebCore::CSSStyleSelector::applyMatchedProperties(WebCore::CSSStyleSelector::MatchResult const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:2747  

#12 0x467eb62 in WebCore::CSSStyleSelector::styleForElement(WebCore::Element\*, WebCore::RenderStyle\*, bool, bool, WebCore::RenderRegion\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:1557  

#13 0x3dee899 in WebCore::Element::styleForRenderer() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1021  

#14 0x3e4eb07 in WTF::RefPtr[WebCore::RenderStyle](javascript:void(0);)::operator=(WTF::PassRefPtr[WebCore::RenderStyle](javascript:void(0);) const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:141  

#15 0x3e2ad86 in ~NodeRendererFactory /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/NodeRenderingContext.h:112  

#16 0x3decdef in WebCore::Node::getFlag(WebCore::Node::NodeFlags) const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:697  

#17 0x3f70833 in WebCore::Node::renderer() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Node.h:478  

#18 0x41b7838 in WebCore::executeTask(WebCore::HTMLConstructionSiteTask&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:101  

#19 0x41b72a8 in WebCore::HTMLConstructionSite::executeQueuedTasks() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:139  

#20 0x410701b in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:459  

#21 0x40b8e30 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:263  

#22 0x40ba9de in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:372  

#23 0x78d4849 in ~Deque /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/Deque.h:370  

==2973== ABORTING  

Stats: 56M malloced (46M for red zones) by 97035 calls  

Stats: 3M realloced by 3770 calls  

Stats: 53M freed by 86486 calls  

Stats: 0M really freed by 0 calls  

Stats: 128M (32790 full pages) mmaped in 32 calls  

mmaps by size class: 8:81915; 9:16382; 10:8190; 11:2047; 12:1024; 13:2048; 14:256; 15:384; 16:64; 17:64; 18:16; 19:8; 20:8; 22:6;  

mallocs by size class: 8:75686; 9:11763; 10:5278; 11:1462; 12:543; 13:1732; 14:190; 15:277; 16:26; 17:46; 18:16; 19:4; 20:6; 22:6;  

frees by size class: 8:66363; 9:11191; 10:5020; 11:1207; 12:467; 13:1710; 14:175; 15:270; 16:19; 17:32; 18:16; 19:4; 20:6; 22:6;  

rfrees by size class:  

Stats: malloc large: 78 small slow: 503  

Shadow byte and word:  

0x1ffb33693e10: fd  

0x1ffb33693e10: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffb33693df0: fa fa fa fa fa fa fa fa  

0x1ffb33693df8: fa fa fa fa fa fa fa fa  

0x1ffb33693e00: fa fa fa fa fa fa fa fa  

0x1ffb33693e08: fa fa fa fa fa fa fa fa  

=>0x1ffb33693e10: fd fd fd fd fd fd fd fd  

0x1ffb33693e18: fd fd fd fd fd fd fd fd  

0x1ffb33693e20: fd fd fd fd fd fd fd fd  

0x1ffb33693e28: fd fd fd fd fd fd fd fd  

0x1ffb33693e30: fd fd fd fd fd fd fd fd

## Attachments

- [tc-02-03-2012-uaf.zip](attachments/tc-02-03-2012-uaf.zip) (application/zip; charset=binary, 481 B)

## Timeline

### in...@chromium.org (2012-03-02)

Is this the right repro ? I cannot reproduce this on win and neither on linux with asan. Can you please try fixing the repro to make it more reliable.

### ax...@gmail.com (2012-03-02)

Strange - just checked, works fine. You should wait when page is reloaded second time, then crash should happen. Anyway, I will take a look.

### in...@chromium.org (2012-03-02)

do you have chromium trunk build ? will be great to check it if reproduces there. r123195 is kind of old.

### ax...@gmail.com (2012-03-02)

Here is a bit better repro:

<img id="d"/>
<script>
    i = document.getElementById('d');
    i.style.setProperty('background-image', '-webkit-cross-fade(url(x.png), url(x.png), 1%)');
    setTimeout('document.open();location.reload();', 1);
</script>

Unfortunately I will be able to update only tomorrow, have no such possibility atm.

### ts...@chromium.org (2012-03-02)

 Poking around the code it looks like the pattern is to use a CachedResourceHandle<CachedImage> instead of the raw pointers:

    CachedImage* m_cachedFromImage;
    CachedImage* m_cachedToImage;

in CSSCrossFadeValue.h to keep the image valid.


### in...@chromium.org (2012-03-02)

Still not able to reproduce on ClusterFuzz -https://cluster-fuzz.appspot.com/testcase?key=24353063

Tom, were you able to reproduce this ? Mind taking a look.

### ax...@gmail.com (2012-03-02)

I have updated to 19.0.1059.0 (124629) on Linux, checked as well version 19.0.1058.0 canary on Win7 x64 - still works ok. And updated testcase:

<img style="background-image:-webkit-cross-fade(url(x.png), url(x.png), 1%)"/>
<script>
setTimeout('location.reload()', 100);
</script>

New ASan stack trace:
=================================================================
==11277== ERROR: AddressSanitizer heap-use-after-free on address 0x7fbe2c7370a0 at pc 0x7fbe3ce0d61a bp 0x7fff3a79c370 sp 0x7fff3a79c368
READ of size 8 at 0x7fbe2c7370a0 thread T0
    #0 0x7fbe3ce0d61a in WTF::HashMap<WebCore::CachedResourceClient*, WTF::OwnPtr<WebCore::CachedResource::CachedResourceCallback>, WTF::PtrHash<WebCore::CachedResourceClient*>, WTF::HashTraits<WebCore::CachedResourceClient*>, WTF::HashTraits<WTF::OwnPtr<WebCore::CachedResource::CachedResourceCallback> > >::find(WebCore::CachedResourceClient* const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/HashTable.h:812
    #1 0x7fbe3ce0ce54 in WTF::PassOwnPtr<WebCore::CachedResource::CachedResourceCallback>::leakPtr() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassOwnPtr.h:90
    #2 0x7fbe3d061a9e in WebCore::CSSCrossfadeValue::~CSSCrossfadeValue() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSCrossfadeValue.cpp:81
    #3 0x7fbe3c9dd841 in WebCore::CSSValue::destroy() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSValue.cpp:205
    #4 0x7fbe3ca31d73 in WTF::VectorDestructor<true, WebCore::CSSProperty>::destruct(WebCore::CSSProperty*, WebCore::CSSProperty*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:57
    #5 0x7fbe3c0bdd73 in WTF::RefCounted<WebCore::StylePropertySet>::operator delete(void*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:185
    #6 0x7fbe3fc1ffd7 in ~StyledElement /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/StyledElement.cpp:60
    #7 0x7fbe3c22f87b in WebCore::HTMLImageElement::~HTMLImageElement() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/HTMLImageElement.cpp:66
    #8 0x7fbe3c018a54 in void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:51
    #9 0x7fbe3c03c319 in WTF::OwnPtr<WebCore::DocumentMarkerController>::operator->() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:64
    #10 0x7fbe3aed44f9 in v8::internal::RuntimeProfiler::IsEnabled() /media/Chromium/chromium/depot_tools/src/v8/src/runtime-profiler.h:50
0x7fbe2c7370a0 is located 32 bytes inside of 1136-byte region [0x7fbe2c737080,0x7fbe2c7374f0)
freed by thread T0 here:
    #0 0x7fbe40361542 in free ??:0
    #1 0x7fbe3ce0f575 in WebCore::CachedResource::unregisterHandle(WebCore::CachedResourceHandleBase*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:648
    #2 0x7fbe3cde5ee1 in ~CachedResourceHandle /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResourceHandle.h:35
    #3 0x7fbe3e4f700d in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot_tools/src/webkit/glue/weburlloader_impl.cc:662
    #4 0x7fbe3b96bb6a in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot_tools/src/content/common/resource_dispatcher.cc:489
    #5 0x7fbe3b96cd8b in void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), int, net::URLRequestStatus, std::basic_string<char, std::char_traits<char>, std::allocator<char> >, base::TimeTicks>(ResourceDispatcher*, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::TimeTicks const&), Tuple4<int, net::URLRequestStatus, std::basic_string<char, std::char_traits<char>, std::allocator<char> >, base::TimeTicks> const&) /media/Chromium/chromium/depot_tools/src/./base/tuple.h:566
    #6 0x7fbe3b96931c in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/common/resource_dispatcher.cc:559
    #7 0x7fbe3b9671f0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/common/resource_dispatcher.cc:326
    #8 0x7fbe3b8652af in ChildThread::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/content/common/child_thread.cc:172
    #9 0x7fbe3ba2b1f3 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot_tools/src/ipc/ipc_channel_proxy.cc:268
    #10 0x7fbe3a0fc7b6 in base::Callback<void ()()>::Run() const /media/Chromium/chromium/depot_tools/src/./base/callback.h:272
    #11 0x7fbe3a0fd018 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:470
    #12 0x7fbe3a0fe309 in MessageLoop::DoWork() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:660
    #13 0x7fbe3a1087d7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /media/Chromium/chromium/depot_tools/src/base/message_pump_default.cc:28
    #14 0x7fbe3a0fb37e in MessageLoop::RunInternal() /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:418
    #15 0x7fbe3a0f956f in ~AutoRunState /media/Chromium/chromium/depot_tools/src/base/message_loop.cc:745
    #16 0x7fbe3f0c9eac in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot_tools/src/content/renderer/renderer_main.cc:241
    #17 0x7fbe3a052703 in RunZygote /media/Chromium/chromium/depot_tools/src/content/app/content_main_runner.cc:234
    #18 0x7fbe3a050cba in content::ContentMain(int, char const**, content::ContentMainDelegate*) /media/Chromium/chromium/depot_tools/src/content/app/content_main.cc:35
    #19 0x7fbe3878fa47 in ChromeMain /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_main.cc:32
    #20 0x7fbe3878f99b in main /media/Chromium/chromium/depot_tools/src/chrome/app/chrome_exe_main_gtk.cc:18
    #21 0x7fbe31bb7d8e in __libc_start_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258
previously allocated by thread T0 here:
    #0 0x7fbe40361602 in malloc ??:0
    #1 0x7fbe3bb9d83b in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268
    #2 0x7fbe3ce19ff8 in WebCore::CachedResource::operator new(unsigned long) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResource.h:58
    #3 0x7fbe3ce19cf0 in WebCore::CachedResourceLoader::revalidateResource(WebCore::CachedResource*, WebCore::ResourceLoadPriority, WebCore::ResourceLoaderOptions const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:472
    #4 0x7fbe3ce15f36 in WebCore::CachedResourceLoader::requestResource(WebCore::CachedResource::Type, WebCore::ResourceRequest&, WTF::String const&, WebCore::ResourceLoaderOptions const&, WebCore::ResourceLoadPriority, bool) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:445
    #5 0x7fbe3ce14dfc in WebCore::CachedResourceLoader::requestImage(WebCore::ResourceRequest&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:165
    #6 0x7fbe3c8a53ec in WebCore::CSSImageValue::cachedImage(WebCore::CachedResourceLoader*, WTF::String const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSImageValue.cpp:90
    #7 0x7fbe3c8a5003 in WebCore::CSSImageValue::cachedImage(WebCore::CachedResourceLoader*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSImageValue.cpp:79
    #8 0x7fbe3d062ec0 in WTF::RefPtr<WebCore::CSSValue>::get() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSCrossfadeValue.cpp:59
    #9 0x7fbe3c9c6308 in PassRefPtr /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:60
    #10 0x7fbe3c9a159b in WTF::RefPtr<WebCore::StyleImage>::operator=(WTF::PassRefPtr<WebCore::StyleImage> const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:141
    #11 0x7fbe3c98ad7b in WebCore::CSSStyleSelector::applyMatchedProperties(WebCore::CSSStyleSelector::MatchResult const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:2755
    #12 0x7fbe3c976e26 in WebCore::CSSStyleSelector::styleForElement(WebCore::Element*, WebCore::RenderStyle*, bool, bool, WebCore::RenderRegion*) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/css/CSSStyleSelector.cpp:1574
    #13 0x7fbe3c0ad649 in WebCore::Element::styleForRenderer() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Element.cpp:1018
    #14 0x7fbe3c10f60e in WTF::RefPtr<WebCore::RenderStyle>::operator=(WTF::PassRefPtr<WebCore::RenderStyle> const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:141
    #15 0x7fbe3c0ea5c6 in ~NodeRendererFactory /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/NodeRenderingContext.h:120
    #16 0x7fbe3c0ac022 in WebCore::Node::getFlag(WebCore::Node::NodeFlags) const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Node.h:682
    #17 0x7fbe3c231d03 in WebCore::Node::renderer() const /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/dom/Node.h:471
    #18 0x7fbe3c47f068 in WebCore::executeTask(WebCore::HTMLConstructionSiteTask&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:101
    #19 0x7fbe3c47ead8 in WebCore::HTMLConstructionSite::executeQueuedTasks() /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:139
    #20 0x7fbe3c3cfc9b in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:459
    #21 0x7fbe3c381b40 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:263
    #22 0x7fbe3c3836ee in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) /media/Chromium/chromium/depot_tools/src/third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:372
==11277== ABORTING
Stats: 50M malloced (43M for red zones) by 92590 calls
Stats: 3M realloced by 3981 calls
Stats: 47M freed by 81268 calls
Stats: 0M really freed by 0 calls
Stats: 120M (30740 full pages) mmaped in 30 calls
  mmaps   by size class: 8:81915; 9:16382; 10:8190; 11:2047; 12:1024; 13:2048; 14:256; 15:256; 16:64; 17:64; 18:16; 19:8; 20:8; 22:5;
  mallocs by size class: 8:72117; 9:10848; 10:5234; 11:1508; 12:498; 13:1938; 14:194; 15:157; 16:26; 17:40; 18:16; 19:4; 20:5; 22:5;
  frees   by size class: 8:62043; 9:10271; 10:4952; 11:1262; 12:421; 13:1915; 14:179; 15:150; 16:19; 17:26; 18:16; 19:4; 20:5; 22:5;
  rfrees  by size class:
Stats: malloc large: 70 small slow: 476
Shadow byte and word:
  0x1ff7c58e6e14: fd
  0x1ff7c58e6e10: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff7c58e6df0: fa fa fa fa fa fa fa fa
  0x1ff7c58e6df8: fa fa fa fa fa fa fa fa
  0x1ff7c58e6e00: fa fa fa fa fa fa fa fa
  0x1ff7c58e6e08: fa fa fa fa fa fa fa fa
=>0x1ff7c58e6e10: fd fd fd fd fd fd fd fd
  0x1ff7c58e6e18: fd fd fd fd fd fd fd fd
  0x1ff7c58e6e20: fd fd fd fd fd fd fd fd
  0x1ff7c58e6e28: fd fd fd fd fd fd fd fd
  0x1ff7c58e6e30: fd fd fd fd fd fd fd fd


### ts...@chromium.org (2012-03-02)

Tom wonders if you need an actual x.png to load to see the exploit.

### ax...@gmail.com (2012-03-02)

Yes, x.png is needed, without that it won't crash. You still have no luck with repro?

### in...@chromium.org (2012-03-02)

yeah i have been using x.png. even with this new repro, it does no crash on win, linux with asan.

### ax...@gmail.com (2012-03-02)

That's really strange. I have tested Chrome with mentioned versions on Linux (in VirtualBox), on Windows (works on real hardware), also cleaned cache. I shall try on other computer then.

### ts...@chromium.org (2012-03-02)

Tom also wonders if x.png is coming from a webserver so that the timing may be different than when it would come from a file.

### ax...@gmail.com (2012-03-02)

Ah right, I was using web-server to test repro, and image was located on the server. Right now loaded testcase from the file - it doesn't work, though when loading from server, crash happens. 
FYI, tested also on another computer - 17.0.963.56, Ubuntu 10.04 x64, works there.

### ax...@gmail.com (2012-03-02)

So, the final testcase that works also from file:

<img style="background-image:-webkit-cross-fade(url(http://www.google.lv/favicon.ico), url(http://www.google.lv/favicon.ico), 1%)"/>
<script>
setTimeout('location.reload()', 1000);
</script>

Second url() can be empty, but I've used it here to improve reliability (to affect timing). And instead of 'img', another tag is also possible - e.g. div'.


### in...@chromium.org (2012-03-02)

https://bugs.webkit.org/show_bug.cgi?id=80186

trying to reproduce on CF to see which releases it impacts.

### in...@chromium.org (2012-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-03-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

Thanks, Arthur. This bug feels like a good catch.
Didn't even know we had a CSS cross fade object :)
$1000

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

### in...@chromium.org (2012-03-09)

http://trac.webkit.org/changeset/110326

### sc...@gmail.com (2012-03-12)

M18: http://trac.webkit.org/changeset/110454

### sc...@gmail.com (2012-03-20)

M17: http://trac.webkit.org/changeset/111421

### sc...@gmail.com (2012-03-21)

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

This issue was migrated from crbug.com/chromium/116461?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054402)*
