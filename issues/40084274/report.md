# Heap-use-after-free in blink::DeferredTaskHandler::handleDirtyAudioNodeOutputs

| Field | Value |
|-------|-------|
| **Issue ID** | [40084274](https://issues.chromium.org/issues/40084274) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-05-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5175218980519936

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6020001aa8b8
Crash State:
  blink::DeferredTaskHandler::handleDirtyAudioN

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084274)*
