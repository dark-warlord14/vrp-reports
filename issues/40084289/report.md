# Heap-use-after-free in v8::Isolate::VisitHandlesWithClassIds

| Field | Value |
|-------|-------|
| **Issue ID** | [40084289](https://issues.chromium.org/issues/40084289) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2016-05-11 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4623653819383808

Fuzzer: therealholden_worker
Job Type: windows_asan_content_shell
Platform Id: windows

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x1c80b204
Crash State:
  v8::Isolate::VisitHandlesWithClassIds
  blink::V8GC

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084289)*
