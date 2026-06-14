# Security: heap-use-after-free in blink::NGPaintFragment::AssociateWithLayoutObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40095442](https://issues.chromium.org/issues/40095442) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout, Blink>Paint |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2019-06-19 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**   
  
**VULNERABILITY DETAILS**   
The following testcase crashes the latest ASAN build of content_shell  
  
**VERSION**   
Chrome Version: asan-linux-release-670550  
Operating System: Linux 64bit  
  
**REPRODUCTION CASE**   
<script>  
function start() {  
        o

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095442)*
