# Security: Possible to retrieve cross-origin data in certain cases using devtools custom formatters

| Field | Value |
|-------|-------|
| **Issue ID** | [40096102](https://issues.chromium.org/issues/40096102) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | bm...@chromium.org |
| **Created** | 2019-08-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
When using the "with" statement on a cross-origin object (at least in the case where the associated cross-origin frame is within the same renderer), the devtools debugger will display the properties of the object, even if the frame being debugged doesn't have access to t

## Attachments

- [file1.html](attachments/file1.html) (text/plain, 1.1 KB)
- [file2.html](attachments/file2.html) (text/plain, 224 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096102)*
