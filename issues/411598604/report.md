# V8 Sandbox Bypass: UAF during LargeObjectSpace tear down

| Field | Value |
|-------|-------|
| **Issue ID** | [411598604](https://issues.chromium.org/issues/411598604) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | v8...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2025-04-18 |
| **Bounty** | $5,000.00 |

## Description

#### VERSION

V8 commit: 9a9a2b2d796da6e8b4ae1bb294aff41294b882fc

#### REPRODUCTION CASE

Build args:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
v8_static_library=true
v8_fuzzilli=false
target_cpu="x64"

```

Shell args: `d8 --single-threaded --sandbox-fuzzing --allow-natives-syntax --expose-gc bug.js`

##### ASAN Report:

```
==1515577==ERROR: AddressSanitizer: heap-use-after-free on address 0x7dff2a8ef228 at pc 0x560b63b47ea5 bp 0x7fff5d8ee640 sp 0x7fff5d8ee638
READ of size 8 at 0x7dff2a8ef228 thread T0
    #0 0x560b63b47ea4 in get third_party/libc++/src/include/__memory/unique_ptr.h:268:94
    #1 0x560b63b47ea4 in IsLargePage src/heap/mutable-page-metadata.h:281:33
    #2 0x560b63b47ea4 in v8::internal::MemoryAllocator::DeleteMemoryChunk(v8::internal::MutablePageMetadata*) src/heap/memory-allocator.cc:663:17
    #3 0x560b63b8fadc in v8::internal::PagePool::ReleaseOnTearDown(v8::internal::Isolate*) src/heap/page-pool.cc:72:11
    #4 0x560b639a7149 in v8::internal::Heap::TearDown() src/heap/heap.cc:6223:31
    #5 0x560b637dfcc6 in v8::internal::Isolate::Deinit() src/execution/isolate.cc:4547:9
    #6 0x560b637deed0 in v8::internal::Isolate::Delete(v8::internal::Isolate*) src/execution/isolate.cc:4137:12
    #7 0x560b62f9d93e in v8::Shell::OnExit(v8::Isolate*, bool) src/d8/d8.cc:4471:14
    #8 0x560b62fb529c in v8::Shell::Main(int, char**) src/d8/d8.cc:6874:3
    #9 0x7faf2b6a61c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #10 0x7faf2b6a628a in __libc_start_main csu/../csu/libc-start.c:360:3
    #11 0x560b62e74029 in _start (/work/v8-build/v8/out/Reproduction/d8+0x1143029) (BuildId: 47bbc0a8c91a8f29)

0x7dff2a8ef228 is located 296 bytes inside of 8528-byte region [0x7dff2a8ef100,0x7dff2a8f1250)
freed by thread T0 here:
    #0 0x560b62f4e89d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:143:3
    #1 0x560b63a53015 in v8::internal::LargeObjectSpace::TearDown() src/heap/large-spaces.cc:73:33
    #2 0x560b63a56823 in v8::internal::LargeObjectSpace::~LargeObjectSpace() src/heap/large-spaces.h:38:34
    #3 0x560b63a5679d in v8::internal::OldLargeObjectSpace::~OldLargeObjectSpace() src/heap/large-spaces.h:144:7
    #4 0x560b639a6f70 in operator() third_party/libc++/src/include/__memory/unique_ptr.h:76:5
    #5 0x560b639a6f70 in reset third_party/libc++/src/include/__memory/unique_ptr.h:287:7
    #6 0x560b639a6f70 in v8::internal::Heap::TearDown() src/heap/heap.cc:6218:15
    #7 0x560b637dfcc6 in v8::internal::Isolate::Deinit() src/execution/isolate.cc:4547:9
    #8 0x560b637deed0 in v8::internal::Isolate::Delete(v8::internal::Isolate*) src/execution/isolate.cc:4137:12
    #9 0x560b62f9d93e in v8::Shell::OnExit(v8::Isolate*, bool) src/d8/d8.cc:4471:14
    #10 0x560b62fb529c in v8::Shell::Main(int, char**) src/d8/d8.cc:6874:3
    #11 0x7faf2b6a61c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #12 0x7faf2b6a628a in __libc_start_main csu/../csu/libc-start.c:360:3
    #13 0x560b62e74029 in _start (/work/v8-build/v8/out/Reproduction/d8+0x1143029) (BuildId: 47bbc0a8c91a8f29)

previously allocated by thread T0 here:
    #0 0x560b62f4e03d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x560b63b4873d in v8::internal::MemoryAllocator::AllocatePage(v8::internal::MemoryAllocator::AllocationMode, v8::internal::Space*, v8::internal::Executability) src/heap/memory-allocator.cc:393:16
    #2 0x560b63b993a6 in v8::internal::PagedSpaceBase::TryExpand(v8::internal::LocalHeap*, v8::internal::AllocationOrigin) src/heap/paged-spaces.cc:305:52
    #3 0x560b63a61edf in v8::internal::PagedSpaceAllocatorPolicy::TryExpandAndAllocate(unsigned long, v8::internal::AllocationOrigin) src/heap/main-allocator.cc:775:18
    #4 0x560b63a6138c in v8::internal::PagedSpaceAllocatorPolicy::RefillLab(int, v8::internal::AllocationOrigin) src/heap/main-allocator.cc:748:9
    #5 0x560b63a5ce9f in v8::internal::MainAllocator::EnsureAllocation(int, v8::internal::AllocationAlignment, v8::internal::AllocationOrigin) src/heap/main-allocator.cc:333:29
    #6 0x560b63a5c9a1 in v8::internal::MainAllocator::AllocateRawSlowUnaligned(int, v8::internal::AllocationOrigin) src/heap/main-allocator.cc:212:8
    #7 0x560b64a4a06a in AllocateRaw src/heap/main-allocator-inl.h:39:31
    #8 0x560b64a4a06a in AllocateRaw<(v8::internal::AllocationType)1> src/heap/heap-allocator-inl.h:130:35
    #9 0x560b64a4a06a in AllocateRawWith<(v8::internal::HeapAllocator::AllocationRetryMode)1> src/heap/heap-allocator-inl.h:227:14
    #10 0x560b64a4a06a in v8::internal::Heap::AllocateRawOrFail(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) src/heap/heap-inl.h:204:9
    #11 0x560b64a43460 in Allocate src/snapshot/deserializer.cc:1665:50
    #12 0x560b64a43460 in v8::internal::Deserializer<v8::internal::Isolate>::ReadObject(v8::internal::SnapshotSpace) src/snapshot/deserializer.cc:800:7
    #13 0x560b64a5c4ce in int v8::internal::Deserializer<v8::internal::Isolate>::ReadNewObject<v8::internal::SlotAccessorForRootSlots>(unsigned char, v8::internal::SlotAccessorForRootSlots) src/snapshot/deserializer.cc:1098:42
    #14 0x560b64a4502e in ReadData src/snapshot/deserializer.cc:975:16
    #15 0x560b64a4502e in v8::internal::Deserializer<v8::internal::Isolate>::VisitRootPointers(v8::internal::Root, char const*, v8::internal::FullObjectSlot, v8::internal::FullObjectSlot) src/snapshot/deserializer.cc:381:3
    #16 0x560b6399dc1e in v8::internal::Heap::IterateRoots(v8::internal::RootVisitor*, v8::base::EnumSet<v8::internal::SkipRoot, int>, v8::internal::Heap::IterateRootsMode) src/heap/heap.cc:4675:6
    #17 0x560b64ac7ef3 in v8::internal::StartupDeserializer::DeserializeIntoIsolate() src/snapshot/startup-deserializer.cc:42:24
    #18 0x560b637ed8f8 in v8::internal::Isolate::Init(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) src/execution/isolate.cc:5791:26
    #19 0x560b637ef698 in v8::internal::Isolate::InitWithSnapshot(v8::internal::SnapshotData*, v8::internal::SnapshotData*, v8::internal::SnapshotData*, bool) src/execution/isolate.cc:5245:10
    #20 0x560b64a8e187 in v8::internal::Snapshot::Initialize(v8::internal::Isolate*) src/snapshot/snapshot.cc:198:19
    #21 0x560b6339f9b5 in v8::Isolate::Initialize(v8::Isolate*, v8::Isolate::CreateParams const&) src/api/api.cc:10088:8
    #22 0x560b6339ff84 in New src/api/api.cc:10127:3
    #23 0x560b6339ff84 in v8::Isolate::New(v8::Isolate::CreateParams const&) src/api/api.cc:10121:10
    #24 0x560b62fb465b in v8::Shell::Main(int, char**) src/d8/d8.cc:6684:22
    #25 0x7faf2b6a61c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x7faf2b6a628a in __libc_start_main csu/../csu/libc-start.c:360:3
    #27 0x560b62e74029 in _start (/work/v8-build/v8/out/Reproduction/d8+0x1143029) (BuildId: 47bbc0a8c91a8f29)

SUMMARY: AddressSanitizer: heap-use-after-free third_party/libc++/src/include/__memory/unique_ptr.h:268:94 in get
Shadow bytes around the buggy address:
  0x7dff2a8eef80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dff2a8ef000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dff2a8ef080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7dff2a8ef100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7dff2a8ef200: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7dff2a8ef480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1515577==ABORTING

## V8 sandbox violation detected!


```
#### CREDIT INFORMATION

Reporter credit: v8sbxfuzz

## Attachments

- [bug.js](attachments/bug.js) (text/javascript, 427 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-04-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5034912511885312.

### an...@chromium.org (2025-04-18)

[security shepherd]: Thank you for the report. Uploaded test case and assigning to current sheriff @cf...@chromium.org with the provisional severity of S1.

### ch...@google.com (2025-04-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-05-03)

cffsmith: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-04)

cffsmith: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### cf...@google.com (2025-05-05)

Thanks for the report! I can reproduce this with the given gn args on HEAD.  

mlippautz@ could you PTAL?

### ml...@chromium.org (2025-05-06)

Large pages shouldn't make it into the pool.

### ml...@chromium.org (2025-05-06)

Dominik, do you have time to take a look?

### ml...@chromium.org (2025-05-06)

Maybe this is related to growing a page beyong large page size and we get confused how to handle it then?

### dx...@google.com (2025-05-06)

Project: v8/v8  

Branch: main  

Author: Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6513778>

[heap] Avoid page flag check for large page detection

---


Expand for full commit details
```
     
    This CL improves performance of Scavenger::HandleLargeObject by 
    delaying the page flag checks for each and every object. Instead 
    of page flags the method now simply checks the offset on the page 
    first. This should filter out most objects already. In order to 
    filter out regular objects at the start of a page, we still need to 
    perform page flag checks but this should be quite unlikely. 
     
    In addition this CL ensures that promoted large pages are proper 
    large pages by checking that PageMetadata::IsLargePage() holds. This 
    is necessary because HandleLargeObject() only checks the untrusted 
    page flags. 
     
    Bug: 411598604 
    Change-Id: I03390950abf1e482d2be2b7df72834693ee29115 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6513778 
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100102}

