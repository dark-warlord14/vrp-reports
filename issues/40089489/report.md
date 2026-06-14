# Security: heap-use-after-free blink::AudioSummingJunction::UpdateRenderingState

| Field | Value |
|-------|-------|
| **Issue ID** | [40089489](https://issues.chromium.org/issues/40089489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | rt...@chromium.org |
| **Created** | 2017-11-02 |
| **Bounty** | $3,000.00 |

## Description

I have tested this on asan-linux-release-513290 and asan-linux-stable-62.0.3202.75.

This is a UAF in webAudio

==21486==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000050550 at pc 0x55abc8b3e0f3 bp 0x7fe0b6a84190 sp 0x7fe0b6a84188
READ of size 4 at 0x60b000050550 thread T743 (

## Attachments

- [DSP_UAF.html](attachments/DSP_UAF.html) (text/plain, 4.5 KB)
- [asan_uaf.txt](attachments/asan_uaf.txt) (text/plain, 24.7 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089489)*
