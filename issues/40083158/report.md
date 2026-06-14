# Heap-use-after-free in blink::LayoutBlock::removeChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40083158](https://issues.chromium.org/issues/40083158) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2015-11-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5636999954825216

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000056320
Crash State:
  blink::LayoutBlock::removeChild
  blink::LayoutObject::wi

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083158)*
