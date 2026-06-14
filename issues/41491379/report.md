# Security:  [Network Process] 8-byte use-after-free in `net::QuicChromiumClientSession`

| Field | Value |
|-------|-------|
| **Issue ID** | [41491379](https://issues.chromium.org/issues/41491379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Mac |
| **Reporter** | op...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2024-01-15 |
| **Bounty** | $7,000.00 |

## Description

## Tested Version

  •  121.0.6140.0 (Developer Build)
  •  `mac-release-asan-mac-release-1227262` from storage bucket
  •  macOS 14.2 (23C5055b)

## Attachments

  •  Apple MacOS Crash Report: 1-apple-macos-crash-report.log
  •  Chromium ASAN Report: 2-chromium-asan-report.log
  •  Proof

## Attachments

- [1-apple-macos-crash-report.log](attachments/1-apple-macos-crash-report.log) (text/plain, 26.1 KB)
- [2-chromium-asan-report.log](attachments/2-chromium-asan-report.log) (text/plain, 28.2 KB)
- deleted (application/octet-stream, 0 B)
- [3-proof-of-concept.html](attachments/3-proof-of-concept.html) (text/html, 320 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491379)*
