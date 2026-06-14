# Automation API leaks tab URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40085155](https://issues.chromium.org/issues/40085155) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-08-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36

Steps to reproduce the problem:
1. Open a dev build; the Automation API is not present in stable.
2. Open a few tabs with secret URLs.
3. Unpack and load the attached extension.

## Attachments

- [urlleak_extension.zip](attachments/urlleak_extension.zip) (application/octet-stream, 886 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085155)*
