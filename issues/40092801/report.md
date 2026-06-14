# Security:  assert 'srcPos <= GetReceiverLengthProperty(sortState) - length' at array-sort.tq:613:

| Field | Value |
|-------|-------|
| **Issue ID** | [40092801](https://issues.chromium.org/issues/40092801) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-10-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the latest Debug build of d8 on ARM64  
  
**VERSION**   
Chrome Version: v8 latest   
Operating System: Linux on ARM64  
  
**REPRODUCTION CASE**   
function opt(ar){  
        Array.prototype.unshift(2.3023e-320)  
}  
ar={};  
for(var xo

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092801)*
