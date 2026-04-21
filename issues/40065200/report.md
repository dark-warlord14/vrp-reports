# UAF in MarkingWorklists::Local::IsEmpty(v8)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065200](https://issues.chromium.org/issues/40065200) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-06-02 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

Tested OS:  

ubuntu 2204  

macos Ventura 13.4

Chrome Version:  

Chromium 115.0.5773.4  

Chromium 116.0.5806.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1151812.zip)

repro steps:  

1 python3 -m http.server 8000 --dir=|path|  

2 ./chrome-js-flags=--harmony-struct <http://localhost:8000/poc.html> --user-data-dir=/tmp/xx1

Note:  

It is difficult to reproduce directly opening poc.html. So I wrote a script that opens multiple browsers at the same time and renders poc.html in iframes through wrapper.html.  

This method is still unstable in ubuntu, and the repro probability is less than 10%. But it can be reproduced 100% stably in MacOS.  

./launcher.sh 2>&1 |grep -E 'heap-use'

**Problem Description:**  

==909972==ERROR: AddressSanitizer: heap-use-after-free on address 0x5160026dc982 at pc 0x558e98552f59 bp 0x7f6812a8fcf0 sp 0x7f6812a8fce8  

READ of size 2 at 0x5160026dc982 thread T79 (DedicatedWorker)  

#0 0x558e98552f58 in IsEmpty ./../../v8/src/heap/base/worklist.h:27:33  

#1 0x558e98552f58 in IsLocalEmpty ./../../v8/src/heap/base/worklist.h:413:25  

#2 0x558e98552f58 in v8::internal::MarkingWorklists::Local::IsEmpty() ./../../v8/src/heap/marking-worklist.cc:131:17  

#3 0x558e984629af in v8::internal::IncrementalMarking::ShouldFinalize() const ./../../v8/src/heap/incremental-marking.cc:767:16  

#4 0x558e9842395a in v8::internal::Heap::ShouldExpandOldGenerationOnSlowAllocation(v8::internal::LocalHeap\*, v8::internal::AllocationOrigin) ./../../v8/src/heap/heap.cc:5140:7  

#5 0x558e982f4f86 in v8::internal::ConcurrentAllocator::AllocateFromSpaceFreeList(unsigned long, unsigned long, v8::internal::AllocationOrigin) ./../../v8/src/heap/concurrent-allocator.cc:226:22  

#6 0x558e982f37d7 in v8::internal::ConcurrentAllocator::AllocateLab(v8::internal::AllocationOrigin) ./../../v8/src/heap/concurrent-allocator.cc:152:17  

#7 0x558e982f361d in v8::internal::ConcurrentAllocator::AllocateInLabSlow(int, v8::internal::AllocationAlignment, v8::internal::AllocationOrigin) ./../../v8/src/heap/concurrent-allocator.cc:142:8  

#8 0x558e983be7f2 in AllocateRaw ./../../v8/src/heap/concurrent-allocator-inl.h:43:16  

#9 0x558e983be7f2 in AllocateRaw<(v8::internal::AllocationType)5> ./../../v8/src/heap/heap-allocator-inl.h:124:47  

#10 0x558e983be7f2 in AllocateRaw ./../../v8/src/heap/heap-allocator-inl.h:173:14  

#11 0x558e983be7f2 in v8::internal::HeapAllocator::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ./../../v8/src/heap/heap-allocator.cc:78:29  

#12 0x558e983c1145 in v8::internal::HeapAllocator::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) ./../../v8/src/heap/heap-allocator.cc:105:7  

#13 0x558e983654c1 in AllocateRawWith<(v8::internal::HeapAllocator::AllocationRetryMode)1> ./../../v8/src/heap/heap-allocator-inl.h:224:16  

#14 0x558e983654c1 in v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment) ./../../v8/src/heap/factory.cc:350:23  

#15 0x558e9834e2a4 in AllocateRaw ./../../v8/src/heap/factory-base.cc:1193:18  

#16 0x558e9834e2a4 in AllocateRawWithImmortalMap ./../../v8/src/heap/factory-base.cc:1184:23  

#17 0x558e9834e2a4 in v8::internal::MaybeHandle[v8::internal::SeqOneByteString](javascript:void(0);) v8::internal::FactoryBase[v8::internal::Factory](javascript:void(0);)::NewRawStringWithMap[v8::internal::SeqOneByteString](javascript:void(0);)(int, v8::internal::Map, v8::internal::AllocationType) ./../../v8/src/heap/factory-base.cc:712:24  

