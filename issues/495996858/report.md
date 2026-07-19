# UAF in WebRTC LibaomAv1Encoder sync issues triggered by frequent resolution changes

| Field | Value |
|-------|-------|
| **Issue ID** | [495996858](https://issues.chromium.org/issues/495996858) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2026-03-25 |
| **Bounty** | $7,000.00 |

## Description

### Summary

`VideoFramePool::PoolImpl::CreateFrame` drops non-matching pooled backing allocations while AV1 encoder row-worker threads still hold raw pointers into the freed memory, leading to the UAF in webrtc.

### Details

When the WebRTC encoder needs a mapped I420 buffer, the call chain `ConvertToWebRtcVideoFrameBuffer` → `WebRtcVideoFrameAdapter::AdaptBestFrame` → `SharedResources::CreateFrame` delegates to [`VideoFramePool::PoolImpl::CreateFrame`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/video_frame_pool.cc;l=83) for allocation. `SharedResources::CreateFrame` is a direct passthrough:

```
scoped_refptr<media::VideoFrame>
WebRtcVideoFrameAdapter::SharedResources::CreateFrame(
    media::VideoPixelFormat format,
    const gfx::Size& coded_size,
    const gfx::Rect& visible_rect,
    const gfx::Size& natural_size,
    base::TimeDelta timestamp) {
  return pool_.CreateFrame(format, coded_size, visible_rect, natural_size,
                           timestamp);
}

```

Inside `VideoFramePool::PoolImpl::CreateFrame`, the pool iterates over cached frames looking for a size/format match. Non-matching frames are popped and their backing memory is freed immediately when the `scoped_refptr` goes out of scope:

```
while (!frames_.empty()) {
  scoped_refptr<VideoFrame> pool_frame = std::move(frames_.back().frame);
  frames_.pop_back();

  if (pool_frame->IsSameAllocation(format, coded_size, visible_rect,
                                   natural_size)) {
    frame = pool_frame;
    frame->set_timestamp(timestamp);
    frame->clear_metadata();
    break;
  }
}

```

When a matching frame is found (or a new one allocated), it is returned wrapped. The wrapper's destruction observer reinserts the backing frame into the pool:

```
scoped_refptr<VideoFrame> wrapped_frame = VideoFrame::WrapVideoFrame(
    frame, frame->format(), frame->visible_rect(), frame->natural_size());
wrapped_frame->AddDestructionObserver(base::BindOnce(
    &VideoFramePool::PoolImpl::FrameReleased, this, std::move(frame)));
return wrapped_frame;

```

The converted frame is surfaced to the encoder through [`I420FrameAdapter`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/webrtc/convert_to_webrtc_video_frame_buffer.cc;l=40), whose accessors return raw pointers into the underlying `media::VideoFrame` data:

```
const uint8_t* DataY() const override {
  return frame_->visible_data(media::VideoFrame::Plane::kY);
}

```

The AV1 encoder (`LibaomAv1Encoder::Encode`) calls `GetMappedFrameBuffer`, which triggers `AdaptBestFrame` → `ConvertToWebRtcVideoFrameBuffer` → `CreateFrame`.

This invokes `VideoFramePool::PoolImpl::CreateFrame` on the encoder thread. If a previous frame's wrapper has already been returned to the pool, and the new `CreateFrame` call encounters a size change, it drops that pooled backing. However, the AV1 encoder dispatches encoding work to `CodecWorker` threads via `enc_row_mt_worker_hook`, and those workers read frame plane data through the raw pointers obtained from `I420FrameAdapter`. There is no synchronization that prevents a subsequent `CreateFrame` call from reclaiming the backing while row workers from a prior encode are still reading from those pointers, leading to the UAF.

### Reproduction

Run chromium (e.g., <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1603396.zip>) with:

```
./chrome --no-sandbox poc.html

```

You would observe the stack-use-after-return crash shown in `asan.txt`

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 21.1 KB)
- [poc.html](attachments/poc.html) (text/html, 5.1 KB)
- [asan.txt](attachments/asan_74778674.txt) (text/plain, 26.2 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5733203801210880.

### hc...@google.com (2026-03-25)

using asan 148.0.7743.0 (linux), got the attached asan trace

Unsure why clusterfuzz was unable to repro

### hc...@google.com (2026-03-25)

Foundin of 148 definitely, though unsure if this extends further back

### da...@chromium.org (2026-03-25)

Ilya, were you already looking at this area?

### da...@chromium.org (2026-03-25)

FWIW, callers are expected to hold a ref on the VideoFrame when handing off frames to non-Chromium consumers. We don't have any examples in the code base of this anymore, but here's the old usage in FFmpegVideoDecoder:

- <https://chromium.googlesource.com/chromium/src/+/6adf299788d21db963d2141b79b9bf1ebacaae77/media/filters/ffmpeg_video_decoder.cc#203>

### eu...@chromium.org (2026-03-25)

I think this is more or less the same issue as <https://issues.chromium.org/issues/495477995>

### eu...@chromium.org (2026-03-25)

I'm more or less sure that this has nothing to do with `VideoFramePool`

### eu...@chromium.org (2026-03-25)

## Magical computer brain says this:

### [Issue 1](https://issues.chromium.org/issues/1): `media::CodecWorkerImpl` Synchronization

This crash occurs because `aom_codec_encode` (on thread T5) is running concurrently with `aom_codec_destroy` (on thread T16).

- The Race: `LibaomAv1Encoder::Release()` (called during encoder destruction or reconfiguration) calls `aom_codec_destroy(&ctx_)`, which frees frame buffers and other context-related memory.
  Simultaneously, `LibaomAv1Encoder::DoEncode()` is calling `aom_codec_encode(&ctx_, ...)` which reads from these buffers.
- The Concurrency: In WebRTC, the VideoStreamEncoder is supposed to serialize all encoder calls (Encode, Release, InitEncode) on a single encoder\_queue\_. However, the ASAN trace shows
  two different ThreadPool threads (T5 and T16) executing these tasks concurrently. This implies that either the VideoStreamEncoder is being accessed from multiple task queues or
  multiple VideoStreamEncoder instances are somehow sharing the same encoder state. Given the POC's rapid replaceTrack and setParameters calls, it's likely triggering a race during the
  transition between encoder instances where an old encoder is being released while a stray "frame prepared" callback still triggers an encode on it.

```
==3281329==ERROR: AddressSanitizer: stack-use-after-return on address 0x7b099b912a80 at pc 0x562b9eaf2e94 bp 0x7b0a40a05050 sp 0x7b0a40a05048
READ of size 32 at 0x7b099b912a80 thread T16 (ThreadPoolPrese)
==3281329==WARNING: invalid path to external symbolizer!
==3281329==WARNING: Failed to use and restart external symbolizer!
    #0 0x562b9eaf2e93 in aom_sad32x32_avx2 ./../../third_party/libaom/source/libaom/aom_dsp/x86/sad_avx2.c:135:16
    #1 0x562bb85e200a in av1_nonrd_pick_inter_mode_sb ./../../third_party/libaom/source/libaom/av1/encoder/nonrd_pickmode.c:2000:21
    #2 0x562bb85be1e4 in pick_sb_modes_nonrd ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:2334:5
    #3 0x562bb85bc437 in av1_nonrd_use_partition ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:3020:7
    #4 0x562bb85bac74 in av1_nonrd_use_partition ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:3095:11
    #5 0x562bb8478acc in av1_encode_sb_row ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:658:3
    #6 0x562bb853a211 in enc_row_mt_worker_hook ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:727:5
    #7 0x562b9d2949e6 in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::Execute(AVxWorker*) ./../../media/base/codec_worker_impl.h:69:29
    #8 0x562bb8536d36 in av1_encode_tiles_row_mt ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:1490:7
    #9 0x562bb847ffca in encode_frame_internal ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:2389:5
    #10 0x562bb84e70d8 in encode_with_recode_loop_and_filter ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:3199:3
    #11 0x562bb84d74b2 in av1_encode ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:4430:9
    #12 0x562bb850c06b in av1_encode_strategy ./../../third_party/libaom/source/libaom/av1/encoder/encode_strategy.c:1724:7
    #13 0x562bb84de106 in av1_get_compressed_data ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:5374:22
    #14 0x562bb83c42ff in encoder_encode ./../../third_party/libaom/source/libaom/av1/av1_cx_iface.c:3635:20
    #15 0x562bb83b2b72 in aom_codec_encode ./../../third_party/libaom/source/libaom/aom/src/aom_encoder.c:191:11
    #16 0x562bc79ecbdf in webrtc::(anonymous namespace)::LibaomAv1Encoder::DoEncode(unsigned int, long, webrtc::ScalableVideoController::LayerFrameConfig*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:1108:7
    #17 0x562bc79e46cd in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:1000:16
    #18 0x562bc7a2ca45 in webrtc::SimulcastEncoderAdapter::StreamContext::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:282:23
    #19 0x562bc7a3581c in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:687:23
    #20 0x562bc7f6bfbb in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2230:43
    #21 0x562bc7f69561 in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2059:3
    #22 0x562bc7f53404 in webrtc::VideoStreamEncoder::OnFramePrepared(unsigned long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1928:5
    #23 0x562bc7f677cf in webrtc::VideoStreamEncoder::MaybePrepareVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1909:5
    #24 0x562bc7f66c92 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/video_stream_encoder.cc:1688:5


```
#### 1. Incorrect Destruction Order

In `media/base/codec_worker_impl.h`, the member variables are declared as follows:

```
base::Thread thread_;
base::Lock mutex_;
base::WaitableEvent event_;

```

In C++, members are destroyed in the reverse order of declaration. This means `event_` is destroyed **before** `thread_` is stopped and joined. If the worker thread is currently executing a task that signals this event (e.g., during a `Sync()` or `End()` call), it will attempt to access a deleted `WaitableEvent` object, leading to a crash.

#### 2. Mutual Exclusion Over Work Execution

The implementation intended to use a `WaitableEvent` to signal when asynchronous work is "depleted." However, the worker thread holds a lock for the **entire duration** of the encoding work:

```
void ExecuteOnTaskRunner(Worker* worker) {
  base::AutoLock lock(mutex_); // Lock held during the actual encoding
  Execute(worker);             // Actual libaom work
  worker->status_ = StatusOk;
}

```

When the main thread calls `Sync()`, it also tries to acquire `mutex_`. This causes the main thread to block on the lock itself rather than the `WaitableEvent`. By the time the main thread acquires the lock, the work is already done, and the `WaitableEvent` logic becomes a redundant, yet still dangerous, race point. If the main thread wakes up and proceeds to delete the `CodecWorkerImpl` while the worker thread is still physically inside the `Signal()` function (on its own stack), the "stack-use-after-return" occurs.

---

### [Issue 2](https://issues.chromium.org/issues/2): WebRTC Encoder Lifecycle Race

**Symptom:** Heap-use-after-free in `aom_sad32x32_avx2` via `aom_codec_encode`.

```
==2885224==ERROR: AddressSanitizer: heap-use-after-free on address 0x79dd9183d140 at pc 0x55fb1fb81184 bp 0x7b392e8a9f30 sp 0x7b392e8a9f28
READ of size 32 at 0x79dd9183d140 thread T5 (ThreadPoolPrese)
==2885224==WARNING: invalid path to external symbolizer!
==2885224==WARNING: Failed to use and restart external symbolizer!
    #0 0x55fb1fb81183 in aom_sad32x32_avx2 ./../../third_party/libaom/source/libaom/aom_dsp/x86/sad_avx2.c:135:16
    #1 0x55fb3944ef2a in av1_nonrd_pick_inter_mode_sb ./../../third_party/libaom/source/libaom/av1/encoder/nonrd_pickmode.c:2000:21
    #2 0x55fb3942b104 in pick_sb_modes_nonrd ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:2334:5
    #3 0x55fb39429357 in av1_nonrd_use_partition ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:3020:7
    #4 0x55fb39427b94 in av1_nonrd_use_partition ./../../third_party/libaom/source/libaom/av1/encoder/partition_search.c:3095:11
    #5 0x55fb392e5b3c in av1_encode_sb_row ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:656:3
    #6 0x55fb393a7131 in enc_row_mt_worker_hook ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:727:5
    #7 0x55fb1e45d606 in media::CodecWorkerImpl<AVxWorkerInterface, AVxWorkerImpl, AVxWorker, AVxWorkerStatus, (AVxWorkerStatus)0, (AVxWorkerStatus)1, (AVxWorkerStatus)2>::Execute(AVxWorker*) ./../../media/base/codec_worker_impl.h:69:29
    #8 0x55fb393a3c56 in av1_encode_tiles_row_mt ./../../third_party/libaom/source/libaom/av1/encoder/ethread.c:1492:7
    #9 0x55fb392ed03a in encode_frame_internal ./../../third_party/libaom/source/libaom/av1/encoder/encodeframe.c:2387:5
    #10 0x55fb39354148 in encode_with_recode_loop_and_filter ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:3199:3
    #11 0x55fb39344522 in av1_encode ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:4429:9
    #12 0x55fb39378f8b in av1_encode_strategy ./../../third_party/libaom/source/libaom/av1/encoder/encode_strategy.c:1715:7
    #13 0x55fb3934b176 in av1_get_compressed_data ./../../third_party/libaom/source/libaom/av1/encoder/encoder.c:5373:22
    #14 0x55fb3923126f in encoder_encode ./../../third_party/libaom/source/libaom/av1/av1_cx_iface.c:3641:20
    #15 0x55fb3921fae2 in aom_codec_encode ./../../third_party/libaom/source/libaom/aom/src/aom_encoder.c:191:11
    #16 0x55fb48871b6f in webrtc::(anonymous namespace)::LibaomAv1Encoder::DoEncode(unsigned int, long, webrtc::ScalableVideoController::LayerFrameConfig*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:1108:7
    #17 0x55fb4886965d in webrtc::(anonymous namespace)::LibaomAv1Encoder::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc:1000:16
    #18 0x55fb488b1db5 in webrtc::SimulcastEncoderAdapter::StreamContext::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:282:23
    #19 0x55fb488bab8c in webrtc::SimulcastEncoderAdapter::Encode(webrtc::VideoFrame const&, std::__Cr::vector<webrtc::VideoFrameType, std::__Cr::allocator<webrtc::VideoFrameType>> const*) ./../../third_party/webrtc/media/engine/simulcast_encoder_adapter.cc:687:23
    #20 0x55fb48df113b in webrtc::VideoStreamEncoder::EncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2230:43
    #21 0x55fb48dee6e1 in webrtc::VideoStreamEncoder::MaybeEncodeVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:2059:3
    #22 0x55fb48dd8584 in webrtc::VideoStreamEncoder::OnFramePrepared(unsigned long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1928:5
    #23 0x55fb48dec94f in webrtc::VideoStreamEncoder::MaybePrepareVideoFrame(webrtc::VideoFrame const&, long) ./../../third_party/webrtc/video/video_stream_encoder.cc:1909:5
    #24 0x55fb48debe12 in webrtc::VideoStreamEncoder::OnFrame(webrtc::Timestamp, bool, webrtc::VideoFrame const&) ./../../third_party/webrtc/video/video_stream_encoder.cc:1688:5

```
#### 1. The Async Frame Preparation Gap

WebRTC uses an asynchronous path for frame preparation (`PrepareMappedBufferAsync`). When a frame is "prepared," a callback (`OnFramePrepared`) is triggered, which then posts a task back to the `encoder_queue_` to perform the actual `Encode()`.

#### 2. The Race Mechanism

The POC performs rapid `replaceTrack` and `setParameters` calls. This sequence causes `VideoStreamEncoder` to frequently reconfigure or swap encoder instances.

1. **Frame N** starts an asynchronous preparation.
2. A **Reconfiguration** occurs. `VideoStreamEncoder` calls `ReleaseEncoder()` for the current encoder.
3. `LibaomAv1Encoder::Release()` is called, which internally executes `aom_codec_destroy(&ctx_)`, freeing the libaom internal buffers.
4. **Frame N** finishes preparation and triggers `OnFramePrepared`.
5. A stray task is posted to the `encoder_queue_` to encode Frame N using the *now released* encoder instance.
6. `LibaomAv1Encoder::DoEncode()` is called on the destroyed context, resulting in a heap-use-after-free when libaom tries to access its motion estimation buffers.

#### 3. Why the Serial Queue Fails

While `VideoStreamEncoder` uses a serial `encoder_queue_`, it does not currently synchronize the *completion* of the asynchronous "frame prepared" callbacks with the destruction of the encoder. The `PreparedFramesProcessor` continues to funnel callbacks back to the encoder even after `ReleaseEncoder()` has been initiated, allowing `Encode()` calls to "outrun" the cleanup logic.

### ch...@google.com (2026-03-26)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-26)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### il...@google.com (2026-03-26)

I doubt the second issue from analysis in #9 is valid. It requires --enable-features=WebrtcAceleratedScaling, which is DEFAULT\_DISABLED and not rolled anywhere.
Nothing works asynchronously right now.

The first issue from #9 also seems incorrect. All the encoders are engaged/created/destroyed in a single encoder queue sequence in webrtc. So there can't be concurrent Release() call with ongoing Encode()

I don't think the analysis in #1 is correct either. The VideoFrame created by the pool is exposed to the encoder as VideoFrameAdapter (the mentioned I420FrameWrapper holds WebrtcVideoFrameAdapter, which holds the VideoFrame in adapter\_frames\_) It isn't returned to the pool until the VideoFrameBuffer is destroyed, but it's in a [local variable](https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc;l=851;drc=5460d74631c9df16c9f0d160fb872c9834f8bb59), which isn't freed until the aom\_codec\_encode() call to libaom encoder completes. That aom\_codec\_encode() call is creating multiple threads, but I presume all threads have to complete the work before the aom\_codec\_encode() call returns, because immediately after that we gather encoded data with no wait.

So the videoFrame is not destroyed, so it's not returned to the pool, and the pool dropping VideoFrames of a different size can't trigger any UAF issues, because the pool doesn't hold the frame which data planes are passed to the libaom encoder.

The strange thing is that in the asan.txt we see that the data is allocated in the CodecThread:

```
READ of size 32 at 0x7b099b912a80 thread T16 (ThreadPoolPrese)

Address 0x7b099b912a80 is located in stack of thread T221 (CodecWorker) at offset 0 in frame
    #0 0x562bb38e6e3f in base::WaitableEvent::Signal() ./../../base/synchronization/waitable_event.cc:36:0

```

But these CodecThreads don't interract with VideoFrameBuffer at all, they only get the pointers to I420 data planes already held by the T16, which executes `LibaomAv1Encoder::Encode`.

The crashing function seems to be reading the pixels indeed. But these may be pixels created by libaom internally to store lower resolution image for smaller SVC layers or denoiser.

So I believe something else is at play here. We need to dive deeper into libaom internals here.

That is all true if we assume that the `aom_codec_encode()` doesn't return while some of the CodecWorker threads still do some work.  

Again, we need libaom developers here.

### il...@google.com (2026-03-26)

Adding jianj@ and marpan@

The asan.txt from #3 is slightly different, but indicates a similar issue.

There the UAFed data is allocated by `aom_realloc_frame_buffer` inside the libaom codec worker.

This confirms my idea from the previous comment: The webrtc/chrome VideoFramePool has nothing to do with this UAF. This is some data allocated inside libaom, but dropped by it internally.

Seems like changing the resolution triggers the issue. Some state lingers from the previous configuration and not updated accordingly.

### dx...@google.com (2026-03-27)

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/209581>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 4369bd1258dc99fa759916d9aba6509cdda9d877  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-03-30)

