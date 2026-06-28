# Use-after-free in AudioRendererMixerInput via setSinkId/createMediaElementSource race

| Field | Value |
|-------|-------|
| **Issue ID** | [492218537](https://issues.chromium.org/issues/492218537) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $4,000.00 |

## Description

# Use-after-free in AudioRendererMixerInput via setSinkId/createMediaElementSource race

## Summary

A race condition between `HTMLMediaElement.setSinkId()` and `AudioContext.createMediaElementSource()` causes a use-after-free of an `AudioRendererMixerInput` object. The asynchronous device-switch callback `OnDeviceSwitchReady` captures stale state snapshots of `mixer_` and `playing_` without holding `sink_lock_`, then proceeds to re-register the input with a new mixer based on those snapshots. If `SetClient()` runs concurrently on the main thread and drops the provider's reference to the input, the callback becomes the sole owner; when it completes, the input is destroyed while still registered in the mixer's `error_callbacks_` set and the `AudioConverter`'s `transform_inputs_` list. Subsequent audio rendering on the AudioOutputDevice thread dereferences the dangling pointers, producing a heap-use-after-free. This affects all desktop platforms (Linux, macOS, Windows) and requires at least two audio output devices to be present.

## Bisect

Introducing Commit: `41607b54686f80bc672c294161ca0da1cf49f89f`

- Date: 2018-11-30
- Author: Dale Curtis
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1347795>

This commit converted the `<audio>` pipeline to use asynchronous device info requests. The prior implementation used a static helper for `OnDeviceSwitchReady` that could safely outlive the pipeline, but the conversion made it a non-static member function bound via `RetainedRef(this)` without introducing the synchronization necessary to protect against concurrent `SetClient()` calls.

## Root Cause

`AudioRendererMixerInput` is explicitly documented as not thread-safe. Its header states that callers should rely on `WebAudioSourceProviderImpl::sink_lock_` to serialize access between the main thread (WebAudio APIs) and the media thread (HTMLMediaElement APIs). The `OnDeviceSwitchReady` callback violates this contract: it runs on the media thread's task runner without acquiring `sink_lock_`, yet reads and writes `mixer_`, `playing_`, `callback_`, and `sink_`.

When `SwitchOutputDevice()` initiates an asynchronous device query, it binds the completion callback with `RetainedRef(this)`:

```
// audio_renderer_mixer_input.cc:229-232
new_sink->GetOutputDeviceInfoAsync(
    blink::BindOnce(&AudioRendererMixerInput::OnDeviceSwitchReady,
                    blink::RetainedRef(this), std::move(callback), new_sink));

```

When the async query completes, `OnDeviceSwitchReady` snapshots the current state and then tears down and rebuilds the mixer connection:

```
// audio_renderer_mixer_input.cc:327-353
const bool has_mixer = !!mixer_;
const bool is_playing = playing_;

// ... Stop old sink, update device info ...

auto callback = callback_;
Stop();
callback_ = callback;

if (has_mixer) {
  Start();           // Registers in new mixer's error_callbacks_
  if (is_playing) {
    Play();          // Registers in AudioConverter's transform_inputs_
  }
}

```

The race window opens between the state snapshot and the `Start()`/`Play()` calls. During this window, `AudioContext.createMediaElementSource()` on the main thread synchronously calls `WebAudioSourceProviderImpl::SetClient()`. With the `kDelayStopForMediaElementSourceNode` feature disabled (the default), `SetClient()` acquires `sink_lock_` and drops the provider's reference to the `AudioRendererMixerInput`:

```
// web_audio_source_provider_impl.cc:147-155
if (!base::FeatureList::IsEnabled(kDelayStopForMediaElementSourceNode)) {
  if (sink_) {
    sink_->Stop();
    sink_ = nullptr;   // Drops scoped_refptr<AudioRendererMixerInput>
  }
}

```

After `SetClient()` returns, the `RetainedRef` inside the pending `OnDeviceSwitchReady` callback is the only remaining reference to the `AudioRendererMixerInput`. When the callback resumes on the media thread, it uses stale `has_mixer = true` and `is_playing = true` to call `Start()` and `Play()`, which register the input with a freshly obtained mixer via `AddErrorCallback(this)` and `AddMixerInput(params_, this)`. The mixer stores these as raw pointers:

```
// audio_renderer_mixer.h:84-85
base::flat_set<raw_ptr<AudioRendererMixerInput, CtnExperimental>>
    error_callbacks_ GUARDED_BY(lock_);

```
```
// audio_converter.h:129-130
typedef std::list<raw_ptr<InputCallback, CtnExperimental>> InputCallbackSet;
InputCallbackSet transform_inputs_;

```

When `OnDeviceSwitchReady` returns and its `BindState` is destroyed, the `RetainedRef` releases the last reference, freeing the 440-byte `AudioRendererMixerInput` object. The destructor only contains `DCHECK(!started_)` and `DCHECK(!mixer_)`, which are compiled out in Release and ASAN builds, so it does not unregister from the mixer. The `AudioOutputDevice` thread then enters `AudioRendererMixer::Render()`, which calls `aggregate_converter_.ConvertWithInfo()`, iterating `transform_inputs_` and calling `ProvideInput()` on the dangling pointer.

The `raw_ptr<T, CtnExperimental>` annotations provide BackupRefPtr protection in production Release builds with PartitionAlloc, but ASAN replaces the allocator, disabling this mitigation entirely. In Release builds without ASAN, the `CtnExperimental` tag enables BRP quarantine that would catch the dangling access, but the underlying race condition and object lifecycle bug remain.

## Reproduce

Tested at commit `457566e1c0b41`. Apply `patch.diff` (adds a 500ms sleep in `OnDeviceSwitchReady` to widen the race window), then build and run:

```
git apply issue_setsinkid_mixer_uaf/patch.diff
autoninja -C out/asan-release chrome

```

A virtual audio sink is required if no secondary hardware output is available:

```
pactl load-module module-null-sink sink_name=virtual_out sink_properties=device.description=VirtualOutput

```

Launch:

```
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --autoplay-policy=no-user-gesture-required \
  --use-fake-device-for-media-stream \
  --use-fake-ui-for-media-stream \
  --user-data-dir=/tmp/poc-$(date +%s) \
  issue_setsinkid_mixer_uaf/poc.html

```

The renderer process crashes with heap-use-after-free within seconds. Full ASAN log:

```
==3681971==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c56d3894650 at pc 0x7f1749df1dae bp 0x7b11cfffad50 sp 0x7b11cfffad48
READ of size 8 at 0x7c56d3894650 thread T19 (AudioOutputDevi)
    #0 0x7f1749df1dad in media::AudioConverter::SourceCallback(int, media::AudioBus*) media/base/audio_converter.cc:224:33
    #1 0x7f1749df0c43 in media::AudioConverter::ProvideInput(int, media::AudioBus*) media/base/audio_converter.cc:266:5
    #2 0x7f1749df341d in base::internal::Invoker<...> base/functional/bind_internal.h:740:12
    #3 0x7f1749e1dbd0 in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(...) base/functional/callback.h:346:12
    #4 0x7f1749eb30ea in media::MultiChannelResampler::ProvideInput(int, int, float*) media/base/multi_channel_resampler.cc:101:14
    ...
    #9 0x7f1749df2ee8 in media::AudioConverter::ConvertWithInfo(...) media/base/audio_converter.cc:160:19
    #10 0x7f1749e92eb7 in media::LoopbackAudioConverter::ProvideInput(...) media/base/loopback_audio_converter.cc:21:20
    #11 0x7f1749df14a2 in media::AudioConverter::SourceCallback(int, media::AudioBus*) media/base/audio_converter.cc:224:33
    #12 0x7f1749df2f31 in media::AudioConverter::ConvertWithInfo(...) media/base/audio_converter.cc:157:5
    #13 0x7f16e9658328 in blink::AudioRendererMixer::Render(...) audio_renderer_mixer.cc:155:24
    #14 0x7f1749d4cde2 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) audio_output_device_thread_callback.cc:107:21
    #15 0x7f1749d0a045 in media::AudioDeviceThread::ThreadMain() audio_device_thread.cc:106:16

0x7c56d3894650 is located 16 bytes inside of 440-byte region [0x7c56d3894640,0x7c56d38947f8)
freed by thread T14 (Media) here:
    #0 0x55ab875a2cc2 in operator delete(void*, unsigned long)
    #1 0x7f16e9661a35 in base::internal::BindState<...>::Destroy(...) base/memory/ref_counted.h:438:5

previously allocated by thread T0 (chrome) here:
    #0 0x55ab875a20bd in operator new(unsigned long)
    #1 0x7f16e9662184 in blink::AudioRendererMixerManager::CreateInput(...) base/memory/scoped_refptr.h:151:12
    #2 0x7f16e964e44e in blink::AudioDeviceFactory::NewMixableSink(...) audio_device_factory.cc:151:26

SUMMARY: AddressSanitizer: heap-use-after-free media/base/audio_converter.cc:224:33 in media::AudioConverter::SourceCallback(int, media::AudioBus*)

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw_ptr<T> object prior to this crash.

```

The complete untruncated ASAN log is in `asan.log`.

## References

- [audio\_renderer\_mixer\_input.cc (OnDeviceSwitchReady)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc;l=308-361)
- [audio\_renderer\_mixer\_input.h (class declaration)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.h;l=37-158)
- [web\_audio\_source\_provider\_impl.cc (SetClient)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_audio_source_provider_impl.cc;l=138-184)
- [audio\_renderer\_mixer.h (error\_callbacks\_ / raw\_ptr)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media/audio/audio_renderer_mixer.h;l=84-85)
- [audio\_converter.h (transform\_inputs\_ / raw\_ptr)](https://source.chromium.org/chromium/chromium/src/+/main:media/base/audio_converter.h;l=129-130)
- [Introducing CL 1347795](https://chromium-review.googlesource.com/c/chromium/src/+/1347795)

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 4.0 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 30.7 KB)

## Timeline

### je...@gmail.com (2026-03-13)

Due to the need for audio equipment and sleep, please do not use ClusterFuzz to reproduce this vulnerability, as it is not very easy to replicate. If you encounter any difficulties during the reproduction process, feel free to let me know, and I will provide assistance.

And I checked, and this might indeed be protected by MiraclePtr, but I'm not entirely sure. Please verify it as well.

### th...@chromium.org (2026-03-13)

[security shepherd] I can reproduce this on linux on M148 with the patch. It required an additional gn arg `dcheck_always_on = false` because otherwise I was hitting a DCHECK. Setting the Found In to current extended stable based on the bisect CL. Setting high severity for UAF in renderer.

My miracle pointer note is different:
MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw\_ptr<T> object prior to this crash.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

Based on the description, it seems that the use is coming after the free, but I have not taken a closer look.

jophba@: Could you PTAL? Also, could you please:

1. Confirm that the race condition patch is valid. (e.g. do we expect that there are production cases without the patch that could hit this?)
2. Confirm that the use is after the free.

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7673253>

Ensure AudioRendererMixer holds lock during sink switch

---


Expand for full commit details
```
     
    This guards `switch_output_device_in_progress_` with a lock that 
    can be held during the final phase of a setSinkId() operation 
    within the AudioRendererMixerInput. It ensures that if Stop() 
    is called, we don't incorrectly reconnect the new sink, and if 
    a device changes is in flight, that we stall the Stop() call. 
     
    R=tguilbert 
     
    Fixed: 492218537 
    Change-Id: I9ec6efb9678762a22b1b1c8a2f8918771c264678 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673253 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600910}

```

---

Files:

- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.h`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input_test.cc`

---

Hash: [fccaeb9e0967fdc628a6057c4140d2be7649a706](https://chromiumdash.appspot.com/commit/fccaeb9e0967fdc628a6057c4140d2be7649a706)  

Date: Wed Mar 18 00:33:03 2026


---

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1600910) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1600910) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### da...@chromium.org (2026-03-18)

1. <https://chromium-review.googlesource.com/7673253>
2. No, we should let this soak for a while.
3. Yes, it touches core audio playback surfaces.
4. Yes, same as #3.
5. No

I'd suggest we only merge to 147 and then later back port to LTS if everything looks okay.

### ch...@google.com (2026-03-19)

Merge review required: M147 is already shipping to beta.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-19)

