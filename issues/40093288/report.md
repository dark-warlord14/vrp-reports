# Security: XSS Auditor & History Web API can be chained to create a cross-origin covert channel

| Field | Value |
|-------|-------|
| **Issue ID** | [40093288](https://issues.chromium.org/issues/40093288) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>XSSAuditor, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | th...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-12-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
A cross-origin covert channel that can be used to leak information from a victim origin can be created by chaining the blocking mode of XSS Auditor with the History Web API.  
  
Before we elaborate on the specifics of this attack, we'd like to draw attention to the r

## Attachments

- [attacker.html](attachments/attacker.html) (text/plain, 1.2 KB)
- [victim.html](attachments/victim.html) (text/plain, 127 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093288)*
