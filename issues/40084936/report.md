# Use-after-poison in blink::CompositorAnimationPlayer::NotifyAnimationStarted

| Field | Value |
|-------|-------|
| **Issue ID** | [40084936](https://issues.chromium.org/issues/40084936) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-07-25 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5078527401787392

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9287e2d1d0
Crash State:
  blink::CompositorAnimationPlayer::NotifyAnimationStarted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084936)*
