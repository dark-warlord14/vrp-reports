# chrome_6dc70000!WebCore::EventHandler::updateSelectionForMouseDrag use after free

| Field | Value |
|-------|-------|
| **Issue ID** | [40084916](https://issues.chromium.org/issues/40084916) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-11-13 |
| **Bounty** | $500.00 |

## Description

test chrome 9.0.576.0 dev windows xp sp3

1,Press Ctrl+Shift+J open devtools
2,Type scan = 1; press enter
3,Type s then Use mouse drag at the end line and move mouse left and right
4, -> #3

video
http://picasaweb.google.com/lh/photo/BQzNlKGEAQKI5M-J8x0c-t9rm2lLix-o8COEQf4uDsI?feat=directlink

logout
====
(53c.97c): Access violation - code c0000005 (!!! second chance !!!)
eax=0528c8b8 ebx=024ef568 ecx=0528c874 edx=0042f4ec esi=6ed1fe38 edi=0042f43c
eip=00000000 esp=0042f434 ebp=0042f514 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
00000000 ??              ???
0:000> .exr -1
ExceptionAddress: 73c2c9f1
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 00000000
Attempt to execute non-executable address 00000000

## Timeline

### ku...@gmail.com (2010-11-13)

0:000> kp
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0042f430 6e17a561 0x0
0042f514 6e17a461 chrome_6dc70000!WebCore::EventHandler::updateSelectionForMouseDrag(class WebCore::Node * targetNode = 0x05a7dc00, class WebCore::IntPoint * localPoint = 0x0042f530)+0x70 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\page\eventhandler.cpp @ 613]
0042f53c 6e17bc8d chrome_6dc70000!WebCore::EventHandler::handleMouseDraggedEvent(class WebCore::MouseEventWithHitTestResults * event = 0x0042f580)+0xd4 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\page\eventhandler.cpp @ 543]
0042f608 6e17b8ba chrome_6dc70000!WebCore::EventHandler::handleMouseMoveEvent(class WebCore::PlatformMouseEvent * mouseEvent = 0x0042f6a0, class WebCore::HitTestResult * hoveredNode = 0x0042f628)+0x39b [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\page\eventhandler.cpp @ 1517]
0042f68c 6e45edf8 chrome_6dc70000!WebCore::EventHandler::mouseMoved(class WebCore::PlatformMouseEvent * event = 0x0528c8b8)+0x2c [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\page\eventhandler.cpp @ 1395]
0042f6d0 6e45fe82 chrome_6dc70000!WebKit::WebViewImpl::mouseMove(class WebKit::WebMouseEvent * event = 0x0528c8b8)+0x65 [c:\b\slave\chrome-official\build\src\third_party\webkit\webkit\chromium\src\webviewimpl.cpp @ 362]
0042f72c 6dda47a1 chrome_6dc70000!WebKit::WebViewImpl::handleInputEvent(class WebKit::WebInputEvent * inputEvent = 0x05890894)+0x15d [c:\b\slave\chrome-official\build\src\third_party\webkit\webkit\chromium\src\webviewimpl.cpp @ 1116]
0042f754 6dda438d chrome_6dc70000!RenderWidget::OnHandleInputEvent(class IPC::Message * message = 0x05a83580)+0x7a [c:\b\slave\chrome-official\build\src\chrome\renderer\render_widget.cc @ 351]
0042f77c 6dd6af09 chrome_6dc70000!RenderWidget::OnMessageReceived(class IPC::Message * msg = 0x05a83580)+0x140 [c:\b\slave\chrome-official\build\src\chrome\renderer\render_widget.cc @ 175]
0042f850 6e0b8293 chrome_6dc70000!RenderView::OnMessageReceived(class IPC::Message * message = 0x05a83580)+0xb75 [c:\b\slave\chrome-official\build\src\chrome\renderer\render_view.cc @ 893]
0042f864 6e0b8265 chrome_6dc70000!MessageRouter::RouteMessage(class IPC::Message * msg = 0x05a83580)+0x2a [c:\b\slave\chrome-official\build\src\chrome\common\message_router.cc @ 47]
0042f874 6e0a7d4f chrome_6dc70000!MessageRouter::OnMessageReceived(class IPC::Message * msg = 0x05a83580)+0x22 [c:\b\slave\chrome-official\build\src\chrome\common\message_router.cc @ 39]
0042f894 6dfd5ab8 chrome_6dc70000!ChildThread::OnMessageReceived(class IPC::Message * msg = 0x05a83580)+0x84 [c:\b\slave\chrome-official\build\src\chrome\common\child_thread.cc @ 165]
0042f8a0 6dd37246 chrome_6dc70000!RunnableMethod<browser_sync::SyncBackendHost::Core,void (void)+0x17 [c:\b\slave\chrome-official\build\src\base\task.h @ 330]
0042f8c0 6dd372cd chrome_6dc70000!MessageLoop::RunTask(class Task * task = 0x05a83570)+0x7d [c:\b\slave\chrome-official\build\src\base\message_loop.cc @ 419]
0042f8d0 6dd37467 chrome_6dc70000!MessageLoop::DeferOrRunPendingTask(struct MessageLoop::PendingTask * pending_task = 0x0528c8b8)+0x28 [c:\b\slave\chrome-official\build\src\base\message_loop.cc @ 430]

