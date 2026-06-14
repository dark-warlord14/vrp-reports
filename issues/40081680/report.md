# Stack-buffer-overflow in CFX_WideString::FormatV

| Field | Value |
|-------|-------|
| **Issue ID** | [40081680](https://issues.chromium.org/issues/40081680) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-03-20 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6139696074194944

Fuzzer: Attekett_surku_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x0031c780
Crash State:
  CFX_WideString::FormatV
  CFX_WideString::Format
  util::printf
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=321438:321503

Minimized Testcase (3.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94iodRRfpwpRFrwhEsVpxSu1CvMlYqQZzL5jCF7zMDtlAiOMaffcOnnVkqCjzONIqAQfm0PEw82BdUTUhP7heHnb2yCb8M4gJTsXetdBAlMiVulaVI8ifJQIGbdI2BZ_AWRjYPzFWl9yH3i38ja_c8p5aAGaQ

Filer: inferno

## Timeline

### in...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-21)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-04)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-04-07)

It's pending in https://codereview.chromium.org/1062983002/.

### ju...@foxitsoftware.com (2015-04-09)

Fixed in https://pdfium.googlesource.com/pdfium/+/5a82342845335770f975ef7f9a1b0bca1cf2d971.

### am...@chromium.org (2015-04-09)

Is there a merge required here?

### th...@chromium.org (2015-04-09)

I'll take care of the merge for this at the same time as https://crbug.com/chromium/466790.

### bu...@chromium.org (2015-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/49cac9b06ec43030b706432b5d98fd2e6621d63c

commit 49cac9b06ec43030b706432b5d98fd2e6621d63c
Author: thestig <thestig@chromium.org>
Date: Thu Apr 09 22:20:00 2015

Roll DEPS for PDFium to 1ed2ceb70476b135a3dedbb45549d6b3bc6ecdea

1ed2ceb Fix a global buffer overflow in GCPDF_CIDFont::_CharCodeFromUnicode
cbcc730 Fix reference to timezone variable - removed in VS 2015
45a3d33 Fix IWYU in formfiller/ directory.
d80a434 Use pdfium-specific tree closer for gating landings
5a82342 Fix a stack overflow issue caused by an invalid usage of snprintf
8d42107 FFL_MIN and FFL_MAX are pointless and stupid.
34f5fc0 Fix windows compile class vs. struct confusion in e300c8c32d73
e300c8c Fix IWYU in pdfwindow/ directory.
0415b38 Fix (nearly all) IWYU in fpdfskd/include/javascript/ headers.
a6d4030 fix missing semicolons
f158073 Fix a fatal error due to cloning a global document object
6fcecb5 Fix IWYU in fxcrt headers.

BUG=440500, 454595, 466790, 469244
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1062803008

Cr-Commit-Position: refs/heads/master@{#324522}

[modify] http://crrev.com/49cac9b06ec43030b706432b5d98fd2e6621d63c/DEPS


### in...@chromium.org (2015-04-09)

Please keep bugs in fixed status, merges to be tracked via merge labels.

### cl...@chromium.org (2015-04-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### dx...@google.com (2015-04-13)

[Empty comment from Monorail migration]

### la...@google.com (2015-04-13)

Approved for M43 (branch: 2357)

### bu...@chromium.org (2015-04-13)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=71873

------------------------------------------------------------------
r71873 | thestig@google.com | 2015-04-13T21:29:07.096830Z

-----------------------------------------------------------------

### th...@chromium.org (2015-04-13)

Merged to M43 / rolled DEPS.

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


### ju...@foxitsoftware.com (2015-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M43 label.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-14)

$1000 here ($500 for the report + $500 ClusterFuzz Bonus).

This one will also go through the new payment process.

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### cl...@chromium.org (2015-07-16)

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

This issue was migrated from crbug.com/chromium/469244?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081680)*
