# Heap-use-after-free in blink::DeprecatedPaintLayer::setGroupedMapping

| Field | Value |
|-------|-------|
| **Issue ID** | [40082450](https://issues.chromium.org/issues/40082450) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2015-07-08 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4874486313123840

Fuzzer: Miaubiz_css_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x048701e4
Crash State:
  blink::DeprecatedPaintLayer::setGroupedMapping
  blink::CompositedDeprecatedPaint

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082450)*
