# Integer overflow in libANGLE that results in memory corruption in GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [40094318](https://issues.chromium.org/issues/40094318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2019-03-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36

Steps to reproduce the problem:
I reproduce the issue by launching the attached PoC with ASAN build of Chromium Version 74.0.3726.0 (Developer Build) (64-bit), on

## Attachments

- deleted (application/octet-stream, 0 B)
- [gpu.html](attachments/gpu.html) (text/plain, 121.2 KB)
- [main.cpp](attachments/main.cpp) (text/plain, 3.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094318)*
