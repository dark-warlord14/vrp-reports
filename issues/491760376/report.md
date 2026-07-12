# Integer overflow in ANGLE D3D11 TextureStorage11::setData() leads to heap buffer overflow via WebGL2

| Field | Value |
|-------|-------|
| **Issue ID** | [491760376](https://issues.chromium.org/issues/491760376) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac, Windows |
| **Reporter** | yu...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-11 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

Integer overflow in ANGLE D3D11 backend TextureStorage11::setData() leads to
heap buffer overflow in the GPU process via WebGL2. This vulnerability primarily
affects Chrome on Windows (D3D11 is the default ANGLE backend).

When a WebGL2 texture with RGB32F internal format is uploaded via texSubImage2D,
ANGLE's D3D11 backend converts the source data from RGB to RGBA format. The
destination staging buffer size calculation at TextureStorage11.cpp:910-913 uses
UINT (uint32_t) arithmetic that silently overflows, producing a zero-byte
allocation. The subsequent LoadToNative3To4 call writes up to 4 GB of data into
this zero-byte buffer, causing a heap buffer overflow in the GPU process.

This is triggerable from any web page using WebGL2 JavaScript, with no user
interaction beyond visiting the page. A GPU with >= 4 GB VRAM is required.


ROOT CAUSE

File: third_party/angle/src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp
Function: TextureStorage11::setData()
Lines: 910-913

Vulnerable code:

    UINT bufferRowPitch   = static_cast<unsigned int>(outputPixelSize) * width;
    UINT bufferDepthPitch = bufferRowPitch * height;

    const size_t neededSize = bufferDepthPitch * depth;

Type analysis (C++ usual arithmetic conversions):

  Line 910: bufferRowPitch
    static_cast<unsigned int>(outputPixelSize) * width
    = (unsigned int)16 * (int)16384
    -> unsigned int promotion: 16u * 16384u = 262,144
    Fits in UINT. Correct.

  Line 911: bufferDepthPitch
    bufferRowPitch * height
    = (UINT)262,144 * (int)16384
    -> unsigned int promotion: 262,144u * 16384u = 4,294,967,296
    = 2^32 -> WRAPS TO 0 (defined behavior for unsigned int)

  Line 913: neededSize
    bufferDepthPitch * depth
    = (UINT)0 * (int)1
    -> unsigned int: 0u * 1u = 0
    -> zero-extended to size_t: neededSize = 0

The overflowed neededSize (0) is passed to getScratchMemoryBuffer() at line 920,
which allocates a zero-byte (or minimal) scratch buffer. Then the load function
LoadToNative3To4 at line 921-923 iterates over all 16384*16384 pixels, writing
4 components * sizeof(float) = 16 bytes per pixel using the CORRECT (non-overflowed)
bufferRowPitch of 262,144. This writes 16384 * 262,144 = 4,294,967,296 bytes
(4 GB) to the zero-byte buffer, causing a massive heap buffer overflow.

Key detail: bufferRowPitch (262,144) is correct and does NOT overflow. The load
function uses it to compute write offsets for each row:
  Row 0:     offset 0
  Row 1:     offset 262,144
  Row 16383: offset 4,294,705,152
Each row writes 262,144 bytes. Total written: ~4 GB to a ~0-byte buffer.


TRIGGER PATH (WebGL2 JavaScript -> GPU process heap overflow)

1. Create a TEXTURE_2D with gl.RGB32F internal format at 16384x16384:
   gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGB32F, 16384, 16384);

   On D3D11, ANGLE maps GL_RGB32F to DXGI_FORMAT_R32G32B32A32_FLOAT
   (confirmed in texture_format_map.json: "GL_RGB32F": "R32G32B32A32_FLOAT").
   The D3D11 format has pixelBytes = 16 (128 bits / 8).

2. Upload texture data with RGB/FLOAT format:
   gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, 16384, 16384, gl.RGB, gl.FLOAT, data);

   The source format is RGB FLOAT (12 bytes/pixel). The D3D11 destination
   format is RGBA FLOAT (16 bytes/pixel). The load function
   RGB32F_to_R32G32B32A32_FLOAT(GL_FLOAT) returns:
     LoadToNative3To4<GLfloat, gl::Float32One> with requiresConversion = true
   (confirmed in load_functions_table_autogen.cpp:3189-3194)

