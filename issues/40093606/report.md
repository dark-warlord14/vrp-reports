# Security: Cross origin resource size infoleak

| Field | Value |
|-------|-------|
| **Issue ID** | [40093606](https://issues.chromium.org/issues/40093606) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2018-12-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
It is possible to leak cross-origin resources exact size using appcache + storage estimator.  
  
To exploit it it is enough to have entry in cache manifest file for this cross origin resource and then receive size using storage size estimator. If some more bytes are add

## Attachments

- [attack.py](attachments/attack.py) (text/plain, 313 B)
- [index.html](attachments/index.html) (text/plain, 776 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093606)*
