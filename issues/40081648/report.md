# Use-of-uninitialized-value in parse_font_matrix

| Field | Value |
|-------|-------|
| **Issue ID** | [40081648](https://issues.chromium.org/issues/40081648) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-03-18 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4950464961970176

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  parse_font_matrix
  parse_dict
  T1_Face_Init
  

Minimized Testcase (57.40 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97tSzF7EEWHlet4mRoKzZRGy6OZf-5NjJzO9YOob4l9ODGy6y_4Inw_zBpre5BqEk1O4mMmqxvLATQ6-JtU2VdaQuyai5yEPmp_uuii1whDUGukjIWvcM8vGTDi_-ywsgRszqCXDutwaS1aUSiLQI1GVfhoOfcY92hejYuCQmfhnptu5F4

Filer: inferno

## Timeline

### in...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-04-21)

Fixed in https://pdfium.googlesource.com/pdfium/+/672bd1706a990069dce401afead6c2ecfcdb3357.

### ju...@foxitsoftware.com (2015-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

Merge requested for M43 (branch 2357)

### ti...@google.com (2015-05-08)

[Empty comment from Monorail migration]

### la...@google.com (2015-05-08)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### la...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-05-11)

I'll do the merge.

### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=73326

------------------------------------------------------------------
r73326 | thestig@google.com | 2015-05-11T21:12:16.916094Z

-----------------------------------------------------------------

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

$500 for this report + $500 for the clusterfuzz bonus. Congrats!

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-07-29)

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

This issue was migrated from crbug.com/chromium/468167?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081648)*
