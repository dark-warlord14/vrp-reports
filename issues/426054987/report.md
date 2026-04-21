# use-after-poison in blink::MediaStreamAudioTrack::StopAndNotify(class base::OnceCallback<(void)>)

| Field | Value |
|-------|-------|
| **Issue ID** | [426054987](https://issues.chromium.org/issues/426054987) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ev...@google.com |
| **Created** | 2025-06-19 |
| **Bounty** | $8,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
AddressSanitizer: use-after-poison in blink::MediaStreamAudioTrack::StopAndNotify(class base::OnceCallback<(void)>)

## VERSION

`asan-win32-release_x64-1476007`

## Reproduction Steps

- python -m http.server 8000
- Run: `chrome --autoplay-policy=no-user-gesture-required --js-flags="-expose-gc" --no-sandbox --user-data-dir=test --enable-logging=stderr poc.html`

## Type of crash

Tab

## Root Cause Analysis (RCA)

Coming soon.

## Attachments

- asan.txt (text/plain, 21.9 KB)
- poc.html (text/html, 1.7 KB)

## Timeline

### am...@chromium.org (2025-06-21)

Thanks for the report. Apologies for the delay here. I am having difficulty reproducing this. It looks like it should be straight forward, but I've attempted to reproduce nearly 10 times. The core difference is that I'm relegated to a linux asan build, but I'm unsure as to why it would matter in the case of this issue.

I'm going to go ahead and send this forward based on the stack trace. 
Tentatively setting as S1 / high severity based on the potential for UAF in the renderer / renderer process memory corruption. 
Since I am unable to reproduce, setting the found-in to 136 (current extended stable), completely speculative based on looking simply looking at the involved code.

### ch...@google.com (2025-06-21)

Setting milestone because of s0/s1 severity.

### m....@gmail.com (2025-06-24)

This issue was discovered this time due to `https://chromium-review.googlesource.com/c/chromium/src/+/6422562`. However, changing `var v1404 = new SpeechRecognition();` to `var v1404 = new window.webkitSpeechRecognition();` can trigger it in earlier versions, so the root cause still needs to be identified.

### m....@gmail.com (2025-06-26)

Bisect:`https://chromium-review.googlesource.com/c/chromium/src/+/5906320`

This issue has existed for a long time, but before this CL, the crash occurred at a different point.

### m....@gmail.com (2025-06-26)

`SpeechRecognitionMediaStreamAudioSink` is an on-heap object.  

`MediaStreamAudioTrack` uses a `Vector<WebMediaStreamAudioSink*>` to directly store on-heap objects,  

causing a use-after-free (UAF) issue when `SpeechRecognitionMediaStreamAudioSink` is garbage-collected and subsequently accessed by `MediaStreamAudioTrack::StopAndNotify`.

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/speech/speech_recognition.cc;drc=a533a36dfe878045cd210166b8c3f1678fc987e7;l=508
void SpeechRecognition::StartInternal() {
  final_results_.clear();

  auto task_runner =
      GetExecutionContext()->GetTaskRunner(TaskType::kMiscPlatformAPI);
  if (RuntimeEnabledFeatures::MediaStreamTrackWebSpeechEnabled() &&
      stream_track_) {
    SpeechRecognitionMediaStreamAudioSink* sink =
        MakeGarbageCollected<SpeechRecognitionMediaStreamAudioSink>(
            GetExecutionContext(),
            WTF::BindOnce(&SpeechRecognition::StartController,
                          WrapPersistent(this),
                          session_.BindNewPipeAndPassReceiver(task_runner)));
    WebMediaStreamAudioSink::AddToAudioTrack(
        sink, WebMediaStreamTrack(stream_track_->Component()));
    stream_track_->RegisterSink(sink);
  } else {
    StartController(session_.BindNewPipeAndPassReceiver(task_runner));
  }

  started_ = true;
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/mediastream/media_stream_audio_track.cc;drc=13075886efc851f658b6b14500272e62e5521614;l=144
void MediaStreamAudioTrack::StopAndNotify(base::OnceClosure callback) {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  WebRtcLog(kTag, this, "%s()", __func__);

  if (!stop_callback_.is_null())
    std::move(stop_callback_).Run();

  Vector<WebMediaStreamAudioSink*> sinks_to_end;
  deliverer_.GetConsumerList(&sinks_to_end);
  for (WebMediaStreamAudioSink* sink : sinks_to_end) {
    deliverer_.RemoveConsumer(sink);
    sink->OnReadyStateChanged(WebMediaStreamSource::kReadyStateEnded);
  }

}

```

### da...@chromium.org (2025-06-30)

=>evliu since it's speech recognition related.

### m....@gmail.com (2025-07-07)

ping@

### dx...@google.com (2025-07-14)

Project: chromium/src  

Branch:  main  

Author:  Evan Liu [evliu@google.com](mailto:evliu@google.com)  

Link:    <https://chromium-review.googlesource.com/6712212>

Fix potential UAF in MediaStreamTrackImpl

---


Expand for full commit details
```
     
    This CL fixes a potential UAF vulnerability in MediaStreamTrackImpl 
    where pointers to the SpeechRecognitionMediaStreamAudioSinks that are 
    owned by the MediaStreamTrackImpl could potentially be accessed after 
    the sinks are destroyed. 
     
    Fixed: 426054987 
    Change-Id: I453160a8eed7926e2cc3500260de04d2722c98e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6712212 
    Commit-Queue: Evan Liu <evliu@google.com> 
    Reviewed-by: Mark Foltz <mfoltz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1486476}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`

---

Hash: [90d99dcd83af2f13e0f917b5a9dc59eeee0204d0](http://crrev.com/90d99dcd83af2f13e0f917b5a9dc59eeee0204d0)  

Date: Mon Jul 14 19:21:45 2025


---

### ch...@google.com (2025-07-15)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ev...@google.com (2025-07-15)

Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/6712212

Has this fix been verified on Canary to not pose any stability regressions?
No.

Does this fix pose any potential non-verifiable stability risks?
No.

Does this fix pose any known compatibility risks?
No.

Does it require manual verification by the test team? If so, please describe required testing.
No.

### am...@chromium.org (2025-07-17)

no issues related to this fix on canary nor looking at this change, merges approved for <https://crrev.com/c/6712212>; please merge this fix to M139 Beta / branch 7258 and M138 Stable / branch 7204 by EOD tomorrow / Friday so this fix can be included in Tuesday's update of M138 Stable and the Stable RC cut for M139

### ch...@google.com (2025-07-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@chromium.org (2025-07-21)

I am getting merge conflicts when i tried to CP, can you please help with the merge to 138 ( asap) and 139 ( due EOD today) 

### dx...@google.com (2025-07-21)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Evan Liu [evliu@google.com](mailto:evliu@google.com)  

Link:    <https://chromium-review.googlesource.com/6775582>

[Cherry-pick] Fix potential UAF in MediaStreamTrackImpl

---


Expand for full commit details
```
     
    This CL fixes a potential UAF vulnerability in MediaStreamTrackImpl 
    where pointers to the SpeechRecognitionMediaStreamAudioSinks that are 
    owned by the MediaStreamTrackImpl could potentially be accessed after 
    the sinks are destroyed. 
     
    (cherry picked from commit 90d99dcd83af2f13e0f917b5a9dc59eeee0204d0) 
     
    Fixed: 426054987 
    Change-Id: I453160a8eed7926e2cc3500260de04d2722c98e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6712212 
    Commit-Queue: Evan Liu <evliu@google.com> 
    Reviewed-by: Mark Foltz <mfoltz@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1486476} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6775582 
    Auto-Submit: Evan Liu <evliu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7258@{#1725} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`

---

Hash: [5af814cec4fee13dc8b00ea1e1456cd84a1f4dc6](http://crrev.com/5af814cec4fee13dc8b00ea1e1456cd84a1f4dc6)  

Date: Mon Jul 21 21:04:45 2025


---

### pe...@google.com (2025-07-21)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-07-21)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Evan Liu [evliu@google.com](mailto:evliu@google.com)  

Link:    <https://chromium-review.googlesource.com/6775561>

[Cherry-pick] Fix potential UAF in MediaStreamTrackImpl

---


Expand for full commit details
```
     
    This CL fixes a potential UAF vulnerability in MediaStreamTrackImpl 
    where pointers to the SpeechRecognitionMediaStreamAudioSinks that are 
    owned by the MediaStreamTrackImpl could potentially be accessed after 
    the sinks are destroyed. 
     
    (cherry picked from commit 90d99dcd83af2f13e0f917b5a9dc59eeee0204d0) 
     
    Validate-Test-Flakiness: skip 
    Fixed: 426054987 
    Change-Id: I453160a8eed7926e2cc3500260de04d2722c98e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6712212 
    Commit-Queue: Evan Liu <evliu@google.com> 
    Reviewed-by: Mark Foltz <mfoltz@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1486476} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6775561 
    Auto-Submit: Evan Liu <evliu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#2086} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`

---

Hash: [35265300b717b63de5513a80160305cc072a3298](http://crrev.com/35265300b717b63de5513a80160305cc072a3298)  

Date: Mon Jul 21 22:45:55 2025


---

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### m....@gmail.com (2025-07-30)

Please credit to `dnpushme & Zhiniang Peng with HUST`

I made changes at `bughunters.google.com/profile`, but they don't seem to have synced here.

### am...@chromium.org (2025-07-30)

Our integration with the bughunters portal simply forwards reports submitted here here, allows the bughunters site to pull metadata -- such as email address, report status, and reward into into it for payments processing and the leaderboard. We do not use any features or profile data in the Chromium tracker in any way.

Would you like all future credit related to this email address to reflect the data in c#20? If yes, we have a system on our side we have to update to ensure that future security advisories reflect the correct data.

### m....@gmail.com (2025-07-31)

Yes, please update your system to ensure that all future credit related to this email address reflects the data in c#20 for security advisories.

### qk...@google.com (2025-08-04)

Labelling as not applicable for LTS 132 because the Web Speech API doesn't support MediaStreamTrack in M132.

### ch...@google.com (2025-10-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/426054987)*
