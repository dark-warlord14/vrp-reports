# Security: UAP on creating WebAssembly memories on document reload

| Field | Value |
|-------|-------|
| **Issue ID** | [40057594](https://issues.chromium.org/issues/40057594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2021-10-13 |
| **Bounty** | $7,500.00 |

## Description

I am opening a separate issue to track ​https://bugs.chromium.org/p/chromium/issues/detail?id=1252878#c42.

https://crbug.com/chromium/1252878 already contains a fix which addressed the initially reported issue in there. 

The other minimal repro (https://crbug.com/chromium/1259587#c42) results in a different stack which may  fundamentaly be a different issue. If it turns out to be related, we can merge it back.

For posterity, the report by "emilykim8708@gmail.com" is as follows:

After simple modification of the poc file, I can still repro this issue. Can someone check it?
version: Chromium 97.0.4665.0 gs://chromium-browser-asan/linux-release/asan-linux-release-929567.zip

READ of size 8 at 0x7ee000299b70 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x559a553490e2 in cppgc::internal::(anonymous namespace)::TraceConservatively(cppgc::internal::ConservativeTracingVisitor*, cppgc::internal::HeapObjectHeader const&) ./../../v8/src/heap/cppgc/visitor.cc:38
    #1 0x559a553490e2 in ?? ??:0
    #2 0x559a5531e5a4 in cppgc::internal::MarkerBase::MarkNotFullyConstructedObjects() ./../../v8/src/heap/cppgc/marker.cc:556
    #3 0x559a5531e5a4 in ?? ??:0
    #4 0x559a5531dfe0 in cppgc::internal::MarkerBase::EnterAtomicPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc/marker.cc:254
    #5 0x559a5531dfe0 in ?? ??:0
    #6 0x559a53f07493 in non-virtual thunk to v8::internal::CppHeap::EnterFinalPause(cppgc::EmbedderStackState) ./../../v8/src/heap/cppgc-js/cpp-heap.cc:475
    #7 0x559a53f07493 in ?? ??:0
    #8 0x559a53f1a67a in ?? ??:0
    #9 0x559a53f1a67a in v8::internal::LocalEmbedderHeapTracer::EnterFinalPause() ./../../v8/src/heap/embedder-tracing.cc:57
    #10 0x559a53f1a67a in ?? ??:0
    #11 0x559a5406a0de in v8::internal::MarkCompactCollector::MarkLiveObjects() ./../../v8/src/heap/mark-compact.cc:2080
    #12 0x559a5406a0de in ?? ??:0
    #13 0x559a54069587 in v8::internal::MarkCompactCollector::CollectGarbage() ./../../v8/src/heap/mark-compact.cc:580
    #14 0x559a54069587 in ?? ??:0
    #15 0x559a53fa76d9 in v8::internal::Heap::MarkCompact() ./../../v8/src/heap/heap.cc:2480
    #16 0x559a53fa76d9 in ?? ??:0
    #17 0x559a53fa0fbf in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:2210
    #18 0x559a53fa0fbf in ?? ??:0
    #19 0x559a53f9942d in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) ./../../v8/src/heap/heap.cc:1793
    #20 0x559a53f9942d in ?? ??:0
    #21 0x559a53f9e6e6 in v8::internal::Heap::FinalizeIncrementalMarkingAtomically(v8::internal::GarbageCollectionReason) ./../../v8/src/heap/heap.cc:1464
    #22 0x559a53f9e6e6 in FinalizeIncrementalMarkingAtomically ./../../v8/src/heap/heap.cc:3730
    #23 0x559a53f9e6e6 in ?? ??:0
    #24 0x559a53a98710 in v8::EmbedderHeapTracer::IncreaseAllocatedSize(unsigned long) ./../../v8/src/heap/embedder-tracing.h:108
    #25 0x559a53a98710 in IncreaseAllocatedSize ./../../v8/src/api/api.cc:10071
    #26 0x559a53a98710 in ?? ??:0
    #27 0x559a55337e5f in cppgc::internal::StatsCollector::NotifySafePointForConservativeCollection() stats-collector.cc:?
    #28 0x559a55337e5f in ForAllAllocationObservers<(lambda at ../../v8/src/heap/cppgc/stats-collector.cc:82:29)> ./../../v8/src/heap/cppgc/stats-collector.h:367
    #29 0x559a55337e5f in AllocatedObjectSizeSafepointImpl ./../../v8/src/heap/cppgc/stats-collector.cc:82
    #30 0x559a55337e5f in NotifySafePointForConservativeCollection ./../../v8/src/heap/cppgc/stats-collector.cc:63
    #31 0x559a55337e5f in ?? ??:0
    #32 0x559a553284a4 in cppgc::internal::ObjectAllocator::OutOfLineAllocate(cppgc::internal::NormalPageSpace&, unsigned long, unsigned short) ./../../v8/src/heap/cppgc/object-allocator.cc:120
    #33 0x559a553284a4 in ?? ??:0
    #34 0x559a66a726b7 in blink::AutoplayPolicy::AutoplayPolicy(blink::HTMLMediaElement*) ./../../v8/include/cppgc/allocation.h:64
    #35 0x559a66a726b7 in Allocate ./../../v8/include/cppgc/allocation.h:112
    #36 0x559a66a726b7 in Call<blink::HTMLMediaElement *&> ./../../v8/include/cppgc/allocation.h:173
    #37 0x559a66a726b7 in MakeGarbageCollected<blink::AutoplayUmaHelper, blink::HTMLMediaElement *&> ./../../v8/include/cppgc/allocation.h:212
    #38 0x559a66a726b7 in MakeGarbageCollected<blink::AutoplayUmaHelper, blink::HTMLMediaElement *&> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #39 0x559a66a726b7 in AutoplayPolicy ./../../third_party/blink/renderer/core/html/media/autoplay_policy.cc:158
    #40 0x559a66a726b7 in ?? ??:0
    #41 0x559a66a20162 in blink::HTMLMediaElement::HTMLMediaElement(blink::QualifiedName const&, blink::Document&) ./../../v8/include/cppgc/allocation.h:174
    #42 0x559a66a20162 in MakeGarbageCollected<blink::AutoplayPolicy, blink::HTMLMediaElement *> ./../../v8/include/cppgc/allocation.h:212
    #43 0x559a66a20162 in MakeGarbageCollected<blink::AutoplayPolicy, blink::HTMLMediaElement *> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #44 0x559a66a20162 in HTMLMediaElement ./../../third_party/blink/renderer/core/html/media/html_media_element.cc:571
    #45 0x559a66a20162 in ?? ??:0
    #46 0x559a66a81a49 in blink::HTMLVideoElement::HTMLVideoElement(blink::Document&) ./../../third_party/blink/renderer/core/html/media/html_video_element.cc:83
    #47 0x559a66a81a49 in ?? ??:0
    #48 0x559a6864bc09 in blink::HTMLVideoConstructor(blink::Document&, blink::CreateElementFlags) ./../../v8/include/cppgc/allocation.h:174
    #49 0x559a6864bc09 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> ./../../v8/include/cppgc/allocation.h:212
    #50 0x559a6864bc09 in MakeGarbageCollected<blink::HTMLVideoElement, blink::Document &> ./../../third_party/blink/renderer/platform/heap/heap.h:26
    #51 0x559a6864bc09 in HTMLVideoConstructor ./gen/third_party/blink/renderer/core/html_element_factory.cc:678
    #52 0x559a6864bc09 in ?? ??:0
    #53 0x559a68637444 in blink::HTMLElementFactory::Create(WTF::AtomicString const&, blink::Document&, blink::CreateElementFlags) ./gen/third_party/blink/renderer/core/html_element_factory.cc:857
    #54 0x559a68637444 in ?? ??:0
    #55 0x559a6558bdea in blink::Document::CreateElementForBinding(WTF::AtomicString const&, blink::ExceptionState&) ./../../third_party/blink/renderer/core/dom/document.cc:1033
    #56 0x559a6558bdea in ?? ??:0
    #57 0x559a6c6ee809 in blink::(anonymous namespace)::v8_document::CreateElementOperationCallbackForMainWorld(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:5294
    #58 0x559a6c6ee809 in CreateElementOperationCallbackForMainWorld ./gen/third_party/blink/renderer/bindings/modules/v8/v8_document.cc:5352
    #59 0x559a6c6ee809 in ?? ??:0
    #60 0x559a53b348e7 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:152
    #61 0x559a53b348e7 in ?? ??:0
    #62 0x559a53b3253e in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:112
    #63 0x559a53b3253e in ?? ??:0
    #64 0x559a53b2ff9a in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:142
    #65 0x559a53b2ff9a in ?? ??:0

## Attachments

- [min_poc3.html](attachments/min_poc3.html) (text/plain, 358 B)

## Timeline

### ml...@chromium.org (2021-10-13)

I can reproduce this on today's main 9051ac131283f04ebf92e8e3e557c7965bc2253b.

gn args:
  use_goma= true
  is_debug = false
  is_component_build = false
  enable_nacl = false
  dcheck_always_on = true
  is_asan = true

### am...@chromium.org (2021-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-13)

The underlying bug is related to https://crbug.com/chromium/1252878 in that there still exists a corner case where we don't process an ephemeron and the fix in the previous bug is incomplete.

Technical details:
- A C++ object that's in construction is generally pushed to a work list for later processing (to get a chance that it's fully constructed).
- For ephemerons, we use the same marking for incremental/concurrent processing and final processing.
- This results in an ephemeron pair not being processed as it's further "delayed" even though there's no delay in the final GC pause [1].

Working on a fix now.

[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/cppgc/marking-state.h;l=306;bpv=1;bpt=0

### [Deleted User] (2021-10-13)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-13)

Adding Anton in here as CL reviewer.

### gi...@appspot.gserviceaccount.com (2021-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/32a09a6bce6cc75806dee5ec748bb1d081048fd0

commit 32a09a6bce6cc75806dee5ec748bb1d081048fd0
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Wed Oct 13 18:26:12 2021

cppgc: Fix marking of ephemerons with keys in construction

Consider in-construction keys as live during the final GC pause.

Bug: chromium:1259587
Change-Id: Ia8c05923db6e5827b68b17a51561fbc8b2c4b467
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3221153
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77386}

[modify] https://crrev.com/32a09a6bce6cc75806dee5ec748bb1d081048fd0/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/32a09a6bce6cc75806dee5ec748bb1d081048fd0/src/heap/cppgc/marker.cc
[modify] https://crrev.com/32a09a6bce6cc75806dee5ec748bb1d081048fd0/test/unittests/heap/cppgc/ephemeron-pair-unittest.cc


### ml...@chromium.org (2021-10-14)

Fixed on main. Needs some Canary coverage now.

### ad...@google.com (2021-10-14)

Approving merge to M96, but please give it 24 hours on Canary first.

### ml...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-14)

Sorry, wrong bug...

### be...@chromium.org (2021-10-14)

Amy: Can we consider this for the security refresh of M95?

### am...@chromium.org (2021-10-14)

Hi Ben, yes this should go into the security refresh for M95; as this was just landed less than a day ago, would prefer to give it more bake time on Canary before approving the merge 

### go...@chromium.org (2021-10-14)

Please merge your change to M96 branch 4664 ASAP. Thank you.

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-14)

