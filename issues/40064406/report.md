# Security: On Chrome OS, any webpage is able to interface with the Chrome Goodies extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40064406](https://issues.chromium.org/issues/40064406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
By putting `chrome-extension://kddnkjkcjddckihglkfcickdhbmaodcn/broker.html` inside an iframe, any webpage is able to access `chrome.echoPrivate.getUserConsent` or `chrome.echoPrivate.getOfferInfo` by posting messages to that iframe. Neither one of these requires any use

## Attachments

- [index.html](attachments/index.html) (text/plain, 2.8 KB)
- [echo.js](attachments/echo.js) (text/plain, 2.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064406)*
