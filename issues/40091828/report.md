# Security: Confused deputy attack against Chrome Android application might lead to internal storage file disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40091828](https://issues.chromium.org/issues/40091828) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | an...@truel.it |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-07-01 |
| **Bounty** | $1,000.00 |

## Description

Tested on:
---------

- Android 5.1.1 Chrome 56.0.292487
- Android 8.0.0 Chrome 67.0.3396.87

Vulnerability Description
-------------------------

Due to the lack of validation on the file:// URI taken from the result Intent of a GET_CONTENT action, the Chrome Android application can be tri

## Attachments

- [chrome1.png](attachments/chrome1.png) (image/png, 61.2 KB)
- [chrome2.png](attachments/chrome2.png) (image/png, 124.9 KB)
- [chrome3.png](attachments/chrome3.png) (image/png, 61.4 KB)
- [chrome4.png](attachments/chrome4.png) (image/png, 359.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091828)*
