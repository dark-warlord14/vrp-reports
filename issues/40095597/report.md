# Security: Memory corruption in BrowserList::NotifyBrowserNoLongerActive(Browser*) ()

| Field | Value |
|-------|-------|
| **Issue ID** | [40095597](https://issues.chromium.org/issues/40095597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-07-03 |
| **Bounty** | $500.00 |

## Description

Chrome Version: Chromium 77.0.3843.0 (Developer Build) (64-bit)  
Operating System: All  
  
  
**REPRODUCTION CASE**   
1. Open http://permission.site  
2. Open again on another tab http://permission.site  
3. On the first tab, click on “Share screen” and switch Chrome Tab and try to share the seco

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.3 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095597)*
