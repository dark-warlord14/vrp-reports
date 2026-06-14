# Undefined behavior in ipcz::DriverMemory::Clone()

| Field | Value |
|-------|-------|
| **Issue ID** | [41494539](https://issues.chromium.org/issues/41494539) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core |
| **Platforms** | Fuchsia, Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2024-01-25 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**   
Will attach detail soon  
  
**Problem Description:**   
browser UAF  
  
**Additional Comments:**   
  
  
**Chrome version: ** 122.0.6260.0 **Channel: ** Canary  
  
**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.8 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 31.0 KB)
- [fuzz_6f88f0111c445a39a0c2a67423e9b745.html](attachments/fuzz_6f88f0111c445a39a0c2a67423e9b745.html) (text/plain, 421.4 KB)
- [fuzz_000279ad0281af80064383a321534c3b.html](attachments/fuzz_000279ad0281af80064383a321534c3b.html) (text/plain, 361.3 KB)
- [fuzz_642aa74350c70182b18b050bc41f099c.html](attachments/fuzz_642aa74350c70182b18b050bc41f099c.html) (text/plain, 381.3 KB)
- [fuzz_793baf97d768b7c6df7256c41f9f28a7.html](attachments/fuzz_793baf97d768b7c6df7256c41f9f28a7.html) (text/plain, 348.0 KB)
- [fuzz_a9081ae57dacc1f850e68c56cec5c2bd.html](attachments/fuzz_a9081ae57dacc1f850e68c56cec5c2bd.html) (text/plain, 345.7 KB)
- [fuzz_e83c811473b6c25c8041ba18faf1bbbd.html](attachments/fuzz_e83c811473b6c25c8041ba18faf1bbbd.html) (text/plain, 435.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494539)*
