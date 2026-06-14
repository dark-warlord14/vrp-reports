# CSSCursorImageValue not clearing SVGElement back pointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40086036](https://issues.chromium.org/issues/40086036) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ja...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-12-13 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 8.0.552.224  

URLs (if applicable) : <https://bug330638.bugzilla.mozilla.org/attachment.cgi?id=497286>  

Other browsers tested: FF4.0b7  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5: -  

Firefox 3.x: Ok  

IE 7/8: N/A

**What steps will reproduce the problem?**

1. Open URL,
2. Press the mouse button on green wheel
3. Move the mouse (rotate the wheel)
4. Release the mouse button
5. Pres the mouse button again

**What is the expected result?**

- rotating the wheel again

**What happens instead?**

- crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

- it seems to be regression as I encounter this problem after update from the previous version (8.0.552.215).

## Timeline

### ja...@gmail.com (2010-12-13)

It is probably connected with the 'cursor' attribute. When the mouse pointer is changed via CSS (style="cursor: url('#hand...."), no crash is detected.

### th...@chromium.org (2010-12-13)

Can you get a crash report id?
http://dev.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug

### ja...@gmail.com (2010-12-15)

Sorry for that misleading title, actually it is not 'crash' of the app, but just failure of rendering the content. I see the 'Aw, Snap!' page with black background with the smiley icon and the link to this page: http://www.google.com/support/chrome/bin/answer.py?answer=95669 


### ja...@gmail.com (2010-12-15)

Oops, I forgot to mention my environment: Win7/64bit

### th...@chromium.org (2010-12-15)

http://crash/reportdetail?reportid=5177d9a97c7fa148

Thread 0 *CRASHED* ( SIGSEGV @ 0x00000000 )
0x01b8a9d9 	[chrome 	- third_party/WebKit/JavaScriptCore/wtf/HashTable.h:280] 	WTF::HashTable<WebCore::SVGElement*,WebCore::SVGElement*,WTF::IdentityExtractor<WebCore::SVGElement*>,WTF::PtrHash<WebCore::SVGElement*>,WTF::HashTraits<WebCore::SVGElement*>,WTF::HashTraits<WebCore::SVGElement*> >::find<WebCore::SVGElement*, WTF::IdentityHashTranslator<WebCore::SVGElement*, WebCore::SVGElement*, WTF::PtrHash<WebCore::SVGElement*> > >
0x01b8aa8e 	[chrome 	- third_party/WebKit/JavaScriptCore/wtf/HashTable.h:326] 	WebCore::CSSCursorImageValue::removeReferencedElement
0x01c4cad6 	[chrome 	- third_party/WebKit/WebCore/svg/SVGElement.cpp:220] 	WebCore::SVGElement::setCursorImageValue
0x01b8ba5d 	[chrome 	- third_party/WebKit/WebCore/css/CSSCursorImageValue.cpp:105] 	WebCore::CSSCursorImageValue::updateIfSVGCursorIsUsed
0x0183ebd6 	[chrome 	- third_party/WebKit/WebCore/css/CSSStyleSelector.cpp:3487] 	WebCore::CSSStyleSelector::applyProperty
0x0184448f 	[chrome 	- third_party/WebKit/WebCore/css/CSSStyleSelector.cpp:2902] 	WebCore::CSSStyleSelector::applyDeclarations<false>
0x01846753 	[chrome 	- third_party/WebKit/WebCore/css/CSSStyleSelector.cpp:1299] 	WebCore::CSSStyleSelector::styleForElement
0x0188a805 	[chrome 	- third_party/WebKit/WebCore/dom/Element.cpp:973] 	WebCore::Element::recalcStyle
0x0188aabe 	[chrome 	- third_party/WebKit/WebCore/dom/Element.cpp:1041] 	WebCore::Element::recalcStyle
0x0188aabe 	[chrome 	- third_party/WebKit/WebCore/dom/Element.cpp:1041] 	WebCore::Element::recalcStyle
0x01872f76 	[chrome 	- third_party/WebKit/WebCore/dom/Document.cpp:1574] 	WebCore::Document::recalcStyle
0x018678a1 	[chrome 	- third_party/WebKit/WebCore/dom/Document.cpp:1616] 	WebCore::Document::updateStyleIfNeeded
0x018966eb 	[chrome 	- third_party/WebKit/WebCore/dom/MouseRelatedEvent.cpp:152] 	WebCore::MouseRelatedEvent::receivedTarget
0x01b9ce3c 	[chrome 	- third_party/WebKit/WebCore/dom/EventContext.cpp:46] 	WebCore::EventContext::handleLocalEvents
0x018a1504 	[chrome 	- third_party/WebKit/WebCore/dom/Node.cpp:2619] 	WebCore::Node::dispatchGenericEvent
0x018a15dc 	[chrome 	- third_party/WebKit/WebCore/dom/Node.cpp:2561] 	WebCore::Node::dispatchEvent
0x018a0582 	[chrome 	- third_party/WebKit/WebCore/dom/Node.cpp:2815] 	WebCore::Node::dispatchMouseEvent
0x018a1857 	[chrome 	- third_party/WebKit/WebCore/dom/Node.cpp:2724] 	WebCore::Node::dispatchMouseEvent
0x01a1c258 	[chrome 	- third_party/WebKit/WebCore/page/EventHandler.cpp:1841] 	WebCore::EventHandler::dispatchMouseEvent
0x01a2401a 	[chrome 	- third_party/WebKit/WebCore/page/EventHandler.cpp:1569] 	WebCore::EventHandler::handleMouseReleaseEvent
0x01426e8c 	[chrome 	- third_party/WebKit/WebKit/chromium/src/WebViewImpl.cpp:542] 	WebKit::WebViewImpl::mouseUp
0x0142a7e4 	[chrome 	- third_party/WebKit/WebKit/chromium/src/WebViewImpl.cpp:1149] 	WebKit::WebViewImpl::handleInputEvent
0x00aba53c 	[chrome 	- chrome/renderer/render_widget.cc:334] 	RenderWidget::OnHandleInputEvent
0x00abb2e6 	[chrome 	- ./ipc/ipc_message.h:148] 	RenderWidget::OnMessageReceived
0x00aa730e 	[chrome 	- chrome/renderer/render_view.cc:1045] 	RenderView::OnMessageReceived
0x01d9e855 	[chrome 	- chrome/common/message_router.cc:46] 	MessageRouter::RouteMessage
0x00b8eda0 	[chrome 	- base/message_loop.cc:418] 	MessageLoop::RunTask

