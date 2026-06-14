# heap-use-after-free on sw::Renderer::finishRendering

| Field | Value |
|-------|-------|
| **Issue ID** | [40093054](https://issues.chromium.org/issues/40093054) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2018-11-13 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Download asan version asan-linux-release-606772
2. Run ./chrome.exe --disable-gpu poc.html

What is the expected behavior?

What went wrong?

## Attachments

- [utility.js](attachments/utility.js) (text/plain, 2.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 998 B)
- [asan.log](attachments/asan.log) (text/plain, 14.9 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093054)*
