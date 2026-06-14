# Security: Arbitrary bad cast in optimized Javascript code

| Field | Value |
|-------|-------|
| **Issue ID** | [40088597](https://issues.chromium.org/issues/40088597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Reporter** | sk...@chromium.org |
| **Assignee** | ms...@chromium.org |
| **Created** | 2017-08-03 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
Specially crafted JavaScript can cause Chrome to use an instance of any class as if it was an instance of pretty much any other class. This allows an "arbitrary bad cast": an attacker can call almost any method of almost any class `A` on an object of almost any other class `B`

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 133 B)
- [PoC - write-what-where.html](attachments/PoC - write-what-where.html) (text/plain, 1.6 KB)
- [PoC - information disclosure.html](attachments/PoC - information disclosure.html) (text/plain, 12.2 KB)
- [AVR@NULL fdd.fbd @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։M11.html](attachments/AVR@NULL fdd.fbd @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։M11.html) (text/plain, 167.8 KB)
- [AV_@Invalid 7b5.537 @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։SetM11.html](attachments/AV_@Invalid 7b5.537 @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։SetM11.html) (text/plain, 177.3 KB)
- [PoC - code execution.html](attachments/PoC - code execution.html) (text/plain, 15.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088597)*
