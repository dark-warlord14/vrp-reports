# XSS from chrome-untrusted://new-tab-page URL parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40057777](https://issues.chromium.org/issues/40057777) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2021-10-31 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36

Steps to reproduce the problem:
Direct URL navigation:
chrome-untrusted://new-tab-page/custom_background_image?url=https://a.a&size=%3C/style%3E%3Cscript%3Ealert(1)%3C/s

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057777)*
