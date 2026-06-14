# Heap-buffer-overflow in opj_dwt_decode_1

| Field | Value |
|-------|-------|
| **Issue ID** | [40081235](https://issues.chromium.org/issues/40081235) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | ha...@hboeck.de |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-01-22 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36

Steps to reproduce the problem:
1. take the asan-prebuilt chrome package
2. run pdfium_test with attached pdf files, see asan crash report:

==6815==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x61500000def8 at pc 0x00000079409a bp 0x7fffedbc4b10 sp 0x7fffedbc4b08
==6816==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000c208 at pc 0x00000079409a bp 0x7fff7c160550 sp 0x7fff7c160548

I've attached asan debug output, however it seems it's not that useful, seems debugging symbols are missing from prebuilt pdfium.

What is the expected behavior?

What went wrong?
pdfium exposes out of bounds memory read access. That should never happen.

Did this work before? N/A 

Chrome version: 40.0.2214.85  Channel: beta
OS Version: 
Flash Version: Shockwave Flash 16.0 r0

## Attachments

- [crash2.pdf](attachments/crash2.pdf) (application/pdf, 10.6 KB)
- [test0.pdf](attachments/test0.pdf) (application/pdf, 1.1 KB)
- [crash2.pdf.asan.log](attachments/crash2.pdf.asan.log) (text/plain, 19.0 KB)
- [test0.pdf.asan.log](attachments/test0.pdf.asan.log) (text/plain, 54.5 KB)

## Timeline

### cl...@chromium.org (2015-01-22)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5667768262197248

### cl...@chromium.org (2015-01-22)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6148455717142528

### cl...@chromium.org (2015-01-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6148455717142528

Uploader: rickyz@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x61500000a7f8
Crash State:
  opj_dwt_decode_1
  opj_dwt_decode
  opj_tcd_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (10.63 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97tjRE2jBKZjDjzDSC2-HirgK3kxx5rEp9l4SQ20X_9czxelk0YwJbUhuXqod1qQARgNkBvxcl6pBcNooz_4sM0BHtzSjR7JfhDq2l0nnuJMJaIPmzmrWwzqX3EsnVFu0bayGm0T7LyWeAafS8ZV57i_u1i3w



### cl...@chromium.org (2015-01-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5667768262197248

Uploader: rickyz@chromium.org
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x609000000978
Crash State:
  opj_dwt_decode_1
  opj_dwt_decode
  opj_tcd_decode_tile
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (1.06 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95T-ivoOS3YJ_g5HXoINHxPR_qjqUX6oJRKPSzQK2tb2NiLGOlaAuJv0HOCntu4yfT9k-vTLDWWbNuX0rqFzz7w5yDBM2YjY7OHaJ2lSoH3axiS7w0v-wH1LWjt1N7P2kZG_dTNgSy68BUsgw0VdKcKhyZjcA



### in...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2015-01-23)

Jun will be in charge of these issues.

### ts...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-13)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-10)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 46 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-03-11)

It's an openjpeg issue and pending in https://code.google.com/p/openjpeg/issues/detail?id=480&thanks=480&ts=1426035078.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-07)

Does anyone on this thread have contacts with openjpeg? Jun submitted a patch with the report, so hopefully it should be straightforward to fix.

### oc...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-15)

Jun - do you know anyone over at openjpeg? If not, grateful if you could bump that bug (in #13).

### mj...@google.com (2015-06-26)

This bug was also reported in https://crbug.com/chromium/471797. Please see the latest comment in that bug entry -- it is subject to the Google Project Zero disclosure policy, with the 90 day period starting today.

### in...@chromium.org (2015-06-26)

Jun, can you merge this fix to pdfium asap. If upstream isn't responding, we can't just keep waiting on them. Lets take the patch locally in our branch.

### th...@chromium.org (2015-06-27)

I would also ping upstream again.

+tsepez

### ti...@google.com (2015-06-30)

@mjurczyk - can you please provide a link to the P0 bug tracker for reference (and provide access to timwillis@, inferno@ and mbarbella@).

### mj...@google.com (2015-07-01)

This issue is tracked in https://code.google.com/p/google-security-research/issues/detail?id=307 on the Project Zero side. We don't grant access to the bug tracker entries to people outside of our team prior to public access derestriction; however, that bug is used only for tracking purposes and doesn't contain any more technical information than the original report (i.e. offending sample and ASAN stack trace).

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-07-13)

So what's the plan here? Has anyone responded on the openjpeg bug? Shall we fix this in PDFium first?

### cl...@chromium.org (2015-07-23)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-13)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-08-13)

So... shall we just patch PDFium given the lack of response on the openjpeg bug?

### ts...@chromium.org (2015-08-19)

Jun, did you come up with a patch? Let's just do it locally.

### th...@chromium.org (2015-08-19)

The patch is attached to https://code.google.com/p/openjpeg/issues/detail?id=480

### ju...@foxitsoftware.com (2015-08-19)

OK. Let me do it locally. 

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-08-24)

It doesn't reproduce in the last version of pdfium. Lei, can you double check it in your side? 

### ju...@foxitsoftware.com (2015-08-24)

It can be reproduced in the embedded pdfium of chrome.

### ju...@foxitsoftware.com (2015-08-24)

[Comment Deleted]

### ju...@foxitsoftware.com (2015-08-29)

It's pending in https://codereview.chromium.org/1320443003/.

### ju...@foxitsoftware.com (2015-08-29)

Fixed in https://pdfium.googlesource.com/pdfium/+/463b77b4f1e4257cd89f3460b5a6fdb102f44265.

### th...@chromium.org (2015-08-29)

Let's start with a merge to M46.

### pe...@google.com (2015-08-29)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### cl...@chromium.org (2015-08-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6c00fdebe1395316fd3d3b2af9a1f30e8cef9de4

commit 6c00fdebe1395316fd3d3b2af9a1f30e8cef9de4
Author: thestig <thestig@chromium.org>
Date: Sat Aug 29 08:09:14 2015

Roll PDFium a2b3ae2..5e4a5cc

https://pdfium.googlesource.com/pdfium.git/+log/a2b3ae2..5e4a5cc

BUG=450844
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1310183013

Cr-Commit-Position: refs/heads/master@{#346314}

[modify] http://crrev.com/6c00fdebe1395316fd3d3b2af9a1f30e8cef9de4/DEPS


### ti...@google.com (2015-08-31)

+pennymac@ - want to make sure this was/is approved.

### ti...@google.com (2015-08-31)

Adding Merge-Triage to consider this for an M-45 patch release

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Merge approved for M46.
Also add the Merge-Review-46 label so that it can be triaged for M45 patch release by amineer@ 
[to timwillis@: pls use "Merge-Review-<mstone>" label for future ones to get them timely triaged :-) ]

### pe...@google.com (2015-08-31)

We're going to leave the decision to request merges to the developer (and security team) Tina.  They only requested M46 at this point.

### bu...@chromium.org (2015-08-31)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=77986

------------------------------------------------------------------
r77986 | thestig@google.com | 2015-08-31T19:08:30.005655Z

-----------------------------------------------------------------

### th...@chromium.org (2015-08-31)

Merge to M46? Should I set some more labels for M45?

### th...@chromium.org (2015-09-03)

And finally merge to M45.

### pe...@google.com (2015-09-03)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### am...@google.com (2015-09-10)

Merge approved for M45 branch 2454.

### th...@chromium.org (2015-09-10)

Merged to 2454 branch as 496d9484da9332ba7abf7430ff7b474902ad546f, will roll DEPS once for this and https://crbug.com/chromium/522131.

### bu...@chromium.org (2015-09-10)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=78317

------------------------------------------------------------------
r78317 | thestig@google.com | 2015-09-10T19:10:03.921012Z

-----------------------------------------------------------------

### ti...@google.com (2015-10-09)

Congratulations hanno - $1000 for this report.

We'll start payment next week, so you should have the cash ~2 weeks from today,

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-12-05)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/450844?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/414121, crbug.com/chromium/464683, crbug.com/chromium/471797, crbug.com/chromium/497356]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081235)*
