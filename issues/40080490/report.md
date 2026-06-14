# Heap-buffer-overflow in chrome_pdf::PDFiumEngine::GetPageRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40080490](https://issues.chromium.org/issues/40080490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ts...@chromium.org |
| **Created** | 2014-09-17 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5086083801939968

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xce011a3c
Crash State:
  chrome_pdf::PDFiumEngine::GetPageRect
  chrome_pdf::Instance::HandleInputEvent
  pp::InputEvent_HandleEvent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=277079:277175

Minimized Testcase (869.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957oI5FhgAtvVgYoIis7a2zRjHOjjRLTNh4OyOFE_NsK5x7jPNxQfBmZCLILt1jDwDMPMGEmApwFiKftJJEoL059W81sab0mDnXw7eMl4XaikhIRjbDLcsius1aLp6hp_HJTb83Ix0Gn9JQOfSeSQLEsbK2S9oL3nDYSVrZhpB3yp1DA2E

Additional requirements: Requires Gestures

Filer: inferno

## Timeline

### in...@chromium.org (2014-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-17)

Presumably need to check for engine_->GetFirstVisiblePage() returning -1 at or about instance.cc:522 and 533. This would be consistent with indexing 4 bytes before the vector storage on ARM when evaluating pages_[-1].  

I can't repro locally -- but I'll cobble up a speculative fix for this.

### ts...@chromium.org (2014-09-17)

CL at https://codereview.chromium.org/560133004/

### bu...@chromium.org (2014-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9b04ffd8e7a07e9b2947fe5b71acf85dff38a63f

commit 9b04ffd8e7a07e9b2947fe5b71acf85dff38a63f
Author: tsepez <tsepez@chromium.org>
Date: Thu Sep 18 05:35:57 2014

Let PDFium handle event when there is not yet a visible page.

Speculative fix for 415307. CF will confirm.
The stack trace for that bug indicates an attempt to index by -1, which is consistent with no visible page.

BUG=415307

Review URL: https://codereview.chromium.org/560133004

Cr-Commit-Position: refs/heads/master@{#295421}

[modify] https://chromium.googlesource.com/chromium/src.git/+/9b04ffd8e7a07e9b2947fe5b71acf85dff38a63f/pdf/instance.cc


### cl...@chromium.org (2014-09-18)

ClusterFuzz has detected this issue as fixed in range 295414:295429.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5086083801939968

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xce011a3c
Crash State:
  chrome_pdf::PDFiumEngine::GetPageRect
  chrome_pdf::Instance::HandleInputEvent
  pp::InputEvent_HandleEvent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=277079:277175
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=295414:295429

Minimized Testcase (869.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957oI5FhgAtvVgYoIis7a2zRjHOjjRLTNh4OyOFE_NsK5x7jPNxQfBmZCLILt1jDwDMPMGEmApwFiKftJJEoL059W81sab0mDnXw7eMl4XaikhIRjbDLcsius1aLp6hp_HJTb83Ix0Gn9JQOfSeSQLEsbK2S9oL3nDYSVrZhpB3yp1DA2E

Additional requirements: Requires Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-18)

clicked redo on fixed, since there is no pdf change in fixed range.

### cl...@chromium.org (2014-09-18)

ClusterFuzz has detected this issue as fixed in range 295414:295429.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5086083801939968

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xce011a3c
Crash State:
  chrome_pdf::PDFiumEngine::GetPageRect
  chrome_pdf::Instance::HandleInputEvent
  pp::InputEvent_HandleEvent
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=277079:277175
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=295414:295429

Minimized Testcase (869.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957oI5FhgAtvVgYoIis7a2zRjHOjjRLTNh4OyOFE_NsK5x7jPNxQfBmZCLILt1jDwDMPMGEmApwFiKftJJEoL059W81sab0mDnXw7eMl4XaikhIRjbDLcsius1aLp6hp_HJTb83Ix0Gn9JQOfSeSQLEsbK2S9oL3nDYSVrZhpB3yp1DA2E

Additional requirements: Requires Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ts...@chromium.org (2014-09-18)

@inferno - fix is on the chrome side at https://chromium.googlesource.com/chromium/src/+/9b04ffd8e7a07e9b2947fe5b71acf85dff38a63f

### in...@chromium.org (2014-09-18)

ah! great! Thanks Tom, your speculative fix nailed it :)

### cl...@chromium.org (2014-09-18)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

Matthew - Merge requested for M38 (branch 2125)

### [Deleted User] (2014-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2014-09-23)

Approved for 38.

### ti...@chromium.org (2014-09-24)

tsepez@ - please merge to M38 (branch 2125)

### ts...@chromium.org (2014-09-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5f8a65e99ec9add1fbef4759e8109711d9b7582f

commit 5f8a65e99ec9add1fbef4759e8109711d9b7582f
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 25 18:31:42 2014

Merge M38: Let PDFium handle event when there is not yet a visible page.

Speculative fix for 415307. CF will confirm.
The stack trace for that bug indicates an attempt to index by -1, which is consistent with no visible page.

BUG=415307
TBR=gene@chromium.org

Review URL: https://codereview.chromium.org/560133004

Cr-Commit-Position: refs/heads/master@{#295421}
(cherry picked from commit 9b04ffd8e7a07e9b2947fe5b71acf85dff38a63f)

Review URL: https://codereview.chromium.org/601343002

Cr-Commit-Position: refs/branch-heads/2125@{#480}
Cr-Branched-From: b68026d94bda36dd106a3d91a098719f952a9477-refs/heads/master@{#290040}

[modify] https://chromium.googlesource.com/chromium/src.git/+/5f8a65e99ec9add1fbef4759e8109711d9b7582f/pdf/instance.cc


### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations Atte - $1500 for this report. ($1000 baseline + $500 bonus for running this fuzzer on ClusterFuzz). We're paying a $500 ClusterFuzz bonus for any valid bug that is found using an external fuzzer on ClusterFuzz.


### ti...@google.com (2014-12-08)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-12-25)

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

This issue was migrated from crbug.com/chromium/415307?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/414096]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080490)*