Project: aom  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/209821>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: a047955845e50e43786d51cdefcfc9e87804ed61  

Date: Mon Mar 30 03:27:20 2026


---

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7718706>

Roll src/third\_party/libaom/source/libaom/ de575da20..dc0b27cfb (15 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/de575da20409..dc0b27cfbc49 
     
    $ git log de575da20..dc0b27cfb --date=short --no-merges --format='%ad %ae %s' 
    2026-03-27 juliobbv Update CHANGELOG with more changes 
    2026-03-26 jianj use unaligned load for av1_convolve_*_avx2 
    2026-03-25 fgalligan Add support for more color spaces 
    2026-03-27 wtc Revert "av1/decoder/obu.c: don't fail on undefined levels" 
    2026-03-26 jzern remove third_party/SVT-AV1 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
    2026-03-25 rohan.baid Enable SIMD of av1_apply_temporal_filter() for 422 format 
    2026-03-25 jzern Revert "Prune the evaluation of inter transform split" 
    2026-03-20 rohan.baid Enable AVX2 and SSE2 for av1_highbd_apply_temporal_filter() 
    2026-03-25 fgalligan Fix typo in matrix_coefficients_enum 
    2026-03-24 yunqingwang Optimize diamond_search_sad 
    2026-03-24 jzern encode_api_test.cc: fix Visual Studio warnings 
    2026-03-24 juliobbv Update CHANGELOG with new features and bug fixes 
    2026-03-24 ranjit.tulabandu Prune the evaluation of inter transform split 
    2026-03-23 diksha.singh Extend sf 'prune_single_ref' to speed 2 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 307414544, 495477995, 495996858, 446258249 
    Change-Id: Ifee42bc36eda1442f612a2479d47bd4c58385c78 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7718706 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Auto-Submit: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608139}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/cmake_update.sh`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.c`