3. Since requiresConversion is true, TextureStorage11::setData() takes the
   conversion branch (line 918-924):
   a. Line 908: outputPixelSize = dxgiFormatInfo.pixelBytes = 16
   b. Line 910: bufferRowPitch = 16 * 16384 = 262,144 (fits in UINT)
   c. Line 911: bufferDepthPitch = 262,144 * 16384 = 2^32 -> WRAPS TO 0
   d. Line 913: neededSize = 0 * 1 = 0
   e. Line 920: getScratchMemoryBuffer(context11, 0, &conversionBuffer)
      -> allocates 0-byte (or minimal) scratch buffer
   f. Line 921-923: LoadToNative3To4 writes 4 GB to 0-byte buffer
      -> HEAP BUFFER OVERFLOW


ADDITIONAL OVERFLOW INSTANCES (same pattern)

a) BlitGL.cpp:831-833 - copySubTexture() [OpenGL backend]
   size_t destBufferSize = readPixelsArea.width * readPixelsArea.height *
                           destInternalFormatInfo.pixelBytes;
   Type chain: int * int -> int (268M, fits), then int * GLuint -> unsigned int
   For pixelBytes=16 at 16384x16384: unsigned int overflow to 0.
   Affects Chrome on Linux with native OpenGL (non-Vulkan ANGLE).

b) FrameBufferMtl.mm:82 - CopyTextureSliceLevelToTempBuffer() [Metal backend]
   uint32_t sizeInBytes = width * height * angleFormat.pixelBytes;
   All three operands are uint32_t. For RGBA32F at 16384x16384: overflows to 0.
   Note: Only reachable when copyTextureToBufferForReadOptimization feature is
   enabled, which is restricted to AMD GPUs (DisplayMtl.mm:1265). Not reachable
   on Apple Silicon by default. Triggerable via readPixels on AMD-based Macs.

c) Image11.cpp:428 - copyFromFramebuffer() [D3D11, low exploitability]
   size_t bufferSize = destFormatInfo.pixelBytes * sourceArea.width * sourceArea.height;
   The overflow pattern exists, but exploitability is limited: for RGBA32F (16 bpp),
   the load function RGBA32F_to_R32G32B32A32_FLOAT returns requiresConversion=false
   (load_functions_table_autogen.cpp:3622), so the vulnerable scratch buffer path
   is not taken. For RGB32F, destFormatInfo.pixelBytes=12 (GL-side), which does not
   overflow at 16384x16384. No known exploitable format/type combination found.

None of these use CheckedNumeric or any overflow validation. The D3D11 and
OpenGL instances are independent from the previously reported Vulkan backend
overflow in TextureVk::reinitImageAsRenderable() — different functions,
different trigger paths, different backends.


IMPACT

- Heap buffer overflow in Chrome's GPU process on Windows (D3D11)
- Up to 4 GB of data written to a zero-byte buffer
- The overflow data comes from the LoadToNative3To4 conversion function, which
  copies source texture data (attacker-controlled via texSubImage2D) and adds
  a fourth component (1.0f). Attacker controls 3/4 of the overflow data.
- The GPU process has weaker sandboxing than the renderer process
  (broader syscall allowlist on Windows)
- No user interaction required beyond visiting a malicious web page
- Requires >= 4 GB GPU VRAM (common: GTX 1070+, RTX 2060+, etc.)


AFFECTED PLATFORMS

Primary: Windows with any GPU supporting D3D11 Feature Level 11_0
  - MAX_TEXTURE_SIZE = 16384 on FL 11_0 (all modern GPUs since ~2013)
  - D3D11 is the default ANGLE backend on Windows Chrome
  - Requires >= 4 GB GPU VRAM
  - NVIDIA GTX 1070+ (8 GB), RTX 2060+ (6-24 GB): AFFECTED
  - AMD RX 580+ (8 GB), RX 5600+ (6-16 GB): AFFECTED
  - Intel Arc A380+ (6 GB): AFFECTED
  - GPUs with < 4 GB VRAM: NOT affected (texStorage2D fails with OUT_OF_MEMORY)

Secondary: Linux with ANGLE OpenGL backend (same pattern in BlitGL.cpp)
  - Less common: Linux Chrome defaults to ANGLE Vulkan, not OpenGL

Tertiary: macOS with AMD GPU only (FrameBufferMtl.mm:82)
  - Overflow exists but gated behind copyTextureToBufferForReadOptimization
    feature, enabled only for AMD GPUs (DisplayMtl.mm:1265)
  - Apple Silicon Macs: NOT affected (feature disabled)
  - Intel Macs with AMD dGPU: potentially affected via readPixels path


