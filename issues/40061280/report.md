# use after poison in  HeapObjectHeader::LoadEncoded()

| Field | Value |
|-------|-------|
| **Issue ID** | [40061280](https://issues.chromium.org/issues/40061280) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2022-10-08 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

os version:ubuntu 22.04  

chrome version:Chromium 108.0.5327.0  

chrome version: Chromium 108.0.5347.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1056570.zip)

repro step:  

in version 108.0.5347.0  

./chrome --disable-gpu --no-sandbox --disable-gpu --window-position=0,0 --window-size=1000,600 <http://localhost:8001/crash2/crash.html> --incognito --user-data-dir=/tmp/xx1  

The repro is stable. I can repro one or two execution in the local test.

in version 108.0.5327.0:  

repro not stable. You can try launcher.js to execute multi browser at once.  

./launcher.sh

**Problem Description:**  

==582973==ERROR: AddressSanitizer: use-after-poison on address 0x7ea500238544 at pc 0x5604f5c29920 bp 0x7fff35c94950 sp 0x7fff35c94948  

READ of size 2 at 0x7ea500238544 thread T0 (chrome)  

#0 0x5604f5c2991f in LoadEncoded<(cppgc::internal::AccessMode)0, (cppgc::internal::HeapObjectHeader::EncodedHalf)1, (std::Cr::memory\_order)2> ./../../v8/src/heap/cppgc/heap-object-header.h:341:46  

#1 0x5604f5c2991f in GetGCInfoIndex<(cppgc::internal::AccessMode)0> ./../../v8/src/heap/cppgc/heap-object-header.h:217:7  

#2 0x5604f5c2991f in IsFree<(cppgc::internal::AccessMode)0> ./../../v8/src/heap/cppgc/heap-object-header.h:305:10  

#3 0x5604f5c2991f in cppgc::internal::BasePage::TryObjectHeaderFromInnerAddress(void const\*) const ./../../v8/src/heap/cppgc/heap-page.cc:118:15  

#4 0x5604f5c68214 in TryTracePointerConservatively ./../../v8/src/heap/cppgc/visitor.cc:85:24  

#5 0x5604f5c68214 in cppgc::internal::ConservativeTracingVisitor::TraceConservativelyIfNeeded(void const\*) ./../../v8/src/heap/cppgc/visitor.cc:95:3  

#6 0x5604f3ecf9c3 in v8::internal::(anonymous namespace)::UnifiedHeapConservativeMarkingVisitor::TraceConservativelyIfNeeded(void const\*) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:273:33  

#7 0x5604f5c6b597 in heap::base::(anonymous namespace)::IteratePointersImpl(heap::base::Stack const\*, heap::base::StackVisitor\*, long\*) ./../../v8/src/heap/base/stack.cc:142:14  

#8 0x5604f5c6b7a2 in PushAllRegistersAndIterateStack push\_registers\_asm.cc:0:0  

#9 0x5604f5c349a0 in cppgc::internal::MarkerBase::VisitRoots(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc/marker.cc:444:21  

#10 0x5604f5c358db in cppgc::internal::MarkerBase::EnterAtomicPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc/marker.cc:271:5  

#11 0x5604f3ecce97 in v8::internal::CppHeap::EnterFinalPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:702:10  

#12 0x5604f401cdec in v8::internal::MarkCompactCollector::MarkLiveObjects() ./../../v8/src/heap/mark-compact.cc:2818:40  

#13 0x5604f401bc6c in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:655:3  

#14 0x5604f3f9f836 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2704:29  

#15 0x5604f3f95f1c in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const\*, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2376:5  

#16 0x5604f3f8b64e in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1903:33  

#17 0x5604f3f93521 in CollectAllGarbage ./../../v8/src/heap/heap.cc:1611:3  

#18 0x5604f3f93521 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:3924:3  

#19 0x5604f3ecde75 in IncreaseAllocatedSize ./../../v8/src/heap/embedder-tracing.h:136:7  

#20 0x5604f3ecde75 in ReportBufferedAllocationSizeIfPossible ./../../v8/src/heap/cppgc-js/cpp-heap.cc:835:13  

#21 0x5604f3ecde75 in AllocatedObjectSizeIncreased ./../../v8/src/heap/cppgc-js/cpp-heap.cc:807:3  

#22 0x5604f3ecde75 in non-virtual thunk to v8::internal::CppHeap::AllocatedObjectSizeIncreased(unsigned long) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:0:0  

#23 0x5604f5c56795 in operator() ./../../v8/src/heap/cppgc/stats-collector.cc:0:0  

#24 0x5604f5c56795 in ForAllAllocationObservers<(lambda at ../../v8/src/heap/cppgc/stats-collector.cc:83:29)> ./../../v8/src/heap/cppgc/stats-collector.h:388:7  

#25 0x5604f5c56795 in cppgc::internal::StatsCollector::AllocatedObjectSizeSafepointImpl() ./../../v8/src/heap/cppgc/stats-collector.cc:83:3  

#26 0x5604f5c42707 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, cppgc::internal::AlignVal, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:120:20  

