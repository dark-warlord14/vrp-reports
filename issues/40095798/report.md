# Security: Possible to leak global window object via console

| Field | Value |
|-------|-------|
| **Issue ID** | [40095798](https://issues.chromium.org/issues/40095798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-07-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
The global window object is typically accessed through a proxy that allows access checks to be performed. The actual global object is set as a hidden prototype on the proxy and isn't usually exposed to user JavaScript.  
  
The devtools console, however, will display the

## Attachments

- [site1_index.html](attachments/site1_index.html) (text/plain, 236 B)
- [site1_main.js](attachments/site1_main.js) (text/plain, 2.0 KB)
- [site2_index.html](attachments/site2_index.html) (text/plain, 168 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095798)*
