# DCHECK failure in GetReadOnlyRoots().fixed_cow_array_map() != map() in fixed-array-inl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40094554](https://issues.chromium.org/issues/40094554) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | du...@microsoft.com |
| **Created** | 2019-04-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=4867906201583616

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  GetReadOnlyRoots().fixed_cow_array_map() != map() in fixed-array-inl.h
  v8::internal::FixedArray

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094554)*
