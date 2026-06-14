# Stack-use-after-return in v8::internal::HandleBase::IsDereferenceAllowed

| Field | Value |
|-------|-------|
| **Issue ID** | [40084668](https://issues.chromium.org/issues/40084668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2016-06-23 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6008956061483008

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 8
Crash Address: 0x7f6eaf8b5110
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084668)*
