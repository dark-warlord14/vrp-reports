# UAF in gpu::GpuChannelHost

| Field | Value |
|-------|-------|
| **Issue ID** | [41492634](https://issues.chromium.org/issues/41492634) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2024-01-18 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**   
tested chrome version:  
Chromium 122.0.6238.2   
Chromium 122.0.6257.0  
  
repro steps:  
1 git apply sleep.patch  
2 build chrome with asan:  
    args.gn is as follows:  
    is_asan = true  
    is_debug = false  
    enable_nacl = false  
    treat_warnin

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 236 B)
- [sleep.patch](attachments/sleep.patch) (text/plain, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 33.2 KB)
- [asan-new.log](attachments/asan-new.log) (text/plain, 34.4 KB)
- [asan-old.log](attachments/asan-old.log) (text/plain, 22.7 KB)
- [asan-1519655.txt](attachments/asan-1519655.txt) (text/plain, 25.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41492634)*
