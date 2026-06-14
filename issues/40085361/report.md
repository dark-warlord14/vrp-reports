# Use-after-poison in blink::TimerBase::runInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40085361](https://issues.chromium.org/issues/40085361) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Scheduling |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-09-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5836363167694848

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9026aa55d0
Crash State:
  blink::TimerBase::runInternal
  base::debug::TaskAnnotat

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085361)*
