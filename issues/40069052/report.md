# Security: virglrenderer | heap-buffer-overflow on vrend_set_constants

| Field | Value |
|-------|-------|
| **Issue ID** | [40069052](https://issues.chromium.org/issues/40069052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-08 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**   
Steps to reproduce the problem:  
1. tested on google pixelbook go, build fuzzer and run with iris gpu  
  
**Problem Description:**   
There's maybe missing boundary checking for following code that may lead to heap-buffer-overflow.  
Tested on real devices ch

## Attachments

- [virgl-sub-issue-371.png](attachments/virgl-sub-issue-371.png) (image/png, 94.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069052)*
