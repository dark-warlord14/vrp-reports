# Security: potential UAF in pdfium timer

| Field | Value |
|-------|-------|
| **Issue ID** | [40086459](https://issues.chromium.org/issues/40086459) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ji...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

There is js timer implementation in src/third\_party/pdfium/fpdfsdk/javascript/app.cpp.

When GlobalTimer is removed, it must delete <timer ID>-><GlobalTimer> mapping, but if m\_TimerID is 0, it doesn't remove it.

On Line 81:  

GlobalTimer::~GlobalTimer() {  

if (!m\_nTimerID)  

return;

if (GetRuntime())  

m\_pFormFillEnv->GetSysHandler()->KillTimer(m\_nTimerID);

GetGlobalTimerMap()->erase(m\_nTimerID);  

}

Additionally, GetGlobalTimerMap is referenced in GlobalTimer::Trigger, which is called as timer callback. However if m\_nTimerID is 0, it doesn't kill the timer, so it seems like UAF.

**VERSION**  

Chrome Version: 55.0.2883.87 stable  

Operating System: Windows 10

**REPRODUCTION CASE**  

For now there is memory leak on app.setTimeOut / app.clearTimeOut, so can't reproduce in my laptop.

## Timeline

### ji...@gmail.com (2017-01-10)

However after 16 hours of waiting, it can be triggered without memory leak. The step is:

1. Have a textbox field
2. focus on that field and other field, again and again. The caret creates timer and kills the timer when focused/unfocused.
3. Loop.

42 sec on 0x400000 tries..

### ji...@gmail.com (2017-01-10)

Possible mitigations would be adjusting timerid as 64bit, or just remove the check.

### ts...@chromium.org (2017-01-11)

Thanks for the report.  Having an ID that can't overflow seems desirable, even if the check is removed.

### ts...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2017-01-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-01-11)

https://cs.chromium.org/chromium/src/third_party/pdfium/public/fpdf_formfill.h?rcl=1484151649&l=508 means that the timer ID comes from the embedder as an int and can't be enlarged without a public API change.  So much for that idea.

### ts...@chromium.org (2017-01-11)

CL at https://codereview.chromium.org/2626863003/

### mb...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff

commit 34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Thu Jan 12 22:28:15 2017

Roll src/third_party/pdfium/ db7647083..98d00b230 (4 commits).

https://pdfium.googlesource.com/pdfium.git/+log/db7647083d0a..98d00b230aa1

$ git log db7647083..98d00b230 --date=short --no-merges --format='%ad %ae %s'
2017-01-12 dsinclair Remove used items from the CSS code.
2017-01-12 tsepez Don't put timers with ID == 0 into the global timer map.
2017-01-12 tsepez Custom toString() methods may delete annots.
2017-01-12 npm Fix leak in OJPEGReadHeaderInfoSecTablesAcTable when read fails.

BUG=679649,679643,680520

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2627073004
Cr-Commit-Position: refs/heads/master@{#443386}

[modify] https://crrev.com/34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff/DEPS


### ts...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

The panel decided to award $500 for this bug.  Cheers!

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-03)

+awhalley@ for M57 merge review.

### aw...@chromium.org (2017-02-12)

+govind: good to approve for 57.  Note that we only need a merge of "Don't put timers with ID == 0 into the global timer map." not necessarily the full DEPS roll.

### go...@chromium.org (2017-02-13)

Approving merge to M57 branch 2987. Please refer to https://crbug.com/chromium/679649#c21 before merging. Thank you.

### go...@chromium.org (2017-02-13)

[Comment Deleted]

### go...@chromium.org (2017-02-14)

If possible, please merge your change to M57 branch 2987 today (Tuesday) before 5:00 PM PT so we can pick it up for this week beta release. Thank you.

### sh...@chromium.org (2017-02-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-16)

Please merge your change to M57 branch 2987 before 5:00 PM PT Friday (02/17), so we can pick it up for next week Beta release. Thank you.

### go...@chromium.org (2017-02-17)

Please merge your change to M57 branch 2987 before 5:00 PM PT Monday (02/20), so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2017-02-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-21)

Please merge your change to M57 branch 2987 by 5:00 PM PT Tuesday (02/21) so we can pick it up for this week beta release. Thank you.

### go...@chromium.org (2017-02-25)

Please merge your change to M57 branch 2987 by 5:00 PM PT Monday (02/27) so we can take it in for next week last M57 Desktop Beta release before Stable promotion. Thank you.

### th...@chromium.org (2017-02-25)

sheriffbot is being a bit silly. The fix made it in before M57 branched. We should have merged to M56, but now it's probably too late for that, so nothing to do here except for removing the merge label.

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679649?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086459)*
