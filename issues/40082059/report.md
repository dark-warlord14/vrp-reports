# UNKNOWN in _fini

| Field | Value |
|-------|-------|
| **Issue ID** | [40082059](https://issues.chromium.org/issues/40082059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5125299461685248

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: UNKNOWN
Crash Address: 0x7f4a1ad16d75
Crash State:
  _fini
  SkBitmapDevice::drawPoints
  SkCanvas::onDrawPoints
  
Regressed: https://cl

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082059)*
