# SameSite Lax bypass with multiple-nested scenarios

| Field | Value |
|-------|-------|
| **Issue ID** | [40091123](https://issues.chromium.org/issues/40091123) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DOM, Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2018-04-17 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/SameSite.php (this sets SameSite Strict and Lax)
2. Go to https://test.shhnjk.com/sandbox.php?url=https

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091123)*
