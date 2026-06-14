# Cross-origin stylesheet content is readable using SW

| Field | Value |
|-------|-------|
| **Issue ID** | [40091542](https://issues.chromium.org/issues/40091542) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>ServiceWorker |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/steal_css.html
2. Reload

What is the expected behavior?
Throws SecurityError on alert (due to access

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091542)*
