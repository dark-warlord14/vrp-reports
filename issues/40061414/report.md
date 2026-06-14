# Security: Bad cast in WebCore::CalendarPickerElement::hostInput()

| Field | Value |
|-------|-------|
| **Issue ID** | [40061414](https://issues.chromium.org/issues/40061414) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2012-07-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome tab crashed due to heap buffer overflow when date input element is changed to text input element on onclick event.

Think it happens because of a cast error similar to <https://crbug.com/chromium/136145>, which happens with password generation. ASAN backtrace is also similar, except that this issue happens on CalendarPickerElement.cpp.

**VERSION**  

Chrome Version: [20.0.1132.57] + [stable]  

[22.0.1210.0 (146980)] + [dev]  

Operating System: [Ubuntu 12.04, 64 bit]

**REPRODUCTION CASE**

1. Download and host date.html.
2. Open date.html on chrome.
3. Click on the down arrow icon on date input field.  
   
   Tab will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Crash State:ASAN output

==5013== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fc0c408db08 at pc 0x7fc0ddde1857 bp 0x7fff323d4420 sp 0x7fff323d4418  

READ of size 1 at 0x7fc0c408db08 thread T0  

#0 0x7fc0ddde1857 in WebCore::CalendarPickerElement::defaultEventHandler(WebCore::Event\*) /third\_party/WebKit/Source/WebCore/html/shadow/CalendarPickerElement.cpp:92  

#1 0x7fc0dd6b4588 in WTF::PassRefPtr[WebCore::Event](javascript:void(0);)::operator->() const /third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:76  

#2 0x7fc0dd6bf852 in WebCore::MouseEventDispatchMediator::dispatchEvent(WebCore::EventDispatcher\*) const /third\_party/WebKit/Source/WebCore/dom/MouseEvent.cpp:207  

#3 0x7fc0dd6b0d82 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node\*, WTF::PassRefPtr[WebCore::EventDispatchMediator](javascript:void(0);)) /third\_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:128  

#4 0x7fc0dd5ff3d9 in WebCore::Node::dispatchMouseEvent(WebCore::PlatformMouseEvent const&, WTF::AtomicString const&, int, WebCore::Node\*) /third\_party/WebKit/Source/WebCore/dom/Node.cpp:2638  

#5 0x7fc0de9508bd in WebCore::EventHandler::updateMouseEventTargetNode(WebCore::Node\*, WebCore::PlatformMouseEvent const&, bool) /third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:2217  

#6 0x7fc0de94ccf2 in WTF::RefPtr[WebCore::Node](javascript:void(0);)::operator WebCore::Node\* WTF::RefPtr[WebCore::Node](javascript:void(0);)::\*() const /third\_party/WebKit/Source/WTF/wtf/RefPtr.h:70  

#7 0x7fc0de94ed11 in WebCore::EventHandler::handleMouseMoveEvent(WebCore::PlatformMouseEvent const&, WebCore::HitTestResult\*, bool) /third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:1820  

#8 0x7fc0de94d9e0 in WebCore::EventHandler::mouseMoved(WebCore::PlatformMouseEvent const&) /third\_party/WebKit/Source/WebCore/page/EventHandler.cpp:1692  

#9 0x7fc0dd4a0533 in WebKit::PageWidgetEventHandler::handleMouseMove(WebCore::Frame&, WebKit::WebMouseEvent const&) /third\_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:197  

#10 0x7fc0dd4a00c7 in WebKit::PageWidgetDelegate::handleInputEvent(WebCore::Page\*, WebKit::PageWidgetEventHandler&, WebKit::WebInputEvent const&) /third\_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:118  

#11 0x7fc0dd428b8e in WebKit::WebViewImpl::handleInputEvent(WebKit::WebInputEvent const&) /third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1805  

#12 0x7fc0e1443d8e in RenderWidget::OnHandleInputEvent(IPC::Message const&) /content/renderer/render\_widget.cc:569  

#13 0x7fc0e1440c86 in bool IPC::Message::Dispatch<RenderWidget, RenderWidget>(IPC::Message const\*, RenderWidget\*, RenderWidget\*, void (RenderWidget::\*)(IPC::Message const&)) /./ipc/ipc\_message.h:167  

#14 0x7fc0e13eae65 in RenderViewImpl::OnMessageReceived(IPC::Message const&) /content/renderer/render\_view\_impl.cc:967  

#15 0x7fc0dced02f5 in MessageRouter::RouteMessage(IPC::Message const&) /content/common/message\_router.cc:47  

#16 0x7fc0dced0160 in MessageRouter::OnMessageReceived(IPC::Message const&) /content/common/message\_router.cc:40  

#17 0x7fc0dcdd2167 in ChildThread::OnMessageReceived(IPC::Message const&) /content/common/child\_thread.cc:209  

#18 0x7fc0db9c0bf6 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /ipc/ipc\_channel\_proxy.cc:257  

#19 0x7fc0db88b8a1 in base::Callback<void ()>::Run() const /./base/callback.h:388  

#20 0x7fc0db88c04c in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /base/message\_loop.cc:467  

#21 0x7fc0db88d339 in MessageLoop::DoWork() /base/message\_loop.cc:643  

#22 0x7fc0db8976e7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /base/message\_pump\_default.cc:28  

#23 0x7fc0db88a4da in MessageLoop::RunInternal() /base/message\_loop.cc:415  

#24 0x7fc0db8d31e2 in base::RunLoop::AfterRun() /base/run\_loop.cc:84  

#25 0x7fc0db8889b7 in MessageLoop::Run() /base/message\_loop.cc:299  

#26 0x7fc0e146811e in RendererMain(content::MainFunctionParams const&) /content/renderer/renderer\_main.cc:270  

#27 0x7fc0db734224 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:330  

#28 0x7fc0db7354d0 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /content/app/content\_main\_runner.cc:383  

#29 0x7fc0db736bf0 in content::ContentMainRunnerImpl::Run() /content/app/content\_main\_runner.cc:630  

#30 0x7fc0db7337ca in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /content/app/content\_main.cc:35  

#31 0x7fc0da12c1c7 in ChromeMain /chrome/app/chrome\_main.cc:32  

#32 0x7fc0da12c12b in main /chrome/app/chrome\_exe\_main\_gtk.cc:18  

#33 0x7fc0d339d76d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

0x7fc0c408db08 is located 24 bytes to the right of 112-byte region [0x7fc0c408da80,0x7fc0c408daf0)  

allocated by thread T0 here:  

#0 0x7fc0e2a19362 in  

#1 0x7fc0ddde1082 in  

#2 0x7fc0ddd81266 in  

#3 0x7fc0ddb58f58 in  

#4 0x7fc0ddb5c86b in  

#5 0x7fc0dd667d03 in  

#6 0x7fc0dd5a3967 in  

#7 0x7fc0dddcc27b in  

#8 0x7fc0ddd0f42e in  

#9 0x7fc0ddd0093e in  

#10 0x7fc0ddcff92b in  

#11 0x7fc0ddcfcf2f in  

#12 0x7fc0ddcfce0b in  

#13 0x7fc0ddcaa5db in  

#14 0x7fc0ddcac03a in  

#15 0x7fc0e1f6f36c in  

#16 0x7fc0de7f977b in  

#17 0x7fc0de7e5dc1 in  

#18 0x7fc0de85d7f6 in  

#19 0x7fc0e0385567 in  

#20 0x7fc0dcee386b in  

#21 0x7fc0dcee489b in  

#22 0x7fc0dcee112d in  

==5013== ABORTING  

Stats: 56M malloced (66M for red zones) by 161233 calls  

Stats: 3M realloced by 2843 calls  

Stats: 54M freed by 150309 calls  

Stats: 0M really freed by 0 calls  

Stats: 152M (38934 full pages) mmaped in 38 calls  

mmaps by size class: 8:131064; 9:40955; 10:8190; 11:2047; 12:1024; 13:1536; 14:256; 15:128; 16:128; 17:384; 18:16; 19:8;  

mallocs by size class: 8:118284; 9:33477; 10:5823; 11:1298; 12:464; 13:1140; 14:198; 15:101; 16:65; 17:379; 18:1; 19:3;  

frees by size class: 8:108622; 9:32823; 10:5546; 11:1100; 12:388; 13:1115; 14:186; 15:93; 16:60; 17:372; 18:1; 19:3;  

rfrees by size class:  

Stats: malloc large: 383 small slow: 608  

Shadow byte and word:  

0x1ff818811b61: fa  

0x1ff818811b60: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1ff818811b40: fa fa fa fa fa fa fa fa  

0x1ff818811b48: fa fa fa fa fa fa fa fa  

0x1ff818811b50: 00 00 00 00 00 00 00 00  

0x1ff818811b58: 00 00 00 00 00 00 fb fb  

=>0x1ff818811b60: fa fa fa fa fa fa fa fa  

0x1ff818811b68: fa fa fa fa fa fa fa fa  

0x1ff818811b70: 00 fb fb fb fb fb fb fb  

0x1ff818811b78: fb fb fb fb fb fb fb fb  

0x1ff818811b80: fa fa fa fa fa fa fa fa

## Attachments

- [date.html](attachments/date.html) (text/plain; charset=us-ascii, 121 B)

## Timeline

### in...@chromium.org (2012-07-17)

gcasto@, can you please check if this is a dupe of 136145 ? Also, did you get a chance to look at 136145.

### gc...@chromium.org (2012-07-17)

I don't think that it's a dupe. The problematic code is identical, but it does seem to live in two different places. I also don't think that these bugs should be assigned to me, as I don't own this code and I'm not sure how to fix this. I'm going to assign this to tkent for now, and he can re-assign as necessary. I'm willing to help out, but this is not my area.

### ch...@gmail.com (2012-07-17)

Why is this issue SecSeverity-Medium?

### in...@chromium.org (2012-07-18)

Because this requires a user-initiated event. "3. Click on the down arrow icon on date input field."

### tk...@chromium.org (2012-07-18)

[Empty comment from Monorail migration]

### tk...@chromium.org (2012-07-18)

Fixed by http://trac.webkit.org/changeset/122918

This bug affects M20 and M21 branches.


### in...@chromium.org (2012-07-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-18)

[Empty comment from Monorail migration]

### tk...@chromium.org (2012-07-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-24)

merged to m21 in r123531

### sc...@gmail.com (2012-07-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

We've been going though some old bugs, and have rewarded $2,000 for this one!

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/137671?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061414)*
