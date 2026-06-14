# Security: `Android` Top-level redirect from cross-origin iframe by setting `Content-Security-Policy: sandbox allow-top-navigation` Bypass of Issue 1251790

| Field | Value |
|-------|-------|
| **Issue ID** | [41493458](https://issues.chromium.org/issues/41493458) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PopupBlocker |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | lb...@google.com |
| **Created** | 2024-01-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
======================  
After Fixing https://crbug.com/chromium/1251790 , i've found that  this bug come back in Chrome for Android, Regression of https://crbug.com/chromium/1251790 .  
  
Top-level redirect possible from cross-origin iframe without user-interaction by

## Attachments

- [csp-par.html](attachments/csp-par.html) (text/plain, 439 B)
- [poc-canary-csp_22012024_155106_7501.mp4](attachments/poc-canary-csp_22012024_155106_7501.mp4) (video/mp4, 2.8 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493458)*
