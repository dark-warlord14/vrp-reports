# Heap-use-after-free in vorbis_decode_frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40080557](https://issues.chromium.org/issues/40080557) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>FFmpeg |
| **Reporter** | cl...@chromium.org |
| **Assignee** | xh...@chromium.org |
| **Created** | 2014-09-30 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4833912221073408

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-use-after-free READ 2
Crash Address: 0xded28272
Crash State:
  vorbis_decode_frame
  avcodec_decode_audio4
  media::FFmpegAudioDecoder::FFmpegDecode
  

Minimized Testcase (97.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94fynbmP7VrCmejYF02QTiT_6G2WSDb7_Hs2XQlmBEy1XhRQIs2xEr1E_BtVnwFvBwRmmzS0lySun8BjLler0SapWgKUGCAudacqI_kUTlaTrvBooXkIZCkAv8b_xQ8RhoWvnuW_hanp9Cn6T1pxh2toGI2kDg_Rqmoy9jyKe6WuVl43JU

Filer: inferno

## Attachments

- [chrome-heap-use-after-free-vorbisresiduedecodeinternal9.video](attachments/chrome-heap-use-after-free-vorbisresiduedecodeinternal9.video) (application/octet-stream, 3.7 KB)

## Timeline

### in...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2014-09-30)

Probably only M39 since we just did an FFmpeg roll.

John, can you take a look?

### da...@chromium.org (2014-09-30)

Oh interesting, I just realized this was on ARM; possibly it means the size of the allocation is making incorrect assumptions about the primitive type width.

### in...@chromium.org (2014-09-30)

ClusterFuzz says this bug is old, says impacts stable, beta based on regression range. Anyway, the person analyzing will figure it out.

### jr...@chromium.org (2014-10-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Bumping to M39 based on https://crbug.com/chromium/419060#c3. Please update if it turns out that this affects M38.

### cl...@chromium.org (2014-10-09)

jrummell@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-16)

jrummell@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-24)

jrummell@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### at...@gmail.com (2014-10-24)


This is not an ARM only bug.

Here is a repro-file that reproduces the crash on: 

