# Use-After-Free in WebMediaPlayerMS::OnFirstFrameReceived

| Field | Value |
|-------|-------|
| **Issue ID** | [448046109](https://issues.chromium.org/issues/448046109) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 141.0.7358.0 |
| **Reporter** | ss...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2025-09-29 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. chrome.exe --js-flags="--stress-incremental-marking --expose-gc" --no-sandbox

# Problem Description

In the `MaybeCreateWatchTimeReporter` function below, a call to GarbageCollector is possible, which causes Use-After-Free.

```
void WebMediaPlayerMS::OnFirstFrameReceived(
    media::VideoTransformation video_transform,
    bool is_opaque) {
  DVLOG(1) << __func__;
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);

  has_first_frame_ = true;
  OnTransformChanged(video_transform);
  OnOpacityChanged(is_opaque);

  if (use_surface_layer_)
    ActivateSurfaceLayerForVideo(video_transform);

  SetReadyState(WebMediaPlayer::kReadyStateHaveMetadata);
  SetReadyState(WebMediaPlayer::kReadyStateHaveEnoughData);
  TriggerResize();
  ResetCanvasCache();
  MaybeCreateWatchTimeReporter();

```

The most annoying code in the code is the function below called from the `WebMediaPlayerMS::SetReadyState` function, and the `ScheduleNamedEvent` function can be avoided by satisfying the `tracks_are_ready` condition in the function below.

```
void HTMLMediaElement::SetReadyState(ReadyState state) {
  '''
  bool was_potentially_playing = PotentiallyPlaying();

  ReadyState old_state = ready_state_;
  ReadyState new_state = state;

  bool tracks_are_ready = TextTracksAreReady();

  '''
  if (ready_state_ == kHaveEnoughData && old_state < kHaveEnoughData &&
      tracks_are_ready) {
    if (old_state <= kHaveCurrentData) {
      ScheduleNamedEvent(event_type_names::kCanplay);
      if (is_potentially_playing)
        ScheduleNotifyPlaying();
    }

    if (autoplay_policy_->RequestAutoplayByAttribute()) {
      paused_ = false;
      SetShowPosterFlag(false);
      GetCueTimeline().InvokeTimeMarchesOn();
      ScheduleNamedEvent(event_type_names::kPlay);
      ScheduleNotifyPlaying();
      can_autoplay_ = false;
    }

    ScheduleNamedEvent(event_type_names::kCanplaythrough);
  }

  UpdatePlayState();
}

```

The exact location of the function that calls the GarbageCollector can be found through the `AudioComponents` or `VideoComponents` function call in the `WebMediaPlayerMS::GetMediaStreamType` function called by `WebMediaPlayerMS::MaybeCreateWatchTimeReporter`.

```
WebMediaPlayerMS::GetMediaStreamType() {
  if (web_stream_.IsNull())
    return std::nullopt;

  // If either the first video or audio source is remote, the media stream is
  // of remote source.
  MediaStreamDescriptor& descriptor = *web_stream_;
  MediaStreamSource* media_source = nullptr;
  if (HasVideo()) {
    auto video_components = descriptor.VideoComponents();
    DCHECK_GT(video_components.size(), 0U);
    media_source = video_components[0]->Source();
  } else if (HasAudio()) {
    auto audio_components = descriptor.AudioComponents();
    DCHECK_GT(audio_components.size(), 0U);
    media_source = audio_components[0]->Source();
  }

```

If the trigger doesn't proceed smoothly, try using native Chromium instead of ASAN Chromium. Depending on your computer's specifications, there may still be areas where the task order and GC condition processing probability are low. We will improve this in the future and re-upload the proof-of-concept (PoC).

The Chromium commit that triggered this vulnerability is `06773e4fd40f4b8ad8a3c94a86ff14613b626c8e`

# Summary

Use-After-Free in WebMediaPlayerMS::OnFirstFrameReceived

# Custom Questions

#### Type of crash:

Renderer

#### Crash state:

An action occurs that references a freed object member object.

#### Reporter credit:

sherkito

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 17.2 KB)
- [poc.html](attachments/poc.html) (text/html, 3.3 KB)
- [poc.html](attachments/poc.html) (text/html, 3.3 KB)

## Timeline

### aj...@google.com (2025-09-29)

I'm not yet able to reproduce a crash here - in your poc you include `http://localhost:8000/aaaaa` is it necessary to serve something from this endpoint for the poc to succeed?

### ss...@gmail.com (2025-09-29)

This part is the code to meet the tracks\_are\_ready condition, and it doesn't have to be a valid path. If possible, could you try reproducing this with a VM with 8GB of RAM and 4 CPU cores?

### pe...@google.com (2025-09-29)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2025-09-30)

-> mediastream folks to have a look - this seems pretty racy and I've not been able to reproduce the crash but it also seems feasible. Setting to sev=medium as a racy uaf in the renderer.

### ss...@gmail.com (2025-09-30)

It worked well on a 16GB 4-core VM. If it doesn't work on ASAN, please test it on the default Chromium.  

