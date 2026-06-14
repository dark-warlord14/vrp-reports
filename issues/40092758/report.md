# Security: IDN URL Spoofing with U+02ec

| Field | Value |
|-------|-------|
| **Issue ID** | [40092758](https://issues.chromium.org/issues/40092758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Internationalization |
| **Platforms** | Windows |
| **Reporter** | ev...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-10-18 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36

Steps to reproduce the problem:
### SPOOF CASE

(\u02ec) "ˬ" looks like an ".", it's not easy to catch the spoofing.

Real: https://accountsˬgoogle.com --- Spoof domain: h

## Attachments

- [ee082f5e46ac662229b55cb8770eea8.png](attachments/ee082f5e46ac662229b55cb8770eea8.png) (image/png, 2.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092758)*
