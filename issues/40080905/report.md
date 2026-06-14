# Heap-buffer-overflow in std::less<std::string>::operator

| Field | Value |
|-------|-------|
| **Issue ID** | [40080905](https://issues.chromium.org/issues/40080905) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | cl...@chromium.org |
| **Assignee** | cm...@chromium.org |
| **Created** | 2014-11-23 |
| **Bounty** | $4,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6596866958426112

Fuzzer: Therealholden_worker
Job Type: Android_asan_chrome

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x42f4ad74
Crash State:
  std::less<std::string>::operator
  std::priv::_Rb_tree<std::string, std::less<std::string>, std::pair<std::str
  storage::BlobDataHandle*& std::map<std::string, storage::BlobDataHandle*, s
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94hYiJHN2xCqPqZ4pDTyghyqp4zTJZ_mcFd1Dr96jN8EbEP_wvfFm0zZZpM-BuXw_HBYp1dLS4nFfWNNwo954z0sVbgv0pl-YwP9ZYM4ByWZybR6YDKvSxftvbot0xEfX3YCeJUnVOgXCdxamQXLe8_mBGC_g


Additional requirements: Requires HTTP

Filer: inferno

## Timeline

### in...@chromium.org (2014-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-02)

cmumford@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cm...@chromium.org (2014-12-03)

I believe this is actually a heap-use-after-free - at least the ASAN Linux build reports an error when running this test - on the same file/line: content/browser/indexed_db/indexed_db_dispatcher_host.cc:216. I'm not sure if the Android ASAN is less mature than the Linux version.

This same test also is reproducible on a debug build (yeah! :-). A DCHECK fails at content/browser/indexed_db/indexed_db_dispatcher_host.cc:215 which is asserting that the blob's UUID isn't already in IndexedDBDispatcherHost's blob_data_handle_map_ - which it is.

It looks like the cause is the fact that the test creates two cursors to iterate over the BLOB, and the second cursor tries to create and register a second BLOB, but it's UUID conflicts with the first. Still thinking about what the correct solution is.

### pa...@google.com (2014-12-03)

I'm just going to guess, based on the age of the DCHECK in git blame, that this affects stable. You have permission to personally laugh at me if I am wrong. And to change the label. :)

### js...@chromium.org (2014-12-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c

commit 2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c
Author: cmumford <cmumford@chromium.org>
Date: Fri Dec 05 20:01:05 2014

IndexedDB: Fixed cursor/blob use-after-free bug

The IndexedDBDispatcherHost maintains a map of BLOB UUID's to BLOBs, but if two
(or more) cursors are both active and referencing the same BLOB then two (or
more) BLOBs would exist with the same UUID, and their keys would collide in this
map. This change reference counts these BLOBs to avoid duplication.

Also, access to the existing map was not synchronized and was accessed on two
different threads.

BUG=435880,436137

Review URL: https://codereview.chromium.org/774593004

Cr-Commit-Position: refs/heads/master@{#307063}

[modify] http://crrev.com/2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c/content/browser/indexed_db/indexed_db_callbacks.cc
[modify] http://crrev.com/2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c/content/browser/indexed_db/indexed_db_dispatcher_host.cc
[modify] http://crrev.com/2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c/content/browser/indexed_db/indexed_db_dispatcher_host.h


### cm...@chromium.org (2014-12-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-15)

Approved for M40 (branch: 2214)

### bu...@chromium.org (2014-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5ef0af0662dc1b5ed46f62c4c52b08bdf1e29b6a

commit 5ef0af0662dc1b5ed46f62c4c52b08bdf1e29b6a
Author: Chris Mumford <cmumford@chromium.org>
Date: Wed Dec 17 22:59:07 2014

IndexedDB: Fixed cursor/blob use-after-free bug

The IndexedDBDispatcherHost maintains a map of BLOB UUID's to BLOBs, but if two
(or more) cursors are both active and referencing the same BLOB then two (or
more) BLOBs would exist with the same UUID, and their keys would collide in this
map. This change reference counts these BLOBs to avoid duplication.

Also, access to the existing map was not synchronized and was accessed on two
different threads.

BUG=435880,436137

Review URL: https://codereview.chromium.org/774593004

Cr-Commit-Position: refs/heads/master@{#307063}
(cherry picked from commit 2d74497dfa5e6fd6ddddc93248c322a57dd8dd2c)

R=jsbell@chromium.org

Review URL: https://codereview.chromium.org/816533003

Cr-Commit-Position: refs/branch-heads/2214@{#321}
Cr-Branched-From: 03655fd3f6d72165dc3c9bd2c89807305316fe6c-refs/heads/master@{#303346}

[modify] http://crrev.com/5ef0af0662dc1b5ed46f62c4c52b08bdf1e29b6a/content/browser/indexed_db/indexed_db_callbacks.cc
[modify] http://crrev.com/5ef0af0662dc1b5ed46f62c4c52b08bdf1e29b6a/content/browser/indexed_db/indexed_db_dispatcher_host.cc
[modify] http://crrev.com/5ef0af0662dc1b5ed46f62c4c52b08bdf1e29b6a/content/browser/indexed_db/indexed_db_dispatcher_host.h


### in...@chromium.org (2014-12-17)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-19)

Updating severity

### ti...@google.com (2015-01-22)

Congrats - $4500 for this report. Notes from panel: "$4000 for OOB read, +$500 ClusterFuzz bonus".

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/435880?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080905)*
