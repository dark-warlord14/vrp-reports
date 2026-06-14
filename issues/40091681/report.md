# use-after-free in operator-> buildtools/third_party/libc++/trunk/include/memory (WebAudio thread)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091681](https://issues.chromium.org/issues/40091681) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio, Blink>Workers |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2018-06-17 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
Version 69.0.3451.0 (Developer Build) (64-bit)

use-after-free in operator-> buildtools/third_party/libc++/trunk/include/memory (WebAudio thre

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [original_fuzz.html](attachments/original_fuzz.html) (text/plain, 1.7 KB)
- [uaf_symbolised2.log](attachments/uaf_symbolised2.log) (text/plain, 40.6 KB)
- deleted (application/octet-stream, 0 B)
- [audio-worklet.wasmmodule.js](attachments/audio-worklet.wasmmodule.js) (text/plain, 160.4 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 5.7 MB)
- [crash3.html](attachments/crash3.html) (text/plain, 351 B)
- [crash4.html](attachments/crash4.html) (text/plain, 351 B)
- [back.html](attachments/back.html) (text/plain, 100 B)
- [crash4.html](attachments/crash4_53054013.html) (text/plain, 355 B)
- [back.html](attachments/back_53054016.html) (text/plain, 129 B)
- [new.zip](attachments/new.zip) (application/octet-stream, 59.7 KB)
- [new2.zip](attachments/new2.zip) (application/octet-stream, 33.3 KB)
- [new3.zip](attachments/new3.zip) (application/octet-stream, 8.4 MB)
- [back.html](attachments/back_53054292.html) (text/plain, 138 B)
- [UNKNOWN_ReadAV_windows_release.txt](attachments/UNKNOWN_ReadAV_windows_release.txt) (text/plain, 3.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091681)*
