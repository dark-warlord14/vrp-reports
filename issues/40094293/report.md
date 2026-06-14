# DCHECK failure in 0 <= index && index < node->op()->ValueInputCount() in node-properties.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40094293](https://issues.chromium.org/issues/40094293) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | si...@chromium.org |
| **Created** | 2019-03-14 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5661775296069632

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  0 <= index && index < node->op()->ValueInputCount() in node-properties.cc
  
Sanitizer: address (

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094293)*
