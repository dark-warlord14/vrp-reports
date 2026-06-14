# Security:IDN url spoofing using U+4e00

| Field | Value |
|-------|-------|
| **Issue ID** | [40091930](https://issues.chromium.org/issues/40091930) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zx...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-07-14 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
http://xn--ipaddress-w75n.com/

What is the expected behavior?

What went wrong?
As you disallow U+30FC(ー), but U+4e00(一) still avail

## Attachments

- [ip.jpg](attachments/ip.jpg) (image/jpeg, 3.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091930)*
