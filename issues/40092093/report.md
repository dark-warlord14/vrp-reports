# Use-after-poison in void blink::Visitor::HandleWeakCell<blink::SVGElement>

| Field | Value |
|-------|-------|
| **Issue ID** | [40092093](https://issues.chromium.org/issues/40092093) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ke...@chromium.org |
| **Created** | 2018-08-02 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5058318557773824

Fuzzer: miaubiz_svg_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee5e1a2d628
Crash State:
  void blink::Visitor::HandleWeakCell<blink::SVGElement>
  blink::ThreadHeap::

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092093)*