RELATIONSHIP TO PREVIOUS REPORT

This vulnerability shares the same ROOT CAUSE PATTERN (uint32 overflow in
buffer size calculations using GLuint/UINT types) as the previously reported
TextureVk::reinitImageAsRenderable() overflow in the ANGLE Vulkan backend.
However, the bugs are in completely independent code:

  TextureVk (Vulkan): reinitImageAsRenderable() — format fallback conversion
  TextureStorage11 (D3D11): setData() — texSubImage2D upload conversion

The D3D11 backend was NOT mentioned in the TextureVk report's "additional
overflow instances" list, which only covered Vulkan-specific files
(TextureVk.cpp, vk_helpers.cpp). If the TextureVk fix was scoped to only
the Vulkan backend, these D3D11/OpenGL overflow instances remain unfixed.


SUGGESTED FIX

1. Use checked arithmetic for staging buffer size (TextureStorage11.cpp:910-913):

   angle::CheckedNumeric<UINT> bufferRowPitch =
       angle::CheckedNumeric<UINT>(static_cast<unsigned int>(outputPixelSize)) * width;
   angle::CheckedNumeric<UINT> bufferDepthPitch = bufferRowPitch * height;
   angle::CheckedNumeric<size_t> neededSize =
       angle::CheckedNumeric<size_t>(bufferDepthPitch.ValueOrDie()) * depth;
   if (!bufferRowPitch.IsValid() || !bufferDepthPitch.IsValid() || !neededSize.IsValid()) {
       ANGLE_TRY_HR(context11, E_OUTOFMEMORY, "Integer overflow in buffer size");
   }

2. Fix BlitGL.cpp:831-833:

   angle::CheckedNumeric<size_t> destBufferSize =
       angle::CheckedNumeric<size_t>(readPixelsArea.width) *
       readPixelsArea.height * destInternalFormatInfo.pixelBytes;

3. Fix FrameBufferMtl.mm:82 (defense-in-depth, currently AMD-gated):

   angle::CheckedNumeric<uint32_t> sizeInBytes =
       angle::CheckedNumeric<uint32_t>(width) * height * angleFormat.pixelBytes;

4. Fix Image11.cpp:428 (defense-in-depth, no known exploitable path):

   angle::CheckedNumeric<size_t> bufferSize =
       angle::CheckedNumeric<size_t>(destFormatInfo.pixelBytes) *
       sourceArea.width * sourceArea.height;


VERSION

Chrome Version: 147.0.7682.0 (dev)
Operating System: Windows 10/11 with D3D11 Feature Level 11_0 GPU (>= 4 GB VRAM)
ANGLE Backend: D3D11 (Windows default)


REPRODUCTION CASE

Prerequisites:
- Windows system with GPU having >= 4 GB VRAM
- Chrome using D3D11 ANGLE backend (default on Windows)
- GPU MAX_TEXTURE_SIZE >= 16384 (all D3D11 FL11_0 GPUs)

Steps:
1. Serve poc.html locally:
     python -m http.server 8080

2. Open Chrome on Windows:
     chrome.exe http://localhost:8080/poc.html

3. Click "Check Environment" to verify:
   - WebGL2 is available with D3D11 backend
   - MAX_TEXTURE_SIZE >= 16384
   - RGB32F requires format conversion (estimated by checking GL_RENDERER)

4. Click "Run PoC" to trigger the overflow:
   - Expected: GPU process crashes, WebGL context is lost

For ASAN builds (recommended for clear crash report):
  gn gen out/asan --args='
    is_asan = true
    is_debug = false
    is_component_build = false
    dcheck_always_on = true
    target_cpu = "x64"
    angle_enable_d3d11 = true
  '
  autoninja -C out/asan chrome
  out/asan/chrome.exe --no-sandbox --disable-gpu-sandbox ^
    http://localhost:8080/poc.html

Expected ASAN output:
  ==GPU_PID==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...
  WRITE of size ... at 0x... thread T...
      #0 in LoadToNative3To4Impl<float>(...)
      #1 in LoadToNative3To4<float, ...>(...)
      #2 in rx::TextureStorage11::setData(...)

Standalone arithmetic verification (no GPU required):
  cl /Fe:verify_overflow.exe verify_overflow.c && verify_overflow.exe
  (or: cc -o verify_overflow verify_overflow.c && ./verify_overflow)
  This confirms the integer overflow using the exact C++ type promotion rules.


