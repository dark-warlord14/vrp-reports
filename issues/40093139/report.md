# Security: Possible to retrieve cross-origin image data from canvas

| Field | Value |
|-------|-------|
| **Issue ID** | [40093139](https://issues.chromium.org/issues/40093139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-11-20 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**   
The canvas element allows cross-origin images to be drawn within it, but will prevent the image data from being read back out. Internally, the canvas caches the list of URLs it's seen before and whether or not they tainted the canvas. That way, when an image is drawn, th

## Attachments

- [index.html](attachments/index.html) (text/plain, 266 B)
- [local.png](attachments/local.png) (image/png, 156 B)
- [main.js](attachments/main.js) (text/plain, 1.6 KB)
- [service_worker.js](attachments/service_worker.js) (text/plain, 343 B)
- [index.html](attachments/index_53093312.html) (text/plain, 266 B)
- [local.png](attachments/local_53093313.png) (image/png, 156 B)
- [main.js](attachments/main_53093314.js) (text/plain, 1.6 KB)
- [service_worker.js](attachments/service_worker_53093315.js) (text/plain, 341 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093139)*
