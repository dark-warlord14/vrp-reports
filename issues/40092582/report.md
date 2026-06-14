# heap buffer overflow in skia::SkTDPQueue::insert

| Field | Value |
|-------|-------|
| **Issue ID** | [40092582](https://issues.chromium.org/issues/40092582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | fs...@chromium.org |
| **Created** | 2018-09-29 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. download and unzip the release asan chromium :asan-linux-release-593799
2. Run ./chrome crash.html

What is the expected behavior?

What wen

## Attachments

- deleted (application/octet-stream, 0 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092582)*
