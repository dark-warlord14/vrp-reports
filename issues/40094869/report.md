# Multiple file download protection bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40094869](https://issues.chromium.org/issues/40094869) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-05-05 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Chrome has multiple file download protection. But download request followed by cross-origin redirect can cause multiple download if final end point after redirect results in download.  
  
**VERSION**   
Chrome Version:74 stable  
Operating System: Windows 10  
  
**REPR

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094869)*
