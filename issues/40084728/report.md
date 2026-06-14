# Heap-buffer-overflow in CWeightTable::Calc

| Field | Value |
|-------|-------|
| **Issue ID** | [40084728](https://issues.chromium.org/issues/40084728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-06-29 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4580419215556608

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x7fb7dcdfc004
Crash State:
  CWeightTable::Calc
  CStretchEngine::StartStretchHorz

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084728)*
