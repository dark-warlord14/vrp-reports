# Self-XSS via modal, window.open, and delayed navigation

| Field | Value |
|-------|-------|
| **Issue ID** | [40091605](https://issues.chromium.org/issues/40091605) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2018-06-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
By combining three vulnerabilities it's possible to trick an user into executing javascript in an arbitrary origin.  
  
The following vulnerabilities are being chained in this attack:  
1. It's possible to open an empty new tab with an arbitrary scheme and authority tha

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 1.0 MB)
- [device-2018-09-26-104956.mp4](attachments/device-2018-09-26-104956.mp4) (video/mp4, 12.2 MB)
- [device-2018-09-26-125500.mp4](attachments/device-2018-09-26-125500.mp4) (video/mp4, 8.2 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091605)*
