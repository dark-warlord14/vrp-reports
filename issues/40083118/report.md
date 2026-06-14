# Use-after-poison in blink::WorkerWebSocketChannel::Bridge::traceImpl<blink::InlinedGlobalMarkingVisi

| Field | Value |
|-------|-------|
| **Issue ID** | [40083118](https://issues.chromium.org/issues/40083118) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Network>WebSockets, Blink>Workers |
| **Platforms** | Windows |
| **Reporter** | th...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2015-11-02 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5934574129905664

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Use-after-poison READ 4
Crash Address: 0x0c226e48
Crash State:
  blink::WorkerWebSocketChannel::Bridge::traceImpl<blink::Inlin

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083118)*
