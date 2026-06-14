# Security: Stack out-of-bounds writes in WebmMuxer::AddAudioTrack

| Field | Value |
|-------|-------|
| **Issue ID** | [40093994](https://issues.chromium.org/issues/40093994) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>MediaRecording |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ml...@stanford.edu |
| **Assignee** | mc...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Security: Stack out-of-bounds writes in WebmMuxer::AddAudioTrack  

I'm not certain that its triggerable, but it looks as if it should be fixed

**REPRODUCTION CASE**

1. Stack allocated opus header in AddAudioTrack:

uint8\_t opus\_header[OPUS\_EXTRADATA\_SIZE]; // and OPUS\_EXTRADATA\_SIZE is 19  

(see: <https://cs.chromium.org/chromium/src/media/muxers/webm_muxer.cc?type=cs&q=WebmMuxer::AddAudioTrack&g=0&l=303>)

2. Function calls WriteOpusHeader(params, opus\_header);  
   
   (function <https://cs.chromium.org/chromium/src/media/muxers/webm_muxer.cc?l=20&gsn=WriteOpusHeader>)
3. WriteOpusHeader does:

header[OPUS\_EXTRADATA\_NUM\_COUPLED\_OFFSET] = 0;

where  

OPUS\_EXTRADATA\_NUM\_STREAMS\_OFFSET = OPUS\_EXTRADATA\_SIZE,  

OPUS\_EXTRADATA\_NUM\_COUPLED\_OFFSET = OPUS\_EXTRADATA\_NUM\_STREAMS\_OFFSET + 1,  

OPUS\_EXTRADATA\_STREAM\_MAP\_OFFSET = OPUS\_EXTRADATA\_NUM\_STREAMS\_OFFSET + 2  

(allocated size was OPUS\_EXTRADATA\_SIZE)

4. It continues to write out of bounds:  
   
   for (int i = 0; i < params.channels(); ++i) {  
   
   header[OPUS\_EXTRADATA\_STREAM\_MAP\_OFFSET + i] =  
   
   kOpusVorbisChannelMap[params.channels() - 1][i];  
   
   }

## Timeline

### mm...@chromium.org (2019-02-08)

On a relevant note, existing fuzz targets do not cover that particular branch which has a potential overflow reported: https://chromium-coverage.appspot.com/reports/630030_fuzzers_only/linux/chromium/src/media/muxers/webm_muxer.cc.html#L41

Regarding the report, +1, not clear is it's triggerable, but looks legit.



[Monorail components: Blink>Media>Audio]

### mm...@chromium.org (2019-02-08)

Btw, mlfbrown@, how did you find this issue, if you don't mind to share? Just manual audit or did you use any tools?

### ml...@stanford.edu (2019-02-09)

No problem: we found it with a new prototype checking system.

### sh...@chromium.org (2019-02-22)

mcasas: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2019-02-26)

Assigning to me and lowering the prio since the WebRTC infra doesn't support
stereo (or anything above mono for the case) MediaStreamTracks, so this code
is essentially unreachable.

[Monorail components: -Blink>Media>Audio Blink>MediaRecording]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8095e5d9d219ceff1aab5d00aaec59d629d50270

commit 8095e5d9d219ceff1aab5d00aaec59d629d50270
Author: Miguel Casas <mcasas@chromium.org>
Date: Wed Feb 27 16:48:19 2019

WebmMuxer: do not support >2 audio channels

ToT WebmMuxer supports Opus with >2 channels. This configuration is
never actually used (because AudioMediaStreams in Chrome don't
support it [1]) and can cause a write after bounds (see bug). This
CL removes the guilty code by not supporting >2 channels audio.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/third_party/blink/renderer/modules/mediarecorder/README.md#can-record-stereo

Bug: 930035
Change-Id: I964c66bc660e76ee152563804c63276643f4acd6
Reviewed-on: https://chromium-review.googlesource.com/c/1489185
Commit-Queue: Miguel Casas <mcasas@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/heads/master@{#636056}
[modify] https://crrev.com/8095e5d9d219ceff1aab5d00aaec59d629d50270/media/muxers/webm_muxer.cc


### mc...@chromium.org (2019-02-27)

[Empty comment from Monorail migration]

### mc...@chromium.org (2019-02-27)

Removing RVS since effectively the code was unreachable anyway (and 
it should be fixed now).

### sh...@chromium.org (2019-02-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-07)

Congrats! The Panel decided to reward $500 for this report and is interested in learning more about the prototype testing system you are developing. 

Please include how you would like to be credited in our release notes and a member from the finance team will be in touch shortly. 

### aw...@google.com (2019-03-07)

[Empty comment from Monorail migration]

### ml...@stanford.edu (2019-03-08)

Thanks! mlfbrown in release notes is great

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-26)

Pls apply appropriate OSs label.

### ad...@chromium.org (2019-03-26)

mcasas@, can you confirm that this code is entirely unreachable (#8) rather than "essentially unreachable" (#5)? It will make a difference as to whether we backport it into M74. Any other evidence for that decision is also appreciated. Thanks!

### mc...@chromium.org (2019-03-26)

#18: I'm not sure I understand the difference :-) but the code was 
100% unreachable due to WebRTC not supporting multi audio tracks
whatsoever as to M74 and as of today. So the code was not exercisable.
Makes sense?

### go...@chromium.org (2019-03-26)

Pls apply appropriate OSs label.

### go...@chromium.org (2019-03-29)

Pls apply appropriate OSs label.

### go...@chromium.org (2019-03-31)

+adetaylor@ (security TPM) for M74 merge review. We also need to know which OSs this bug is applicable too.

### ad...@chromium.org (2019-04-01)

mcasas@ thanks muchly!
govind@, per #19 this code is not reachable, so no need to merge to M74.

### go...@chromium.org (2019-04-01)

Rejecting merge to M74 based on https://crbug.com/chromium/930035#c23. 

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-01)

Confirmed affected platforms with mcasas@; adding.

### sh...@chromium.org (2019-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-06)

This issue was migrated from crbug.com/chromium/930035?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093994)*
