# Security: Debug check failed: slot < sentinel_ in UpdateUntypedOldToSharedPointers

| Field | Value |
|-------|-------|
| **Issue ID** | [40061784](https://issues.chromium.org/issues/40061784) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2022-11-17 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

It seems to be sharedheap gc issue in v8, it can lead to potential oob or uaf, but I don't have a full root cause analysis.  

However, I found when it was introduced by bisect.

## Introduce

```
commit 6fbe1bf2987462ab31f6ed3ede5226ab21f75580  
Author: Dominik Inführ <dinfuehr@chromium.org>  
Date:   Mon Aug 1 08:20:41 2022 +0200  
  
    [heap] Also record old-to-shared slots on promotion and evacuation  
      
    When an object either gets promoted or evacuated, old-to-shared slots  
    need to be recorded like we already do for old-to-old or old-to-new.  
      
    Bug: v8:11708  
    Change-Id: Ifb5b3d50a59aa45bf8289e1cd7610bb2f317fd6c  
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3794648  
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>  
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>  
    Cr-Commit-Position: refs/heads/main@{#82096}  

```
## crash analysis

- poc1

```
bool InvalidatedSlotsFilter::IsValid(Address slot) {  
#ifdef DEBUG  
  DCHECK_LT(slot, sentinel_);  
  // Slots must come in non-decreasing order.  
  DCHECK_LE(last_slot_, slot);  
  last_slot_ = slot;  
#endif  
  if (slot < current_.address) {  
    return true;  
  }  
  ...  

```

<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/invalidated-slots-inl.h;l=21?q=invalidated-slots-inl.h>

The source code shows that both slot and sentinel\_ are addresses, and slot should be smaller than sentinel\_, but here slot is larger than sentinel\_, and there may be a potential OOB.

```
#  
# Fatal error in ../../src/heap/invalidated-slots-inl.h, line 21  
# Debug check failed: slot < sentinel_ (68174019043664 vs. 68174019043660).  
#  
#  
#  
#FailureMessage Object: 0x7f0e4c49c780  
==== C stack trace ===============================  
  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f0e51abfb93]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libplatform.so(+0x187ed) [0x7f0e51a677ed]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x154) [0x7f0e51a9f3c4]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(+0x2ae65) [0x7f0e51a9ee65]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::InvalidatedSlotsFilter::IsValid(unsigned long)+0x524) [0x7f0e53823424]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(+0x1d70624) [0x7f0e53837624]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::PointersUpdatingJob::Run(v8::JobDelegate\*)+0x42c) [0x7f0e5383a64c]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0xd3) [0x7f0e51a66633]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x29) [0x7f0e51a68a09]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(+0x4a920) [0x7f0e51abe920]  
    /lib/x86_64-linux-gnu/libpthread.so.0(+0x8609) [0x7f0e515f7609]  
    /lib/x86_64-linux-gnu/libc.so.6(clone+0x43) [0x7f0e513cb133]  
[1]    14819 trace trap (core dumped)  d8-linux-debug-v8-component-84320/d8 --expose-gc --harmony-struct poc.js  

```

- poc2  
  
  There is another variant of this crash, also introduced by the same commit.

```
#  
# Fatal error in ../../src/heap/base/basic-slot-set.h, line 85  
# Debug check failed: (\*slot_set->bucket(i)) == nullptr.  
#  
#  
#  
#FailureMessage Object: 0x7fff8ce1de00  
==== C stack trace ===============================  
  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f2b46f88b93]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libplatform.so(+0x187ed) [0x7f2b46f307ed]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x154) [0x7f2b46f683c4]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8_libbase.so(+0x2ae65) [0x7f2b46f67e65]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::MemoryChunk::ReleaseAllocatedMemoryNeededForWritableChunk()+0x2aa) [0x7f2b48d2ebba]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::MemoryAllocator::PerformFreeMemory(v8::internal::MemoryChunk\*)+0x33) [0x7f2b48d28063]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::LargeObjectSpace::TearDown()+0x101) [0x7f2b48ca17c1]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::LargeObjectSpace::~LargeObjectSpace()+0x1d) [0x7f2b48ca598d]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::OldLargeObjectSpace::~OldLargeObjectSpace()+0xe) [0x7f2b48ca595e]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::Heap::TearDown()+0x840) [0x7f2b48c81af0]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::Isolate::Deinit()+0x5e3) [0x7f2b48b2db13]  
    /usr/class/data/d8-linux-debug-v8-component-84320/libv8.so(v8::internal::Isolate::Delete(v8::internal::Isolate\*)+0x114) [0x7f2b48b2d224]  
    d8-linux-debug-v8-component-84320/d8(v8::Shell::OnExit(v8::Isolate\*, bool)+0x2e) [0x564467003c7e]  
    d8-linux-debug-v8-component-84320/d8(v8::Shell::Main(int, char\*\*)+0x102e) [0x56446700ff5e]  
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf3) [0x7f2b46799083]  
    d8-linux-debug-v8-component-84320/d8(_start+0x2a) [0x564466fdfaaa]  
[1]    14788 trace trap (core dumped)  d8-linux-debug-v8-component-84320/d8 --expose-gc --harmony-struct poc2.js  

```

**VERSION**  

Tested on v8 version 10.6-11.0

**REPRODUCTION CASE**

1. Download debug v8 from:  
   
   <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84320.zip?generation=1668684401965995&alt=media>
2. d8-linux-debug-v8-component-84314/d8 --expose-gc --harmony-struct poc.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 486 B)
- [poc2.js](attachments/poc2.js) (text/plain, 232 B)

