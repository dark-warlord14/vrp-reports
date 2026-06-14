# Security: UaF in MojoAudioDecoder (Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050145](https://issues.chromium.org/issues/40050145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Audio, Internals>Media>Encrypted |
| **Platforms** | Android |
| **Reporter** | mm...@semmle.com |
| **Assignee** | xh...@chromium.org |
| **Created** | 2019-09-17 |
| **Bounty** | $15,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Summary: On Android, a compromised renderer can cause a UaF in the gpu process, which is not an isolated process, this can lead to sandbox escape.

In MojoAudioDecoderService, a raw pointer to CdmContext is obtained from `mojo_cdm_service_context_->GetCdmContextRef(cdm_id)` [1]:

CdmContext\* cdm\_context = nullptr;  

if (config.is\_encrypted()) {  

cdm\_context\_ref\_ = mojo\_cdm\_service\_context\_->GetCdmContextRef(cdm\_id); //<-- a. Gets cdm\_context\_ref\_ from mojo\_cdm\_service\_context\_  

if (!cdm\_context\_ref\_) {  

DVLOG(1) << "CdmContextRef not found for CDM id: " << cdm\_id;  

std::move(callback).Run(false, false);  

return;  

}

```
cdm_context = cdm_context_ref_->GetCdmContext(); //<-- obtain the cdm_context  

```

}

decoder\_->Initialize(  

config, cdm\_context, //<-- raw cdm\_context used to initialize decoder\_  

base::Bind(&MojoAudioDecoderService::OnInitialized, weak\_this\_,  

base::Passed(&callback)),  

base::Bind(&MojoAudioDecoderService::OnAudioBufferReady, weak\_this\_),  

base::Bind(&MojoAudioDecoderService::OnWaiting, weak\_this\_));

This raw pointer is then used to initialize |decoder\_|. The lifetime of |cdm\_context| here is protected by |cdm\_context\_ref\_| and will be alive as long as |cdm\_context\_ref\_| is. Now |cdm\_context\_ref\_| comes from the |cdm\_services\_| map that in MojoCdmServiceContext[2]. A MojoCdmService is added to this map during the construction, when MojoCdmServiceContext::RegisterCdm is called [3], [4]. When a MojoCdmService is destroyed, it will remove itself from |cdm\_services\_|[5].

So by first create a MojoCdmService and then call MojoAudioDecoderService::Initialize with its cdm\_id, we can store a raw pointer |media\_crypto\_context\_| in a MediaCodecAudioDecoder that is owned by |cdm\_context|, which is owned by |cdm\_context\_ref\_|. If we then destroy the MojoCdmService with the corresponding cdm\_id, and call MojoAudioDecoderService::Initialize again with the same cdm\_id, then during the second initialization, because the MojoCdmService is destroyed and removed from the |cdm\_services\_| map, point a. in the above snippet will return nullptr, which frees |cdm\_context\_ref\_|, and at the same time, causes an early exit in the MojoAudioDecoderService::Initialize, which will not re-initialize |decoder\_|, leaving a free'd |media\_crypto\_context\_| behind. The use-after-free can then be triggered either by calling the SetCdm method, or by destroying |decoder\_| [7],[8].

This sequence of calls can be achieved from a compromised renderer (See reproduction case). As the MojoAudioDecoderService runs on the gpu process, which is a privileged process (not an isolated process) on Android, this leads to sandbox escape.

Thank you very much for your help and please let me know if there is anything I can help. Thanks.

