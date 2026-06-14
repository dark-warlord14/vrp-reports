# UNKNOWN in _CMapLookupCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40082690](https://issues.chromium.org/issues/40082690) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-08-18 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5084391036944384

Fuzzer: ochang_neurofuzz_borgfuzz
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x6080000196f0
Crash State:
  _CMapLookupCallback
  CFX_BaseSegmentedArray::IterateIndex
  CFX_BaseSegmentedArray::Iterate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=325288:325416

Minimized Testcase (54.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95sYjbR2n0BQ0FLTXEp41JegooyTe-W-5kIIxi5rbflXbVixBji6ToRXfygA7Vq_xOcrlaI-_8kUwwLDQXXfJ-kwSr3F1c9opoqxsRXJ2B4gDmzCbxcBYFm4H391BSOPbhZFvwY6SAGrDvzSWKkpt0R0fiDPnsIwHG8uBSaIWYv02T9hfU

Filer: mbarbella

## Timeline

### es...@chromium.org (2015-08-18)

tsepez@, do you think you might be able to help find an owner for this?

### cl...@chromium.org (2015-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-08-21)

-->tsepez, per offline conversation

### cl...@chromium.org (2015-09-02)

tsepez@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-09-03)

Is the plan to get rid of CFX_CMapByteStringToPtr here? From writing a few tests, it appears the container is basically a std::map<std::string, std::queue<T>>, with SetAt() modifying the head of the queue, and AddValue() adding to the queue.

### th...@chromium.org (2015-09-03)

Oh, I think I found the actual problem - we did an invalid cast :(

### th...@chromium.org (2015-09-03)

https://codereview.chromium.org/1327913002/

### th...@chromium.org (2015-09-03)

FYI, reporter "attekett" stumbled on to this in https://code.google.com/p/chromium/issues/detail?id=472506#c11 a week before CF.

### mb...@chromium.org (2015-09-03)

Adding reward-topanel based on c#9.

### th...@chromium.org (2015-09-03)

Just landed https://codereview.chromium.org/1327913002/

Will roll DEPS for Chromium now. Will start the cherry-picking process starting with M46 on Monday unless someone else wants to expedite this.


### bu...@chromium.org (2015-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b68f5c2b1cf7fe850312b49804af3a14472aa021

commit b68f5c2b1cf7fe850312b49804af3a14472aa021
Author: thestig <thestig@chromium.org>
Date: Thu Sep 03 22:39:34 2015

Roll PDFium 7c9e452..640c395

https://pdfium.googlesource.com/pdfium.git/+log/7c9e452..640c395

BUG=522131
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1307343004

Cr-Commit-Position: refs/heads/master@{#347271}

[modify] http://crrev.com/b68f5c2b1cf7fe850312b49804af3a14472aa021/DEPS


### th...@chromium.org (2015-09-04)

Fixed on trunk

### cl...@chromium.org (2015-09-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-09-08)

And Monday was a holiday, so requesting the merge today.

### pe...@google.com (2015-09-08)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@google.com (2015-09-09)

Merge approved for M46 (branch: 2490).
Pls note the DEPS changes in trunk is different from in release branch, and make sure you're comfortable to make the DEPS changes in release branch. Let me know if more info is needed.

### bu...@chromium.org (2015-09-09)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=78258

------------------------------------------------------------------
r78258 | thestig@google.com | 2015-09-09T00:56:33.932064Z

-----------------------------------------------------------------

### th...@chromium.org (2015-09-09)

Merged to M46. Will request the M45 merge on Thursday unless anything think we should expedite this.

### oc...@chromium.org (2015-09-09)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-10)

[Empty comment from Monorail migration]

### am...@google.com (2015-09-10)

Merge approved for M45 branch 2454.

### bu...@chromium.org (2015-09-10)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=78317

------------------------------------------------------------------
r78317 | thestig@google.com | 2015-09-10T19:10:03.921012Z

-----------------------------------------------------------------

### ti...@google.com (2015-10-12)

Adding Release-0-M46 so that this is captured in those release notes.

### ti...@google.com (2015-10-12)

Internal fuzzer.

### ti...@google.com (2015-10-12)

Wait, https://crbug.com/chromium/522131#c9.

### ti...@google.com (2015-10-13)

Congratulations @attekett - $3000 for this report.

I'll start the payment process later this week.

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-12-11)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/522131?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082690)*
