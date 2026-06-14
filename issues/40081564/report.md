# Flash: use-after-free in display list handling from KeenTeam (repros 2-5, 6)

| Field | Value |
|-------|-------|
| **Issue ID** | [40081564](https://issues.chromium.org/issues/40081564) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-06 |
| **Bounty** | $4,000.00 |

## Description

Copying details from https://code.google.com/p/google-security-research/issues/detail?id=207

Adobe have since confirmed that repros 2-5 are one bug / code change, and repro 6 is a variant that required a separate code change, so recommending it be considered a different bug for reward purposes.

---
Credit is to "Jihui Lu of KeenTeam (@K33nTeam), working with the Chromium vulnerability reward program"

Flash player 15.0.0.239 in Chrome 39 Linux x64.

There is a use-after-free in display list handling. I attach a variety of repro cases, which I believe are all the same root cause based on crash stack traces.

The file "display_list_uaf6.swf" does seem to manifest differently and not be as reliable, so it is worth extra checking that any fix fixes this case.
---

## Attachments

- [display_list_uaf2.as](attachments/display_list_uaf2.as) (application/octet-stream, 2.2 KB)
- [display_list_uaf4.as](attachments/display_list_uaf4.as) (application/octet-stream, 1.6 KB)
- [display_list_uaf3.as](attachments/display_list_uaf3.as) (application/octet-stream, 1.8 KB)
- [display_list_uaf2.swf](attachments/display_list_uaf2.swf) (application/octet-stream, 1.2 KB)
- [display_list_uaf5.swf](attachments/display_list_uaf5.swf) (application/octet-stream, 1.1 KB)
- [display_list_uaf3.swf](attachments/display_list_uaf3.swf) (application/octet-stream, 1.1 KB)
- [display_list_uaf5.as](attachments/display_list_uaf5.as) (application/octet-stream, 1.6 KB)
- [display_list_uaf4.swf](attachments/display_list_uaf4.swf) (application/octet-stream, 1.1 KB)

## Timeline

### sc...@gmail.com (2015-03-07)

This is PSIRT-3170

### sc...@gmail.com (2015-03-26)

Fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-05.html

### sc...@gmail.com (2015-04-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

As discussed, reward should arrive this week.

### ti...@google.com (2015-09-14)

Missing unpaid tag.

### ra...@gmail.com (2015-09-30)

Why are these tagged with 0351 and 0342 both ?

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/464871?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081564)*
