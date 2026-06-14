# WebRTC UsingFlexibleMode OOB memory write from picture id

| Field | Value |
|-------|-------|
| **Issue ID** | [40086039](https://issues.chromium.org/issues/40086039) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Video |
| **Platforms** | Windows |
| **Reporter** | is...@vulture.fm |
| **Assignee** | ph...@chromium.org |
| **Created** | 2016-11-21 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36

Steps to reproduce the problem:
The problem is reproducible in our web app while playing and swapping around lots of video. Unfortunately, the repro is not fully deterministic. Though it does almost always crash after a period of several minutes.

However, the bug itself is easily visible by looking at the source code, so nailing down an exact repro (which may be related to a race condition or other randomness) is less a priority for us than just reporting this. Details in the "What went wrong" box.

What is the expected behavior?
Chrome tab doesn't crash while playing video.

What went wrong?
There are several potentials for OOB memory writes in webrtc/modules/video_coding/main/source/decoding_state.cc in VCMDecodingState::SetState, with at least one confirmed in several minidumps.

We suspect this commit introduced the bug: https://chromium.googlesource.com/external/webrtc/+blame/cfc319be1d6afec77bd41eeb70d3e7886dd524db/webrtc/modules/video_coding/main/source/decoding_state.cc#76

The one we have recorded in several minidumps happens at line 93 (different line in master due to other commits since that one) :
 frame_decoded_[frame_index] = true;
Here, frame_index is (uint16_t)0xffff, and 
  bool frame_decoded_[kFrameDecodedLength=(1<<7)];
Tracing back:
 uint16_t frame_index = picture_id_ % kFrameDecodedLength;
picture_id_ is a signed int with value -1 (kNoPictureId). thus the % operation returns -1 and truncates down to 0xffff when converting to uint16_t. Since frame_decoded_ has only 128 entries, this allows out of bounds accesses. The while loop on line 86 may also be able to write large blocks of memory beyond the end of the array. However, all the minidumps we collected are on the above line mentioned.

It seems the problem stems from:

  picture_id_ = frame->PictureId();

which bubbles to the session_info.cc code:

int VCMSessionInfo::PictureId() const {
  if (packets_.empty())
    return kNoPictureId;
  if (packets_.front().video_header.codec == kRtpVideoVp8) {
    return packets_.front().video_header.codecHeader.VP8.pictureId;
  } else if (packets_.front().video_header.codec == kRtpVideoVp9) {
    return packets_.front().video_header.codecHeader.VP9.picture_id;
  } else {
    return kNoPictureId;
  }
}

for which there are many cases where it can return kNoPictureId (-1), but a lack of error(?) checking allows  this -1 value to be used as an unsigned index, allowing OOB memory writes.

Without knowing the code myself, I can't suggest the best bugfix for this, but at the very least, checking for a -1 picture id value as well as making sure frame_decoded_[]'s length is never exceeded, would be a good start.

Did this work before? Yes Before the commit that introduced the bug

Chrome version: 54.0.2840.99  Channel: stable
OS Version: 6.3
Flash Version: 

The minidumps we have are for an internal version of our Electron app, so probably not terribly useful to you without symbols etc, or I would upload the .dmp files. However, it also reproduces in a Chrome 54 browser tab (crashes). We won't be able to provide an external repro website until a later date, but if the explanation given for the code was insufficient, we will try to follow up with that after release dates etc.

## Timeline

### is...@vulture.fm (2016-11-22)

-  if (UsingFlexibleMode(frame)) {
+  if (picture_id_ >= 0 && UsingFlexibleMode(frame)) {

No idea if this is a correct fix for the problem, but... we tried using this patch, and it seems to have fixed not only crashes, but another completely unrelated (we thought) video freeze issue that was occurring. I suppose the same issue, when not crashing, could still have caused other unintended consequences resulting from OOB memory write.

You guys can probably figure out a better/more real solution, just thought I'd share some preliminary results.

### me...@chromium.org (2016-11-22)

Thanks for the report and the detailed analysis!

philipel: Can you please take a look and see if this is related to https://codereview.webrtc.org/1431283002? Thanks.

[Monorail components: Blink>WebRTC>Video]

### sh...@chromium.org (2016-11-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/ee414d90b046e3e7feb4130b0567091a43c36702

commit ee414d90b046e3e7feb4130b0567091a43c36702
Author: philipel <philipel@webrtc.org>
Date: Tue Nov 29 15:01:23 2016

Added sanity check to VCMDecodingState::UsingFlexibleMode to prevent OOB error.

BUG=chromium:667504

Review-Url: https://codereview.webrtc.org/2534883003
Cr-Commit-Position: refs/heads/master@{#15298}

[modify] https://crrev.com/ee414d90b046e3e7feb4130b0567091a43c36702/webrtc/modules/video_coding/decoding_state.cc


### ph...@chromium.org (2016-11-29)

As meacer@ said, thanks for the detailed bug report!

A fix has now landed, isu@ could you try it out and verify that it solved your problem?

### is...@vulture.fm (2016-11-30)

Removed our patch and added yours instead -- seems to be working! :)

### ph...@chromium.org (2016-11-30)

Thanks for testing it!

### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-09)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-09)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### ph...@chromium.org (2016-12-09)

dimu@, do I have to create a merge CL or is it automated in the case of the sheriffbot making the merge request?

### sh...@chromium.org (2016-12-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/external/webrtc.git/+/598cf6f23ad635d07ecc78406e82607bbb70c048

commit 598cf6f23ad635d07ecc78406e82607bbb70c048
Author: philipel <philipel@webrtc.org>
Date: Mon Dec 12 16:35:30 2016

Added sanity check to VCMDecodingState::UsingFlexibleMode to prevent OOB error.

BUG=chromium:667504

TBR=stefan@webrtc.org

Review-Url: https://codereview.webrtc.org/2534883003
Cr-Commit-Position: refs/heads/master@{#15298}
(cherry picked from commit ee414d90b046e3e7feb4130b0567091a43c36702)

Review URL: https://codereview.webrtc.org/2573483002 .

Cr-Commit-Position: refs/branch-heads/56@{#6}
Cr-Branched-From: 613152af11d6e9a4d046af3c48a7be7642dfcc68-refs/heads/master@{#15101}

[modify] https://crrev.com/598cf6f23ad635d07ecc78406e82607bbb70c048/webrtc/modules/video_coding/decoding_state.cc


### ph...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-12)

Congratulations, the panel awarded $3,000 for this bug!

### aw...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/667504?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086039)*
