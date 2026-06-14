# Security: Two autocomplete flaws together allow sites to invisibly read credit card numbers after a single keypress

| Field | Value |
|-------|-------|
| **Issue ID** | [40093523](https://issues.chromium.org/issues/40093523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@curative.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2018-12-20 |
| **Bounty** | $3,337.00 |

## Description

**VULNERABILITY DETAILS**   
Two bugs together allow an attack that steals user card details with minimal user interaction and no indication that there was even a card entry form on the page.  
  
1. When a user hovers over an option in an autocomplete dialog, or selects it with the arrow keys, but

## Attachments

- [opentype.js](attachments/opentype.js) (text/plain, 443.4 KB)
- [demo.html](attachments/demo.html) (text/plain, 4.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093523)*
