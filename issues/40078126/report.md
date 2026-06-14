# Heap-use-after-free in WebCore::RenderObject::childAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40078126](https://issues.chromium.org/issues/40078126) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing |
| **Reporter** | cl...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2013-09-19 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
The following testcase crashes the Chrome ASAN build.  
  
**VERSION**   
Chrome Version: asan-symbolized-linux-release-223354  
Operating System: Linux 64-bit  
  
**REPRODUCTION CASE**   
  
<html>  
<head>  
<script>  
function start() {  
o2=document.createElement('i

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain; charset=us-ascii, 17.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078126)*
