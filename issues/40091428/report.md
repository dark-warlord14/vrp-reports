# heap-use-after-free on AudioOutputDevi

| Field | Value |
|-------|-------|
| **Issue ID** | [40091428](https://issues.chromium.org/issues/40091428) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Audio, Blink>MediaStream, Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2018-05-19 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36

Steps to reproduce the problem:
Version 68.0.3430.0 (Developer Build) (64-bit)
Version 66.0.3359.170(Windows Release)(32-bit)
heap-use-after-free on AudioOutputDevi

1.Get

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 4.2 KB)
- [asan_symbolized.log](attachments/asan_symbolized.log) (text/plain, 22.3 KB)
- [res.zip](attachments/res.zip) (application/octet-stream, 2.6 KB)
- [844833.zip](attachments/844833.zip) (application/octet-stream, 1.9 KB)
- [asan_symbolized2.log](attachments/asan_symbolized2.log) (text/plain, 19.7 KB)
- [asan_symbolized_withpatch.log](attachments/asan_symbolized_withpatch.log) (text/plain, 22.8 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091428)*