```

---

Files:

- M `src/heap/scavenger-inl.h`
- M `src/heap/scavenger.cc`

---

Hash: 41614e86a3e9f3b94f7bb36d83cd9f0fb1c52a17  

Date:  Tue May 6 16:43:56 2025


---

### 24...@project.gserviceaccount.com (2025-05-06)

Testcase 5034912511885312 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5034912511885312.

### 24...@project.gserviceaccount.com (2025-05-06)

ClusterFuzz testcase 5034912511885312 appears to be flaky, updating reproducibility hotlist.

### di...@chromium.org (2025-05-07)

I think the issue should be fixed now.

### dx...@google.com (2025-05-07)

Project: v8/v8  

Branch: main  

Author: Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6516383>

[heap] Fix sandbox access in MutablePageMetadata::owner\_identity()

---


Expand for full commit details
```
     
    owner_identity() is used in a SBXCHECK and this is not supposed to 
    access the sandbox. However, in a DCHECK we were accessing the 
    sandbox just to check the page flags in a DCHECK. This CL allows 
    the sandbox access just for the DCHECK. 
     
    Bug: 411598604, 415968772 
    Cq-Include-Trybots: luci.v8.try:v8_linux64_pku_dbg,v8_linux64_pku_rel 
    Change-Id: I9d73e39917e6ddb320d8be7aa93197bda81d17d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6516383 
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org> 
    Reviewed-by: Stephen Röttger <sroettger@google.com> 
    Cr-Commit-Position: refs/heads/main@{#100112}

```

---

Files:

- M `src/heap/mutable-page-metadata-inl.h`

---

Hash: 21fcc74333ed48097025343dcdb70227e04f933c  

Date:  Wed May 7 09:04:22 2025


---

### ch...@google.com (2025-05-07)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### di...@chromium.org (2025-05-07)

Sandbox bypasses currently don't require backmerges, so no backmerge needed.

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of V8 heap sandbox bypass demonstrating memory corruption outside of the V8 sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-16)

Congratulations and thank you for your continued efforts in fuzzing the V8 heap sandbox!

### ch...@google.com (2025-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of V8 heap sandbox bypass demonstrating memory corruption outside of the V8 sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/411598604)*
