# DCHECK-only validation of WebRTC APM output buffer size leads to heap buffer overflow from compromised renderer

| Field | Value |
|-------|-------|
| **Issue ID** | [493957495](https://issues.chromium.org/issues/493957495) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2026-03-19 |
| **Bounty** | $4,000.00 |

## Description

# DCHECK-only validation of WebRTC APM output buffer size leads to heap buffer overflow from compromised renderer

## Summary

A compromised renderer can cause a heap buffer overflow in the audio service process by sending crafted `AudioParameters` through the `blink.mojom.RendererAudioInputStreamFactory.CreateStream` Mojo interface. The constraint that the output buffer's `frames_per_buffer` must equal `sample_rate / 100` when WebRTC audio processing is enabled is enforced only by a `DCHECK_EQ`, which is compiled out in release builds. A renderer that supplies `frames_per_buffer=1` with `sample_rate=48000` causes the audio service to allocate a 1-frame output buffer while the WebRTC Audio Processing Module writes 480 frames into it, overflowing the heap allocation by approximately 1916 bytes. All desktop platforms are affected.

## Bisect

Introducing Commit: `d33edbcc63a9f12be07f68e392a6126d1a3b370c`

- Date: 2021-12-09
- Author: Sam Zackrisson
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/3309225>

## Root Cause

When a renderer requests an audio input stream with WebRTC audio processing enabled, it supplies `media::AudioParameters` that specify the desired output format. These parameters travel from the renderer through `RenderFrameAudioInputStreamFactory`, `ForwardingAudioStreamFactory`, `audio::StreamFactory`, `audio::InputStream`, and `audio::InputController` into `media::AudioProcessor` without any CHECK-level validation of the relationship between `sample_rate` and `frames_per_buffer`.

The `AudioProcessor` constructor contains the following assertion:

```
// media/webrtc/audio_processor.cc:287-293
CHECK(input_format_.IsValid());
CHECK(output_format_.IsValid());
if (webrtc_audio_processing_) {
  DCHECK_EQ(
      webrtc::AudioProcessing::GetFrameSize(output_format_.sample_rate()),
      output_format_.frames_per_buffer());
}

```

The two `CHECK` calls validate `IsValid()`, which only requires `frames_per_buffer > 0` and `frames_per_buffer <= 768000`. A parameter set of `{sample_rate=48000, frames_per_buffer=1}` passes this validation. The subsequent `DCHECK_EQ` verifies the 10ms alignment requirement, but this is stripped from release builds.

The constructor then allocates the output buffer using the unchecked `frames_per_buffer`:

```
// media/webrtc/audio_processor.cc:323-326
if (webrtc_audio_processing_) {
  output_bus_ = std::make_unique<AudioProcessorCaptureBus>(
      output_format_.channels(), output_format.frames_per_buffer());
}

```

With `frames_per_buffer=1`, this allocates a single-frame buffer. When audio data arrives, `ProcessData` constructs the APM output configuration from the sample rate, which determines a 480-frame write size:

```
// media/webrtc/audio_processor.cc:552-557
const webrtc::StreamConfig apm_output_config = webrtc::StreamConfig(
    output_format_.sample_rate(), num_apm_output_channels);

int err =
    ap->ProcessStream(process_ptrs.data(), CreateStreamConfig(input_format_),
                      apm_output_config, output_bus->channel_ptrs().data());

```

`webrtc::AudioProcessing::GetFrameSize(48000)` returns 480. The `ProcessStream` call writes 480 float samples through the raw `float*` channel pointers, which point into the 1-frame buffer. This produces a heap buffer overflow of 479 floats, or 1916 bytes.

The write target is a raw `float*` array inside an `AudioBus` allocation. No libc++ hardening, PartitionAlloc bucket isolation, or MiraclePtr protection applies to this access path.

## Reproduce

Tested at commit `d0f83d769eeed0b61ffc7d3c15172b2c257acf4e` on macOS (arm64).

Build configuration (`out/asan-release/args.gn`):

```
is_asan = true
is_debug = false
dcheck_always_on = false
is_component_build = true
target_cpu = "arm64"

```

Apply the renderer-side patch and build:

```
git apply issue_mojo034/patch.diff
autoninja -C ~/chromium/src/out/asan-release chrome

```

Launch:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --user-data-dir=/tmp/poc-audio \
  --use-fake-device-for-media-stream \
  --use-fake-ui-for-media-stream \
  issue_mojo034/poc.html

```

The audio service thread crashes within one second of the page loading.

```
==62908==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300008f750 at pc 0x0001170fa3d0 bp 0x00030a04e2a0 sp 0x00030a04e298
WRITE of size 16 at 0x60300008f750 thread T13
    #0 webrtc::FloatS16ToFloat(float const*, unsigned long, float*)
    #1 webrtc::AudioBuffer::CopyTo(webrtc::StreamConfig const&, float* const*)
    #2 webrtc::AudioProcessingImpl::ProcessStream(float const* const*, webrtc::StreamConfig const&, webrtc::StreamConfig const&, float* const*)
    #3 media::AudioProcessor::ProcessData(...)
    #4 media::AudioProcessor::ProcessCapturedAudio(media::AudioBus const&, base::TimeTicks, int, double)
    #5 audio::AudioProcessorHandler (via callback)
    #6 audio::ProcessingAudioFifo::ProcessAudioLoop(base::WaitableEvent*)

0x60300008f750 is located 0 bytes after 16-byte region [0x60300008f740,0x60300008f750)
allocated by thread T0 here:
    #0 __asan_memmove
    #1 base::AlignedAlloc(unsigned long, unsigned long)
    #2 base::AlignedUninit<float>(unsigned long, unsigned long)
    #3 media::AudioBus::AudioBus(int, int)
    #4 media::AudioProcessor::AudioProcessor(...)
    #5 media::AudioProcessor::Create(...)
    #6 audio::AudioProcessorHandler::AudioProcessorHandler(...)
    #7 audio::InputController::MaybeSetUpAudioProcessing(...)
    #8 audio::InputController::InputController(...)
    #9 audio::InputController::Create(...)
    #10 audio::InputStream::InputStream(...)
    #11 audio::StreamFactory::CreateInputStream(...)
    #12 media::mojom::AudioStreamFactoryStubDispatch::AcceptWithResponder(...)

Thread T13 created by T0 here:
    #5 audio::InputController::Record()
    #6 audio::InputStream::Record()
    #7 media::mojom::AudioInputStreamStubDispatch::Accept(...)

SUMMARY: AddressSanitizer: heap-buffer-overflow in webrtc::FloatS16ToFloat(float const*, unsigned long, float*)

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 894 B)
- [asan.log](attachments/asan.log) (text/plain, 32.8 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.1 KB)
- [bug_493957495.txt](attachments/bug_493957495.txt) (text/plain, 27.4 KB)

