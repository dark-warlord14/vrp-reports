# libANGLE heap-buffer-overflow triggered by WebGL2 on Windows 10

| Field | Value |
|-------|-------|
| **Issue ID** | [40094331](https://issues.chromium.org/issues/40094331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36

Steps to reproduce the problem:
To reproduce the problem, load the attached HTML with Chromium ASAN build on Windows 10.

ASAN log:
===================================

## Attachments

- [test3-final.html](attachments/test3-final.html) (text/plain, 1.5 KB)
- [test2-2.html](attachments/test2-2.html) (text/plain, 148.4 KB)
- [gpu.html](attachments/gpu.html) (text/plain, 121.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094331)*
