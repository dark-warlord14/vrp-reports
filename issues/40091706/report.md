# Security: OOB read in Array.prototype.sort

| Field | Value |
|-------|-------|
| **Issue ID** | [40091706](https://issues.chromium.org/issues/40091706) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2018-06-19 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**   
https://cs.chromium.org/chromium/src/v8/src/builtins/array-sort.tq?rcl=dd5dd45db8522e2c7b3b3b9ae80132b6d0b8bc24&l=185  
  macro ArrayInsertionSort<E : type>(  
      context: Context, receiver: Object, elements: Object,  
      initialReceiverMap: Object, initialReceiver

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 1022 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091706)*
