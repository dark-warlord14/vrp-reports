# Security: Use After Free in UserMediaRequest::OnMediaStreamInitialized

| Field | Value |
|-------|-------|
| **Issue ID** | [40054110](https://issues.chromium.org/issues/40054110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2020-6422, CVE-2020-6550 |
| **Reporter** | et...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2020-12-08 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36

Steps to reproduce the problem:
Include the attached files media-1.html, media-2.html in the same folder and serve it on local host. open media-1.html in the chromium, and click the button in the page

What is the expected behavior?

What went wrong?
Similar to CVE-2020-6550 (https://bugs.chromium.org/p/chromium/issues/detail?id=1116706) and CVE-2020-6422(https://bugs.chromium.org/p/chromium/issues/detail?id=1051748).

In function UserMediaRequest::OnMediaStreamInitialized, Invoking Promise.resolve may trigger user callback. 

The execution context is destroyed in the callback, then "RecordIdentifiabilityMetric" use it.

```c++
void UserMediaRequest::OnMediaStreamInitialized(MediaStream* stream) {
  DCHECK(!is_resolved_);

  MediaStreamTrackVector audio_tracks = stream->getAudioTracks();
  for (const auto& audio_track : audio_tracks)
    audio_track->SetConstraints(audio_);

  MediaStreamTrackVector video_tracks = stream->getVideoTracks();
  for (const auto& video_track : video_tracks)
    video_track->SetConstraints(video_);

  callbacks_->OnSuccess(nullptr, stream); // [0] Invoking Promise.resolve thenable, and callback to iframe detach
  RecordIdentifiabilityMetric(surface_, GetExecutionContext(), // [1] use execution context destroyed
                              IdentifiabilityBenignStringToken(g_empty_string));
  is_resolved_ = true;
}
```

```c++
//third_party/blink/renderer/modules/mediastream/media_devices.cc
void OnSuccess(ScriptWrappable* callback_this_value,
                MediaStream* stream) override {
    resolver_->Resolve(stream);
}
```

Did this work before? N/A 

Chrome version: 87.0.4280.67  Channel: stable
OS Version: OS X 10.15.7
Flash Version: 

This poc cannot directly cause a crash, but by Debug, you can see that it is reentered to js, and the Execution Context is destroyed.

And its vulnerability pattern is similar to the previous two vulnerabilities, so I will report this issue to you.

## Attachments

- [media1.html](attachments/media1.html) (text/plain, 535 B)
- [media2.html](attachments/media2.html) (text/plain, 1.1 KB)
- [BED5219FA8905053665B3F4B6B0D80BD.png](attachments/BED5219FA8905053665B3F4B6B0D80BD.png) (image/png, 136.5 KB)
- [D4BF4EA3BAED4994E3C5CEC6193CA5AB.png](attachments/D4BF4EA3BAED4994E3C5CEC6193CA5AB.png) (image/png, 150.0 KB)
- [patch_log.png](attachments/patch_log.png) (image/png, 140.1 KB)

## Timeline

### et...@gmail.com (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### et...@gmail.com (2020-12-08)

I'm not sure if this is a real security issue, but I discovered it when I audited the code, and the vulnerability pattern is very similar to CVE-2020-6550 (https://bugs.chromium.org/p/chromium/issues/detail?id=1116706) .
If I understand it wrong, please let me know.

### wf...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-08)

Hi, thanks for your report. Does this need a real camera attached to the test machine and for the user to accept the camera permission?

### wf...@chromium.org (2020-12-08)

I couldn't reproduce this... I had to remove the constraints to get the video capture to start, but even then, I hit the console.log("then"); and get console output, but no UAF. I am running asan-win32-release_x64-834098. I wonder if this is being correctly handled by oilpan tracked callbacks_ member? guidou-> could you take a look here?

### wf...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>MediaStream]

### gu...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-12-08)

I'll take a look.

### gu...@chromium.org (2020-12-08)

The issue is present since M88.

### wf...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f05627a89b39301d18458849152a1d42288bcdc

commit 2f05627a89b39301d18458849152a1d42288bcdc
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Dec 09 14:44:18 2020

Record identifiability metrics before getUserMedia() settles

When the promise of a getUserMedia() call is settled, it can result
in the detachment of the execution context.
The idenfiability metrics for getUserMedia() require a valid
execution context and therefore should run before the getUserMedia()
call ends.

Bug: 1156510
Change-Id: I29975c9d779858b1574506f5d60ecfe4ae6a1690
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2580070
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Chris Fredrickson <cfredric@chromium.org>
Reviewed-by: Chris Fredrickson <cfredric@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835178}

[modify] https://crrev.com/2f05627a89b39301d18458849152a1d42288bcdc/third_party/blink/renderer/modules/mediastream/user_media_request.cc


### gu...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### gu...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-09)

The older reward-topanel https://crbug.com/chromium/1156509 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ad...@google.com (2020-12-09)

Approving merge to M88, branch 4324.

Assuming severity high due to renderer UaF.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/439152a0437971afacf74ae4c9b31062debae094

commit 439152a0437971afacf74ae4c9b31062debae094
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Dec 10 10:21:11 2020

Record identifiability metrics before getUserMedia() settles

When the promise of a getUserMedia() call is settled, it can result
in the detachment of the execution context.
The idenfiability metrics for getUserMedia() require a valid
execution context and therefore should run before the getUserMedia()
call ends.

(cherry picked from commit 2f05627a89b39301d18458849152a1d42288bcdc)

Bug: 1156510
Change-Id: I29975c9d779858b1574506f5d60ecfe4ae6a1690
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2580070
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Chris Fredrickson <cfredric@chromium.org>
Reviewed-by: Chris Fredrickson <cfredric@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#835178}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2582042
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#777}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/439152a0437971afacf74ae4c9b31062debae094/third_party/blink/renderer/modules/mediastream/user_media_request.cc


### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $5000 for this bug.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

@eternalsakuraalpha - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### et...@gmail.com (2021-03-30)

@aamyressler
Hello, I reviewed some previous issues and saw that some attachments with bounty issues have been deleted. Can you recover them? Thanks!


### am...@chromium.org (2021-03-30)

Hi, eternalsakuraalpha. I undeleted a lot of previously deleted attachments from other reports from a query I ran yesterday. It is quite likely that I may have missed some, however. Are there specific issues in mind to which you are referring? Please feel free to send me an email with specific bug ID numbers and I would be happy to look into it. 

### is...@google.com (2021-03-30)

This issue was migrated from crbug.com/chromium/1156510?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1156509]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-27)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054110)*
