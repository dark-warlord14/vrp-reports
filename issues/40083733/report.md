# Heap-use-after-free in blink::CanvasAsyncBlobCreator::createBlobAndCall

| Field | Value |
|-------|-------|
| **Issue ID** | [40083733](https://issues.chromium.org/issues/40083733) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | xl...@chromium.org |
| **Created** | 2016-02-22 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4903892581613568

Fuzzer: cdiehl_dharma
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b00001cfc8
Crash State:
  blink::CanvasAsyncBlobCreator::createBlobAndCall
  base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base
  base::debug::TaskAnnotator::RunTask
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=375259:376263

Minimized Testcase (1.19 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95SqyLZZ4a3h6CgHD4bkgfmF1KqsVnlXRU89RgBpfiL5iz9-A2hhTmaXUrsDg5wunQJ7Cv60xlkqwVUkPLL_OImE922fSDXlwNHafkSDg7P_K2xwjcUN_gx__Nac5IXj7S5cL3cszPYpOGvLasCuNkjLxUhyw

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2016-02-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas]

### ju...@chromium.org (2016-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9ab084e093bcee42c0423d4d845142fd7cc13e5b

commit 9ab084e093bcee42c0423d4d845142fd7cc13e5b
Author: xlai <xlai@chromium.org>
Date: Fri Feb 26 17:20:32 2016

Fix heap-use-after-free bug in CanvasAsyncBlobCreator::createBlobAndCall

BUG=588550

Review URL: https://codereview.chromium.org/1742603002

Cr-Commit-Position: refs/heads/master@{#377910}

[modify] https://crrev.com/9ab084e093bcee42c0423d4d845142fd7cc13e5b/third_party/WebKit/Source/core/html/canvas/CanvasAsyncBlobCreator.cpp


### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-02)

ClusterFuzz has detected this issue as fixed in range 377898:378030.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4903892581613568

Fuzzer: cdiehl_dharma
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b00001cfc8
Crash State:
  blink::CanvasAsyncBlobCreator::createBlobAndCall
  base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base
  base::debug::TaskAnnotator::RunTask
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=375259:376263
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_chromeos&range=377898:378030

Minimized Testcase (1.19 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95SqyLZZ4a3h6CgHD4bkgfmF1KqsVnlXRU89RgBpfiL5iz9-A2hhTmaXUrsDg5wunQJ7Cv60xlkqwVUkPLL_OImE922fSDXlwNHafkSDg7P_K2xwjcUN_gx__Nac5IXj7S5cL3cszPYpOGvLasCuNkjLxUhyw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### xl...@chromium.org (2016-03-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-21)

As discussed via email, $3,500 for this report: ($3,000 for the report + $500 for the fuzzer).

### ti...@google.com (2016-06-21)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/588550?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083733)*
