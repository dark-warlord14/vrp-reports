# Code review: ReadBits may return uninitialized value due to unchecked return status.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093992](https://issues.chromium.org/issues/40093992) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@microsoft.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134

Steps to reproduce the problem:
Found through code review, no repro steps provided. Instead there's an analysis and a proposed fix.

What is the expected

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093992)*
