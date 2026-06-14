# Use-after-free in WebCore::RootInlineBox::closestLeafChildForPoint

| Field | Value |
|-------|-------|
| **Issue ID** | [40078923](https://issues.chromium.org/issues/40078923) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Reporter** | cl...@chromium.org |
| **Assignee** | yu...@chromium.org |
| **Created** | 2014-02-16 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4618611087900672

Fuzzer: Miaubiz_css_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x0aeefef3
Crash State:
  - crash stack -
  WebCore::RootInlineBox::closestLeafChildForPoint
  WebCore::previousLinePosition
  - free stack -
  WebCore::RootInlineBox::`scalar deleting destructor'
  WebCore::RootInlineBox::destroy
  

Minimized Testcase (155.13 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95iclDkuf_higdy9z5Ivhscm--8RrOzeK-Q_ptEpX1hVekUqqfHF3JteZAEZ1k3c1UGyzp9jDWs3eYtqHhPKJHhTrTr1zjm-UM_HKpwADsLauRlvQGQ0MrDipVYfIpgJGIgxDwLm4_65kvKAvslLC3kug-D3kopdAHPhajGzvL1bsO-WmM

## Timeline

### in...@chromium.org (2014-02-16)

Looks like old bug - RenderObject* renderer = root->closestLeafChildForPoint(pointInLine, isEditablePosition(p))->renderer(); . isEditablePosition triggers layout, and then root is a raw pointer which gets accessed.

### cl...@chromium.org (2014-02-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-25)

yosin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### yu...@chromium.org (2014-02-27)

I tried to reproduce this on syzyasan Chromium but couldn't.
Is there any special instruction required to reproduce this?

### in...@chromium.org (2014-02-27)

i clicked redo on report to see if cf can tell if this is fixed or not.

### yu...@chromium.org (2014-03-03)

ClusterFuzz page says it's fixed, so I assume this has become unreproducible
and I'm closing the issue.

### in...@chromium.org (2014-03-03)

might be http://src.chromium.org/viewvc/blink?view=rev&revision=167275 that fixed this.

### cl...@chromium.org (2014-03-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-25)

Adding this to reward spreadsheet.

### ti...@chromium.org (2014-05-13)

Congrats - $1000 for this one.

### cl...@chromium.org (2014-06-09)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/344230?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078923)*
