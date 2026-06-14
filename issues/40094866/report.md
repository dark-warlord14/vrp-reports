# Security: Mixed content state reset when navigating back

| Field | Value |
|-------|-------|
| **Issue ID** | [40094866](https://issues.chromium.org/issues/40094866) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>PageSecurityState |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2019-05-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
When a https site includes a http asset (e.g. an image) or targets a http site with a form, the lock icon shown in the omnibox will change to indicate that the site is including mixed content.  
  
However, if a site uses history.pushState(), adds mixed content and then

## Attachments

- [index.html](attachments/index.html) (text/plain, 136 B)
- [main.js](attachments/main.js) (text/plain, 289 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094866)*
