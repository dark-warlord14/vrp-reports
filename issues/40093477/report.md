# Security: Origin header-based CSRF protection bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40093477](https://issues.chromium.org/issues/40093477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Submission, Blink>SecurityFeature, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | lu...@chromium.org |
| **Created** | 2018-12-16 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
CSRF protection bypass with user input is possible via a bug where refreshing a failed cross-origin form submission changes the request origin upon resubmission.  
  
**VERSION**   
Chrome Version: 71.0.3578.98 (Official Build) (64-bit)  
Operating System: Mac OS Sierra

## Attachments

- [chrome origin bypass devtools.mp4](attachments/chrome origin bypass devtools.mp4) (video/mp4, 147.3 KB)
- [csrf bypass no devtools.mp4](attachments/csrf bypass no devtools.mp4) (video/mp4, 346.2 KB)
- [csrf-bypass-simple.html](attachments/csrf-bypass-simple.html) (text/plain, 649 B)
- [csrf-bypass-simple.html](attachments/csrf-bypass-simple_53014739.html) (text/plain, 666 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093477)*
