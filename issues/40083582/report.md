# Crash (assert) in blink::AudioDelayDSPKernel::process

| Field | Value |
|-------|-------|
| **Issue ID** | [40083582](https://issues.chromium.org/issues/40083582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-01-30 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5213979443462144

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x7f5f69e0d800
Crash State:
  blink::AudioDelayDSPKernel::process
  blink::AudioDSPKernelProce

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083582)*
