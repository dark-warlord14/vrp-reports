# Use-after-poison in blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,

| Field | Value |
|-------|-------|
| **Issue ID** | [40084711](https://issues.chromium.org/issues/40084711) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Workers |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | th...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-06-28 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5286150310985728

Fuzzer: therealholden_worker
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x574e97d0
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridg

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084711)*
