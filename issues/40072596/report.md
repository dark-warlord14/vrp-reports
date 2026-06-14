# [LangFuzz] Crash at v8::internal::MarkCompactCollector::EvacuateNewSpace with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40072596](https://issues.chromium.org/issues/40072596) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2012-09-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes d8 shell (trunk version as in Chrome 23.0.1262.0) in function v8::internal::MarkCompactCollector::EvacuateNewSpace with an invalid read from a random address. As the test requires gc() to reproduce, I only tested this on the v8-trunk shell (version as included in current Chrome dev).

**VERSION**  

Chrome Version: 23.0.1262.0 dev  

Operating System: Ubuntu 12.04 64 bit

**REPRODUCTION CASE**  

Object.prototype.**defineSetter**('x', function(value) { result\_x = value; });  

function setx() {  

x = 100000;  

}  

setx();  

**defineSetter**('x', function() {});  

var keys = Object.keys( 3 && this || this ? this : this >>= "x");  

gc();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash state:

==8041== Invalid read of size 8  

==8041== at 0x5550B0: v8::internal::MarkCompactCollector::EvacuateNewSpace() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x555EBD: v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x557250: v8::internal::MarkCompactCollector::SweepSpaces() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x55FEF1: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x4B9639: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x4B9E83: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x4BA6CA: v8::internal::Heap::CollectAllGarbage(int, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x4743BE: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x43EF97: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==8041== by 0x125452006361: ???  

==8041== by 0x12545203FB4F: ???  

==8041== by 0x12545200CFA6: ???  

==8041== Address 0xc0fd7794360 is not stack'd, malloc'd or (recently) free'd

## Timeline

### in...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### ms...@chromium.org (2012-09-12)

I can repro this, will take a look.

### ms...@chromium.org (2012-09-12)

Related to Toon's recent changes, handing off to him.

### in...@chromium.org (2012-09-12)

I am assuming m23 then, no merges required, right ?

### ve...@chromium.org (2012-09-12)

No merges are required, it's in there since 3.13.6.

### in...@chromium.org (2012-09-12)

Sounds good, then the mstones labels are right.

### ve...@chromium.org (2012-09-13)

Fixed in v8:12494.

### sc...@gmail.com (2012-09-13)

@verwaest @decoder.oh: how serious is this? A bad read "of size 8" makes me think it could be the use of an invalid pointer, which would be more serious?

### de...@googlemail.com (2012-09-13)

@scarybeasts: Since https://crbug.com/chromium/148373 is a duplicate of this, the worst that can happen here seems to be a SIGILL (see the other bug for possible other ways to crash here), so this could mean code execution.

### ve...@chromium.org (2012-09-13)

The bug overwrites the length of an array with a pointer in CopyEnumKeysTo; thus an arbitrarily large value. If nothing wrongly happens earlier (eg in the RightTrimFixedArray method); a subsequent GC will most likely crash.

I don't immediately see an easy way how this can be exploited especially since the value that's written over the length has to be the (tagged) address of a symbol. However, the heap does get corrupted by the pointer, or by a subsequent GC, which might potentially lead to unforeseen code execution.

I don't exactly know what causes the SIGILL in the other bug, but afaict it is also failing while performing GC.

### sc...@gmail.com (2012-09-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

@decoder.oh: another nice regression catch! $1000

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

This issue was migrated from crbug.com/chromium/148376?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail mergedwith: crbug.com/chromium/148373]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072596)*
