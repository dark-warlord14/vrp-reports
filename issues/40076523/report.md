# Heap-use-after-free in WebCore::Frame::dispatchVisibilityStateChangeEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40076523](https://issues.chromium.org/issues/40076523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-10-28 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

This vulnerbility is in Frame.cpp->dispatchVisibilityStateChangeEvent method.

void Frame::dispatchVisibilityStateChangeEvent()  

{  

if (m\_doc)  

m\_doc->dispatchVisibilityStateChangeEvent();  

for (Frame\* child = tree()->firstChild(); child; child = child->tree()->nextSibling())  

child->dispatchVisibilityStateChangeEvent();  

}

It is possible to capture visibility change event from javascript and remove the first child frame which causes the use after free.

**VERSION**  

Chrome Version: [24.0.1309.0 (164506)] + [trunk build]

\*webkitvisibilitychange event is available in dev and stable releases. But this issue does NOT reproduce in stable or dev releases. But Frame.cpp->dispatchVisibilityStateChangeEvent method which I think is the cause of the issue is added to code long time back. So I really don't understand why this does not reproduce in stable or dev releases.

In case this bug happens because of code currently being developed, please ignore this issue.

Operating System: [Ubuntu 12.04, 64 bit]

**REPRODUCTION CASE**

1. Download and copy pagevisibility\_parent.html and pagevisibility.html to same folder.
2. Open pagevisibility\_parent.html on chrome.
3. Click on the "Click" button or open another tab.
4. Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [Address sanitizer output]

==4771== ERROR: AddressSanitizer heap-use-after-free on address 0x7f3cc7ffa098 at pc 0x7f3cfce84de5 bp 0x7fff63039940 sp 0x7fff63039938  

READ of size 8 at 0x7f3cc7ffa098 thread T0  

#0 0x7f3cfce84de4 in WebCore::FrameTree::firstChild() const third\_party/WebKit/Source/WTF/wtf/RefPtr.h:58  

#1 0x7f3cfce84db7 in WebCore::Frame::dispatchVisibilityStateChangeEvent() third\_party/WebKit/Source/WebCore/page/Frame.cpp:674  

#2 0x7f3cfae74d3d in WebKit::WebViewImpl::setVisibilityState(WebKit::WebPageVisibilityState, bool) third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:4176  

#3 0x7f3d005cd241 in content::RenderViewImpl::OnWasHidden() content/renderer/render\_view\_impl.cc:5673  

#4 0x7f3d005e398e in bool IPC::Message::Dispatch<content::RenderWidget, content::RenderWidget>(IPC::Message const\*, content::RenderWidget\*, content::RenderWidget\*, void (content::RenderWidget::\*)()) ./ipc/ipc\_message.h:156  

#5 0x7f3d00586d58 in content::RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render\_view\_impl.cc:1040  

#6 0x7f3cfa87dd40 in content::MessageRouter::RouteMessage(IPC::Message const&) content/common/message\_router.cc:49  

#7 0x7f3cfa87dbb3 in content::MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message\_router.cc:41  

#8 0x7f3cfa76b0dc in content::ChildThread::OnMessageReceived(IPC::Message const&) content/common/child\_thread.cc:275  

#9 0x7f3cfa70c0e2 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc\_channel\_proxy.cc:261  

#10 0x7f3cf9be3617 in base::Callback<void ()>::Run() const ./base/callback.h:391  

#11 0x7f3cf9be3bf1 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message\_loop.cc:482  

#12 0x7f3cf9be49ad in MessageLoop::DoWork() base/message\_loop.cc:661  

#13 0x7f3cf9bef336 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_pump\_default.cc:28  

#14 0x7f3cf9be23ca in MessageLoop::RunInternal() base/message\_loop.cc:427  

#15 0x7f3cf9c2a3b1 in base::RunLoop::Run() base/run\_loop.cc:45  

#16 0x7f3cf9be0886 in MessageLoop::Run() base/message\_loop.cc:307  

#17 0x7f3d0060ea4f in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:241  

#18 0x7f3cf9a6fb2a in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:402  

#19 0x7f3cf9a710f9 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:456  

#20 0x7f3cf9a7290f in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:741  

#21 0x7f3cf9a6f257 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) content/app/content\_main.cc:35  

#22 0x7f3cf89a2cb6 in ChromeMain chrome/app/chrome\_main.cc:32  

#23 0x7f3cf89a2c1a in main chrome/app/chrome\_exe\_main\_gtk.cc:31  

#24 0x7f3cf1af276c in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226  

0x7f3cc7ffa098 is located 88 bytes inside of 2704-byte region [0x7f3cc7ffa040,0x7f3cc7ffaad0)  