1. <https://cs.chromium.org/chromium/src/media/mojo/services/mojo_audio_decoder_service.cc?gsn=GetSupportedCodecs&q=mojoaudiodecoderservice&g=0&l=43&rcl=a4468afb596d492089debe1676934676bb899ca0>
2. <https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service_context.cc?gsn=GetSupportedCodecs&g=0&rcl%3Da4468afb596d492089debe1676934676bb899ca0&l=108>
3. <https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service.cc?gsn=GetSupportedCodecs&rcl%3Da4468afb596d492089debe1676934676bb899ca0&g=0&l=163>
4. <https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service_context.cc?gsn=GetSupportedCodecs&rcl%3Da4468afb596d492089debe1676934676bb899ca0&g=0&l=75>
5. <https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service.cc?gsn=GetSupportedCodecs&rcl%3Da4468afb596d492089debe1676934676bb899ca0&g=0&l=50>
6. <https://cs.chromium.org/chromium/src/media/filters/android/media_codec_audio_decoder.cc?gsn=decoder_&g=0&l=115&rcl=a4468afb596d492089debe1676934676bb899ca0>
7. <https://cs.chromium.org/chromium/src/media/filters/android/media_codec_audio_decoder.cc?dr=C&targetos=android&g=0&rcl=a4468afb596d492089debe1676934676bb899ca0&l=247>
8. <https://cs.chromium.org/chromium/src/media/filters/android/media_codec_audio_decoder.cc?dr=C&targetos=android&g=0&rcl=a4468afb596d492089debe1676934676bb899ca0&l=50>

**VERSION**  

Chrome Version: master branch build b416cca, release build  

Operating System: Tested on an emulator with Pixel 2 API 28 2.

**REPRODUCTION CASE**  

Apply the patch audio\_decoder.patch to emulate a compromised renderer. (MojoCdm runs on renderer) Then serve audio\_decoder.html from an https server and open the page in an android device with the patched version of Chromium. This should result in a crash in the gpu process.

I have a crash log, but no symbol so probably not too helpful for debugging, but I've included in anyway.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Man Yue Mo of Semmle Security Research Team

## Attachments

- [audio_decoder.patch](attachments/audio_decoder.patch) (text/plain, 3.4 KB)
- deleted (application/octet-stream, 0 B)
- [audio_context_decoder_stack](attachments/audio_context_decoder_stack) (text/plain, 8.2 KB)
- [mojo_audio_decoder.html](attachments/mojo_audio_decoder.html) (text/plain, 622 B)

## Timeline

### dc...@chromium.org (2019-09-17)

This looks a lot like https://crbug.com/chromium/999311. Given this, I think we should strongly consider implementing the suggestion in https://bugs.chromium.org/p/chromium/issues/detail?id=999311#c8 ASAP.

### rs...@chromium.org (2019-09-17)

I was not able to repro this because the Mojo JS files in audio_decoder.html do not load for me:

mojo_bindings.js:1 Failed to load resource: the server responded with a status of 404 (File not found)
interface_factory.mojom.js:1 Failed to load resource: the server responded with a status of 404 (File not found)
bug-1004730.html:8 Uncaught ReferenceError: media is not defined
    at bug-1004730.html:8

But the explanation in the bug does make sense and it does seem like there is a real issue, so assigning.

[Monorail components: Internals>Media>Audio Internals>Media>Encrypted]

### mm...@semmle.com (2019-09-18)

Sorry about that, wrong file. Please find attached the correct file. Please let me know if there is other issue. Thanks.

### sh...@chromium.org (2019-09-18)

[Empty comment from Monorail migration]

### xh...@chromium.org (2019-09-18)

Re #1: Thanks for your suggestion. This case is actually a bit different. MojoAudioDecoderService::Initialize() is not a one-shot call and is supposed to be called multiple times during a media playback, e.g. to handle codec switch or config change. See [1] for more details.

The fundamental issue here after failing to get the cdm context, we reset |cdm_context_ref_| without cleaning the |decoder_|, which still holds a raw |cdm_context|, whose lifetime depends on |cdm_context_ref_|. We assumed that the client side won't call Decode() again, but since the renderer process is compromised it can do anything.

I'll work on a fix. At the same time, we probably should review all media/mojo code and keep in mind that the client can make any calls at any time.

[1] https://cs.chromium.org/chromium/src/media/base/video_decoder.h?q=VideoDecoder::Initia&sq=package:chromium&g=0&l=75

