# OOB Write in FFTConvolver of WebAudio

| Field | Value |
|-------|-------|
| **Issue ID** | [487495466](https://issues.chromium.org/issues/487495466) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $11,000.00 |

## Description

### Summary

A heap-buffer-overflow (WRITE) occurs in [`FFTConvolver::Process()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/fft_convolver.cc;l=43) when `OfflineAudioContext` is created with a non-power-of-2 `renderSizeHint`. Its internal `read_write_index_` accumulates `frames_to_process` each call and only resets when it equals the power-of-2 `half_size`. A non-power-of-2 quantum never hits that reset, so the index grows past `input_buffer_` and a subsequent `memcpy` writes out of bounds.

### Details

[`OfflineAudioContext::Create()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/offline_audio_context.cc;l=145) parses the `renderSizeHint` option when the `WebAudioConfigurableRenderQuantum` runtime flag is enabled. The value is validated by [`IsValidRenderQuantumSize()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/audio_utilities.cc;l=138), which only enforces a range check:

From `audio_utilities.cc`:

```
bool IsValidRenderQuantumSize(uint32_t render_quantum_size, float sample_rate) {
  return render_quantum_size >= MinRenderQuantumSize() &&
         render_quantum_size <= MaxRenderQuantumSize(sample_rate);
}

```

There is no power-of-2 constraint. Any integer in `[1, 6 * sample_rate]` passes. The accepted value propagates to `BaseAudioContext` as the render quantum size.

When a `PannerNode` with `panningModel: 'HRTF'` is connected, [`PannerHandler::Initialize()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/panner_handler.cc;l=324) creates the panner with the non-power-of-2 render quantum:

```
panner_ = Panner::Create(panning_model_, Context()->sampleRate(),
                         GetDeferredTaskHandler().RenderQuantumFrames(),
                         listener_handler_->HrtfDatabaseLoader());

```

This creates an [`HRTFPanner`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/hrtf_panner.cc;l=79) whose internal `FFTConvolver` objects are initialized with a power-of-2 FFT size derived from the sample rate (512 for 44100 Hz). During rendering, `HRTFPanner::Pan()` calls `FFTConvolver::Process()` with `frames_to_process` equal to the non-power-of-2 render quantum.

The overflow occurs inside `FFTConvolver::Process()`. From [`fft_convolver.cc`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/fft_convolver.cc;l=43):

```
void FFTConvolver::Process(const FFTFrame* fft_kernel,
                           const float* source_p,
                           float* dest_p,
                           uint32_t frames_to_process) {
  unsigned half_size = FftSize() / 2;

  bool is_good =
      !(half_size % frames_to_process && frames_to_process % half_size);
  DCHECK(is_good);

  size_t number_of_divisions =
      half_size <= frames_to_process ? (frames_to_process / half_size) : 1;
  size_t division_size =
      number_of_divisions == 1 ? frames_to_process : half_size;

  for (size_t i = 0; i < number_of_divisions;
       ++i, source_p += division_size, dest_p += division_size) {
    float* input_p = input_buffer_.Data();

    DCHECK_LE(read_write_index_ + division_size, input_buffer_.size());

    memcpy(input_p + read_write_index_, source_p,
           sizeof(float) * division_size);

    // ...
    read_write_index_ += division_size;

    if (read_write_index_ == half_size) {
      // Perform FFT, multiply, inverse FFT, overlap-add...
      read_write_index_ = 0;
    }
  }
}

```

When `frames_to_process = 131` and `half_size = 256`:

- The DCHECK at line 54 (`is_good`) evaluates to `false` but is compiled out in release.
- `number_of_divisions = 1`, `division_size = 131`.
- `read_write_index_` accumulates: 0 → 131 → 262 → 393. The equality check `read_write_index_ == half_size` (131 ≠ 256, 262 ≠ 256, 393 ≠ 256) never triggers, so the index never resets.
- On the fourth call, `memcpy(input_p + 393, source_p, 131 * sizeof(float))` writes to byte offsets [393, 524) of a 512-element buffer, overflowing with OOB by 12 floats (48 bytes).

### Bisection

This issue is introduced by the commit: `eb71f9f80d543fb285987489376223e1c5ad711b` Pipe numeric renderSizeHint to deferred task handler.

This commit connected the user-supplied `renderSizeHint` value to the audio processing pipeline without adding a power-of-2 constraint, enabling non-power-of-2 render quanta to reach `FFTConvolver`, `DirectConvolver`, `UpSampler`, and `DownSampler`.

### Reproduction

Download the chromium from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1590057.zip`

Run chromium with:

```
./chrome --no-sandbox --enable-experimental-web-platform-features poc.html

```

You would get the OOB crash shown in `asan.txt`.

### Suggested Fix

`IsValidRenderQuantumSize()` in `audio_utilities.cc` should reject values that are not powers of two, since `FFTConvolver::Process()`, `HRTFPanner::Pan()`, `UpSampler::Process()`, and `DownSampler::Process()` all assume power-of-2 render quanta for buffer sizing, index arithmetic, and FFT boundary alignment. A minimal fix adds a power-of-2 check:

```
bool IsValidRenderQuantumSize(uint32_t render_quantum_size, float sample_rate) {
  return render_quantum_size >= MinRenderQuantumSize() &&
         render_quantum_size <= MaxRenderQuantumSize(sample_rate) &&
         (render_quantum_size & (render_quantum_size - 1)) == 0;
}

```

Additionally, the existing DCHECKs in `FFTConvolver::Process()` and `HRTFPanner::Pan()` should be turn into CHECKs.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 41.4 KB)
- [poc.html](attachments/poc.html) (text/html, 418 B)

## Timeline

### li...@chromium.org (2026-02-25)

@mj...@chromium.org do you mind taking a look or rerouting as necessary? thanks!

### mj...@chromium.org (2026-02-25)

Yes, I'm the right person for this.

Mitigation plan would be to strengthen assertions, and replace unsafe operations with safe operations if possible. I am gardener today so I don't have time to look into this deeply right now. Note that renderSizeHint can only be set with a command-line switch or via OT which is currently closed.

### mj...@chromium.org (2026-03-06)

I have been working on fixing unsafe operations but haven't gotten to this yet.

### 24...@project.gserviceaccount.com (2026-03-09)

ClusterFuzz testcase 5404727386767360 appears to be flaky, updating reproducibility hotlist.

### mj...@chromium.org (2026-03-10)

Increasing priority/severity to match similar issues.

### mj...@chromium.org (2026-03-12)

May be fixed by <https://crrev.com/c/7656645>

### he...@gmail.com (2026-03-12)

Yes, the CL 7656645 indeed fix this issue. We can further mark this issue as fixed.

Many thanks!

### mj...@chromium.org (2026-03-12)

Thank you for verifying, setting to fixed.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487495466)*
