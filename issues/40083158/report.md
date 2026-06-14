# Heap-use-after-free in blink::LayoutBlock::removeChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40083158](https://issues.chromium.org/issues/40083158) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2015-11-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5636999954825216

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000056320
Crash State:
  blink::LayoutBlock::removeChild
  blink::LayoutObject::willBeDestroyed
  blink::LayoutBoxModelObject::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=356784:357082

Minimized Testcase (2.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95eTTR6kC7t6VSBDa-bMrCjDxucyIk7JHRvu_gCB_7INC2pzoswyTDj2EIrtJEuPi1ihlbpzWUyjwPn0z2cEK62PRcRKgRruWiqDlksbQWJpQodrnbsG_-Pcm4y4MXQiPmYWlJsCDjs1Stpy8oaeI4Nko6b8g

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-11-08)

Looks like a new repro that is still reproducing after all the other fixes. Robert, can you please take a look.

### cl...@chromium.org (2015-11-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-09)

Hey, a friendly reminder M48 branching is coming on Nov 13,and this bug is marked as a beta blocker. Please take a look and land a fix by Nov 11, so that your change can go through bake time on trunk/master before branching. Thanks!

### bu...@chromium.org (2015-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c6d1fbfdc27b3a15940b588ef1cd83a0ddcc0171

commit c6d1fbfdc27b3a15940b588ef1cd83a0ddcc0171
Author: robhogan <robhogan@gmail.com>
Date: Thu Nov 12 01:15:29 2015

Don't attempt to collapse anonymous children while destroying them

BUG=553048

Review URL: https://codereview.chromium.org/1411283012

Cr-Commit-Position: refs/heads/master@{#359202}

[add] http://crrev.com/c6d1fbfdc27b3a15940b588ef1cd83a0ddcc0171/third_party/WebKit/LayoutTests/fast/block/dont-collapse-anonymous-children-when-destroying-them-expected.txt
[add] http://crrev.com/c6d1fbfdc27b3a15940b588ef1cd83a0ddcc0171/third_party/WebKit/LayoutTests/fast/block/dont-collapse-anonymous-children-when-destroying-them.html
[modify] http://crrev.com/c6d1fbfdc27b3a15940b588ef1cd83a0ddcc0171/third_party/WebKit/Source/core/layout/LayoutBlock.cpp


### in...@chromium.org (2015-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-13)

ClusterFuzz has detected this issue as fixed in range 359182:359367.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5636999954825216

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000056320
Crash State:
  blink::LayoutBlock::removeChild
  blink::LayoutObject::willBeDestroyed
  blink::LayoutBoxModelObject::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=356784:357082
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=359182:359367

Minimized Testcase (2.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95eTTR6kC7t6VSBDa-bMrCjDxucyIk7JHRvu_gCB_7INC2pzoswyTDj2EIrtJEuPi1ihlbpzWUyjwPn0z2cEK62PRcRKgRruWiqDlksbQWJpQodrnbsG_-Pcm4y4MXQiPmYWlJsCDjs1Stpy8oaeI4Nko6b8g

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-11-23)

Looks like this just missed the M48 cut. Merge-requested to M48.

### ti...@google.com (2015-11-23)

[Automated comment] Commit may have occurred before M48 branch point (11/13/2015), needs manual review.

### ti...@google.com (2015-11-30)

This is already in M48 branch, no need to merge

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

(another backlog round bug) 

Miaubuz - another $3,500 to your tab. 

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/553048?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083158)*
