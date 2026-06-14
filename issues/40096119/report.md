# Security: Possible to temporarily spoof URL by navigating back then forward

| Field | Value |
|-------|-------|
| **Issue ID** | [40096119](https://issues.chromium.org/issues/40096119) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-08-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
When a browser-initiated navigation is pending, a page that calls history.back/history.forward can cancel the navigation, at least in the case where the page has user activation. If a page with user activation calls history.back, immediately followed by history.forward,

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.0 KB)
- [index.html](attachments/index.html) (text/plain, 401 B)
- [manifest.json](attachments/manifest.json) (text/plain, 195 B)
- [spoof.html](attachments/spoof.html) (text/plain, 720 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096119)*
