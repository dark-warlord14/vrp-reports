# Heap-buffer-overflow in blink::TimerBase::stop

| Field | Value |
|-------|-------|
| **Issue ID** | [40083475](https://issues.chromium.org/issues/40083475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Platforms** | Windows |
| **Reporter** | mi...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2015-12-30 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6507228867067904

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-buffer-overflow WRITE 16
Crash Address: 0x0e10eb80
Crash State:
  blink::TimerBase::stop
  blink::HTMLInputEleme

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083475)*
