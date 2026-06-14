# Stack-buffer-overflow in spv::Builder::createMatrixConstructor

| Field | Value |
|-------|-------|
| **Issue ID** | [40769704](https://issues.chromium.org/issues/40769704) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>Internals |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sy...@chromium.org |
| **Created** | 2021-06-01 |
| **Bounty** | $6,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=6215979714281472

Fuzzer: aohelin_ni
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-buffer-overflow WRITE 4
Crash Address: 0x7f4caaada160
Crash State:
  spv::Builder::createMatrixConstructor
  TGlslangToSpvTraverser::visitAg

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40769704)*
