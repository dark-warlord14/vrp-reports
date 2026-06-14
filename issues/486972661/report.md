# Heap buffer overflow in ANGLE copyImageDataToBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [486972661](https://issues.chromium.org/issues/486972661) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | oj...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2026-02-23 |
| **Bounty** | $15,000.00 |

## Description

---

### Report description

Heap buffer overflow in ANGLE copyImageDataToBuffer

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium>

---

### The problem

#### Please describe the technical details of the vulnerability

## Description

Commit [`a08731cf`](https://chromium-review.googlesource.com/c/angle/angle/+/7595734) (Bug: chromium:485622239) fixed a 32-bit integer overflow in the destination buffer size calculation in `TextureVk::reinitImageAsRenderable()` at [`TextureVk.cpp:3170`](https://github.com/google/angle/blob/main/src/libANGLE/renderer/vulkan/TextureVk.cpp#L3170) by splitting the multiplication into two stages with `static_assert` guards.

That same function also calls `ImageHelper::copyImageDataToBuffer()` at [`TextureVk.cpp:3155`](https://github.com/google/angle/blob/main/src/libANGLE/renderer/vulkan/TextureVk.cpp#L3155), which does its own staging buffer allocation with the same kind of unchecked 32-bit multiply at [`vk_helpers.cpp:10788`](https://github.com/google/angle/blob/main/src/libANGLE/renderer/vulkan/vk_helpers.cpp#L10788):

```
uint32_t pixelBytes = imageFormat.pixelBytes;
size_t bufferSize =
    sourceArea.width * sourceArea.height * sourceArea.depth * pixelBytes * layerCount;

```

Every operand here is 32-bit (`int` or `uint32_t`), so the product wraps before it gets assigned to the 64-bit `size_t`. When the true result hits 2^32 the value becomes zero, a zero-byte staging buffer gets allocated, and the following `vkCmdCopyImageToBuffer` writes the full image data into it, overflowing the heap.

In short: the fix patched the destination buffer (caller) but missed the source buffer (callee).

## Steps to Reproduce

Tested on Windows 11 with Chrome 145 Stable. The PoC allocates a 4 GiB texture, so the Vulkan driver must support a single allocation of that size. Most discrete GPUs (e.g. NVIDIA RTX 4050, 6 GB VRAM) cap `maxMemoryAllocationSize` just under 4 GiB, causing `texStorage3D` to return `GL_OUT_OF_MEMORY` before the vulnerable path is reached. On laptops with an Intel Iris Xe iGPU, the Vulkan driver allocates from system RAM and supports allocations up to ~16 GiB, which is enough.

1. Place `poc.html` in a directory and start a local web server (PowerShell):

```
cd path\to\poc
python -m http.server 8765

```

2. Open a second PowerShell window. Force Chrome to use the Intel Vulkan driver and launch with logging to file:

```
$env:VK_ICD_FILENAMES = "C:\Windows\System32\DriverStore\FileRepository\iigd_dch.inf_amd64_9741ef1f4093481f\igvk64.json"

New-Item -ItemType Directory -Force "$env:TEMP\chrome-vulkan-test" | Out-Null

& "C:\Program Files\Google\Chrome\Application\chrome.exe" --use-angle=vulkan --disable-gpu-sandbox --no-sandbox --user-data-dir="$env:TEMP\chrome-vulkan-test" --no-first-run --enable-logging --log-file="$env:TEMP\chrome-vulkan-test\chrome.log" http://localhost:8765/poc.html

```

The `VK_ICD_FILENAMES` path is for the Intel driver on the test system. On other machines, find it under `C:\Windows\System32\DriverStore\FileRepository\iigd_dch.inf_amd64_*\igvk64.json`.

3. The page will go blank within a few seconds (GPU process crash). Wait ~10 seconds, then check the log:

```
Select-String "GPU process exited unexpectedly" "$env:TEMP\chrome-vulkan-test\chrome.log"

```

Expected output:

```
[ERROR:gpu_process_host.cc:996] GPU process exited unexpectedly: exit_code=-1073741819

```

`-1073741819` is `0xC0000005` (`STATUS_ACCESS_VIOLATION`).

4. Crashpad also writes a minidump to the user-data-dir:

```
ls "$env:TEMP\chrome-vulkan-test\Crashpad\reports\*.dmp"

```

Minidump from test system:

```
ExceptionCode:  EXCEPTION_ACCESS_VIOLATION (0xC0000005)
Access type:    WRITE
Faulting addr:  libglesv2.dll + 0x0044A120
Write target:   0x1B1D28C0000 (unmapped, past end of staging buffer)

```

**What the PoC does:** it creates a `TEXTURE_2D_ARRAY` (RGB8, 2048x2048, 256 layers). ANGLE stores RGB8 as RGBA8 (4 bytes/pixel) on Vulkan since RGB8 is not natively renderable. Attaching layer 0 to an FBO and calling `gl.clear()` forces `reinitImageAsRenderable`, which calls `copyImageDataToBuffer`. The buffer size wraps: `2048 * 2048 * 1 * 4 * 256 = 2^32 = 0`.

### Control tests

| Test | Result |
| --- | --- |
| `poc.html` (2048x2048x256, overflows) | GPU crash, `exit_code=-1073741819` |
| `about:blank` (no WebGL) | No crash |
| `poc_safe.html` (256x256x4, no overflow) | No crash |

## Root Cause

Looking at the [commit diff](https://github.com/google/angle/commit/a08731cf6d70c60fd74b1d75f2e8b94c52e18140), the fix only touches `TextureVk.cpp` (the destination buffer allocation). `ImageHelper::copyImageDataToBuffer` in `vk_helpers.cpp` (the source buffer allocation) was left as-is and still does the whole multiplication in one 32-bit expression.

## GPU memory note

The PoC needs a single Vulkan allocation of exactly 4 GiB (2^32 bytes). Many discrete GPUs cap `maxMemoryAllocationSize` just below that (the RTX 4050 caps at `0xffe00000`, ~2 MiB short). The Intel Iris Xe iGPU allocates from system RAM with a limit of ~16 GiB, so it works on any machine with enough free RAM. On Linux or systems without an Intel iGPU, lowering `IMPLEMENTATION_MAX_2D_TEXTURE_SIZE` in `src/libANGLE/Constants.h` to 256 and rebuilding ANGLE makes the overflow trigger with only a few hundred KiB.

#### Impact analysis

A web page can cause a heap buffer overflow in Chrome's GPU process through WebGL 2. The data written past the buffer comes from texture contents, which the page controls through `texSubImage3D`. The GPU process runs at higher privilege than the renderer.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome 145.0.7632.110 Stable, Windows 11 x86\_64

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [chrome.log](attachments/chrome.log) (application/octet-stream, 4.2 KB)
- [58b59575-d88b-48fd-87dc-85302ab44e63.dmp](attachments/58b59575-d88b-48fd-87dc-85302ab44e63.dmp) (application/octet-stream, 835.9 KB)
- [poc_safe.html](attachments/poc_safe.html) (text/html, 1.0 KB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [ad684400-7aeb-4f88-9a00-9e67c9df44c7.dmp](attachments/ad684400-7aeb-4f88-9a00-9e67c9df44c7.dmp) (application/octet-stream, 860.1 KB)
- [controlled_write.html](attachments/controlled_write.html) (text/html, 1.9 KB)
- [parse_dump.py](attachments/parse_dump.py) (text/x-python, 3.6 KB)

## Timeline

### oj...@gmail.com (2026-02-24)

Follow-up: the overflow writes attacker-controlled data, not just uninitialized memory.

I made a second PoC (`controlled_write.html`) that fills the texture with known bytes before triggering the overflow. Layer 0 gets 0x41 via `texSubImage3D`, layer 1 gets 0x42. ANGLE stores RGB8 as RGBA8, so each pixel is `[0x41, 0x41, 0x41, 0xFF]` = dword `0xFF414141`.

The PoC also sprays 64 MiB of WebGL ARRAY\_BUFFERs filled with `0xDEADBEEF` before triggering. On UMA (Intel iGPU) these end up in the same VMA heap as the staging buffer, so the overflow runs through them.

**Steps to reproduce** (PowerShell, same setup as before):

1. Kill any running Chrome, clean old profile:

```
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:TEMP\chrome-vulkan-test" -ErrorAction SilentlyContinue

```

2. Serve `controlled_write.html`:

```
python -m http.server 8765

```

3. In a second PowerShell window, launch Chrome on the Intel Vulkan driver:

```
$env:VK_ICD_FILENAMES = "C:\Windows\System32\DriverStore\FileRepository\iigd_dch.inf_amd64_9741ef1f4093481f\igvk64.json"

& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --use-angle=vulkan --disable-gpu-sandbox --no-sandbox `
  --user-data-dir="$env:TEMP\chrome-vulkan-test" --no-first-run `
  --enable-logging --log-file="$env:TEMP\chrome-vulkan-test\chrome.log" `
  http://localhost:8765/controlled_write.html

```

(The `VK_ICD_FILENAMES` path is machine-specific. Find yours with: `dir C:\Windows\System32\DriverStore\FileRepository\iigd_dch.inf_amd64_*\igvk64.json`)

4. Wait ~15 seconds for the GPU process crash, then check the log:

```
Select-String "GPU process exited unexpectedly" "$env:TEMP\chrome-vulkan-test\chrome.log"

```

Expected: `exit_code=-1073741819` (0xC0000005, STATUS\_ACCESS\_VIOLATION).

5. Parse the minidump (`pip install minidump`):

```
$dmp = (Get-ChildItem "$env:TEMP\chrome-vulkan-test\Crashpad\reports\*.dmp").FullName
python parse_dump.py $dmp

```

**Output from my test** (addresses vary per run, the rest is stable):

```
Exception:    WRITE AV at 0x000002A14C960000
RAX:          0x0000000000000041  << attacker byte (0x41)
RIP:          libglesv2.dll+0x44A120

  0x000002A14B180000   23.9 MiB  MEM_COMMIT  PAGE_READWRITE
  0x000002A14C960000    8.1 MiB  MEM_RESERVE  NONE  << CRASH
Overflow reached end of 23.9 MiB committed block

0xFF414141 first seen at 0x000002A14C95FF80
0xFF414141 total:  32 dwords in captured memory

Last 128 bytes before crash address:
  0x02A14C95FF80: 41 41 41 FF 41 41 41 FF 41 41 41 FF 41 41 41 FF  AAA.AAA.AAA.AAA.
  0x02A14C95FF90: 41 41 41 FF 41 41 41 FF 41 41 41 FF 41 41 41 FF  AAA.AAA.AAA.AAA.
  0x02A14C95FFA0: 41 41 41 FF 41 41 41 FF 41 41 41 FF 41 41 41 FF  AAA.AAA.AAA.AAA.
  0x02A14C95FFB0: 41 41 41 FF 41 41 41 FF 41 41 41 FF 41 41 41 FF  AAA.AAA.AAA.AAA.
  ... (128 bytes total, all 41 41 41 FF)

```

RAX=0x41 at crash, so the CPU was writing our byte. The 128 bytes captured right before the crash address are all `41 41 41 FF`. That's our texture data past the staging buffer. The overflow went through ~24 MiB of committed VMA memory before hitting the unmapped page.

The overflow is always 4 GiB (staging buffer wraps to ~0, GPU copies the whole image), so not a precision write, but it does corrupt everything in the VMA block with content the page chose via `texSubImage3D`.

Attached: `controlled_write.html`, `parse_dump.py`

### ch...@google.com (2026-02-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sy...@chromium.org (2026-02-24)

@ab...@google.com would you mind giving me a hand with this? Fixing the bug itself is trivial, it'd be similar to <https://chromium-review.googlesource.com/c/angle/angle/+/7595734>.

But we need two additional things to do:

1. Audit the code as much as possible, see if there are other cases where we're multiplying width \* height \* depth \* layers.
2. In a follow up, we should introduce a limit like described in [issue 485900022](https://issues.chromium.org/issues/485900022) that prevents large memory allocations in the first place, like practically all drivers already do, so that problems like this cannot arise.

### ab...@google.com (2026-02-24)

Hello,

Sounds good! I will look into it.

Thanks.

### dx...@google.com (2026-03-02)

Project: angle/angle  

Branch:  main  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7615650>

Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [4de47461e45248eeaf8fd0ef04ca3949f98029da](https://chromiumdash.appspot.com/commit/4de47461e45248eeaf8fd0ef04ca3949f98029da)  

Date: Thu Feb 26 23:17:40 2026


---

### ab...@google.com (2026-03-02)

Hello,

In [the change above](https://crrev.com/c/7615650), the allocation size for a single device memory on the Vulkan backend has been limited to 1GB (or the reported max size from the driver, whichever is smaller), which should make overflow in the size calculations across the Vulkan backend code less likely.

In addition, in the size calculations in the functions `TextureVk::reinitImageAsRenderable()` and `ImageHelper::copyImageDataToBuffer()`, the dimension operands have been casted to `size_t` to avoid overflow.

This change should resolve the heap overflow issue described at the top. (Unfortunately I was unable to reliably reproduce the issue locally.)

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7623972>

Roll ANGLE from 425ea1de41aa to 71f8079e12be (5 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/425ea1de41aa..71f8079e12be 
     
    2026-03-02 cclao@google.com Vulkan: Only dirty flipXY when it changed. 
    2026-03-02 lexa.knyazev@gmail.com Update GetTexLevelParameter* and multisample texture ANGLE specs 
    2026-03-02 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 7d6f99b1bd5d to 0b8ee538955f (934 revisions) 
    2026-03-02 ynovikov@chromium.org Promote angle_deqp_egl_vulkan_tests skip to Stable 
    2026-03-02 abdolrashidi@google.com Vulkan: Cap memory allocation size to 1GB 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,ynovikov@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:486972661,chromium:487208468 
    Tbr: ynovikov@google.com 
    Change-Id: I7e767625d9a0f7b69fa3f23702acb6e161be57cd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623972 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1592814}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [379e51beedc724b45efe1b5d03102a3365244d2b](https://chromiumdash.appspot.com/commit/379e51beedc724b45efe1b5d03102a3365244d2b)  

Date: Tue Mar 3 00:13:45 2026


---

### ab...@google.com (2026-03-04)

Since this change has rolled into Chromium, I will mark this issue as closed.

However, please feel free to re-open in case of further questions or concerns.

### ch...@google.com (2026-03-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-05)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1592814) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1592814) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ab...@google.com (2026-03-05)

Hello,

Regarding [comment #13](https://issues.chromium.org/issues/486972661#comment13):

1. The fix CL: <https://chromium-review.git.corp.google.com/c/angle/angle/+/7615650>
2. Yes. The change is already merged to main and rolled in Chromium.
3. No
4. No
5. No, security fix tests are automated.

### dr...@chromium.org (2026-03-07)

Thanks, approved to merge to M146. We don't plan any more M145 releases, so removing that label.

### dx...@google.com (2026-03-09)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7648876>

[M146] Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    (cherry picked from commit 4de47461e45248eeaf8fd0ef04ca3949f98029da) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7648876 
    Reviewed-by: Yuly Novikov <ynovikov@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [1a72ef5e089e464fefae8b89922060bdbc5a5d2d](https://chromiumdash.appspot.com/commit/1a72ef5e089e464fefae8b89922060bdbc5a5d2d)  

Date: Thu Feb 26 23:17:40 2026


---

### ab...@google.com (2026-03-09)

Thank you. The change has now merged to M146.

### pe...@google.com (2026-03-20)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ab...@google.com (2026-03-20)

Hello,

Regarding [comment #18](https://issues.chromium.org/issues/486972661#comment18):

1. No
2. No

### qk...@google.com (2026-03-27)

Labled 'LTS-NotApplicable-138' because M138 didn't have the suspected CL[1].

[1] https://chromium-review.git.corp.google.com/c/angle/angle/+/7595734

### pe...@google.com (2026-03-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-27)

1. https://chromium-review.git.corp.google.com/c/angle/angle/+/7691581
2. Low - there was a few conflict.
3. 146.
4. Yes, because the suspected CL[1] was merged into M144 partially[2]. But the merged code looked like the root cause of the bug.

[1] https://chromium-review.git.corp.google.com/c/angle/angle/+/7595734
[2] https://chromium-review.googlesource.com/c/angle/angle/+/7613247

### an...@google.com (2026-03-30)

Merge approved for LTS-144

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
High Quality. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### oj...@gmail.com (2026-04-01)

Thank you to the team for the quick triage, the thorough fix, and for running a program that makes this kind of work worthwhile. Looking forward to the public disclosure window.

And if there's ever a spot on the team, you know where to find me. 😊

### dx...@google.com (2026-04-16)

Project: angle/angle  

Branch:  chromium/7559  

Author:  Amirali Abdolrashidi [abdolrashidi@google.com](mailto:abdolrashidi@google.com)  

Link:    <https://chromium-review.googlesource.com/7691581>

[M144-LTS] Vulkan: Cap memory allocation size to 1GB

---


Expand for full commit details
```
     
      Currently the maximum memory allocation size for a single object 
    can be inquired from the Vulkan driver via KHR_maintenance3 (promoted 
    to core in Vulkan 1.1). However, the reported limit can still be quite 
    large for common usage. In addition, it can increase the risk of memory 
    size calculations overflowing if the operands are not 64 bits. As an 
    example, if the limit is 4GB and an image is defined with 32-bit dims 
    and format that theoretically require 4GB, the multiplication of these 
    values can result in overflow, even if it is to be assigned to a 64-bit 
    value. 
      * (One way to avoid such overflow cases is to split multiplication 
        into several steps, e.g., CL:7595734) 
     
    This change aims to reduce the maximum size allowed for allocation in 
    order to reduce the risk of such overflow issues. 
     
    * Added kMemoryAllocationSizeLimit to vk_renderer. 
      * Currently set to 1GB. 
     
    * Added to vk::Renderer: mMaxMemoryAllocationSize 
      * Set to the minimum of kMemoryAllocationSizeLimit and 
        the maxMemoryAllocationSize reported from the driver. 
     
    * Cast the values used in some buffer size calculations to 
      size_t. 
      * (The leftmost value being size_t should be enough to propagate 
        this type for the result of each multiplication.) 
     
    * Updated the following test to use a smaller width and height to 
      avoid error due to the new cap: 
      TextureCubeTestES32.MaxArrayTextureLayersVerify 
     
    Bug: chromium:486972661 
    Bug: chromium:487208468 
    Change-Id: I98bde71ede153324f524bb579b19043a474823d5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7615650 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    (cherry picked from commit 4de47461e45248eeaf8fd0ef04ca3949f98029da) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7691581 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>

```

---

Files:

- M `src/libANGLE/renderer/vulkan/TextureVk.cpp`
- M `src/libANGLE/renderer/vulkan/vk_helpers.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.cpp`
- M `src/libANGLE/renderer/vulkan/vk_renderer.h`
- M `src/tests/gl_tests/TextureTest.cpp`

---

Hash: [f56543421c45455f1c5d746a4d84ebe0549da745](https://chromiumdash.appspot.com/commit/f56543421c45455f1c5d746a4d84ebe0549da745)  

Date: Thu Feb 26 23:17:40 2026


---

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486972661)*
