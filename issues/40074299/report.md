# Security: Bypassing Chrome's File URI Restrictions with View-Source in Extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40074299](https://issues.chromium.org/issues/40074299) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-10-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
In the latest version of Chrome, navigation to the file URI is disabled when "Allow File Access" is turned off. This change addresses most file access vulnerabilities in extensions and aims to prevent future exploitations. However, I've discovered a method where this res

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.0 MB)
- [background.js](attachments/background.js) (text/plain, 87 B)
- [manifest.json](attachments/manifest.json) (text/plain, 180 B)
- [error.png](attachments/error.png) (image/png, 24.1 KB)
- [changes-to-file-scheme.png](attachments/changes-to-file-scheme.png) (image/png, 80.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074299)*
