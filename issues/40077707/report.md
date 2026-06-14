# Heap-use-after-free in WebCore::RenderObject::destroyAndCleanupAnonymousWrappers

| Field | Value |
|-------|-------|
| **Issue ID** | [40077707](https://issues.chromium.org/issues/40077707) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | cl...@chromium.org |
| **Assignee** | tk...@chromium.org |
| **Created** | 2013-06-27 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4593723610497024

Fuzzer: Miaubiz_css_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x619002994a10
Crash State:
  - crash stack -
  WebCore::RenderObject::destroyAndCleanupAnonymousWrappers
  WebCore::Node::detach
  - free stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=207299:207325

Minimized Testcase (7.81 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94aUQLOWpzA3qWjHnScZUXGczCQC4mHbBISZDIZirO0Zkn8tMMg-gkDloB2IuioGjuUHJSYPd-UEx4NJftVKbtFvqhkPavg4oiuU1_oxi4zA-2VCnS5decj4aUjM0t6OiddP5eZWF51o_2ckxLRDR41i-OvGg

## Timeline

### in...@chromium.org (2013-06-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-06-27)

Looks like regression from http://src.chromium.org/viewvc/blink?view=rev&revision=152700. I can't see anything else related to shadow dom in the regression range.

### tk...@chromium.org (2013-06-27)

Confirmed this was a regression by blink r152700.


### tk...@chromium.org (2013-06-30)

Fixed: http://src.chromium.org/viewvc/blink?view=revision&revision=153212


### tk...@chromium.org (2013-07-03)

> Fixed: http://src.chromium.org/viewvc/blink?view=revision&revision=153212

It seems this made a regression. See https://crbug.com/chromium/256732.
This issue affects M29 branch. I recommend to revert Blink r152700 from M29 branch rather than merging Blink r153212 and a coming fix of https://crbug.com/chromium/256732.


### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-31)

Ok. Reverted r152700 on M29 branch (http://src.chromium.org/viewvc/blink?view=revision&revision=155218) as suggested. Thanks.

### sc...@gmail.com (2013-08-11)

Nice regression catch, $1000

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/254783?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077707)*
