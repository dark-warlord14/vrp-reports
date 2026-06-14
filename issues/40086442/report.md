# WebRTC crash (?) on appear.in

| Field | Value |
|-------|-------|
| **Issue ID** | [40086442](https://issues.chromium.org/issues/40086442) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Video |
| **Reporter** | ph...@googlemail.com |
| **Assignee** | ph...@chromium.org |
| **Created** | 2017-01-09 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 57.0.2970.0
Operating System: Linux 4.4.0-57-generic

Hard to reproduce. I was trying to hunt down simulcast issues where when rewriting packets into a single stream which lead to video corruption. And close to the point where I suspected this happens it crashed.


****DO NOT CHANGE BELOW THIS LINE****
Crash ID: crash/d31282d080000000


## Timeline

### ph...@googlemail.com (2017-01-09)

another one:
Crash ID: crash/0e6e5e2480000000

### ph...@googlemail.com (2017-01-09)

and another one. Not even close to the point where I suspected this happened (which was rtp sequence number wraparound)

Crash ID: crash/099622d080000000

### aj...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>Video]

### ch...@chromium.org (2017-01-10)

philipel@: Please take a look:

https://crash.corp.google.com/browse?stbtiq=d31282d080000000#3
https://crash.corp.google.com/browse?stbtiq=0e6e5e2480000000#4
https://crash.corp.google.com/browse?stbtiq=099622d080000000#4

### bu...@chromium.org (2017-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/1c056254a6b8b6521ad2799c8c705b8bbfb9c210

commit 1c056254a6b8b6521ad2799c8c705b8bbfb9c210
Author: philipel <philipel@webrtc.org>
Date: Tue Jan 31 17:53:12 2017

Fix race condition in FrameBuffer2

If the frame buffer is cleared while the decoding thread is waiting to acquire
the lock in order to return the |next_frame_it| will be invalidated.

BUG=chromium:679306

Review-Url: https://codereview.webrtc.org/2668743002
Cr-Commit-Position: refs/heads/master@{#16384}

[modify] https://crrev.com/1c056254a6b8b6521ad2799c8c705b8bbfb9c210/webrtc/modules/video_coding/frame_buffer2.cc
[modify] https://crrev.com/1c056254a6b8b6521ad2799c8c705b8bbfb9c210/webrtc/modules/video_coding/frame_buffer2.h


### ph...@chromium.org (2017-02-01)

The fix in #5 fix only one bug that caused webrtc::video_coding::FrameBuffer::NextFrame to crash, but there is another bug that also cause crashes in this function.

### ph...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-04-19)

Copy pasting from a duplicate:

I have found what is causing the crash, and it is due to the FrameBuffer2 not handling large jumps in picture id correctly.

For example when receiving these frames in a stream:
5453, 5454, 15670, 29804, 29805, 29806, 33819, 41248

Then the order will be considered to be:
5453 < 5454 < 15670 < 29804 < 29805 < 29806 < 33819

But when inserting 41248 it is both 33819 < 41248 and 41248 < 5453 due to the picture id wrapping at 2^16. This cause problems in the NextFrame function when we want to iterate over all continuous frames to find the best frame to return next.

### ph...@googlemail.com (2017-04-19)

\o/

the typical case where that happens is when simulcast is used -- I don't think SFUs will rewrite the picture id. Can you clear the buffer when receiving a keyframe?

### ho...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### ho...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-04-20)

Since this bug can cause us to dereference non-nullptrs we consider this to be a security risk.

Fix here: https://codereview.chromium.org/2830723002/

### bu...@chromium.org (2017-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/146a48b0fabef7e74f2a2b62fb5cb45f9b393408

commit 146a48b0fabef7e74f2a2b62fb5cb45f9b393408
Author: philipel <philipel@webrtc.org>
Date: Thu Apr 20 11:04:38 2017

Check if the order of frames becomes ambiguous if we were to insert the incoming frame, and if so, clear the FrameBuffer.

BUG=chromium:679306

Review-Url: https://codereview.webrtc.org/2830723002
Cr-Commit-Position: refs/heads/master@{#17785}

[modify] https://crrev.com/146a48b0fabef7e74f2a2b62fb5cb45f9b393408/webrtc/modules/video_coding/frame_buffer2.cc
[modify] https://crrev.com/146a48b0fabef7e74f2a2b62fb5cb45f9b393408/webrtc/modules/video_coding/frame_buffer2_unittest.cc


### ph...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-20)

> Since this bug can cause us to dereference non-nullptrs we consider this to be a security risk.

In this case I'm marking this as a high severity bug as the security sheriff.

philipel: Can you please confirm that this bug can be triggered by an attacker supplied stream?

### go...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-04-20)

#16
An attacker can craft a malicious stream which will cause this crash. 

What happens is that we iterate past the end of the map containing all frames, so the pointer we dereference is whatever the invalid iterator was pointing to.

I'm not sure if the attacker can decide which memory address that will be dereferences, but there might be some clever way.

### me...@chromium.org (2017-04-20)

#18: Thanks for confirming!

### ph...@googlemail.com (2017-04-20)

the effort to reliably trigger it is quite high, it would take me a week of effort to create the preconditions.

meacer@ (or someone else): if you could view-restrict 
 https://bugs.chromium.org/p/chromium/issues/detail?id=708074 that would be good as it contains information that would allow a targeted reproduction (to someone who knows webrtc and vp8 sufficiently well... that is an extremly limited audience)

### aw...@google.com (2017-04-20)

Done.

### to...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-04-21)

We still don't have a canary version with the fix in #13 included, but it should be built later today.

### sh...@chromium.org (2017-04-21)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-21)

This bug requires manual review: Only 3 days from stable, we might already have a stable candidate build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-21)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-04-21)

I have tested canary version 60.0.3077.0 on mac and I can no longer reproduce the crash.

### li...@chromium.org (2017-04-21)

For Mac in stable channel-58.0.3029.81 this crash ranks #5, 45 reports with 41 unique clients.


### go...@chromium.org (2017-04-21)

+ awhalley@ for M58 merge review.

### go...@chromium.org (2017-04-21)

Please merge your change to M59 branch #3071 latest before 4:00 PM PT, Monday (04/24) so we can take it for next week last M59 dev release. Thank you.

### sh...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/6d56d2ebf0e40bc73dee99093ac7c223ddc7b6e5

commit 6d56d2ebf0e40bc73dee99093ac7c223ddc7b6e5
Author: philipel <philipel@webrtc.org>
Date: Mon Apr 24 08:56:55 2017

Check if the order of frames becomes ambiguous if we were to insert the incoming frame, and if so, clear the FrameBuffer.

BUG=chromium:679306

Review-Url: https://codereview.webrtc.org/2830723002
Cr-Commit-Position: refs/heads/master@{#17785}
(cherry picked from commit 146a48b0fabef7e74f2a2b62fb5cb45f9b393408)

R=stefan@webrtc.org

Review-Url: https://codereview.webrtc.org/2835963002 .
Cr-Commit-Position: refs/branch-heads/59@{#4}
Cr-Branched-From: 10d095d4f743bc16f8e486e156c48a6d023b32c5-refs/heads/master@{#17657}

[modify] https://crrev.com/6d56d2ebf0e40bc73dee99093ac7c223ddc7b6e5/webrtc/modules/video_coding/frame_buffer2.cc
[modify] https://crrev.com/6d56d2ebf0e40bc73dee99093ac7c223ddc7b6e5/webrtc/modules/video_coding/frame_buffer2_unittest.cc


### sh...@chromium.org (2017-04-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-04-24)

Per https://crbug.com/chromium/679306#c34, this is already merged to M59. Hence, removing "Merge-Approved-59" label. Thank you.

### aw...@google.com (2017-04-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### kj...@chromium.org (2017-04-25)

[Empty comment from Monorail migration]

### an...@chromium.org (2017-04-25)

awhalley@ did you have the chance to review the merge for m58 (requested in #23)?

### an...@chromium.org (2017-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-27)

anatolid@, govind@ - good for 58

### go...@chromium.org (2017-04-27)

Per https://crbug.com/chromium/679306#c37, this is NOT a Stable blocker. 
Is it absolutely necessary to take this merge in for next M58 refresh and will be a fully safe merge? We can't take any risk at all as M58 is already in stable currently rolling out to 50% of users on Windows & Mac, 100% Linux.

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

Nice one! The VRP panel decided to award $500 for this report. A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-05-01)

Based on comments by holmer@ and confirmation that this is a safe merge from both developer and security team, approving this merge for M58. 

### bu...@chromium.org (2017-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/6c9caaad7dfdea48a72a691d760ea0d89cb64816

commit 6c9caaad7dfdea48a72a691d760ea0d89cb64816
Author: Zijie He <zijiehe@chromium.org>
Date: Mon May 01 17:48:01 2017

Check if the order of frames becomes ambiguous if we were to insert the incoming frame, and if so, clear the FrameBuffer.

On behalf of Philip Eliasson (philipel@webrtc.org).

BUG=chromium:679306

Review-Url: https://codereview.webrtc.org/2830723002
Cr-Commit-Position: refs/heads/master@{#17785}
(cherry picked from commit 146a48b0fabef7e74f2a2b62fb5cb45f9b393408)

Review-Url: https://codereview.webrtc.org/2848283002 .
Cr-Commit-Position: refs/branch-heads/58@{#19}
Cr-Branched-From: f31969a584bcafe9406c214a9d4c3afb49d19650-refs/heads/master@{#16937}

[modify] https://crrev.com/6c9caaad7dfdea48a72a691d760ea0d89cb64816/webrtc/modules/video_coding/frame_buffer2.cc
[modify] https://crrev.com/6c9caaad7dfdea48a72a691d760ea0d89cb64816/webrtc/modules/video_coding/frame_buffer2_unittest.cc


### go...@chromium.org (2017-05-01)

Per https://crbug.com/chromium/679306#c48, this is already merged to M58. Hence removing "Merge-Approved-58" label. Thank you zijiehe@ for merging the change to M58.

### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2017-05-02)

[Empty comment from Monorail migration]

### hu...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### ph...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### pa...@google.com (2017-05-09)

[Empty comment from Monorail migration]

### ju...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/e95b78bd8da556fe85d1603f6ef5558e50c81189

commit e95b78bd8da556fe85d1603f6ef5558e50c81189
Author: tommi <tommi@webrtc.org>
Date: Sun May 14 14:23:11 2017

Add a couple of checks to FrameBuffer while we're continuing to look at RtpFrameReferenceFinder.

BUG=chromium:679306
TBR=terelius@webrtc.org, philipel@webrtc.org

Review-Url: https://codereview.webrtc.org/2879073002
Cr-Commit-Position: refs/heads/master@{#18140}

[modify] https://crrev.com/e95b78bd8da556fe85d1603f6ef5558e50c81189/webrtc/modules/video_coding/frame_buffer2.cc


### bu...@chromium.org (2017-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/7daab660ce0e35fecad717fefab4cf935d3c253e

commit 7daab660ce0e35fecad717fefab4cf935d3c253e
Author: Stefan Holmer <stefan@webrtc.org>
Date: Thu May 18 15:20:13 2017

Add a couple of checks to FrameBuffer while we're continuing to look at RtpFrameReferenceFinder.

BUG=chromium:679306
R=philipel@webrtc.org
TBR=terelius@webrtc.org

Review-Url: https://codereview.webrtc.org/2879073002
Cr-Commit-Position: refs/heads/master@{#18140}
(cherry picked from commit e95b78bd8da556fe85d1603f6ef5558e50c81189)

Review-Url: https://codereview.webrtc.org/2891073002 .
Cr-Commit-Position: refs/branch-heads/59@{#11}
Cr-Branched-From: 10d095d4f743bc16f8e486e156c48a6d023b32c5-refs/heads/master@{#17657}

[modify] https://crrev.com/7daab660ce0e35fecad717fefab4cf935d3c253e/webrtc/modules/video_coding/frame_buffer2.cc


### sh...@chromium.org (2017-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679306?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/708074]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086442)*
