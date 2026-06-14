# Security: Malicious link opens multiple tabs via URI handler 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094180](https://issues.chromium.org/issues/40094180) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Core |
| **Platforms** | Windows |
| **Reporter** | jp...@gmail.com |
| **Assignee** | je...@google.com |
| **Created** | 2019-03-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
Someone can craft a malicious URL that will trick chrome into opening multiple tabs when the URL is activated. This bug is closely related to https://bugs.chromium.org/p/chromium/issues/detail?id=933004. I did mention the bug described below in https://crbug.com/chrom

## Attachments

- [OrderOfOperations.png](attachments/OrderOfOperations.png) (image/png, 2.2 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094180)*
