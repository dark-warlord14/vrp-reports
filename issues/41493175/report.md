# Security: Signal SIGSEGV in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493175](https://issues.chromium.org/issues/41493175) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-01-20 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91451
    - link: https://crrev.com/92d982471f346255af8a75024dc5f0792392436d
- Commit Message

```
commit 92d982471f346255af8a75024dc5f0792392436d
Author: Olivi

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)
- [poc.js](attachments/poc_53263912.js) (text/plain, 1.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493175)*
