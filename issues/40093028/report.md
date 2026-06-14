# Security: Sites can open extension pages using WindowClient.navigate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093028](https://issues.chromium.org/issues/40093028) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker, Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-11-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
Normally, sites are prevented from being able to open extension pages. While this restriction applies to methods like window.open() or window.location.href = ..., it doesn't apply when a site triggers a navigation event using WindowClient.navigate(). In that case, the pa

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 227 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 578 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093028)*
