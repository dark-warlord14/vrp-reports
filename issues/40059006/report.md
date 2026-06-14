# Heap-use-after-free in WebCore::RenderBlock::layoutPositionedObjects

| Field | Value |
|-------|-------|
| **Issue ID** | [40059006](https://issues.chromium.org/issues/40059006) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-05-30 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=46677350

Fuzzer: Marty_html_twiddler

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f7811c9cab0
Crash State:
  - crash stack -
  WebCore::RenderBlock::layoutPositionedObjects
  WebCore::RenderDeprecatedFlexibleBox::layoutBlock
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (1.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95m2BedSgxuLAmjDboV5eQIcDGtfSamebgW6P_seK7AnDbOC3YRLCqO1IJiSOEquwXjZPB4bjLtngaHbp8DrRK9Xry47YX5Wq-vSZKlmOqjfZZiVCp0Cjcxh7uWyAWZZVHDV4yBQOqyn06hzd8g1q6ky1eHtw

## Timeline

### in...@chromium.org (2012-05-30)

Waiting to get better repros...

### in...@chromium.org (2012-06-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-06-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-06-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-06-04)

I am going this and 130605 in one shot. Adding reward-topanel from duped bug.

### in...@chromium.org (2012-06-04)

http://trac.webkit.org/changeset/119409

### sc...@gmail.com (2012-06-07)

M20: http://trac.webkit.org/changeset/119646

### sc...@gmail.com (2012-08-20)

@miaubiz: thanks for your help here.
According to Abhishek, your test case was for a different bug in the same function, which helped to make sure the fix was thorough.
$1000


### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-09-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/130369?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/130605, crbug.com/chromium/130886]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059006)*
