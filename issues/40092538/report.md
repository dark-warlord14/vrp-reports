#  heap-use-after-free on incontent::RenderFrameHostImpl::AudioContextPlaybackStarted(int)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092538](https://issues.chromium.org/issues/40092538) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Media>Autoplay, Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2018-09-23 |
| **Bounty** | $5,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36

Steps to reproduce the problem:
Version 71.0.3560.0 (Developer Build) (64-bit)
1.build new chrome with asan.
	is_asan = true
	is_debug = false
	enable_nacl = false

## Attachments

- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 2.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092538)*
