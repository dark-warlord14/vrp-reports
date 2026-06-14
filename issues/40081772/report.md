# Heap-use-after-free in content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportW

| Field | Value |
|-------|-------|
| **Issue ID** | [40081772](https://issues.chromium.org/issues/40081772) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | cl...@chromium.org |
| **Assignee** | cm...@chromium.org |
| **Created** | 2015-04-01 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6059461953716224

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x03f7de80
Crash State:
  content::IndexedDBBackingStore::Transaction::ChainedBlobWriterImpl::ReportW
  base::internal::Invoker<IndexSequence<0,1,2>,base::internal::BindState<base
  base::debug::TaskAnnotator::RunTask
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv950dm51HDGN9rk1q16pVsOX65HnOzg88PbLQ1f7My6_ZIKA0279WhRNpxUMD8W770wbDbp2aG4H040jo9VV5h8ArJSRfF8NbXGSM-Jhg1Dr__sA_956vdEsyyR5wxSu-3sVWQJxg8kTL3XKfMqcNVy2ZlGPfA


Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2015-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-04-01)

Given the age of the code in question I'm going to assume it impacts stable. Please change if determined otherwise.

### js...@chromium.org (2015-04-01)

Passing it off to cmumford, but I'll take a quick look.

### js...@chromium.org (2015-04-01)

From a first glance, looks like the ChainedBlobWriterImpl's Abort() should be checking aborted_ - it looks plausible that during backing store close the transaction would be aborted and call Abort() on the writer. Later, the posted task still runs, and the writer's raw pointer to the backing store is derefed -> boom.

### cl...@chromium.org (2015-04-01)

[Empty comment from Monorail migration]

### cm...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### cm...@chromium.org (2015-04-03)

jsbell: I don't see how checking aborted_ (and doing an early return?) would fix this. Do you think it's possible for WriteBlobFile to result in Abort being called before it can set waiting_for_callback_ to true?

### js...@chromium.org (2015-04-03)

The "free" stack shows that the backing store has been closed. That would cause the transactions to all be aborted, which would Abort() their blob writers. I confess I didn't dig through the entire state machine of the writer to see what would happen next; I was guessing that if they had outstanding tasks (i.e. from the constructor?) it would fall into the bad path.


### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-18)

cmumford@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cm...@chromium.org (2015-04-21)

Not able to reproduce, but I did put up a change (crrev.com/1060613002) which is a (very) speculative fix for this.

### bu...@chromium.org (2015-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29777a8ee0f45b8160ec004e74013d5b62b6828a

commit 29777a8ee0f45b8160ec004e74013d5b62b6828a
Author: cmumford <cmumford@chromium.org>
Date: Thu Apr 23 18:56:12 2015

IndexedDB: Protect against use-after-free in ChainedBlobWriter.

This is a speculative fix for a heap user-after-free bug. Was unable
to verify using a Windows SyzyASan build. The theory is that if Abort()
was called before ChainedBlobWriterImpl::WriteNextFile() could set
waiting_for_callback_ then the ReportWriteCompletion() would never know
that it was aborted and attempt to use it's dangling raw pointer to a
deleted IndexedDBBackingStore instance.

Also in this change is the elimination of the redundant aborted_
member variable.

BUG=472614

Review URL: https://codereview.chromium.org/1060613002

Cr-Commit-Position: refs/heads/master@{#326597}

[modify] http://crrev.com/29777a8ee0f45b8160ec004e74013d5b62b6828a/content/browser/indexed_db/indexed_db_backing_store.cc


### cm...@chromium.org (2015-04-24)

The speculative fix in #13 _might_ fix this, and if not will hopefully shed more light on the cause. Being as I cannot reproduce this I am marking as Fixed and will revisit this issue if reopened.

### cl...@chromium.org (2015-04-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-11)

We can let this roll in with M44 or reopen if the issue isn't fixed. 

(Note: If reopening, please remove the "Release-0-M44" and "Merge-NA" labels.

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-31)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-09)

Congrats - $3500 for this report ($3000 for the bug + $500 ClusterFuzz bonus).

I'll start payment next week, so you should have the reward ~2 weeks from today.

Thanks again!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

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

This issue was migrated from crbug.com/chromium/472614?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081772)*
