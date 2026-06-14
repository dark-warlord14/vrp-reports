# Use-after-free in WebCore::RenderTextControl::isSelectableElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40091700](https://issues.chromium.org/issues/40091700) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

textarea -> crash

**VERSION**  

Chrome Version: r86329 onwards. it's a webkit roll 87065:87089. pretty sure it's webkit r87067

Operating System: linux, osx

**REPRODUCTION CASE**

<textarea id="A"></textarea>
<textarea id="B"></textarea>
<script>
A.selectionStart = 0;
B.style.display = "none";
B.selectionStart = 0;
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

at 0x100: ???  

by 0x1A75156: WebCore::RenderTextControl::isSelectableElement(WebCore::Node\*) const  

by 0x1A75D67: WebCore::RenderTextControl::indexForVisiblePosition(WebCore::VisiblePosition const&) const

## Attachments

- [isSelectableElement.html](attachments/isSelectableElement.html) (text/plain; charset=us-ascii, 153 B)
- [isSelectableElement-vg-85418.txt](attachments/isSelectableElement-vg-85418.txt) (text/plain; charset=us-ascii, 11.9 KB)

## Timeline

### in...@chromium.org (2011-06-08)

Very Very nice Miaubiz. We didnt have a repro for this one, but just a stack.

### in...@chromium.org (2011-06-08)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-06-08)

this is like /WebKit/LayoutTests/fast/dom/text-control-crash-on-select.html  

with line 28 removed.
which is:
     $(id).style.display = "none";

for textarea3

### in...@chromium.org (2011-06-08)

Kent-san, can you please take a look.

### mi...@gmail.com (2011-06-08)

vg log

### in...@chromium.org (2011-06-08)

