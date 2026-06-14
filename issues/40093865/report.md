# protocol property of URL including specific character doesn't return correct value

| Field | Value |
|-------|-------|
| **Issue ID** | [40093865](https://issues.chromium.org/issues/40093865) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML, Internals>Core |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | cs...@chromium.org |
| **Created** | 2019-01-26 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.4 Safari/537.36

Steps to reproduce the problem:
If an anchor element has the URL including one of U+FDD0 ~ U+FDEF, U+FFFE or U+FFFF character in the `href` attribute, the protocol propert

## Attachments

- [protocol_check_bypass.html](attachments/protocol_check_bypass.html) (text/plain, 227 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093865)*
