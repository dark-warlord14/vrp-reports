# Heap-buffer-overflow in media::VideoFrame::visible_data

| Field | Value |
|-------|-------|
| **Issue ID** | [40092207](https://issues.chromium.org/issues/40092207) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Core |
| **Platforms** | Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mc...@chromium.org |
| **Created** | 2018-08-17 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=6542630163578880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x603000134ccc
Crash State:
  media::VideoFrame::visible_data
  media::CopyRowsToRGBABuff

## Attachments

- [clusterfuzz-testcase-6542630163578880.webm](attachments/clusterfuzz-testcase-6542630163578880.webm) (video/webm, 89.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092207)*
