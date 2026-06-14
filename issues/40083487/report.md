# Use-of-uninitialized-value in S32A_Opaque_BlitRow32_SSE4

| Field | Value |
|-------|-------|
| **Issue ID** | [40083487](https://issues.chromium.org/issues/40083487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2016-01-04 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6133678582792192

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  S32A_Opaque_BlitRow32_SSE4
  SkARGB32_Shader_Blitter::blitAntiH
  SkRec

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083487)*
