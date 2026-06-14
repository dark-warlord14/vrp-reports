# Heap-buffer-overflow in ps_table_add

| Field | Value |
|-------|-------|
| **Issue ID** | [40084275](https://issues.chromium.org/issues/40084275) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | bu...@chromium.org |
| **Created** | 2016-05-10 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4548226098659328

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 7
Crash Address: 0x61b000014f90
Crash State:
  ps_table_add
  parse_encoding
  parse_dict
  
Reco

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084275)*
