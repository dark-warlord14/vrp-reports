# Bad-cast to SessionService from invalid vptr;bind_internal.h:248:12

| Field | Value |
|-------|-------|
| **Issue ID** | [40080144](https://issues.chromium.org/issues/40080144) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sk...@chromium.org |
| **Created** | 2014-08-01 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6460471810981888

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_ubsan_vptr_chrome

Crash Type: Bad-cast
Crash Address: 0x0a711bb06700
Crash State:
  - crash stack -
  Bad-cast to SessionService from invalid vptr
  bind_internal.h:248:12
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95dDmy4kxdWhKNWKF6lA0FkgXWJPAJOWc9-ZB6lulmLsncv8Kr-MTLWZ0vjNxME8RuvaFB9QnD6lLLs-8YBQal8yKdkOtUF5BSWwJp6vX4mV_Ni3CZmn1JCiGr9K4EsMjyYx60Hi9l8l8RZ_oXj1mw8cKM-_lQb1y04il6v2WvJ0qSA1VI


Additional requirements: Requires Gestures

Filer: inferno

## Timeline

### in...@chromium.org (2014-08-01)

Looks like a use-after-free hitting in ubsan. Sorry testcase is just a one-time-crasher, can you check if you can work out the problem from the stacktrace.

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

kaiwang@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-08-12)

sky@: This looks like a significant security bug with a bad pointer to a SessionService object, but unfortunately we don't have a consistently reproducing test case. Are you able to have a look at the test case, or pass it on to somebody who could?

### cl...@chromium.org (2014-08-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-20)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-08-20)

has been hitting for a while, assuming stable.

### cl...@chromium.org (2014-08-20)

[Empty comment from Monorail migration]

### sk...@chromium.org (2014-08-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae

commit 1a14f497bd17d41d0e0ffceb1fb23dea507b8eae
Author: sky <sky@chromium.org>
Date: Tue Aug 26 21:44:26 2014

Fixes possible use after free in SessionService

SessionService::GetLastSession used a base::Unretained but there was
no guarantee that the SessionService would be valid by the time the
callback was processed.

BUG=399655
TEST=covered by test now
R=marja@chromium.org

Review URL: https://codereview.chromium.org/500143002

Cr-Commit-Position: refs/heads/master@{#291985}

[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/base_session_service.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/base_session_service.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/session_service.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/session_service.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/session_service_test_helper.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/session_service_test_helper.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/1a14f497bd17d41d0e0ffceb1fb23dea507b8eae/chrome/browser/sessions/session_service_unittest.cc


### in...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sk...@chromium.org (2014-09-04)

I haven't seen any regressions on trunk, so requesting merge.

### [Deleted User] (2014-09-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-23)

sky@ - can you please merge your change to branch 2125?

### sk...@chromium.org (2014-09-24)

Ya, sorry, I got frustrated and gave up when I saw drover no longer worked. *SIGH* I just merged it over.

### bu...@chromium.org (2014-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d

commit aefd3b8ad196b8316638f36481efed6162255d6d
Author: Scott Violet <sky@chromium.org>
Date: Wed Sep 24 20:19:00 2014

MERGE: Fixes possible use after free in SessionService

SessionService::GetLastSession used a base::Unretained but there was
no guarantee that the SessionService would be valid by the time the
callback was processed.

BUG=399655
TEST=covered by test now
TBR=marja@chromium.org

Review URL: https://codereview.chromium.org/600113002

Cr-Commit-Position: refs/branch-heads/2125@{#468}
Cr-Branched-From: b68026d94bda36dd106a3d91a098719f952a9477-refs/heads/master@{#290040}

[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/base_session_service.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/base_session_service.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/session_service.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/session_service.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/session_service_test_helper.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/session_service_test_helper.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/aefd3b8ad196b8316638f36481efed6162255d6d/chrome/browser/sessions/session_service_unittest.cc


### in...@chromium.org (2014-09-24)

Sky, is the merge done (please add changeset number). If yes, change Merge-Approved to Merged-Merged and add label Release-0-M38.

### in...@chromium.org (2014-09-24)

my bad, i should have wait for commit to show up.

### ti...@chromium.org (2014-10-07)

Congratulations - $1000 reward for this plus an additional $500 fuzzer bonus (we're paying an additional $500 for each report that comes from a fuzzer hosted on Clusterfuzz). Total of $1500.

Notes from the panel: "needs user interaction and is racy"

### in...@chromium.org (2014-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-03)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-09)

Payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

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

This issue was migrated from crbug.com/chromium/399655?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080144)*
