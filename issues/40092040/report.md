# Security: Loading mixed content without insecure warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40092040](https://issues.chromium.org/issues/40092040) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>Video, Internals>Media>Network, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2018-07-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
The site seems secure but is loading mixed / insecure content.  
  
The first time loading a page, the page is flagged unsecure. When a page refresh happens the page is flagged secure.  
To get the secure flagged page a refresh can be done through the meta refresh or a J

## Attachments

- [mixedmp4.html](attachments/mixedmp4.html) (text/plain, 350 B)
- [mixedjs.html](attachments/mixedjs.html) (text/plain, 235 B)
- [mixedpng.html](attachments/mixedpng.html) (text/plain, 283 B)
- [2018-07-31 12-11-04.mp4](attachments/2018-07-31 12-11-04.mp4) (video/mp4, 3.9 MB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092040)*
