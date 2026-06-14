# blob:chrome-extension:-URLs should not bypass CSP in extension pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40088758](https://issues.chromium.org/issues/40088758) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2017-08-18 |
| **Bounty** | $1,000.00 |

## Description

The default Content Security Policy in Chrome extensions is designed to block remote scripts.
Extensions can opt in to allowing remote scripts, but only with a custom content_security_policy (https://developer.chrome.com/extensions/contentSecurityPolicy#relaxing). This makes it easier to audit the

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 155 B)
- [background.js](attachments/background.js) (text/plain, 590 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088758)*
