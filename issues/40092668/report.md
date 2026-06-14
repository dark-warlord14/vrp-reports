# Security: window.location update methods don't always restrict access to local resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40092668](https://issues.chromium.org/issues/40092668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2018-10-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
Two of the window.location update methods (window.location.replace() and window.location.href = ...) don't always restrict access to local resources. This allows an extension to load an iframe containing a local file resource, even when "Allow access to file URLs" is dis

## Attachments

- [window_location_poc.zip](attachments/window_location_poc.zip) (application/octet-stream, 1.4 KB)
- [background.js](attachments/background.js) (text/plain, 67 B)
- [manifest.json](attachments/manifest.json) (text/plain, 314 B)
- [poc.html](attachments/poc.html) (text/plain, 273 B)
- [poc.js](attachments/poc.js) (text/plain, 308 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092668)*
