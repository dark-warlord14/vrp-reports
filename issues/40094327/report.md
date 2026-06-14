# libANGLE use-after-free (gl::State::syncTextures) triggered through WebGL2 in the GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [40094327](https://issues.chromium.org/issues/40094327) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-19 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36

Steps to reproduce the problem:
I launched the HTML with the ASAN build of the latest Chromium on latest Windows 10, and got the following ASAN log:

==================

## Attachments

- [x.html](attachments/x.html) (text/plain, 1.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094327)*
