# UNKNOWN in _fini

| Field | Value |
|-------|-------|
| **Issue ID** | [40082059](https://issues.chromium.org/issues/40082059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5125299461685248

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x7f4a1ad16d75
Crash State:
  _fini
  SkBitmapDevice::drawPoints
  SkCanvas::onDrawPoints
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=328953:329019

Minimized Testcase (0.73 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95aKyiZMFofVHyJwPaf_ovxrFYJwXopJDVNHFUGqDdKJ0Ex6u4ZhAYBWA4qh19ZnmyPk0DhH9FYb-1lp7yCVcXAqL2284mpuCWNk8oZ6CxGxzEtwyRt_Y8V3n020nAxWemiaiqP_BwyDJokc9QtVPi0rAhrlg

Filer: mbarbella

## Timeline

### mb...@chromium.org (2015-05-11)

Bulk edit: I'm starting to look at some of the crashes from the batch of test cases we got now, but could use help with triage.

### mb...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### pe...@chromium.org (2015-05-14)

Hello,

M44 is branching tomorrow.  I'm pushing this issue to RB-Stable, but please fix as soon as possible and request a merge.

Cheers.

### cl...@chromium.org (2015-05-14)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

ClusterFuzz has detected this issue as fixed in range 330167:330204.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5125299461685248

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x7f4a1ad16d75
Crash State:
  _fini
  SkBitmapDevice::drawPoints
  SkCanvas::onDrawPoints
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=328953:329019
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=330167:330204

Minimized Testcase (0.73 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95aKyiZMFofVHyJwPaf_ovxrFYJwXopJDVNHFUGqDdKJ0Ex6u4ZhAYBWA4qh19ZnmyPk0DhH9FYb-1lp7yCVcXAqL2284mpuCWNk8oZ6CxGxzEtwyRt_Y8V3n020nAxWemiaiqP_BwyDJokc9QtVPi0rAhrlg

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-18)

ClusterFuzz has detected this issue as fixed in range 329829:329845.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5125299461685248

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x7f4a1ad16d75
Crash State:
  _fini
  SkBitmapDevice::drawPoints
  SkCanvas::onDrawPoints
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=328953:329019
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=329829:329845

Minimized Testcase (0.73 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95aKyiZMFofVHyJwPaf_ovxrFYJwXopJDVNHFUGqDdKJ0Ex6u4ZhAYBWA4qh19ZnmyPk0DhH9FYb-1lp7yCVcXAqL2284mpuCWNk8oZ6CxGxzEtwyRt_Y8V3n020nAxWemiaiqP_BwyDJokc9QtVPi0rAhrlg

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### oc...@chromium.org (2015-05-18)

This is a bug in PtProcRec::chooseProc (once again this occurs because this is checked by an SkAssert):

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/core/SkDraw.cpp&sq=package:chromium&type=cs&l=478&rcl=1431949430

fMode is not checked here, and is used to index into a static array of function pointers which is then called in SkDraw::drawPoints.

### oc...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-05-20)

Can one of the SKIA folks in the CC list take ownership of this bug and investigate? It's been open for about ten days and it would be good to get this going :) Thanks!

### mb...@chromium.org (2015-05-20)

The fix for https://crbug.com/chromium/486947 should cover this as well.

### am...@chromium.org (2015-05-20)

Is there a merge required here?

### cl...@chromium.org (2015-05-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### pe...@chromium.org (2015-06-30)

No merge required here. (https://crbug.com/chromium/486947 is approved for merge, and is the fix for this.) 

### ti...@google.com (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-28)

@cloudfuzzer - another $5,000 here. Looks like it's an array of function pointers - what could possibly go wrong? :)

### aw...@chromium.org (2016-07-01)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/486946?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082059)*
