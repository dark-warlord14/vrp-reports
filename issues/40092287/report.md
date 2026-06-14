# Crash in gpu::gles2::Texture::ClearRenderableLevels

| Field | Value |
|-------|-------|
| **Issue ID** | [40092287](https://issues.chromium.org/issues/40092287) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-08-27 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

Steps to reproduce the problem:
Version 70.0.3515.0 (Developer Build) (64-bit)(ubuntu)
68.0.3440.106(release)(32bit)(windows)

1.build new chrome with asan.
2. ./chrome ./

## Attachments

- deleted (application/octet-stream, 0 B)
- [minimised.html](attachments/minimised.html) (text/plain, 2.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092287)*
