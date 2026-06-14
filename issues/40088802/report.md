# Security: document.baseURI contains not-encoded representation of URI and may lead to DOM based XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40088802](https://issues.chromium.org/issues/40088802) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DOM, Blink>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-08-24 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
Chrome is rendering unencoded version of URI when using document.write(document.baseURI); This is not expected behavior and Firefox renders encoded characters in that case.

Please have a look into it.

VERSION
Chrome Version: 60.0.3112.101 (Official Build) (64-bit)
Oper

## Attachments

- [test.html](attachments/test.html) (text/plain, 110 B)
- [reproduced.png](attachments/reproduced.png) (image/png, 21.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088802)*
