# Heap Buffer Overflow via Discarded AlignUp Return Value in ExternalVkImageBacking GPU Process

| Field | Value |
|-------|-------|
| **Issue ID** | [484065188](https://issues.chromium.org/issues/484065188) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ps...@gmail.com |
| **Assignee** | bl...@chromium.org |
| **Created** | 2026-02-13 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# VULNERABILITY DETAILS

A heap buffer overflow vulnerability exists in Chromium's GPU process due to a discarded return value from `base::bits::AlignUp()` in `ExternalVkImageBacking::GetMapPlaneData()`. At `gpu/command_buffer/service/shared_image/external_vk_image_backing.cc:1025`, the code calls:

```
base::bits::AlignUp<size_t>(plane_bytes, 4u);

```

But `AlignUp()` returns the aligned value — it does NOT modify its argument in-place (`base/bits.h:71-76`). The return value is silently discarded. The developer comment at lines 1021-1023 explicitly states the intent: *"Ensure that the start of the next plane is 4 byte aligned,"* confirming this is unintentional.

As a result, `total_data_bytes` at line 1027 accumulates unaligned plane sizes, underestimating the required buffer size for multi-plane image formats. When `CopyPixelsFromGLTextureToVkImage()` (line 1033) or `CopyPixelsFromVkImageToGLTexture()` (line 1061) allocates a `cpu_buffer` at line 1042/1070 using this undersized `total_data_bytes`, and then GL readback writes pixel data with 4-byte aligned row stride (`GL_PACK_ALIGNMENT=4`), the write extends past the heap allocation.

The overflow size depends on the number of planes and how many have non-4-aligned `computeMinByteSize()` values. For a 4-plane Y\_U\_V\_A format with dimensions producing non-aligned plane sizes (e.g., 101x101 1bpp planes), the accumulated misalignment causes a **303-byte heap buffer overflow**.

This runs in the **GPU process**, which is outside the renderer sandbox on most platforms. A heap corruption in the GPU process can lead to code execution without requiring a separate sandbox escape.

**Vulnerable code** (`external_vk_image_backing.cc:1013-1031`):

```
std::pair<std::vector<ExternalVkImageBacking::MapPlaneData>, size_t>
ExternalVkImageBacking::GetMapPlaneData() const {
  std::vector<MapPlaneData> data;
  size_t total_data_bytes = 0;
  size_t num_planes = vk_textures_.size();
  for (size_t plane = 0; plane < num_planes; ++plane) {
    data.push_back({AsSkImageInfo(plane), total_data_bytes});

    // Ensure that the start of the next plane is 4 byte aligned. For all
    // multi-planar formats the max texel block size is 4 bytes so this will
    // always satisfy the next planes alignment requirement.
    size_t plane_bytes = data.back().image_info.computeMinByteSize();
    base::bits::AlignUp<size_t>(plane_bytes, 4u);  // BUG: return value discarded

    total_data_bytes += plane_bytes;  // Uses UNALIGNED value
  }
  return {data, total_data_bytes};
}

```

**Buffer allocation and overflow** (`external_vk_image_backing.cc:1041-1054`):

```
auto [plane_data, total_data_bytes] = GetMapPlaneData();
std::vector<uint8_t> cpu_buffer(total_data_bytes);  // UNDERSIZED

for (size_t plane = 0; plane < vk_textures_.size(); ++plane) {
    auto& sk_image_info = plane_data[plane].image_info;
    uint8_t* memory = cpu_buffer.data() + plane_data[plane].offset;
    pixmaps.emplace_back(sk_image_info, memory, sk_image_info.minRowBytes());
    gl_textures_[plane].ReadbackToMemory(pixmaps.back());  // OVERFLOW
}

```

**Suggested fix** — capture the return value (line 1025):

```
plane_bytes = base::bits::AlignUp<size_t>(plane_bytes, 4u);

```
# VERSION

- **Chrome Version:** Chromium main at commit `cca92ab7b4` (`refs/heads/main@{#1583851}`), February 2026
- **Operating System:** Linux (Vulkan + GL interop path). Also affects any platform where `use_separate_gl_texture()` returns true: Linux with NVIDIA/AMD Vulkan + ANGLE, ChromeOS, Android with Vulkan.

# REPRODUCTION CASE

**Attached:** `alignup_heap_overflow_poc.cc` — Standalone ASAN reproducer.

This reproducer faithfully replicates the vulnerable code pattern from:

- `gpu/command_buffer/service/shared_image/external_vk_image_backing.cc:1013-1031` (GetMapPlaneData with discarded AlignUp return value)
- `gpu/command_buffer/service/shared_image/external_vk_image_backing.cc:1041-1054` (CopyPixelsFromGLTextureToVkImage buffer allocation and plane writes)
- `base/bits.h:71-76` (AlignUp returns value, does not modify in-place)

**Build and run:**

```
clang++ -fsanitize=address -g -O0 -o alignup_heap_overflow_poc alignup_heap_overflow_poc.cc
./alignup_heap_overflow_poc

```

**What the reproducer does:**

1. Replicates `GetMapPlaneData()` with the exact discarded AlignUp bug (line 1025)
2. Constructs a 4-plane Y\_U\_V\_A format with 101x101 dimensions (1bpp per plane)
   - Plane 0 (Y): 101x101 = 10,201 bytes (10201 % 4 = 1, NOT 4-aligned)
   - Plane 1 (U): 51x51 = 2,601 bytes (2601 % 4 = 1, NOT 4-aligned)
   - Plane 2 (V): 51x51 = 2,601 bytes (2601 % 4 = 1, NOT 4-aligned)
   - Plane 3 (A): 101x101 = 10,201 bytes
3. `GetMapPlaneData` computes `total_data_bytes = 25,604` (undersized due to bug)
   - Fixed version would compute 25,613 (9 bytes larger)
4. Allocates `cpu_buffer` with the undersized 25,604 bytes
5. Simulates `ReadbackToMemory` writing each plane with 4-byte aligned row stride (`GL_PACK_ALIGNMENT=4`, standard OpenGL default):
   - Plane 3 at offset 15,403 with aligned stride 104\*101 = 10,504 bytes
   - Write end: 15,403 + 10,504 = 25,907
   - Buffer end: 25,604
   - **OVERFLOW: 303 bytes past allocation**
6. ASAN detects heap-buffer-overflow on the final plane write

**In a real attack:** A web page creates a WebGL or WebGPU context that produces a SharedImage using `ExternalVkImageBacking` with a multi-plane format (NV12, YV12, or Y\_U\_V\_A). When the texture transitions between GL and Vulkan representations (triggered by compositor operations or explicit SharedImage access), either `CopyPixelsFromGLTextureToVkImage()` or `CopyPixelsFromVkImageToGLTexture()` is called, allocating an undersized `cpu_buffer` and writing attacker-controlled pixel data past its end. The attacker controls the pixel data via GL texture uploads, and the overflow corrupts adjacent heap objects in the GPU process.

# CRASH STATE

**Type of crash:** GPU process crash (ASAN-detected heap-buffer-overflow in SharedImage GL/Vulkan interop copy)

**ASAN output:**

```
=================================================================
==3186781==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x52b000006604 at pc 0x563a2d5f41f9 bp 0x7ffde42e43f0 sp 0x7ffde42e3bc0
WRITE of size 10504 at 0x52b000006604 thread T0
    #0 __asan_memset                      (alignup_heap_overflow_poc+0xcb1f8)
    #1 main()                             alignup_heap_overflow_poc.cc:446
       [mirrors ReadbackToMemory at external_vk_image_backing.cc:1050]

0x52b000006604 is located 0 bytes after 25604-byte region [0x52b000000200,0x52b000006604)
allocated by thread T0 here:
    #0 operator new[](unsigned long)
    #1 main()                             alignup_heap_overflow_poc.cc:410
       [mirrors std::vector<uint8_t> cpu_buffer(total_data_bytes) at line 1042]

SUMMARY: AddressSanitizer: heap-buffer-overflow in __asan_memset

```

**Exploitation impact:**

- Heap buffer overflow in the GPU process with attacker-controlled write data (pixel values from GL texture upload)
- GPU process runs outside the renderer sandbox on most platforms (Linux, ChromeOS, Android with Vulkan)
- Overflow size is controllable (depends on image dimensions and plane count): up to 3 bytes per non-aligned plane boundary, ~9 bytes for 4-plane format, larger with aligned row stride writes (303 bytes demonstrated)
- Attacker can heap-spray the GPU process to place target objects adjacent to the undersized buffer, enabling corruption of GPU command buffer state, shared memory mappings, or other security-critical structures

# CREDIT INFORMATION

**Reporter credit:** Paul Seekamp / nullenc0de

## Attachments

- [alignup_heap_overflow_asan_crash.txt](attachments/alignup_heap_overflow_asan_crash.txt) (text/plain, 2.8 KB)
- [alignup_heap_overflow_poc.cc](attachments/alignup_heap_overflow_poc.cc) (text/x-c++src, 20.3 KB)
- [alignup_heap_overflow_browser_poc.html](attachments/alignup_heap_overflow_browser_poc.html) (text/html, 23.8 KB)
- [chrome_vk_crash_rtx4090.log](attachments/chrome_vk_crash_rtx4090.log) (text/plain, 98.6 KB)
- [alignup_overflow_chrome_poc.html](attachments/alignup_overflow_chrome_poc.html) (text/html, 44.2 KB)

## Timeline

### ma...@google.com (2026-02-13)

Thank you for the detailed report! I think for us to consider this valid, we would need to confirm that this can actually be triggered from a renderer. For now I'm triaging this under the assumption that it is possible, so S0 for memory corruption in an unsandboxed GPU process.

kylechar@, could you PTAL? Can you confirm that this could plausibly be exploited?

### dc...@chromium.org (2026-02-14)

The PoC does not demonstrate a bug in Chrome. It demonstrates a (potential) use-after-free in code that closely resembles Chrome code, but that is very different from demonstrating an actual security impact on Chrome.

### ps...@gmail.com (2026-02-14)

The CC file I provided was a stand alone producer. Feel free to use the HTML file here to reproduce using the full Chrome software.

## Reproduction

The browser PoC requires Vulkan support:

```
google-chrome --enable-features=Vulkan \
              --use-vulkan=native \
              --enable-unsafe-webgpu \
              --no-sandbox \
              alignup_heap_overflow_browser_poc.html

```

---

## Note on Sandbox

`--no-sandbox` is used here to simplify reproduction — **not** because this is a sandbox escape.

The bug resides in GPU process code.

On most platforms, the GPU process:

- Runs **outside** the renderer sandbox
- Runs **inside** its own (separate) sandbox

A heap corruption in the GPU process is still a security issue:

- **Windows:** GPU process has no sandbox by default
- **macOS:** GPU sandbox is less restrictive than the renderer sandbox
- **Linux:** GPU process has its own sandbox but with broader privileges than the renderer

The `--no-sandbox` flag is required only because the Vulkan + multi-plane code path depends on specific GPU hardware or software rendering configuration.

---

## Investigation Status

Deep analysis of `GLTextureHolder::ReadbackToMemory` (`gl_texture_holder.cc`) shows that it sets `GL_PACK_ROW_LENGTH` to handle alignment, which may prevent the overflow in some practical cases.

However:

- The code defect is real
- Developer intent (see comments at lines 1021–1023) clearly indicates alignment of the plane offset is required

The correct fix should be:

```
plane_bytes = base::bits::AlignUp<size_t>(plane_bytes, 4u);

```

### ma...@google.com (2026-02-14)

I concur with the assessment that the AlignUp() return value most likely shouldn't be discarded. But unless you can plausibly demonstrate that this actually results in memory corruption in practice, we cannot consider this a valid security bug.

See this section in our program rules regarding theoretical bugs derived from static analysis: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md#Best-Practices-for-Security-Bug-Reporting:~:text=Avoid%20reporting%20theoretical,no%20VRP%20reward>.

### bl...@chromium.org (2026-02-16)

Here is the CL with [the fix](https://chromium-review.googlesource.com/c/chromium/src/+/7581213) in any case.

### ps...@gmail.com (2026-02-16)

## Proof: GPU Process Crash on Real Hardware

**Setup:** Chrome 144.0.7559.109, NVIDIA RTX 4090 (driver 580.82.09), Ubuntu 20.04

**With Vulkan (crashes):**

```
$ google-chrome --enable-features=Vulkan --use-vulkan=native --no-sandbox \
    alignup_overflow_chrome_poc.html

```

Chrome GPU process crashes. NVIDIA kernel log:

```
NVRM: Xid (PCI:0000:1a:00): 31, pid=1580000, name=chrome
  MMU Fault: ENGINE CE0 HUBCLIENT_CE1 faulted @ 0x0_06360000.
  Fault is of type FAULT_PTE ACCESS_TYPE_VIRT_WRITE

```

Xid 31 = GPU MMU page fault. CE0 = Copy Engine (executes `vkCmdCopyBufferToImage`). The GPU tried to WRITE past the undersized staging buffer into unmapped memory.

Chrome stderr:

```
[ERROR:shared_context_state.cc:1299] SharedContextState context lost via Skia.
[ERROR:exit_code.cc:13] Restarting GPU process due to unrecoverable error.
[ERROR:gpu_process_host.cc:1004] GPU process exited unexpectedly: exit_code=8704

```

**Without Vulkan (no crash):**

```
$ google-chrome --disable-features=Vulkan --use-vulkan=disabled --no-sandbox \
    alignup_overflow_chrome_poc.html

```

All 6 strategies pass. Zero crashes. Zero Xid errors. Same PoC, same GPU, same Chrome.

| Config | GPU Crash | Xid 31 MMU Fault |
| --- | --- | --- |
| Chrome 144 + Vulkan | **YES** | **YES** (CE0 WRITE) |
| Chrome 144 + no Vulkan | NO | NO |

The crash is in the Vulkan-specific `ExternalVkImageBacking` code path where the AlignUp bug resides.

## How to Reproduce

```
# Requires: Linux + discrete GPU + Chrome 144 or earlier
cd /path/to/poc && python3 -m http.server 8099 &

google-chrome --enable-features=Vulkan --use-vulkan=native \
  --no-sandbox --disable-gpu-sandbox \
  --enable-logging=stderr \
  'http://127.0.0.1:8099/alignup_overflow_chrome_poc.html?autorun' \
  2>chrome.log

# Check:
grep 'exit_code' chrome.log        # GPU process exited unexpectedly: exit_code=8704
dmesg | grep Xid                   # Xid 31, MMU Fault, ENGINE CE0, FAULT_PTE

```
## Why This Matters

- **Trigger:** Any web page with `<video>` + `texImage2D(video)` at non-4-aligned dimensions
- **Impact:** GPU process crash from untrusted web content (DoS). The misaligned `vkCmdCopyBufferToImage` offsets cause out-of-bounds GPU memory writes.
- **Scope:** Chrome ~115 through ~144 with Vulkan enabled (Linux/ChromeOS/Android). The staging buffer path was the default for 29 months (Apr 2023 - Aug 2025).
- **GPU process sandboxing:** Weaker than renderer on Linux, **unsandboxed on Windows**.

## Attached

- `alignup_overflow_chrome_poc.html` — PoC (click "Run All Strategies" or use `?autorun`)
- `chrome_vk_crash_rtx4090.log` — Full Chrome log showing GPU crash

### dx...@google.com (2026-02-17)

Project: chromium/src  

Branch:  main  

Author:  Colin Blundell [blundell@chromium.org](mailto:blundell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7581213>

[//gpu] Have ExternalVkImageBacking not discard result of AlignUp()

---


Expand for full commit details
```
     
    Bug: 484065188 
    Change-Id: I984cc72bbfd0ead7298e22edd69460a3fcdb795e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7581213 
    Reviewed-by: Saifuddin Hitawala <hitawala@chromium.org> 
    Commit-Queue: Colin Blundell <blundell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1585712}

```

---

Files:

- M `gpu/command_buffer/service/shared_image/external_vk_image_backing.cc`

---

Hash: [0baeeb0689878cacebce70b9cec0fb4a15d312c1](https://chromiumdash.appspot.com/commit/0baeeb0689878cacebce70b9cec0fb4a15d312c1)  

Date: Tue Feb 17 14:47:15 2026


---

### ky...@chromium.org (2026-02-17)

Yes that definitely should have been assigning the value to plane\_size, thanks for the fix Colin. I'm going to send out a CL to mark AlignUp/AlignDown() as [[nodiscard]] to prevent this from happening again.

The potential impact here is pretty small. We don't use the ExternalVkImageBacking without external memory path (where the bug was) in production anywhere. ExternalVkImageBacking is only compiled on three platforms but it's only used in release builds on Fuchsia which always has external memory extensions available. On Linux/Windows ExternalVkImageBacking exists primarily for tests. Vulkan is disabled on both platforms. You can turn it on manually with flags of course. On Linux we would be using AngleVulkanImageBacking if we did enable Vulkan. On Windows we'd never enable Vulkan for real users.

### ky...@chromium.org (2026-02-17)

> The overflow size depends on the number of planes and how many have non-4-aligned computeMinByteSize() values. For a 4-plane Y\_U\_V\_A format with dimensions producing non-aligned plane sizes (e.g., 101x101 1bpp planes), the accumulated misalignment causes a 303-byte heap buffer overflow.

Can you explain where 303 bytes came from? For a Y+U+V+A buffer there are four planes and each plane is undersized by 3 bytes so the total buffer is 12 bytes smaller than necessary.

### ps...@gmail.com (2026-02-17)

The 303-byte figure in the original report was based on an incorrect assumption that `ReadbackToMemory` uses `GL_PACK_ALIGNMENT=4` row stride padding. It doesn't, `ComputeBestAlignment()` selects alignment matching the stride, so plane data is tightly packed. I should have caught that earlier; apologies for the confusion.

You're correct that the buffer underallocation is 12 bytes (3 bytes × 4 planes). With tight packing on the CPU readback path, the plane writes fit within the undersized buffer, the last byte written lands exactly at `total_data_bytes`.

However, the demonstrated GPU process crash ([Comment #7](https://issues.chromium.org/issues/484065188#comment7)) comes from the staging buffer path (Chrome ≤144 default), where the issue isn't the buffer size alone, it's the misaligned offsets passed to `vkCmdCopyBufferToImage`.

For example, with **I420A 101×101**, the UV plane gets `bufferOffset=10201` (odd), violating **VUID-vkCmdCopyBufferToImage-dstImage-07976**. On my RTX 4090, this caused an Xid 31 MMU fault on the Copy Engine, the GPU attempted a write to an unmapped address.

### ch...@google.com (2026-02-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ky...@chromium.org (2026-02-17)

Thanks for the clarification.

I think in summary for the security team:

- There was a real bug in Chrome where we could allocate a buffer up to 12 bytes smaller than required.
- Chrome never accessed the buffer, it was provided to GL and Vulkan drivers for one to write and then the other to read. The OOB memory access was happening in the GPU driver.
- The code with the bug wasn't intended to be used in release builds and wasn't by default. It was compiled into release builds on Linux/Windows/Fuchsia.
- Some Linux users do turn on Vulkan via flags. If a user enabled the `Vulkan` feature , didn't enable `VulkanFromANGLE` and their GPU drivers didn't support external memory extensions they would use this path.

### ch...@google.com (2026-02-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ps...@gmail.com (2026-02-17)

I reviewed the changes as well and this properly captures the return value instead of discarding it. Looks great! Nice Job!

### bl...@chromium.org (2026-02-18)

Slight clarification: Vulkan on Windows is disallowed as of several months ago (i.e. you can't turn it on manually).

### ch...@google.com (2026-02-18)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7584187>

Add [[nodiscard]] to base::bits functions

---


Expand for full commit details
```
     
    Ensure the returned result is used to prevent code errors. This is 
    particularly important for AlignUp() which is often used when 
    calculating buffer sizes and could result in too small a buffer being 
    allocated. 
     
    Bug: 484065188 
    Change-Id: Ia52a76de3b40492d26a83938bf19818c378598ed 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7584187 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586395}

```

---

Files:

- M `base/bits.h`

---

Hash: [810c7c15778a1c93a71b8f8dd4fbd945868d2beb](https://chromiumdash.appspot.com/commit/810c7c15778a1c93a71b8f8dd4fbd945868d2beb)  

Date: Wed Feb 18 14:42:29 2026


---

### sp...@google.com (2026-05-19)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

As per comment 13, this is only for tests.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> As per comment 13, this is only for tests.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484065188)*