#27 0x56050e07f9b5 in Invoke ./../../v8/include/cppgc/allocation.h:94:14  

#28 0x56050e07f9b5 in Allocate ./../../v8/include/cppgc/allocation.h:180:12  

#29 0x56050e07f9b5 in blink::FrameFetchContext::FrozenState\* cppgc::MakeGarbageCollectedTrait[blink::FrameFetchContext::FrozenState](javascript:void(0);)::Call<blink::KURL const&, blink::ContentSecurityPolicy\*, net::SiteForCookies, scoped\_refptr<blink::SecurityOrigin const>, blink::ClientHintsPreferences const&, float, WTF::String&, absl::optional[blink::UserAgentMetadata](javascript:void(0);), bool, bool, WTF::String>(cppgc::AllocationHandle&, blink::KURL const&, blink::ContentSecurityPolicy\*&&, net::SiteForCookies&&, scoped\_refptr<blink::SecurityOrigin const>&&, blink::ClientHintsPreferences const&, float&&, WTF::String&, absl::optional[blink::UserAgentMetadata](javascript:void(0);)&&, bool&&, bool&&, WTF::String&&) ./../../v8/include/cppgc/allocation.h:241:9  

#30 0x56050e07cd09 in MakeGarbageCollected<blink::FrameFetchContext::FrozenState, const blink::KURL &, blink::ContentSecurityPolicy \*, net::SiteForCookies, scoped\_re

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.5327.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 770 B)
- [launcher.sh](attachments/launcher.sh) (text/plain, 1.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 22.5 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 15.3 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 898 B)

## Timeline

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5165943846273024.

### an...@chromium.org (2022-10-09)

Clusterfuzz was unable to reproduce. I was also unable to reproduce. I used 108.0.5347.0 with the single command line. I also tried launcher.sh to launch multiple windows.
@emilykim8708, can you double check the repro details? Also, maybe provide a video if possible? Thanks.

### em...@gmail.com (2022-10-09)

In local tests, a single command line can reproduce stably, so repro video may not help much either. I will try to find another pc and test again.

### em...@gmail.com (2022-10-09)

I have tested it in other Linux real machines with different performance, and it can also repro stably, but it cannot repro in virtual machines. I suspect if it can only be reproduced on the real machine. did you test in virtual machine environment?

### em...@gmail.com (2022-10-09)

I'm sorry,There is some mismatch with the original asan log and  poc file.I uploaded new one.

### em...@gmail.com (2022-10-09)

You can try this a little modified poc.
./launcher.js

Modify the chrome path and IP address of./launcer according to the actual environment.
Execute./launcher If it does not repro immediately(just wait about 5s), press ctrl+c to close all browsers and execute again.

### an...@chromium.org (2022-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-10-09)

I have indeed been trying to reproduce this in a Linux VM. In https://crbug.com/chromium/1372784#c7, did you mean to attach a modified launcher.js? 
I don't have access to an actual Linux m/c, but will ask to see if someone else here can try.

### em...@gmail.com (2022-10-09)

I mean modify original launcher.js,the path and ip address was hard coded.But I think you already modified.
And try the new poc(crash2.html).
Thanks~


### em...@gmail.com (2022-10-10)

I also reproduced with macos(Monterey 12.6).But tried more times then in linux.
Chromium 108.0.5350.0(https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-1056755.zip?generation=1665334181571367&alt=media)


### an...@chromium.org (2022-10-10)

I think we have enough information here for the relevant V8 experts to digest. mlippautz@, please re-route as necessary. Thanks!


[Monorail components: Blink>JavaScript>GarbageCollection]

### ml...@chromium.org (2022-10-10)

Looks like a recursive GC (GC call from sweeping) which we are supposed to have guards against. Will take a closer look tomorrow.

### ml...@chromium.org (2022-10-11)

Fix is on the way. This broke in 108.0.5313.0 [1].

https://chromiumdash.appspot.com/commit/19f6eda36691023d2438b96d8d01d225176f87cc

### ml...@chromium.org (2022-10-11)

This can lead to memory corruption and UAF. Only Canary/Dev are affected.

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9e8dd823c3ec55e09809796bdbcdf0ae89076a0f

commit 9e8dd823c3ec55e09809796bdbcdf0ae89076a0f
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Tue Oct 11 08:31:44 2022

cppgc: Add missing sweeping scope

The scope prevents recursive garbage collections that may otherwise
trigger through allocations in destructors.

Bug: chromium:1372784
Change-Id: I98525333701551962bbc2a16f8f50eeb637fc03d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3942651
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83625}

[modify] https://crrev.com/9e8dd823c3ec55e09809796bdbcdf0ae89076a0f/src/heap/cppgc/sweeper.cc


### ml...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-14)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-14)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2022-10-17)

This patch is already rolled on a M108 dev. I don't think there's anything to merge here.

https://chromiumdash.appspot.com/commit/9e8dd823c3ec55e09809796bdbcdf0ae89076a0f

### [Deleted User] (2022-10-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering this issue and reporting it to us, along with providing an updated / modified POC to assist with our efforts in reproduction. Nice work! 

### am...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1372784?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061280)*
