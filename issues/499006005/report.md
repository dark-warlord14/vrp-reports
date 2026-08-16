# Cross-origin information disclosure via stale ANGLE Metal texture views (GPU process heap leak)

| Field | Value |
|-------|-------|
| **Issue ID** | [499006005](https://issues.chromium.org/issues/499006005) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU, Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | th...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-04-03 |
| **Bounty** | $10,000.00 |

## Description

VULNERABILITY

Any WebGL2 page on macOS can continuously read GPU process heap memory, leaking cross-origin URLs, pointers, and metadata from other tabs. ~35 MB/s sustained, no user interaction, default Chrome config.

The GPU process composites all tabs. URL strings from resource loading end up on its heap. Stale ANGLE texture views expose this memory to JavaScript through readPixels.

REPRODUCTION (cross-origin URL leak)

1. Open attached poc-heap-leak.html in official Google Chrome (stable or canary) on macOS
2. Open other tabs with any websites (e.g. reddit.com)
3. Watch the PoC page — leaked URL fragments, pointers, and strings appear within seconds

See attached video (poc-heap-leak.mov) and screenshot (poc-heap-leak.png).

Works on both stable (147) and canary (148). The PoC tries multiple exploitation strategies to cover different ANGLE internal layouts.

ROOT CAUSE

TextureMtl::retainImageDefinitions() in TextureMtl.mm. When a texture is redefined (format or size change), redefineImage() calls deallocateNativeStorage(keepImages=true) which saves stale image views on all mip levels. These views reference old Metal texture allocations whose backing memory contains recycled GPU data from other tabs' compositor textures.

6d8b704e2a ("Remove TextureMtl::mFormat", cherry-picked to M146/M147) does not fix this. The stale image definitions survive — getImageDefinition() only updates when imageDef.image is null, but retained images are non-null.

OOB READ/WRITE (ASAN)

The same root cause also produces OOB read and write, confirmable with ASAN. The HTML PoC does NOT trigger ASAN (ASAN cannot catch Metal-managed memory issues). To reproduce under ASAN:

1. Apply attached angle-texturetest.diff, build angle_end2end_tests with ASAN on macOS
2. OOB read: ANGLE_DEFAULT_PLATFORM=metal ./out/asan/angle_end2end_tests --gtest_filter="*StaleFormatIDHeapOverflowRead*"
3. OOB write: MTL_DEBUG_LAYER=1 ANGLE_DEFAULT_PLATFORM=metal ./out/asan/angle_end2end_tests --gtest_filter="*StaleImageSizeHeapOverflowWrite*"

OOB READ ASAN stack traces attached: `StaleFormatIDHeapOverflowRead.txt`
OOB Write AGX Assert attached: `StaleImageSizeHeapOverflowWrite.txt`

SUGGESTED FIX

Attached angle-fix-stale-imagedef.diff addresses the root cause.

VERSION
Chrome Version: 147.0.7727.50 (stable), 148.0.7769.0 (canary)
Operating System: macOS ARM64

ATTACHMENTS
- poc-heap-leak.html — live cross-origin URL leak PoC
- poc-heap-leak.mp4 — video demonstration
- poc-heap-leak.png — screenshot
- angle-texturetest.diff — ANGLE test for ASAN reproduction
- StaleFormatIDHeapOverflowRead.txt — ASAN stack trace
- StaleImageSizeHeapOverflowWrite.txt — ASAN stack trace
- angle-fix-stale-imagedef.diff — suggested fix

CREDIT INFORMATION
Reporter credit: Thomas Guillem <thomas@gllm.fr>


## Attachments

- [angle-fix-stale-imagedef.diff](attachments/angle-fix-stale-imagedef.diff) (text/x-diff, 1.0 KB)
- [angle-texturetest.diff](attachments/angle-texturetest.diff) (text/x-diff, 5.1 KB)
- [poc-heap-leak.html](attachments/poc-heap-leak.html) (text/html, 14.0 KB)
- [poc-heap-leak.mov](attachments/poc-heap-leak.mov) (video/quicktime, 44.4 MB)
- [poc-heap-leak.png](attachments/poc-heap-leak.png) (image/png, 1.3 MB)
- [StaleFormatIDHeapOverflowRead.txt](attachments/StaleFormatIDHeapOverflowRead.txt) (text/plain, 11.3 KB)
- [StaleImageSizeHeapOverflowWrite.txt](attachments/StaleImageSizeHeapOverflowWrite.txt) (text/plain, 4.1 KB)
- [poc-leak-incognito.png](attachments/poc-leak-incognito.png) (image/png, 1.0 MB)
- [poc-heap-leak.html](attachments/poc-heap-leak_75152064.html) (text/html, 14.8 KB)
- [incognito-leak.mov](attachments/incognito-leak.mov) (video/quicktime, 32.3 MB)
- [poc-heap-leak.html](attachments/poc-heap-leak_75152086.html) (text/html, 14.4 KB)

## Timeline

### th...@gmail.com (2026-04-03)

Fixup of the VERSION section:

The leak was reproduced on macOS 26.3.1 ARM64, Mac Mini M2.
With current official chrome stable and canary:
 - Version 148.0.7770.0 (Official Build) canary (arm64)
 - Version 146.0.7680.178 (Official Build) (arm64)

It does not seem to leak anything with Intel Mac mini.

### th...@gmail.com (2026-04-03)

It is also possible to leak URLs navigated in incognito mode (from a non-incognito tab).

### th...@gmail.com (2026-04-03)

Here is an improved version of the poc (faster String/URL leak) with a video proof of an incognito URL leak.

### th...@gmail.com (2026-04-04)

Here is the last version of the poc. I removed the misleading counter in kB, because there is no real way to know if the returned gpu data is leaked or not.

Opening this poc on Safari, Firefox, Linux Chromium or any other browser/config now show 0 leaks (it was the case before, but the leak kb counter was not 0). 
It still shows URL/STRING leaks on macOS chromium.

### ch...@google.com (2026-04-04)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-04)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-05-04)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7806315>

Metal: Treat glGenerateMipmap as an image redefinition.

---


Expand for full commit details
```
     
    When TextureMtl::generateMipmap creates a native storage, it doesn't 
    treat it as a texture redefinition and clear out old images. This leaves 
    images with formats and sizes that do not match the storage. 
     
    Fixed: chromium:499006005 
    Change-Id: I78cdbf77ccb75469fba3ca4654ea9118aa80edd5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7806315 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/ContextMtl.mm`
- M `src/libANGLE/renderer/metal/TextureMtl.h`
- M `src/libANGLE/renderer/metal/TextureMtl.mm`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [cf8ec6403ff88f7ff8e544d59b9c405452279cc1](https://chromiumdash.appspot.com/commit/cf8ec6403ff88f7ff8e544d59b9c405452279cc1)  

Date: Fri May 1 17:20:55 2026


---

### wf...@chromium.org (2026-05-12)

reporter: do not post restricted content to vulnerability reports. This is against the VRP rules which state that comments are public so others can learn from them.

### aj...@google.com (2026-05-12)

reporter: if the restricted comments do not contain PII could you please unrestrict them.

### th...@gmail.com (2026-05-12)

Fixed !

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High quality. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514924563](https://crbug.com/514924563) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514928735](https://crbug.com/514928735) to have this merge reviewed.**

### th...@gmail.com (2026-06-12)

For your information. The issue is still present in latest 148/149 versions. Just checked with 149.0.7827.115 on macOS: it is still possible to leak URLs from incognito tabs.

I don't know if that is expected, but the 2 148/149 backport merge requests since to be stalled.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499006005)*
