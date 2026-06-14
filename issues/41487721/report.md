# Security: Spoofing request source of Apple mobile configuration profile downloads by UI impersonation

| Field | Value |
|-------|-------|
| **Issue ID** | [41487721](https://issues.chromium.org/issues/41487721) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2024-01-02 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
When receiving a response with a MIME type of "application/x-apple-aspen-config", Chromium for iOS shows a confirmation dialog to ask whether to download the iOS configuration profile, and after that, opens SFSafariViewController.  
https://source.chromium.org/chromium/c

## Attachments

- [chromium-ios-mobileconfig-download-ui-spoofing.gif](attachments/chromium-ios-mobileconfig-download-ui-spoofing.gif) (image/gif, 423.0 KB)
- [current.png](attachments/current.png) (image/png, 522.1 KB)
- [proposed-fix.png](attachments/proposed-fix.png) (image/png, 519.9 KB)
- [LongURL.png](attachments/LongURL.png) (image/png, 1.8 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487721)*
