# UNKNOWN in TcmapEncodingTable::GetSubtableAtIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40080513](https://issues.chromium.org/issues/40080513) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | rs...@chromium.org |
| **Created** | 2014-09-22 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5029534366695424

Fuzzer: Attekett_surku_fuzzer
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0x24538dc1
Crash State:
  TcmapEncodingTable::GetSubtableAtIndex
  TcmapEncodingTable::FindPreferredMacCmap
  TcmapEncodingTable::TcmapEncodingTable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=273280:273333

Minimized Testcase (153.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv941I92M0dEqZ7KReaM79jmGK5g6_c2Qe5a6Y0we8QLwhVt-sPZuxoqkpDG-_jVV8C2RI2IYyqQDbzitEK4hnmmZHMgQWD015KroLOyreqbCUA6fqZK2B5VnAAiaT8ty7maQEoZ-fiGen2W29y2KH6CZA8bLf8Ec9ZO7-YjPHh19HFhQwmo

Filer: inferno

## Timeline

### in...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-07)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-10-07)

Bumping to M39

### cl...@chromium.org (2014-10-14)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-22)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6083843508404224

Fuzzer: Ifratric_pdf_generic
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0x2422737b
Crash State:
  TcmapEncodingTable::GetSubtableAtIndex
  TcmapEncodingTable::FindPreferredMacCmap
  TcmapEncodingTable::TcmapEncodingTable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=271393:271739

Minimized Testcase (1597.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv961OLjLo_gPnHgokafvFjR25AYqJpc5HLyx2sWE-IwR5S_XtUUXJlKi06weuAc4CJqxEbMiQGs2L4lw-pDU3686P4sQDSca3h7hOlXrO5uerFM_kLwch3uiwTQQ-fmkMcAttnKx5B8LHpJ3a6YqUyNovgSKsRsSDzQz8xN6E0WxxItp7i0

Filer: inferno

### cl...@chromium.org (2014-10-29)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-05)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-13)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-20)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-22)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-16)

ClusterFuzz has detected this issue as fixed in range 305030:305059.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5029534366695424

Fuzzer: Attekett_surku_fuzzer
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0x24538dc1
Crash State:
  TcmapEncodingTable::GetSubtableAtIndex
  TcmapEncodingTable::FindPreferredMacCmap
  TcmapEncodingTable::TcmapEncodingTable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=273998:274265
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=305030:305059

Minimized Testcase (153.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94hQMJJDCOciQMvb3QoIkI4SIxiTSR-i67nGHQnvYv-_m_ch9nGTYusPBIsm08oFJIxQQDcLBIBi7rEoEsbucAThWpPuIe6T0sit0NShfTwL7GUs-9D-JYGm6cH8Pulv-6tZxuIWSDzk8m4emDspZbVy26ljwlBcq23Rhti_3OXWqLSK0o

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bo...@foxitsoftware.com (2014-12-16)

@thestig, is there a fast way(Google internal tool) to bisect the PDFium/Chromium revision that fixes this issue?

### th...@chromium.org (2014-12-16)

Probably do a manual bisect if needed. The changelog for the "fixed" range is https://chromium.googlesource.com/chromium/src/+log/56c60209b09297951f2321d5b5818e1a97dca465..512e25f331e03b33c60d9e9ec6fcb9f42761985e?pretty=fuller and I don't see what would have fixed this.

### cl...@chromium.org (2014-12-16)

ClusterFuzz has detected this issue as fixed in range 305030:305059.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6083843508404224

Fuzzer: Ifratric_pdf_generic
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0x2422737b
Crash State:
  TcmapEncodingTable::GetSubtableAtIndex
  TcmapEncodingTable::FindPreferredMacCmap
  TcmapEncodingTable::TcmapEncodingTable
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=281494:281514
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=305030:305059

Minimized Testcase (1597.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv961OLjLo_gPnHgokafvFjR25AYqJpc5HLyx2sWE-IwR5S_XtUUXJlKi06weuAc4CJqxEbMiQGs2L4lw-pDU3686P4sQDSca3h7hOlXrO5uerFM_kLwch3uiwTQQ-fmkMcAttnKx5B8LHpJ3a6YqUyNovgSKsRsSDzQz8xN6E0WxxItp7i0

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bo...@foxitsoftware.com (2014-12-17)

The fix is https://chromium.googlesource.com/chromium/src/+/602b4bf2748b43b9cb697b039a35131b9e0c913c

So it looks like the bug is due to the mac 32 bit build.

### th...@chromium.org (2014-12-17)

+rsesek to help take a look. This is crashing in OS X code, right?

### bo...@foxitsoftware.com (2014-12-17)

Yep, OS X crash

### bo...@foxitsoftware.com (2014-12-20)

@rsesek, any thought on this? Shall we close the issue?

### cl...@chromium.org (2014-12-20)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6321027008167936

### in...@chromium.org (2014-12-21)

rsesek@ - is 64-bit mac stable enough to enable on M40 ?

### cl...@chromium.org (2014-12-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### rs...@chromium.org (2014-12-22)

Mac is now 64-bit only, so yes.

This crash looks like it's inside Apple's typesetting engine.

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 for this report. Notes from reward panel: "Doesn't affect Mac 64-bit though $500 reward as report received before Mac 64-bit went to stable channel. +$500 ClusterFuzz bonus".

### ea...@chromium.org (2015-01-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-28)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### la...@google.com (2015-06-13)

[Empty comment from Monorail migration]

### la...@google.com (2015-06-13)

Attempting to remove dominik.rottsches@intel.com from cc.

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

This issue was migrated from crbug.com/chromium/416323?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080513)*