#18 0x558e9834de09 in NewRawOneByteString ./../../v8/src/heap/factory-base.cc:725:10  

#19 0x558e9834de09 in v8::internal::FactoryBase[v8::internal::Factory](javascript:void(0);)::NewStringFromOneByte(v8::base::Vector<unsigned char const>, v8::internal::AllocationType) ./../../v8/src/heap/factory-base.cc:878:3  

#20 0x558e9869b131 in v8::internal::SourceCodeCache::Add(v8::internal::Isolate\*, v8::base::Vector<char const>, v8::internal::Handle[v8::internal::SharedFunctionInfo](javascript:void(0);)) ./../../v8/src/init/bootstrapper.cc:122:13  

#21 0x558e986e5371 in v8::internal::Genesis::CompileExtension(v8::internal::Isolate\*, v8::Extension\*) ./../../v8/src/init/bootstrapper.cc:4224:12  

#22 0x558e986f505e in v8::internal::Genesis::InstallExtension(v8::internal::Isolate\*, v8::RegisteredExtension\*, v8::internal::Genesis::ExtensionStates\*) ./../../v8/src/init/bootstrapper.cc:6490:8  

#23 0x558e986f3d03 in InstallExtension ./../../v8/src/init/bootstrapper.cc:6461:14  

#24 0x558e986f3d03 in v8::internal::Genesis::InstallExtensions(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Context](javascript:void(0);), v8::ExtensionConfiguration\*) ./../../v8/src/init/bootstrapper.cc:6413:11  

#25 0x558e9869c06f in InstallExtensions ./../../v8/src/init/bootstrapper.cc:6350:10  

#26 0x558e9869c06f in v8::internal::Bootstrapper::CreateEnvironment(v8::internal::MaybeHandle[v8::internal::JSGlobalProxy](javascript:void(0);), v8::Local[v8::ObjectTemplate](javascript:void(0);), v8::ExtensionConfiguration\*, unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue\*) ./../../v8/src/init/bootstrapper.cc:343:27  

#27 0x558e97da472b in Invoke ./../../v8/src/api/api.cc:6635:39  

#28 0x558e97da472b in CreateEnvironment[v8::internal::Context](javascript:void(0);) ./../../v8/src/api/api.cc:6739:21  

#29 0x558e97da472b in v8::NewContext(v8::Isolate\*, v8::ExtensionConfiguration\*, v8::MaybeLocal[v8::ObjectTemplate](javascript:void(0);), v8::MaybeLocal[v8::Value](javascript:void(0);), unsigned long, v8::DeserializeInternalFieldsCallback, v8::MicrotaskQueue\*) ./../../v8/src/api/api.cc:6780:31  

#30 0x558e97da5f1f in v8::Context::New(v8::Isolate\*, v8::ExtensionConfiguration\*, v8::MaybeLocal[v8::ObjectTemplate](javascript:void(0);), v8::MaybeLocal<v8::Va

**Additional Comments:**

\*\*Chrome version: \*\* 115.0.5773.4 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [empty.js](attachments/empty.js) (text/plain, 7 B)
- [wrapper.html](attachments/wrapper.html) (text/plain, 255 B)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 1.7 KB)
- [asan_ubuntu_headless.log](attachments/asan_ubuntu_headless.log) (text/plain, 59.4 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 947 B)
- [asan2-heap-buffer-overflow.log](attachments/asan2-heap-buffer-overflow.log) (text/plain, 30.8 KB)

## Timeline

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-06-02)

Because there was an error when uploading the attachment(I found out it was because of empty file contents), I resubmitted it.

### em...@gmail.com (2023-06-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4517812402585600.

### aj...@google.com (2023-06-06)

Hi - I'm not able to reproduce this (although I do not have a mac) - can you answer some questions:

a) does this need --harmony-struct?
b) can you bisect to a commit that introduces this?
c) we'd love a minimized test case

As it is it's difficult for me to understand where to assign this.

### em...@gmail.com (2023-06-07)

a) Does this require the --harmony-struct flag?
- Yes, I was only able to reproduce this issue when this flag was enabled.
  
b) Can you bisect to a commit that introduces this?
- Since it's not easy to reproduce, bisecting might take some time. I will update as soon as I make any progress.

c) We'd appreciate a minimized test case
- This is already the most minimized proof of concept (POC). I've tried many times, and reducing it further no longer reproduces the issue.

This is an issue related to v8 gc and should be assigned to component:Blink>JavaScript>GarbageCollection. I will update as soon as I make progress on my analysis.

