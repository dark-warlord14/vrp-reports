# Heap-buffer-overflow in blink::SVGFilterGraphNodeMap::addPrimitive

| Field | Value |
|-------|-------|
| **Issue ID** | [40083011](https://issues.chromium.org/issues/40083011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SVG |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | fs...@opera.com |
| **Created** | 2015-10-09 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4572849078009856

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x61200006ac88
Crash State:
  blink::SVGFilterGraphNodeMap::addPrimitive
  blink::SVGF

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083011)*
