# Security: Possible to override browser-initiated navigation using WindowClient.navigate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093998](https://issues.chromium.org/issues/40093998) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
A service worker can call the WindowClient.navigate method to direct a page under its control to a specific URL. Unlike the usual methods of redirecting (e.g. window.location.href = ..., window.location.replace(...), etc), which don't work once the beforeunload event has

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 478 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 521 B)
- [index.html](attachments/index_53099748.html) (text/plain, 134 B)
- [main.js](attachments/main_53099749.js) (text/plain, 413 B)
- [service_worker.js](attachments/service_worker_53099750.js) (text/plain, 675 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093998)*
