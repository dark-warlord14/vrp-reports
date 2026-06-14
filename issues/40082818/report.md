# Heap-use-after-free in content::EmbeddedWorkerInstance::ReleaseProcess

| Field | Value |
|-------|-------|
| **Issue ID** | [40082818](https://issues.chromium.org/issues/40082818) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fa...@chromium.org |
| **Created** | 2015-09-09 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5681139094650880

Fuzzer: therealholden_worker
Job Type: windows_asan_content_shell
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x17718fe8
Crash State:
  content::EmbeddedWorkerInstance::ReleaseProcess
  content::EmbeddedWorkerInstance::SendStartWorker
  base::internal::RunnableAdapter<void
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97n9jkGhG72F8qiYEJKHNEJX-BOoiGttMSTlUPQjDRl0GSCiGn-NX2MhULMRQiqc3ek7VLnyskrmzOWWqUJoQVPLkzYdkt5QX_fI1bl5PcRqNptHiMCwBxucJKbMkY0hJJgyZW6A6s4TqZLanvvnEt0O88Ugg


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-09)

[Empty comment from Monorail migration]

### fa...@chromium.org (2015-09-09)

After callback.Run(), |this| may be destroyed, since SWVersion's refcount may die causing EWInstance to die.

### ri...@chromium.org (2015-09-15)

What confuses me about this is that the callback in question takes a weak pointer, which I thought was supposed to guard against this:

https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/service_worker/embedded_worker_instance.cc&l=306

The callback seems to run on the same thread that should have invalidated the weak pointer, so I don't see what went wrong - just for my curiosity, do you have a better understanding of what's going on here, falken@?

### ri...@chromium.org (2015-09-15)

Never mind, I didn't realize that the free was happening from inside the callback :-)

### ri...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37b83877e63f62f8aebb337494f1116539182bdf

commit 37b83877e63f62f8aebb337494f1116539182bdf
Author: falken <falken@chromium.org>
Date: Thu Sep 17 07:14:03 2015

Fix crash during EmbeddedWorkerInstance startup sequence failures

Once EWInstance startup calls the callback, it's possible that the
underlying ServiceWorkerVersion is destroyed, hence destroying
|this|. We must guard against that.

Also some failure points in the startup sequence weren't calling
OnStopped() as expected.

BUG=529520, 531345

Review URL: https://codereview.chromium.org/1327723005

Cr-Commit-Position: refs/heads/master@{#349368}

[modify] http://crrev.com/37b83877e63f62f8aebb337494f1116539182bdf/content/browser/service_worker/embedded_worker_instance.cc
[modify] http://crrev.com/37b83877e63f62f8aebb337494f1116539182bdf/content/browser/service_worker/embedded_worker_instance.h
[modify] http://crrev.com/37b83877e63f62f8aebb337494f1116539182bdf/content/browser/service_worker/embedded_worker_instance_unittest.cc


### aa...@google.com (2015-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### fa...@chromium.org (2015-09-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-28)

[Automated comment] Request affecting a post-stable build (M45), manual review required.

### ti...@google.com (2015-09-28)

Approved for M46 (branch: 2490)

### am...@google.com (2015-09-29)

I don't plan to push any more M45 releases, so rejecting this.

### ti...@chromium.org (2015-10-02)

We're quickly approaching M46 final build cut, pls make sure to merge your change into M46 by Oct-6 (PT), to catch up with it! 
The sooner the better so that it gets more bake time.
(If your change misses the Oct-6 final cut, it misses M46 but can catch up with next launch M47)

### bu...@chromium.org (2015-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a5f0eacc3ee761addef759ceb50b421a0f806627

commit a5f0eacc3ee761addef759ceb50b421a0f806627
Author: Matt Falkenhagen <falken@chromium.org>
Date: Sat Oct 03 01:23:38 2015

(M46) Fix crash during EmbeddedWorkerInstance startup sequence failures

Once EWInstance startup calls the callback, it's possible that the
underlying ServiceWorkerVersion is destroyed, hence destroying
|this|. We must guard against that.

Also some failure points in the startup sequence weren't calling
OnStopped() as expected.

BUG=529520, 531345

Review URL: https://codereview.chromium.org/1327723005

Cr-Commit-Position: refs/heads/master@{#349368}
(cherry picked from commit 37b83877e63f62f8aebb337494f1116539182bdf)

TBR=nhiroki

Review URL: https://codereview.chromium.org/1388483003 .

Cr-Commit-Position: refs/branch-heads/2490@{#482}
Cr-Branched-From: 7790a3535f2a81a03685eca31a32cf69ae0c114f-refs/heads/master@{#344925}

[modify] http://crrev.com/a5f0eacc3ee761addef759ceb50b421a0f806627/content/browser/service_worker/embedded_worker_instance.cc
[modify] http://crrev.com/a5f0eacc3ee761addef759ceb50b421a0f806627/content/browser/service_worker/embedded_worker_instance.h
[modify] http://crrev.com/a5f0eacc3ee761addef759ceb50b421a0f806627/content/browser/service_worker/embedded_worker_instance_unittest.cc


### bu...@chromium.org (2015-10-03)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/a5f0eacc3ee761addef759ceb50b421a0f806627

commit a5f0eacc3ee761addef759ceb50b421a0f806627
Author: Matt Falkenhagen <falken@chromium.org>
Date: Sat Oct 03 01:23:38 2015


### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

Congratulations - $3500 for this report ($3000 for the bug report + $500 Clusterfuzz bonus).

Panel notes: Nice bug. If this were a more reliable crash, the reward amount would have been higher.

We'll start payment later this week so you should have the funds ~2 weeks from today. I'll update this issue with a CVE shortly.

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-12-24)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/529520?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082818)*