Merge review required: M95 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-14)

Merge review required: M94 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2021-10-15)

Will merge to M96, as I don't see any immediate problems.

Merge review:

1. Why does your merge fit within the merge criteria for these milestones?

Security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3221153

3. Have the changes been released and tested on canary?

The change is released on Canary 97.0.4670.0: https://chromiumdash.appspot.com/commit/32a09a6bce6cc75806dee5ec748bb1d081048fd0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No, manual verification required. The fix has been tested locally to address a security issue and accomodates a test.

### sr...@google.com (2021-10-15)

This issue has been approved for Merge to M96, Please help complete your merges no later than 12pm PST (Monday Oct 18) so that they can go out in next week beta promotion build. I would like to get beta coverage for these CL's as much as we can .

### gi...@appspot.gserviceaccount.com (2021-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4feccb9b4e4ac2accc92dd24b17f6b2f12611354

commit 4feccb9b4e4ac2accc92dd24b17f6b2f12611354
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Wed Oct 13 18:26:12 2021

cppgc: Fix marking of ephemerons with keys in construction

Consider in-construction keys as live during the final GC pause.

Bug: chromium:1259587
Change-Id: Ia8c05923db6e5827b68b17a51561fbc8b2c4b467
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3221153
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Anton Bikineev <bikineev@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77386}
(cherry picked from commit 32a09a6bce6cc75806dee5ec748bb1d081048fd0)
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3226785
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/4feccb9b4e4ac2accc92dd24b17f6b2f12611354/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/4feccb9b4e4ac2accc92dd24b17f6b2f12611354/src/heap/cppgc/marker.cc
[modify] https://crrev.com/4feccb9b4e4ac2accc92dd24b17f6b2f12611354/test/unittests/heap/cppgc/ephemeron-pair-unittest.cc


