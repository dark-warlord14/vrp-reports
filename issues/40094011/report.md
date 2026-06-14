# Security: READ heap-buffer-overflow in libxslt (type confusion?)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094011](https://issues.chromium.org/issues/40094011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2019-02-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
The following XSLT stylesheet will trigger a READ heap buffer overflow (as detected by ASan). Given that namespaces (a special type of nodes in libxslt) are invloved, I'd bet on another (cf https://bugs.chromium.org/p/chromium/issues/detail?id=583156) type confusion b

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094011)*