OS:Ubuntu 14.04
Chromium: 40.0.2197.0 (Developer Build) 
Revision	05bc9c84e44660e9ba56f5566092228d3674679a-refs/heads/master@{#300565}

The repro-file has to be loaded with a small html-snippet:

<html><body>
<video autoplay src="chrome-heap-use-after-free-vorbisresiduedecodeinternal9.video" ></video>
</body></html>

ASAN-trace:

==11327==ERROR: AddressSanitizer: heap-use-after-free on address 0x619000074672 at pc 0x7fab3ad7f153 bp 0x7fab0fff8140 sp 0x7fab0fff8138
READ of size 2 at 0x619000074672 thread T12 (Media)
    #0 0x7fab3ad7f152 in vorbis_residue_decode_internal /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vorbisdec.c:1416:25    #1 0x7fab3ad7f152 in vorbis_residue_decode /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vorbisdec.c:1525:0
    #2 0x7fab3ad77ef9 in vorbis_parse_audio_packet /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vorbisdec.c:1661:19
    #3 0x7fab3ad75d00 in vorbis_decode_frame /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vorbisdec.c:1792:16
    #4 0x7fab3ad6b87c in avcodec_decode_audio4 /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/utils.c:2428:19
    #5 0x7fab57016aef in media::FFmpegAudioDecoder::FFmpegDecode(scoped_refptr<media::DecoderBuffer> const&, bool*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/ffmpeg_audio_decoder.cc:257:24
.
.
.
0x619000074672 is located 498 bytes inside of 1024-byte region [0x619000074480,0x619000074880)
freed by thread T12 (Media) here:
    #0 0x7fab4d36f19e in __interceptor_realloc ??:0:0
    #1 0x7fab3ae6afa4 in av_realloc_f /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavutil/mem.c:179:9
    #2 0x7fab3acc6858 in alloc_table /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/bitstream.c:114:22
    #3 0x7fab3acc5d78 in build_table /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/bitstream.c:171:19
    #4 0x7fab3acc6309 in build_table /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/bitstream.c:226:21
    #5 0x7fab3acc5782 in ff_init_vlc_sparse /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/bitstream.c:337:11
.
.
.

### in...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### jr...@chromium.org (2014-10-29)

I am able to reproduce this crash on ToT running with ASAN.

It is not a Heap-use-after-free error. It is caused by an index out of bounds.

failing line src/third_party/ffmpeg/libavcodec/vorbisdec.c:1416:25
    int vqbook  = vr->books[vqclass][pass];

Added some debugging logs, and I get:
vqclass 190, pass = 0, vr = 0x61d000082a80
=================================================================
==10==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d000083672

vr->books defined as:
    int16_t books[64][8];

So even though it is attempting to read a realloced block of memory, it is really reading off the end of the block allocated @ 0x61d000082a80.

### jr...@chromium.org (2014-10-30)

Have sent a possible patch to ffmpeg. Waiting for a response.

### jr...@chromium.org (2014-10-31)

This was fixed in ffmpeg about a month ago. It will get merged into Chromium with the M40 ffmpeg roll (https://crbug.com/chromium/426560).

Commit: 8c50704ebf1777bee76772c4835d9760b3721057
Date:   Fri Oct 3 18:12:34 2014
avcodec/vorbisdec: Fix off by 1 error in ptns_to_read
Fixes read of uninitialized memory

### bu...@chromium.org (2014-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25eeccf24ff44b010f12879c57979d89bc9ee820

commit 25eeccf24ff44b010f12879c57979d89bc9ee820
Author: xhwang <xhwang@chromium.org>
Date: Fri Nov 07 01:50:46 2014

Roll FFmpeg DEPS.

This includes two bug fixes.

BUG=419060,427266

Review URL: https://codereview.chromium.org/705193002

Cr-Commit-Position: refs/heads/master@{#303160}

[modify] https://chromium.googlesource.com/chromium/src.git/+/25eeccf24ff44b010f12879c57979d89bc9ee820/DEPS


### xh...@chromium.org (2014-11-07)

Fixed by: https://gerrit.chromium.org/gerrit/72103

### cl...@chromium.org (2014-11-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

ClusterFuzz has detected this issue as fixed in range 303095:303227.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4833912221073408

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Heap-use-after-free READ 2
Crash Address: 0xded28272
Crash State:
  vorbis_decode_frame
  avcodec_decode_audio4
  media::FFmpegAudioDecoder::FFmpegDecode
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=303095:303227

Minimized Testcase (97.79 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94fynbmP7VrCmejYF02QTiT_6G2WSDb7_Hs2XQlmBEy1XhRQIs2xEr1E_BtVnwFvBwRmmzS0lySun8BjLler0SapWgKUGCAudacqI_kUTlaTrvBooXkIZCkAv8b_xQ8RhoWvnuW_hanp9Cn6T1pxh2toGI2kDg_Rqmoy9jyKe6WuVl43JU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### xh...@chromium.org (2014-11-13)

This has been in the trunk for a few days and it's confirmed by ClusterFuzz. Request to merge to M39.

### cl...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2014-11-14)

[Empty comment from Monorail migration]

### xh...@chromium.org (2014-11-18)

Assign to myself to handle the merge request.

amineer: Double check with you.. Is it okay to merge this fix back to M39?

### am...@chromium.org (2014-11-18)

+mbarbella@ from the security team.  M39 has already been released to stable (the merge request came after stable candidate was cut by a few days) and I don't plan to take anything that isn't critical.  Martin, do we need this in M39, or can we wait until M40?

### mb...@chromium.org (2014-11-18)

If there is going to be a patch to M39, this looks like it would be worth including.

### am...@chromium.org (2014-12-03)

Moving back to merge review, same justification as https://code.google.com/p/chromium/issues/detail?id=427266#c29

### am...@chromium.org (2014-12-03)

spoke with dale, merge is approved for m39 branch 2171.  please roll deps by tomorrow evening PST.

### [Deleted User] (2014-12-10)

Has this been merged into 40?

### xh...@chromium.org (2014-12-10)

This was fixed in M40 per #16 and verified on M40 per #19.

The fix was also merged to M39 in https://codereview.chromium.org/755623005/, but I don't know why this issue wasn't updated with that.

### [Deleted User] (2014-12-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-05)

adjusting severity based on c#13.

### ti...@google.com (2015-01-22)

Congratulations - $1500 for this report. Panel notes: "$1000 for bug - not a use after free but an index out of bounds. +$500 ClusterFuzz bonus".

### cl...@chromium.org (2015-02-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/419060?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/426560]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080557)*
