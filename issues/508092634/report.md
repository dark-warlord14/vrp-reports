# Forged audio_forwarder in SpeechRecognition IPC bypasses per-origin microphone permission on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [508092634](https://issues.chromium.org/issues/508092634) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Speech |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ev...@google.com |
| **Created** | 2026-04-30 |
| **Bounty** | $8,000.00 |

## Description

# Forged audio\_forwarder in SpeechRecognition IPC bypasses per-origin microphone permission on Android

## Summary

On Android, a compromised renderer can bypass the browser-enforced per-origin microphone permission check for the Web Speech API by injecting a forged `audio_forwarder` into the `StartSpeechRecognitionRequestParams` Mojo message. The browser process uses the presence of this field as a trusted signal that audio will be forwarded from the renderer rather than captured from the device microphone, and accordingly skips the `CheckRecognitionIsAllowed` permission gate. However, on Android the speech recognition backend (`SpeechRecognizerImplAndroid`) unconditionally opens the real device microphone via the Android `SpeechRecognizer` API regardless of whether an `audio_forwarder` was provided; it simply ignores the field. The result is that any origin with a compromised renderer can silently activate the microphone and receive speech transcription results without the user ever seeing a permission prompt, provided the Chrome app already holds the Android-level `RECORD_AUDIO` permission. Platform: Android only.

## Bisect

Introducing Commit: `881ab7a9d5955a4f57c19c11a49703b468984fa6`

- Date: 2024-08-01
- Author: Evan Liu
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5631655>

## Root Cause

When the "Add MediaStreamTrack support to the Web Speech API" feature was introduced, a new `audio_forwarder` field was added to `StartSpeechRecognitionRequestParams` in the Mojo interface. This field allows the renderer to supply its own audio stream to the speech recognition engine instead of having the browser capture from the microphone. The permission model was updated to treat the presence of this field as meaning "the renderer is providing audio, so no microphone access is needed":

```
// content/browser/speech/speech_recognition_manager_impl.cc:620-625
auto session = std::make_unique<Session>();
session->id = session_id;
session->config = config;
session->context = config.initial_context;
session->use_microphone = !audio_forwarder_config.has_value();

```

The `use_microphone` flag is the sole gate controlling whether the browser performs permission checks. In `StartSession`, when `use_microphone` is false, the entire permission path is skipped and recognition begins immediately:

```
// content/browser/speech/speech_recognition_manager_impl.cc:249-277
void SpeechRecognitionManagerImpl::StartSession(int session_id) {
  if (sessions_[session_id]->use_microphone) {
    microphone_session_id_ = session_id;
    if (delegate_) {
      delegate_->CheckRecognitionIsAllowed(
          session_id,
          base::BindOnce(
              &SpeechRecognitionManagerImpl::RecognitionAllowedCallback,
              weak_factory_.GetWeakPtr(), session_id));
    }
    return;
  }
  // Permission check skipped entirely.
  base::SingleThreadTaskRunner::GetCurrentDefault()->PostTask(
      FROM_HERE,
      base::BindOnce(&SpeechRecognitionManagerImpl::DispatchEvent,
                     weak_factory_.GetWeakPtr(), session_id, EVENT_START));
}

```

On desktop platforms, this logic is sound because the `SpeechRecognizerImpl` class actually consumes the forwarded audio from the renderer and never opens the microphone. On Android, however, the code takes an entirely different branch. The `CreateSession` method is guarded by `#if !BUILDFLAG(IS_ANDROID)` for the desktop recognizer, and the `#else` branch unconditionally creates a `SpeechRecognizerImplAndroid` that has no knowledge of `audio_forwarder` at all:

```
// content/browser/speech/speech_recognition_manager_impl.cc:741-743
#else
  session->recognizer = new SpeechRecognizerImplAndroid(this, session_id);
#endif

```

`SpeechRecognizerImplAndroid::StartRecognition` delegates directly to the Java `SpeechRecognitionImpl` class via JNI, which calls `android.speech.SpeechRecognizer.startListening()` to capture audio from the real device microphone:

```
// SpeechRecognitionImpl.java:298-312
private void startRecognition(String language, boolean continuous, boolean interimResults) {
    mRecognizer.startListening(mIntent);
}

```

This creates a semantic contradiction: the browser decided to skip the permission check because it believes the renderer is providing its own audio, but the Android backend opens the actual microphone anyway.

The `SpeechRecognitionDispatcherHost::Start` method does validate that `channel_count` and `sample_rate` are positive when `audio_forwarder` is present, but this is trivially satisfied by the attacker. There is no validation rejecting the `audio_forwarder` field on Android where it has no effect, and there is no re-verification at the point where the recognizer actually begins capturing audio.

The Android `SpeechRecognizer` API used here is the in-process variant (`SpeechRecognizer.createSpeechRecognizer` with a `RecognitionListener`), which operates silently with no system UI. On Android 12 and later the OS displays a small green privacy indicator dot in the status bar, but earlier versions provide no indication at all.

