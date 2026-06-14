# WebRTC: Potential Use-after-free in VP8 Block Decoding (MFQE feature)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093356](https://issues.chromium.org/issues/40093356) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2018-6155 |
| **Reporter** | ey...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2018-12-09 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36

Steps to reproduce the problem:
Always happens, the feature will never work.

The MFQE feature in VP8 block decoding (WebRTC) *never* works, due to a bug. If it will w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093356)*
