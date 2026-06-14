# CSP bypass with blob URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40090110](https://issues.chromium.org/issues/40090110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-01-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/blobCSP.html

What is the expected behavior?
Script is blocked by CSP "script-src 'nonce-test'"

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090110)*
