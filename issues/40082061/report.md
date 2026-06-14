# Heap-buffer-overflow in SkData::NewUninitialized

| Field | Value |
|-------|-------|
| **Issue ID** | [40082061](https://issues.chromium.org/issues/40082061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5870588761997312

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xf4202bd4
Crash State:
  SkData::NewUninitialized
  SkPictureData::parseBufferTag
  Sk

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082061)*
