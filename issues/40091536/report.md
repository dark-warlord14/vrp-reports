# Security: V8 Incorrect type cast in String.p.split function leads to OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [40091536](https://issues.chromium.org/issues/40091536) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $5,000.00 |

## Description

This vulnerability exists in 64-bit v8 in the String.p.slit CSA code. The allocation size is stored in int64 but improperly casted to smi which causes the allocated space too small and OOB write. It may potentially lead to remote code execution.  
  
POC  
var str2 = String.fromCharCode(0x2c);//add

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 150 B)
- [v8.patch](attachments/v8.patch) (application/octet-stream, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091536)*
