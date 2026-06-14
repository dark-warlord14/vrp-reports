# Crash in v8::internal::Simulator::DecodeType2

| Field | Value |
|-------|-------|
| **Issue ID** | [40086197](https://issues.chromium.org/issues/40086197) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-12-12 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5916664546983936

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffff
Crash State:
  v8::internal::Simulator::DecodeType2
  v8::internal::Simulator::

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086197)*
