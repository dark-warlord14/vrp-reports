# Security:  Debug check failed: string->InSharedHeap() in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40062163](https://issues.chromium.org/issues/40062163) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2022-12-10 |
| **Bounty** | $8,000.00 |

## Description

```
Title : Debug check failed: string->InSharedHeap() in v8  
  
**VULNERABILITY DETAILS**   
## INTRODUCE  
  
After bisect, it was determined that commit 9f0d20b0feea980e4a7c64211addb2145316bd53	caused this problem.  
  
- 82260 will trigger crash: `Debug check failed: unreachable code`  
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82260.zip?generation=1659958526814570&alt=media  
- And 82261 will trigger crash: `Debug check failed: string->InSharedHeap()`  
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82261.zip?generation=1659961012417163&alt=media  
  

```

commit 9f0d20b0feea980e4a7c64211addb2145316bd53 [log] [tgz]  

author Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org) Fri Aug 05 12:19:59 2022  

committer V8 LUCI CQ [v8-scoped@luci-project-accounts.iam.gserviceaccount.com](mailto:v8-scoped@luci-project-accounts.iam.gserviceaccount.com) Mon Aug 08 12:04:52 2022  

tree 2bb6381ce625687f02801275295422ad42644f2b  

parent 557a84d620872aa6b9f89cb0910f7bd96ab2d8c5 [diff]  

[heap] Support allocation of large shared objects

So far there was no support for allocating large objects in the  

shared heap.

Bug: v8:11708  

Change-Id: Ie4ec8244fee2e75fc0e2265847fe5976da2645ea  

Reviewed-on: <https://chromium-review.googlesource.com/c/v8/v8/+/3811579>  

Reviewed-by: Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Commit-Queue: Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Cr-Commit-Position: refs/heads/main@{#82261}

```
  
## CRASH LOG  
- Debug output  

```

➜ Desktop linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/d8 --harmony-struct /tmp/poc.js

# 

# Fatal error in ../../src/objects/string-inl.h, line 786

# Debug check failed: string->InSharedHeap().

# 

# 

# 

#FailureMessage Object: 0x7ffe50087a20  

==== C stack trace ===============================

```
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f319e315963]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8_libplatform.so(+0x195bd) [0x7f319e2bc5bd]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x153) [0x7f319e2f5023]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8_libbase.so(+0x2aac5) [0x7f319e2f4ac5]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8.so(v8::internal::String::Share(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::String>)+0x1fb) [0x7f31a05102bb]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8.so(v8::internal::Object::ShareSlow(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::ShouldThrow)+0x1df) [0x7f31a050febf]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8.so(v8::internal::Object::Share(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Object>, v8::internal::ShouldThrow)+0xda) [0x7f31a050f93a]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8.so(+0x23f7252) [0x7f31a0714252]  
/home/kiprey/Desktop/linux-debug%2Fd8-linux-debug-v8-component-82261/d8-linux-debug-v8-component-82261/libv8.so(v8::internal::Runtime_AtomicsStoreSharedStructOrArray(int, unsigned long\*, v8::internal::Isolate\*)+0xb7) [0x7f31a0713e47]  
[0x7f311fa047bf]  

```

[1] 4103784 trace trap --harmony-struct /tmp/poc.js

```
  
**VERSION**   
Tested on v8 version 10.6.0-11.0.0  
  
**REPRODUCTION CASE**   
1. Download debug v8 from: https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84768.zip?generation=1670646083479813&alt=media  
2. Run: ./d8 --harmony-struct /tmp/poc.js  
  
**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**   
Type of crash: tab  
  
**CREDIT INFORMATION**   
Reporter credit: Zhenghang Xiao (@Kipreyyy)  

```

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 147 B)

## Timeline

### [Deleted User] (2022-12-10)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-12-10)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-12-10)

If you want to use clusterfuzz for classification, please note to include the flags: --harmony-struct

### ki...@gmail.com (2022-12-10)

CRASH ANALYSIS

1. When v8 intends to share an EXTRA-LONG string, the string object may no longer be kept in the shared memory, thus triggering the DCHECK [1].
2. After DCHECK, there is an operation related to the write barrier [2], and since the string object is no longer on shared memory, this operation may change the stability of current memory region, causing a potential UAF vulnerabilit.

```
Handle<String> String::Share(Isolate* isolate, Handle<String> string) {
  DCHECK(v8_flags.shared_string_table);
  MaybeHandle<Map> new_map;
  switch (
      isolate->factory()->ComputeSharingStrategyForString(string, &new_map)) {
    case StringTransitionStrategy::kCopy:
      return SlowShare(isolate, string);
    case StringTransitionStrategy::kInPlace:
      // A relaxed write is sufficient here, because at this point the string
      // has not yet escaped the current thread.
      DCHECK(string->InSharedHeap());    <------------------------------------- [1]
      string->set_map_no_write_barrier(*new_map.ToHandleChecked()); <---------- [2]
      return string;
    case StringTransitionStrategy::kAlreadyTransitioned:
      return string;
  }
}
```

