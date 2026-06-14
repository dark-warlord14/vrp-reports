# Use-of-uninitialized-value in avx::store_NUMBER

| Field | Value |
|-------|-------|
| **Issue ID** | [40094105](https://issues.chromium.org/issues/40094105) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mt...@google.com |
| **Created** | 2019-02-21 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5968280726667264

Fuzzer: jesse_avalanche
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  avx::store_NUMBER
  avx::start_pipeline
  SkMaskFilterBase::filterPath
  
Sanitizer: m

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094105)*
