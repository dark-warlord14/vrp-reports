# Heap-buffer-overflow in CPDF_CMap::GetNextChar

| Field | Value |
|-------|-------|
| **Issue ID** | [40081752](https://issues.chromium.org/issues/40081752) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-03-30 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4879892554973184

Fuzzer: Attekett_surku_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x4b724f77
Crash State:
  CPDF_CMap::GetNextChar
  CPDF_CMap::CountChar
  CPDF_TextObject::SetSegments
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=322702:322707

Minimized Testcase (152.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94PCdHTByWY4vcpEIVBRn91Nhuv9eO0xkxbf78NmNj7gEYWTsr4nMl-UNJEePmoipKf4Hj3KZ3lS5_2-u8IZFOXupOm_lIHwQ91fpeNoiu2jCHWd_FKVytlQnQVwdHSErlUcskTdTS_sVFWlgMMcc4PP9yA-XZL6vuEW8dlkLrdW7gHVtQ

Filer: inferno

## Timeline

### in...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-04-07)

It's pending in https://codereview.chromium.org/1067073003/.

### ju...@foxitsoftware.com (2015-04-11)

Fixed in https://pdfium.googlesource.com/pdfium/+/f265ee5a5f0e96d1a91111f4f27eb2f1edd8835a and https://pdfium.googlesource.com/pdfium/+/eeccab8f6a1785d9c94c126524b982c9d4c4b946.

### ju...@foxitsoftware.com (2015-04-11)

Fixed in https://pdfium.googlesource.com/pdfium/+/f265ee5a5f0e96d1a91111f4f27eb2f1edd8835a and https://pdfium.googlesource.com/pdfium/+/eeccab8f6a1785d9c94c126524b982c9d4c4b946.

### am...@chromium.org (2015-04-11)

Is there a merge required here?

### cl...@chromium.org (2015-04-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### dx...@google.com (2015-04-13)

[Empty comment from Monorail migration]

### la...@google.com (2015-04-13)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### dx...@google.com (2015-04-13)

[Empty comment from Monorail migration]

### dx...@chromium.org (2015-04-13)

waiting for a canary.

### bu...@chromium.org (2015-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8c0df8c5f8cd199a5fe3e3b4bf0ddd60b7ad1eb5

commit 8c0df8c5f8cd199a5fe3e3b4bf0ddd60b7ad1eb5
Author: thestig <thestig@chromium.org>
Date: Tue Apr 14 00:09:36 2015

Roll DEPS for PDFium to eddab4425614e49146f904f00da4a664ba4b581b

eddab44 Fix a heap overflow in CJBig2_Context::parseSymbolDict
eeccab8 Fix compiling warnings on Windows
f265ee5 Fix a heap buffer overflow issue in CPDF_CMap::GetNextChar
9c7b094 Fix the noisiest variable shadowing warnings in pdfium.
d794018 Better fix for snprintf non-termination on windows.
1569728 Fix a stack overflow in CPDF_Parser::LoadCrossRefV5
e45a2e4 Don't call FPDF_InitLibrary() in individual unit_tests.
ea18d0b Update DEPS to pull V8 from the new repository.
70476c2 Include windows.h instead of the MFC header afxres.h
308e05e Consider platform-specific expected .png files.

BUG=440500, 469244, 471651, 473400, 476107
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1088713002

Cr-Commit-Position: refs/heads/master@{#324955}

[modify] http://crrev.com/8c0df8c5f8cd199a5fe3e3b4bf0ddd60b7ad1eb5/DEPS


### la...@google.com (2015-04-27)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-05-11)

Not sure who did the PDFium merge here, but we haven't rolled DEPS on the 2357 branch to pick this up yet.

### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=73326

------------------------------------------------------------------
r73326 | thestig@google.com | 2015-05-11T21:12:16.916094Z

-----------------------------------------------------------------

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M43 label.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-16)

Thanks CF - you're the best.

### ti...@google.com (2015-06-14)

We decided to pay $500 here (which was $0 for the bug and $500 for the CF bonus). Noting that this was a case where we believed that the bug didn't meet the threshold for reward but was very close. 

Note to future people looking at this bug: This was an edge case and not to be used as a precedent for future $0 reports running on ClusterFuzz. Normally, the ClusterFuzz bonus only applies to bugs that get a cash reward and a $0 reward would not be applicable for the CF bonus.

We'll also take this one through the new payment system.

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### cl...@chromium.org (2015-07-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/471651?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/465753]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081752)*
