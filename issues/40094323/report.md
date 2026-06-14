# use-after-free in libANGLE triggered by WebGL2 on Windows 10

| Field | Value |
|-------|-------|
| **Issue ID** | [40094323](https://issues.chromium.org/issues/40094323) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36

Steps to reproduce the problem:
Simply launch the attached PoC with the ASAN build of Chromium on Windows 10 (d3d11 supported).

======================================

## Attachments

- [final.html](attachments/final.html) (text/plain, 1.3 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094323)*
