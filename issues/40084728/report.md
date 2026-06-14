# Heap-buffer-overflow in CWeightTable::Calc

| Field | Value |
|-------|-------|
| **Issue ID** | [40084728](https://issues.chromium.org/issues/40084728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-06-29 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4580419215556608

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x7fb7dcdfc004
Crash State:
  CWeightTable::Calc
  CStretchEngine::StartStretchHorz
  CFX_ImageStretcher::StartStretch
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=393856:393893

Minimized Testcase (4.13 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96K80q4u40O_HAo6b2Cg0D1rYfwb3ORucxXErxkKgVG-2eRiC8D1TqoAl7OGqkQ8upW9xDQXzg1EKfE3g-UftF3EnjQcnjV-mTlK0x8Ln20ToSQ5sHyRaN19pEB6tlcxSGhRkgm2E_UGXQP1pxm4tN6q3kgKg?testcase_id=4580419215556608

Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### pa...@chromium.org (2016-06-29)

thestig: Could you please handle this or re-assign it to someone who can? Thank you!

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2016-06-30)

Well, I tried fixing the indexing to be more sane, but now some images don't display correctly. I'll keep looking.

### cl...@chromium.org (2016-06-30)

ClusterFuzz has detected this issue as fixed in range 398351:398496.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4580419215556608

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x7fb7dcdfc004
Crash State:
  CWeightTable::Calc
  CStretchEngine::StartStretchHorz
  CFX_ImageStretcher::StartStretch
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=393856:393893
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=398351:398496

Minimized Testcase (4.13 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96K80q4u40O_HAo6b2Cg0D1rYfwb3ORucxXErxkKgVG-2eRiC8D1TqoAl7OGqkQ8upW9xDQXzg1EKfE3g-UftF3EnjQcnjV-mTlK0x8Ln20ToSQ5sHyRaN19pEB6tlcxSGhRkgm2E_UGXQP1pxm4tN6q3kgKg?testcase_id=4580419215556608

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-30)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-02)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

M53 beta launch is coming soon.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Monday (07/18/16). Thank you.

### sh...@chromium.org (2016-07-16)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2016-07-19)

M53 beta launch is next week.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Friday (07/22/16). Thank you.

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-21)

ReleaseBlock-Stable after discussion with thestig@

### sh...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-30)

thestig: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2016-08-02)

https://codereview.chromium.org/2204773003/

### go...@chromium.org (2016-08-03)

M53 Stable launch is coming soon.Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix asap so it gets chance to bake in beta before stable promotion. Thank you.

### th...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8c5429e3337f1635fee44eb51d4c9330d05e54db

commit 8c5429e3337f1635fee44eb51d4c9330d05e54db
Author: thestig <thestig@chromium.org>
Date: Thu Aug 04 23:07:09 2016

Roll PDFium a72ab5e..32e693f

https://pdfium.googlesource.com/pdfium.git/+log/a72ab5e..32e693f

BUG=634394,624514
TBR=tsepez@chromium.org

Review-Url: https://codereview.chromium.org/2210063004
Cr-Commit-Position: refs/heads/master@{#409927}

[modify] https://crrev.com/8c5429e3337f1635fee44eb51d4c9330d05e54db/DEPS


### th...@chromium.org (2016-08-05)

Will request the merge on Monday.

### sh...@chromium.org (2016-08-07)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-07)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-08-08)

+awhalley@, is this good to take in for this week M53 Beta release?

### aw...@chromium.org (2016-08-09)

Yep, good for M53, along with the other bugs bugs that have a PDFium roll: 624514, 628304, 628890

### go...@chromium.org (2016-08-09)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/624514#c25. Please merge ASAP (latest by tomorrow, Tuesday 3:00 PM PT) so we can take it in for this week beta release.

### bu...@chromium.org (2016-08-09)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/205c3faca7f4c678fddf6e3811ec6fe9b0fd7031

commit 205c3faca7f4c678fddf6e3811ec6fe9b0fd7031
Author: Oliver Chang <ochang@google.com>
Date: Tue Aug 09 16:01:16 2016


### aw...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

$3,500 for this one - good to see the fuzzer churning out great bugs.  Thanks.

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2017-09-18)

We have made a bunch of changes on ClusterFuzz side, so resetting ClusterFuzz-Wrong label.

### is...@google.com (2017-09-18)

This issue was migrated from crbug.com/chromium/624514?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084728)*
