# Security: Possible to spoof the contents of the omnibox to display any http/https URL, some extension URLs and some internal URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40095159](https://issues.chromium.org/issues/40095159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2019-05-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**   
By redirecting a same-origin download and then performing a specific location assignment during the beforeunload event, it's possible to update the omnibox to display any desired http/https URL, some extension URLs and some internal URLs. One caveat is that the omnibox w

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 153 B)
- [iframe-main.js](attachments/iframe-main.js) (text/plain, 109 B)
- [index.html](attachments/index.html) (text/plain, 493 B)
- [main.js](attachments/main.js) (text/plain, 1.2 KB)
- [server.py](attachments/server.py) (text/plain, 2.4 KB)
- [iframe.html](attachments/iframe_53105092.html) (text/plain, 153 B)
- [iframe-main.js](attachments/iframe-main_53105093.js) (text/plain, 109 B)
- [index.html](attachments/index_53105094.html) (text/plain, 3.1 KB)
- [main.js](attachments/main_53105095.js) (text/plain, 2.1 KB)
- [server.py](attachments/server_53105096.py) (text/plain, 927 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095159)*
