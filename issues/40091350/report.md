# Security: Speech permission request UI spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40091350](https://issues.chromium.org/issues/40091350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-05-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**   
Chrome Version: 68.0.3424.0 (Official Build) canary (64-bit)  
Operating System: macOS Sierra 10.12.6  
  
**REPRODUCTION CASE**   
1. Load the testcase  
2. Click on the button and wait  
3. Observe the permission request stays open after navigation to mixed.badssl.com

## Attachments

- [Screen Shot 2018-05-10 at 01.02.18.png](attachments/Screen Shot 2018-05-10 at 01.02.18.png) (image/png, 555.8 KB)
- [poc (16).html](attachments/poc (16).html) (text/plain, 643 B)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 295.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091350)*
