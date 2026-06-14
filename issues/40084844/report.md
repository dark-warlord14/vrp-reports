# Heap-use-after-free in blink::PaintController::commitNewDisplayItems

| Field | Value |
|-------|-------|
| **Issue ID** | [40084844](https://issues.chromium.org/issues/40084844) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2016-07-14 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5841673557114880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0xcf18c780
Crash State:
  blink::PaintController::commitNewDisplayItems
  blink:

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084844)*
