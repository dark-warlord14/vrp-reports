# Heap-use-after-free in blink::LayoutObject::containingBlock

| Field | Value |
|-------|-------|
| **Issue ID** | [40084223](https://issues.chromium.org/issues/40084223) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Editing>Selection, Blink>HTML>Meter |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2016-05-03 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6516471743643648

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000045de0
Crash State:
  blink::LayoutObject::containingBlock
  blink::CaretBase:

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084223)*
