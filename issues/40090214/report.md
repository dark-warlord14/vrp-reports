# DCHECK failure in current_ == next_ in node.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40090214](https://issues.chromium.org/issues/40090214) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2018-01-17 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5874775150034944

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  current_ == next_ in node.h
  v8::internal::compiler::Node::Uses::const_iterator::operator++
  v8

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090214)*