### ku...@gmail.com (2010-11-13)

0042f900 6dd4c8a4 chrome_6dc70000!MessageLoop::DoWork(void)+0x71 [c:\b\slave\chrome-official\build\src\base\message_loop.cc @ 534]
0042f92c 6dd36fec chrome_6dc70000!base::MessagePumpDefault::Run(class base::MessagePump::Delegate * delegate = 0x0042fa10)+0xbf [c:\b\slave\chrome-official\build\src\base\message_pump_default.cc @ 50]
0042f940 6dd36f6a chrome_6dc70000!MessageLoop::RunInternal(void)+0x38 [c:\b\slave\chrome-official\build\src\base\message_loop.cc @ 267]
0042f948 6dd36f18 chrome_6dc70000!MessageLoop::RunHandler(void)+0x17 [c:\b\slave\chrome-official\build\src\base\message_loop.cc @ 238]


### in...@chromium.org (2010-11-15)

Thanks kuzzcc, you are a Mouse Ninja. Clear use after free. Nice bug showing issue in the event handler. Note than devtools does not look to be needed and only some editing and mouse event firing is required.

renderer is free (vtable clearly messed up) by the point of VisiblePosition line. looks like function canMouseDragExtendSelect is dispatching an event which blows away the renderer. Fix seems simple and targetrenderer should be calculated after the function call. key is designing the layouttest with event sender.

line 603, eventhandler.cpp
    RenderObject* targetRenderer = targetNode->renderer();
    if (!targetRenderer)
        return;
        
    if (!canMouseDragExtendSelect(targetNode))
        return;

    VisiblePosition targetPosition(targetRenderer->positionForPoint(localPoint));

### ku...@gmail.com (2010-11-15)

Thank you for your compliment :)

### in...@chromium.org (2010-11-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-11-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-11-15)

Fixed in http://trac.webkit.org/changeset/72013. Needs to be merged to 552. This is medium severity since requires mouse drag behavior.

### in...@chromium.org (2010-11-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-11-15)

Merged to 552 in r72022.

### sc...@gmail.com (2010-11-18)

@kuzzcc: cool! This bug qualifies for a $500 Chromium Security Reward.

Note that we cannot promise to reward every, or even most, SecSeverity-Medium bugs. However, the panel found this bug interesting -- hence the reward in this particular case.

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

### ku...@gmail.com (2010-11-19)

:) Yes thanks for the reward.

### sc...@gmail.com (2010-12-20)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/63051?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084916)*
