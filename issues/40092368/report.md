# Security: ANGLE TextureStorage11::setData Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40092368](https://issues.chromium.org/issues/40092368) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2018-09-05 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on Chrome Stable version 69.0.3497.81.
There is a crash which occurs on an invalid reference to pixelData in TextureStorage11::setData.

This is reproducible on any GPU driver, I have attached a testcase with Nvidia.

3:034> r
rax=0000022684109300 rbx=000082239303ed50 rcx=00

## Attachments

- [texstor11.html](attachments/texstor11.html) (text/plain, 2.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092368)*
