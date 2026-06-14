# AddressSanitizer: heap-use-after-free in blink::Screen::AreWebExposedScreenPropertiesEqual

| Field | Value |
|-------|-------|
| **Issue ID** | [40058028](https://issues.chromium.org/issues/40058028) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Screen>MultiScreen, UI>Browser>WebAppInstalls>Desktop |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dm...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2021-11-25 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0

Steps to reproduce the problem:
I reproduce this in MacOS Big Sur (11.6) with BetterDummy (https://github.com/waydabber/BetterDummy/releases/tag/v1.0.10) to simulate another screens. Maybe it's reproduc

## Attachments

- [heap-uaf-screens.txt](attachments/heap-uaf-screens.txt) (text/plain, 32.5 KB)
- [screens.zip](attachments/screens.zip) (application/octet-stream, 956 B)
- [ChromiumHeapUseAfterFreeViaScreens.mp4](attachments/ChromiumHeapUseAfterFreeViaScreens.mp4) (video/mp4, 9.3 MB)
- [crbug1273841.html](attachments/crbug1273841.html) (text/plain, 1.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058028)*
