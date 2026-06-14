# Security: Bypass the CSP when popup with "javascript:"-URL 

| Field | Value |
|-------|-------|
| **Issue ID** | [40095955](https://issues.chromium.org/issues/40095955) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2019-08-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
When set the CSP as  <meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'"> , the eval function will also work in `javascript:` URL.Just like the https://crbug.com/chromium/582387.  
  
**VERSION**   
Chrome Version: [76.0.3809.100] + [stable]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095955)*
