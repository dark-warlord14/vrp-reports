# Security: UAF in WorkerThreadableLoader in Blink

| Field | Value |
|-------|-------|
| **Issue ID** | [40086589](https://issues.chromium.org/issues/40086589) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM, Blink>Loader |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ng...@tresorit.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2017-01-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a UAF bug in WorkerThreadableLoader. It contains a raw pointer to a ThreadableLoaderClient (in the reproduction case it is an XMLHttpRequest),  

which can be freed before freeing the WorkerThreadableLoader that tries use it.  

I can only trigger it with version 57 (dev), I couldn't reproduce the crash on 55 (stable) and 56 (beta) but I did not try to debug what happens with those.

I have attached a patch that prints info with LOG(ERROR) in ~XMLHttpRequest() and WorkerThreadableLoader::didReceiveData(), this helps to see what the problem is.

My reproduction case is not 100% reliable. When it does not crash it shows something like this:  

[1:1:0121/000142.666580:ERROR:WorkerThreadableLoader.cpp(539)] mainThreadDidReceiveData() wtl=0x7b8e8a21c08  

[1:11:0121/000142.666543:ERROR:WorkerThreadableLoader.cpp(353)] didReceiveData() wtl=0x7b8e8a21c08 xhr=0x1c19d4ac1878  

[1:11:0121/000142.666681:ERROR:WorkerThreadableLoader.cpp(353)] didReceiveData() wtl=0x7b8e8a21c08 xhr=0x1c19d4ac1878  

[1:11:0121/000142.666796:ERROR:WorkerThreadableLoader.cpp(353)] didReceiveData() wtl=0x7b8e8a21c08 xhr=0x1c19d4ac1878  

[1:11:0121/000142.684346:ERROR:XMLHttpRequest.cpp(253)] ~XMLHttpRequest() xhr=0x1c19d4ac1878  

[1:11:0121/000142.684545:ERROR:WorkerThreadableLoader.cpp(219)] ~WorkerThreadableLoader() wtl=0x7b8e8a21c08  

[1:1:0121/000142.692910:ERROR:WorkerThreadableLoader.cpp(539)] mainThreadDidReceiveData() wtl=0

When a crash occurs then it shows something like this:  

[1:1:0121/000136.106021:ERROR:WorkerThreadableLoader.cpp(539)] mainThreadDidReceiveData() wtl=0x10905c881c08  

[1:1:0121/000136.106133:ERROR:WorkerThreadableLoader.cpp(539)] mainThreadDidReceiveData() wtl=0x10905c881c08  

[1:11:0121/000136.107999:ERROR:XMLHttpRequest.cpp(253)] ~XMLHttpRequest() xhr=0xe2c48ec1878  

[1:11:0121/000136.108074:ERROR:WorkerThreadableLoader.cpp(353)] didReceiveData() wtl=0x10905c881c08 xhr=0xe2c48ec1878

It seems that XMLHttpRequest and WorkerThreadableLoader are both destructed during the same GC sweep but in the wrong order.  

If there is a didReceiveData() call between the two destructors then there is a crash.

**VERSION**

Chrome Version: 57 (dev)  

Operating System: Reproduced on Linux x64 and Windows x86 (all OSes should be affected)

**REPRODUCTION CASE**

1. Load the attached html page.
2. Trigger a GC sweep (DevConsole -> Timeline/Memory -> Trash icon)  
   
   3.a. Aw, Snap!  
   
   3.b. If it didn't crash then refresh the page and go to Step 2.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab  

Crash State:

Received signal 11 SEGV\_ACCERR 25fe8a9a1878  

#0 0x55d740a2ec64 base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#1 0x7f7846fe5600 <unknown>  

#2 0x55d742f79217 blink::WorkerThreadableLoader::didReceiveData()  

#3 0x55d742f80749 \_ZN4base8internal7InvokerINS0\_9BindStateIMN5blink22WorkerThreadableLoaderEFvSt10unique\_ptrIN3WTF6VectorIcLm0ENS6\_18PartitionAllocatorEEESt14default\_deleteIS9\_EEEJNS3\_21CrossThreadPersistentIS4\_EENS6\_13PassedWrapperISC\_EEEEEFvvEE3RunEPNS0\_13BindStateBaseE  

#4 0x55d742736ea3 blink::internal::CallClosureTask<>::performTask()  

#5 0x55d7430cc0a3 blink::WorkerThread::performTaskOnWorkerThread()  

#6 0x55d7430cd8c6 \_ZN4base8internal7InvokerINS0\_9BindStateIMN5blink12WorkerThreadEFvSt10unique\_ptrINS3\_20ExecutionContextTaskESt14default\_deleteIS6\_EEbEJN3WTF17UnretainedWrapperIS4\_LNSC\_22FunctionThreadAffinityE0EEENSC\_13PassedWrapperIS9\_EEbEEEFvvEE3RunEPNS0\_13BindStateBaseE  

#7 0x55d742675ac7 \_ZN4base8internal7InvokerINS0\_9BindStateIPFvSt10unique\_ptrIN3WTF8FunctionIFvvELNS4\_22FunctionThreadAffinityE0EEESt14default\_deleteIS8\_EEEJNS0\_13PassedWrapperISB\_EEEEES6\_E3RunEPNS0\_13BindStateBaseE  

#8 0x55d740ab052e base::debug::TaskAnnotator::RunTask()  

#9 0x55d7426b5022 blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue()  

#10 0x55d7426b3c84 blink::scheduler::TaskQueueManager::DoWork()  

#11 0x55d740ab052e base::debug::TaskAnnotator::RunTask()  

#12 0x55d740a4746d base::MessageLoop::RunTask()  

#13 0x55d740a47ba5 base::MessageLoop::DoWork()  

#14 0x55d740a48b8a base::MessagePumpDefault::Run()  

#15 0x55d740a47197 base::MessageLoop::RunHandler()  

#16 0x55d740a6512e base::RunLoop::Run()  

#17 0x55d740a86257 base::Thread::ThreadMain()  

#18 0x55d740a81f93 base::(anonymous namespace)::ThreadFunc()  

#19 0x7f7846fdb550 <unknown>  

#20 0x7f784079b5fd clone  

r8: 00007f7840a4e6f0 r9: 00007f7832551700 r10: 00007f7840a4e6f0 r11: 0000000000000000  

r12: 00007f78325500a8 r13: 00007f7832550640 r14: 00007f7832550258 r15: 00007f78325500a0  

di: 000025fe8a9a1878 si: 0000000000000000 bp: 0000092aae7c58c0 bx: 00001e624ec81c08  

dx: 0000000000000932 ax: c69fce12d598e700 cx: 0000000000000002 sp: 00007f78325500a0  

ip: 000055d742f79217 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004  

trp: 000000000000000e msk: 0000000000000000 cr2: 000025fe8a9a1878  

[end of stack trace]

## Attachments

- [debuglog.patch](attachments/debuglog.patch) (application/octet-stream, 1.9 KB)
- [xhr_uaf.html](attachments/xhr_uaf.html) (text/plain, 343 B)
- [xhrgc.html](attachments/xhrgc.html) (text/plain, 410 B)
- [xhrgc2.html](attachments/xhrgc2.html) (text/plain, 513 B)
- xhrgc3.html (text/plain, 395 B)

## Timeline

### cl...@chromium.org (2017-01-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6023665130143744

### es...@chromium.org (2017-01-23)

Note: I couldn't reproduce a crash on 58.0.2989.0 canary on Mac OS X, but we'll see if Clusterfuzz can.

### es...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>Loader]

### ng...@tresorit.com (2017-01-23)

Git bisect showed that the crash is reproducible since turning on TraceWrappables in https://codereview.chromium.org/2592713002
I will try it on latest canary too.

### ng...@tresorit.com (2017-01-23)

The crash cannot be reproduced in 58 because https://codereview.chromium.org/2649513002 fixed it.
This commit is not included in version 57 though so I think this is a valid vulnerability for the current Dev channel (57).
It might be possible to reproduce it with another ThreadableLoaderClient, not XMLHttpRequest.
Probably the best would be to make ThreadableLoaderClient inherit from GarbageCollectedMixin and WorkerThreadableLoader should have a Member or WeakMember to it instead of a raw pointer.

### ng...@tresorit.com (2017-01-23)

Can you please CC yhirano@ or sof@ ? They were discussing something similar in the CL that fixed this a few days ago.

I have attached a new reproduction case which is probably more useful for ClusterFuzz.

The crash can be triggered with either:
1. run "./chrome xhrgc.html"; manually trigger the gc via devconsole
2. run "./chrome --js-flags=--expose-gc xhrgc.html"
3. run "./content_shell --run-layout-test xhrgc.html"

### lg...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-01-24)

yhirano, could you please take a look at this? See https://crbug.com/chromium/683406#c5: sounds like it is fixed by your CL https://codereview.chromium.org/2649513002, but maybe that needs to be merged to 57.

### ng...@tresorit.com (2017-01-24)

#9: There are multiple implementations for ThreadableLoaderClient (not just XMLHttpRequest), I think this issue could be reproduced with the others as well.

### [Deleted User] (2017-01-24)

Confirmed that https://codereview.chromium.org/2649513002 addresses, yhirano@ will no doubt request a M57 merge at first available opportunity.

A real fine bug report & test, btw - we should add it. https://crbug.com/chromium/667254 (which might not be visible) was about locating the loader client that didn't cleanly detach from its loader. XHR was the one culprit identified.

### yh...@chromium.org (2017-01-25)

The problem happens because in some cases (I don't know exactly what they are though), ContextLifecycleObserver::contextDestroyed is not called. Some ThreadableLoaderClient expects it to be called (in combination with ActiveScriptWrappable::hasPendingActivity). I believe that the expectation should be valid and there is an infra-issue. +haraken@.

[Monorail components: Blink>DOM]

### sh...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-25)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-01-25)

[Bulk edit]

A friendly reminder that M57 Beta launch is coming soon on February 2nd (in a week)! Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix and get it merged into the release branch (2987) ASAP so it gets enough baking time in Dev (before Beta promotion). Thank you!

### [Deleted User] (2017-01-26)

See https://bugs.chromium.org/p/chromium/issues/detail?id=667254#c48 for the M57 merge.

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### ng...@tresorit.com (2017-01-26)

There is another bug regarding this same issue.
I do not want to file another report until this is visible to the public.

Sometimes if an XMLHttpRequest is started from a worker, it is prematurely GC'd before it can finish.
If you run "./content_shell --run-layout-test xhrgc2.html" with my now attached file then it should report that there is a text field "error", but it does not because GC destroys blink::XMLHttpRequest and it has a prefinalizer that cancels the loader (before yhirano's patch it did not have a prefinalizer but the WorkerThreadable loader was GC'd as well, and when it did not crash it stopped the downlaod).

This is a regression in 57. Before 57 the TraceWrappables runtime feature was disabled (https://crrev.com/2592713002) and somehow that makes it work. I checked what happens if I remove the "status=stable" part from the TraceWrappables line in //third_party/WebKit/Source/platform/RuntimeEnabledFeatures.in and it works correctly again. (running the layout test reports the text field "error")
I'm not familiar with Blink internals, I do not know what's supposed to keep the XMLHttpRequest alive, but something really should.

This bug kind of makes XMLHttpRequests unusable from workers so I think it will affect lots of projects.
(For example https://web.tresorit.com can not download files at all because of this bug).

Please fix this issue too or disable TraceWrappables as a temporary workaround.

### [Deleted User] (2017-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2017-01-26)

Confirmed #19, but this is a separate (non-security) issue. The XHR object signals that it must be kept alive (hasPendingActivity() returns |true|), but the v8 GC fails to trace through its wrapper to mark and keep the XHR object alive.

Handled as-wanted if the test snippet is instead run within the context of a document.

### ml...@chromium.org (2017-01-26)

If it's prematurely collected it probably has to do with pending activities. I think wrapper tracing by now uses a different notion of active scruptwrappable (see MajorGCWrapperVisitor before I deleted it). 

I am a bit low on cycles this week (traveling + talk) but will have a look early next week if the issue still persists.


### ml...@chromium.org (2017-01-26)

Thanks sigbjorn for investigating! That's what I thought. 

(Written at 39k feet altitude :))

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Removing ReleaseBlock-Beta per #17

### [Deleted User] (2017-01-27)

#23: as far as i could gather, the weak that DOMWrapperMap::set() created in a worker setting, wasn't being retained when the associated ScriptWrappable::hasPendingActivity() returned |true|. Which precipitated it not being traced through later on.

### ml...@chromium.org (2017-01-27)

Yeah, this is related to wrapper worlds.

As far as I can see the bug is an artifact from the prototype. We marked only the main world wrapper, where we actually should have put it onto the marking deque, effectively triggering processing in all worlds.

I am about to verify that theory.

### ml...@chromium.org (2017-01-27)

Alright, the problem seems to be more subtle.

Workers are not running on the main thread and are not being stored in the main world wrapper. Since we currently check for main thread when marking wrappers in all worlds, we will never mark through the DOMWrapperMap in workers.

Thinking of a proper fix now.

### ha...@chromium.org (2017-01-27)

FWIW, workers don't have DOM trees, so we won't need to support incremental tracing.


### ml...@chromium.org (2017-01-27)

#29: True, but we can just reuse the existing infra.

The problem is that the worker world is not stored anywhere. So we only use the main world wrapper only for the main world and not workers. Worker worlds are also not part of the isolated world map, so we cannot reach it from there.

### ml...@chromium.org (2017-01-27)

We could (a) make WorkerWorld part of the isolatedWorldsMap and trace (b) all isolated worlds in markWrappersInAllWorlds. Locally, this fixes the issue.

haraken/jochen: Any reason we wouldn't be allowed to do (a) ?

### ha...@chromium.org (2017-01-28)

Can we create a separate map for worker worlds (e.g., workerWorldsMap)?

Conceptually:

- The main thread has its main world (WindowProxy::m_world) and isolated worlds.
- A worker thread has its own world (WorkerOrWorkletScriptController::m_world).

In that sense, it looks a bit strange to classify worker's world as isolated worlds.


### ha...@chromium.org (2017-01-28)

Sorry I'm confused.

Why do we need to visit wrappers in the worker world when we run a GC on the main thread? V8 heaps are completely separated per thread, so we won't need to worry about wrappers in a worker (or the main thread) when running a GC on the main thread (or a worker).


### jo...@chromium.org (2017-01-28)

as far as I understand the bug here is that we're not visiting those wrappers when doing a GC in the worker because of the incorrect assumption that wrappres in the worker thread are stored in ScriptWrappables

### ha...@chromium.org (2017-01-28)

Ah, makes sense. Then can we visit WorkerOrWorkletScriptController::m_world when we run a GC on a worker thread?


### jo...@chromium.org (2017-01-28)

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/bindings/core/v8/DOMWrapperWorld.cpp?rcl=1485491011&l=137 doesn't have access to that, but that should be easy to fix

### [Deleted User] (2017-01-29)

Really don't want to pre-empt mlippautz@'s work, but if it helps getting a change in sooner during the upcoming busy week, https://codereview.chromium.org/2663643002/ adds the worker special case.

### [Deleted User] (2017-01-29)

https://crbug.com/chromium/686563 handles the fix for the above.

### ng...@tresorit.com (2017-01-30)

The current CL (patchset 8) does solve the issue when I call "self.gc()" from the worker.
But the issue still persists if I click on the Trash icon in the DevConsole.

You can reproduce this by running "./chrome xhrgc3.html" with my now attached file and then manually triggering the GC from the DevConsole before the download finishes.

I have seen some cases where an automatically triggered GC kills the XHR but I cannot easily reproduce that.

### ml...@chromium.org (2017-01-30)

Thanks for all your efforts. Will take a look today.

### yh...@chromium.org (2017-01-30)

[Empty comment from Monorail migration]

### ml...@chromium.org (2017-01-30)

The crasher and security issue here has been fixed. 

Lets move the discussion about correctness and the corresponding fix to https://crbug.com/chromium/686563. What is left is properly tracing through wrappers in workers which is tracked by the other issue.

### sh...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### ng...@tresorit.com (2017-01-31)

Does this issue qualify for the reward program?
If so, please add the label reward-topanel.
Or is it only a duplicate of https://crbug.com/chromium/667254?
(I have no permission to see that bug, so I cannot tell for sure.)
Thanks!

### ml...@chromium.org (2017-02-01)

Given the repro steps and the useful test cases, I am adding the label for now. If somebody disagrees, please take it off.

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-04)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-06)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Monday (02/06/) so we can pick it up for next Beta release. Thank you.

### ng...@tresorit.com (2017-02-06)

govind@ Both fixes are already merged into 2987
This is the fix for the UAF: https://crrev.com/995de01d
This is the fix for the non-security part: https://crrev.com/730c14f1

### go...@chromium.org (2017-02-06)

[Comment Deleted]

### go...@chromium.org (2017-02-06)

Per https://crbug.com/chromium/683406#c49, both fixes are merged to M57.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Congratulations! The panel decided to award $3,000 in this case.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-09)

This issue was migrated from crbug.com/chromium/683406?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Blink>Loader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086589)*
