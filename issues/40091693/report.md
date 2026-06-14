# XSS by hosting JS and JSON looking file

| Field | Value |
|-------|-------|
| **Issue ID** | [40091693](https://issues.chromium.org/issues/40091693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | go...@chromium.org |
| **Created** | 2018-06-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/pay_handler.html
2. Hold Enter key for 3 seconds
3. Observe that attacker gets XSS capability in test

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091693)*