## Timeline

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-11-17)

sorry, run: `d8-linux-debug-v8-component-84320/d8 --expose-gc --harmony-struct poc.js`

### cl...@chromium.org (2022-11-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5240588057378816.

### dr...@chromium.org (2022-11-18)

While clusterfuzz couldn't reproduce it, it immediately crashes for me as far back as commit position 83238 (https://commondatastorage.googleapis.com/v8-asan/index.html?prefix=linux-debug/d8-linux-debug-v8-component-83238). If I've tracked the dependencies right, that's the version in M107, so setting FoundIn appropriately.

mlippautz@, hpayer@ - can you take a look at this? Can you let me know what is the security impact of this DCHECK failure?


[Monorail components: Blink>JavaScript>GarbageCollection]

### [Deleted User] (2022-11-18)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-11-18)

This requires `--expose-gc --harmony-struct` to reproduce, please set the flag of clusterfuzz correctly


### ki...@gmail.com (2022-11-18)

https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82096.zip?generation=1659360804757385&alt=media

This is the build corresponding to the commit that introduced this problem, so maybe it should be Foundin-106


### ml...@chromium.org (2022-11-18)

--harmony-struct is not enabled in production. 

### di...@chromium.org (2022-11-18)

Thanks for reporting this! I can reproduce both crashes locally. Looking into it now.

### di...@chromium.org (2022-11-18)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-11-21)

I'm adding security labels assuming this leads to arbitrary memory corruption in the renderer process. Let me know if that's not the case.

### di...@chromium.org (2022-11-21)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-11-21)

> I'm adding security labels assuming this leads to arbitrary memory corruption in the renderer process. Let me know if that's not the case.

This is not the case per https://crbug.com/chromium/1385717#c8, as this POC depends on passing --harmony-struct, which gates an experimental V8 feature, and is off by default.

### dr...@chromium.org (2022-11-21)

Sorry, this is a nuance of our security labels. We track "severity" and "impact" separately. The former answers "what's the worst-case outcome for affected users?" and the latter answers "what are the affected users?". This is correctly marked Security_Impact-None, because the feature is off by default. But the severity still isn't clear. For users running with --harmony-struct, would this vulnerability lead to memory corruption?

### sy...@chromium.org (2022-11-21)

Ah I see, thank you for the correction. I'll defer to dinfuehr@ for the severity question.

### gi...@appspot.gserviceaccount.com (2022-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/96b83b8160a8215f7e8013fca1d15325872a3cdb

commit 96b83b8160a8215f7e8013fca1d15325872a3cdb
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Fri Nov 18 12:55:41 2022

[heap] Remove OLD_TO_SHARED slots when shrinking large objects

Clear OLD_TO_SHARED slots in free memory after shrinking large objects.
This CL now clear all slots outside of the object and not just from
the next OS page boundary.

Since we are already here also stop clearing OLD_TO_NEW and OLD_TO_OLD
since they should already be cleared at this stage of the GC. Add
DCHECKs that this always holds. We also don't need to iterate large
code objects since we do not shrink such pages anyway.

Bug: v8:13267, chromium:1385717
Change-Id: I75f6e56a7c13974ce669bbba29262e95eb94d287
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4037981
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84407}

[modify] https://crrev.com/96b83b8160a8215f7e8013fca1d15325872a3cdb/src/heap/base/basic-slot-set.h
[modify] https://crrev.com/96b83b8160a8215f7e8013fca1d15325872a3cdb/src/heap/large-spaces.cc
[modify] https://crrev.com/96b83b8160a8215f7e8013fca1d15325872a3cdb/src/heap/mark-compact.cc
[add] https://crrev.com/96b83b8160a8215f7e8013fca1d15325872a3cdb/test/mjsunit/shared-memory/shrink-large-object.js


### di...@chromium.org (2022-11-21)

This should be fixed now.

Regarding Security severity: AFAICS this is an use-after-free issue and since I don't know better, I will just leave the Security_Severity-High label for now.

### ki...@gmail.com (2022-11-22)

Since this is a UAF case caused by GC, I think it is appropriate to keep security-high. Thanks for your fix :)

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Zhenghang Xiao! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-28)

This issue was migrated from crbug.com/chromium/1385717?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061784)*