### aj...@google.com (2023-06-08)

Thanks - sending to v8 who might want to wait for further information.

[Monorail components: Blink>JavaScript>GarbageCollection]

### ml...@chromium.org (2023-06-09)

--harmony-struct is an experimental V8 flag.

Maybe we are checking the wrong heap here.

### em...@gmail.com (2023-06-09)

1) I minimize the poc and deleted irrelevant codes.
2) I have tested multiple versions and narrowed down the scope of repro , but I don't have bisect problem CL yet.
Chromium 115.0.5736.0 (No Repro)
Chromium 115.0.5738.0 ~ latest (Repro)
Although it has been tested many times, the repro is not stable, so the above range cannot be 100% sure.

### [Deleted User] (2023-06-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2023-06-12)

Dominik, can you take a look? Also, please adjust severity afterwards as I don't think it's correct right now.

### di...@chromium.org (2023-06-12)

This issue requires --harmony-struct (or --shared-string-table) so doesn't affect production.

@reporter: Can you reproduce this with --shared-string-table alone (so replacing --harmony-struct with --shared-string-table)? Does e.g. --stress-incremental-marking help in making the repro more stable? So far I wasn't able to reproduce this issue locally, so trying to understand the stack trace now.

### di...@chromium.org (2023-06-12)

Ah and also since I can't reproduce this issue locally: Does this patch fix your crash?

```
diff --git a/src/heap/heap.cc b/src/heap/heap.cc
index 3ce0d2ed8d..2b65a54654 100644
--- a/src/heap/heap.cc
+++ b/src/heap/heap.cc
@@ -5168,7 +5168,7 @@ bool Heap::IsMainThreadParked(LocalHeap* local_heap) {
 }
 
 bool Heap::IsMajorMarkingComplete(LocalHeap* local_heap) {
-  if (!local_heap || !local_heap->is_main_thread()) return false;
+  if (!local_heap || !local_heap->is_main_thread() || local_heap->heap() != this) return false;
   return incremental_marking()->IsMajorMarkingComplete();
 }
```

### em...@gmail.com (2023-06-12)

@#12
After many tests (macos), it cannot be reproduced after replacing --harmony-struct with --shared-string-table. And --stress-incremental-marking doesn't seem to increase the probability of repro much.
@#13
I have run it dozens of times with the patch, and the UAF has not been reproduced again.

### em...@gmail.com (2023-06-13)

I ran with patch all night, and it still crashed once. This time asan output is heap-buffer-overflow.


### ml...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/be22803420ab9b94334964ac3e7db3fe33b93415

commit be22803420ab9b94334964ac3e7db3fe33b93415
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Mon Jun 12 15:01:38 2023

[heap] Stop checking marking worlists for main threads of clients

When allocating in the shared space from a client isolate, the
ConcurrentAllocator invokes Heap::ShouldExpandOldGenerationOnSlowAllocation and then Heap::IsMajorMarkingComplete for the heap of the shared space isolate.
IsMajorMarkingComplete checks the local marking worklist of the
main thread of the shared space isolate which is not thread-safe.
Hence checking it from a client isolate's main thread is illegal.
So far we already bail out for background threads. This CL
now also bails out for client isolate main threads.

Bug: chromium:1450809
Change-Id: Ib468979d61a8d3a99cd9547d48e7587df9956459
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4608401
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88189}

[modify] https://crrev.com/be22803420ab9b94334964ac3e7db3fe33b93415/src/heap/heap.cc


### di...@chromium.org (2023-06-13)

@Reporter: Thanks, so it looks like the patch fixed the issue. I've landed a CL here: https://chromium-review.googlesource.com/c/v8/v8/+/4608401. Can you please check whether the CL still fixes the crash? I will close this issue until then and please re-open in case you still see it.

Regarding that crash: I suspect this is a different issue. Can you open a separate issue for this?

### di...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-06-13)

I have tested many times with above patch(in macos and ubuntu), and the UAF issue does not repro again.

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### sa...@google.com (2023-06-27)

We believe that the issue should've also affected --shared-string-table. This makes a difference because --harmony-struct is considered experimental (i.e. bugs would not be treated as security issues and would instead be "downgraded" to Type-Bug, see https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules), but --shared-string-table is not considered experimental (but is also not enabled by default). This issue should've led to memory corruption, so updating the labels accordingly.

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations on another one, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us --nice work! 

### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-19)

This issue was migrated from crbug.com/chromium/1450809?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065200)*
