# Security: Skia: Out-of-bounds Read in src/codec/SkSwizzler

| Field | Value |
|-------|-------|
| **Issue ID** | [40092762](https://issues.chromium.org/issues/40092762) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | sc...@google.com |
| **Created** | 2018-10-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
  
https://cs.chromium.org/chromium/src/third_party/skia/src/codec/SkSwizzler.cpp?l=54  
  
```  
static void sample6(void\* dst, const uint8_t\* src, int width, int bpp, int deltaSrc, int offset,  
        const SkPMColor ctable[]) {  
    src += offset;  
    uint8_t\*

## Attachments

- [Sk_android_codec_crash](attachments/Sk_android_codec_crash) (text/plain, 2.0 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092762)*