freed by thread T0 here:  

#0 0x7f3d02203e10 in \_\_interceptor\_free ??:0  

#1 0x7f3cfce90f2e in WTF::RefCounted[WebCore::Frame](javascript:void(0);)::operator delete(void\*) third\_party/WebKit/Source/WTF/wtf/RefCounted.h:197  

#2 0x7f3cfce9061d in ~FrameView third\_party/WebKit/Source/WebCore/page/FrameView.cpp:227  

#3 0x7f3cfb192321 in WTF::RefCounted[WebCore::Widget](javascript:void(0);)::deref() third\_party/WebKit/Source/WTF/wtf/RefCounted.h:202  

#4 0x7f3cfb188fb1 in WebCore::EventDispatcher::~EventDispatcher() third\_party/WebKit/Source/WebCore/dom/EventDispatcher.h:70  

#5 0x7f3cfb0c924d in WebCore::Node::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) third\_party/WebKit/Source/WebCore/dom/Node.cpp:2579  

#6 0x7f3cfafe850f in WebCore::Document::dispatchVisibilityStateChangeEvent() third\_party/WebKit/Source/WebCore/dom/Document.cpp:1650  

#7 0x7f3cfce84d76 in WebCore::Frame::dispatchVisibilityStateChangeEvent() third\_party/WebKit/Source/WebCore/page/Frame.cpp:672  

#8 0x7f3cfce84db7 in WebCore::Frame::dispatchVisibilityStateChangeEvent() third\_party/WebKit/Source/WebCore/page/Frame.cpp:674  

#9 0x7f3cfae74d3d in WebKit::WebViewImpl::setVisibilityState(WebKit::WebPageVisibilityState, bool) third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:4176  

#10 0x7f3d005cd241 in content::RenderViewImpl::OnWasHidden() content/renderer/render\_view\_impl.cc:5673  

#11 0x7f3d005e398e in bool IPC::Message::Dispatch<content::RenderWidget, content::RenderWidget>(IPC::Message const\*, content::RenderWidget\*, content::RenderWidget\*, void (content::RenderWidget::\*)()) ./ipc/ipc\_message.h:156  

#12 0x7f3d00586d58 in content::RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render\_view\_impl.cc:1040  

#13 0x7f3cfa87dd40 in content::MessageRouter::RouteMessage(IPC::Message const&) content/common/message\_router.cc:49  

#14 0x7f3cfa87dbb3 in content::MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message\_router.cc:41  

previously allocated by thread T0 here:  

#0 0x7f3d02203ed0 in \_\_interceptor\_malloc ??:0  

#1 0x7f3cfaf5ad08 in WTF::fastMalloc(unsigned long) third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:269  

#2 0x7f3cfce82012 in WTF::RefCounted[WebCore::Frame](javascript:void(0);)::operator new(unsigned long) third\_party/WebKit/Source/WTF/wtf/RefCounted.h:197  

#3 0x7f3cfae0ddb5 in WebKit::WebFrameImpl::createChildFrame(WebCore::FrameLoadRequest const&, WebCore::HTMLFrameOwnerElement\*) third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2233  

#4 0x7f3cfaed3dbc in WebKit::FrameLoaderClientImpl::createFrame(WebCore::KURL const&, WTF::String const&, WebCore::HTMLFrameOwnerElement\*, WTF::String const&, bool, int, int) third\_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1459  

#5 0x7f3cfcd7495f in WebCore::SubframeLoader::loadSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::String const&, WTF::String const&) third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:366  

#6 0x7f3cfcd6f692 in WebCore::SubframeLoader::loadOrRedirectSubframe(WebCore::HTMLFrameOwnerElement\*, WebCore::KURL const&, WTF::AtomicString const&, bool, bool) third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:337  

#7 0x7f3cfcd6f09d in WebCore::SubframeLoader::requestFrame(WebCore::HTMLFrameOwnerElement\*, WTF::String const&, WTF::AtomicString const&, bool, bool) third\_party/WebKit/Source/WebCore/loader/SubframeLoader.cpp:87  

#8 0x7f3d01853ae6 in WebCore::HTMLFrameElementBase::openURL(bool, bool) third\_party/WebKit/Source/WebCore/html/HTMLFrameElementBase.cpp:100

## Attachments

- [pagevisibility_parent.html](attachments/pagevisibility_parent.html) (text/plain; charset=us-ascii, 236 B)
- [pagevisibility.html](attachments/pagevisibility.html) (text/plain; charset=us-ascii, 159 B)
- [page-visibility-iframe-child-delete-test.html](attachments/page-visibility-iframe-child-delete-test.html) (text/html; charset=us-ascii, 1.3 KB)
- [page-visibility-iframe-child-delete-test-expected.txt](attachments/page-visibility-iframe-child-delete-test-expected.txt) (text/plain; charset=us-ascii, 5 B)