int RenderTextControl::selectionEnd() const
{
    Frame* frame = this->frame();
    if (!frame)
        return 0;
    return indexForVisiblePosition(frame->selection()->end());

frame->selection()->end() create VisiblePosition which updates layout and hence blows away the RenderTextControl from underneath.

### in...@chromium.org (2011-06-08)

Probably we should update layout earlier by using textRendererAfterUpdateLayout in HTMLTextFormControlElement::selectionStart, HTMLTextFormControlElement::selectionEnd. In that case, we will bail out early without the use after free.

RenderTextControl* HTMLTextFormControlElement::textRendererAfterUpdateLayout()
{
    if (!isTextFormControl())
        return 0;
    document()->updateLayoutIgnorePendingStylesheets();
    return toRenderTextControl(renderer());
}

int HTMLTextFormControlElement::selectionStart() const
{
    if (!isTextFormControl())
        return 0;
    if (document()->focusedNode() != this && cachedSelectionStart() >= 0)
        return cachedSelectionStart();
    if (!renderer())
        return 0;
    return toRenderTextControl(renderer())->selectionStart();
}

I think this bug is not introduced by 87067, but existed earlier as well.

### in...@chromium.org (2011-06-08)

Probably we should update layout earlier by using textRendererAfterUpdateLayout in HTMLTextFormControlElement::selectionStart, HTMLTextFormControlElement::selectionEnd. In that case, we will bail out early without the use after free.

RenderTextControl* HTMLTextFormControlElement::textRendererAfterUpdateLayout()
{
    if (!isTextFormControl())
        return 0;
    document()->updateLayoutIgnorePendingStylesheets();
    return toRenderTextControl(renderer());
}

int HTMLTextFormControlElement::selectionStart() const
{
    if (!isTextFormControl())
        return 0;
    if (document()->focusedNode() != this && cachedSelectionStart() >= 0)
        return cachedSelectionStart();
    if (!renderer())
        return 0;
    return toRenderTextControl(renderer())->selectionStart();
}

I think this bug is not introduced by 87067, but existed earlier as well.

### in...@chromium.org (2011-06-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-09)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=62329

### in...@chromium.org (2011-06-09)

I can see crash reports on this on Chrome 9, 10, 11 - http://crash/search?query=product%3A%22Chrome%22+%22isSelectableElement%22. Thanks Miaubiz, Kostya and cross_fuzz for catching this.

### in...@chromium.org (2011-06-09)

Fixed in http://trac.webkit.org/changeset/88456

Kostya, if you ever see this kind of stack again, do keep me in loop. I think it should definitely be fixed now.

### sc...@gmail.com (2011-06-14)

Merged to M13: http://trac.webkit.org/changeset/88774
Merged to M12: http://trac.webkit.org/changeset/88776

### sc...@gmail.com (2011-06-16)

@miaubiz: yes, very nice catch. Looks like it's been a stability headache for a while too. Thanks for the repro for this one! Most definitely worth a $1000 Chromium Security Reward.

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

### [Deleted User] (2011-07-01)

[testing Dr. Memory for sanity]
I just got the following report while running the attached repro on r85800:
UNADDRESSABLE ACCESS: 0x257df3a0-0x257df3a1 1 byte(s) within 0x257df3a0-0x257df3a4
 # 1                                                    third_party\webkit\source\javascriptcore\wtf\refptr.h:68
 # 2 WebCore::RenderTextControl::isSelectableElement    third_party\webkit\source\webcore\rendering\rendertextcontrol.cpp:261
 # 3 WebCore::RenderTextControl::indexForVisiblePosition third_party\webkit\source\webcore\rendering\rendertextcontrol.cpp:340
 # 4 WebCore::RenderTextControl::selectionEnd           third_party\webkit\source\webcore\rendering\rendertextcontrol.cpp:216
 # 5 WebCore::HTMLTextFormControlElement::selectionEnd  third_party\webkit\source\webcore\html\htmlformcontrolelement.cpp:677
 # 6 WebCore::HTMLTextFormControlElement::setSelectionStart third_party\webkit\source\webcore\html\htmlformcontrolelement.cpp:631
 # 7 WebCore::HTMLTextAreaElementInternal::selectionStartAttrSetter build\debug\obj\global_intermediate\webcore\bindings\v8htmltextareaelement.cpp:290
 # 8 v8::internal::JSObject::SetPropertyWithCallback    v8\src\objects.cc:1811
 # 9 v8::internal::JSObject::SetProperty                v8\src\objects.cc:2216
 #10 v8::internal::JSObject::SetProperty                v8\src\objects.cc:1768
 #11 v8::internal::StoreIC::Store                       v8\src\ic.cc:1385
 #12 v8::internal::StoreIC_Miss                         v8\src\ic.cc:1739
 #13 v8::internal::Invoke                               v8\src\execution.cc:122
 #14 v8::internal::Execution::Call                      v8\src\execution.cc:158
 #15 v8::Script::Run                                    v8\src\api.cc:1490
 #16 WebCore::V8Proxy::runScript                        third_party\webkit\source\webcore\bindings\v8\v8proxy.cpp:419
 #17 WebCore::V8Proxy::evaluate                         third_party\webkit\source\webcore\bindings\v8\v8proxy.cpp:373
 #18 WebCore::ScriptController::evaluate                third_party\webkit\source\webcore\bindings\v8\scriptcontroller.cpp:235
 #19 WebCore::ScriptElement::executeScript              third_party\webkit\source\webcore\dom\scriptelement.cpp:276
 #20 WebCore::ScriptElement::prepareScript              third_party\webkit\source\webcore\dom\scriptelement.cpp:233
 #21 WebCore::HTMLScriptRunner::runScript               third_party\webkit\source\webcore\html\parser\htmlscriptrunner.cpp:296
 #22 WebCore::HTMLScriptRunner::execute                 third_party\webkit\source\webcore\html\parser\htmlscriptrunner.cpp:170
 #23 WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder third_party\webkit\source\webcore\html\parser\htmldocumentparser.cpp:205
 #24 WebCore::HTMLDocumentParser::canTakeNextToken      third_party\webkit\source\webcore\html\parser\htmldocumentparser.cpp:223
 #25 WebCore::HTMLDocumentParser::pumpTokenizer         third_party\webkit\source\webcore\html\parser\htmldocumentparser.cpp:261
 #26 WebCore::HTMLDocumentParser::resumeParsingAfterYield third_party\webkit\source\webcore\html\parser\htmldocumentparser.cpp:192
 #27 WebCore::HTMLParserScheduler::continueNextChunkTimerFired third_party\webkit\source\webcore\html\parser\htmlparserscheduler.cpp:87
 #28 WebCore::Timer<WebCore::HTMLParserScheduler>::fired third_party\webkit\source\webcore\platform\timer.h:100
 #29 WebCore::ThreadTimers::sharedTimerFiredInternal    third_party\webkit\source\webcore\platform\threadtimers.cpp:112
 #30 WebCore::ThreadTimers::sharedTimerFired            third_party\webkit\source\webcore\platform\threadtimers.cpp:90
 #31 webkit_glue::WebKitClientImpl::DoTimeout           webkit\glue\webkitclient_impl.h:86
 #32 DispatchToMethod<webkit_glue::WebKitClientImpl,void (__thiscall webkit_glue::WebKitClientImpl::*)(void)> base\tuple.h:541
 #33 base::BaseTimer<webkit_glue::WebKitClientImpl,0>::TimerTask::Run base\timer.h:161
 #34 `anonymous namespace'::TaskClosureAdapter::Run     base\message_loop.cc:101

### [Deleted User] (2011-07-01)

additional info: my drmemory report humanizer script accidentally stripped the following info:
Error #1: UNADDRESSABLE ACCESS: 0x257df3a0-0x257df3a1 1 byte(s) within 0x257df3a0-0x257df3a4
Note: prev lower malloc:  0x257df270-0x257df304
 # 1 chrome.dll!WTF::RefPtr<WebCore::TextControlInnerTextElement>::operator! third_party\webkit\source\javascriptcore\wtf\refptr.h:68

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### [Deleted User] (2011-07-27)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/85418?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/84852]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091700)*
