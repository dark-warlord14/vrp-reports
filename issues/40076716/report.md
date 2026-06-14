# [LangFuzz] Crash at v8::internal::HeapObject::SizeFromMap with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40076716](https://issues.chromium.org/issues/40076716) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2012-12-18 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20121216 Firefox/19.0

Steps to reproduce the problem:
Run the following code in d8 with --expose_gc:

JSON.stringify(String.fromCharCode(1, -11).toString())
gc();

What is the expected behavior?

What went wrong?
Crash:

==13010== Invalid read of size 1
==13010==    at 0x8148FE9: v8::internal::HeapObject::SizeFromMap(v8::internal::Map*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x8194949: v8::internal::MarkCompactCollector::EvacuateNewSpace() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x8195742: v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x8196CF3: v8::internal::MarkCompactCollector::SweepSpaces() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x81979FA: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x80F7851: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x80FACC0: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x80FB179: v8::internal::Heap::CollectAllGarbage(int, char const*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x80B7E09: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x8084B2D: v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==13010==    by 0x4340A3F5: ???
==13010==    by 0x4342A38C: ???
==13010==  Address 0x10082312 is not stack'd, malloc'd or (recently) free'd

Did this work before? Yes 

Chrome version: 25.0.1359.3 dev  Channel: dev
OS Version: 12.04

Not tested in the browser because I don't have a build working with --expose_gc, but verified with V8 r13169, which is the version used in the specified Chrome build.

## Timeline

### in...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### ul...@chromium.org (2012-12-18)

Bisected it to [Improve array to string conversion]: https://code.google.com/p/v8/source/detail?r=13144

Fix is in review: https://chromiumcodereview.appspot.com/11576069

### ul...@chromium.org (2012-12-18)

Fixed on V8 bleeding_edge in r13235.

### in...@chromium.org (2012-12-18)

ulan@, what was the bug here (bad cast / oob write / oob read ) ? We need to gauge the bug severity.

### ul...@chromium.org (2012-12-18)

The bug can lead to oob write. I saw this assertion hit while debugging:

void SeqOneByteString::SeqOneByteStringSet(int index, uint16_t value) {
  ASSERT(index >= 0 && index < length() && value <= kMaxAsciiCharCode);
  WRITE_BYTE_FIELD(this, kHeaderSize + index * kCharSize,
                   static_cast<byte>(value));
}

where index is 43, and length() is 32.


### in...@chromium.org (2012-12-18)

Thanks! is this a recent regression ?

### ul...@chromium.org (2012-12-18)

> is this a recent regression ?
Yes, the bug was introduced on Dec 5, 2012 in this CL: https://code.google.com/p/v8/source/detail?r=13144, which corresponds to V8 version 3.15.9.

### in...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-19)

ulan@, there is similar testcase that is hitting on ClusterFuzz [https://cluster-fuzz.appspot.com/testcase?key=151857583]. Can you please check if your fix fixes it.

=================================================================
==5356== ERROR: AddressSanitizer: SEGV on unknown address 0x7f637d7fff60 (pc 0x7f638ff24ab3 sp 0x7fff59987b40 bp 0x7fff59987c30 T0)
AddressSanitizer can not provide additional info.
    #0 0x7f638ff24ab2 in v8::internal::SlotsBuffer::UpdateSlotsRecordedIn(v8::internal::Heap*, v8::internal::SlotsBuffer*, bool) v8/src/mark-compact.cc:2397
    #1 0x7f638ff22ba4 in v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() v8/src/mark-compact.cc:3007
    #2 0x7f638ff0f245 in v8::internal::MarkCompactCollector::SweepSpaces() v8/src/mark-compact.cc:3613
    #3 0x7f638ff0cddc in v8::internal::MarkCompactCollector::CollectGarbage() v8/src/mark-compact.cc:396
    #4 0x7f638fcb9b93 in v8::internal::Heap::MarkCompact(v8::internal::GCTracer*) v8/src/heap.cc:1016
    #5 0x7f638fcb7097 in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) v8/src/heap.cc:891

### ul...@chromium.org (2012-12-19)

inferno@, I can't repro that crash. The renderer process is just running with 100% cpu and doing nothing. I've built release chromium with these flags:
 export GYP_GENERATORS=ninja; export GYP_DEFINES='disable_nacl=1 asan=1 linux_use_tcmalloc=0 release_extra_cflags="-g" ' as described in http://www.chromium.org/developers/testing/addresssanitizer

Are the flags correct?

### in...@chromium.org (2012-12-19)

Are you passing these flags to chrome -  --js-flags="--expose-gc" --no-first-run --no-sandbox --use-gl=any --user-data-dir=/mnt/scratch0/tmp/user_profile_chrome_0

Also, we are using an additional build flag -  v8_enable_verify_heap=1, do you think that will make a difference.

### ul...@chromium.org (2012-12-20)

Tried Debug and Release with the mentioned chrome flags and v8_enable_verify_heap=1 gyp flag: no luck with repro on revision @174116.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-11)

M25: http://code.google.com/p/v8/source/detail?r=13357

### sc...@gmail.com (2013-01-22)

@decoder: thank you. OOB write => $1000

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-25)

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

### pa...@chromium.org (2013-06-24)

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

This issue was migrated from crbug.com/chromium/166553?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076716)*
