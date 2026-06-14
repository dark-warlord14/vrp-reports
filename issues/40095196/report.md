# Security: Code run by redirecting same-origin download to a javascript: URL gains user activation and bypasses CSP

| Field | Value |
|-------|-------|
| **Issue ID** | [40095196](https://issues.chromium.org/issues/40095196) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2019-05-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
When redirecting a same-origin download to a javascript: URL, the code that runs has user activation and bypasses CSP.  
  
This issue was found as part of https://bugs.chromium.org/p/chromium/issues/detail?id=966914.  
  
**VERSION**   
Chrome Version: Tested on 74.0.37

## Attachments

- [index.html](attachments/index.html) (text/plain, 211 B)
- [main.js](attachments/main.js) (text/plain, 202 B)
- [server.py](attachments/server.py) (text/plain, 725 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095196)*
