# Security: Use-after-free in CPWL_Wnd::Destroy

| Field | Value |
|-------|-------|
| **Issue ID** | [40092844](https://issues.chromium.org/issues/40092844) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
Use-after-free in CPWL_Wnd::Destroy  
  
**VERSION**   
Operating System: Windows 10  
  
**REPRODUCTION CASE**   
1. Build chrome without XFA enabled   
2. open file `poc_controlEIP.pdf` in chrome  
  
  
(13c4.4d8): Access violation - code c0000005 (first chance)  
Fir

## Attachments

- [poc_controlEIP.pdf](attachments/poc_controlEIP.pdf) (application/pdf, 5.5 KB)
- [stacktrace_NoPageHeap.txt](attachments/stacktrace_NoPageHeap.txt) (text/plain, 21.0 KB)
- [stacktrace_PageHeap.txt](attachments/stacktrace_PageHeap.txt) (text/plain, 21.9 KB)
- [bug_898531.in](attachments/bug_898531.in) (application/octet-stream, 2.5 KB)
- [bug_898531.txt](attachments/bug_898531.txt) (text/plain, 23.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092844)*