### xh...@chromium.org (2019-09-18)

Tentative fix is at: https://chromium-review.googlesource.com/c/chromium/src/+/1810846

I also have a unit test that can repro the reported crash. Let me know if I should include the test in the CL or submit it later. I pasted the test at http://go/paste/5138604441468928.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d496219fd9061eaba1be73be05f8fac1dda86a27

commit d496219fd9061eaba1be73be05f8fac1dda86a27
Author: Xiaohan Wang <xhwang@chromium.org>
Date: Thu Sep 19 05:29:04 2019

media: Keep |cdm_context_ref_| in mojo media services on failure

When unexpected failure happens, we expect the service to stay in a
valid state.

Bug: 1004730
Test: Manually tested
Change-Id: Ib35035705e4604b9aa8cf5212de07bc1069e73d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1810846
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Reviewed-by: John Rummell <jrummell@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#697907}

[modify] https://crrev.com/d496219fd9061eaba1be73be05f8fac1dda86a27/media/mojo/services/mojo_audio_decoder_service.cc
[modify] https://crrev.com/d496219fd9061eaba1be73be05f8fac1dda86a27/media/mojo/services/mojo_renderer_service.cc
[modify] https://crrev.com/d496219fd9061eaba1be73be05f8fac1dda86a27/media/mojo/services/mojo_video_decoder_service.cc


### xh...@chromium.org (2019-09-19)

Request to merge the fix in #7 to M78 and if possible M77. The fix is straightforward and the risk is very low.

### rs...@chromium.org (2019-09-19)

Does the fix for this issue also address https://crbug.com/chromium/1005124?

### sh...@chromium.org (2019-09-19)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-19)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xh...@chromium.org (2019-09-19)

[Empty comment from Monorail migration]

### xh...@chromium.org (2019-09-19)

Re #9: Sorry I just saw https://crbug.com/chromium/1005124. Yes, the fix also fixes https://crbug.com/chromium/1005124, as well as potential similar issue in MojoRenderer.

### go...@chromium.org (2019-09-19)

+adetaylor@ (Security TPM) for M78 merge review.

Also +benmason@  as M77 merge request is also added. 

### sh...@chromium.org (2019-09-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-23)

Yes, please merge to M77 and M78. xhwang@ please feel free to merge the unit test code anytime. We are a bit wary of JavaScript test code, but this shouldn't be too risky.

### na...@google.com (2019-09-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-09-23)

Approving merge to M78 branch 3904 based on https://crbug.com/chromium/1004730#c17. Please merge ASAP. 

benmason@ will review M77 merge. 

### be...@chromium.org (2019-09-23)

Merge approved to M77, branch 3865.

### go...@chromium.org (2019-09-23)

Please merge your change to M78 branch 3904 ASAP so we can pick it up for this week beta release. Thank you.

### xh...@chromium.org (2019-09-23)

The fix has been merged to M77 and M78 but it seems the bugdroid is slow to update this bug.

- https://chromium-review.googlesource.com/c/chromium/src/+/1819640
- https://chromium-review.googlesource.com/c/chromium/src/+/1816808

### xh...@chromium.org (2019-09-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-09-23)

Removing "Merge-Approved-77" label per https://crbug.com/chromium/1004730#c22.

### sh...@chromium.org (2019-09-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $15,000 for this report!

### na...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-09-26)

natashapabrai@ Thanks! My employer has a policy of donating reward to charity. Do you mind donating the reward to TearFund (https://www.tearfund.org/) please? Thanks.

### ad...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

xhwang@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### sh...@chromium.org (2019-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### dc...@chromium.org (2020-02-26)

[Empty comment from Monorail migration]

### aw...@google.com (2020-04-01)

[Comment Deleted]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1004730?no_tracker_redirect=1

[Multiple monorail components: Internals>Media>Audio, Internals>Media>Encrypted]
[Monorail mergedwith: crbug.com/chromium/1005124]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050145)*
