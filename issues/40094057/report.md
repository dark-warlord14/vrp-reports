# Heap-use-after-free in aura::EventObserverAdapter::~EventObserverAdapter

| Field | Value |
|-------|-------|
| **Issue ID** | [40094057](https://issues.chromium.org/issues/40094057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Aura |
| **Platforms** | ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ms...@chromium.org |
| **Created** | 2019-02-16 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5101997038632960

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x613000177f28
Crash State:
  aura::EventObserverAdapter::~EventObserverAdapter
  views::

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094057)*
