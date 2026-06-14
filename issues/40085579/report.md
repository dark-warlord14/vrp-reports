# Use-of-uninitialized-value in blink::PropertyHandle::operator==

| Field | Value |
|-------|-------|
| **Issue ID** | [40085579](https://issues.chromium.org/issues/40085579) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-10-03 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6656629452046336

Fuzzer: attekett_dom_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::PropertyHandle::operator==
  std::__1::pair<WTF::KeyValuePair<blin

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085579)*
