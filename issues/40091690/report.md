# SameSite cookies leakage via child browsing context

| Field | Value |
|-------|-------|
| **Issue ID** | [40091690](https://issues.chromium.org/issues/40091690) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2018-06-18 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version       : 66.0.3359.181 (Official Build) (64-bit)  
**URLs (if applicable) :**  http://cm2.pw/xss?xss=%3Ciframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/httpleaks/child.html%27%3E%3C/iframe%3E  
  
**Other browsers tested:**   
    Firefox: OK (version: 61.0b14 (64-b

## Attachments

- [child.png](attachments/child.png) (image/png, 59.0 KB)
- [child2.html](attachments/child2.html) (text/plain, 913 B)
- [cookies.php](attachments/cookies.php) (text/plain, 976 B)
- [SameSite-cookies.png](attachments/SameSite-cookies.png) (image/png, 146.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091690)*
