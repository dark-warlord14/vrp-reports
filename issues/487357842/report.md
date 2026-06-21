# OOB in WaveShaper of WebAudio

| Field | Value |
|-------|-------|
| **Issue ID** | [487357842](https://issues.chromium.org/issues/487357842) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $3,000.00 |

## Description

### Summary

OOB occurs in Blink's WebAudio `DirectConvolver` when `OfflineAudioContext` is configured with a `renderSizeHint` smaller than 128. The `UpSampler` used by `WaveShaperNode` creates a [`DirectConvolver`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/direct_convolver.cc;l=43) whose `input_block_size` equals the render quantum but whose convolution kernel is fixed at 128 taps (`kDefaultKernelSize`). When `input_block_size < kernel_size`, the source pointer passed to [`vector_math::Conv()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/vector_math.cc;l=76) is computed as `buffer_.Data() + input_block_size_ - kernel_size + 1`, which underflows to an address before the heap allocation. The SSE/AVX Conv inner loop then reads from this negative offset, causing a heap read underflow.

> NOTE: this issue is different with the issue I previous report in 487495466 since their root causes are different.

### Details

When the `WebAudioConfigurableRenderQuantum` feature is enabled, [`OfflineAudioContext::Create()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/offline_audio_context.cc;l=145) accepts an arbitrary `renderSizeHint` value. The only validation is a range check in [`IsValidRenderQuantumSize()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/audio_utilities.cc;l=138) that accepts any integer in `[1, 6 * sample_rate]` with no power-of-2 or minimum-size constraint.

A `WaveShaperNode` with `oversample: '2x'` triggers lazy initialization of oversampling in [`WaveShaperKernel::LazyInitializeOversampling()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/wave_shaper_handler.cc;l=88):

```
void LazyInitializeOversampling(unsigned render_quantum_frames) {
  if (!IsInitialized()) {
    temp_buffer_ =
        std::make_unique<AudioFloatArray>(render_quantum_frames * 2);
    up_sampler_ = std::make_unique<UpSampler>(render_quantum_frames);
    down_sampler_ = std::make_unique<DownSampler>(render_quantum_frames * 2);
    // ...
  }
}

```

The [`UpSampler`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/up_sampler.cc;l=79) constructor creates a `DirectConvolver` when `input_block_size <= 128`, passing the render quantum as the block size and a fixed 128-tap kernel:

```
UpSampler::UpSampler(unsigned input_block_size)
    : input_block_size_(input_block_size),
      temp_buffer_(input_block_size),
      input_buffer_(input_block_size * 2) {
  std::unique_ptr<AudioFloatArray> convolution_kernel =
      MakeKernel(kDefaultKernelSize);  // kDefaultKernelSize = 128
  if (input_block_size_ <= 128) {
    direct_convolver_ = std::make_unique<DirectConvolver>(
        input_block_size_, std::move(convolution_kernel));

```

The `DirectConvolver` constructor allocates `buffer_` with size `2 * input_block_size` and stores the 128-element kernel. During processing, [`DirectConvolver::Process()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/direct_convolver.cc;l=55) computes the source pointer for the convolution:

```
void DirectConvolver::Process(const float* source_p,
                              float* dest_p,
                              uint32_t frames_to_process) {
  DCHECK_EQ(frames_to_process, input_block_size_);

  size_t kernel_size = ConvolutionKernelSize();
  DCHECK_LE(kernel_size, input_block_size_);  // FAILS when input_block_size < 128

  float* input_p = buffer_.Data() + input_block_size_;

  memcpy(input_p, source_p, sizeof(float) * frames_to_process);

  Conv(input_p - kernel_size + 1, 1,
       kernel_p + kernel_size - 1, -1, dest_p, 1,
       frames_to_process, kernel_size, &prepared_convolution_kernel_);

```

The Conv source pointer is `input_p - kernel_size + 1 = buffer_.Data() + input_block_size_ - 128 + 1`. When `input_block_size_ < 128`, this evaluates to a negative offset from `buffer_.Data()`. For example, with `input_block_size_ = 96`:

- `source_p = buffer_.Data() + 96 - 127 = buffer_.Data() - 31`

The DCHECK at line 61 (`kernel_size <= input_block_size_`) would catch this, but it is compiled out in release.

The underflowed pointer reaches the x86 Conv dispatcher in [`vector_math_x86.h`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/cpu/x86/vector_math_x86.h;l=111). When `frames_to_process` is a multiple of 8, the AVX path is selected:

```
if (CPUSupportsAVX() && (filter_size & ~avx::kFramesToProcessMask) == 0u) {
  CHECK_EQ(frames_to_process & ~avx::kFramesToProcessMask, 0u);
  avx::Conv(source_p, prepared_filter_p, dest_p, frames_to_process,
            filter_size);
  return;
}

```

The AVX Conv inner loop in [`vector_math_impl.h`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/cpu/x86/vector_math_impl.h;l=62) executes `_mm256_loadu_ps(source_p + k)` which reads 8 floats (32 bytes) starting from the underflowed address, triggering the ASAN-detected heap-buffer-overflow READ:

```
while (dest_p < dest_end_p) {
  MType m_convolution_sum = MM_PS(setzero)();
  for (size_t i = 0; i < filter_size; i += kPackedFloatsPerRegister) {
    for (size_t j = 0; j < kPackedFloatsPerRegister; ++j) {
      size_t k = i + j;
      m_source = MM_PS(loadu)(source_p + k);  // source_p is before buffer start
      m_product = MM_PS(mul)(reversed_filter[kReversedFilterStride * k], m_source);
      m_convolution_sum = MM_PS(add)(m_convolution_sum, m_product);
    }
  }
  // ...
}

```

Note: the `renderSizeHint` must be a multiple of 8 (for AVX) or 4 (for SSE) to fit the alignment check. Values such as 96, 64, or 32 satisfy the alignment requirement and produce the underflow with OOB memory access.

### Bisection

This issue is introduced by the commit `eb71f9f80d543fb285987489376223e1c5ad711b`.

#### Reproduction Case

Download the chromium from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1590057.zip`

Run chromium with:

```
./chrome --no-sandbox --enable-experimental-web-platform-features poc.html

```

You would get the OOB crash shown in `asan.txt`.

### Suggested Fix

Turn the DCHECK in `DirectConvolver::Process()` at line 61 (`DCHECK_LE(kernel_size, input_block_size_)`) into CHECK to abort cleanly when the pointer underflowed.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 41.7 KB)
- [poc.html](attachments/poc.html) (text/html, 478 B)

## Timeline

### li...@chromium.org (2026-02-25)

@mj...@chromium.org do you mind taking a look or rerouting as necessary? thanks!

### mj...@chromium.org (2026-02-25)

May already be mitigated by <https://crrev.com/c/7586734> -- submitter please try running on canary (found in version is not set so I don't know what version this was discovered in).

### he...@gmail.com (2026-02-25)

I can still reproduced on the latest canary in <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1589819.zip>, if this is the canary version (correct me if I'm wrong) I think that commit might not mitigate this issues.

I'll try to reproduce it on my manual build on HEAD, will need couple of hours for manual building. Many thanks.

### pe...@google.com (2026-02-25)

Thank you for providing more feedback. Adding the requester to the CC list.

### he...@gmail.com (2026-02-26)

Hi, I can reproduce it on the ToT (on commit b11ef27c5cd9b119d9f2555be73684b226361b90) for my manual asan build. The <https://crrev.com/c/7586734> doesn't mitigate it since it hasn't touch the checks in the x86 Conv dispatcher.

Many thanks!

### mj...@chromium.org (2026-02-26)

[#comment6](https://issues.chromium.org/issues/487357842#comment6) Thank you for confirming, and for the report. I will look at further mitigations.

### he...@gmail.com (2026-03-05)

friendly ping - maybe we can land a DCHECK into CHECK fix to mitigate it.

Many thanks!

### mj...@chromium.org (2026-03-05)

Thank you for checking in. I'm currently looking at converting the memory-unsafe operations to safe operations, which should also mitigate this issue.

### mj...@chromium.org (2026-03-05)

<https://crrev.com/c/7640131> may mitigate this, although I haven't checked directly yet and I am still working on a more comprehensive solution.

### mj...@chromium.org (2026-03-10)

Increasing priority/severity to match similar issues.

### dx...@google.com (2026-03-10)

Project: chromium/src  

Branch:  main  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7640131>

Replace UNSAFE\_TODO in DirectConvolver with safe operations

---


Expand for full commit details
```
     
    This required updating some calling functions to use span instead of 
    raw pointers. 
     
    This should cause no functional change. 
     
    Bug: 401184803 
    Bug: 487357842 
    Change-Id: I6943414d32eb0948d74e42e9c923615505d31958 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7640131 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597150}

```

---

Files:

- M `third_party/blink/renderer/platform/audio/direct_convolver.cc`
- M `third_party/blink/renderer/platform/audio/direct_convolver.h`
- M `third_party/blink/renderer/platform/audio/reverb_convolver.cc`
- M `third_party/blink/renderer/platform/audio/reverb_convolver_stage.cc`
- M `third_party/blink/renderer/platform/audio/reverb_convolver_stage.h`
- M `third_party/blink/renderer/platform/audio/reverb_input_buffer.cc`
- M `third_party/blink/renderer/platform/audio/reverb_input_buffer.h`
- M `third_party/blink/renderer/platform/audio/up_sampler.cc`

---

Hash: [2078530c5eb2237e877d65d53375306dedd1cdb0](https://chromiumdash.appspot.com/commit/2078530c5eb2237e877d65d53375306dedd1cdb0)  

Date: Tue Mar 10 17:06:03 2026


---

### 24...@project.gserviceaccount.com (2026-03-11)

ClusterFuzz testcase 6573202901762048 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1597149:1597152

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dr...@chromium.org (2026-03-15)

No crashes in Canary, so approving merge to M146 and M147.

### mj...@chromium.org (2026-03-16)

Merge to M146 will require pulling in some additional changes. M147 seems like it can be a clean cherry-pick.

### dr...@chromium.org (2026-03-16)

Let me know if you think there's additional stability risk to merging to M146. If we don't think existing pre-Stable channels can prove your code doesn't crash, it might not be worth merging.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7670819>

[M147] Replace UNSAFE\_TODO in DirectConvolver with safe operations

---


Expand for full commit details
```
     
    This required updating some calling functions to use span instead of 
    raw pointers. 
     
    This should cause no functional change. 
     
    (cherry picked from commit 2078530c5eb2237e877d65d53375306dedd1cdb0) 
     
    Bug: 401184803 
    Bug: 487357842 
    Change-Id: I6943414d32eb0948d74e42e9c923615505d31958 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7640131 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597150} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670819 
    Cr-Commit-Position: refs/branch-heads/7727@{#692} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/platform/audio/direct_convolver.cc`
- M `third_party/blink/renderer/platform/audio/direct_convolver.h`
- M `third_party/blink/renderer/platform/audio/reverb_convolver.cc`
- M `third_party/blink/renderer/platform/audio/reverb_convolver_stage.cc`
- M `third_party/blink/renderer/platform/audio/reverb_convolver_stage.h`
- M `third_party/blink/renderer/platform/audio/reverb_input_buffer.cc`
- M `third_party/blink/renderer/platform/audio/reverb_input_buffer.h`
- M `third_party/blink/renderer/platform/audio/up_sampler.cc`

---

Hash: [e93e3fe0f3f22c1577a25ff66fc01cc1ffdaef90](https://chromiumdash.appspot.com/commit/e93e3fe0f3f22c1577a25ff66fc01cc1ffdaef90)  

Date: Wed Mar 18 06:31:57 2026


---

### mj...@chromium.org (2026-03-19)

[#comment16](https://issues.chromium.org/issues/487357842#comment16) We would at least need to pull in <https://crrev.com/c/7627464> as well. I don't think there is a significant stability concern, but there may be other CLs that are necessary too.

### ch...@google.com (2026-03-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dr...@chromium.org (2026-03-19)

Okay, I think we probably don't want the complexity then given the severity of this bug. I'll go ahead and remove the merge approval for M146.

### mj...@chromium.org (2026-03-19)

Thank you, I agree. M147 already landed, so I will abandon the M146 cherry-pick and then all merges are resolved.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. Moderately mitigated (sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487357842)*
