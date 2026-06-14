# Heap-use-after-free in WebCore::ApplyBlockElementCommand::rangeForParagraphSplittingTextNodesIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40078056](https://issues.chromium.org/issues/40078056) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | es...@chromium.org |
| **Created** | 2013-09-05 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4979070022451200

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x6080000221f4
Crash State:
  - crash stack -
  WebCore::ApplyBlockElementCommand::rangeForParagraphSplittingTextNodesIfNeeded
  WebCore::ApplyBlockElementCommand::formatSelection
  - free stack -
  WebCore::RenderObject::setStyle
  WebCore::Text::recalcTextStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=221237:221297

Minimized Testcase (3.84 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ZPQ85JGdNCtzu1h612-vYnMk8T4-dJjsZ-BltShVf2GpbV8LXfvkfhXgIuDpkJUOqX2ZFLY2W4-LADpMr1MtbmFyOCazAmrOp6DF1GijG243Ir27kvFWOXWEDm8H11dPvGAyBl8xHcxFMVPnKo-S0VNhE9Q

## Timeline

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-05)

http://src.chromium.org/viewvc/blink?view=rev&revision=157182 looks to have caused it.

### es...@chromium.org (2013-09-05)

I'm looking, worst case we can just roll it out.

### es...@chromium.org (2013-09-05)

Patch is up: https://codereview.chromium.org/23561004/

### bu...@chromium.org (2013-09-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157337

------------------------------------------------------------------------
r157337 | esprehn@chromium.org | 2013-09-06T01:48:59.667046Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/ApplyBlockElementCommand.cpp?r1=157337&r2=157336&pathrev=157337
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/ApplyBlockElementCommand.h?r1=157337&r2=157336&pathrev=157337

Don't use updateStyleForNodeIfNeeded in ApplyBlockElementCommand::rangeForParagraphSplittingTextNodesIfNeeded

It's not correct to use updateStyleForNodeIfNeeded in this method because it's going
to return a raw pointer to a RenderStyle and a later call could cause a style recalc
which would free this style (and might also change the style of this node).

Instead we should call updateStyleIfNeeded() before the calls to this method.

BUG=285787

Review URL: https://chromiumcodereview.appspot.com/23561004
------------------------------------------------------------------------

### in...@chromium.org (2013-09-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-07)

ClusterFuzz has detected this issue as fixed in range 221297:221323.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4979070022451200

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x6080000221f4
Crash State:
  - crash stack -
  WebCore::ApplyBlockElementCommand::rangeForParagraphSplittingTextNodesIfNeeded
  WebCore::ApplyBlockElementCommand::formatSelection
  - free stack -
  WebCore::RenderObject::setStyle
  WebCore::Text::recalcTextStyle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=221237:221297
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221297:221323

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96ZPQ85JGdNCtzu1h612-vYnMk8T4-dJjsZ-BltShVf2GpbV8LXfvkfhXgIuDpkJUOqX2ZFLY2W4-LADpMr1MtbmFyOCazAmrOp6DF1GijG243Ir27kvFWOXWEDm8H11dPvGAyBl8xHcxFMVPnKo-S0VNhE9Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### in...@chromium.org (2013-09-16)

Does not impact m30, fixing flags.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mi...@gmail.com (2013-09-26)

can I have the repro case please?

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $1000 reward. It does not qualify for a higher reward since there does not seem to be any control between the free and the use.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/285787?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078056)*
