# Security: Debug check failed: is_loadable(). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41494611](https://issues.chromium.org/issues/41494611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-01-25 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91912
    - link: https://crrev.com/16f9aac2b8b4fd89768519b130afff47728b9136 
- Commit Message

```
commit 16f9aac2b8b4fd89768519b130afff47728b9136
Author: Oliv

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 383 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494611)*
