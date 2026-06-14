# Heap-use-after-free in blink::LayoutBoxModelObject::invalidateStickyConstraints

| Field | Value |
|-------|-------|
| **Issue ID** | [40083992](https://issues.chromium.org/issues/40083992) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-04-01 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4893865365995520

Fuzzer: attekett_dom_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7d340000b000
Crash State:
  blink::LayoutBoxModelObject::invalidateStickyConstraints

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083992)*
