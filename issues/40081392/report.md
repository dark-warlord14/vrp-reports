# Heap-buffer-overflow in opj_dwt_decode

| Field | Value |
|-------|-------|
| **Issue ID** | [40081392](https://issues.chromium.org/issues/40081392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ha...@hboeck.de |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-02-11 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.35 Safari/537.36

Steps to reproduce the problem:
1. run attached pdf through pdfium_test (compiled with asan)
2. will crash and show invalid memory read access (full asan debugging output attached)

What is the expected behavior?

What went wrong?
Shouldn't access invalid memory.

Did this work before? N/A 

Chrome version: 41.0.2272.35  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [pdfium-overflow-opj_dwt_interleave_h.pdf](attachments/pdfium-overflow-opj_dwt_interleave_h.pdf) (application/pdf, 1.0 KB)
- [pdfium-overflow-opj_dwt_interleave_h.pdf.asan.txt](attachments/pdfium-overflow-opj_dwt_interleave_h.pdf.asan.txt) (text/plain, 55.1 KB)

## Timeline

### cl...@chromium.org (2015-02-11)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5643077000101888

### js...@chromium.org (2015-02-11)

Verified. CF is working out the regression range.

### js...@chromium.org (2015-02-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5643077000101888

Uploader: jschuh@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x6090000343d4
Crash State:
  opj_dwt_decode
  opj_tcd_decode_tile
  opj_j2k_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=299683:299856

Minimized Testcase (1.03 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963b2D441MB78t9SUIgh_20Deeht3cWOtjVmJT0s1R9UuPhlXRZgy9IkTrhWq7PHrcM3wrZuyGCBOtCE6WGVltJ5yGmzZgBT3AovgmvDvzK0caM5DBinZv2cL1tSfmybW34uZkk-8phRq2tCRygld1XMxrojA



### cl...@chromium.org (2015-02-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-25)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-11)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-27)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 44 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-12)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 60 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-13)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-04-17)

It's an open-jpeg issue tracked in http://code.google.com/p/openjpeg/issues/detail?id=486.

### ti...@google.com (2015-06-15)

@Jun - same for this one.

### in...@chromium.org (2015-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-08)

I vote for also fixing this in our copy of openjpeg since upstream hasn't responded.

### ju...@foxitsoftware.com (2015-09-14)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-09-14)

It's pending in https://codereview.chromium.org/1338973005/.

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-10-13)

Fixed in https://pdfium.googlesource.com/pdfium/+/c212b684cb028a5d98e57f711c9eed931b853a44.

### cl...@chromium.org (2015-10-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e7df2d7d0c7a185834722cea42589caefd44da96

commit e7df2d7d0c7a185834722cea42589caefd44da96
Author: thestig <thestig@chromium.org>
Date: Wed Oct 14 00:11:11 2015

Roll PDFium 3acb1ef..24c1eec

https://pdfium.googlesource.com/pdfium.git/+log/3acb1ef..24c1eec

BUG=457480,497355
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1397173005

Cr-Commit-Position: refs/heads/master@{#353919}

[modify] http://crrev.com/e7df2d7d0c7a185834722cea42589caefd44da96/DEPS


### th...@chromium.org (2015-10-14)

tsepez: Do you know how long it takes for ClusterFuzz to verify the fix? Assuming it tries. Same for https://crbug.com/chromium/497355.

### oc...@chromium.org (2015-10-14)

Looks like this one errored out a few months ago while retrying the fixed testing. You can manually trigger this on testcases by doing Redo -> Fixed on the testcase page (I've done this).

### cl...@chromium.org (2015-10-14)

ClusterFuzz has detected this issue as fixed in range 353893:353966.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5643077000101888

Uploader: jschuh@google.com
Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x6090000343d4
Crash State:
  opj_dwt_decode
  opj_tcd_decode_tile
  opj_j2k_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=353893:353966

Minimized Testcase (1.03 Kb): https://cluster-fuzz.appspot.com/download/AMIfv963b2D441MB78t9SUIgh_20Deeht3cWOtjVmJT0s1R9UuPhlXRZgy9IkTrhWq7PHrcM3wrZuyGCBOtCE6WGVltJ5yGmzZgBT3AovgmvDvzK0caM5DBinZv2cL1tSfmybW34uZkk-8phRq2tCRygld1XMxrojA

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### th...@chromium.org (2015-10-14)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-14)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ss...@google.com (2015-10-16)

Approved for M47 (branch 2526)

### th...@chromium.org (2015-10-16)

The fix is in the same commit as https://crbug.com/chromium/497355.

### bu...@chromium.org (2015-10-19)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79724

------------------------------------------------------------------
r79724 | thestig@google.com | 2015-10-19T23:17:35.296815Z

-----------------------------------------------------------------

### th...@chromium.org (2015-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-28)

Adding reward-topanel for consideration under the Chrome Reward Program. Details here: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2015-12-01)

Our reward panel decided to award you $3,000 for this report. Thanks for your efforts! I'll start payment later this week using your details that we already have.

We'll credit you in our release notes as "Hanno Böck". If you'd like to use another name for credit, update this bug or contact me at timwillis@ and I'll update the release notes.

Thanks again for your report!

### ha...@hboeck.de (2015-12-01)

Thanks. Name in release notes is fine.

I am aware that the Chrome Bug Bounty program allows redirecting money to an established charity and Google will double it. Who should I contact about that?

### ti...@google.com (2015-12-01)

That's me as well - feel free to start an email thread at your convenience. Cheers.

### ti...@google.com (2015-12-14)

Reward doubled and paid to charity today - thanks for being awesome Hanno!

### cl...@chromium.org (2016-01-19)

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

This issue was migrated from crbug.com/chromium/457480?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/506642]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081392)*
