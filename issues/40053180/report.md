# Heap-use-after-free in WebCore::EventTarget::dispatchEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40053180](https://issues.chromium.org/issues/40053180) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | pa...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-02-01 |
| **Bounty** | $500.00 |

## Description

stacktrace from recent webkit nightly.

webkit/Source/WebCore/page/EventHandler.cpp

bool EventHandler::updateDragAndDrop(const PlatformMouseEvent& event, Clipboard* clipboard)
{
    ...
1   Node* newTarget = targetNode(mev);
    if (newTarget && newTarget->isTextNode())
2       newTarget = newTarget->parentNode();
    ...

    if (m_dragTarget != newTarget) {
            ...
            if (dragState().m_dragSrc && dragState().shouldDispatchEvents()) {
3               dispatchDragSrcEvent(eventNames().dragEvent, event);
            }    
4           accept = dispatchDragEvent(eventNames().dragenterEvent, newTarget, event, clipboard);

1 - newTarget is the target of d&d operation
2 - we are dropping over a text node ("drag the kitty here..."), so newTarget is set to textnode's parent.
3 - "drag" event is dispatched to the kitty. we catch it with an "ondrag" handler. inside the handler, we delete newTarget node
4 - newTarget is stale. use after free.

newTarget must be a text node, because targetNode(mev) returns a "raw" pointer taken from a RefPtr node.

Program received signal EXC_BAD_ACCESS, Could not access memory.
Reason: 13 at address: 0x0000000000000000
0x0000000102c18541 in WebCore::EventTarget::dispatchEvent (this=0x1099aa110, event=@0x7fff5fbfd2b0, ec=@0x7fff5fbfd31c) at /Users/p/webkit/Source/WebCore/dom/EventTarget.cpp:165
165     if (!scriptExecutionContext())
(gdb) dpc
Dump of assembler code from 0x102c18541 to 0x102c18559:
0x0000000102c18541 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+161>:  call   rax
0x0000000102c18543 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+163>:  test   rax,rax
0x0000000102c18546 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+166>:  sete   al
0x0000000102c18549 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+169>:  test   al,al
0x0000000102c1854b <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+171>:  je     0x102c18556 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+182>
0x0000000102c1854d <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+173>:  mov    DWORD PTR [rbp-0x3c],0x0
0x0000000102c18554 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+180>:  jmp    0x102c1858a <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+234>
0x0000000102c18556 <_ZN7WebCore11EventTarget13dispatchEventEN3WTF10PassRefPtrINS_5EventEEERi+182>:  mov    rax,QWORD PTR [rbp-0x28]
End of assembler dump.
(gdb) i r
rax            0x1098a0008000000    74742601567174656 ;<- garbage from heap
rbx            0x0  0
rcx            0x11 17
rdx            0x7fff5fbfd31c   140734799794972
rsi            0x7fff5fbfd2b0   140734799794864
rdi            0x1099aa110  4456096016
rbp            0x7fff5fbfd200   0x7fff5fbfd200
rsp            0x7fff5fbfd1c0   0x7fff5fbfd1c0
r8             0x2d9    729
r9             0x7fff5fbfce10   140734799793680
r10            0x7fffffe00050   140737486258256
r11            0x75de   30174
r12            0x0  0
r13            0x0  0
r14            0x0  0
r15            0x72 114
rip            0x102c18541  0x102c18541 <WebCore::EventTarget::dispatchEvent(WTF::PassRefPtr<WebCore::Event>, int&)+161>
eflags         0x10206  66054
cs             0x27 39
ss             0x0  0
ds             0x0  0
es             0x0  0
fs             0x0  0
gs             0x0  0
(gdb) bt 
#0  0x0000000102c18541 in WebCore::EventTarget::dispatchEvent (this=0x1099aa110, event=@0x7fff5fbfd2b0, ec=@0x7fff5fbfd31c) at /Users/p/webkit/Source/WebCore/dom/EventTarget.cpp:165
#1  0x0000000102c004b1 in WebCore::EventHandler::dispatchDragEvent (this=0x100871900, eventType=@0x10086d8e8, dragTarget=0x1099aa110, event=@0x7fff5fbfd470, clipboard=0x1099c2af0) at /Users/p/webkit/Source/WebCore/page/EventHandler.cpp:1766
#2  0x0000000102c05a1d in WebCore::EventHandler::updateDragAndDrop (this=0x100871900, event=@0x7fff5fbfd470, clipboard=0x1099c2af0) at /Users/p/webkit/Source/WebCore/page/EventHandler.cpp:1852
#3  0x0000000102bc0ca6 in WebCore::DragController::tryDHTMLDrag (this=0x109921d00, dragData=0x7fff5fbfd6b0, operation=@0x7fff5fbfd5d0) at /Users/p/webkit/Source/WebCore/page/DragController.cpp:583
#4  0x0000000102bc0ea2 in WebCore::DragController::tryDocumentDrag (this=0x109921d00, dragData=0x7fff5fbfd6b0, actionMask=WebCore::DragDestinationActionAny, dragSession=@0x7fff5fbfd5d0) at /Users/p/webkit/Source/WebCore/page/DragController.cpp:304
#5  0x0000000102bc13c4 in WebCore::DragController::dragEnteredOrUpdated (this=0x109921d00, dragData=0x7fff5fbfd6b0) at /Users/p/webkit/Source/WebCore/page/DragController.cpp:253
#6  0x0000000102bc1429 in WebCore::DragController::dragUpdated (this=0x109921d00, dragData=0x7fff5fbfd6b0) at /Users/p/webkit/Source/WebCore/page/DragController.cpp:192
#7  0x000000010108f07a in WebKit::WebPage::performDragControllerAction (this=0x10a027800, action=1, clientPosition={m_x = 58, m_y = 114}, globalPosition={m_x = 261, m_y = 208}, draggingSourceOperationMask=15, dragStorageName=@0x7fff5fbfd7f0, flags=2, sandboxExtensionHandle=@0x7fff5fbfd7fc) at /Users/p/webkit/Source/WebKit2/WebProcess/WebPage/WebPage.cpp:1914
#8  0x000000010114b4b7 in CoreIPC::callMemberFunction<WebKit::WebPage, void (WebKit::WebPage::*)(unsigned long long, WebCore::IntPoint, WebCore::IntPoint, unsigned long long, WTF::String const&, unsigned int, WebKit::SandboxExtension::Handle const&), unsigned long long, WebCore::IntPoint, WebCore::IntPoint, unsigned long long, WTF::String, unsigned int, WebKit::SandboxExtension::Handle> (args=@0x7fff5fbfd7d0, object=0x10a027800, function={__pfn = 0x10108eef4 <WebKit::WebPage::performDragControllerAction(unsigned long long, WebCore::IntPoint, WebCore::IntPoint, unsigned long long, WTF::String const&, unsigned int, WebKit::SandboxExtension::Handle const&)>, __delta = 0}) at HandleMessage.h:55
#9  0x000000010115003c in CoreIPC::handleMessage<Messages::WebPage::PerformDragControllerAction, WebKit::WebPage, void (WebKit::WebPage::*)(unsigned long long, WebCore::IntPoint, WebCore::IntPoint, unsigned long long, WTF::String const&, unsigned int, WebKit::SandboxExtension::Handle const&)> (argumentDecoder=0x11cce8760, object=0x10a027800, function={__pfn = 0x10108eef4 <WebKit::WebPage::performDragControllerAction(unsigned long long, WebCore::IntPoint, WebCore::IntPoint, unsigned long long, WTF::String const&, unsigned int, WebKit::SandboxExtension::Handle const&)>, __delta = 0}) at HandleMessage.h:277
#10 0x0000000101149f58 in WebKit::WebPage::didReceiveWebPageMessage (this=0x10a027800, messageID={m_messageID = 983105}, arguments=0x11cce8760) at /Users/p/webkit/WebKitBuild/Debug/DerivedSources/WebKit2/WebPageMessageReceiver.cpp:295
#11 0x000000010108a7f2 in WebKit::WebPage::didReceiveMessage (this=0x10a027800, connection=0x10011f610, messageID={m_messageID = 983105}, arguments=0x11cce8760) at /Users/p/webkit/Source/WebKit2/WebProcess/WebPage/WebPage.cpp:2248
#12 0x00000001010e4525 in WebKit::WebProcess::didReceiveMessage (this=0x100117830, connection=0x10011f610, messageID={m_messageID = 983105}, arguments=0x11cce8760) at /Users/p/webkit/Source/WebKit2/WebProcess/WebProcess.cpp:657
#13 0x0000000101005798 in CoreIPC::Connection::dispatchMessage (this=0x10011f610, message=@0x7fff5fbfdf10) at /Users/p/webkit/Source/WebKit2/Platform/CoreIPC/Connection.cpp:689
#14 0x000000010100590c in CoreIPC::Connection::dispatchMessages (this=0x10011f610) at /Users/p/webkit/Source/WebKit2/Platform/CoreIPC/Connection.cpp:716
#15 0x0000000101008003 in MemberFunctionWorkItem0<CoreIPC::Connection>::execute (this=0x109946fc0) at WorkItem.h:79
#16 0x0000000101047dd5 in RunLoop::performWork (this=0x100117180) at /Users/p/webkit/Source/WebKit2/Platform/RunLoop.cpp:63
#17 0x0000000101048f2d in RunLoop::performWork (context=0x100117180) at /Users/p/webkit/Source/WebKit2/Platform/mac/RunLoopMac.mm:37
#18 0x00007fff83eff3d1 in __CFRunLoopDoSources0 ()
#19 0x00007fff83efd5c9 in __CFRunLoopRun ()
#20 0x00007fff83efcd8f in CFRunLoopRunSpecific ()
#21 0x00007fff83b957ee in RunCurrentEventLoopInMode ()
#22 0x00007fff83b955f3 in ReceiveNextEventCommon ()
#23 0x00007fff83b954ac in BlockUntilNextEventMatchingListInMode ()
#24 0x00007fff81767eb2 in _DPSNextEvent ()
#25 0x00007fff81767801 in -[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:] ()
#26 0x00007fff8172d68f in -[NSApplication run] ()
#27 0x0000000101048cf0 in RunLoop::run () at /Users/p/webkit/Source/WebKit2/Platform/mac/RunLoopMac.mm:64
#28 0x00000001010f1882 in WebKit::WebProcessMain (commandLine=@0x7fff5fbff3d0) at /Users/p/webkit/Source/WebKit2/WebProcess/mac/WebProcessMainMac.mm:118
#29 0x00000001010877d1 in WebKitMain (commandLine=@0x7fff5fbff3d0) at /Users/p/webkit/Source/WebKit2/WebProcess/WebKitMain.cpp:50
#30 0x0000000101087890 in WebKitMain (argc=8, argv=0x7fff5fbff4a0) at /Users/p/webkit/Source/WebKit2/WebProcess/WebKitMain.cpp:74
#31 0x0000000100000e30 in main ()
(gdb) 


## Attachments

- [webkit-dd.zip](attachments/webkit-dd.zip) (application/zip; charset=binary, 31.1 KB)
- [remove-node-in-drag.html](attachments/remove-node-in-drag.html) (text/html; charset=us-ascii, 1.0 KB)

## Timeline

### sk...@chromium.org (2012-02-01)

Odd. the first time I tried this (in 16.0.912.77 m), I got a sad tab. After that I have been unable to repro in any version of Chromium, both under a debugger and not. So, I have been unable to confirm.

Given that I did see a sad tab and that the analysis sounds reasonable, I'll assign flags accordingly. I would appreciate if somebody else could try to confirm this.

@pawlkt - did you open a bug at webkit.org for this too? If so, what is the bug number?

### js...@chromium.org (2012-02-01)

Please do not set speculative flags. You haven't confirmed it in a debugger to determine the severity or what branches are impacted.

### sk...@chromium.org (2012-02-01)

@rniwa - you show up in SVN Blame as having worked on the code mentioned in the first comment. Can you help me find an owner for this bug? If not, do you know somebody that could?

### pa...@gmail.com (2012-02-01)

@skylined:
I didn't open a bug at webkit.org.
I'm getting a sad tab in 16.0.912.77 m every time. Try changing constants in spray(), so that it claims more heap space.

### sk...@chromium.org (2012-02-01)

Thanks pawlkt. Once we've confirmed the issue, we'll open a WebKit bug.

I'll try to tweak the repro a little to see if I can trigger the crash.

### sk...@chromium.org (2012-02-01)

Confirmed in Chromium version 18.0.1026.0
Chromium revision 119905
WebKit revision 76115
v8 revision 10507
Skia revision 3100
I'll try to repro in stable now as well.

@Abhishek/Martin; is there a way to automate drag & drop in ClusterFuzz, so I can feed this repro as a testcase?

### in...@chromium.org (2012-02-01)

BJ, the trick for drag and drop is to create a testcase for DumpRenderTree and call event handler for moving mouse. when you upload testcase to clusterfuzz, specify linux_asan_drt as job type. then rest everything clusterfuzz will do to help in traging. 

### [Deleted User] (2012-02-01)

I can't hit the crash but the analysis seems correct. We just need to turn it into a RefPtr.

### sk...@chromium.org (2012-02-01)

@pawlkt: Something strange is going on here; the explanation in https://crbug.com/chromium/112259#c1 does not match the stack you provided. I have been able to reproduce the crash that matches the stack you provided, but on investigation that appears to be a simple NULL ptr in EventTarget::dispatchEvent. I've attached a reduced repro for that.

This NULL ptr requires an event handler to keep the main thread busy (a simple while loop will suffice) so the user can trigger a second event. Then the event handler needs to show a popup. When this popup is closed, the NULL ptr happens. This last step can be automated using showModalDialog().

Affects 16.0.912.77-18.0.1026.0

@pawlkt: as I have effectively been unable to reproduce the use-after-free mentioned in https://crbug.com/chromium/112259#c1, I have downgraded severity to None (for a NULL ptr). If you can create a repro that does trigger it somewhat reliably, please let us know, so we can investigate further.

@rniwa: thanks for the quick analysis. do you think that this repro (or any other) could trigger the bug?

### pa...@gmail.com (2012-02-01)

@skylined:
#0  0x0000000102c18541 in WebCore::EventTarget::dispatchEvent (this=0x1099aa110, event=@0x7fff5fbfd2b0, ec=@0x7fff5fbfd31c) at /Users/p/webkit/Source/WebCore/dom/EventTarget.cpp:165
#1  0x0000000102c004b1 in WebCore::EventHandler::dispatchDragEvent (this=0x100871900, eventType=@0x10086d8e8, dragTarget=0x1099aa110, event=@0x7fff5fbfd470, clipboard=0x1099c2af0) at /Users/p/webkit/Source/WebCore/page/EventHandler.cpp:1766
#2  0x0000000102c05a1d in WebCore::EventHandler::updateDragAndDrop (this=0x100871900, event=@0x7fff5fbfd470, clipboard=0x1099c2af0) at 

These frames do match the situation I'm describing, no?

You may be seeing NULL derefs because of how the memory allocator behaves. Before a node is freed, its various pointers (like next, previous siblings etc) are set to null. You may be observing webkit manipulating such "cleaned" object, that was not yet spammed by JS spraying.

Do this:
- put a BP on 2 (see 1st comment) and step over it
- print *newTarget (in gdb) and observe that m_refcnt is zero (since this Node is not RefPtr<> it can be freed before the function returns)
- step over 3
- print *newTarget, and see that the object did change (was freed, but not necessarily reclaimed by JS spray()).


### [Deleted User] (2012-02-01)

I was able to create a new reduction for DRT based on the analysis posted in the original report.

### [Deleted User] (2012-02-01)

Filed https://bugs.webkit.org/show_bug.cgi?id=77569.

### sk...@chromium.org (2012-02-01)

Thanks pawlkt, unfortunately, it seems I didn't look close enough. Here's the stack I am seeing:
                chrome.dll!WebCore::EventTarget::dispatchEvent
                chrome.dll!WebCore::EventHandler::dispatchDragEvent
                chrome.dll!WebCore::EventHandler::dispatchDragSrcEvent
                chrome.dll!WebCore::EventHandler::handleDrag
                chrome.dll!WebCore::EventHandler::handleMouseDraggedEvent
                chrome.dll!WebCore::EventHandler::handleMouseMoveEvent
                chrome.dll!WebCore::EventHandler::mouseMoved
                chrome.dll!WebKit::WebViewImpl::mouseMove
                chrome.dll!WebKit::WebViewImpl::handleInputEvent
                chrome.dll!RenderWidget::OnHandleInputEvent
                chrome.dll!IPC::Message::Dispatch<...>

bool EventTarget::dispatchEvent(PassRefPtr<Event> event, ExceptionCode& ec)
{
    if (!event || event->type().isEmpty()) {
        ec = EventException::UNSPECIFIED_EVENT_TYPE_ERR;
        return false;
    }

    if (event->isBeingDispatched()) {
        ec = EventException::DISPATCH_REQUEST_ERR;
        return false;
    }

    if (!scriptExecutionContext())            /// <!------- CRASH HERE
        return false;

    return dispatchEvent(event);
}

This crash is in the same function, and on the same line, but with a different call stack leading up to it. It is caused by dragTarget being NULL. Maybe we've found two problems in the same code (since my repro does not modify the DOM, I can't see how it can be the same as the bug you are describing). I'll have to look at this some more tomorrow.

### sk...@chromium.org (2012-02-01)

Ryosuke Niwa for the win!

### in...@chromium.org (2012-02-01)

Ryosuke rocks. clusterfuzz report coming soon with regression ranges and stable, beta impact - https://cluster-fuzz.appspot.com/testcase?key=17434031

### in...@chromium.org (2012-02-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17434031

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f2a5ad86280
Crash State:
  - crash stack -
  WebCore::EventTarget::dispatchEvent
  WebCore::EventHandler::dispatchDragEvent
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  WebCore::HTMLTextAreaElement::create
  

Minimized Testcase (27.91 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95lfP1_MlSG6Xvvo5sjk5cYjjfQQkcU_lVMHAwKCFWhSDKwEZ0XwMC4w5bicOBTty7Ue3t8eaetzda3TJGzftwS-O5RQ2_jqdeI0t6Vw0VqPjZSbSsjY3gkUOppJfgFKoEqHq4DjApAmihfXhBPO8cpHIwKAg

### in...@chromium.org (2012-02-01)

user interaction lowers down severity.

### in...@chromium.org (2012-02-01)

http://trac.webkit.org/changeset/106488

### sc...@gmail.com (2012-02-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-05)

@pawlkt: thanks for a great bug! Since it's a security bug, it qualifies for a Chromium Security Reward. We're rewarding at the $500 level, taking into account the user interaction required.

We'll credit this discovery in our release notes, of course. Any particular name / affiliation you'd like us to use?

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

### pa...@gmail.com (2012-02-05)

@scarybeasts: 

just "pa_kt". that was fast, btw.

### sc...@gmail.com (2012-02-10)

M17: http://trac.webkit.org/changeset/107413
M18: http://trac.webkit.org/changeset/107414

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-06)

Reward to be upped to $1337 and to go to EFF

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-05-26)

$1337 donated to EFF. Thanks again :D

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

This issue was migrated from crbug.com/chromium/112259?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053180)*
