# Redirect circumvents same-origin restrictions for AudioWorklet

| Field | Value |
|-------|-------|
| **Issue ID** | [40090937](https://issues.chromium.org/issues/40090937) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SameOriginPolicy, Blink>WebAudio |
| **Reporter** | s....@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2018-03-27 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://vuln.shhnjk.com/oudi-work.html
2. Play audio

What is the expected behavior?
MediaElementAudioSource outputs zeroes due to CORS access restrictions.

What went wrong?
Spec (https://webaudio.github.io/web-audio-api/#MediaElementAudioSourceOptions-security) says:
To prevent this, a MediaElementAudioSourceNode MUST output silence instead of the normal output of the HTMLMediaElement if it has been created using an HTMLMediaElement for which the execution of the fetch algorithm labeled the resource as CORS-cross-origin.

If you play around with 2 buttons, whenever audio is set directly to "https://www.w3schools.com/tags/horse.mp3", output is zeroed correctly. But when you set audio through redirect, it'll happily output real audio.

Per spec, Web Audio allows inspection of the content of the resource. So this bug should leak cross-origin audio, but I haven't figured out how yet :(

Did this work before? N/A 

Chrome version: 67.0.3377.1  Channel: dev
OS Version: Windows 10
Flash Version:

## Timeline

### el...@chromium.org (2018-03-28)

Nice find, thanks!

[Monorail components: Blink>SecurityFeature>SameOriginPolicy Blink>WebAudio]

### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-03-28)

It seems like ScriptProcessorNode has the same issue.

PoC
https://vuln.shhnjk.com/uudi-work.html

Play audio in above page and check the devtools console. You will see non-0 outputs logged by AudioWorkletProcessor as well as ScriptProcessor. Those might have different root cause because captureStream doesn't work on that audio (which suggests that audio is tainted at least for Media Capture APIs).
But ScriptProcessor is already released so above PoC works with Chrome 65.

PS
I'm stuck on converting Typed array data to audio data :(  What a shame...


### sh...@chromium.org (2018-03-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-29)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-03-30)

This is very likely not a security regression since it also appears in ScriptProcessorNode. This has probably existed since CORS support was added to MediaElementAudioSourceNode several years ago. It only showed up now because someone was testing it with the newly released AudioWorklet.

### s....@gmail.com (2018-03-30)

Just FYI, I would like to publish this bug on November if fixed. It’d be great if this bug could be fixed before that. Thanks!

### s....@gmail.com (2018-04-04)

Here is a proper PoC of stealing cross-origin audio.
https://vuln.shhnjk.com/eudi-work.html

### sh...@chromium.org (2018-04-14)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-04-25)

M67 Stable promotion is coming soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. Thank you.



### sh...@chromium.org (2018-04-29)

rtoy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-05-09)

Somewhat related issue:  619114

### es...@chromium.org (2018-05-18)

rtoy, can you please give an update on this bug? Thanks!

### rt...@chromium.org (2018-05-21)

Still in progress.

### bu...@chromium.org (2018-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/761c75d2d607638ff53c764b4925bcca9be601d8

commit 761c75d2d607638ff53c764b4925bcca9be601d8
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Jun 05 00:28:50 2018

Redirect should not circumvent same-origin restrictions

Check whether we have access to the audio data when the format is set.
At this point we have enough information to determine this. The old approach
based on when the src was changed was incorrect because at the point, we
only know the new src; none of the response headers have been read yet.

This new approach also removes the incorrect message reported in 619114.

Bug: 826552, 619114
Change-Id: I95119b3a1e399c05d0fbd2da71f87967978efff6
Reviewed-on: https://chromium-review.googlesource.com/1069540
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#564313}
[add] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/WebKit/LayoutTests/http/tests/security/media-element-audio-source-node-redirect-expected.txt
[add] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/WebKit/LayoutTests/http/tests/security/media-element-audio-source-node-redirect.html
[modify] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/WebKit/LayoutTests/http/tests/security/resources/webaudio/media-element-audio-source-node-test.js
[modify] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/blink/renderer/modules/webaudio/base_audio_context.h
[modify] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc
[modify] https://crrev.com/761c75d2d607638ff53c764b4925bcca9be601d8/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.h


### rt...@chromium.org (2018-06-05)

Probably too late for M67, but this might be good to have for M68.

Therefore requesting merge to 68.

### sh...@chromium.org (2018-06-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-06)

Your change meets the bar and is auto-approved for M68. Please go ahead and merge the CL to branch 3440 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559

commit 93d25b7e2449ca6fd7b1c3dc003f5bfce1495559
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Jun 06 15:48:11 2018

Redirect should not circumvent same-origin restrictions

Check whether we have access to the audio data when the format is set.
At this point we have enough information to determine this. The old approach
based on when the src was changed was incorrect because at the point, we
only know the new src; none of the response headers have been read yet.

This new approach also removes the incorrect message reported in 619114.

Bug: 826552, 619114
Change-Id: I95119b3a1e399c05d0fbd2da71f87967978efff6
Reviewed-on: https://chromium-review.googlesource.com/1069540
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#564313}(cherry picked from commit 761c75d2d607638ff53c764b4925bcca9be601d8)
Reviewed-on: https://chromium-review.googlesource.com/1089070
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#210}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[add] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/WebKit/LayoutTests/http/tests/security/media-element-audio-source-node-redirect-expected.txt
[add] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/WebKit/LayoutTests/http/tests/security/media-element-audio-source-node-redirect.html
[modify] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/WebKit/LayoutTests/http/tests/security/resources/webaudio/media-element-audio-source-node-test.js
[modify] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/blink/renderer/modules/webaudio/base_audio_context.h
[modify] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc
[modify] https://crrev.com/93d25b7e2449ca6fd7b1c3dc003f5bfce1495559/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.h


### s....@gmail.com (2018-06-06)

Just FYI, it's also possible to steal audio data of cross-origin video.

PoC: https://vuln.shhnjk.com/webvideo.html

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

Nice one s.h.h.n.j.k@, $1,000 for this report!

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/826552?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>SameOriginPolicy, Blink>WebAudio]
[Monorail mergedwith: crbug.com/chromium/839983]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090937)*
