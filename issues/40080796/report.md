# Heap-buffer-overflow in opj_jp2_apply_pclr

| Field | Value |
|-------|-------|
| **Issue ID** | [40080796](https://issues.chromium.org/issues/40080796) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | fu...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-11-05 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Loading the attached testcase.pdf in pdfium\_test causes a crash in libopenjpeg.

**VERSION**  

Chrome Version: Tested in the ASAN prebuild "asan-symbolized-linux-release-302783"  

Operating System: Linux debian 3.16-3-amd64 #1 SMP Debian 3.16.5-1 (2014-10-10) x86\_64 GNU/Linux

**REPRODUCTION CASE**  

The attached testcase.pdf reproduces the issue.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See the attached symbolised ASAN output in asan\_sym.log

## Attachments

- [asan_sym.log](attachments/asan_sym.log) (text/plain, 7.3 KB)
- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 34.9 KB)

## Timeline

### cl...@chromium.org (2014-11-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5649734646628352

### cl...@chromium.org (2014-11-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5649734646628352

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60900001c66c
Crash State:
  opj_jp2_apply_pclr
  opj_jp2_decode
  CJPX_Decoder::Init
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (34.91 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94vyQVOli2mmCBW6hNACeawFWwRtPFYwpY3qFP44iI826RJRYr7st9MOWlqcwN7fm2b0B0ZZPAKzo131Q6NvAnFZXMUN2xTgFCOpLlWPuEI9JMqCDXfODVInloJUOSjZ3P4Z51HqpGyph7nhDZa1sDq1UYmgWGT7f5LrYG1GqBEF4wkKXo



### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-13)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-11-13)

Hi Antonin, please take a look at this one. Thanks.

### cl...@chromium.org (2014-11-21)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bo...@foxitsoftware.com (2014-11-24)

Fixed in https://pdfium.googlesource.com/pdfium/+/4643533ca3dabe945fd174caf892a3ccb6cf2fd6

### cl...@chromium.org (2014-11-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### [Deleted User] (2014-12-16)

Change looks pretty big, is this absolutely required?  Also, has this made it to canary/dev yet?

### th...@chromium.org (2014-12-16)

There's 3 bugs depending on the same merge and the other 2 have approvals. :)
This has been on canary for 2-3 weeks now.

### bu...@chromium.org (2014-12-16)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=65928

------------------------------------------------------------------
r65928 | thestig@google.com | 2014-12-16T06:55:04.676426Z

-----------------------------------------------------------------

### cl...@chromium.org (2014-12-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5649734646628352

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60900001c66c
Crash State:
  opj_jp2_apply_pclr
  opj_jp2_decode
  CJPX_Decoder::Init
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (34.91 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94vyQVOli2mmCBW6hNACeawFWwRtPFYwpY3qFP44iI826RJRYr7st9MOWlqcwN7fm2b0B0ZZPAKzo131Q6NvAnFZXMUN2xTgFCOpLlWPuEI9JMqCDXfODVInloJUOSjZ3P4Z51HqpGyph7nhDZa1sDq1UYmgWGT7f5LrYG1GqBEF4wkKXo



### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$500 for this report... and it would have been another $500 if you used clusterfuzz, fuzztercluck! :)

### cl...@chromium.org (2015-03-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/430566?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080796)*