## Timeline

### in...@chromium.org (2012-10-29)

Very nice catch Chamal.

### in...@chromium.org (2012-10-29)

CF report coming - https://cluster-fuzz.appspot.com/testcase?key=132701773

### ch...@gmail.com (2012-10-29)

Inferno, Can you reproduce this on stable(Labels:SecImpacts-Stable SecImpacts-Beta)?
I cannot reproduce this on stable or dev release.

### in...@chromium.org (2012-10-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=132701773

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7c5dd8098
Crash State:
  - crash stack -
  WebCore::Frame::dispatchVisibilityStateChangeEvent
  WebCore::Frame::dispatchVisibilityStateChangeEvent
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114961:114982

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94mcBbz3xFAw5rlJsauaIQ4DduB83zzl6aTw-1fzCRL2Q1CV2GlmiVTyp7xsTMB5BKBY5ybL-yBtmLiHib0xdJY6MN2M_KDNt_yLEHoMo1_BZQUvlPm5WGmSMIlho2ki8uA2COukFXjDBHCqkNFiMRr7Kmy1uJdUYyqQUALMhd117OjzjI

Additional requirements: Requires Interaction Gestures

### ch...@gmail.com (2012-11-07)

Increasing the ref count of child frame in Frame.cpp->dispatchVisibilityStateChangeEvent method fixed the bug. If this fix is ok I'd like to submit a patch.

void Frame::dispatchVisibilityStateChangeEvent()
{
    if (m_doc)
        m_doc->dispatchVisibilityStateChangeEvent();
    //fix RefPtr<Frame> child
    for (RefPtr<Frame> child = tree()->firstChild(); child; child = child->tree()->nextSibling())
        child->dispatchVisibilityStateChangeEvent();
}

### in...@chromium.org (2012-11-12)

Chamal, please file an upstream security bug in webkit and submit a patch as per webkit guidelines [http://www.webkit.org/coding/contributing.html] with a test. [you can trigger the user interaction in layout tests using eventSender]

### ch...@gmail.com (2012-11-13)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=102053

### ch...@gmail.com (2012-11-13)

Fix and layout test is ready. But webkit-patch upload command fails for me with OSError: [Errno 2] No such file or directory error. I ll try to download webkit seperately and submit a patch tomorrow.

### ch...@gmail.com (2012-11-14)

I wrote this attached layout test. It reproduces in webkit which is in chrome.
But it does NOT reproduce in webkit taken from webkit trunk repository. So I think this bug does not exist in webkit trunk.

Inferno, Can a chrome developer please take over this issue from me, because I am unable to provide a fix for this issue :(.

### in...@chromium.org (2012-11-19)

Note: The regression range in these bugs starting with '114961:' is wrong. There was a ASAN string change which caused ClusterFuzz to not detect the end tag of an ASAN stack. I have fixed this on ClusterFuzz now and clicked redo on these testcases. The ClusterFuzz report will be updated with new regression range for these bugs.

### in...@chromium.org (2012-11-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-26)

http://trac.webkit.org/changeset/135740

### cl...@chromium.org (2012-11-28)

ClusterFuzz has detected this issue as fixed in range 169616:169821.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=132701773

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fe7c5dd8098
Crash State:
  - crash stack -
  WebCore::Frame::dispatchVisibilityStateChangeEvent
  WebCore::Frame::dispatchVisibilityStateChangeEvent
  - free stack -
  WebCore::FrameView::~FrameView
  WebCore::FrameView::~FrameView
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=169616:169821

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94mcBbz3xFAw5rlJsauaIQ4DduB83zzl6aTw-1fzCRL2Q1CV2GlmiVTyp7xsTMB5BKBY5ybL-yBtmLiHib0xdJY6MN2M_KDNt_yLEHoMo1_BZQUvlPm5WGmSMIlho2ki8uA2COukFXjDBHCqkNFiMRr7Kmy1uJdUYyqQUALMhd117OjzjI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-11-30)

M23: http://trac.webkit.org/changeset/136273
M24: http://trac.webkit.org/changeset/136274

### sc...@gmail.com (2012-12-04)

Thank you Chamal!
A $1500 reward.
$1000 for the bug and a $500 bonus for your assistance filing the WebKit bug, making a nice LayoutTest and suggesting the fix.

### ch...@gmail.com (2012-12-04)

Thank you very much for the reward :)

### sc...@gmail.com (2012-12-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-14)

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

This issue was migrated from crbug.com/chromium/158204?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076523)*
