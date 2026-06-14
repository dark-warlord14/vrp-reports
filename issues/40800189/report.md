# Non-positive-vla-bound-value in blink::CanvasPath::roundRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40800189](https://issues.chromium.org/issues/40800189) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>Canvas, Blink>JavaScript>API |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2021-10-26 |
| **Bounty** | $1,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6010514792316928

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_ubsan_chrome
Platform Id: linux

Crash Type: Non-positive-vla-bound-value
Crash Address: 
Crash State:
  blink::CanvasPath::roundRect
  blink::v8_canvas_rendering_context_2d::RoundRec

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40800189)*
