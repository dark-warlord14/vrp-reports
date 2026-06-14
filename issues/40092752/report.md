# Security: IDN URL Spoofing with Georgian Letter Jil "ძ"

| Field | Value |
|-------|-------|
| **Issue ID** | [40092752](https://issues.chromium.org/issues/40092752) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2018-10-18 |
| **Bounty** | $500.00 |

## Description

**VERSION**   
Chrome Version: 72.0.3582.0 (Official Build) canary (64-bit)  
Operating System: Mac  
  
**REPRODUCTION CASE**   
Cyrillic letter U+10EB (ძ) looks very similar to the Latin letter d.  
  
Visit: http://xn--4000-pfr.com/  
  
Real domain 4000.com (listed in top-100k domain)

## Attachments

- [Screen Shot 2018-10-18 at 02.16.16.png](attachments/Screen Shot 2018-10-18 at 02.16.16.png) (image/png, 17.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092752)*
