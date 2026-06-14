# Heap-use-after-free in blink::LargeTextFirst

| Field | Value |
|-------|-------|
| **Issue ID** | [40095490](https://issues.chromium.org/issues/40095490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-06-24 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5183421999087616

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0xf399e398
Crash State:
  blink::LargeTextFirst
  blink::TextPaintTimingDetector::RecordAggr

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095490)*
