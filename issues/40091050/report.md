# Security: heap-use-after-free in check_client_download_request.cc when in incognito mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40091050](https://issues.chromium.org/issues/40091050) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2018-04-09 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
chrome Version: 67.0.3392.0 (Developer Build) (64-bit)
ubuntu version: 16.04

Security: heap-use-after-free in check_client_download_request.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [repro_video.mp4](attachments/repro_video.mp4) (video/mp4, 8.9 MB)
- [repro_video2.mp4](attachments/repro_video2.mp4) (video/mp4, 9.0 MB)
- [asan_symbolized2.log](attachments/asan_symbolized2.log) (text/plain, 51.5 KB)
- [ASANsymbolizedvmodule.log](attachments/ASANsymbolizedvmodule.log) (text/plain, 51.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091050)*
