# Security: [v8] Type Confusion in Builtins_CallUndefinedReceiver1Handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40093900](https://issues.chromium.org/issues/40093900) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2019-01-30 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
A lazy-compiled function generates an interpreter code confusing smi value as a heap object. seems like it accesses a function object mutated to smi when generating a call stack.  
  
**VERSION**   
Chrome Version: 72.0.3626.81 stable (v8 7.2.502.24)  
Operating System:

## Attachments

- [test.html](attachments/test.html) (text/plain, 624 B)
- [test.html](attachments/test_53347303.html) (text/plain, 850 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093900)*