### ad...@google.com (2021-10-18)

VRP panel:
* This issue was reported on Fri Oct 8th in https://bugs.chromium.org/p/chromium/issues/detail?id=1252878#c42
* However, https://bugs.chromium.org/p/chromium/issues/detail?id=1248435#c63 appears to be reporting the same issue and that was reported on Sept 21st.
See https://bugs.chromium.org/p/chromium/issues/detail?id=1251673#c29 for the evidence that they're the same issue.

### ad...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

Unless there's been any issues or concerns of note since this has been on Canary, please go ahead and merge to M95 (branch 4638) and M94 (branch 4606) so the fixes can be included in the first stable and extended stable refreshes. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2e9b90efde2faeb80211eaf0b0077d160b33817a

commit 2e9b90efde2faeb80211eaf0b0077d160b33817a
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Wed Oct 13 18:26:12 2021

Merged: cppgc: Fix marking of ephemerons with keys in construction

Consider in-construction keys as live during the final GC pause.

(cherry picked from commit 32a09a6bce6cc75806dee5ec748bb1d081048fd0)

Bug: chromium:1259587
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ib1c490dcbc1d7e5a5b38947109fe0e8f7fe52002
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3234198
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.5@{#42}
Cr-Branched-From: 4a03d61accede9dd0e3e6dc0456ff5a0e3f792b4-refs/heads/9.5.172@{#1}
Cr-Branched-From: 9a607043cb3161f8ceae1583807bece595388108-refs/heads/main@{#76741}

[modify] https://crrev.com/2e9b90efde2faeb80211eaf0b0077d160b33817a/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/2e9b90efde2faeb80211eaf0b0077d160b33817a/src/heap/cppgc/marker.cc
[modify] https://crrev.com/2e9b90efde2faeb80211eaf0b0077d160b33817a/test/unittests/heap/cppgc/ephemeron-pair-unittest.cc


### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/656c2769c5803f19c238590154d05114b2f3a04c

commit 656c2769c5803f19c238590154d05114b2f3a04c
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Wed Oct 20 08:10:56 2021

Merged: cppgc: Fix marking of ephemerons with keys in construction

Revision: 32a09a6bce6cc75806dee5ec748bb1d081048fd0

BUG=chromium:1259587
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=dinfuehr@chromium.org

Change-Id: Ief330b4b71705c16bc61a3aca6d3aa1db172cdf3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3234200
Reviewed-by: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.4@{#46}
Cr-Branched-From: 3b51863bc25492549a8bf96ff67ce481b1a3337b-refs/heads/9.4.146@{#1}
Cr-Branched-From: 2890419fc8fb9bdb507fdd801d76fa7dd9f022b5-refs/heads/master@{#76233}

[modify] https://crrev.com/656c2769c5803f19c238590154d05114b2f3a04c/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/656c2769c5803f19c238590154d05114b2f3a04c/src/heap/cppgc/marker.cc
[modify] https://crrev.com/656c2769c5803f19c238590154d05114b2f3a04c/test/unittests/heap/cppgc/ephemeron-pair-unittest.cc


### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Hi, Cassidy Kim- just for awareness and full disclosure, despite this issue being the same as https://crbug.com/chromium/1251673, which was reported earlier than this report (in follow-up of https://crbug.com/chromium/1248435, on 21 September) we have decided to go against our normal rules and precedent in this specific case and extend VRP rewards for both reports. Your initial report (https://crbug.com/chromium/1252878) was instrumental in allowing for the issue to be reproduced by our teams and root cause to be identified, which is why we have decided in the interest in utmost fairness that both reports could be eligible for a reward in this case.

We have decided to award you $7500 for this report. We greatly appreciate the time and efforts you took to not only test the patch, but modify the POC in order and determine the issue had not been fully resolved. Thank you and nice work! 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-28)

[Empty comment from Monorail migration]

### eu...@chromium.org (2021-10-29)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-29)

I don't think the LTS M90 is necessary.

The library has only been enabled on M94, so while some code is present it is never used in production. There's also no runtime flag to turn it on.

### eu...@chromium.org (2021-10-29)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### rz...@google.com (2021-11-04)

Labelling as not applicable as the library was only enabled in M94

### am...@google.com (2021-11-23)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-12-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7d79acbd12d59e54be23c5b17245d797a7f19bde

commit 7d79acbd12d59e54be23c5b17245d797a7f19bde
Author: Hannes Payer <hpayer@chromium.org>
Date: Mon Dec 20 13:15:37 2021

Merged: cppgc: Fix marking of ephemerons with keys in construction

Revision: 4feccb9b4e4ac2accc92dd24b17f6b2f12611354

BUG=chromium:1259587
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: I941058dedebdde5c2d4567a57a953a2ce212e4d3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3350459
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Hannes Payer <hpayer@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.6@{#44}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/7d79acbd12d59e54be23c5b17245d797a7f19bde/src/heap/cppgc/marking-state.h
[modify] https://crrev.com/7d79acbd12d59e54be23c5b17245d797a7f19bde/src/heap/cppgc/marker.cc
[modify] https://crrev.com/7d79acbd12d59e54be23c5b17245d797a7f19bde/test/unittests/heap/cppgc/ephemeron-pair-unittest.cc


### va...@chromium.org (2021-12-20)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### is...@google.com (2022-12-13)

This issue was migrated from crbug.com/chromium/1259587?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1251673, crbug.com/chromium/1261570]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057594)*
