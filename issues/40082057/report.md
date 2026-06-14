# Stack-buffer-overflow in SkPackBits::Unpack8

| Field | Value |
|-------|-------|
| **Issue ID** | [40082057](https://issues.chromium.org/issues/40082057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | hc...@chromium.org |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4850438600392704

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Stack-buffer-overflow WRITE {*}
Crash Address: 0x7f13a2a961a0
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkVa

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082057)*
