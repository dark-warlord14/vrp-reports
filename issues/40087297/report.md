# Security: <link rel='prerender'> causes same-site cookies to be sent along with cross-site requests

| Field | Value |
|-------|-------|
| **Issue ID** | [40087297](https://issues.chromium.org/issues/40087297) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Preload |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ge...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-04-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**   
If an HTML-page contains a <link rel="prerender">-tag with the href pointing to a page on another domain than the domain hosting this HTML-page, then upon visiting this HTML-page the browser will send along all strict and lax same-site cookies with this cross-site reques

## Attachments

- [prerender.html](attachments/prerender.html) (text/plain, 2.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087297)*
