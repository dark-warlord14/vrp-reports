# WebRTC: Potential Use-after-free in VP8 Block Decoding (MFQE feature)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093356](https://issues.chromium.org/issues/40093356) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2018-6155 |
| **Reporter** | ey...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2018-12-09 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36

Steps to reproduce the problem:
Always happens, the feature will never work.

The MFQE feature in VP8 block decoding (WebRTC) *never* works, due to a bug. If it will work, there will be a Use-after-free vulnerability in it, similar to: https://bugs.chromium.org/p/chromium/issues/detail?id=842265.

What is the expected behavior?
The MFQE feature of the VP8 decoding should work. And once active, it shouldn't be vulnerable.

What went wrong?
libvpx has duplicate declarations for the configuration flags.
First declaration in vp8/common/ppflags.h:
enum {
  VP8D_NOFILTERING = 0,
  VP8D_DEBLOCK = 1 << 0,
  VP8D_DEMACROBLOCK = 1 << 1,
  VP8D_ADDNOISE = 1 << 2,
  VP8D_MFQE = 1 << 3
};

The second declaration is in vpx/vp8.h:
/*!\brief post process flags
 *
 * The set of macros define VP8 decoder post processing flags
 */
enum vp8_postproc_level {
  VP8_NOFILTERING = 0,
  VP8_DEBLOCK = 1 << 0,
  VP8_DEMACROBLOCK = 1 << 1,
  VP8_ADDNOISE = 1 << 2,
  VP8_DEBUG_TXT_FRAME_INFO = 1 << 3, /**< print frame information */
  VP8_DEBUG_TXT_MBLK_MODES =
      1 << 4, /**< print macro block modes over each macro block */
  VP8_DEBUG_TXT_DC_DIFF = 1 << 5,   /**< print dc diff for each macro block */
  VP8_DEBUG_TXT_RATE_INFO = 1 << 6, /**< print video rate info (encoder only) */
  VP8_MFQE = 1 << 10
};

While the first enum is used internally, the second enum is used by WebRTC. Although MFQE is on by default, the difference between VP8_MFQE (1 << 10) and VP8D_MFQE (1 << 3) causes libvpx to think that this flag is never set, effectively disabling this feature.

When this feature will be re-enabled, it will enable an attacker to send a frame to function "vp8_multiframe_quality_enhance" in file vp8/common/mfqe.c, which contains the same vulnerability (CVE-2018-6155) as was patched in this ticket: https://bugs.chromium.org/p/chromium/issues/detail?id=842265

Did this work before? N/A 

Chrome version: 70.0.3538.110  Channel: n/a
OS Version: 10.0
Flash Version:

## Timeline

### su...@chromium.org (2018-12-09)

[Empty comment from Monorail migration]

### dt...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC]

### ca...@chromium.org (2018-12-11)

Assigning high severity to be on the safe side since the vulnerability is in the code, but the code seems to be unreached in the current state (as described by the reporter). 

### ca...@chromium.org (2018-12-11)

jianj: Passing to you since you fixed the other similar issue, can you take a look and reassign if appropriate? Thanks.

### ji...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libvpx/+/763f8318de2cee41d748539cee5810fc0efcad68

commit 763f8318de2cee41d748539cee5810fc0efcad68
Author: Marco Paniconi <marpan@google.com>
Date: Wed Dec 12 06:03:50 2018

vp8: Fix to enabling MFQE

Remove the unused *_DEBUG_* enum values in vpx/vp8.h

This fixes issue with enabling MFQE, which was
caused in 4807f15, where the unused DEBUG flags
were removed from common/ppflags.h but not in vp8.h.

BUG=913246

Change-Id: I47f114ef20adc084cb4883add5ac3ebf58ae9f1d

[modify] https://crrev.com/763f8318de2cee41d748539cee5810fc0efcad68/vpx/vp8.h


### bu...@chromium.org (2018-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/088948eb741c000b5cf1f46c2078be8351e71b94

commit 088948eb741c000b5cf1f46c2078be8351e71b94
Author: Jerome Jiang <jianj@google.com>
Date: Thu Dec 13 23:05:42 2018

Roll src/third_party/libvpx/source/libvpx/ 418acaa0b..c62d9d568 (25 commits)

