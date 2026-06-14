# Security: OOB read/write in Array.prototype.sort

| Field | Value |
|-------|-------|
| **Issue ID** | [40091646](https://issues.chromium.org/issues/40091646) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2018-06-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**   
https://cs.chromium.org/chromium/src/v8/src/builtins/array.tq?rcl=6a21b5f98ec12d8e96e64f74f9ffb60a6fded7ce&l=578  
macro CanUseSameAccessor<ElementsAccessor : type>(  
    context: Context, receiver: Object, initialReceiverMap: Object,  
    initialReceiverLength: Number

## Attachments

- [sort-asan.log](attachments/sort-asan.log) (text/plain, 1.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 7.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091646)*
