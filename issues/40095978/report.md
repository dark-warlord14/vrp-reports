# Use-after-poison in blink::Node::EnsureEventTargetData

| Field | Value |
|-------|-------|
| **Issue ID** | [40095978](https://issues.chromium.org/issues/40095978) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM, Blink>GarbageCollection, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | om...@chromium.org |
| **Created** | 2019-08-13 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6219506298257408

Fuzzer: domino
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0xe9f81938
Crash State:
  blink::Node::EnsureEventTargetData
  blink::EventTarget::AddEventListenerInternal

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095978)*
