# Use after free in table :before, :after content.

| Field | Value |
|-------|-------|
| **Issue ID** | [40096132](https://issues.chromium.org/issues/40096132) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-10-11 |
| **Bounty** | $1,000.00 |

## Description

credit:miaubiz

Testcase::
<html>
  <head>
    <style>
      @font-face { font-family: A; src: url(); }

      .tr {
        font-family: A;
        display: table-row;
      }

      .td {
        display: table-cell;
      }

      div.tr:before {
        content:"A";
      }
      div.tr:after {
        content:"B";
      }
    </style>
  </head>
  <body>
    <div class="tbody">
      <div class="tr">
        <div class="td"></div>
      </div>
    </div>
  </body>
</html>
<style>
</style>

## Timeline

### in...@chromium.org (2011-10-11)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=69854

### in...@chromium.org (2011-10-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-11)

Fixed in http://trac.webkit.org/changeset/97180, and changelog fixed in r97181(bad update-webkit)

merged to m15 in r97183.

### in...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/99880?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096132)*
