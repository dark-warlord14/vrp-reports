# Security: URL bar spoofing via download redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40095527](https://issues.chromium.org/issues/40095527) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2019-06-28 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**   
Chrome Version: 77.0.3836.3 canary  
Operating System: Android  
  
**REPRODUCTION CASE**   
1. Go to https://shhnjk.azurewebsites.net/download_redirector.php?url=https://www.google.com:1234  
  
Observed Results: Observe that google.com:1234 displayed but the content area still shows

## Attachments

- [976549F7-B41B-4D28-B841-462FC3D5D14C.MP4](attachments/976549F7-B41B-4D28-B841-462FC3D5D14C.MP4) (video/mp4, 1.4 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095527)*
