# UNKNOWN in SkRegion::setPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40078590](https://issues.chromium.org/issues/40078590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fm...@chromium.org |
| **Created** | 2013-12-20 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5728750750662656

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0001fffffff3
Crash State:
  - crash stack -
  SkRegion::setPath
  SkRasterClip::setPath
  SkCanvas::clipPath
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232571:232580

Minimized Testcase (10.27 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96U98sNUo9J-jaHhqQdy6aQK84H2ciR-mvS1QmgZNZztSZ-4jpZqXw5V3IDv-xcV-cU2EsYlDVlNg-gum1fQiKvt5s9z3CsLzpMBZiuSj6zUxNwjpOdA9yIQwlkN-E6KD6mNlbkVR-MewJYmLEVk99XWz6djw

## Timeline

### mb...@chromium.org (2013-12-20)

I think that http://src.chromium.org/viewvc/blink?revision=161169&view=revision may be related to this issue.

Could you take a look or help find another owner for this when you get a chance?

### cl...@chromium.org (2013-12-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-29)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### fm...@chromium.org (2013-12-30)

Looking.

### fm...@chromium.org (2013-12-30)

It's possible that r161169 exposed this, but it looks like a Skia problem. Patch up: https://codereview.chromium.org/122313002/

### in...@chromium.org (2014-01-01)

http://code.google.com/p/skia/source/detail?r=12846

### cl...@chromium.org (2014-01-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-02)

ClusterFuzz has detected this issue as fixed in range 241995:242017.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5728750750662656

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0001fffffff3
Crash State:
  - crash stack -
  SkRegion::setPath
  SkRasterClip::setPath
  SkCanvas::clipPath
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=232571:232580
Fixed: https://cluster-fuzz.appspot.com/revisions?range=241995:242017

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96U98sNUo9J-jaHhqQdy6aQK84H2ciR-mvS1QmgZNZztSZ-4jpZqXw5V3IDv-xcV-cU2EsYlDVlNg-gum1fQiKvt5s9z3CsLzpMBZiuSj6zUxNwjpOdA9yIQwlkN-E6KD6mNlbkVR-MewJYmLEVk99XWz6djw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### dh...@google.com (2014-01-07)

[Empty comment from Monorail migration]

### la...@google.com (2014-01-08)

[Empty comment from Monorail migration]

### fm...@chromium.org (2014-01-08)

Merged to m33: https://code.google.com/p/skia/source/detail?r=12963

Requesting merge to m32 also.

### dh...@google.com (2014-01-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-17)

approved for M32

### fm...@chromium.org (2014-01-17)

Merged in M32: https://code.google.com/p/skia/source/detail?r=13123


### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-27)

Thanks, miaubiz! This qualifies for a $3000 reward. It seems like it is possible for an attacker to control the address that is freed in this case.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-17)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!

### cl...@chromium.org (2014-04-09)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-1-M32 label.

- Your friendly ClusterFuzz

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

This issue was migrated from crbug.com/chromium/330293?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078590)*
