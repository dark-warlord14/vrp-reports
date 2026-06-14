# Heap-buffer-overflow in blink::FindBuffer::RangeFromBufferIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40093972](https://issues.chromium.org/issues/40093972) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Editing |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ra...@chromium.org |
| **Created** | 2019-02-06 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6231480191811584

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x60500016a068
Crash State:
  blink::FindBuffer::RangeFromBufferIndex
  blink::FindBuffer::FindMat

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093972)*
