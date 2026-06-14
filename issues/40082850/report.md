# Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel;DOMWrapperMap.h:148:20

| Field | Value |
|-------|-------|
| **Issue ID** | [40082850](https://issues.chromium.org/issues/40082850) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Bindings |
| **Platforms** | Linux |
| **Reporter** | th...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2015-09-13 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5492489312534528

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f0909ea8150
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel
  DOMWr

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082850)*
