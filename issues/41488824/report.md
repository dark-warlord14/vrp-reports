# Heap-use-after-free in webrtc::JsepTransportController::ValidateAndMaybeUpdateBundleGroups

| Field | Value |
|-------|-------|
| **Issue ID** | [41488824](https://issues.chromium.org/issues/41488824) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | to...@webrtc.org |
| **Created** | 2024-01-05 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5162171615346688

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x50d0000b05b0
Crash State:
  webrtc::JsepTransportController::ValidateAndMaybeUpdateBundleGro

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41488824)*
