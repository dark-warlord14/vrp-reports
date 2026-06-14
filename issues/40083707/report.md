# Use after free in HTMLTextFormControlElement::selection()

| Field | Value |
|-------|-------|
| **Issue ID** | [40083707](https://issues.chromium.org/issues/40083707) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | vk...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-10-11 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 6.0.472.63  

URLs (if applicable) : <http://tatianastomatobase.com/seed-order/html/tis/>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

Firefox 3.x: OK  

IE 7: OK  

IE 8: OK

**What steps will reproduce the problem?**

1. Click on View Inventory
2. Click on a white table cell, to activate it
3. Hold down CTRL, and press the LEFT or RIGHT arrow key
4. Your browser tab should crash.

**What is the expected result?**

The cell to the LEFT or RIGHT of the activated cell should be activated, while the original cell should be deactivated

**What happens instead?**

The tab crashes.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

I've tracked the problem down to one specific method -

<http://tatianastomatobase.com/seed-order/js/tis/view.js>

The method code is as follows:

/\*\*  

\* Deactivates a cell, hiding its input field, and showing its span field  

\*/  

View.prototype.deactivateCell = function (cell){  

//Show the span, hide the input  

var label = cell.descendants()[0];  

var input = cell.descendants()[1];  

if(label){  

label.show();  

if(label.innerHTML == 0){  

label.innerHTML = "";  

}  

}  

if(input){  

input.addClassName("hiddenInput");  

input.hide();  

if(input.value == 0){  

input.value = "";  

}  

}  

}

The method is invoked in other situations of the web-app, without causing the tab to crash - it only crashes when invoked after a CTRL-LEFT or CTRL-RIGHT event is processed.

The cell variable is not null, the input variable is not null, the input variable points to the right input... That method should not crash the browser.

I could not reproduce this by isolating that small piece of code - some other part of the web-app puts the browser into a state that causes the crash.

## Attachments

- [render-text-crash-ajax.html](attachments/render-text-crash-ajax.html) (text/html; charset=us-ascii, 16.6 KB)
- [render-text-crash-ajax.html](attachments/render-text-crash-ajax_53405590.html) (text/html; charset=us-ascii, 655 B)

## Timeline

### te...@gmail.com (2010-10-11)

I can confirm the tab crash with Chromium 8.0.550.0 (r62017) and Safari 5. I'll try creating a reduced testcase for it.

### pe...@gtempaccount.com (2010-10-11)

Thank you for reporting this issue. I can reproduce this on the given page, which gives the following crash-dump.

The associated code can be found here: http://goo.gl/unuk

00000000()	
chrome.dll!WebCore::Position::upstream(WebCore::Position::EditingBoundaryCrossingRule rule=CannotCrossEditingBoundary)  Line 502	C++
chrome.dll!WebCore::VisiblePosition::canonicalPosition(const WebCore::Position & passedPosition={...})  Line 462	C++
chrome.dll!WebCore::VisiblePosition::init(const WebCore::Position & position={...}, WebCore::EAffinity affinity=DOWNSTREAM)  Line 61 + 0x1c bytes	C++
chrome.dll!WebCore::VisiblePosition::VisiblePosition(WebCore::Node * node=0x08e67bc0, int offset=0x00000000, WebCore::EAffinity affinity=DOWNSTREAM)  Line 54 + 0x46 bytes	C++
chrome.dll!WebCore::RenderTextControl::selection(int start=0x00000000, int end=0x00000000)  Line 268 + 0x2d bytes	C++
chrome.dll!WebCore::HTMLTextFormControlElement::selection()  Line 599 + 0x2a bytes	C++
chrome.dll!WebCore::Editor::selectionForCommand(WebCore::Event * event=0x08aa52a0)  Line 101 + 0xc bytes	C++
chrome.dll!WebCore::enabledInEditableTextOrCaretBrowsing(WebCore::Frame * frame=0x08ddd800, WebCore::Event * event=0x08aa52a0, WebCore::EditorCommandSource __formal=CommandFromMenuOrKeyBinding)  Line 1209 + 0x35 bytes	C++
chrome.dll!WebCore::Editor::Command::execute(const WTF::String & parameter={...}, WebCore::Event * triggeringEvent=0x08aa52a0)  Line 1602 + 0x33 bytes	C++
chrome.dll!WebCore::Editor::Command::execute(WebCore::Event * triggeringEvent=0x08aa52a0)  Line 1613 + 0x19 bytes	C++
chrome.dll!WebKit::EditorClientImpl::handleEditingKeyboardEvent(WebCore::KeyboardEvent * evt=0x08a6f2a0)  Line 571 + 0xa bytes	C++
chrome.dll!WebKit::EditorClientImpl::handleKeyboardEvent(WebCore::KeyboardEvent * evt=0x08aa52a0)  Line 640 + 0x22 bytes	C++
chrome.dll!WebCore::EventHandler::defaultKeyboardEventHandler(WebCore::KeyboardEvent * event=0x08aa52a0)  Line 2370	C++
chrome.dll!WebCore::Node::defaultEventHandler(WebCore::Event * event=0x08aa52a0)  Line 2982	C++
chrome.dll!WebCore::HTMLFormControlElementWithState::defaultEventHandler(WebCore::Event * event=0x08aa52a0)  Line 471 + 0x8 bytes	C++
chrome.dll!WebCore::HTMLInputElement::defaultEventHandler(WebCore::Event * evt=0x08aa5200)  Line 1600	C++
chrome.dll!WebCore::Node::dispatchGenericEvent(WTF::PassRefPtr<WebCore::Event> prpEvent={...})  Line 2670	C++
chrome.dll!WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event> prpEvent={...})  Line 2577 + 0xc bytes	C++
chrome.dll!WebCore::EventTarget::dispatchEvent(WTF::PassRefPtr<WebCore::Event> event={...}, int & ec=0x04d3f698)  Line 278 + 0x1a bytes	C++
chrome.dll!WebCore::EventHandler::keyEvent(const WebCore::PlatformKeyboardEvent & initialKeyEvent={...})  Line 2290	C++
chrome.dll!WebKit::WebViewImpl::keyEvent(const WebKit::WebKeyboardEvent & event={...})  Line 579 + 0xc bytes	C++
chrome.dll!WebKit::WebViewImpl::handleInputEvent(const WebKit::WebInputEvent & inputEvent={...})  Line 1123 + 0x8 bytes	C++
chrome.dll!RenderWidget::OnHandleInputEvent(const IPC::Message & message={...})  Line 351 + 0x8 bytes	C++
chrome.dll!IPC::Message::Dispatch<RenderWidget>(const IPC::Message * msg=0x08b3bb20, RenderWidget * obj=0x08d55b00, void (const IPC::Message &)* func=0x69179ea0)  Line 149	C++
chrome.dll!RenderWidget::OnMessageReceived(const IPC::Message & msg={...})  Line 175 + 0x1d bytes	C++
chrome.dll!RenderView::OnMessageReceived(const IPC::Message & message={...})  Line 806	C++
chrome.dll!MessageRouter::RouteMessage(const IPC::Message & msg={...})  Line 46 + 0xa bytes	C++
chrome.dll!MessageRouter::OnMessageReceived(const IPC::Message & msg={...})  Line 37 + 0x5 bytes	C++
chrome.dll!ChildThread::OnMessageReceived(const IPC::Message & msg={...})  Line 163 + 0xb bytes	C++
chrome.dll!RunnableMethod<UserStyleSheetLoader,void (__thiscall UserStyleSheetLoader::*)(GURL const &),Tuple1<GURL> >::Run()  Line 330 + 0xf bytes	C++
chrome.dll!MessageLoop::RunTask(Task * task=0x08b3bb10)  Line 411	C++
chrome.dll!MessageLoop::DoWork()  Line 526 + 0x8 bytes	C++
chrome.dll!base::MessagePumpForUI::DoRunLoop()  Line 203	C++
chrome.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x04d3fb6c)  Line 80 + 0x42 bytes	C++
chrome.dll!MessageLoop::RunInternal()  Line 258 + 0xb bytes	C++
chrome.dll!MessageLoop::Run()  Line 209	C++
chrome.dll!base::Thread::Run(MessageLoop * message_loop=0x04d3fb6c)  Line 141	C++
chrome.dll!base::Thread::ThreadMain()  Line 167	C++
chrome.dll!`anonymous namespace'::ThreadFunc(void * closure=0x04012a20)  Line 27	C++
kernel32.dll!757deccb()
[Frames below may be incorrect and/or missing, no symbols loaded for kernel32.dll]	
ntdll.dll!77bad24d()
chrome.dll!xsltParseStylesheetImport(_xsltStylesheet * style=, _xmlNode * cur=)  Line 143 + 0x16 bytes	C

https://crbug.com/chromium/33106 crashed in the same method (WebCore::Position::upstream) and has been marked as fixed, but noting it for reference. I'll try to create a reduced test-case later on unless temp01 can create one.

### pe...@gtempaccount.com (2010-10-11)

This should be untriaged, excuse me.

### dg...@chromium.org (2010-10-11)

Ryosuke, could take a look at this? If it's not in your area, please bounce this back to me.

### ry...@gmail.com (2010-10-11)

Test case without Prototype.  Click white blocks below 2006-2010 and move to left or right.  WebKit TOT crashes.
I'm going to spend a little more time reducing the test case and file a WebKit bug.


### [Deleted User] (2010-10-12)

The WebKit https://crbug.com/chromium/47522 (https://bugs.webkit.org/show_bug.cgi?id=47522) has been filed with a reduction.

### vk...@gmail.com (2010-10-12)

I've done some more testing, and it seems that this crash occurs when the Key press event has the "keydown" type.

It does not occur when the event's type is keyup.

It does not occur when the event keypress an alphanumerical character, Space, or Return.

It occurs with the Right, left, up, down arrow keys, Page Up, Page Down, End, Home, Delete, Backspace keys.

It does not require the CTRL key modifier to be active.

### [Deleted User] (2010-10-12)

It turned out that this is a security hole.

### in...@chromium.org (2010-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2010-10-12)

(I was asked by temp01irc)
Will the original reporter be eligible for http://dev.chromium.org/Home/chromium-security/vulnerability-rewards-program ?


### la...@chromium.org (2010-10-12)

Bulk moving to mstone 8, at this point work on m7 should effectively be closed.  If something in this bulk edit is not actively being worked on, please change the mstone to m9.

### in...@chromium.org (2010-10-12)

We should aim v7 1st patch for this. Moving back flags.

### [Deleted User] (2010-10-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-13)

ccing reporter from dup 58972

### [Deleted User] (2010-10-13)

Turned out that this is a part of much bigger security issue we have in WebKit.  While we might check in a temporary fix for this crash, we might need to do a surgery on WebCore/rendering to kill similar security holes.

### [Deleted User] (2010-10-15)

WebKit bug has a patch that has been reviewed.  The patch will be landed shortly and will be merged to the chromium branch.

### sc...@gmail.com (2010-10-15)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-15)

Landed upstream: http://trac.webkit.org/changeset/69831

Need to merge to m8. Probably want to catch the next stable refresh on m7 as well.

### in...@chromium.org (2010-10-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-22)

m7 merge in r70348, m8 merge in r70349.

### sc...@gmail.com (2010-10-23)

@vkouchna: thanks for filing this report. And congratulations! We'd like to provisionally offer you a $500 Chromium Security Reward.
Although this bug report was not originally filed a security report, we found the information very useful to track down a security issue.

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

### vk...@gmail.com (2010-10-24)

Good to hear - my disclosure to date has been a Stack Overflow question, posted roughly a day before filing this report - I was at the time fishing for work-arounds to the issue.

I didn't provide my app's source, and I don't think that question would in itself sufficient to reproduce the issue.

### vk...@gmail.com (2010-10-24)

Or at least, no source but the single method posted above.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-22)

@vkouchna: thanks again! Please e-mail me, cevans@chromium.org to collect your reward.

### sc...@gmail.com (2010-12-02)

Payment is in the electronic system.

### la...@chromium.org (2011-03-19)

Chrome Version : 6.0.472.63  

URLs (if applicable) : <http://tatianastomatobase.com/seed-order/html/tis/>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

Firefox 3.x: OK  

IE 7: OK  

IE 8: OK

**What steps will reproduce the problem?**

1. Click on View Inventory
2. Click on a white table cell, to activate it
3. Hold down CTRL, and press the LEFT or RIGHT arrow key
4. Your browser tab should crash.

**What is the expected result?**

The cell to the LEFT or RIGHT of the activated cell should be activated, while the original cell should be deactivated

**What happens instead?**

The tab crashes.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

I've tracked the problem down to one specific method -

<http://tatianastomatobase.com/seed-order/js/tis/view.js>

The method code is as follows:

/\*\*  

\* Deactivates a cell, hiding its input field, and showing its span field  

\*/  

View.prototype.deactivateCell = function (cell){  

//Show the span, hide the input  

var label = cell.descendants()[0];  

var input = cell.descendants()[1];  

if(label){  

label.show();  

if(label.innerHTML == 0){  

label.innerHTML = "";  

}  

}  

if(input){  

input.addClassName("hiddenInput");  

input.hide();  

if(input.value == 0){  

input.value = "";  

}  

}  

}

The method is invoked in other situations of the web-app, without causing the tab to crash - it only crashes when invoked after a CTRL-LEFT or CTRL-RIGHT event is processed.

The cell variable is not null, the input variable is not null, the input variable points to the right input... That method should not crash the browser.

I could not reproduce this by isolating that small piece of code - some other part of the web-app puts the browser into a state that causes the crash.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2011-10-21)

[Empty comment from Monorail migration]

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/58741?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/58972]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083707)*
