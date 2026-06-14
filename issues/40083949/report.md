# Security: Bypassing web_accessible_resources protections

| Field | Value |
|-------|-------|
| **Issue ID** | [40083949](https://issues.chromium.org/issues/40083949) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Mac |
| **Reporter** | ja...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-03-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
If a web page tries to open a Chrome extension file, without have been authorized, Chrome will throw a security error exception:  
  
Denying load of chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo/RestClient.html. Resources must be listed in the web_accessible_re

## Attachments

- [chrome-extension.html](attachments/chrome-extension.html) (text/plain, 1.4 KB)
- [chrome_installed_extensions.html](attachments/chrome_installed_extensions.html) (text/plain, 1.4 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083949)*
