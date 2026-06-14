# Security: virglrenderer | heap-buffer-overflow on vrend_decode_set_debug_mask

| Field | Value |
|-------|-------|
| **Issue ID** | [40068966](https://issues.chromium.org/issues/40068966) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-07 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**   
1. tested on google pixelbook go, build fuzzer and run with iris gpu  
  
**Problem Description:**   
There's maybe missing boundary checking for following code that may lead to heap-buffer-overflow.  
Tested on real devices chromebook (Chromium 117.0.5928.0) w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068966)*
