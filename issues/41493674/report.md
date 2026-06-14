# Security: Debug check failed: start_instr <= end_instr . in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493674](https://issues.chromium.org/issues/41493674) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-01-23 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91736
    - link: https://crrev.com/4a31b449133e3c1315e46fa7b15529e7fa4ae879 
- Commit Message

```
commit 4a31b449133e3c1315e46fa7b15529e7fa4ae879
Author: Dari

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 920 B)
- [poc.js](attachments/poc_53087948.js) (text/plain, 920 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493674)*
