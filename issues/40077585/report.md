# [LangFuzz] Crash at v8::internal::HeapObject::Size() on 64 bit with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40077585](https://issues.chromium.org/issues/40077585) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2013-05-22 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:23.0) Gecko/20130520 Firefox/23.0

Steps to reproduce the problem:
1. Run this JS code in the shell or browser:

for (var i = 0; i < 100000; i++) {
  Error("", "",  [], [], [,,[],,], toString);
}

Note: In the browser I had to reload the page a few times to get the crash.

2. Observe Crash

What is the expected behavior?
No Crash.

What went wrong?
Browser tab crashes:

Program received signal SIGSEGV, Segmentation fault.
0x0000555556d82114 in ?? ()
(gdb) bt
#0  0x0000555556d82114 in ?? ()
[...]
#29 0x0000000000000000 in ?? ()
(gdb) x /i $pc
=> 0x555556d82114:      movzbl 0x7(%rdx),%eax
(gdb) info reg rdx eax
rdx            0xe000009300000000       -2305842377853501440
eax            0x0      0

d8 shell shows:

==21618== Invalid read of size 8
==21618==    at 0x584AA0: v8::internal::HeapObject::Size() (in v8-3.18/out/x64.release/d8)
==21618==    by 0x58FB3F: v8::internal::MarkCompactCollector::EvacuateNewSpace() (in v8-3.18/out/x64.release/d8)
==21618==    by 0x59DDE7: v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() (in v8-3.18/out/x64.release/d8)
==21618==    by 0x59F3A7: v8::internal::MarkCompactCollector::SweepSpaces() (in v8-3.18/out/x64.release/d8)
==21618==    by 0x59F495: v8::internal::MarkCompactCollector::CollectGarbage() (in v8-3.18/out/x64.release/d8)
==21618==    by 0x4D60CB: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) (in v8-3.18/out/x64.release/d8)
==21618==    by 0x4D69D1: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) (in v8-3.18/out/x64.release/d8)
==21618==    by 0x482E51: v8::internal::Factory::NewFixedArrayWithHoles(int, v8::internal::PretenureFlag) (in v8-3.18/out/x64.release/d8)
==21618==    by 0x54BC36: v8::internal::Isolate::CaptureSimpleStackTrace(v8::internal::Handle<v8::internal::JSObject>, v8::internal::Handle<v8::internal::Object>, int) (in v8-3.18/out/x64.release/d8)
==21618==    by 0x623FE3: v8::internal::Runtime_CollectStackTrace(int, v8::internal::Object**, v8::internal::Isolate*) (in v8-3.18/out/x64.release/d8)
==21618==    by 0xBCA8F0616D: ???
==21618==    by 0xBCA8F175D2: ???
==21618==  Address 0x2c0d604d85c8 is not stack'd, malloc'd or (recently) free'd

Did this work before? N/A 

Chrome version: 28.0.1500.20  Channel: dev
OS Version: Ubuntu 12.04 LTS

## Timeline

### in...@chromium.org (2013-05-22)

Also seeing it in https://cluster-fuzz.appspot.com/testcase?key=183959516

### in...@chromium.org (2013-05-22)

Danno@, Mstarzinger@, Verwaest@ - we still need to add severity label to this, is it just a oob read or anything scarier could happen later like oob write, bad function pointer, etc ?

### de...@googlemail.com (2013-05-22)

In terms of severity, my initial guess is that a heap object is corrupted (hence it crashes when trying to determine its size). So I guess all sorts of stuff could happen if this heap object is used in a different way than the size call.

### in...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### ms...@chromium.org (2013-05-22)

I am looking into this.

### ms...@chromium.org (2013-05-22)

The fix just landed on V8 bleeding edge. The analysis from https://crbug.com/chromium/242924#c3 is pretty accurate. The bug leaves a half initialized memory area on the heap and the GC crashes when interpreting this area as an object. Carefully crafted objects from previous allocations will "shine through" that area. The only component that looks at this area is the GC though and references to this area won't escape into JavaScript.

https://code.google.com/p/v8/source/detail?r=14757

### sc...@gmail.com (2013-05-22)

@mstarzinger: was this a dev-channel-only regression?

### ve...@chromium.org (2013-05-22)

This regression was introduced in v8 3.17.6.5, so it's also in stable.

### sc...@gmail.com (2013-05-22)

Thanks! We can merge the fix for the first M27 patch?

### ms...@chromium.org (2013-05-23)

Will merge back to V8 3.17 once we have enough Canary coverage of the fix.

### ms...@chromium.org (2013-05-28)

The statement in https://crbug.com/chromium/242924#c8 is wrong. The regression was first introduced in V8 version 3.18.0, not before. This means that M27 is not affected.

The fix was merged back to M28 as V8 version 3.18.5.6 already.

https://code.google.com/p/v8/source/detail?r=14799

### sc...@gmail.com (2013-05-28)

Thanks for clearing that up!

### sc...@gmail.com (2013-05-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-03)

@decoder.oh: thanks! $1000

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/242924?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077585)*
