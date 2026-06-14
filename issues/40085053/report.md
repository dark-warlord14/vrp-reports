# Use-after-poison in blink::CrossThreadPersistentRegion::shouldTracePersistentNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40085053](https://issues.chromium.org/issues/40085053) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Mac |
| **Reporter** | th...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-08-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5170535808106496

Fuzzer: therealholden_worker
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ecde1ce8338
Crash State:
  blink::CrossThreadPersistentRegion::shouldTracePersistentNode
  blink::PersistentRegion::tracePersistentNodes
  blink::ThreadHeap::visitPersistentRoots
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=409589:409828

Minimized Testcase (2.28 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96jXqJu43my6uL7cwZa8coxo3lgrj3uliw7eiNxhHJ3kKAhFCWlyZRVcA2zeA01zBYzMOgd3XD_2HEqrHwl4k9ZHJ-R29j94HxFbpgbTQf4_qYbyszE6Bcd_UFMzUmqlvw2uJ-V0FAscTevs3XMm6nNtufEww?testcase_id=5170535808106496

Additional requirements: Requires HTTP

Issue manually filed by: mbarbella

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-09)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-08-09)

sigbjornf, mind taking a look at this one?

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### [Deleted User] (2016-08-09)

If CrossThreadPersistent<>s will be increasingly kept as fields on Blink GCed objects, then requiring all of those to be eagerly finalized, seems unworkable.

Hence, CrossThreadPersistentRegion::shouldTracePersistentNode() will at times be working over nodes that point into heap pages that will be lazily swept. So we'll have to exempt shouldTrace*() from ASan sanitization, as those lazily swept heap pages will have been poisoned by Oilpan.

### bu...@chromium.org (2016-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c00a99cd755fb8d985d811fef885a3dcf446abf2

commit c00a99cd755fb8d985d811fef885a3dcf446abf2
Author: sigbjornf <sigbjornf@opera.com>
Date: Wed Aug 10 06:24:46 2016

ASan-exempt CrossThreadPersistentRegion::shouldTracePersistentNode().

CrossThreadPersistent<T>s can reside on heap objects which are lazily
swept. Consequently, when a (per-)thread GC runs and it iterates over the
CrossThreadPersistentRegion to determine what nodes point into its heaps,
it can in the general case also touch lazily sweepable heap objects.

This is a benign read access to a region of memory that Oilpan has poisoned;
therefore, shouldTracePersistentNode() must be exempt from ASan checks to
prevent false negatives from being caught and reported.

R=
BUG=635574

Review-Url: https://codereview.chromium.org/2230623002
Cr-Commit-Position: refs/heads/master@{#410980}

[modify] https://crrev.com/c00a99cd755fb8d985d811fef885a3dcf446abf2/third_party/WebKit/Source/platform/heap/PersistentNode.h


### [Deleted User] (2016-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-08-11)

ClusterFuzz has detected this issue as fixed in range 410309:410323.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5170535808106496

Fuzzer: therealholden_worker
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ecde1ce8338
Crash State:
  blink::CrossThreadPersistentRegion::shouldTracePersistentNode
  blink::PersistentRegion::tracePersistentNodes
  blink::ThreadHeap::visitPersistentRoots
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=409589:409828
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=410309:410323

Minimized Testcase (2.28 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96jXqJu43my6uL7cwZa8coxo3lgrj3uliw7eiNxhHJ3kKAhFCWlyZRVcA2zeA01zBYzMOgd3XD_2HEqrHwl4k9ZHJ-R29j94HxFbpgbTQf4_qYbyszE6Bcd_UFMzUmqlvw2uJ-V0FAscTevs3XMm6nNtufEww?testcase_id=5170535808106496

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### [Deleted User] (2016-08-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

Another $3,500 courtesy of your fuzzer!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/635574?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/638574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085053)*
