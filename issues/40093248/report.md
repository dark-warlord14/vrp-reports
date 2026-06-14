# [LangFuzz] Crash at RootMarkingVisitor::VisitPointers (32 bit)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093248](https://issues.chromium.org/issues/40093248) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2011-07-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 15.0.838.0 and V8 shell at function "RootMarkingVisitor::VisitPointers". Although this crashes at 0x0 (-0x1(%eax) where %eax is 0x1), this could still be problematic as it is inside GC code and I don't really know what else could possibly happen here.

**VERSION**  

Chrome Version: 15.0.838.0 (Developer Build 94616 Linux) dev  

Operating System: Ubuntu 11.04, tested on 32 bit

**REPRODUCTION CASE**  

var i = 500000  

var a = new Array(i)  

for (var j = 0; j < i; j++) { var o = 1; o.x = 42; delete o.x; a[j] = o; }

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x00ffe522 in map\_word (this=0xbfffd3e4, start=0xbfffd6ec, end=0xbfffd704)  

at v8/src/objects-inl.h:1228  

1228 v8/src/objects-inl.h: No such file or directory.  

in v8/src/objects-inl.h  

(gdb) bt  

#0 0x00ffe522 in map\_word (this=0xbfffd3e4, start=0xbfffd6ec, end=0xbfffd704)  

at v8/src/objects-inl.h:1228  

#1 ShortCircuitConsString (this=0xbfffd3e4, start=0xbfffd6ec, end=0xbfffd704)  

at v8/src/mark-compact.cc:354  

#2 MarkObjectByPointer (this=0xbfffd3e4, start=0xbfffd6ec, end=0xbfffd704)  

at v8/src/mark-compact.cc:1052  

#3 v8::internal::RootMarkingVisitor::VisitPointers (this=0xbfffd3e4,  

start=0xbfffd6ec, end=0xbfffd704) at v8/src/mark-compact.cc:1044  

#4 0x00f7789b in v8::internal::StandardFrame::IterateExpressions (  

this=0xbfffd244, v=0xbfffd3e4) at v8/src/frames.cc:1122  

#5 0x00f77953 in v8::internal::JavaScriptFrame::Iterate (this=0xbfffd244,  

v=0xbfffd3e4) at v8/src/frames.cc:1127  

#6 0x00fdb925 in v8::internal::Isolate::Iterate (this=0x3581000,  

v=0xbfffd3e4, thread=0x358150c) at v8/src/isolate.cc:471  

#7 0x00fdb9b1 in v8::internal::Isolate::Iterate (this=0x3581000, v=0xbfffd3e4)  

at v8/src/isolate.cc:478  

#8 0x00f9429b in v8::internal::Heap::IterateStrongRoots (this=0x358104c,  

v=0xbfffd3e4, mode=v8::internal::VISIT\_ONLY\_STRONG) at v8/src/heap.cc:4693  

#9 0x01003131 in v8::internal::MarkCompactCollector::MarkRoots (  

this=0x358147c, visitor=0xbfffd3e4) at v8/src/mark-compact.cc:1283  

#10 0x01003645 in v8::internal::MarkCompactCollector::MarkLiveObjects (  

this=0x358147c) at v8/src/mark-compact.cc:1477  

#11 0x010056cb in v8::internal::MarkCompactCollector::CollectGarbage (  

this=0x358147c) at v8/src/mark-compact.cc:79  

#12 0x00f95335 in v8::internal::Heap::MarkCompact (this=0x358104c,  

tracer=0xbfffd520) at v8/src/heap.cc:822  

#13 0x00f9575c in v8::internal::Heap::PerformGarbageCollection (  

this=0x358104c, collector=v8::internal::MARK\_COMPACTOR, tracer=0xbfffd520)  

at v8/src/heap.cc:731  

#14 0x00f9701e in v8::internal::Heap::CollectGarbage (this=0x358104c,  

space=v8::internal::NEW\_SPACE, collector=v8::internal::MARK\_COMPACTOR)  

at v8/src/heap.cc:508  

#15 0x00f6f413 in CollectGarbage (this=0x3581000, constructor=...,  

pretenure=v8::internal::NOT\_TENURED) at v8/src/heap-inl.h:427  

#16 v8::internal::Factory::NewJSObject (this=0x3581000, constructor=...,  

pretenure=v8::internal::NOT\_TENURED) at v8/src/factory.cc:844  

#17 0x01061fc8 in v8::internal::Runtime\_NewObject (args=..., isolate=0x3581000)  

at v8/src/runtime.cc:7809  

#18 0x2fe8c0b6 in ?? ()  

#19 0x2fe92bab in ?? ()  

#20 0x2fe9af5c in ?? ()  

#21 0x2fe99bb1 in ?? ()  

#22 0x2fea1d69 in ?? ()  

#23 0x2fe9f4fa in ?? ()  

#24 0x2fe8fdeb in ?? ()  

#25 0x00f63433 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffd94f)  

at v8/src/execution.cc:121  

#26 0x00f63b15 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffd94f) at v8/src/execution.cc:158  

#27 0x00f2eff6 in v8::Script::Run (this=0x37220d4) at v8/src/api.cc:1555  

#28 0x017c7dd8 in WebCore::V8Proxy::runScript (this=0x35ed480, script=...,  

isInlineCode=false)

(gdb) info registers  

eax 0x1 1  

ecx 0x308580a1 814055585  

edx 0x0 0  

ebx 0x347de8c 55041676  

esp 0xbfffd110 0xbfffd110  

ebp 0x1 0x1  

esi 0x308580a0 814055584  

edi 0xbfffd6f8 -1073752328  

eip 0xffe522 0xffe522 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+82>  

eflags 0x210246 [ PF ZF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

(gdb) x /4i $pc  

=> 0xffe522 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+82>: mov -0x1(%eax),%esi  

0xffe525 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+85>: mov %esi,%ecx  

0xffe527 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+87>: or $0x1,%ecx  

0xffe52a <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+90>: movzbl 0x7(%ecx),%edx

## Timeline

### js...@chromium.org (2011-07-30)

@ager, @sgjesse - Could one of you direct this to the appropriate person on the v8 team?

### sc...@gmail.com (2011-08-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-08-02)

[Empty comment from Monorail migration]

### ve...@chromium.org (2011-08-02)

Fixed in v8:r8781

For security evaluation: bug allows to construct arbitrary 31-bit value in the slot which will be treated as a valid object pointer by GC or generated code.

### sc...@gmail.com (2011-08-02)

Definitely "High". Thanks.

### sc...@gmail.com (2011-08-24)

Nice catch, nice repro. Definitely $1000

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

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/91013?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093248)*
