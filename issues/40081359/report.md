# Heap-buffer-overflow in parse_encoding

| Field | Value |
|-------|-------|
| **Issue ID** | [40081359](https://issues.chromium.org/issues/40081359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-02-06 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Linux; Android 4.4.2; SM-T705 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.109 Safari/537.36

Steps to reproduce the problem:
1. $ chrome-asan ch-bofr-parse_encoding.pdf

What is the expected behavior?

What went wrong?
==15256==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x619000403725 at pc 0x7f00acee24d7 bp 0x7fffbdf385f0 sp 0x7fffbdf385e8
READ of size 1 at 0x619000403725 thread T0 (chrome)
    #0 0x7f00acee24d6 in parse_encoding /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/type1/t1load.c:1276
    #1 0x7f00acee0cdc in t1_load_keyword /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/type1/t1load.c:937
    #2 0x7f00acede9fa in parse_dict /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/type1/t1load.c:1983
    #3 0x7f00acedc025 in T1_Open_Face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/type1/t1load.c:2091
    #4 0x7f00aced5b74 in T1_Face_Init /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/type1/t1objs.c:321
    #5 0x7f00ace1d41e in open_face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:1149
    #6 0x7f00ace1c126 in FT_Open_Face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:2076
    #7 0x7f00ace1d036 in FT_New_Memory_Face /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/freetype2/src/src/base/ftobjs.c:1238
    #8 0x7f009ae6e4eb in FT_LoadFont(unsigned char*, int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_font.cpp:170
    #9 0x7f009ae6e2e8 in CFX_Font::LoadEmbedded(unsigned char const*, unsigned int) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_font.cpp:187

Did this work before? N/A 

Chrome version:   Channel: dev
OS Version: 
Flash Version: 

This also happens in pdfium_test. Sorry about the repro size. I usually minimize manually, but only have a tablet with me at the moment.

## Attachments

- [ch-bofr-parse_encoding.pdf](attachments/ch-bofr-parse_encoding.pdf) (application/pdf, 4.6 MB)

## Timeline

### cl...@chromium.org (2015-02-06)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5835111864991744

### cl...@chromium.org (2015-02-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5835111864991744

Uploader: mbarbella@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x619000698125
Crash State:
  parse_encoding
  parse_dict
  T1_Face_Init
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=314095:314100

Minimized Testcase (4677.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ftg9mce7YHEo1tjtqGjmvBcWRDV-TCdG1zv8WTSsb_d5Y-_kHzvkAZqhE8z2Fe_dxhDDidq6EpmrlqXfbCm2rxjrKxgk_HThuArA_7kLsiZ-LWLHGE7MdjyOiLIe_S-wU1uawWtZy0KMG3Cz7cxEpwaTp-5KqshZWjexq5V-jlQl5Ziw



### js...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-10)

might be same as crbug.com/455363

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-21)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-10)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 31 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-27)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 48 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-04-01)

It's a freetype issue. It has been fixed in freetype 2.5.0.1. It's suggested to upgrade freetype to 2.5.0.1 when this issue occurs on Linux.

### ju...@foxitsoftware.com (2015-04-01)

It's suggested to upgrade system freetype on Linux to fix this problem.

### cl...@chromium.org (2015-04-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-04-08)

Nothing to merge here - freetype issue.

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-13)

Severity here should be medium - one byte read, hard to read back.

### ti...@google.com (2015-04-14)

Copngratulations - $500 for this report.

Note from reward panel: 1 byte read and hard to read back. $500 reward mainly for the good quality report and provided repro.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-07-08)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2015-08-07)

ClusterFuzz has detected this issue as fixed in range 341793:342089.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5835111864991744

Uploader: mbarbella@google.com
Job Type: linux_asan_pdfium
Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x619000698125
Crash State:
  parse_encoding
  parse_dict
  T1_Face_Init
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=314095:314100
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=341793:342089

Minimized Testcase (4677.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ftg9mce7YHEo1tjtqGjmvBcWRDV-TCdG1zv8WTSsb_d5Y-_kHzvkAZqhE8z2Fe_dxhDDidq6EpmrlqXfbCm2rxjrKxgk_HThuArA_7kLsiZ-LWLHGE7MdjyOiLIe_S-wU1uawWtZy0KMG3Cz7cxEpwaTp-5KqshZWjexq5V-jlQl5Ziw

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/456206?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081359)*