### cl...@chromium.org (2022-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6197745464573952.

### cl...@chromium.org (2022-12-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2022-12-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/9f0d20b0feea980e4a7c64211addb2145316bd53 ([heap] Support allocation of large shared objects).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2022-12-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6197745464573952

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  string->InSharedHeap() in string-inl.h
  v8::internal::String::Share
  v8::internal::Object::ShareSlow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=82260:82261

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6197745464573952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-12-10)

[Empty comment from Monorail migration]

### di...@chromium.org (2022-12-12)

I can reproduce this locally. This doesn't affect production since --harmony-struct is needed.

### di...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/303facf5e132c45aaa4a8fad019998848133691c

commit 303facf5e132c45aaa4a8fad019998848133691c
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Dec 13 09:30:42 2022

[heap] Also promote strings in large objects into shared heap

With --shared-string-table all in-place internalizable strings are
directly promoted from new space into the shared heap. However, this
wasn't the case with large objects. This CL fixes this and adds test
to guide fuzzers.

Bug: v8:13267, chromium:1400048
Change-Id: I6f850d480956c63bfbe1a7060140df850e284933
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4096818
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84805}

[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/memory-allocator.h
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/scavenger.cc
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/runtime/runtime.h
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/basic-memory-chunk.h
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/heap-verifier.cc
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/scavenger.h
[add] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/test/mjsunit/shared-memory/shared-string-promotion-minor-large.js
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/runtime/runtime-test.cc
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/mark-compact.cc
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/large-spaces.cc
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/memory-allocator.cc
[add] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/test/mjsunit/shared-memory/shared-string-promotion-major-large.js
[modify] https://crrev.com/303facf5e132c45aaa4a8fad019998848133691c/src/heap/large-spaces.h


### di...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-13)

ClusterFuzz testcase 6197745464573952 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84804:84805

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2022-12-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6197745464573952

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  string->InSharedHeap() in string-inl.h
  v8::internal::String::Share
  v8::internal::Object::ShareSlow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=82260:82261
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84804:84805

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6197745464573952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### di...@chromium.org (2022-12-13)

This only happens with the --shared-string-table flag and doesn't affect production.

### gi...@appspot.gserviceaccount.com (2022-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45

commit 8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Dec 13 14:33:05 2022

Revert "[heap] Also promote strings in large objects into shared heap"

This reverts commit 303facf5e132c45aaa4a8fad019998848133691c.

Reason for revert: Causes failures with fuzzers.

Original change's description:
> [heap] Also promote strings in large objects into shared heap
>
> With --shared-string-table all in-place internalizable strings are
> directly promoted from new space into the shared heap. However, this
> wasn't the case with large objects. This CL fixes this and adds test
> to guide fuzzers.
>
> Bug: v8:13267, chromium:1400048
> Change-Id: I6f850d480956c63bfbe1a7060140df850e284933
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4096818
> Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#84805}

Bug: v8:13267, chromium:1400048
Change-Id: If20528bbf804b73ce8ad10f8addc9a1f11b50d96
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4101261
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84813}

[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/memory-allocator.h
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/scavenger.cc
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/runtime/runtime.h
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/basic-memory-chunk.h
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/heap-verifier.cc
[delete] https://crrev.com/317bc26ac93ac3fd91cf669ff6e72e95aa151782/test/mjsunit/shared-memory/shared-string-promotion-minor-large.js
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/scavenger.h
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/runtime/runtime-test.cc
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/large-spaces.cc
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/mark-compact.cc
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/memory-allocator.cc
[delete] https://crrev.com/317bc26ac93ac3fd91cf669ff6e72e95aa151782/test/mjsunit/shared-memory/shared-string-promotion-major-large.js
[modify] https://crrev.com/8f911e423e3a478dd22c4bf09b5f2cdd2c6a7e45/src/heap/large-spaces.h


### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3915384f58cc8b592c566c0092f055a794ce6173

commit 3915384f58cc8b592c566c0092f055a794ce6173
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Dec 13 14:40:52 2022

Reland "[heap] Also promote strings in large objects into shared heap"

This is a reland of commit 303facf5e132c45aaa4a8fad019998848133691c

This CL fixes DCHECK failures by using BasicMemoryChunk in
RecordOldToSharedSlot.

Original change's description:
> [heap] Also promote strings in large objects into shared heap
>
> With --shared-string-table all in-place internalizable strings are
> directly promoted from new space into the shared heap. However, this
> wasn't the case with large objects. This CL fixes this and adds test
> to guide fuzzers.
>
> Bug: v8:13267, chromium:1400048
> Change-Id: I6f850d480956c63bfbe1a7060140df850e284933
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4096818
> Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#84805}

Bug: v8:13267, chromium:1400048, v8:13588
Change-Id: I221592ec723d2b5e92094ff2598a99576d72a677
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4098831
Auto-Submit: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84830}

