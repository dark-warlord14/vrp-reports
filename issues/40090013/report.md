# heap-buffer-overflow in SkAAClip::quickContains

| Field | Value |
|-------|-------|
| **Issue ID** | [40090013](https://issues.chromium.org/issues/40090013) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2017-12-29 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3298.3/
2. run ./filter_fuzz_stub ./poc 

What is the expected behavior?

## Attachments

- [poc](attachments/poc) (text/plain, 744 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090013)*
