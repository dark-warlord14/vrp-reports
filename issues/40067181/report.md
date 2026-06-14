# Security: Segment Fault in v8 wasm at address > page size

| Field | Value |
|-------|-------|
| **Issue ID** | [40067181](https://issues.chromium.org/issues/40067181) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-07-11 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 88364
    - link: https://crrev.com/a81cc3b433d1660528b5da5c97a4396ab35debe7 
- Commit Message

```
commit a81cc3b433d1660528b5da5c97a4396ab35debe7
Author: Jian

## Attachments

- [wasm.js](attachments/wasm.js) (text/plain, 4.2 KB)
- [wasm.js](attachments/wasm_53102300.js) (text/plain, 4.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067181)*
