# Heap-use-after-free in SelectFileDialogExtension::ExtensionDialogClosing

| Field | Value |
|-------|-------|
| **Issue ID** | [40093674](https://issues.chromium.org/issues/40093674) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Views, UI>Browser |
| **Platforms** | ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | xi...@chromium.org |
| **Created** | 2019-01-08 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6332039456096256

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_chromeos
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000186110
Crash State:
  SelectFileDialogExtension::ExtensionDialogClosing
  vi

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093674)*
