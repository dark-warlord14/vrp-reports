# Security: heap after free at `RenderFrameHostManager::GetFrameHostForNavigation`

| Field | Value |
|-------|-------|
| **Issue ID** | [40073755](https://issues.chromium.org/issues/40073755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 18...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2023-09-29 |
| **Bounty** | $1,000.00 |

## Description

Hey, I want to report a UAF bug at [RenderFrameHostManager::GetFrameHostForNavigation](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1527). however , The bug is a strange bug(because there not only one bug, and I don't know shou

## Attachments

- [patch.cpp](attachments/patch.cpp) (text/plain, 3.4 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 23.5 KB)
- [4278923_issue.cpp](attachments/4278923_issue.cpp) (text/plain, 3.3 KB)
- [4278923_issue_asan.txt](attachments/4278923_issue_asan.txt) (text/plain, 23.7 KB)
- [server.py](attachments/server.py) (text/plain, 1.7 KB)
- [found_18f.pem](attachments/found_18f.pem) (application/octet-stream, 2.8 KB)
- [fake_asan.log](attachments/fake_asan.log) (text/plain, 32.4 KB)
- [fake_patch.diff](attachments/fake_patch.diff) (text/plain, 1.5 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073755)*
