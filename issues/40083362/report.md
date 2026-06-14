# Heap-use-after-free in content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportWriteC

| Field | Value |
|-------|-------|
| **Issue ID** | [40083362](https://issues.chromium.org/issues/40083362) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | cm...@chromium.org |
| **Created** | 2015-12-10 |
| **Bounty** | $5,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6608324696473600

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x05981d80
Crash State:
  content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportWriteC
  base::internal::Invoker<base::IndexSequence<0,1,2>,base::internal::BindState<bas
  base::debug::TaskAnnotator::RunTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=363351:363859

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94jDXELDguAKC8yinS1v-_vOiAEpI1bXAZKww9XEyG_v4gmlc1CePFDXaImhguz0O6wovrP1EpN8_8NioVtgFDYNyhN5Q1q6_lQGH9LNzWkgxqceF9LRBGhfbJKuNhpGt8wUyZUvdgKR_XVNv7CRpjtwKKVWg


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Attachments

- [asan_trace.txt](attachments/asan_trace.txt) (text/plain, 11.9 KB)

## Timeline

### in...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-10)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-12-10)

cmumford@, can you take this?

Looks like ChainedBlobWriterImpl holds the backing store in a raw pointer, and the blob writer posted task isn't aware that the backing store has been is destructed.

Might be as simple as a weakptr, but I haven't looked closely yet.

### cm...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### cm...@chromium.org (2015-12-10)

Looks like this is a nonoccurrence of https://crbug.com/chromium/472614. Am investigating possibility of using a weakptr as suggested by jsbell.

### bu...@chromium.org (2015-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/32d3e6f802f40471496f08ea818515074970f4de

commit 32d3e6f802f40471496f08ea818515074970f4de
Author: cmumford <cmumford@chromium.org>
Date: Sat Dec 12 02:14:52 2015

Fixed use-after-free bug in ChainedBlobWriterImpl.

This bug originally reported in https://crbug.com/chromium/472614. The problem was that if
Abort() was called, but there was no pending callbacks then no state
would be changed, and if ReportWriteCompletion() was called later then
it could in turn call WriteNextFile resulting in the use of a dangling
pointer to a deleted IndexedDBBackingStore.

This change reverts the original fix (#326597), and just sets the aborted_
flag to prevent this bug.

BUG=568433

Review URL: https://codereview.chromium.org/1516123003

Cr-Commit-Position: refs/heads/master@{#364868}

[modify] http://crrev.com/32d3e6f802f40471496f08ea818515074970f4de/content/browser/indexed_db/indexed_db_backing_store.cc


### cl...@chromium.org (2015-12-12)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6608324696473600

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x05981d80
Crash State:
  content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportWriteC
  base::internal::Invoker<base::IndexSequence<0,1,2>,base::internal::BindState<bas
  base::debug::TaskAnnotator::RunTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=363351:363859

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94jDXELDguAKC8yinS1v-_vOiAEpI1bXAZKww9XEyG_v4gmlc1CePFDXaImhguz0O6wovrP1EpN8_8NioVtgFDYNyhN5Q1q6_lQGH9LNzWkgxqceF9LRBGhfbJKuNhpGt8wUyZUvdgKR_XVNv7CRpjtwKKVWg


Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### th...@gmail.com (2015-12-12)

I can repro this on stable (47.0.2526.80) which makes sense considering #7.

### cm...@chromium.org (2015-12-14)

Fix is in 49.0.2590.0

### js...@chromium.org (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-14)

Congrats your change is auto-approved for M48 (branch: 2564)

### cl...@chromium.org (2015-12-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-01-04)

cmumford@, could you please merge the change to M48 branch 2564. Thank you.

### bu...@chromium.org (2016-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c3ead76a07f6a61bbe4d85baa8741143fb833361

commit c3ead76a07f6a61bbe4d85baa8741143fb833361
Author: Chris Mumford <cmumford@chromium.org>
Date: Tue Jan 05 00:51:17 2016

Fixed use-after-free bug in ChainedBlobWriterImpl.

This bug originally reported in https://crbug.com/chromium/472614. The problem was that if
Abort() was called, but there was no pending callbacks then no state
would be changed, and if ReportWriteCompletion() was called later then
it could in turn call WriteNextFile resulting in the use of a dangling
pointer to a deleted IndexedDBBackingStore.

This change reverts the original fix (#326597), and just sets the aborted_
flag to prevent this bug.

BUG=568433

Review URL: https://codereview.chromium.org/1516123003

Cr-Commit-Position: refs/heads/master@{#364868}
(cherry picked from commit 32d3e6f802f40471496f08ea818515074970f4de)

Review URL: https://codereview.chromium.org/1558063002 .

Cr-Commit-Position: refs/branch-heads/2564@{#464}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/c3ead76a07f6a61bbe4d85baa8741143fb833361/content/browser/indexed_db/indexed_db_backing_store.cc


### bu...@chromium.org (2016-01-05)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/c3ead76a07f6a61bbe4d85baa8741143fb833361

commit c3ead76a07f6a61bbe4d85baa8741143fb833361
Author: Chris Mumford <cmumford@chromium.org>
Date: Tue Jan 05 00:51:17 2016


### mb...@chromium.org (2016-01-25)

Fixing severity.

### sh...@chromium.org (2016-03-22)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

(part of non-stable reward backlog round)

$5,000 for this report, + $500 for the fuzzer. Congrats!

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/568433?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083362)*