FOR CRASHES

Type of crash: GPU process crash (not tab, not browser)
Crash state:

  Expected crash stack:
    LoadToNative3To4Impl<float>(...)                    <- writes 4 GB to 0-byte buffer
    LoadToNative3To4<float, gl::Float32One>(...)        <- loadimage.inc:88-102
    rx::TextureStorage11::setData(...)                  <- TextureStorage11.cpp:921
    rx::TextureD3D_2D::setSubImage(...)
    gl::Texture::setSubImage(...)

  Root cause frame: TextureStorage11.cpp:910-911
    UINT bufferRowPitch   = static_cast<unsigned int>(outputPixelSize) * width;
    UINT bufferDepthPitch = bufferRowPitch * height;
    // bufferDepthPitch = 262,144 * 16,384 = 2^32 -> 0

  Allocation frame: TextureStorage11.cpp:920
    getScratchMemoryBuffer(context11, neededSize=0, &conversionBuffer)
    // Allocates 0-byte (or minimal) scratch buffer

  Overflow frame: TextureStorage11.cpp:921-923
    loadFunctionInfo.loadFunction(... width=16384, height=16384, depth=1,
                                  ... conversionBuffer->data(),
                                  bufferRowPitch=262144, bufferDepthPitch=0);
    // LoadToNative3To4 writes 16384*16384*16 = 4,294,967,296 bytes to 0-byte buffer

  The GPU process will crash with access violation (release build) or report
  heap-buffer-overflow (ASAN build). In a release build, the GPU process
  restarts and the WebGL context is reported as lost.


ATTACHED FILES

1. poc.html                - Self-contained WebGL2 PoC with environment check
2. verify_overflow.c  - Standalone C program proving the integer overflow
                                     (reproduces exact C++ type promotion chain)


CREDIT INFORMATION
Reporter credit: heesun

## Attachments

- [poc.html](attachments/poc.html) (text/html, 10.8 KB)
- [verify_overflow.c](attachments/verify_overflow.c) (text/x-csrc, 4.4 KB)

## Timeline

### ch...@google.com (2026-03-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-13)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-26)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7695232>

D3D11: Protect against overflows for texture staging buffers

---


Expand for full commit details
```
     
    When TextureStorage11 needs to calculate sizes of intermediate buffers 
    for data conversion, do the math in 64-bit using CheckedNumerics. 
    Validate that the results fit into 32 bits. 
     
    Bug: chromium:491760376 
    Change-Id: Ie5942291fe7790c229cb1070fa9a2325fa40ac2f 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7695232 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/d3d/d3d11/TextureStorage11.cpp`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [88ff9f4e6924c230bc924ab7dd9ab1f78068bf12](https://chromiumdash.appspot.com/commit/88ff9f4e6924c230bc924ab7dd9ab1f78068bf12)  

Date: Mon Mar 23 21:32:05 2026


---

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7705721>

Roll ANGLE from 47db665315a7 to 353f6fe8e3f3 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/47db665315a7..353f6fe8e3f3 
     
    2026-03-26 mattiass@google.com Vulkan: Invalidate sampler if any YCbCr parameter changes 
    2026-03-26 geofflang@chromium.org D3D11: Protect against overflows for texture staging buffers 
    2026-03-26 nuskos@chromium.org Use CheckedNumeric for size calculation in TextureGL. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:491760376 
    Tbr: yuxinhu@google.com 
    Test: Test: Google Meet 
    Test: Test: dEQP-EGL* 
    Test: Test: dEQP-GL* 
    Change-Id: I14124ab5a3299c3fdc705589c2cb6bc809f0349f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705721 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1605722}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [38da1fe02ebb29f4f9bd47608207f4a28865ebce](https://chromiumdash.appspot.com/commit/38da1fe02ebb29f4f9bd47608207f4a28865ebce)  

Date: Thu Mar 26 19:49:58 2026


---

### ch...@google.com (2026-04-01)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1605722) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1605722) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-04-01)

No crashes in Canary. Approved to merge to M147. We don't plan any more M146 releases, so removing that request.

### ch...@google.com (2026-04-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### yu...@gmail.com (2026-04-16)

deleted

### yu...@gmail.com (2026-04-22)

Following up - it looks like the merge to M147 was approved on April 2 but hasn't landed yet. Could the cherry-pick be completed so this fix reaches users in the next point release?

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline (no ASAN trace). Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491760376)*
