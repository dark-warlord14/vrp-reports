# Crash in v8::internal::InnerPointerToCodeCache::GcSafeFindCodeForInnerPointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40083887](https://issues.chromium.org/issues/40083887) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2016-03-17 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5403499919048704

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7fff7ea00030
Crash State:
  v8::internal::InnerPointerToCodeCache::GcSafeFindCodeForInnerPointer
  v8::i

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083887)*
