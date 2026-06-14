# Security: WriteTexture heap-buffer-overflow in WebGL on macOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40090246](https://issues.chromium.org/issues/40090246) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | zm...@chromium.org |
| **Created** | 2018-01-20 |
| **Bounty** | $1,000.00 |

## Description

heap overflow in WriteTextureData on macOS, tested on asan-mac-release-529226.zip

==801==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000046a04 at pc 0x000101cc248b bp 0x7ffeedf9f5f0 sp 0x7ffeedf9ed90
READ of size 8 at 0x602000046a04 thread T0
    #0 0x101cc248a  (libclang_rt.a

## Attachments

- [writeTexture.html](attachments/writeTexture.html) (text/plain, 1.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 9.6 KB)
- [simplied_test_case_for_crbug_804118.html](attachments/simplied_test_case_for_crbug_804118.html) (text/plain, 516 B)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090246)*
