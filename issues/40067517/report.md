# Initiator origin not propagated on cross-profile navigations

| Field | Value |
|-------|-------|
| **Issue ID** | [40067517](https://issues.chromium.org/issues/40067517) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>Permissions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2023-07-17 |
| **Bounty** | $500.00 |

## Description

Normally it should open a link like ms-calculator:: , tel:// , or whatsapp: and different link should show Extension URL Access.  
  
After open link in new tab/window/incognito URL permission is show, but if link open link as different profile URL permission not show.  
   
**VERSION**   
  
Chrome

## Attachments

- [open.html](attachments/open.html) (text/plain, 205 B)
- [POC.mp4](attachments/POC.mp4) (video/mp4, 520.2 KB)
- [POC_Update.mp4](attachments/POC_Update.mp4) (video/mp4, 402.8 KB)
- [POC.mp4](attachments/POC_53017933.mp4) (video/mp4, 377.1 KB)
- [pdf-calc.html](attachments/pdf-calc.html) (text/plain, 865 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067517)*