The attack requires a compromised renderer. An attacker sends a `StartSpeechRecognitionRequestParams` message with a valid `audio_forwarder` `PendingReceiver` (the receiver need not be bound to anything functional), `channel_count` set to 1, and `sample_rate` set to 16000. The browser process accepts these parameters, sets `use_microphone` to false, and starts recognition without any permission check. On a device with Google Mobile Services installed, the Android `SpeechRecognizer` will successfully capture microphone audio and deliver speech transcription results back through the `SpeechRecognitionSessionClient` Mojo interface to the compromised renderer.

## Reproduce

Tested at commit `18ff6ec31153904f6f7613dcc6cc79c09dbc7042` on a Pixel 7 Pro running AOSP Android 15 (SDK 35). The Chrome app must already hold the Android `RECORD_AUDIO` permission (as it would after any prior legitimate microphone grant to any origin).

Apply the renderer and browser instrumentation patch:

```
cd ~/chromium/src
git apply issue_ipc006/patch.diff

```

Build and install:

```
autoninja -C out/android chrome_public_apk
out/android/bin/chrome_public_apk install

```

Serve the PoC and set up port forwarding:

```
python3 -m http.server 8888 --directory issue_ipc006 &
adb reverse tcp:8888 tcp:8888

```

Launch Chrome:

```
adb logcat -c
out/android/bin/chrome_public_apk launch \
  --args='--enable-logging=stderr' \
  http://localhost:8888/poc.html

```

The page auto-starts speech recognition after two seconds. No permission dialog appears. Within a few seconds, the following appears in `adb logcat`:

```
04-30 20:49:38.955  8255  8267 E chromium: [ERROR:third_party/blink/renderer/modules/speech/speech_recognition_controller.cc:124] POC: Forged audio_forwarder injected by compromised renderer
04-30 20:49:38.959  8208  8271 E chromium: [ERROR:content/browser/speech/speech_recognition_manager_impl.cc:628] POC: CreateSession use_microphone=0 audio_forwarder_config=1
04-30 20:49:38.960  8208  8271 E chromium: [ERROR:content/browser/speech/speech_recognition_manager_impl.cc:254] POC: StartSession use_microphone=0
04-30 20:49:38.960  8208  8271 E chromium: [ERROR:content/browser/speech/speech_recognizer_impl_android.cc:46] POC: SpeechRecognizerImplAndroid::StartRecognition called - will open REAL microphone via Android SpeechRecognizer API
04-30 20:49:38.974  8208  8208 E SpeechRecognizer: no selected voice recognition service

```

The log confirms that the renderer (PID 8255) injected a forged `audio_forwarder`, the browser process (PID 8208) set `use_microphone=0` and skipped `CheckRecognitionIsAllowed`, and `SpeechRecognizerImplAndroid::StartRecognition` was called. The final error "no selected voice recognition service" is an artifact of the AOSP test device lacking Google Speech Services (AGSA/SSBG); on a production device with GMS, `startListening()` would succeed and deliver transcription results to the attacker.

This is a logic permission bypass, not a memory safety violation, so there is no ASAN or HWASAN report. Verification is through the logcat trace confirming that the permission check path was skipped while the real microphone backend was invoked.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 3.1 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.6 KB)
- [logcat.log](attachments/logcat.log) (text/plain, 832 B)

## Timeline

### je...@gmail.com (2026-04-30)

I am not entirely sure whether silently stealing microphone access from a compromised renderer, without the user ever seeing a permission prompt, crosses a security boundary you defend. If your team considers this out of scope, please let me know and I will shift my focus away from privacy-leakage class issues.

### ch...@google.com (2026-05-01)

Setting milestone because of s2 severity.

### ch...@google.com (2026-05-01)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  main  

Author:  Evan Liu [evliu@google.com](mailto:evliu@google.com)  

Link:    <https://chromium-review.googlesource.com/7809951>

Reject SpeechRecognition requests with audio forwarder on Android

---


Expand for full commit details
```
     
    A compromised renderer could bypass the per-origin microphone 
    permission check by supplying a forged `audio_forwarder` parameter in 
    the `StartSpeechRecognitionRequestParams` IPC message. The browser 
    process would see the forwarder and assume the renderer was providing 
    audio, skipping the permission prompt. However, the Android backend 
    ignores the forwarder and captures from the hardware microphone anyway. 
     
    Because Android's native `SpeechRecognizer` API does not support 
    consuming forwarded audio streams, this CL explicitly rejects any 
    speech recognition requests on Android that contain a valid 
    `audio_forwarder`. The request is aborted early with a `kNotAllowed` 
    error, preventing the hardware microphone from being activated. 
     
    Fixed: 508092634 
    Change-Id: Ia8406e37918c82ccb249e494270d1284801b896d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7809951 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Commit-Queue: Evan Liu <evliu@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1625917}

```

---

Files:

- M `content/browser/speech/speech_recognition_dispatcher_host.cc`

---

Hash: [a10d218219c11e19953692a8536c6bc10351436d](https://chromiumdash.appspot.com/commit/a10d218219c11e19953692a8536c6bc10351436d)  

Date: Wed May 6 01:57:48 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
High Quality. Web Platform Priviledge Escalation with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-14)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/508092634)*
