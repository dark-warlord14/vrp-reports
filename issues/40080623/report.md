# UNKNOWN in SuperBlitter::blitH

| Field | Value |
|-------|-------|
| **Issue ID** | [40080623](https://issues.chromium.org/issues/40080623) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2014-10-11 |
| **Bounty** | $2,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 40.0.2184.0 (Developer Build) 

ASAN-trace:

==29498==ERROR: AddressSanitizer: SEGV on unknown address 0x7f4aea3c2f58 (pc 0x7f4b037e8651 bp 0x7f4ac67f9490 sp 0x7f4ac67f9460 T9)
    #0 0x7f4b037e8650 in SkAlphaRuns::Break(short*, unsigned char*, int, int) ??:0:0
    #1 0x7f4b037e678a in SuperBlitter::blitH(int, int, int) ??:0:0
    #2 0x7f4b037f29ed in walk_convex_edges(SkEdge*, SkPath::FillType, SkBlitter*, int, int, void (*)(SkBlitter*, int, bool)) ??:0:0
    #3 0x7f4b037f2014 in sk_fill_path(SkPath const&, SkIRect const*, SkBlitter*, int, int, int, SkRegion const&) ??:0:0
    #4 0x7f4b037e79f7 in SkScan::AntiFillPath(SkPath const&, SkRegion const&, SkBlitter*, bool) ??:0:0
    #5 0x7f4b03913c6d in SkAAClip::setPath(SkPath const&, SkRegion const*, bool) ??:0:0
    #6 0x7f4b037abbea in SkRasterClip::setPath(SkPath const&, SkRegion const&, bool) ??:0:0
    #7 0x7f4b037abead in SkRasterClip::op(SkPath const&, SkTSize<int> const&, SkRegion::Op, bool) ??:0:0
    #8 0x7f4b037201f5 in rasterclip_path(SkRasterClip*, SkCanvas const*, SkPath const&, SkRegion::Op, bool) ??:0:0
    #9 0x7f4b0371ffcb in SkCanvas::onClipRRect(SkRRect const&, SkRegion::Op, SkCanvas::ClipEdgeStyle) ??:0:0
.
.
.


## Attachments

- [chrome-SEGV-SkAlphaRunsBreak-min.html](attachments/chrome-SEGV-SkAlphaRunsBreak-min.html) (text/html, 531 B)

## Timeline

### cl...@chromium.org (2014-10-11)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4743293047930880

### cl...@chromium.org (2014-10-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4743293047930880

Uploader: mbarbella@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x7f7fdf426f58
Crash State:
  SuperBlitter::blitH
  walk_convex_edges
  sk_fill_path
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291041:291230

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96sDT-KCnrV9Kt-UdtIr2ms1jBq4zi2NAlTicw0qNhMllqrpHir61jMoGqgWtcK09Gd0G3t9qJ_XdLlKCi0DpBFTxKJot3jvNtRAI4HePam0qd4MxmX_q-u5pEbTtdjMysRmw7cYgmISWBXbo0TeBdn8cbK6A



### mb...@chromium.org (2014-10-12)

reed: Could you help find an owner for this one?

### mb...@chromium.org (2014-10-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-14)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2014-10-15)

proposed fix https://codereview.chromium.org/656473004/

### [Deleted User] (2014-10-15)

commit bcba2c9f9fcd14ac7123f9a7ac58fb834abba4e3
Author: reed <reed@google.com>
Date:   Wed Oct 15 08:52:00 2014 -0700

    interesct path bounds with clip bounds before initializing supersampler
    
    BUG=skia:
    
    Review URL: https://codereview.chromium.org/656473004


### in...@chromium.org (2014-10-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-16)

ClusterFuzz has detected this issue as fixed in range 299683:299856.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4743293047930880

Uploader: mbarbella@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x7f7fdf426f58
Crash State:
  SuperBlitter::blitH
  walk_convex_edges
  sk_fill_path
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291041:291230
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=299683:299856

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96sDT-KCnrV9Kt-UdtIr2ms1jBq4zi2NAlTicw0qNhMllqrpHir61jMoGqgWtcK09Gd0G3t9qJ_XdLlKCi0DpBFTxKJot3jvNtRAI4HePam0qd4MxmX_q-u5pEbTtdjMysRmw7cYgmISWBXbo0TeBdn8cbK6A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-21)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

$2000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/422693?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080623)*
