# Security: URL in Omnibox doesn't always match page content

| Field | Value |
|-------|-------|
| **Issue ID** | [40092807](https://issues.chromium.org/issues/40092807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2018-10-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
When a redirect response is received for a request, the browser will follow the redirect. If the redirect location is given as "javascript:", however, the navigation will be cancelled. If this is done at the page level, the URL in the Omnibox will be updated (to whatever

## Attachments

- [background.js](attachments/background.js) (text/plain, 896 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 85 B)
- [manifest.json](attachments/manifest.json) (text/plain, 415 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092807)*
