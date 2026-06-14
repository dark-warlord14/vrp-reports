# heap-use-after-free in Cancel::wasm-engine.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40095298](https://issues.chromium.org/issues/40095298) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2019-06-05 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

Steps to reproduce the problem:
1. Build asan 77.0.3815.0  version of chrome.
2. Put ws.js and bit-crusher.js into the same dir with poc.html and use nodejs to setup a

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [res.zip](attachments/res.zip) (application/octet-stream, 45.6 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095298)*