Also, when testing, add `chrome.exe --enable-blink-features=LongTaskFromLongAnimationFrame --js-flags="--stress-incremental-marking --expose-gc"` to the command line.  

`--enable-blink-features=LongTaskFromLongAnimationFrame` is to prevent it from interfering with normal GC call scenarios by interfering with tree function TASKs.

### ch...@google.com (2025-09-30)

Setting milestone because of s2 severity.

### ch...@google.com (2025-09-30)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ss...@gmail.com (2025-09-30)

I have re-attached the POC code that solved the issue, as it has been confirmed that the issue, which was thought to have been resolved, is reoccurring depending on the environment.

### li...@chromium.org (2025-09-30)

interesting, i'll take a look.

### ss...@gmail.com (2025-10-07)

I'm wondering if there are any updates regarding reproduce or other related issues.

### ch...@google.com (2025-10-15)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### li...@chromium.org (2025-10-15)

oh chome-security-blintz-daily-runner!

but anyway => p2 because this is really hard to trigger without poking the gc manually. fixing it requires some ugliness that i'm working through now.

### aj...@google.com (2025-10-15)

thanks for looking into this - if triggering this requires racy manipulation of state we could lower its severity?

### ss...@gmail.com (2025-10-15)

Playback still doesn't reproduce with the code I reuploaded above? :(

Increasing the `audio_tracks` variable size (e.g., 0xe000~) and refreshing (F5) prevents the trigger from working. Therefore, you need to close the tab and recreate it, creating a new process.

### li...@chromium.org (2025-10-15)

@ajgo: sure, => S3. i admit that i'm not really sure what Pn vs Sn means; my monorail-powered brain just sees a total ordering + an extra number.

@ssherkito: the crash requires not just any GC, but a conservative GC caused when there's significant memory pressure and it's basically panicking. further, it has to trigger on the one(-ish) oilpan object access in the player along that path, and then gc must choose to collect the media element specifically (which is, admittedly, an obvious target). if oilpan gets to a steady state and can trigger a precise gc instead => nothing bad happens.

### ss...@gmail.com (2025-10-15)

deleted

### ss...@gmail.com (2025-10-16)

A similar issue (which seems more difficult to trigger) was `https://issues.chromium.org/issues/41487330`, which had a severity setting of 1.  

Do you see any differences from the current bug?

### li...@chromium.org (2025-10-16)

looks like a similar cause, with a similar solution. i suspect that 'severity' has quite a bit of noise; i've not run into many folks who can give me a clear explanation of what it means.

this:

```
auto* client_on_stack = client_.Get();

```

will prevent gc of `client` but only if we make some assumptions about the emitted code. i considered this as a potential solution, but it's not technically guaranteed to put anything on the stack or in registers that are spilled to the stack. for oilpan-friendly code, i believe this is enforced by compiler magic. i don't know if we can guarantee it more generally in code that is not managed. we might not turn off all the necessary optimizations.

i think a less magic solution is an RAII object that forces `HTMLMediaElement::HasPendingActivity()` to return true.

a more magic solution is to placement-new the client inside the element. then none of this is needed and GC is averted without the client doing anything special. but no, i'm not serious. (and yeah, if one is being precise, the same optimization concerns for the `auto*` approach would apply here.)

### dx...@google.com (2025-10-27)

Project: chromium/src  

Branch:  main  

Author:  Frank Liberato [liberato@chromium.org](mailto:liberato@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7000843>

Prevent media element GC in callbacks in WebMediaPlayerMS

---


Expand for full commit details
```
     
    Callbacks into WebMediaPlayerMS can happen, in general, when 
    the element is eligible for GC.  This CL adds a stack reference 
    to the client (element) to prevent conservative GC from 
    reclaiming the element during the callback. 
     
    Bug: 448046109 
    Change-Id: I67e37bbc2b25ccd54d0d94e1857f07dd3e673418 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7000843 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Frank Liberato <liberato@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1536174}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`

---

Hash: [9696b698f7dc30fbef6a93790aafbd289538a803](https://chromiumdash.appspot.com/commit/9696b698f7dc30fbef6a93790aafbd289538a803)  

Date: Mon Oct 27 19:49:33 2025


---

### li...@google.com (2025-10-27)

turns out that there's a helper `base::debug::Alias()` that forces, from a certain point of view, the compiler to store a local variable in memory rather than elide it / keep it in a register. hopefully, this memory is on the stack -- though i suppose that's not guaranteed. anyway, @reporter please see if that fixes it for you.

### ch...@google.com (2025-10-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ss...@gmail.com (2025-10-30)

Although I can't verify it by running the code due to an issue with the Chromium build, the patch itself looks correct based on a review of the code.

### ss...@gmail.com (2025-11-12)

Is there any update about CVE or reward?

### aj...@google.com (2025-11-17)

RE comment 24 - this is in the queue for the panel but we cannot make any promises on timelines for assessment.

### sp...@google.com (2025-12-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Moderately mitigated RCE with a bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/448046109)*
