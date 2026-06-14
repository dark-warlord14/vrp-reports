# UNKNOWN in v8::internal::Invoke

| Field | Value |
|-------|-------|
| **Issue ID** | [40081058](https://issues.chromium.org/issues/40081058) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | bm...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5088721534713856

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x4494000419c0
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Regressed: V8: r25838:25880

Minimized Testcase (8.76 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96xjlLSUBlUas90eD_NbR2qBEyARJoZ3Ea45JX367bcLqvgX8R5IW7eUg5z9Q9iycITBb0vXT8NKL1e-qojuvJBh5uMtksy26M2gHBeaYCWkGkjHa4V4jWBKmsTNaUCoppKnUtzyfOp70ySLUM9FidUwJlGSA

Filer: mbarbella

## Timeline

### mb...@chromium.org (2014-12-22)

This is a variant of the test from https://crbug.com/chromium/443744, but it's still crashing in r25912. bmeurer, could you please take a look at this when you get a chance?

### cl...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3f00ce2d5933c29660d179e3a7060191fd1a59cd

commit 3f00ce2d5933c29660d179e3a7060191fd1a59cd
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Tue Dec 23 06:53:37 2014

[turbofan] Fix missing ChangeUint32ToUint64 in lowering of LoadBuffer.

TEST=mjsunit/compiler/regress-444695
BUG=chromium:444695
LOG=y
R=hpayer@chromium.org

Review URL: https://codereview.chromium.org/824843002

Cr-Commit-Position: refs/heads/master@{#25932}

[modify] http://crrev.com/3f00ce2d5933c29660d179e3a7060191fd1a59cd/src/compiler/simplified-lowering.cc
[add] http://crrev.com/3f00ce2d5933c29660d179e3a7060191fd1a59cd/test/mjsunit/compiler/regress-444695.js


### in...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-24)

ClusterFuzz has detected this issue as fixed in range 25929:25932.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5088721534713856

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8_dbg

Crash Type: UNKNOWN
Crash Address: 0x4494000419c0
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Regressed: V8: r25838:25880
Fixed: V8: r25929:25932

Minimized Testcase (8.76 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96xjlLSUBlUas90eD_NbR2qBEyARJoZ3Ea45JX367bcLqvgX8R5IW7eUg5z9Q9iycITBb0vXT8NKL1e-qojuvJBh5uMtksy26M2gHBeaYCWkGkjHa4V4jWBKmsTNaUCoppKnUtzyfOp70ySLUM9FidUwJlGSA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-29)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-29)

Approved for M40 (branch: 2214)

### in...@chromium.org (2015-01-02)

Please merges these fixes to M40 (branch: 2214) asap. The branch will be cut soon for M40 release.

### in...@chromium.org (2015-01-05)

Can this result in a OOB write ? or is it just read.

### bm...@chromium.org (2015-01-07)

This applies to reads only.

### bm...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratulations - $3500 for this report. Notes from panel: "$3000 for bug, +$500 ClusterFuzz Bonus".

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-31)

Bulk update: removing view restriction from closed bugs.

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/444695?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081058)*