- M `third_party/libaom/source/config/linux/arm-neon/config/aom_config.h`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.c`
- M `third_party/libaom/source/config/linux/arm64-cpu-detect/config/aom_config.h`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.c`
- M `third_party/libaom/source/config/linux/generic/config/aom_config.h`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.c`
- M `third_party/libaom/source/config/linux/ia32/config/aom_config.h`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.asm`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.c`
- M `third_party/libaom/source/config/linux/x64/config/aom_config.h`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.asm`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.c`
- M `third_party/libaom/source/config/win/arm64-cpu-detect/config/aom_config.h`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.asm`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.c`
- M `third_party/libaom/source/config/win/ia32/config/aom_config.h`
- M `third_party/libaom/source/config/win/x64/config/aom_config.asm`
- M `third_party/libaom/source/config/win/x64/config/aom_config.c`
- M `third_party/libaom/source/config/win/x64/config/aom_config.h`
- M `third_party/libaom/source/libaom`

---

Hash: [5ef6340f7ee1764c9ccdf8e1a225141209477d32](https://chromiumdash.appspot.com/commit/5ef6340f7ee1764c9ccdf8e1a225141209477d32)  

Date: Tue Mar 31 22:23:05 2026


---

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/7722240>

Roll src/third\_party/libaom/source/libaom/ dc0b27cfb..1ee384377 (13 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/dc0b27cfbc49..1ee384377191 
     
    $ git log dc0b27cfb..1ee384377 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-31 wtc Enable Clang's -Wc23-extensions warning 
    2026-03-31 wtc Spelling fix: change "an" to "a" 
    2026-03-31 jianj RC: skip shortern GF when using ext RC 
    2026-03-31 marpan Fix unitialized variable in nonrd_pickmode 
    2026-03-30 wtc Convert some assert() to static_assert() 
    2026-03-31 juliobbv Add valuable tune IQ info to `adjust_rdcost()` 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-29 wtc Enable the ISO C11 standard 
    2026-03-30 li.zhang2 Arm: Improve av1_apply_temporal_filter 
    2026-03-30 li.zhang2 Arm: Enable Neon and Neon Dotprod for av1_apply_temporal_filter 
    2026-03-30 li.zhang2 Fix apply_temporal_filter unit test 
    2026-03-30 diksha.singh Extend sf 'weight_calc_level_in_tf' to speed 3 
    2026-03-28 ranjit.tulabandu Fix the calculation of known_rd 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.com 
     
    Bug: 495477995, 495996858, 307414544 
    Change-Id: I6a059e50d48e93956fd105afdf9785fcd533d1a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722240 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Commit-Queue: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608757}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [8294475710edc805fa56440bc3b82f52385e59fb](https://chromiumdash.appspot.com/commit/8294475710edc805fa56440bc3b82f52385e59fb)  

Date: Wed Apr 1 20:56:52 2026


---

### dx...@google.com (2026-04-02)

Project: aom  

Branch:  main  

Author:  Wan-Teh Chang [wtc@google.com](mailto:wtc@google.com)  

Link:    <https://aomedia-review.googlesource.com/210043>

Change cm back to const in combined\_motion\_search

---


Expand for full commit details
```
     
    The local variable cm in combined_motion_search() was changed to a 
    non-const pointer so that it could be passed to get_ref_scale_factors(). 
    There is a get_ref_scale_factors_const() function for this purpose. 
     
    A follow-up to commit a047955. 
     
    Bug: 495477995, 495996858 
    Change-Id: Ic8b66f8060247a3487a7740fe5383c6e5455fa10

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: c61e9586156f0023ad31e8a6abb0dfdcfd820927  

