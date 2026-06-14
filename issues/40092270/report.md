# Detecting if the XSS Auditor was triggered by changing the hash

| Field | Value |
|-------|-------|
| **Issue ID** | [40092270](https://issues.chromium.org/issues/40092270) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-08-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
If a page is redirected to itself and has a hash set, no navigation is performed, instead, only the hash is changed.  
  
This behavior is different when the page is being blocked by the XSS Auditor. In this case, if the page is redirected to itself and has a hash set, a

## Attachments

- [server1-hash.html](attachments/server1-hash.html) (text/plain, 816 B)
- [server2-auditor.html](attachments/server2-auditor.html) (text/plain, 129 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092270)*
