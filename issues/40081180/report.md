# Heap-buffer-overflow in SkData::NewUninitialized

| Field | Value |
|-------|-------|
| **Issue ID** | [40081180](https://issues.chromium.org/issues/40081180) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2015-01-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The latest 64-bit Asan build of filter\_fuzz\_stub crashes as follows:

# [0113/181345:INFO:filter\_fuzz\_stub.cc(59)] Test case: repro.fil

==20498==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300000ed30 at pc 0x00000053ac1c bp 0x7ffff4517650 sp 0x7ffff4517648  

WRITE of size 8 at 0x60300000ed30 thread T0  

#0 0x53ac1b in SkData /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkData.cpp:27  

#1 0x50c131 in ReadRawPixels /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkBitmap.cpp:1213  

#2 0x5c96bc in readBitmap /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.cpp:268  

#3 0x8e34a7 in CreateProc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:34  

#4 0x6345a8 in readFlattenable /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#5 0x556144 in SkValidatingDeserializeFlattenable(void const\*, unsigned long, SkFlattenable::Type) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#6 0x49fe5f in RunTestCase /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#7 0x7fd854c96ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60300000ed30 is located 8 bytes to the right of 24-byte region [0x60300000ed10,0x60300000ed28)  

allocated by thread T0 here:  

#0 0x4817c9 in \_\_interceptor\_malloc ??:?  

#1 0x9f8c1a in sk\_malloc\_throw /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:50  

#2 0x53aa00 in PrivateNewWithCopy /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkData.cpp:66  

#3 0x50c131 in ReadRawPixels /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkBitmap.cpp:1213  

#4 0x5c96bc in readBitmap /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.cpp:268  

#5 0x8e34a7 in CreateProc /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/effects/SkBitmapSource.cpp:34  

#6 0x6345a8 in readFlattenable /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#7 0x556144 in SkValidatingDeserializeFlattenable(void const\*, unsigned long, SkFlattenable::Type) /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#8 0x49fe5f in RunTestCase /mnt/data/b/build/slave/ASAN\_Release/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#9 0x7fd854c96ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c067fff9d50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff9d60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff9d70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff9d80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c067fff9d90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c067fff9da0: fa fa 00 00 00 fa[fa]fa 00 00 00 fa fa fa fd fd  

0x0c067fff9db0: fd fa fa fa fd fd fd fa fa fa 00 00 05 fa fa fa  

0x0c067fff9dc0: 00 00 04 fa fa fa 00 00 05 fa fa fa 00 00 04 fa  

0x0c067fff9dd0: fa fa 00 00 00 00 fa fa 00 00 00 00 fa fa fd fd  

0x0c067fff9de0: fd fd fa fa fd fd fd fa fa fa fd fd fd fd fa fa  

0x0c067fff9df0: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==20498==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-311241

**REPRODUCTION CASE**  

Attached as repro.fil

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 672 B)

## Timeline

### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5697628737110016

### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5697628737110016

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x60a00000e420
Crash State:
  SkData::NewUninitialized
  SkBitmap::ReadRawPixels
  SkReadBuffer::readBitmap
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=294200:294571

Minimized Testcase (0.66 Kb): https://cluster-fuzz.appspot.com/download/AMIfv954DKsWW_b9rSlTyIJSQiIEbfRF7_l5m4E0EX3a2PDclGcqsFTpC1hVG4R3X9Lil9Yh8KJC7mMC06Yhjv73gwYX7_untydzRq9iA1ayh_U9elHVH6V77IiSp2ZhQcf0Oit8LOqdfQgGfjLatZzTbRFPJWgTTg



### cl...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-28)

sugoi@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### su...@chromium.org (2015-01-28)

This issue is caused by getting a width of -1, which causes info.minRowBytes() to be a huge number, which causes SkMallocPixelRef::NewWithData() to fail and return NULL, which then crashes when "pr" is dereferenced, when calling pr->info(). This is around SkBitmap.cpp:1233, approximately.

### su...@chromium.org (2015-01-28)

Attempted fix under review here:
https://codereview.chromium.org/881423002/

### su...@chromium.org (2015-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge Requested to M41 (Branch 2272)

### pe...@google.com (2015-02-17)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### pe...@chromium.org (2015-02-20)

Note: M41 stable cut happens in days, and you're approved for merge.  Get it in there!  (Let me know if you need any help, or aren't confident.)

### su...@chromium.org (2015-02-23)

Cl created to merge into M41:
https://codereview.chromium.org/949903002/

### su...@chromium.org (2015-02-23)