Date: Thu Apr 2 01:57:32 2026


---

### dx...@google.com (2026-04-02)

Project: aom  

Branch:  main  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210101>

av1\_nonrd\_pick\_inter\_mode\_sb: normalize ref frame check

---


Expand for full commit details
```
     
    Prefer `search_state.use_ref_frame_mask[]` over `cpi->ref_frame_flags`. 
    These are equivalent and checking the former is more consistent with the 
    rest of the function. This is a follow up to: 
     4369bd1258 av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Bug: 495477995, 495996858 
    Change-Id: Ie4bd1f4c80c4182add35c7a9c1977c15ce97d3bd

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 395efd18d8ef31d8452a0336e848c02072feffe7  

Date: Thu Apr 2 03:56:24 2026


---

### dx...@google.com (2026-04-09)

2 changes merged

---

Project: aom  

Branch:  m147-7727  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/210481>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858, 500600182 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e 
    (cherry picked from commit a047955845e50e43786d51cdefcfc9e87804ed61)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: ab9876a5983227865ee26e91caac87c6b8750e27  

Date: Mon Mar 30 03:27:20 2026


---


---

Project: aom  

Branch:  m147-7727  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210461>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858, 500600182 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355 
    (cherry picked from commit 4369bd1258dc99fa759916d9aba6509cdda9d877)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: c17573bf30a4901dedc98ded5b91aec060784d8d  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-04-09)

2 changes merged

---

Project: aom  

Branch:  m146-7680  

Author:  James Zern [jzern@google.com](mailto:jzern@google.com)  

Link:    <https://aomedia-review.googlesource.com/210462>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858, 500599336 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355 
    (cherry picked from commit 4369bd1258dc99fa759916d9aba6509cdda9d877)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 5fb0845b95f21fec4113ce03e9647e31b78e610d  

Date: Fri Mar 27 17:56:13 2026


---


---

Project: aom  

Branch:  m146-7680  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/210463>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858, 500599336 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e 
    (cherry picked from commit a047955845e50e43786d51cdefcfc9e87804ed61)

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: b5d2fb00c10392da233017c223b1a5662bc7bb0c  

Date: Mon Mar 30 03:27:20 2026


---

### pe...@google.com (2026-04-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7745843>

Roll src/third\_party/libaom/source/libaom/ 446588f90..b5d2fb00c (2 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/446588f90da2..b5d2fb00c103 
     
    $ git log 446588f90..b5d2fb00c --date=short --no-merges --format='%ad %ae %s' 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 495477995, 495996858, 500599336 
    Fixed: 500599336 
    Change-Id: I73fa7bcdd1d14cabea5dc27aca53086f74af8fc4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7745843 
    Auto-Submit: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3912} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [038ad16930bf61db3b1f19b1b2a8e8df1fc786e0](https://chromiumdash.appspot.com/commit/038ad16930bf61db3b1f19b1b2a8e8df1fc786e0)  

Date: Fri Apr 10 16:21:20 2026


---

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  James Zern [jzern@chromium.org](mailto:jzern@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7746328>

Roll src/third\_party/libaom/source/libaom/ 9dd1b8af5..ab9876a59 (2 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/9dd1b8af51cf..ab9876a59832 
     
    $ git log 9dd1b8af5..ab9876a59 --date=short --no-merges --format='%ad %ae %s' 
    2026-03-29 marpan Set force_mv_inter_layer earlier in skip_inter_mode 
    2026-03-27 jzern av1_nonrd_pick_inter_mode_sb: add missing ref_frame_flags check 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
     
    Bug: 495477995, 495996858, 500600182 
    Fixed: 500600182 
    Change-Id: I88222975371a637865e185b07391a5a94a54c9bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7746328 
    Auto-Submit: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#2615} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [5baded2e60b157b76c8041d3c9dda1ad5f7b8e3f](https://chromiumdash.appspot.com/commit/5baded2e60b157b76c8041d3c9dda1ad5f7b8e3f)  

Date: Fri Apr 10 17:34:03 2026


---

### dx...@google.com (2026-05-28)

Project: aom  

Branch:  m144-7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://aomedia-review.googlesource.com/212504>

av1\_nonrd\_pick\_inter\_mode\_sb: add missing ref\_frame\_flags check

---


Expand for full commit details
```
     
    Before calling `set_block_source_sad()` ensure `LAST_FRAME` is 
    available. Fixes a crash that may present as a use after free (UAF). 
     
    Bug: 495477995, 495996858 
    Change-Id: I61452ce412fb9071c3370b4350ed8878013a8355

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`

---

Hash: 3d8513679f0a825d02999e3866495e19190a4d8c  

Date: Fri Mar 27 17:56:13 2026


---

### dx...@google.com (2026-05-29)

Project: aom  

Branch:  m144-7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://aomedia-review.googlesource.com/212523>

Set force\_mv\_inter\_layer earlier in skip\_inter\_mode

---


Expand for full commit details
```
     
    For nonrd_pickmode: move the setting of 
    force_mv_inter_layer earlier in the 
    skip_inter_mode_nonrd(), to make sure it always 
    get set (in case of false return in that function). 
     
    Thie prevents the usage of a scaled_ref in pickmode 
    (combined_motion search) when it has actually not been 
    set/scaled in av1_scale_references (before encoding). 
     
    Fixes a crash for use after free (UAF), reported 
    in the issues below. 
     
    Added svc unittest to generate the issue. Also added 
    assert check for scaled_ref in combined_motion_search. 
     
    Bug: 495477995, 495996858 
    Change-Id: I578d19156d97a50546edc9422bc3581566f1236e

```

---

Files:

- M `av1/encoder/nonrd_pickmode.c`
- M `test/svc_datarate_test.cc`

---

Hash: 725d73571b392cb6acdff4a72b8e98ca6f5ce87c  

Date: Mon Mar 30 03:27:20 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495996858)*
