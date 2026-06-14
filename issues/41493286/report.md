# Security: Debug check failed: displacement == 0 in V8.

| Field | Value |
|-------|-------|
| **Issue ID** | [41493286](https://issues.chromium.org/issues/41493286) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-01-21 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91860
    - link: https://crrev.com/bed95642cb2f4d5e9dc490d5b58085b1f2a3c870 
- Commit Message

```
commit bed95642cb2f4d5e9dc490d5b58085b1f2a3c870
Author: Matt

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 3.6 KB)
- [poc_code.js](attachments/poc_code.js) (text/plain, 14.6 KB)
- [poc (1).js](attachments/poc (1).js) (text/plain, 3.4 KB)
- [poc_code (1).js](attachments/poc_code (1).js) (text/plain, 13.7 KB)
- [poc.js](attachments/poc_53164658.js) (text/plain, 3.6 KB)
- [poc_code.js](attachments/poc_code_53164659.js) (text/plain, 14.6 KB)
- [poc.js](attachments/poc_53164711.js) (text/plain, 3.4 KB)
- [poc_code.js](attachments/poc_code_53164712.js) (text/plain, 13.7 KB)
- [poc.js](attachments/poc_53164756.js) (text/plain, 3.0 KB)
- [poc_code.js](attachments/poc_code_53164757.js) (text/plain, 14.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493286)*