Merge review required: M146 is already shipping to stable.

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

### dr...@chromium.org (2026-03-19)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### da...@chromium.org (2026-03-19)

I think we should limit to 147 given the difficulty to trigger w/o patching Chromium. I want to make sure this doesn't introduce any deadlock in the audio pipeline.

### da...@chromium.org (2026-03-19)

147 merge here <https://chromium-review.git.corp.google.com/c/chromium/src/+/7685390>

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7685390>

[M147] Ensure AudioRendererMixer holds lock during sink switch

---


Expand for full commit details
```
     
    This guards `switch_output_device_in_progress_` with a lock that 
    can be held during the final phase of a setSinkId() operation 
    within the AudioRendererMixerInput. It ensures that if Stop() 
    is called, we don't incorrectly reconnect the new sink, and if 
    a device changes is in flight, that we stall the Stop() call. 
     
    R=tguilbert 
     
    (cherry picked from commit fccaeb9e0967fdc628a6057c4140d2be7649a706) 
     
    Fixed: 492218537 
    Change-Id: I9ec6efb9678762a22b1b1c8a2f8918771c264678 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673253 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600910} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685390 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#893} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.h`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input_test.cc`

---

Hash: [131bbd6408421568de871ae65cdf49431925cd7d](https://chromiumdash.appspot.com/commit/131bbd6408421568de871ae65cdf49431925cd7d)  

Date: Thu Mar 19 20:27:57 2026


---

### pe...@google.com (2026-03-19)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### da...@chromium.org (2026-03-19)

1. No, it's been an issue since M73.
2. No.

### ch...@google.com (2026-03-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@chromium.org (2026-03-24)

See [comment#13](https://issues.chromium.org/issues/492218537#comment13), we should limit this to 147 unless otherwise necessary.

### dr...@chromium.org (2026-03-24)

Sure, seems reasonable. We don't need to merge this to M146.

### pe...@google.com (2026-04-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-01)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7692280
2. Low - There was a trivial conflict.
3. 147
4. Yes, the bug has existed since M73.

### pe...@google.com (2026-04-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-16)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7691580
2. Low - There was no conflict.
3. 147
4. Yes, the bug has existed since M73.

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7691580>

[M144-LTS] Ensure AudioRendererMixer holds lock during sink switch

---


Expand for full commit details
```
     
    This guards `switch_output_device_in_progress_` with a lock that 
    can be held during the final phase of a setSinkId() operation 
    within the AudioRendererMixerInput. It ensures that if Stop() 
    is called, we don't incorrectly reconnect the new sink, and if 
    a device changes is in flight, that we stall the Stop() call. 
     
    R=tguilbert 
     
    Fuchsia-Binary-Size: Cherry-pick the CL to M144. 
     
    (cherry picked from commit fccaeb9e0967fdc628a6057c4140d2be7649a706) 
     
    Fixed: 492218537 
    Change-Id: I9ec6efb9678762a22b1b1c8a2f8918771c264678 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673253 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1600910} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7691580 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4842} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.cc`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input.h`
- M `third_party/blink/renderer/modules/media/audio/audio_renderer_mixer_input_test.cc`

---

Hash: [da1c7dba6bd7375c08d52102ab2cc4ae3c87034d](https://chromiumdash.appspot.com/commit/da1c7dba6bd7375c08d52102ab2cc4ae3c87034d)  

Date: Thu Apr 30 06:42:09 2026


---

### sp...@google.com (2026-06-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Mildly mitigated (sandboxed/renderer) plus bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492218537)*
