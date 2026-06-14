# Security: UNKNOWN in v8::internal::GlobalHandles::Node::Release

| Field | Value |
|-------|-------|
| **Issue ID** | [40085589](https://issues.chromium.org/issues/40085589) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-10-04 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 53.0.2785.116 stable  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Log into Facebook
2. Navigate to <https://www.facebook.com/search/top/?q=%D8%A7%D9%84%D8%B4%D8%B1%D8%B7%D9%8A%D8%A9+%D8%A7%D9%84%D9%85%D8%BA%D8%B1%D8%A8%D9%8A%D8%A9+%D8%A7%D9%84%D8%AA%D9%8A+%D8%A3%D8%A8%D9%87%D8%B1%D8%AA+%D8%AC%D9%85%D9%8A%D8%B9+%D8%A7%D9%84%D9%85%D8%BA%D8%A7%D8%B1%D8%A8%D8%A9>
3. Click on the first result to open a popup window and wait until the page is ready
4. Close that tab >> Crash!

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: 878613ed00000000

rax=000007fed2a1b79c rbx=00000000045ea7e0 rcx=92085f0200010463  

rdx=00000000002e7f90 rsi=0000000015d273e0 rdi=00000000001cde40  

rip=000007fed0adff0c rsp=00000000001cddc0 rbp=00000000001ce0a0  

r8=0000000000000036 r9=006d070d01ce0063 r10=0000000078c7e20e  

r11=00000000001cde90 r12=0000000000000000 r13=00000000001ce340  

r14=000007fed300f970 r15=00000000002caca0  

iopl=0 nv up ei pl nz na po nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010206  

\*\*\* WARNING: Unable to verify checksum for chrome\_child.dll  

chrome\_child!v8::internal::GlobalHandles::Node::Release+0x14:  

000007fe`d0adff0c 80610bf0 and byte ptr [rcx+0Bh],0F0h ds:92085f02`0001046e=??  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

Child-SP RetAddr Call Site  

00000000`001cddc0 000007fe`d2a1b7c2 chrome\_child!v8::internal::GlobalHandles::Node::Release+0x14 [c:\b\build\slave\win64-pgo\build\src\v8\src\global-handles.cc @ 118]  

00000000`001cddf0 000007fe`d0b2b4cc chrome\_child!blink::InspectedContext::weakCallback+0x26 [c:\b\build\slave\win64-pgo\build\src\third\_party\webkit\source\platform\v8\_inspector\inspectedcontext.cpp @ 20]  

00000000`001cde20 000007fe`d0b2b310 chrome\_child!v8::internal::GlobalHandles::PendingPhantomCallback::Invoke+0x40 [c:\b\build\slave\win64-pgo\build\src\v8\src\global-handles.cc @ 1097]  

00000000`001cde80 000007fe`d0ce6ed7 chrome\_child!v8::internal::GlobalHandles::InvokeSecondPassPhantomCallbacks+0x64 [c:\b\build\slave\win64-pgo\build\src\v8\src\global-handles.cc @ 949]  

00000000`001cdee0 000007fe`d0b4f9d9 chrome\_child!v8::internal::GlobalHandles::PendingPhantomCallbacksSecondPassTask::RunInternal+0x53 [c:\b\build\slave\win64-pgo\build\src\v8\src\global-handles.cc @ 562]  

00000000`001cdf70 000007fe`d0cae6bd chrome\_child!v8::internal::CancelableTask::Run+0x1d [c:\b\build\slave\win64-pgo\build\src\v8\src\cancelable-task.h @ 132]  

00000000`001cdfa0 000007fe`d0caffb1 chrome\_child!base::debug::TaskAnnotator::RunTask+0x19d [c:\b\build\slave\win64-pgo\build\src\base\debug\task\_annotator.cc @ 53]  

00000000`001ce120 000007fe`d0cace0e chrome\_child!scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x149 [c:\b\build\slave\win64-pgo\build\src\components\scheduler\base\task\_queue\_manager.cc @ 295]  

00000000`001ce2b0 000007fe`d116d99a chrome\_child!scheduler::TaskQueueManager::DoWork+0xf2 [c:\b\build\slave\win64-pgo\build\src\components\scheduler\base\task\_queue\_manager.cc @ 203]  

00000000`001ce700 000007fe`d0cae6bd chrome\_child!base::internal::Invoker<base::internal::BindState<base::internal::RunnableAdapter<void (\_\_cdecl scheduler::TaskQueueManager::\*)(base::TimeTicks,bool) \_\_ptr64>,base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool>,void \_\_cdecl(void)>::Run+0x2e [c:\b\build\slave\win64-pgo\build\src\base\bind\_internal.h @ 346]  

00000000`001ce730 000007fe`d0cada9e chrome\_child!base::debug::TaskAnnotator::RunTask+0x19d [c:\b\build\slave\win64-pgo\build\src\base\debug\task\_annotator.cc @ 53]  

00000000`001ce8b0 000007fe`d0cade41 chrome\_child!base::MessageLoop::RunTask+0x96 [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 494]  

00000000`001ce990 000007fe`d0cadb99 chrome\_child!base::MessageLoop::DoWork+0x1c9 [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 625]  

00000000`001cec40 000007fe`d0f66492 chrome\_child!base::MessagePumpDefault::Run+0x1d [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_pump\_default.cc @ 36]  

00000000`001cec90 000007fe`d0f66421 chrome\_child!base::MessageLoop::RunHandler+0x3a [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 458]  

00000000`001ced20 000007fe`d1061795 chrome\_child!base::RunLoop::Run+0x79 [c:\b\build\slave\win64-pgo\build\src\base\run\_loop.cc @ 36]  

00000000`001ced70 000007fe`d117584f chrome\_child!base::MessageLoop::Run+0x1d [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 296]  

00000000`001cedd0 000007fe`d106001c chrome\_child!content::RendererMain+0x1ef [c:\b\build\slave\win64-pgo\build\src\content\renderer\renderer\_main.cc @ 198]  

00000000`001cef80 000007fe`d0e98d1a chrome\_child!content::RunNamedProcessTypeMain+0xb4 [c:\b\build\slave\win64-pgo\build\src\content\app\content\_main\_runner.cc @ 435]  

00000000`001cf0e0 000007fe`d0e98c49 chrome\_child!content::ContentMainRunnerImpl::Run+0xae [c:\b\build\slave\win64-pgo\build\src\content\app\content\_main\_runner.cc @ 785]

## Attachments

- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 1.2 MB)
- [ASan-output.txt](attachments/ASan-output.txt) (text/plain, 8.2 KB)

