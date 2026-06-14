# Security: libglesv2 heap-buffer-overflow in VertexBuffer11::storeVertexAttributes

| Field | Value |
|-------|-------|
| **Issue ID** | [40091358](https://issues.chromium.org/issues/40091358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2018-05-11 |
| **Bounty** | $1,000.00 |

## Description

I have tested this on the Chrome Canary 68.0.3426.0 and asan-win32-release_x64-554177.

4:041> r
rax=000001777ff60000 rbx=000001770f196d00 rcx=fffffffff4cbac41
rdx=ffffffff8dc7cc40 rsi=000001770dc92000 rdi=00000177800153c0
rip=00007fff91932377 rsp=00000071fcbfd628 rbp=0000000000000000
 r8=0000

## Attachments

- [vertex.html](attachments/vertex.html) (text/plain, 3.2 KB)
- [vertex_log.txt](attachments/vertex_log.txt) (text/plain, 9.4 KB)
- [gpu.html](attachments/gpu.html) (text/plain, 180.5 KB)
- [WindowsASANGPUReport.txt](attachments/WindowsASANGPUReport.txt) (text/plain, 15.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091358)*