[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/memory-allocator.h
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/scavenger.cc
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/runtime/runtime.h
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/basic-memory-chunk.h
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/heap-verifier.cc
[add] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/test/mjsunit/shared-memory/shared-string-promotion-minor-large.js
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/scavenger.h
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/runtime/runtime-test.cc
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/memory-allocator.cc
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/large-spaces.cc
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/mark-compact.cc
[add] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/test/mjsunit/shared-memory/shared-string-promotion-major-large.js
[modify] https://crrev.com/3915384f58cc8b592c566c0092f055a794ce6173/src/heap/large-spaces.h


### gi...@appspot.gserviceaccount.com (2022-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e073775f8eb55ed71c44bd5716e3488b1cef0a4e

commit e073775f8eb55ed71c44bd5716e3488b1cef0a4e
Author: Milad Fa <mfarazma@redhat.com>
Date: Thu Dec 15 15:44:36 2022

[heap] Fix build on platforms without shared heap

Bug: v8:13267, chromium:1400048
Change-Id: I562996384632e6e2568548fcabc1c05c48b9335a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4111940
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Milad Farazmand <mfarazma@redhat.com>
Cr-Commit-Position: refs/heads/main@{#84883}

[modify] https://crrev.com/e073775f8eb55ed71c44bd5716e3488b1cef0a4e/src/heap/heap-verifier.cc


### di...@chromium.org (2022-12-19)

@Patrick: I will revert my CL that promotes large strings into shared space directly. Can you PTAL at this and fix this in String::Share?

### gi...@appspot.gserviceaccount.com (2022-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5

commit 0b36f43e9eaa165b5ebc8e9abadf629d76d178d5
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Sun Dec 18 23:03:53 2022

Revert "[heap] Also promote strings in large objects into shared heap"

Revert of the CLs: https://crrev.com/c/4098831,
https://crrev.com/c/4110739, https://crrev.com/c/4108649.

Promoting large objects into shared space during GC is not really
needed, we can always promote such objects on-demand as well.

Bug: v8:13267, chromium:1400048
Change-Id: Icc01a3bac2698ea442409dec0a86bd7c0c5bf74e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4111850
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84924}

[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/memory-allocator.h
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/scavenger.cc
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/runtime/runtime.h
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/basic-memory-chunk.h
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/heap-verifier.cc
[delete] https://crrev.com/15d123009b7e987e946309cd5724ae17f376bd16/test/mjsunit/shared-memory/shared-string-promotion-minor-large.js
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/scavenger.h
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/runtime/runtime-test.cc
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/large-spaces.cc
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/memory-allocator.cc
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/mark-compact.cc
[delete] https://crrev.com/15d123009b7e987e946309cd5724ae17f376bd16/test/mjsunit/shared-memory/shared-string-promotion-major-large.js
[modify] https://crrev.com/0b36f43e9eaa165b5ebc8e9abadf629d76d178d5/src/heap/large-spaces.h


### pt...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0621c2d553e69ca2a3dae1ddabd3fe8f8e5c0dd2

commit 0621c2d553e69ca2a3dae1ddabd3fe8f8e5c0dd2
Author: pthier <pthier@chromium.org>
Date: Mon Dec 19 15:38:53 2022

[string] Copy when sharing strings that are not in shared space

Usually sharable strings are automatically promoted to shared old space
and can be shared in-place.
There are currently two exceptions:
- When using a non-moving GC (e.g. minor MC)
- Strings in LO space
Account for these exceptions by copying strings to the respective shared
space when sharing them.

Bug: chromium:1400048
Change-Id: I20713b5f32f449c14febd848e289b5767530a257
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4110752
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Patrick Thier <pthier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84942}

[add] https://crrev.com/0621c2d553e69ca2a3dae1ddabd3fe8f8e5c0dd2/test/mjsunit/shared-memory/shared-string-copy-on-share-large.js
[modify] https://crrev.com/0621c2d553e69ca2a3dae1ddabd3fe8f8e5c0dd2/src/heap/factory.cc
[add] https://crrev.com/0621c2d553e69ca2a3dae1ddabd3fe8f8e5c0dd2/test/mjsunit/shared-memory/shared-string-copy-on-share.js


### ma...@google.com (2022-12-21)

Does the above CL fix this issue?

### di...@chromium.org (2022-12-21)

Yes, it should.

### pt...@chromium.org (2022-12-21)

Yes sorry. Was waiting for CF to confirm but apperently it isn't automatically triggered if it already verified the issue as fixed previously.

### cl...@chromium.org (2022-12-21)

Detailed Report: https://clusterfuzz.com/testcase?key=6197745464573952

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  string->InSharedHeap() in string-inl.h
  v8::internal::String::Share
  v8::internal::Object::ShareSlow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=82260:82261
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84804:84805

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6197745464573952

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pt...@chromium.org (2022-12-21)

Update security impact again (see https://crbug.com/chromium/1400048#c17).

### sa...@chromium.org (2023-01-04)

This is an issue in the renderer -> Severity-High, not Critical

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations, Zhenghang! The VRP Panel has decided to award you $7,000 + $1,000 bisect bonus for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-30)

This issue was migrated from crbug.com/chromium/1400048?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062163)*
