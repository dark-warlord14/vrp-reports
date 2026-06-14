# Security: Debug check failed: element_size_log2 == 0 (\x2 vs. 0). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [41493285](https://issues.chromium.org/issues/41493285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91502
    - link: https://crrev.com/afee3b501bed785ae1739bb5c8da6ace5c823e7d 
- Commit Message

```
commit afee3b501bed785ae1739bb5c8da6ace5c823e7d
Author: Matt

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 1.5 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 4.9 KB)
- [poc_code.js](attachments/poc_code_53319761.js) (text/plain, 4.9 KB)
- [poc.js](attachments/poc_53319762.js) (text/plain, 1.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493285)*
