# Security DCHECK failure: RotateTransformOperation::IsMatchingOperationType(transform.GetType()) in rotate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093917](https://issues.chromium.org/issues/40093917) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ke...@chromium.org |
| **Created** | 2019-02-01 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5115262500208640

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  RotateTransformOperation::IsMatchingOperationType(transform.GetType()) in rotate

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093917)*