## Timeline

### ts...@chromium.org (2016-10-04)

Possibly related to 646810.  Haraken, can you tell if this is the same issue?



### ha...@chromium.org (2016-10-05)

jochen@: This looks like an issue of first/second weak callbacks used in InspectedContext. Would you find an owner for this?

https://cs.chromium.org/chromium/src/v8/src/inspector/inspected-context.cc?q=inspectedcontext&sq=package:chromium&dr=C&l=17

(Maybe we can remove the second weak callbacks -- Blink has already removed them entirely.)


### ts...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### jo...@chromium.org (2016-10-06)

happening during the second callback. I wonder why the if (context->m_context.IsEmpty()) check returns false? We could just split up the callback in two differnt functions

### ch...@gmail.com (2016-10-06)

Able to reproduce this issue under ASan-Windows bluid. This is a use-after-free vulnerability.

### ts...@chromium.org (2016-10-06)

Khalil, could you symbolize the asan trace for us?

### ch...@gmail.com (2016-10-06)

I couldn't repro this crash on Linux.

### dg...@chromium.org (2016-10-06)

re https://crbug.com/chromium/652548#c2: what's the alternative for second pass callbacks used in blink? We would definitely switch if possible.

### dg...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-10-12)

[Comment Deleted]

### ko...@chromium.org (2016-10-12)

[Comment Deleted]

### ko...@chromium.org (2016-10-12)

I prepared CL [1] that removes second pass callback from inspected context - it was added to provide additionally guarantee that we remove InspectedContext and related objects when context is gone. But we have another mechanism to remove it and as long as inspector client call contextDestroyed for every contextCreated - nothing will be leaked.

[1] https://codereview.chromium.org/2413583002/

### bu...@chromium.org (2016-10-13)

[Comment Deleted]

### bu...@chromium.org (2016-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2082afcf3c8afe5002689ff3208d546f5775fb9a

commit 2082afcf3c8afe5002689ff3208d546f5775fb9a
Author: kozyatinskiy <kozyatinskiy@chromium.org>
Date: Fri Oct 14 01:59:36 2016

[inspector] added check that context always survives inspected context

Inspected context is created in V8InspectorImpl::contextCreated method and destroyed in V8InspectorImpl::contextDestroyed.
Both methods takes valid v8::Local<v8::Context> handle to the same context, it means that context is created before InspectedContext constructor and is always destroyed after InspectedContext destructor therefore context weak callback in inspected context should be never called.
It's possible only if inspector client doesn't call contextDestroyed which is considered an error.

Therefore CHECK(false) is added into context weak callback to be sure that v8::Context always survives inspected context.

BUG=chromium:652548
R=dgozman@chromium.org

Review-Url: https://codereview.chromium.org/2413583002
Cr-Commit-Position: refs/heads/master@{#40290}

[modify] https://crrev.com/2082afcf3c8afe5002689ff3208d546f5775fb9a/src/inspector/inspected-context.cc
[modify] https://crrev.com/2082afcf3c8afe5002689ff3208d546f5775fb9a/src/inspector/inspected-context.h


### ch...@gmail.com (2016-10-14)

Verified on 56.0.2891.0 (Windows). The crash is no longer seen.

### ko...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-17)

Merge-Triage as we'll want to get it merged into M55 once it's had bake time.

### sh...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-21)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### ko...@chromium.org (2016-10-24)

I'm not sure that we need to merge this change - it just make crash easier to detect by replacing SecondPassCallback with explicit CHECK(false).
But this check allows me to find root of issue: crbug.com/656626, and I think we need merge fix of it instead.

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

$500 for this bug.  We classified this as a low quality report (see https://www.google.com/about/appsecurity/chrome-rewards/index.html#rewards).  Would have been great to have had a symbolized memory tool output and a clean repro.  Cheers!

### ch...@gmail.com (2016-10-24)

Hmm... this qualified only for 500$ because I didn't provide the asan trace (symbolized). Anyway thanks for that!

Next time I'll pay attention for that.

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-25)

Looks like 656626 is already in M55, so removing labels from this bug.

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/652548?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085589)*
