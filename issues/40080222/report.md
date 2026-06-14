# Bad-cast to blink::IDBRequest from invalid vptrblink::GarbageCollectedFinalized<blink::IDBRequest>::finalizeGarbageCollectedObject;blink::HeapPage<blink::FinalizedHeapObjectHeader>::sweep;blink::ThreadHeap<blink::FinalizedHeapObjectHeader>::sweep

| Field | Value |
|-------|-------|
| **Issue ID** | [40080222](https://issues.chromium.org/issues/40080222) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ag...@chromium.org |
| **Created** | 2014-08-18 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5075602265604096

Fuzzer: Therealholden_worker
Job Type: Linux_ubsan_vptr_chrome

Crash Type: Bad-cast
Crash Address: 0x1fae36a7eeb0
Crash State:
  Bad-cast to blink::IDBRequest from invalid vptrblink::GarbageCollectedFinalized<blink::IDBRequest>::finalizeGarbageCollectedObject
  blink::HeapPage<blink::FinalizedHeapObjectHeader>::sweep
  blink::ThreadHeap<blink::FinalizedHeapObjectHeader>::sweep
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=289947:290109

Minimized Testcase (1.25 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963RxHJXUqi6pNb2dl7K073-kVz3_hg8aiUKdC2mOe3Q1JQDRFMxCuRunQspZcS6OnYS_FzffsyCxMq08KMw-t5OAsynYjgDn8SfqJqUFqsD4fb6qrEbMclXug93g9LUqqKDFKQXAvwoIc4GJo5zXk8sITnoA

Filer: inferno

## Timeline

### in...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-18)

looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=180335

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ag...@chromium.org (2014-08-19)

This is definitely a regression caused by that change. I see the issue and will upload fix shortly.

### ag...@chromium.org (2014-08-19)

The regressing CL is in the M38 branch and we therefore have to merge this to branch 2125 once the fix is in.

### bu...@chromium.org (2014-08-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180528

------------------------------------------------------------------
r180528 | ager@chromium.org | 2014-08-19T07:37:52.853548Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/Visitor.h?r1=180528&r2=180527&pathrev=180528
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/HeapTest.cpp?r1=180528&r2=180527&pathrev=180528

Oilpan: Fix conservative marking of objects with uninitialized vtables.

I used Visitor::markNoTracing but that is only implemented for
the object pointer and not for header pointers. This change
implements markNoTracing for header pointers and adds a regression
test.

R=oilpan-reviews@chromium.org, wibling@chromium.org, zerny@chromium.org
BUG=404511

Review URL: https://codereview.chromium.org/487683002
-----------------------------------------------------------------

### ag...@chromium.org (2014-08-19)

Requesting merge to M38 branch. The regression cause is clear and the fix is tiny and localized.

### cl...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-19)

Lets keep in status=Fixed, needed for security tracking purposes.

### cl...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-20)

Is https://cluster-fuzz.appspot.com/testcase?key=6604331903090688 a duplicate ??

### ag...@chromium.org (2014-08-20)

Yes, that is a duplicate.

### cl...@chromium.org (2014-08-20)

ClusterFuzz has detected this issue as fixed in range 290523:290723.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5075602265604096

Fuzzer: Therealholden_worker
Job Type: Linux_ubsan_vptr_chrome

Crash Type: Bad-cast
Crash Address: 0x1fae36a7eeb0
Crash State:
  Bad-cast to blink::IDBRequest from invalid vptrblink::GarbageCollectedFinalized<blink::IDBRequest>::finalizeGarbageCollectedObject
  blink::HeapPage<blink::FinalizedHeapObjectHeader>::sweep
  blink::ThreadHeap<blink::FinalizedHeapObjectHeader>::sweep
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=289947:290109
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=290523:290723

Minimized Testcase (1.25 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963RxHJXUqi6pNb2dl7K073-kVz3_hg8aiUKdC2mOe3Q1JQDRFMxCuRunQspZcS6OnYS_FzffsyCxMq08KMw-t5OAsynYjgDn8SfqJqUFqsD4fb6qrEbMclXug93g9LUqqKDFKQXAvwoIc4GJo5zXk8sITnoA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-08-20)

Mads, was this a security issue or a functional bug in oilpan implementation. Just want to make sure we are rewarding the reporter correctly.

### ag...@chromium.org (2014-08-20)

This is a security issue. We were not correctly marking an object during garbage collection. This means that we would flip one bit in an unrelated object (because we miscalculated the header of the object and would flip the bit in the object before) and we could garbage collect an object that was actually reachable. So, overall this could lead to use-after-free.

### [Deleted User] (2014-08-21)

@ager, have we verified that this is working on canary?

### ag...@chromium.org (2014-08-21)

We have verified using these reproducible cases from clusterfuzz. The bug is obvious once you see it and the fix is as well (and it is a two line change).

On Canary, this will give very rare crashes where it is not clear at all that this bug is causing it. So it will be hard to verify on Canary (I haven't been able to find a crash on the canaries that are clearly caused by this). 

We should merge this ASAP. I don't believe there is any risk in the merge and it fixes a security issue.

### [Deleted User] (2014-08-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-22)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180761

------------------------------------------------------------------
r180761 | ager@chromium.org | 2014-08-22T07:15:34.124947Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/platform/heap/Visitor.h?r1=180761&r2=180760&pathrev=180761
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/platform/heap/HeapTest.cpp?r1=180761&r2=180760&pathrev=180761

Merge 180528 "Oilpan: Fix conservative marking of objects with u..."

> Oilpan: Fix conservative marking of objects with uninitialized vtables.
> 
> I used Visitor::markNoTracing but that is only implemented for
> the object pointer and not for header pointers. This change
> implements markNoTracing for header pointers and adds a regression
> test.
> 
> R=oilpan-reviews@chromium.org, wibling@chromium.org, zerny@chromium.org
> BUG=404511
> 
> Review URL: https://codereview.chromium.org/487683002

TBR=ager@chromium.org

Review URL: https://codereview.chromium.org/495303002
-----------------------------------------------------------------

### ti...@chromium.org (2014-10-07)

therealholden@ - $3500 for this bug under our new reward levels. $3000 for the bug, plus $500 for the fuzzer running on ClusterFuzz.

### cl...@chromium.org (2014-11-25)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/404511?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/404880]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080222)*
