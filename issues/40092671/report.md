# Security: Extensions can continue to temporarily execute code and access file after being uninstalled

| Field | Value |
|-------|-------|
| **Issue ID** | [40092671](https://issues.chromium.org/issues/40092671) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2018-10-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Once uninstalled, all tabs associated with an extension will be closed. While an extension is still installed, it can open a new tab pointing to about:blank from one of its pages. The new tab will have its origin set to the origin used by the chrome extension page that o

## Attachments

- [temporary_persistence_poc.zip](attachments/temporary_persistence_poc.zip) (application/octet-stream, 2.0 KB)
- [about_page.js](attachments/about_page.js) (text/plain, 356 B)
- [background.js](attachments/background.js) (text/plain, 78 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 153 B)
- [extension_page.js](attachments/extension_page.js) (text/plain, 393 B)
- [manifest.json](attachments/manifest.json) (text/plain, 374 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092671)*