## Timeline

### ts...@google.com (2026-03-19)

Repro'd on linux / Chromium 146.0.7680.159 , asan trace attached.


### ts...@google.com (2026-03-19)

Tommi, could you perhaps suggest a reasonable owner for this issue? Thanks!

### ch...@google.com (2026-03-20)

Setting milestone because of s0/s1 severity.

### to...@chromium.org (2026-03-27)

Sam - can you take a look?

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  Tomas Gunnarsson [tommi@chromium.org](mailto:tommi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7710554>

Upgrade DCHECK\_EQ to CHECK\_EQ in audio\_processor.cc.

---


Expand for full commit details
```
     
    This ensures that the frame size check is performed in all build 
    configurations, not just debug builds. 
     
    Bug: 493957495 
    Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710554 
    Reviewed-by: Per Åhgren <peah@chromium.org> 
    Auto-Submit: Tomas Gunnarsson <tommi@chromium.org> 
    Commit-Queue: Per Åhgren <peah@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1606910}

```

---

Files:

- M `media/webrtc/audio_processor.cc`

---

Hash: [8708a22598eb84809063a257db7ffdcede2384ae](https://chromiumdash.appspot.com/commit/8708a22598eb84809063a257db7ffdcede2384ae)  

Date: Mon Mar 30 07:03:07 2026


---

### sa...@webrtc.org (2026-04-09)

From what I can tell, Tommi's fix addresses this issue. CHECKing the params in the same way as the general format `IsValid()` checks. We *could* close as fixed.

The current state still allows for abuse (Denial-of-Service) though, [docs](https://chromium.googlesource.com/chromium/src/+/main/docs/security/mojo.md#reportbadmessage-vs-check). This also concerns:

- the pre-existing `IsValid()` checks, unless we reject the configs at some earlier IPC boundary.
- [media::SincResampler](https://source.chromium.org/chromium/chromium/src/+/main:media/base/sinc_resampler.cc;l=182-184;drc=15be50893f87a32a6a12adea5051b701414e932f), which CHECKs additional requirements on what I think is originally an output stream's `AudioParameters`.

I will have a closer look. The alternatives I see are:

- Test these conditions at IPC boundary and flag the mojo message as bad on failure (== check audio processing criteria far away from the actual audio processing, messy)
- Test these conditions here, and raise the failure higher in the stack to abort stream creation (messy)
- Accept current state, allow compromised renderers to kill audio process

I don't know if there is a common view on how to handle these "extra" late-stage requirements on stream parameters?

+cc Olga, Dale, Thomas FYI

### je...@gmail.com (2026-04-10)

Thanks for the analysis, Sam. I agree this can be closed as fixed — Tommi's CL (<https://chromium-review.googlesource.com/7710554>) upgrades the DCHECK\_EQ to CHECK\_EQ, which converts the heap buffer overflow into a controlled crash, addressing the memory safety issue.

Regarding the remaining DoS concern: a compromised renderer being able to trigger a CHECK failure (and thus crash the audio service) is consistent with Chromium's threat model. The security boundary is designed to prevent a compromised renderer from escalating privileges or corrupting memory in other processes, not to prevent it from causing service disruptions. Crashing the audio process via a bad Mojo message is equivalent to the renderer simply refusing to cooperate, which it can always do.

So I'd suggest closing this as Fixed based on the current patch. The additional hardening options you outlined (IPC-boundary validation, propagating failures up the stack) would be nice defense-in-depth improvements but aren't necessary for resolving the security issue itself.

### sa...@webrtc.org (2026-04-15)

Reasoning in [comment #8](https://issues.chromium.org/issues/493957495#comment8) sgtm, same takeaway talking to Tommi offline.

### ch...@google.com (2026-04-16)

Requesting merge to M146 because latest trunk commit (1606910) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1606910) appears to be after M147 branch point (1596535).

### ch...@google.com (2026-04-16)

**M146** merge request created. **Please update [crbug/503210630](https://crbug.com/503210630) to have this merge reviewed.**

### ch...@google.com (2026-04-16)

**M147** merge request created. **Please update [crbug/503211574](https://crbug.com/503211574) to have this merge reviewed.**

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Tomas Gunnarsson [tommi@chromium.org](mailto:tommi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7785990>

[M146] Upgrade DCHECK\_EQ to CHECK\_EQ in audio\_processor.cc.

---


Expand for full commit details
```
     
    Original change's description: 
    > Upgrade DCHECK_EQ to CHECK_EQ in audio_processor.cc. 
    > 
    > This ensures that the frame size check is performed in all build 
    > configurations, not just debug builds. 
    > 
    > Bug: 493957495 
    > Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710554 
    > Reviewed-by: Per Åhgren <peah@chromium.org> 
    > Auto-Submit: Tomas Gunnarsson <tommi@chromium.org> 
    > Commit-Queue: Per Åhgren <peah@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1606910} 
     
    (cherry picked from commit 8708a22598eb84809063a257db7ffdcede2384ae) 
     
    Bug: 503210630,493957495 
    Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7785990 
    Reviewed-by: Sam Zackrisson <saza@chromium.org> 
    Commit-Queue: Sam Zackrisson <saza@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Mirko Bonadei <mbonadei@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3996} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/webrtc/audio_processor.cc`

---

Hash: [f8965a7ff32ffbaff77cc7c4d0fd1b4dbbe23bad](https://chromiumdash.appspot.com/commit/f8965a7ff32ffbaff77cc7c4d0fd1b4dbbe23bad)  

Date: Wed Apr 22 18:47:37 2026


---

### pe...@google.com (2026-04-22)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Tomas Gunnarsson [tommi@chromium.org](mailto:tommi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7786009>

[M147] Upgrade DCHECK\_EQ to CHECK\_EQ in audio\_processor.cc.

---


Expand for full commit details
```
     
    Original change's description: 
    > Upgrade DCHECK_EQ to CHECK_EQ in audio_processor.cc. 
    > 
    > This ensures that the frame size check is performed in all build 
    > configurations, not just debug builds. 
    > 
    > Bug: 493957495 
    > Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710554 
    > Reviewed-by: Per Åhgren <peah@chromium.org> 
    > Auto-Submit: Tomas Gunnarsson <tommi@chromium.org> 
    > Commit-Queue: Per Åhgren <peah@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1606910} 
     
    (cherry picked from commit 8708a22598eb84809063a257db7ffdcede2384ae) 
     
    Bug: 503211574,493957495 
    Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7786009 
    Commit-Queue: Mirko Bonadei <mbonadei@chromium.org> 
    Reviewed-by: Mirko Bonadei <mbonadei@chromium.org> 
    Reviewed-by: Sam Zackrisson <saza@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3485} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `media/webrtc/audio_processor.cc`

---

Hash: [c410f10052368c2d408cf888978d1001b660be2f](https://chromiumdash.appspot.com/commit/c410f10052368c2d408cf888978d1001b660be2f)  

Date: Wed Apr 22 18:59:06 2026


---

### aj...@google.com (2026-04-23)

Severity Medium as this has a precondition of a compromised renderer

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Baseline with bisect. Mildly mitigated (sandboxed/renderer) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-06-10)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7914103>
2. Low. There was no conflicts.
3. 146 and 147
4. Yes

### dx...@google.com (2026-06-15)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tomas Gunnarsson [tommi@chromium.org](mailto:tommi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7914103>

[M144-LTS] Upgrade DCHECK\_EQ to CHECK\_EQ in audio\_processor.cc.

---


Expand for full commit details
```
[M144-LTS] Upgrade DCHECK_EQ to CHECK_EQ in audio_processor.cc.

This ensures that the frame size check is performed in all build
configurations, not just debug builds.

(cherry picked from commit 8708a22598eb84809063a257db7ffdcede2384ae)

Bug: 493957495
Change-Id: I18bdcf58ef136d0d65c6a8cebd083dabe73299ec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7710554
Reviewed-by: Per Åhgren <peah@chromium.org>
Auto-Submit: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Per Åhgren <peah@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1606910}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7914103
Reviewed-by: Tomas Gunnarsson <tommi@chromium.org>
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Mohamed Omar <mohamedaomar@google.com>
Owners-Override: Mohamed Omar <mohamedaomar@google.com>
Cr-Commit-Position: refs/branch-heads/7559@{#5019}
Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `media/webrtc/audio_processor.cc`

---

Hash: [0ab8989b74e766ffea63335fa586cbc1fa6ea758](https://chromiumdash.appspot.com/commit/0ab8989b74e766ffea63335fa586cbc1fa6ea758)  

Date: Mon Jun 15 11:13:52 2026


---

### ch...@google.com (2026-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493957495)*