### [Deleted User] (2010-12-17)

After loading the page, double clicking on the svg image crashes the renderer on windows.

This is with Google Chrome 10.0.612.1 (Official Build 69289)

Full report @ http://crash/reportdetail?reportid=577077dcdbca0215

### js...@chromium.org (2010-12-17)

This is a lot like https://crbug.com/chromium/64959, but the crash occurs with the fix applied. I'll take a look at it since I've been poking around in those code recently.

### js...@chromium.org (2010-12-17)

Okay, definite stale pointer. I either uncovered a bug or added a new one when I fixed https://crbug.com/chromium/64959.

### js...@chromium.org (2010-12-18)

Okay, I'm an idiot. This is due to a typo in my fix for https://crbug.com/chromium/64959. I'll get a patch upstream this weekend. For anyone who wants a laugh, this is the fix (and the kicker is that I added both those methods):

Index: css/CSSCursorImageValue.cpp
===================================================================
--- css/CSSCursorImageValue.cpp (revision 74255)
+++ css/CSSCursorImageValue.cpp (working copy)
@@ -71,7 +71,7 @@

     for (; it != end; ++it) {
         SVGElement* referencedElement = *it;
-        referencedElement->cursorElementRemoved();
+        referencedElement->cursorImageElementRemoved();
         if (SVGCursorElement* cursorElement = resourceReferencedByCursorElement(url, referencedElement->document()))
             cursorElement->removeClient(referencedElement);
     }


### js...@chromium.org (2010-12-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-12-22)

Reported upstream and patch up for review: https://bugs.webkit.org/show_bug.cgi?id=51417

### js...@chromium.org (2010-12-23)

Patch landed upstream: http://trac.webkit.org/changeset/74574

Definitely want to merge this for the next stable update.

### sc...@gmail.com (2010-12-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-04)

merged to m8 in r75008, needs merging to m9.

### sc...@gmail.com (2011-01-05)

@j.tosovsky@tiscali.cz: congratulations! This bug turned out to be a security issue, and as such it has provisionally qualified for a $500 Chromium Security Reward.
---
NOTE: normally we do not reward security bugs unless initially filed with the
security templaye. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issues.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---
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

### sc...@gmail.com (2011-01-06)

@j.tosovsky@tiscali.cz: if you like, we can credit you under a real / full name in our release notes and Hall of Fame.

### ja...@gmail.com (2011-01-06)

Why not, my 5 minutes of fame :-)
Jan Tošovský (or Jan Tosovsky when a limited charset will be used)
Btw, thanks for that security reward! And that quick fix, of course.

### in...@chromium.org (2011-01-10)

merged to m9 in r75426.

### sc...@gmail.com (2011-01-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-13)

@j.tosovsky@tiscali.cz: autoupdating to users already with http://googlechromereleases.blogspot.com/2011/01/chrome-stable-release.html (8.0.552.237)

Thanks again! Now we pay you :D Please e-mail cevans@chromium.org to start that process.

### sc...@gmail.com (2011-01-24)

Invoice finalized; payment is in e-payment system.

### la...@chromium.org (2011-03-19)

Chrome Version : 8.0.552.224  

URLs (if applicable) : <https://bug330638.bugzilla.mozilla.org/attachment.cgi?id=497286>  

Other browsers tested: FF4.0b7  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5: -  

Firefox 3.x: Ok  

IE 7/8: N/A

**What steps will reproduce the problem?**

1. Open URL,
2. Press the mouse button on green wheel
3. Move the mouse (rotate the wheel)
4. Release the mouse button
5. Pres the mouse button again

**What is the expected result?**

- rotating the wheel again

**What happens instead?**

- crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

- it seems to be regression as I encounter this problem after update from the previous version (8.0.552.215).

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

This issue was migrated from crbug.com/chromium/66748?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/67377]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086036)*
