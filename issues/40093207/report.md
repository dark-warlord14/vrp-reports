# Security: WebGL heap-buffer-overflow in clearBufferuiv()

| Field | Value |
|-------|-------|
| **Issue ID** | [40093207](https://issues.chromium.org/issues/40093207) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebGL, Internals>GPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-11-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
This bug tested in stable chrome asan linux build (asan-linux-release-611016) Chromium 72.0.3623.0  
  
**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**   
  
=================================================================  
==9880==ERROR:

## Attachments

- [bug_01.html](attachments/bug_01.html) (text/plain, 378 B)
- [bug_01-asan.txt](attachments/bug_01-asan.txt) (text/plain, 20.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093207)*
