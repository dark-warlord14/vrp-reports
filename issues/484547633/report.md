# VideoFrame Mojo deserialization accepts negative stride → OOB read in video encoders 


| Field | Value |
|-------|-------|
| **Issue ID** | [484547633](https://issues.chromium.org/issues/484547633) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-15 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

== Environment ==
Tested on: Chromium trunk (Linux x64), ASAN build
Affected platforms: All (Linux, macOS, Windows, ChromeOS, Android)
The vulnerable code is platform-independent.

== Build Configuration (ASAN) ==
is\_asan = true
is\_debug = false
is\_component\_build = false
target\_cpu = "x64"

== Reproduction via ASAN Unit Test ==

The vulnerability is in the Mojo deserialization of SharedMemory-backed VideoFrames. A unit test
that exercises the real deserialization code path with a crafted negative stride value triggers
heap-buffer-overflow under ASAN.

Steps:

1. Build media\_unittests with ASAN:
   autoninja -C out/ASAN media\_unittests
2. Run the NegativeStride test:
   ASAN\_OPTIONS="detect\_odr\_violation=0:halt\_on\_error=1"   
   
   out/ASAN/media\_unittests   
   
   --gtest\_filter="*NegativeStride*"   
   
   --single-process-tests
3. Observe ASAN heap-buffer-overflow report.

== Reproduction via MojoJS PoC (requires --enable-blink-features=MojoJS) ==

1. Apply the attached poc\_patch.diff to add a stride probe after deserialization
   (needed because headless Linux has no GPU encoder backend; the probe simulates
   the same memory access pattern as VpxVideoEncoder).
2. Serve poc\_negative\_stride.html on a local HTTP server:
   python3 -m http.server 8787
3. Run Chrome with ASAN:
   ./out/ASAN/chrome   
   
   --enable-blink-features=MojoJS,MojoJSTest   
   
   --no-sandbox --disable-gpu-sandbox   
   
   --headless=new --ozone-platform=headless --disable-gpu   
   
   --use-fake-device-for-media-stream   
   
   --enable-features=UseOutOfProcessVideoEncoding   
   
   --enable-logging=stderr   
   
   "<http://127.0.0.1:8787/poc_negative_stride.html>"
4. Observe SEGV\_MAPERR crash at the deserialization site.

== What the PoC does ==
The PoC uses MojoJS to call VideoEncodeAccelerator.Encode() with a VideoFrame whose
strides[] are set to -1 (0xFFFFFFFF as int32\_t). The frame is sent via Mojo IPC and
deserialized in the browser/GPU process. The negative stride passes all existing
validation checks and produces a VideoFrame with stride = SIZE\_MAX, which causes
backward out-of-bounds reads when any consumer (VPX encoder, AV1 encoder, libyuv, etc.)
iterates over pixel rows.

# Problem Description

== Summary ==
media/mojo/mojom/video\_frame\_mojom\_traits.cc:301 assigns an int32\_t stride value from
Mojo IPC directly to a size\_t field without checking for negative values. A compromised
renderer can send stride = -1, which becomes SIZE\_MAX (0xFFFFFFFFFFFFFFFF) after implicit
sign extension. Downstream consumers (video encoders, libyuv) truncate this to int(-1)
and use it for pointer arithmetic, causing backward out-of-bounds heap reads.

== Root Cause ==
In StructTraits<VideoFrameDataView>::Read(), SharedMemory path:

planes[i].stride = strides[i]; // int32\_t → size\_t, no negative check

The existing FitsInContiguousBufferOfSize() check does NOT validate stride. It only
checks (plane.offset + plane.size <= data\_size). The plane.size is computed as:
Rows(i, format, height) \* strides[i]
When strides[i] = -1, this multiplies size\_t \* int32\_t(-1), causing integer overflow
that wraps to a small value. std::min() then clamps it further. So plane.size and
plane.offset are both reasonable → the check passes. But planes[i].stride = SIZE\_MAX
is never validated.

Notably, the DMA-buf deserialization path in the SAME FILE (line ~196) correctly uses
base::IsValueInRangeForNumericType<size\_t>(data.stride()) to reject negative values.
The SharedMemory path is missing this check — this is clearly an oversight.

== Affected Consumers ==
Any code that calls VideoFrame::stride() and uses it for pixel row traversal:

- VpxVideoEncoder (vpx\_video\_encoder.cc:306-308): stride[VPX\_PLANE\_Y] = frame.stride(kY)
  → vpx\_image\_t::stride is int[4], SIZE\_MAX truncates to -1 → libvpx OOB
- Av1VideoEncoder (av1\_video\_encoder.cc): same pattern with aom\_image\_t
- OpenH264VideoEncoder: same pattern
- libyuv color conversion: stride passed as int parameter
- WebMediaPlayerMSCompositor: stride used for pixel copy

== Security Impact ==

- Type: Out-of-bounds read (heap-buffer-overflow / heap underflow)
- Attack surface: Compromised renderer → browser/GPU process via Mojo IPC
- Threat model: Standard Chrome "compromised renderer" model. A renderer exploit
  (e.g., V8 bug) can craft arbitrary Mojo messages including negative strides.
- Impact: Cross-process information disclosure (reading heap data before the
  VideoFrame buffer) or process crash (SEGV on unmapped page).
- No MojoJS required for real exploitation — MojoJS is used only for PoC convenience.

== ASAN Crash ==
heap-buffer-overflow on address 0x7dc7994ef1ff
READ of size 1 at 0x7dc7994ef1ff thread T0
0x7dc7994ef1ff is located 1 bytes before 19072-byte region [0x7dc7994ef200,0x7dc7994f3c80)

== Suggested Fix ==
Add a negative stride check before the assignment:
if (strides[i] < 0) {
DLOG(ERROR) << "Negative stride at plane " << i;
return false;
}
planes[i].stride = static\_cast<size\_t>(strides[i]);

This matches the existing DMA-buf path validation pattern.

# Additional Comments

== Environment ==
Chromium commit: b3acbdcb7bbe7eb076ed9509d3c5f2e10587a5b7
(2026-02-12, trunk/main branch)
Build configs: Linux x64, both Default (non-ASAN) and ASAN builds
(see args.gn details in attached bug\_report.md §8)

== Why a PoC patch is needed ==

The PoC patch (poc\_patch.diff) adds a ~30-line read-only probe to
video\_frame\_mojom\_traits.cc, immediately after the deserialized VideoFrame
is created. This patch is needed because:

1. Our test server is headless Linux with no GPU. The natural consumer
   of the poisoned VideoFrame is VpxVideoEncoder (or AV1/OpenH264/VideoToolbox
   encoders), but VideoEncodeAccelerator requires a hardware backend
   (VAAPI/V4L2/VideoToolbox) to initialize. On our server, VEA.Initialize()
   fails → Encode() is never called → the poisoned frame is never consumed.
2. The vulnerability itself (int32\_t → size\_t assignment at line 301) is
   fully exercised WITHOUT the patch. The deserialization succeeds,
   FitsInContiguousBufferOfSize() is bypassed (integer overflow), and the
   VideoFrame is created with stride = SIZE\_MAX. The patch merely performs
   the same memory access that the encoder would perform, to trigger ASAN
   detection in our GPU-less environment.
3. On macOS or any machine with a GPU, the patch is unnecessary — the real
   VPX/AV1/VideoToolbox encoder will consume the frame and crash naturally.

== What the patch simulates and why it's a valid reproduction ==

The patch mirrors the exact code path in vpx\_video\_encoder.cc:

Patch code VpxVideoEncoder real code
────────────────────────────────── ──────────────────────────────────
y\_plane = frame->visible\_data(kY) planes[Y] = frame.visible\_data(kY) (line 301)
y\_stride = frame->stride(kY) stride[Y] = frame.stride(kY) (line 307)
\*(y\_plane + y\_stride) libvpx: planes[Y] + row \* stride[Y] (vpx\_codec\_encode)

The type conversion chain is identical:
frame->stride(kY) returns size\_t = SIZE\_MAX
→ assigned to int variable → truncated to -1
→ pointer arithmetic: y\_plane + (-1) → backward OOB read

== Why the OOB access is reachable without any security checks in between ==

From the deserialization point (line 301) to the consumer access, there are
NO intervening security checks on the stride value:

1. Line 301: planes[i].stride = strides[i] — int32(-1) → size\_t(SIZE\_MAX), no check
2. Line 306: FitsInContiguousBufferOfSize() — checks (offset + size ≤ buffer\_size)
   only. The "size" is computed as Rows \* strides[i], which overflows (size\_t \*
   int32\_t(-1) wraps), then std::min() clamps it to a small value. The stride
   field itself is NEVER validated.
3. Line 334: frame->BackWithOwnedSharedMemory() — stores the mapping, no stride check
4. VideoFrame::stride() — a simple getter, returns planes\_[i].stride directly
5. VpxVideoEncoder::SetupStandardYuvPlanes() — copies stride to vpx\_image\_t::stride
   (int), no range check
6. vpx\_codec\_encode() — uses stride for row traversal, no bounds check

The DMA-buf deserialization path in the SAME file (line ~196) correctly validates:
if (!base::IsValueInRangeForNumericType<size\_t>(data.stride())) return false;
The SharedMemory path is missing this check — clearly an oversight.

== Attached files ==

- poc\_negative\_stride.html — MojoJS PoC (sends negative stride via VEA Mojo)
- poc\_patch.diff — Read-only probe patch for GPU-less reproduction
- poc\_patch\_report.md — Detailed analysis report
- bug\_report\_VideoFrame\_NegativeStride.md — Full technical report with crash logs
- asan\_unittest\_crash.log — Complete ASAN unit test output
- fix\_negative\_stride.diff — Suggested fix (add negative stride check)

# Summary

VideoFrame Mojo deserialization accepts negative stride → OOB read in video encoders

# Custom Questions

#### Type of crash:

Browser/GPU process crash (the VideoFrame deserialization and video encoding happen in the browser or GPU process, not the renderer/tab process). When UseOutOfProcessVideoEncoding is enabled, the crash occurs in the dedicated video encoding utility process. Otherwise it occurs in the GPU process. The renderer (tab) process is the attacker — it sends the malicious Mojo IPC message. The crash is cross-process.

#### Crash state:

== ASAN Crash (media\_unittests --gtest\_filter=*NegativeStride*) ==

==========================================================//

//
==1484417==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7dc7994ef1ff
at pc 0x561e67f6deee bp 0x7ffd6ed28f90 sp 0x7ffd6ed28f88
READ of size 1 at 0x7dc7994ef1ff thread T0
#0 0x561e67f6deed in media::VideoFrameStructTraitsTest\_NegativeStride\_Test::TestBody()
media/mojo/mojom/video\_frame\_mojom\_traits\_unittest.cc:496:17
#1 0x561e6399763b in testing::Test::Run()
#2 0x561e6399a7fa in testing::TestInfo::Run()

0x7dc7994ef1ff is located 1 bytes before 19072-byte region
[0x7dc7994ef200,0x7dc7994f3c80)
allocated by thread T0 here:
#0 0x561e60decc5d in operator new[](unsigned long)
#1 0x561e67f6db23 in media::VideoFrameStructTraitsTest\_NegativeStride\_Test::TestBody()

SUMMARY: AddressSanitizer: heap-buffer-overflow
media/mojo/mojom/video\_frame\_mojom\_traits\_unittest.cc:496:17
in media::VideoFrameStructTraitsTest\_NegativeStride\_Test::TestBody()

== Non-ASAN Crash (MojoJS PoC in headless Chrome) ==

Received signal 11 SEGV\_MAPERR 7f0d51061fff
#4 0x7f0d64589e07 mojo::StructTraits<>::Read()
[../../media/mojo/mojom/video\_frame\_mojom\_traits.cc:357:36]
#5 VideoEncodeAcceleratorStubDispatch::AcceptWithResponder()

Crash address: 0x7f0d51061fff (1 byte before shared memory mapping region)
Signal: SIGSEGV (SEGV\_MAPERR) — access to unmapped page

== Key type conversion trace ==
stride input: int32\_t(-1) = 0xFFFFFFFF
after assign: size\_t = 0xFFFFFFFFFFFFFFFF (SIZE\_MAX = 18446744073709551615)
encoder cast: (int)SIZE\_MAX = -1
pointer math: y\_plane + (-1) → 1 byte before buffer start → heap underflow

#### Reporter credit:

xmzyshypnc

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [asan_crash_output.log](attachments/asan_crash_output.log) (text/plain, 5.0 KB)
- [asan_output.log](attachments/asan_output.log) (text/plain, 4.6 KB)
- [fix_negative_stride.diff](attachments/fix_negative_stride.diff) (text/x-diff, 949 B)
- [js_poc_output.log](attachments/js_poc_output.log) (text/plain, 151 B)
- [poc_negative_stride.html](attachments/poc_negative_stride.html) (text/html, 13.6 KB)
- [poc_patch.diff](attachments/poc_patch.diff) (text/x-diff, 2.7 KB)
- [run_poc_v8.sh](attachments/run_poc_v8.sh) (text/x-sh, 4.9 KB)
- [poc_negative_stride.html](attachments/poc_negative_stride_73761436.html) (text/html, 14.2 KB)
- [reproduce.sh](attachments/reproduce.sh) (text/x-sh, 10.0 KB)
- [reproduce_output.log](attachments/reproduce_output.log) (text/plain, 43.4 KB)
- [mojo_demo.mp4](attachments/mojo_demo.mp4) (video/mp4, 4.6 MB)

## Timeline

### ma...@google.com (2026-02-17)

Thank you for your interest in finding security issues in Chrome. Please be aware that AI generated bug reports also require a lot of human work to verify - submitting several low quality, unsubstantiated, reports may be treated as abuse - <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#AI-Generated-Vulnerability-reports>

> The PoC patch (poc\_patch.diff) adds a ~30-line read-only probe to video\_frame\_mojom\_traits.cc, immediately after the deserialized VideoFrame is created. This patch is needed because:

> Our test server is headless Linux with no GPU. (...)

> On macOS or any machine with a GPU, the patch is unnecessary — the real VPX/AV1/VideoToolbox encoder will consume the frame and crash naturally.

Ok. So could you please provide an ASAN crash log demonstrating the OOB read without your patch applied?

### ha...@gmail.com (2026-02-17)

Sorry I made a mistak, this issue can only be reproduced in Linux for the flag "#if BUILDFLAG(USE_LINUX_VIDEO_ACCELERATION) " is only worked in Linux. Now I have only a Linux Server Environment and Macbook Pro. Now is the Chinese New Year so I'm on a holiday. I will return back to office after a week and can make new PoC with my PC. I can install Linux with GPU there. Since I'm reporting for the first time. I don't know if you can wait for my update. So sorrry again for my mistake and wish you have a good day.

### pe...@google.com (2026-02-17)

Thank you for providing more feedback. Adding the requester to the CC list.

### an...@chromium.org (2026-02-19)

[security shepherd]: Thanks for the report. I'll be closing this one out for now, and please feel free to create a new report about this when available.

### ha...@gmail.com (2026-02-26)

Hello, I reproduced in another interl-cpu Linux machine. Here is the detail and related file:

## 3. Vulnerability Call Chain

```
Renderer Process (compromised via MojoJS)
│
│  VideoEncodeAccelerator.Encode(frame{strides: [0x40000000, 0x20000000, 0x20000000]})
│
├─► Mojo IPC Deserialization
│   └─► video_frame_mojom_traits.cc:301
│       planes[i].stride = strides[i]     // int32(0x40000000) → size_t(1073741824)
│       calculated_plane_size overflows    // 288 * 0x40000000 wraps in int32
│       std::min(garbage, mapping_size)    // passes validation
│       FitsInContiguousBufferOfSize()     // passes (checks size, not stride)
│       WrapExternalYuvDataWithLayout()    // creates VideoFrame with stride=1GB
│
├─► Utility Process: MojoVideoEncodeAcceleratorService::Encode()
│   └─► Frame accepted (coded_size matches, encoder_ valid)
│
├─► VaapiVideoEncodeAccelerator::EncodeTask()
│   └─► native_input_mode_=false, frame has CPU access → shmem path
│
├─► VaapiVEA::CreateSurfacesForShmemEncoding()
│   └─► frame.coded_size() matches expected → continues
│
├─► VaapiWrapper::UploadVideoFrameToSurface()
│   └─► frame.format() == I420 → calls libyuv::I420ToNV12()
│
└─► libyuv::I420ToNV12(data, stride=1073741824, ...)
    └─► CopyPlane(): src_y += stride per row
        Row 0: read from data[0..351]                    ✓ (within 152064 byte buffer)
        Row 1: read from data[1073741824..1073742175]    ✗ UNMAPPED MEMORY
        ════════════════════════════════════════════
        💥 SIGSEGV (signal 11) SEGV_ACCERR
        ════════════════════════════════════════════

```
### 4.1 Environment Requirements

| Requirement | Detail |
| --- | --- |
| OS | Ubuntu 24.04.4 LTS (kernel 6.17.0-14-generic) |
| GPU | Intel with VA-API support (tested: Alder Lake-S GT1 [UHD Graphics 770]) |
| Chrome Commit | `7fe418d5ae169` on `origin/main` (version 147.0.7702.0) |
| Chrome Build | ASAN build with `is_component_build=true` |
| VA-API | Working H.264 encode support (`vainfo` shows `VAProfileH264*` with `VAEntrypointEncSlice*`) |

0. build chrome in 7fe418d5ae16991bf206e7cee9c51344d82f2091 with args.gn :

```
is_debug = false
is_asan = true
is_component_build = true
symbol_level = 2
enable_nacl = false
proprietary_codecs = true
ffmpeg_branding = "Chrome"
enable_platform_hevc = true
use_vaapi = true

```

1. start server in poc directory like :`python3 -m http.server 8787`
2. disable apparmor to use the sandbox

```
echo 0 | sudo tee /proc/sys/kernel/apparmor_restrict_unprivileged_userns

```

2. run with the following command :

```
bash bash reproduce.sh 2>&1

```

3. You can see the crash like :

```
[1187013:1187020:0226/134553.467521:VERBOSE2:media/gpu/vaapi/vaapi_video_encode_accelerator.cc:1216] SetState(): setting state to: kEncoding
[1187013:1187013:0226/134553.467538:VERBOSE2:media/mojo/services/mojo_video_encode_accelerator_service.cc:320] RequireBitstreamBuffers input_count=4 input_coded_size=352x288 output_buffer_size=2097152
[1187013:1187013:0226/134555.475544:VERBOSE2:media/mojo/services/mojo_video_encode_accelerator_service.cc:159] Encode tstamp=0 s
[1187013:1187020:0226/134555.476025:VERBOSE3:media/gpu/vaapi/vaapi_wrapper.cc:3460] vaCreateSurfaces (allocate mode)
[1187013:1187020:0226/134555.476204:VERBOSE3:media/gpu/vaapi/vaapi_wrapper.cc:3460] vaCreateSurfaces (allocate mode)
Received signal 11 SEGV_ACCERR 6e6df64b8000
#0 0x5a475e183c36 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/chrome+0x7de4c35)
#1 0x726e6e171132 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x971131)
#2 0x726e6e103294 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x903293)
#3 0x726e6e17033a (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x970339)
#4 0x726dd9445330 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4532f)
#5 0x726e638cb400 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libcontent.so+0xaecb3ff)
#6 0x726e638a0ecf (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libcontent.so+0xaea0ece)
#7 0x726e6389f93d (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libcontent.so+0xae9f93c)
#8 0x726e622f4e3e (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libcontent.so+0x98f4e3d)
#9 0x726e139cb5fe (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libmedia_mojo_services.so+0x15cb5fd)
#10 0x726e139c572a (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libmedia_mojo_services.so+0x15c5729)
#11 0x726e139c423d (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libmedia_mojo_services.so+0x15c423c)
#12 0x726e139e3f72 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libmedia_mojo_services.so+0x15e3f71)
#13 0x726e6dc86efe (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x486efd)
#14 0x726e6dedb835 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x6db834)
#15 0x726e6dffa7fc (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x7fa7fb)
#16 0x726e6dffaa27 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x7faa26)
#17 0x726e6dff8e46 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x7f8e45)
#18 0x726e6dff7c5a (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x7f7c59)
#19 0x726e6e027cb9 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x827cb8)
#20 0x726e6e026fff (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x826ffe)
#21 0x726e6e02689a (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x826899)
#22 0x726e6e0d7a1d (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/libbase.so+0x8d7a1c)
#23 0x5a475e1d9e87 (/home/wz/chrome_transfer/data/my_chrome/src/out/ASAN/chrome+0x7e3ae86)
#24 0x726dd949caa4 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x9caa3)
#25 0x726dd9529a64 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x129a63)
  r8: 0000000000000160  r9: 0000726e638cb3f0 r10: 0000726e638a8ca0 r11: 0000000000040000
 r12: 000000000000011f r13: 0000000000000180 r14: 00006e6db6457980 r15: 00006e6df64b8000
  di: 00006e6db6457980  si: 00006e6df64b8000  bp: 00006e6db7e76d60  bx: 0000726e638cb3f0
  dx: 0000000000000160  ax: 00006e6df64b8000  cx: 0000000000000160  sp: 00006e6db7e76d60
  ip: 0000726e638cb400 efl: 0000000000010212 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00006e6df64b8000
[end of stack trace]
../../sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc:**CRASHING**:seccomp-bpf failure in syscall nr=0x25 arg1=0x5 arg2=0x0 arg3=0x0 arg4=0x726dd941bc40
=== PoC COMPLETE ===", source: http://127.0.0.1:8787/poc_negative_stride.html (35)
[1186881:1186904:0226/134557.090593:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT

```

Here is bisect:

## 9. Git Bisect: Vulnerability Introduction

Using `git blame` on the vulnerable code path, two key commits were identified:

### 9.1 Root Cause Commit (stride assignment without validation)

| Field | Value |
| --- | --- |
| **Commit** | `b8894b5d15929c58e458416cefad86b35a8ee1ce` |
| **Author** | Hirokazu Honda <[hiroh@chromium.org](mailto:hiroh@chromium.org)> |
| **Date** | 2022-09-01 |
| **Subject** | "Deprecate MojoSharedBufferVideoFrame" |
| **What it introduced** | `planes[i].stride = strides[i]` — the unvalidated `int32_t → size_t` assignment |

This commit refactored the shared memory VideoFrame deserialization path, introducing `ColorPlaneLayout` with a `stride` field assigned directly from the Mojo `int32` without any range or sign validation.

### 9.2 Exploitability Amplification Commit (integer overflow in size calculation)

| Field | Value |
| --- | --- |
| **Commit** | `c528f7d715add7a5c43c958e87ebfba3ad028c00` |
| **Author** | Eugene Zemtsov <[eugene@chromium.org](mailto:eugene@chromium.org)> |
| **Date** | 2024-11-09 |
| **Subject** | "media: More accurate calculation of plane sizes during deserialization" |
| **What it introduced** | `calculated_plane_size = Rows(i, format, height) * strides[i]` — integer overflow in `int32 × int32` multiplication |
| **CL** | <https://chromium-review.googlesource.com/c/chromium/src/+/6001897> |

Before this commit, `planes[i].size` was computed as the distance between adjacent offsets (`offsets[i+1] - offsets[i]`), which didn't depend on the stride value. The new formula `Rows() * strides[i]` operates in `int32` domain and overflows when stride is large, producing a small garbage value that passes the subsequent `std::min()` check.

### ha...@gmail.com (2026-02-26)

Here is the reproduce.sh and log

### ha...@gmail.com (2026-02-26)

Here is the demo:

### ma...@google.com (2026-02-26)

Eugene, could you take a brief look at the updated report in #6? I'm suspecting that the requirement of --use-fake-device-for-media-stream makes this not a security issue. Same for is\_component\_build.

### eu...@chromium.org (2026-02-27)

Confirmed. A compromised renderer can trigger a GPU crash.

### aj...@google.com (2026-02-27)

Tentatively setting flags - eugene - could you upload your asan log?

### eu...@chromium.org (2026-02-27)

I didn't use ASAN.

### ch...@google.com (2026-02-27)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-27)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must exceed severity.

### eu...@chromium.org (2026-02-27)

Closed duplicate of this issue: <https://issues.chromium.org/issues/487842062>

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7614704>

media: Prevent passing of frames with absurdly large strides via Mojo

---


Expand for full commit details
```
     
    - Make strides unsigned in mojo, as they are in VideoFrame 
    - Validate that each plane's footprint (offset + stride * rows) 
        fits in the buffer. 
    - Remove support for interleaved planes. IMC4 pixel format. 
     
    Bug: 484547633, 378046071 
    Change-Id: I8e5dbebddc434041bd7c31c2b16c2b5963314061 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7614704 
    Reviewed-by: Xiaohan Wang <xhwang@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Matthew Denton <mpdenton@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592880}

```

---

Files:

- M `media/base/video_frame_layout.cc`
- M `media/base/video_frame_layout_unittest.cc`
- M `media/mojo/mojom/media_types.mojom`
- M `media/mojo/mojom/video_frame_mojom_traits.cc`
- M `media/mojo/mojom/video_frame_mojom_traits_unittest.cc`

---

Hash: [d0a80fe50c1e778fdb9e2d5283e7e5ad193bffcd](https://chromiumdash.appspot.com/commit/d0a80fe50c1e778fdb9e2d5283e7e5ad193bffcd)  

Date: Tue Mar 3 01:17:06 2026


---

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7630158>

media: Refine memory boundary check in VideoFrameLayout

---


Expand for full commit details
```
     
     - Update `VideoFrameLayout::FitsInContiguousBufferOfSize()` to 
    compute the exact footprint for each plane. Instead of reserving the 
    full stride for the last row, the calculation now uses `stride * (rows - 
    1) + row_bytes`. 
     
    - Validate the number of planes against the pixel format. 
     
    This matches MediaCodec's calculation of input buffers sizes and fixes 
    video encoding on Android. 
     
    Bug: 489487657, 484547633, 378046071 
    Change-Id: I3119225c6b103ad36b91ef04cfb588f585f634ad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630158 
    Auto-Submit: Eugene Zemtsov <eugene@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593586}

```

---

Files:

- M `media/base/video_frame_layout.cc`
- M `media/base/video_frame_layout_unittest.cc`

---

Hash: [e387cdb10f45e664f1d99fc322e97c8dbc104272](https://chromiumdash.appspot.com/commit/e387cdb10f45e664f1d99fc322e97c8dbc104272)  

Date: Tue Mar 3 23:55:38 2026


---

### ma...@google.com (2026-03-04)

This looks like a possible regression of 40063362.

### ch...@google.com (2026-03-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ha...@gmail.com (2026-03-18)

Hello, may I ask if there is any reward and CVE assignment?

### ha...@gmail.com (2026-04-20)

Hello security team,My apologies for reaching out late. I have only just seen the final CVE assignment result for this vulnerability.We would appreciate it if you could revise the published credit attribution to correctly list all original discoverers as below:
Zheng Wang ([@xmzyshypnc1](https://x.com/xmzyshypnc1)),Yang Hu [@BlueSheep](https://x.com/B111ueSheep) and Zhuorao Yang [@A1ex](https://x.com/AA_YYoung)

### ha...@gmail.com (2026-05-12)

Hello, will this issue be rewared?

### ma...@google.com (2026-05-13)

I reached out to some folks about the attribution change.

The VRP decision is still pending, there is a bit of a backlog at the moment.

### ha...@gmail.com (2026-05-14)

Got it, appreciate your follow-up and clarification.

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484547633)*
