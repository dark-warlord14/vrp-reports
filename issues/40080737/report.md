# Heap-use-after-free in base::SupportsUserData::GetUserData

| Field | Value |
|-------|-------|
| **Issue ID** | [40080737](https://issues.chromium.org/issues/40080737) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | wj...@chromium.org |
| **Created** | 2014-10-30 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5817579653300224

Fuzzer: Cdiehl_peach
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61b00015f5a0
Crash State:
  base::SupportsUserData::GetUserData
  ZoomBubbleView::Refresh
  ZoomBubbleView::ShowBubble
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95M0IDCeVOpcaUz5RPKwKF11F-wBuKlQH8DSH5qxsNgrL7rUKSPpvCXFSxT_2j1fS4JEpJtjgo884ZTDycigJpafTQTCTBNWNeCDwQp454nFJOiit5Q62Dh_RikojXK3ppyngHCktL9DAcVB44-8vi9PhaV6Q


Additional requirements: Requires Gestures

Filer: inferno

## Timeline

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-11-03)

this appears to be a lifetime issue for a WebContentsView that's closed when trying to zoom.  There are zoom gestures in the test case.

could be 63d1f9b9a1fb0e67739fdfe59d4aa5a978bf95ac

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-06)

wjmaclean@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-11-10)

wjmaclean: Ping? This is a high severity security bug, can you please take a look asap?

### wj...@chromium.org (2014-11-10)

Yes, looking at it now ...

### wj...@chromium.org (2014-11-10)

Proposed fix at https://codereview.chromium.org/712993004/

### me...@chromium.org (2014-11-11)

Thanks for the quick fix.

### ma...@google.com (2014-11-11)

[Empty comment from Monorail migration]

### wj...@chromium.org (2014-11-11)

So I built ToT asan-chrome and ran it with the ClusterFuzz-on-demand local repro script, and after 1000 iterations on my workstation it has failed to reproduce.

That being said, studying the stacktrace has revealed a mechanism that explains the ASAN stack trace, namely that ZoomBubbleView (which is a singleton accessed via the static ShowBubble() function) can hold onto a stale WebContents*. Even if we cannot reproduce the test result, I think we should fix the pathway regardless.

### mb...@chromium.org (2014-11-11)

Speculatively setting stable impact.

### cl...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d1b6f4d89d002808689a156b739f8d7fd80104fb

commit d1b6f4d89d002808689a156b739f8d7fd80104fb
Author: wjmaclean <wjmaclean@chromium.org>
Date: Thu Nov 13 00:56:09 2014

Reset singleton ZoomBubbleView::zoom_bubble_ in ::Close()

The current implementation of ZoomBubbleView is capable of attempting to re-use a zoom bubble with a stale WebContents*.

This CL resets ZoomBubbleView::zoom_bubble_ in the ZoomBubbleView::Close() method to avoid inadvertent reuse. It also adds a DCHECK to make sure WebContents* are never mis-matched in calls to ZoomBubbleView::ShowBubble().

BUG=428561

Review URL: https://codereview.chromium.org/712993004

Cr-Commit-Position: refs/heads/master@{#303945}

[modify] https://chromium.googlesource.com/chromium/src.git/+/d1b6f4d89d002808689a156b739f8d7fd80104fb/chrome/browser/ui/views/location_bar/zoom_bubble_view.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/d1b6f4d89d002808689a156b739f8d7fd80104fb/chrome/browser/ui/views/location_bar/zoom_bubble_view_browsertest.cc


### wj...@chromium.org (2014-11-13)

Speculatively marking 'fixed', please re-open if needed.

### cl...@chromium.org (2014-11-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### wj...@chromium.org (2014-11-24)

[Empty comment from Monorail migration]

### ma...@google.com (2014-11-24)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### ma...@google.com (2014-11-24)

Approved for M40 (branch: 2214)

### bu...@chromium.org (2014-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f54d31218e0cc558e14dcf5814be5c21d7987bc

commit 6f54d31218e0cc558e14dcf5814be5c21d7987bc
Author: W. James MacLean <wjmaclean@chromium.org>
Date: Mon Nov 24 21:16:58 2014

Reset singleton ZoomBubbleView::zoom_bubble_ in ::Close()

The current implementation of ZoomBubbleView is capable of attempting to
re-use a zoom bubble with a stale WebContents*.

This CL resets ZoomBubbleView::zoom_bubble_ in the
ZoomBubbleView::Close() method to avoid inadvertent reuse. It also adds
a DCHECK to make sure WebContents* are never mis-matched in calls to
ZoomBubbleView::ShowBubble().

BUG=428561

Review URL: https://codereview.chromium.org/712993004

Cr-Commit-Position: refs/heads/master@{#303945}
(cherry picked from commit d1b6f4d89d002808689a156b739f8d7fd80104fb)

TBR=wjmaclean

Review URL: https://codereview.chromium.org/752153005

Cr-Commit-Position: refs/branch-heads/2214@{#127}
Cr-Branched-From: 03655fd3f6d72165dc3c9bd2c89807305316fe6c-refs/heads/master@{#303346}

[modify] http://crrev.com/6f54d31218e0cc558e14dcf5814be5c21d7987bc/chrome/browser/ui/views/location_bar/zoom_bubble_view.cc
[modify] http://crrev.com/6f54d31218e0cc558e14dcf5814be5c21d7987bc/chrome/browser/ui/views/location_bar/zoom_bubble_view_browsertest.cc


### [Deleted User] (2014-12-01)

Looks like it's in M-40, please rerequest if you want to get this into 39.

### am...@chromium.org (2014-12-02)

merge approved for m39 branch 2171

### wj...@chromium.org (2014-12-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-05)

sec-medium, since it needs too many gestures and is racy.

### ti...@google.com (2015-01-22)

Congratulations - $1500 for this report. Notes from the reward panel: "$1000 for the bug as it needs many gestures and is racy, +$500 ClusterFuzz bonus".



### cl...@chromium.org (2015-02-19)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/428561?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/412783]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080737)*
