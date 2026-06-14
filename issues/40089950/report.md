# Heap-buffer-overflow in SkRecorder::onDrawPosTextH

| Field | Value |
|-------|-------|
| **Issue ID** | [40089950](https://issues.chromium.org/issues/40089950) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | m....@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2017-12-19 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36

Steps to reproduce the problem:
1. build https://chromium.googlesource.com/chromium/src/+/65.0.3294.6/
2. run ./filter_fuzz_stub poc 

[1219/185539.631743:INFO:filter_

## Attachments

- [poc234](attachments/poc234) (text/plain, 372 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089950)*
