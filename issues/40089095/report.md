# CSP inheritance to cross-origin navigated data URL allows cross-origin info leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40089095](https://issues.chromium.org/issues/40089095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Privacy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-09-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/simple.html
2. data URL navigated by cross-origin inherited parent's CSP

What is the expected b

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089095)*
