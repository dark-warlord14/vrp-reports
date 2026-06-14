# Security: RTL+ space, formatting, invisible characters can lead to URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40090883](https://issues.chromium.org/issues/40090883) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network, UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2018-03-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
Chrome address bar using RTL-IDNs-TLD  
  
**VERSION**   
Chrome65 on ALL (Windows/macOS/iOS/Android)  
  
**REPRODUCTION CASE**   
  
1.Access http://xisigr.com/test/spoof/chrome/RLT-IDN-TLD.html.  
2.Click on the "gmail.com" button.  
3.Address bar says www.gmail.com -

## Attachments

- [RLT-IDN-TLD.html](attachments/RLT-IDN-TLD.html) (text/plain, 339 B)
- [chrome-ios.png](attachments/chrome-ios.png) (image/png, 81.5 KB)
- [chrome-incognito-ios.png](attachments/chrome-incognito-ios.png) (image/png, 80.7 KB)
- [IMG_3236.png](attachments/IMG_3236.png) (image/png, 183.9 KB)
- [chrome-ios-1.png](attachments/chrome-ios-1.png) (image/png, 198.0 KB)
- [chrome-ios-2.png](attachments/chrome-ios-2.png) (image/png, 176.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090883)*
