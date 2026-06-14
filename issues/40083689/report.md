# Heap-use-after-free in blink::InlineFlowBox::addToLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40083689](https://issues.chromium.org/issues/40083689) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | ea...@chromium.org |
| **Created** | 2016-02-13 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6566106111672320

Fuzzer: attekett_surku_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7d1400014a58
Crash State:
  blink::InlineFlowBox::addToLine
  blink::LayoutBlockF

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083689)*