Scratch that, I forgot the NOTRY=1 on the initial cl and even after adding it through the "edit" menu, it wasn't working so I've recreated a new cl to land this fix in M41 here:
https://codereview.chromium.org/951593002

The commit button still doesn't work, though. I probably need to land this on the command line. I'll double check...

### su...@chromium.org (2015-02-23)

Ok, the patch has landed in M41.

### pe...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $5000 for this report.

### ti...@google.com (2015-03-03)

Correcting CVE

### in...@chromium.org (2015-03-09)

This is not fixed. Still reproduces :(:(
https://cluster-fuzz.appspot.com/testcase?key=5659861220589568

### in...@chromium.org (2015-03-09)

Stack has changed slightly.

=================================================================
==12636==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60a00000e420 at pc 0x0000005202b0 bp 0x7fff1b545b80 sp 0x7fff1b545b78
WRITE of size 8 at 0x60a00000e420 thread T0
    #0 0x5202af in SkData::SkData(unsigned long) third_party/skia/src/core/SkData.cpp:27:5
    #1 0x520562 in SkData::PrivateNewWithCopy(void const*, unsigned long) third_party/skia/src/core/SkData.cpp:67:5
    #2 0x501f20 in SkBitmap::ReadRawPixels(SkReadBuffer*, SkBitmap*) third_party/skia/src/core/SkBitmap.cpp:1213:26
    #3 0x593bd2 in SkReadBuffer::readBitmap(SkBitmap*) third_party/skia/src/core/SkReadBuffer.cpp:268:20
    #4 0x804e0a in SkBitmapSource::CreateProc(SkReadBuffer&) third_party/skia/src/effects/SkBitmapSource.cpp:34:10
    #5 0x5ee678 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third_party/skia/src/core/SkValidatingReadBuffer.cpp:247:15
    #6 0x536b64 in SkValidatingDeserializeFlattenable(void const*, unsigned long, SkFlattenable::Type) third_party/skia/src/core/SkFlattenableSerialization.cpp:26:12
    #7 0x4a082a in (anonymous namespace)::RunTestCase(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >&, SkBitmap&, SkCanvas*) skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:30:32
    #8 0x4a02ab in (anonymous namespace)::ReadAndRunTestCase(char const*, SkBitmap&, SkCanvas*) skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:65:3
    #9 0x49fe61 in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:81:10
    #10 0x7f8f926d1ec4 in __libc_start_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

0x60a00000e420 is located 8 bytes to the right of 24-byte region [0x60a00000e400,0x60a00000e418)
allocated by thread T0 here:
    #0 0x481c79 in __interceptor_malloc
    #1 0x8e6efa in sk_malloc_throw(unsigned long) skia/ext/SkMemory_new_handler.cpp:50:35
    #2 0x520547 in SkData::PrivateNewWithCopy(void const*, unsigned long) third_party/skia/src/core/SkData.cpp:66:28
    #3 0x501f20 in SkBitmap::ReadRawPixels(SkReadBuffer*, SkBitmap*) third_party/skia/src/core/SkBitmap.cpp:1213:26
    #4 0x593bd2 in SkReadBuffer::readBitmap(SkBitmap*) third_party/skia/src/core/SkReadBuffer.cpp:268:20
    #5 0x804e0a in SkBitmapSource::CreateProc(SkReadBuffer&) third_party/skia/src/effects/SkBitmapSource.cpp:34:10
    #6 0x5ee678 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) third_party/skia/src/core/SkValidatingReadBuffer.cpp:247:15
    #7 0x536b64 in SkValidatingDeserializeFlattenable(void const*, unsigned long, SkFlattenable::Type) third_party/skia/src/core/SkFlattenableSerialization.cpp:26:12
    #8 0x4a082a in (anonymous namespace)::RunTestCase(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >&, SkBitmap&, SkCanvas*) skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:30:32
    #9 0x4a02ab in (anonymous namespace)::ReadAndRunTestCase(char const*, SkBitmap&, SkCanvas*) skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:65:3
    #10 0x49fe61 in main skia/tools/filter_fuzz_stub/filter_fuzz_stub.cc:81:10
    #11 0x7f8f926d1ec4 in __libc_start_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### su...@chromium.org (2015-03-09)

That last crash is caused by a width of -1, which results in an extremely large rowBytes and fails to allocate silently and then crashes when deleting the unallocated memory pointer.

Anyway, it's not the same issue as the original one, but I'll look into why this crashes.

### in...@chromium.org (2015-03-09)

ok, let me file a different bug.

### in...@chromium.org (2015-03-09)

ok new bug filed as https://code.google.com/p/chromium/issues/detail?id=465455

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-06-15)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/448423?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081180)*
