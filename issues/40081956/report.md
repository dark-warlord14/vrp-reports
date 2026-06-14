# ASSERTION FAILED: !object || (object->isBox())

| Field | Value |
|-------|-------|
| **Issue ID** | [40081956](https://issues.chromium.org/issues/40081956) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ro...@chromium.org |
| **Created** | 2015-04-28 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5913874063163392

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: !object || (object->isBox())
  blink::HitTestResult::imageAreaForImage
  blink::HitTestResult::setInnerNode
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96HhfYRyGPk7e1_fL_k7g21TeDruySgnMCsWljCll3h3wmGvrr0Ox4eUhgWw-HPGs6qakTJiuCTaSlE3-SSJf3KXTUqQUuHmGOY3avSYkXB_av7MRKkbz8ki0vgkAJKBP-PC0gfekm59_7621i1DBizNdbtRg


Filer: inferno

## Timeline

### cl...@chromium.org (2015-04-28)

[Comment Deleted]

### in...@chromium.org (2015-04-28)

regression from https://chromium.googlesource.com/chromium/blink/+/9b3210f36d993dc01de27414a5dc807cdb9e845a

### pd...@chromium.org (2015-04-28)

Oops, an image isn't always a box I guess.

### cl...@chromium.org (2015-04-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=194773

------------------------------------------------------------------
r194773 | robhogan@gmail.com | 2015-04-30T21:21:39.926003Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/replaced/image-map-alt-content-crash.html?r1=194773&r2=194772&pathrev=194773
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/layout/HitTestResult.cpp?r1=194773&r2=194772&pathrev=194773
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/replaced/image-map-alt-content-crash-expected.txt?r1=194773&r2=194772&pathrev=194773

Use the correct node when hit testing on an image map

This was a slip during https://codereview.chromium.org/1094133004 - I meant to use
the imageElement's layout object, not the one associated with whatever node had
been hit in the alt content.

BUG=482214

Review URL: https://codereview.chromium.org/1119813002
-----------------------------------------------------------------

### in...@chromium.org (2015-04-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-14)

Congrats - $2,500 for this report. ($2000 for the bug, $500 for the ClusterFuzz bonus)

Also taking this through the new payment process.

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/482214?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/482309]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081956)*
