# Heap-use-after-free in WebCore::CompositedLayerMapping::~CompositedLayerMapping

| Field | Value |
|-------|-------|
| **Issue ID** | [40079379](https://issues.chromium.org/issues/40079379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Compositing |
| **Reporter** | cl...@chromium.org |
| **Assignee** | vo...@chromium.org |
| **Created** | 2014-04-19 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4743489860403200

Fuzzer: Miaubiz_css_fuzzer
Job Type: Android_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x42d10c58
Crash State:
  - crash stack -
  WebCore::CompositedLayerMapping::~CompositedLayerMapping
  WebC

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079379)*
