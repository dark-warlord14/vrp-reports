# Security: PWA dialog selects an install button by default Bypassing Google Security Measures in Chrome UI 

| Field | Value |
|-------|-------|
| **Issue ID** | [40064335](https://issues.chromium.org/issues/40064335) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-05-02 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**   
----------------------  
The PWA dialog has the "install" button focused by default. This presents an issue as this makes the dialog key-jackable,Bypassing Google Security measures in Chrome UI sensitive area `installing PWA` which lead to (user information disclosure wi

## Attachments

- [pwa-app-install-accept.js](attachments/pwa-app-install-accept.js) (text/plain, 2.0 KB)
- [a2hs-poc.html](attachments/a2hs-poc.html) (text/plain, 1.1 KB)
- [pwa-app.webmanifest](attachments/pwa-app.webmanifest) (application/octet-stream, 622 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 731 B)
- [style.css](attachments/style.css) (text/plain, 868 B)
- [Canary-WIN 2023-05-02 22-45-02-887.mp4](attachments/Canary-WIN 2023-05-02 22-45-02-887.mp4) (video/mp4, 2.0 MB)
- [Stable-WIN  2023-05-02 22-36-43-208.mp4](attachments/Stable-WIN  2023-05-02 22-36-43-208.mp4) (video/mp4, 2.5 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064335)*
