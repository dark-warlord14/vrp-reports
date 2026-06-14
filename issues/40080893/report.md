# CHECK failure in CHECK(p->IsSmi()) failed: ../../v8/src/objects-debug.cc(32)

| Field | Value |
|-------|-------|
| **Issue ID** | [40080893](https://issues.chromium.org/issues/40080893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mv...@chromium.org |
| **Created** | 2014-11-20 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5804866499772416

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: CHECK failure
Crash Address: 
Crash State:
  CHECK(p->IsSmi()) failed: ../../v8/src/objects-debug.cc(32)
  
Regressed: V8: r25384:25389

Minimized Testcase (8.96 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94XSWvhQPsUIa-Rh12tkFkB2sM-cpkL_WIGuOUiKlfT5mnK_JF_3DXTCkAQKj_j0kCKxLBIenr9uPUv6v6KsLCMMoAwiUMUdbMxFqnS9kFZ2ltdLC-5ztlrnpVLmmVBDvtZlZTzsNoMAR2KYROx_9HAbZarMw

Filer: jarin

## Timeline

### ja...@chromium.org (2014-11-20)

[Empty comment from Monorail migration]

### mv...@chromium.org (2014-11-21)

Fix checked in: https://chromium.googlesource.com/v8/v8/+/3d58b82addcdc72755539631b1d5dc603a9b2135


### mv...@chromium.org (2014-11-21)

[Empty comment from Monorail migration]

### mv...@chromium.org (2014-11-24)

This can allow heap corruption in the v8 gc heap.

### cl...@chromium.org (2014-11-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-11-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-28)

ClusterFuzz has detected this issue as fixed in range 25451:25461.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5804866499772416

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: CHECK failure
Crash Address: 
Crash State:
  CHECK(p->IsSmi()) failed: ../../v8/src/objects-debug.cc(32)
  
Regressed: V8: r25384:25389
Fixed: V8: r25451:25461

Minimized Testcase (8.96 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94XSWvhQPsUIa-Rh12tkFkB2sM-cpkL_WIGuOUiKlfT5mnK_JF_3DXTCkAQKj_j0kCKxLBIenr9uPUv6v6KsLCMMoAwiUMUdbMxFqnS9kFZ2ltdLC-5ztlrnpVLmmVBDvtZlZTzsNoMAR2KYROx_9HAbZarMw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### in...@chromium.org (2015-01-07)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### mv...@chromium.org (2015-01-14)

This merge was done last week. https://codereview.chromium.org/831243005/

### in...@chromium.org (2015-01-14)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congrats (again!) - $3500 for this one. Notes: "$3000 for heap corruption, +$500 ClusterFuzz bonus.

### cl...@chromium.org (2015-02-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/435073?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080893)*
