# Security: IDN URL Spoofing with Georgian Letter Vin

| Field | Value |
|-------|-------|
| **Issue ID** | [40091565](https://issues.chromium.org/issues/40091565) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-06-04 |
| **Bounty** | $500.00 |

## Description

**VERSION**   
Chrome Version: Version 69.0.3449.0 (Official Build) canary (64-bit)  
Operating System: Mac  
  
**REPRODUCTION CASE**   
-(U+10D5) "ვ" looks like an "3" and it's not easy to catch the spoofing.  
  
Real domain: http://www.163.com/  
  
Spoof domain: http://xn--16-pik.com/

## Attachments

- [Screen Shot 2018-06-11 at 20.32.58.png](attachments/Screen Shot 2018-06-11 at 20.32.58.png) (image/png, 26.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091565)*
