# Use-after-poison in blink::CrossThreadPersistentRegion::shouldTracePersistentNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40085053](https://issues.chromium.org/issues/40085053) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Mac |
| **Reporter** | th...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-08-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5170535808106496

Fuzzer: therealholden_worker
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ecde1ce8338
Crash State:
  blink::CrossThreadPersistentRegion::shouldTracePersistentNode
  b

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085053)*