https://chromium.googlesource.com/webm/libvpx.git/+log/418acaa0bd06..c62d9d568fc6

$ git log 418acaa0b..c62d9d568 --date=short --no-merges --format='%ad %ae %s'
2018-12-11 jzern update libwebm to libwebm-1.0.0.27-352-g6ab9fcf
2018-12-11 angiebird Replace mv_arr by pyramid_mv_arr
2018-12-11 marpan vp8: Fix to enabling MFQE
2018-12-11 angiebird Change interface of motion_compensated_prediction
2018-12-10 angiebird Move prepare_nb_full_mvs to vp9_mcomp.c
2018-12-11 deepa.kg Use undamped adjustment for rate correction factors
2018-12-10 jzern test/svc_end_to_end_test: fix SetConfig() signature
2018-12-10 jingning Clean up condition logics in rc_pick_q_and_bounds_two_pass()
2018-12-10 jianj Refactor svc_*_test.cc
2018-12-06 huisu Remove redundant code about motion vector test
2018-12-08 jzern test/svc_*_test: fix SetConfig() signature
2018-12-06 jianj vp9 svc: add test for scaling partition on 1080p crash.
2018-12-04 jianj vp9 screen: Update motion search offset when set to NSTEP.
2018-12-06 jzern test/*: use std::*tuple
2018-12-06 huisu Add enum definition for subpel search precision
2018-12-07 johann.koenig apply -Wextra to third_party/
2018-11-06 sdeng Add high bit Hadamard 32x32 avx2 implementation
2018-10-30 sdeng Add satd avx2 implementation
2018-12-05 angiebird Implement find_prev_nb_full_mvs
2018-12-05 angiebird Implement get_full_mv()
(...)

Created with:
  roll-dep src/third_party/libvpx/source/libvpx
R=johannkoenig@google.com
BUG=913246

Change-Id: Ia09fbe7274726dfbd8760522f4e34341d1c63f8b
Reviewed-on: https://chromium-review.googlesource.com/c/1377136
Reviewed-by: Johann Koenig <johannkoenig@google.com>
Commit-Queue: Jerome Jiang <jianj@google.com>
Cr-Commit-Position: refs/heads/master@{#616469}
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/DEPS
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/README.chromium
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/linux/chromeos-arm-neon/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/linux/chromeos-arm64/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/linux/generic/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/linux/ia32/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/linux/x64/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/mac/ia32/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/mac/x64/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/nacl/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/vpx_version.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/win/arm64/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/win/ia32/vpx_dsp_rtcd.h
[modify] https://crrev.com/088948eb741c000b5cf1f46c2078be8351e71b94/third_party/libvpx/source/config/win/x64/vpx_dsp_rtcd.h


### ey...@gmail.com (2018-12-14)

Just wanted to mention that since the first bug was resolved, and the MFQE feature is now active, the vulnerability that I pointed out to now endangers anyone who uses libvpx. Being mirrored to Github, it now effects everyone who will use the library untill the additional security patch will be issued.

Maybe it would have been a better idea to first patch the security vulnerability I mentioned, and only then fix the MFQE bug.

### ji...@chromium.org (2018-12-14)

Thanks for reporting..

I made a quick fix here
https://chromium-review.googlesource.com/c/webm/libvpx/+/1378790

Hopefully it'll get rolled in soon.

### bu...@chromium.org (2018-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libvpx/+/0e408ea67cd142a3f27189d7e00cbabea96a28d6

commit 0e408ea67cd142a3f27189d7e00cbabea96a28d6
Author: Jerome Jiang <jianj@google.com>
Date: Fri Dec 14 23:00:29 2018

vp8: Fix potential use-after-free in mfqe.

Similar issue to 842265.

The pointer in vp8 postproc refers to show_frame_mi which is only
updated on show frame. However, when there is a no-show frame which also
changes the size (thus new frame buffers allocated), show_frame_mi is
not updated with new frame buffer memory.

Change the pointer in postproc to mi which is always updated.

BUG=913246

Change-Id: I5159ba7134a06db472c29a1d84b8d39bb60c7254

[modify] https://crrev.com/0e408ea67cd142a3f27189d7e00cbabea96a28d6/vp8/common/mfqe.c


### bu...@chromium.org (2018-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3

commit e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3
Author: Jerome Jiang <jianj@google.com>
Date: Mon Dec 17 21:19:25 2018

Roll src/third_party/libvpx/source/libvpx/ 18d260d13..d8f89c49e (2 commits)

https://chromium.googlesource.com/webm/libvpx.git/+log/18d260d13f2b..d8f89c49e17b

$ git log 18d260d13..d8f89c49e --date=short --no-merges --format='%ad %ae %s'
2018-12-14 jianj vp8: Fix potential use-after-free in mfqe.
2018-12-13 sdeng Remove unused code in tiny_ssim

Created with:
  roll-dep src/third_party/libvpx/source/libvpx
R=johannkoenig@google.com

BUG=913246

Change-Id: I886386eaf644c2c5c85234451c5fd53a042920a2
Reviewed-on: https://chromium-review.googlesource.com/c/1380536
Commit-Queue: Johann Koenig <johannkoenig@google.com>
Reviewed-by: Johann Koenig <johannkoenig@google.com>
Cr-Commit-Position: refs/heads/master@{#617232}
[modify] https://crrev.com/e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3/DEPS
[modify] https://crrev.com/e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3/third_party/libvpx/README.chromium
[modify] https://crrev.com/e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3/third_party/libvpx/source/config/vpx_version.h


### ji...@chromium.org (2018-12-17)

Fix has been rolled in chromium.

Feel free to reopen if there is any problem.

### sh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-12-20)

How safe is this merge?

### ji...@chromium.org (2018-12-20)

This change is very safe to merge. A similar change[1] has been working well since M68.

[1]https://chromium.googlesource.com/webm/libvpx/+/52add5896661d186dec284ed646a4b33b607d2c7

### ab...@google.com (2018-12-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-12-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libvpx/+/be3c1ee28aeb699c508b02cfcccf7f13feaed3eb

commit be3c1ee28aeb699c508b02cfcccf7f13feaed3eb
Author: Jerome Jiang <jianj@google.com>
Date: Wed Dec 26 18:39:56 2018

vp8: Fix potential use-after-free in mfqe.

Similar issue to 842265.

The pointer in vp8 postproc refers to show_frame_mi which is only
updated on show frame. However, when there is a no-show frame which also
changes the size (thus new frame buffers allocated), show_frame_mi is
not updated with new frame buffer memory.

Change the pointer in postproc to mi which is always updated.

BUG=913246

Change-Id: I5159ba7134a06db472c29a1d84b8d39bb60c7254
(cherry picked from commit 0e408ea67cd142a3f27189d7e00cbabea96a28d6)

[modify] https://crrev.com/be3c1ee28aeb699c508b02cfcccf7f13feaed3eb/vp8/common/mfqe.c


### sh...@chromium.org (2018-12-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/971a85b22c834e6fb803d31a1417833aecfcb75e

commit 971a85b22c834e6fb803d31a1417833aecfcb75e
Author: Jerome Jiang <jianj@google.com>
Date: Sat Dec 29 19:28:07 2018

libvpx: update DEPS for merge mfqe fix.

BUG=913246

Change-Id: I3792cfe0b490b71d29533e2616ac250e069d30f6
Reviewed-on: https://chromium-review.googlesource.com/c/1391410
Reviewed-by: James Zern <jzern@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#529}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/971a85b22c834e6fb803d31a1417833aecfcb75e/DEPS


### cr...@appspot.gserviceaccount.com (2018-12-29)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/971a85b22c834e6fb803d31a1417833aecfcb75e

Commit: 971a85b22c834e6fb803d31a1417833aecfcb75e
Author: jianj@google.com
Commiter: jzern@chromium.org
Date: 2018-12-29 19:28:07 +0000 UTC

libvpx: update DEPS for merge mfqe fix.

BUG=913246

Change-Id: I3792cfe0b490b71d29533e2616ac250e069d30f6
Reviewed-on: https://chromium-review.googlesource.com/c/1391410
Reviewed-by: James Zern <jzern@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#529}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $1,000 :) 

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?


### ey...@gmail.com (2019-01-10)

Thank you very much for the decided reward :)

It would be great if you could mention me in the release notes as follows:
"Eyal Itkin from Check Point Software Technologies"

Thanks again.

### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/913246?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093356)*
