# Security: use-after-poison in MarkSheetListDirty

| Field | Value |
|-------|-------|
| **Issue ID** | [40092500](https://issues.chromium.org/issues/40092500) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-09-19 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest ASAN build of chrome when loaded from a HTTP server. I was using the following flags: --no-sandbox --js-flags=--expose-gc .  
  
It is fairly unreliable and results in 2 out of 3 attempts in a null pointer crash. It helps to load

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092500)*
