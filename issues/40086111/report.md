# Heap-use-after-free in printing::PrintWebViewHelper::OnMessageReceived

| Field | Value |
|-------|-------|
| **Issue ID** | [40086111](https://issues.chromium.org/issues/40086111) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Printing |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-11-29 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5754609055563776

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61100001b7dc
Crash State:
  printing::PrintWebViewHelper::OnMessageReceived
  content::RenderFrameImpl::OnMessageReceived
  content::ChildThreadImpl::OnMessageReceived
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=434678:434769

Minimized Testcase (953.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94F1azWt_SdrRZJ4bx0hPi8cmk-13Gl4MWJltieZ7oVD7lci13RzJJ8rMGLadq4yxRUvXpSfJ0l2HRRjAg6y779Mc63DoRk-yE7A7bM-4GphogTaJOYGnigvzajuOsoDrX48HT88d6SXugqp_dPYlHQMO5V89mztxrrza9mSem8JkO-D7Y?testcase_id=5754609055563776

Additional requirements: Requires Gestures

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### oc...@chromium.org (2016-11-29)

thestig, are you the right owner for this? thanks.

### oc...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>Printing]

### th...@chromium.org (2016-11-30)

Looks like we need to do another follow up after fixing https://crbug.com/chromium/666616 in r434734.

### th...@chromium.org (2016-11-30)

https://codereview.chromium.org/2537973003

### sh...@chromium.org (2016-11-30)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/149f2a418b32edc71ce700e75084fccf2ce6eb2a

commit 149f2a418b32edc71ce700e75084fccf2ce6eb2a
Author: thestig <thestig@chromium.org>
Date: Wed Nov 30 17:52:57 2016

One more check for PrintWebViewHelper validity.

This check should have been in r434734.

BUG=669534

Review-Url: https://codereview.chromium.org/2537973003
Cr-Commit-Position: refs/heads/master@{#435323}

[modify] https://crrev.com/149f2a418b32edc71ce700e75084fccf2ce6eb2a/components/printing/renderer/print_web_view_helper.cc


### cl...@chromium.org (2016-12-01)

ClusterFuzz has detected this issue as fixed in range 435314:435416.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5754609055563776

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61100001b7dc
Crash State:
  printing::PrintWebViewHelper::OnMessageReceived
  content::RenderFrameImpl::OnMessageReceived
  content::ChildThreadImpl::OnMessageReceived
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=434678:434769
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=435314:435416

Minimized Testcase (953.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94F1azWt_SdrRZJ4bx0hPi8cmk-13Gl4MWJltieZ7oVD7lci13RzJJ8rMGLadq4yxRUvXpSfJ0l2HRRjAg6y779Mc63DoRk-yE7A7bM-4GphogTaJOYGnigvzajuOsoDrX48HT88d6SXugqp_dPYlHQMO5V89mztxrrza9mSem8JkO-D7Y?testcase_id=5754609055563776

Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-12-01)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-12-01)

[Empty comment from Monorail migration]

### na...@chromium.org (2016-12-01)

Now that ClusterFuzz has verified the fix, requesting merge into M56.

### di...@chromium.org (2016-12-01)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### na...@chromium.org (2016-12-01)

I'll take care of the merge.

### bu...@chromium.org (2016-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6e404a5004dc4ac3c9860371f824ba13bcaf5f7

commit a6e404a5004dc4ac3c9860371f824ba13bcaf5f7
Author: Nasko Oskov <nasko@chromium.org>
Date: Thu Dec 01 18:07:52 2016

One more check for PrintWebViewHelper validity.

This check should have been in r434734.

BUG=669534

Review-Url: https://codereview.chromium.org/2537973003
Cr-Commit-Position: refs/heads/master@{#435323}
(cherry picked from commit 149f2a418b32edc71ce700e75084fccf2ce6eb2a)

Review URL: https://codereview.chromium.org/2545853002 .

Cr-Commit-Position: refs/branch-heads/2924@{#251}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/a6e404a5004dc4ac3c9860371f824ba13bcaf5f7/components/printing/renderer/print_web_view_helper.cc


### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-12)

Congratulations!  The panel has awarded $1,500 for this bug.

### lf...@chromium.org (2016-12-12)

Re #15: This was found by clusterfuzz. Wrong bug?

### [Deleted User] (2016-12-12)

This was found by Peach. Looks legit to me. ;-)

### lf...@chromium.org (2016-12-12)

Re #17: Ah, fair enough, didn't see that :)

### aw...@google.com (2016-12-12)

Yep - this is running under the Chrome Fuzzer Program (g.co/ChromeBugRewards)

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-09)

This issue was migrated from crbug.com/chromium/669534?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086111)*
