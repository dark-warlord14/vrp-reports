# Memory corruption in blink::StyleColor

| Field | Value |
|-------|-------|
| **Issue ID** | [41495060](https://issues.chromium.org/issues/41495060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Color |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-01-26 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**   
I'm still investigating the root cause and will attach more analysis soon.  
  
Reproduction step:  
  
./chrome --no-sandbox http://localhost/poc.html  
  
**Problem Description:**   
renderer memory corruption  
  
**Additional Comments:**   
  
  
**Chrome v

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.5 KB)
- [harness.js](attachments/harness.js) (text/plain, 187.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 408 B)
- [poc2.html](attachments/poc2.html) (text/plain, 373 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41495060)*
