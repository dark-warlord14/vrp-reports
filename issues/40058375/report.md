# A GPU crash (or anything that causes loss of GPU support for Chrome) will create framebuffer ghosting with ImageBitmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40058375](https://issues.chromium.org/issues/40058375) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>WebGPU |
| **Platforms** | Windows |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2021-12-30 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version       : 96.0.4664.110 (Official Build) (64-bit) (cohort: Stable)  
**URLs (if applicable) :**  https://www.planetminecraft.com  - currently reproduceable in our dynamic header (the top ~120 pixels at the top that show a rotating planet, if your browser has WebGL support). On Chrome, t

## Attachments

- [1283434.mp4](attachments/1283434.mp4) (video/mp4, 1.8 MB)
- [1283434-M97.mp4](attachments/1283434-M97.mp4) (video/mp4, 2.0 MB)
- [GPU.txt](attachments/GPU.txt) (text/plain, 23.3 KB)
- [index.html](attachments/index.html) (text/plain, 150 B)
- [main.js](attachments/main.js) (text/plain, 343 B)
- [worker.js](attachments/worker.js) (text/plain, 464 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058375)*
