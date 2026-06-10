# ANGLE Vulkan reinitImageAsRenderable uint32 Overflow causes GPU OOB Write

| Field | Value |
|-------|-------|
| **Issue ID** | [485622239](https://issues.chromium.org/issues/485622239) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | ci...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $33,000.00 |

## Description

---

### Report description

ANGLE Vulkan reinitImageAsRenderable uint32 Overflow causes GPU OOB Write

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/+/aca6a0fe0850/src/libANGLE/renderer/vulkan/TextureVk.cpp#3167>

---

### The problem

#### Please describe the technical details of the vulnerability

TextureVk::reinitImageAsRenderable in the ANGLE Vulkan backend computes a staging buffer size using five operands that multiply in 32-bit arithmetic, overflowing before widening to size\_t. When a WebGL2 page creates a non-renderable RGB8 TEXTURE\_2D\_ARRAY and calls copyTexSubImage3D, ANGLE detects that RGB8 is not natively renderable in Vulkan and converts the texture to RGBA8. The size calculation at TextureVk.cpp:3167 multiplies width, height, depth, pixelBytes, and layerCount in 32-bit arithmetic. For a 16384x16384x4-layer texture, the product is exactly 2^32 and wraps to 0. The staging buffer allocation receives the overflowed size (0). CopyImageCHROMIUM then writes 4GB of converted pixel data into it.

The attacker controls the source RGB8 pixel data. After conversion to RGBA8, the R, G, B channels are derived from the attacker's data and the alpha channel is always 0xFF. The attacker controls 3 of every 4 bytes written during the overflow.

No compromised renderer is required. The overflow is triggered entirely from JavaScript via the WebGL2 API.

Affects Stable, Beta, and Dev. The vulnerable code has been present since September 2021. Tested on:

- 144.0.7559.133 (Stable, Windows)
- 146.0.7678.0 (ASan, Windows)

### Affected Code

TextureVk.cpp, lines 3167-3168 in reinitImageAsRenderable:

```
size_t dstBufferSize = sourceBox.width * sourceBox.height * sourceBox.depth *
                       dstFormat.pixelBytes * layerCount;

```

All five operands (width, height, depth as int; pixelBytes, layerCount as uint32\_t) multiply in 32-bit arithmetic. The result overflows before being stored into the 64-bit size\_t. This value is passed to stageSubresourceUpdateAndGetData (line 3172), which calls initBufferForImageCopy to allocate a VMA staging buffer of the overflowed size. The CopyImageCHROMIUM loop at lines 3190-3197 writes the correct (non-overflowed) amount of data per layer, using pitch values from lines 3177-3184.

The pitch calculations at lines 3177-3184 use GLuint (uint32\_t) and have the same overflow class, but they do not overflow at the dimensions required to trigger the size overflow.

### Steps to Reproduce

1. Launch Chrome with: --use-angle=vulkan
2. Navigate to the attached poc.html
3. The PoC auto-fires on page load

For ASan builds, also pass --in-process-gpu --disable-features=SkiaGraphite --disable-gpu-compositing. The latter two flags prevent an unrelated Dawn/D3D11 initialization failure in ASan builds when ANGLE is set to Vulkan; they are not related to the vulnerability, but were required in my testing.

ASan output (Chrome 146.0.7678.0, Windows, Intel HD 620):

```
==17556==ERROR: AddressSanitizer: access-violation on unknown address 0x120973c50000
==17556==The signal is caused by a WRITE memory access.
    #0 angle::R8G8B8A8SRGB::writeColor               imageformats.cpp:392
    #1 rx::CopyImageCHROMIUM                           renderer_utils.cpp:795
    #2 rx::TextureVk::reinitImageAsRenderable          TextureVk.cpp:3192
    #3 rx::TextureVk::respecifyImageStorage            TextureVk.cpp:3260
    #4 rx::TextureVk::ensureRenderableWithFormat       TextureVk.cpp:4907
    #5 rx::TextureVk::ensureRenderableIfCopyTexImage.. TextureVk.cpp:4968
    #6 rx::TextureVk::copySubImage                     TextureVk.cpp:1479
    #7 gl::Texture::copySubImage                       Texture.cpp:1613
    #8 gl::Context::copyTexSubImage3D                  Context.cpp:5139

rax = 41  rcx = 120973c50000

```

RAX holds the attacker's marker byte (0x41) at the point of the crash. RCX is the destination pointer. The faulting instruction is writeColor writing the attacker's R channel byte to the overflow destination.

Chrome 144 stable (no --in-process-gpu) crashes the GPU process with STATUS\_ACCESS\_VIOLATION (0xC0000005), WRITE. The crashpad minidump confirms:

- RAX = 0x41 (attacker's marker byte)
- The 128 bytes immediately before the crash address contain 32 consecutive 41 41 41 FF RGBA pixels
- The overflow wrote through a 4MB PAGE\_READWRITE heap region and crashed at the adjacent PAGE\_NOACCESS boundary

The PoC works as follows:

1. Creates a 16384x16384x4-layer RGB8 TEXTURE\_2D\_ARRAY (non-renderable in Vulkan)
2. Fills the first 512 rows with a controlled marker byte (0x41)
3. Creates a 1x1 RGBA8 renderbuffer FBO as the copy source
4. Calls copyTexSubImage3D from the RGBA8 FBO into the RGB8 texture
5. ANGLE calls reinitImageAsRenderable, which computes dstBufferSize = 0 (uint32 overflow) and writes 4GB of RGBA8 converted data into the undersized staging buffer

The trigger path is:

```
gl.copyTexSubImage3D(TEXTURE_2D_ARRAY, ...)
  -> TextureVk::copySubImage
  -> ensureRenderableIfCopyTexImageCannotTransfer
  -> ensureRenderableWithFormat (RGB8 not renderable, convert to RGBA8)
  -> respecifyImageStorage
  -> reinitImageAsRenderable (layerCount > 1, takes slow path)
  -> dstBufferSize = width * height * depth * pixelBytes * layerCount overflows to 0
  -> stageSubresourceUpdateAndGetData allocates staging buffer with overflowed size
  -> CopyImageCHROMIUM writes 4GB into undersized buffer

```
### Fix

Use CheckedNumeric for the size calculation, consistent with how block-compressed formats are already handled via ANGLE\_VK\_CHECK\_MATH in vk\_helpers.cpp stageSubresourceUpdateImpl (lines 8375-8390):

```
angle::CheckedNumeric<size_t> checkedSize = sourceBox.width;
checkedSize *= sourceBox.height;
checkedSize *= sourceBox.depth;
checkedSize *= dstFormat.pixelBytes;
checkedSize *= layerCount;
ANGLE_VK_CHECK_MATH(contextVk, checkedSize.IsValid());
size_t dstBufferSize = checkedSize.ValueOrDie();

```

The GLuint pitch calculations at lines 3177-3184 should also use CheckedNumeric.

### Bisect

The vulnerable code was introduced in ANGLE commit 8ea87a6767 ("Vulkan: Avoid texture format fallback when possible"), committed 2021-09-08, CL <https://chromium-review.googlesource.com/c/angle/angle/+/3104514>. The entire reinitImageAsRenderable function, including the unchecked multiplication, was added as new code in this commit.

#### Impact analysis

Heap buffer overflow in the GPU process, reachable from JavaScript via WebGL2. The attacker controls 3 of every 4 bytes written during the 4GB overflow (the 4th byte is always 0xFF). The staging buffer is allocated in the VMA (Vulkan Memory Allocator) HOST\_VISIBLE staging pool. The overflow corrupts adjacent heap allocations. In release Chrome on Windows, approximately 4MB of heap data is overwritten with attacker-controlled content before the write reaches an unmapped page.

On Android, ANGLE Vulkan is the default backend and no command-line flags are required. The Android GPU process has no sandbox (kAndroidGpuSandbox is FEATURE\_DISABLED\_BY\_DEFAULT) and shares the same UID as the browser process, so this overflow corrupts memory in an unsandboxed process reachable from JavaScript with no user interaction. On Linux and ChromeOS, ANGLE Vulkan is the default on many configurations.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.133 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.8 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5504280400166912.

### ma...@google.com (2026-02-18)

Security shepherd: Thanks for the thorough report. ANGLE folks, PTAL?

### ci...@gmail.com (2026-02-19)

Looking at the ClusterFuzz output I see:

> WARNING: lavapipe is not a conformant vulkan implementation, testing use only.

> ContextResult::kFatalFailure: WebGL2 blocklisted

It looks like ClusterFuzz is using lavapipe, which may have resulted in WebGL2 being disabled/blocked, thus causing the PoC to exit before running. In my testing, this bug required a real Vulkan-capable GPU to reproduce.

### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sy...@chromium.org (2026-02-20)

The analysis is clear and the fix is easy. I've been trying to trigger it in a test though, but it's rather impractical:

- For one, allocating a 4GB image (and then another 4GB image to copy into) is problematic for a lot of the bots.
- In mesa OpenGL drivers, texture sizes > 1GB fail to allocate
- In many Vulkan drivers, `VkPhysicalDeviceMaintenance3Properties::maxMemoryAllocationSize` is less than 4GB
- In D3D drivers, similarly large allocations fail

The only configs I noticed that can actually run the tests are Nvidia/OpenGL drivers and ARM OpenGL and Vulkan drivers. The former is unrelated to this bug, and on the latter (ARM) RGB8 is actually a renderable format so `reinitImageAsRenderable` is never called.

I'll apply a fix, but unfortunately the regression test would be disabled; if it even runs it will cause instability due to large memory consumption.

@reporter, what OS/GPU did you reproduce this on?

### ci...@gmail.com (2026-02-20)

Testing was done on Windows 11 with Intel HD Graphics 620 GPU

### sy...@chromium.org (2026-02-20)

@reporter, Please verify that this CL fixes the issue: <https://chromium-review.googlesource.com/c/angle/angle/+/7595734>

### ci...@gmail.com (2026-02-20)

That change looks good to me; the fix will prevent dstBufferSize from overflowing by ensuring each multiplication group stays within the int32 range.

### dx...@google.com (2026-02-20)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595734>

Vulkan: Avoid overflow in texture size calculation

---


Expand for full commit details
```
     
    Bug: chromium:485622239 
    Change-Id: Idf9847afa0aa2e72b6433ac8348ae2820c1ad8c5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7595734 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `src/tests/gl_tests/VulkanImageTest.cpp`
- M `util/shader_utils.cpp`
- M `util/shader_utils.h`

---

Hash: [a08731cf6d70c60fd74b1d75f2e8b94c52e18140](https://chromiumdash.appspot.com/commit/a08731cf6d70c60fd74b1d75f2e8b94c52e18140)  

Date: Thu Feb 19 19:42:08 2026


---

### dx...@google.com (2026-02-21)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7598213>

Roll ANGLE from 6ebca85fc147 to 360b74f82869 (7 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/6ebca85fc147..360b74f82869 
     
    2026-02-20 syoussefi@chromium.org Revert "PLS: Add usage flags" 
    2026-02-20 bsheedy@chromium.org Remove linux-test Starlark config 
    2026-02-20 bsheedy@chromium.org Promote chromium-luci linux trace to CQ 
    2026-02-20 bsheedy@chromium.org Replace linux-test reference 
    2026-02-20 xwxw@google.com Replace SharedPreferences with Settings.Global as source of truth 
    2026-02-20 syoussefi@chromium.org Vulkan: Avoid overflow in texture size calculation 
    2026-02-20 chris@rive.app PLS: Add usage flags 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,syoussefi@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:485622239 
    Tbr: syoussefi@google.com 
    Change-Id: I05827da1083a1fd7c89548e4639b86917573b08a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7598213 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1588215}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [9ab88f352be2e6aafc25a6bc900c89e455189762](https://chromiumdash.appspot.com/commit/9ab88f352be2e6aafc25a6bc900c89e455189762)  

Date: Sat Feb 21 01:39:58 2026


---

### ch...@google.com (2026-02-21)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1588215) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1588215) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1588215) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sy...@chromium.org (2026-02-24)

1. <https://chromium-review.googlesource.com/7595734>
2. Landed on Feb 20, I haven't heard of complaints
3. No
4. No
5. No

### dr...@chromium.org (2026-02-25)

No crashes seen on Canary, approving merge.

### dx...@google.com (2026-02-26)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613247>

M144: Vulkan: Avoid overflow in texture size calculation

---


Expand for full commit details
```
     
    Bug: chromium:485622239 
    Change-Id: I0dac469a7493196ac25a399310e7ea7046d07162 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7613247 
    Reviewed-by: Cody Northrop <cnorthrop@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`

---

Hash: [a4490148bd3d1b0cb235d9978a52878bd626280f](https://chromiumdash.appspot.com/commit/a4490148bd3d1b0cb235d9978a52878bd626280f)  

Date: Thu Feb 26 15:38:11 2026


---

### dx...@google.com (2026-02-26)

2 changes merged

---

Project: angle/angle  

Branch:  chromium/7632  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613307>

M145: Vulkan: Avoid overflow in texture size calculation

---


Expand for full commit details
```
     
    Bug: chromium:485622239 
    Change-Id: I90f9e9f3315e9cd3023ef2a4b5a1e06e0a30aaef 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7613307 
    Reviewed-by: Cody Northrop <cnorthrop@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`

---

Hash: [2d051d9cef02bca69a97749a995b138e3dec0e1f](https://chromiumdash.appspot.com/commit/2d051d9cef02bca69a97749a995b138e3dec0e1f)  

Date: Thu Feb 26 15:38:11 2026


---


---

Project: angle/angle  

Branch:  chromium/7680  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613327>

M146: Vulkan: Avoid overflow in texture size calculation

---


Expand for full commit details
```
     
    Bug: chromium:485622239 
    Change-Id: I0fda84bde8a2a5e9f5d30449724f7c461112bf0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7613327 
    Reviewed-by: Cody Northrop <cnorthrop@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`

---

Hash: [1d3190bf5633327395d694d621258978d989dffd](https://chromiumdash.appspot.com/commit/1d3190bf5633327395d694d621258978d989dffd)  

Date: Thu Feb 26 15:38:11 2026


---

### sy...@chromium.org (2026-02-26)

Done, done and done

### sp...@google.com (2026-03-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $33000.00 for this report.

Rationale for this decision:
Baseline, Sandbox escape / Memory corruption in a non-sandboxed process + Bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485622239)*
