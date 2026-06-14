# Security: Heap-use-after-free in AXTreeDistiller::ScreenAIServiceReady

| Field | Value |
|-------|-------|
| **Issue ID** | [41490491](https://issues.chromium.org/issues/41490491) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2024-01-11 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**   
1. download asan-linux-release-1245721.zip and unzip  
2. run chrome `chrome  --user-data-dir=/tmp/noexist123 --no-sandbox` and open `chrome-untrusted://read-anything-side-panel.top-chrome/`  
3. go back and go forward several times to trigger the UAF  
Note th

## Attachments

- [video.webm](attachments/video.webm) (video/webm, 1.4 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 21.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41490491)*
