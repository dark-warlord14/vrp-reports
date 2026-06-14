# Use-of-uninitialized-value in blink::Member<blink::IDBKey>* blink::HeapAllocator::allocateVectorBacking<b

| Field | Value |
|-------|-------|
| **Issue ID** | [40081647](https://issues.chromium.org/issues/40081647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2015-03-18 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4709697483964416

Fuzzer: Therealholden_worker
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::IDBKey>* blink::HeapAllocator::allocateVectorBacking<b
  void WTF::Vector<blink::HeapVector<blink::Member<blink::IDBKey>, 0ul>, 0ul,
  blink::IDBObjectStore::put
  

Minimized Testcase (3.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9421tY_GqjFTLN0Xg2IBR7GGoCEvIaqwriwSVshE6Rd16avzpM5JndjdQG31KKrlEN6NDUEwku6URs-nHQ0QGKHzeHZviL7YCV8P0Ucg8btkxdku6579yDP7FzZwcIE7f_i8qJb3VmYaFIIdFXySIVpUA86Kg

Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5603679239929856

Fuzzer: Therealholden_worker
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::FileReader>* blink::HeapAllocator::allocateVectorBacki
  blink::FileReader::ThrottlingController::pushReader
  blink::FileReader::ThrottlingController::pushReader
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=320471:320682

Minimized Testcase (1.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94wrlQlMCGS7xOXsZfll-2-v9PNSP9e9CjVb7yP4qYRDt37OGPqMY2-E8vmBQb_KJj977P4BbGOqs5iAgEtdqOETaJJnDSAmAP7G8j_zbZFATKchJnMiiQx1Lfv9IzPGCgj_cpF-qvscV1X0OOrjlANMR7Vow

Additional requirements: Requires HTTP

Filer: inferno

### cl...@chromium.org (2015-03-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4771801033342976

Fuzzer: Inferno_layout_test_unmodified
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::EntrySync>* blink::HeapAllocator::allocateVectorBackin
  blink::DirectoryReaderSync::EntriesCallbackHelper::handleEvent
  blink::EntriesCallbacks::didReadDirectoryEntries
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=320682:320684

Minimized Testcase (2.99 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97uUx2e086BptewOKRn7c-kGZsiL2heUVWIXaEJEcdQECMdg6UPn_WQ1LcE5bocrhYkiBJoqVrNg8G8p6Y53ZhhARbuPgJp0sko-tEjiGR1jMM5N99Pbh3ezRTu3LZvXWpkwTArxsF2ZjYERwIj_0aVZvlCbA

Filer: inferno

### in...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-03-21)

Let me take a look at this on Monday.


### bu...@chromium.org (2015-03-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192306

------------------------------------------------------------------
r192306 | sigbjornf@opera.com | 2015-03-21T13:32:46.467244Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/heap/ThreadState.cpp?r1=192306&r2=192305&pathrev=192306

Completely clear the heap ages array.

R=haraken
BUG=468166

Review URL: https://codereview.chromium.org/1021393004
-----------------------------------------------------------------

### cl...@chromium.org (2015-03-23)

ClusterFuzz has detected this issue as fixed in range 321712:321715.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4709697483964416

Fuzzer: Therealholden_worker
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::IDBKey>* blink::HeapAllocator::allocateVectorBacking<b
  void WTF::Vector<blink::HeapVector<blink::Member<blink::IDBKey>, 0ul>, 0ul,
  blink::IDBObjectStore::put
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=321712:321715

Minimized Testcase (3.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9421tY_GqjFTLN0Xg2IBR7GGoCEvIaqwriwSVshE6Rd16avzpM5JndjdQG31KKrlEN6NDUEwku6URs-nHQ0QGKHzeHZviL7YCV8P0Ucg8btkxdku6579yDP7FzZwcIE7f_i8qJb3VmYaFIIdFXySIVpUA86Kg

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-23)

ClusterFuzz has detected this issue as fixed in range 321712:321715.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5603679239929856

Fuzzer: Therealholden_worker
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::FileReader>* blink::HeapAllocator::allocateVectorBacki
  blink::FileReader::ThrottlingController::pushReader
  blink::FileReader::ThrottlingController::pushReader
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=320471:320682
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=321712:321715

Minimized Testcase (1.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94wrlQlMCGS7xOXsZfll-2-v9PNSP9e9CjVb7yP4qYRDt37OGPqMY2-E8vmBQb_KJj977P4BbGOqs5iAgEtdqOETaJJnDSAmAP7G8j_zbZFATKchJnMiiQx1Lfv9IzPGCgj_cpF-qvscV1X0OOrjlANMR7Vow

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-23)

ClusterFuzz has detected this issue as fixed in range 321712:321715.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4771801033342976

Fuzzer: Inferno_layout_test_unmodified
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Member<blink::EntrySync>* blink::HeapAllocator::allocateVectorBackin
  blink::DirectoryReaderSync::EntriesCallbackHelper::handleEvent
  blink::EntriesCallbacks::didReadDirectoryEntries
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=320682:320684
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=321712:321715

Minimized Testcase (2.99 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97uUx2e086BptewOKRn7c-kGZsiL2heUVWIXaEJEcdQECMdg6UPn_WQ1LcE5bocrhYkiBJoqVrNg8G8p6Y53ZhhARbuPgJp0sko-tEjiGR1jMM5N99Pbh3ezRTu3LZvXWpkwTArxsF2ZjYERwIj_0aVZvlCbA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### [Deleted User] (2015-03-23)

Due to https://chromium.googlesource.com/chromium/blink/+/f2df8bbb03baf6a236e59c237d11f05ac3f542d3 

(=> M43 only ?)

### in...@chromium.org (2015-03-23)

Ok.

### ti...@google.com (2015-06-14)

Congrats - $1500 for this report ($1000 for the bug + $500 ClusterFuzz bonus).

We'll start payment via our new process, which should take 1-2 weeks. That 1-2 week period payment time frame starts from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

Reward being paid via our new process - you should receive payment within 2 weeks.

### cl...@chromium.org (2015-06-29)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/468166?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081647)*
