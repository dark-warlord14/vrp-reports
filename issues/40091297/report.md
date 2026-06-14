# Security: Use of uninitialized memory caused by AcmReceiver::AcmReceiver()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091297](https://issues.chromium.org/issues/40091297) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>Audio |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zi...@gmail.com |
| **Assignee** | hl...@chromium.org |
| **Created** | 2018-05-04 |
| **Bounty** | $500.00 |

## Description

[This is a WebRTC bug, that I am filing here because there doesn't appear to be a security template at https://bugs.chromium.org/p/webrtc/issues/entry]

AcmReceiver::AcmReceiver() (modules\audio_coding\acm2\acm_receiver.cc) causes other code in its class to use uninitialized memory by failing fully to initialize a buffer. Line 41, below, initializes only the first half of |last_audio_buffer_|, since, per line 36, the buffer is actually |AudioFrame::kMaxDataSizeSamples * sizeof (int16_t)| bytes long:

35: AcmReceiver::AcmReceiver(const AudioCodingModule::Config& config)
36:     : last_audio_buffer_(new int16_t[AudioFrame::kMaxDataSizeSamples]),
37:       neteq_(NetEq::Create(config.neteq_config, config.decoder_factory)),
38:       clock_(config.clock),
39:       resampled_last_output_frame_(true) {
40:   assert(clock_);
41:   memset(last_audio_buffer_.get(), 0, AudioFrame::kMaxDataSizeSamples);
42: }

I found this bug in the context of Firefox 59.0.2.

You can see the bug in action by starting Firefox, attaching a debugger to it, and putting a BP on line 36. Now go to https://webrtc.github.io/samples/src/content/peerconnection/audio, click "call", and let Firefox use your microphone. When the BP fires, look at the disassembly and notice that line 36 allocates 0x1e00 bytes of memory. Then step line 41 and see that it initializes only 0xf00 bytes of that memory.

This failure can cause a data leak.

On Firefox, this bug is latent because Firefox's allocator appears always to initializes heap blocks, but other codebases might not do that.

This bug is still present in Master: https://webrtc.googlesource.com/src/+/master/modules/audio_coding/acm2/acm_receiver.cc . The Firefox source for the module is in media\webrtc\trunk\webrtc\modules\audio_coding\acm2\acm_receiver.cc .

## Timeline

### ts...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>Audio]

### sh...@chromium.org (2018-05-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-05)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-05-07)

Henrik - can you take a look?

### hl...@chromium.org (2018-05-07)

Thanks for reporting. I'm on it.


### hl...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-08)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/76c106725a227c6c1221356a303d007d707b0a45

commit 76c106725a227c6c1221356a303d007d707b0a45
Author: Henrik Lundin <henrik.lundin@webrtc.org>
Date: Tue May 08 11:40:04 2018

ACM: Properly initialize last_audio_buffer_ array

Only half of the array was initialized. Now all of it is.

Bug: chromium:839960
Change-Id: If8bbe12c4c4c0dc0d529c93b22e49a94ecb09919
Reviewed-on: https://webrtc-review.googlesource.com/74820
Reviewed-by: Karl Wiberg <kwiberg@webrtc.org>
Commit-Queue: Henrik Lundin <henrik.lundin@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#23167}
[modify] https://crrev.com/76c106725a227c6c1221356a303d007d707b0a45/modules/audio_coding/acm2/acm_receiver.cc


### hl...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### hl...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-05-08)

+awhalley@ for M67 merge review (CL listed at #7 needs canary baking, landed in trunk 3 hrs back)

### bu...@chromium.org (2018-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df04b893a4d29cdb1f48473735a33d998d5e1d76

commit df04b893a4d29cdb1f48473735a33d998d5e1d76
Author: webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue May 08 16:01:46 2018

Roll src/third_party/webrtc/ 826738b78..5b2b69207 (7 commits)

https://webrtc.googlesource.com/src.git/+log/826738b78c6a..5b2b692079e6

$ git log 826738b78..5b2b69207 --date=short --no-merges --format='%ad %ae %s'

Created with:
  roll-dep src/third_party/webrtc
BUG=chromium:none,chromium:None,chromium:839960


The AutoRoll server is located here: https://webrtc-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_chromium_archive_rel_ng;master.tryserver.chromium.mac:mac_chromium_archive_rel_ng
TBR=webrtc-chromium-sheriffs-robots@google.com

Change-Id: I45f3d07c607b57730126b195af1cffa4a8064f87
Reviewed-on: https://chromium-review.googlesource.com/1049954
Commit-Queue: webrtc-chromium-autoroll <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: webrtc-chromium-autoroll <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#556811}
[modify] https://crrev.com/df04b893a4d29cdb1f48473735a33d998d5e1d76/DEPS


### go...@chromium.org (2018-05-08)

hlundin@@, pls update the bug with canary result tomorrow. Thank you.

### sh...@chromium.org (2018-05-09)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-05-09)

Any update on canary result?

### hl...@chromium.org (2018-05-09)

The fix was included in 68.0.3425.0, which was released in Win and Mac canary channels some 14 hours ago. I guess it is a bit early to tell what the result was.

Also, since this particular issue wasn't found through any of Chrome's or WebRTC's regular monitoring tools, but rather as a report from a Firefox developer, I doubt that we will be able to see any change in our stats based on the fix.

We can come back next week and revisit the the data if you want to.


### go...@chromium.org (2018-05-09)

Thank you  hlundin@.
awhalley@ (Security TPM) will be doing M67 merge review (Ptal https://crbug.com/chromium/839960#c17).


### aw...@google.com (2018-05-11)

govind@ - good for 67

### go...@chromium.org (2018-05-11)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/839960#c19. Pls merge by Monday morning MTV time.

### hl...@chromium.org (2018-05-14)

Merged to M67 in https://webrtc-review.googlesource.com/c/src/+/76641.

### aw...@google.com (2018-05-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### zi...@gmail.com (2018-05-21)

I reported this bug to Mozilla, which uses this library in Firefox, prior to reporting it here. I have not disclosed it elsewhere.

### aw...@google.com (2018-05-21)

The VRP panel decided to award $500 for this report, thanks! How would you like to be credited in release notes?

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### zi...@gmail.com (2018-05-21)

> The VRP panel decided to award $500 for this report, thanks! How would you like 
> to be credited in release notes?

Thank you. Please credit me as "Ronald E. Crane".

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-28)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/89c6af1578dd6ed086fd144fdd19ae5fa7183435

commit 89c6af1578dd6ed086fd144fdd19ae5fa7183435
Author: Henrik Lundin <henrik.lundin@webrtc.org>
Date: Mon May 14 17:13:43 2018

[MERGE TO M67] ACM: Properly initialize last_audio_buffer_ array

Only half of the array was initialized. Now all of it is.

TBR=henrik.lundin@webrtc.org

(cherry picked from commit 76c106725a227c6c1221356a303d007d707b0a45)

Bug: chromium:839960
Change-Id: If8bbe12c4c4c0dc0d529c93b22e49a94ecb09919
Reviewed-on: https://webrtc-review.googlesource.com/74820
Reviewed-by: Karl Wiberg <kwiberg@webrtc.org>
Commit-Queue: Henrik Lundin <henrik.lundin@webrtc.org>
Cr-Original-Commit-Position: refs/heads/master@{#23167}
Reviewed-on: https://webrtc-review.googlesource.com/76641
Reviewed-by: Henrik Lundin <henrik.lundin@webrtc.org>
Cr-Commit-Position: refs/branch-heads/67@{#28}
Cr-Branched-From: 4da18e89bdee78df4478b66cdd0e6f6a38d61b4d-refs/heads/master@{#22779}
[modify] https://crrev.com/89c6af1578dd6ed086fd144fdd19ae5fa7183435/modules/audio_coding/acm2/acm_receiver.cc


### is...@google.com (2020-10-28)

This issue was migrated from crbug.com/chromium/839960?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091297)*
