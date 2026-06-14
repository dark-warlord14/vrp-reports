# Heap-use-after-free in v8::internal::MemoryReducer::TimerTask::Run

| Field | Value |
|-------|-------|
| **Issue ID** | [40082480](https://issues.chromium.org/issues/40082480) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | th...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2015-07-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6545737242902528

Fuzzer: Therealholden_worker
Job Type: Windows_asan_chrome_no_sandbox

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x07ba48f0
Crash State:
  v8::internal::MemoryReducer::TimerTask::Run
  base::internal::Invoke

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082480)*
