# UAF in webrtc::BitrateAllocator::OnNetworkEstimateChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [41497180](https://issues.chromium.org/issues/41497180) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2024-02-02 |
| **Bounty** | $11,000.00 |

## Description

**Steps to reproduce the problem:**   
repro steps:  
./chrome --use-file-for-fake-video-capture=/xx/fake-video.y4m   --use-fake-ui-for-media-stream --use-fake-device-for-media-stream       --incognito   --user-data-dir=/tmp/xx  --js-flags=--expose-gc http://localhost:8880/crash,html  
  
**Problem

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.2 KB)
- [fake-video.y4m](attachments/fake-video.y4m) (application/octet-stream, 8.1 MB)
- [asan.log](attachments/asan.log) (text/plain, 29.6 KB)
- [asan.log](attachments/asan_53032339.log) (text/plain, 31.2 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41497180)*
