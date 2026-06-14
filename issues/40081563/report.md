# Flash: use-after-free in display list handling from KeenTeam (repro 1)

| Field | Value |
|-------|-------|
| **Issue ID** | [40081563](https://issues.chromium.org/issues/40081563) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-06 |
| **Bounty** | $3,000.00 |

## Description

Separating this repro out from https://code.google.com/p/google-security-research/issues/detail?id=207, because it turns out it's a separate root cause / code change, according to Adobe.

---
Credit is to "Jihui Lu of KeenTeam (@K33nTeam), working with the Chromium vulnerability reward program"

Confirmed: Flash player 15.0.0.239 in Chrome 39 Linux x64.
---

## Attachments

- [display_list_uaf1.swf](attachments/display_list_uaf1.swf) (application/octet-stream, 1.1 KB)
- [display_list_uaf1.as](attachments/display_list_uaf1.as) (application/octet-stream, 1.7 KB)

## Timeline

### sc...@gmail.com (2015-03-07)

This is tracked by Adobe as PSIRT-3385.

### ti...@google.com (2015-09-10)

Fixed based on https://code.google.com/p/google-security-research/issues/detail?id=207

### ti...@google.com (2015-10-09)

Congratulations - $3000 for this report.

### cl...@chromium.org (2015-12-17)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/464870?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081563)*
