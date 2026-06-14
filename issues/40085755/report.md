# Security: V8 OOB read/write in asm.js

| Field | Value |
|-------|-------|
| **Issue ID** | [40085755](https://issues.chromium.org/issues/40085755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-10-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**   
Out of bound read/write is possible after optimizing some asm.js code.  
  
**VERSION**   
Chrome 54.0.2840.71 stable  
V8 5.4.500.36 32bit  
  
**REPRODUCTION CASE**   
--------------------------- poc.js -------------  
boom0 = (function(stdlib, foreign, heap){

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085755)*
