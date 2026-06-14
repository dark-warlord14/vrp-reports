# Security: heap-buffer-overflow in gpu::gles2::StrictIdHandler::FreeIds

| Field | Value |
|-------|-------|
| **Issue ID** | [40091547](https://issues.chromium.org/issues/40091547) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | kb...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $3,000.00 |

## Description

I have tested this on the stable asan linux build (asan-linux-stable-67.0.3396.62).

ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000227832 at pc 0x5642e80f6294 bp 0x7ffec465d810 sp 0x7ffec465d808
WRITE of size 1 at 0x602000227832 thread T0 (chrome)
    #0 0x5642e80f6293 in gpu:

## Attachments

- [gpu_freeids.html](attachments/gpu_freeids.html) (text/plain, 2.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 14.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091547)*
