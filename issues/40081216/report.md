# Heap-buffer-overflow in media::CopyPlane

| Field | Value |
|-------|-------|
| **Issue ID** | [40081216](https://issues.chromium.org/issues/40081216) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2015-01-19 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0

Steps to reproduce the problem:
1. chrome-asan ch-bofr-copyplane.webm

What is the expected behavior?

What went wrong?
==21491==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fb79713a427 at pc 0x7fb7da1670e9 bp 0x7fb79d29c700 sp 0x7fb79d29beb8
READ of size 854 at 0x7fb79713a427 thread T5 (Media)
    #0 0x7fb7da1670e8 in __asan_memcpy ??:?
    #1 0x7fb7e439de2e in CopyPlane /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/base/video_util.cc:47
    #2 0x7fb7e443692b in media::VpxVideoDecoder::CopyVpxImageTo(vpx_image const*, vpx_image const*, scoped_refptr<media::VideoFrame>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:505
    #3 0x7fb7e4435cdc in media::VpxVideoDecoder::VpxDecode(scoped_refptr<media::DecoderBuffer> const&, scoped_refptr<media::VideoFrame>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:438
    #4 0x7fb7e4435264 in media::VpxVideoDecoder::DecodeBuffer(scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:351
    #5 0x7fb7e4434d56 in media::VpxVideoDecoder::Decode(scoped_refptr<media::DecoderBuffer> const&, base::Callback<void (media::VideoDecoder::Status)> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:324
    #6 0x7fb7e447b517 in media::DecoderStream<(media::DemuxerStream::Type)2>::Decode(scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/decoder_stream.cc:296
    #7 0x7fb7e447c893 in media::DecoderStream<(media::DemuxerStream::Type)2>::OnBufferReady(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../media/filters/decoder_stream.cc:483
[...]

Did this work before? N/A 

Chrome version: 42.0.2281.0 (Developer Build) (64-bit)  Channel: dev
OS Version: 3.13.0
Flash Version: 

Checked that this reproduces on two Linux machines, and seems to reproduce way back in r250226, but not in r200032. The issue should turn up every time after the video played for about a second.

## Attachments

- [ch-bofr-copyplane.webm](attachments/ch-bofr-copyplane.webm) (application/octet-stream, 99.5 KB)

## Timeline

### cl...@chromium.org (2015-01-19)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4592671661228032

### cl...@chromium.org (2015-01-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4592671661228032

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x7f15446be427
Crash State:
  media::CopyPlane
  media::VpxVideoDecoder::CopyVpxImageTo
  media::VpxVideoDecoder::VpxDecode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (99.51 Kb): https://cluster-fuzz.appspot.com/download/AMIfv960ppuPp6gT0AFZqEB-cskp8UTWXhk1dOMQfzatMW7WlwBIeVtqCP4bvEAbHl3TrakcqCPzGy2oa4GByI4ii13sb32lL8AuS91eVhI0-l5KLkFC6ZbajNDfRswH803K4lqx_Na_7Ccc3681BT8IlkADyE_6JuWtHiRaA_Xt7JNYLnsfnYc



### in...@chromium.org (2015-01-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-01-20)

Chris has volunteered to take a look, this one looks relatively specific.

### wa...@chromium.org (2015-01-20)

fgalligan, vigneshv: do you know what we should do in this case? 

It's happening when the alpha image stride and height is different from the normal image. See here: https://code.google.com/p/chromium/codesearch#chromium/src/media/filters/vpx_video_decoder.cc&q=vpx_video_decoder&sq=package:chromium&type=cs&l=505

Relevant call copied for posterity:
  CopyAPlane(vpx_image_alpha->planes[VPX_PLANE_Y],
             vpx_image->stride[VPX_PLANE_Y],
             vpx_image->d_h,
             video_frame->get());

In this case the vpx_image_alpha stride and height are always 416 and 241, but vpx_image changes to 928 and 480 for a few frames, so we try to copy too much data.

Should it be an error if they don't match? Or is the right fix  to replace vpx_image with vpx_image_alpha?

### vi...@chromium.org (2015-01-20)

vpx_image and vpx_image_alpha should always have the same width and height. so it should be an error (i.e. invalid file) if they don't match.

also for posterity, it would be better to replace the image->stride with image_alpha->stride in the CopyAPlane call as the strides don't theoretically have to match (only width/height should match)

### fg...@chromium.org (2015-01-21)

What happens if the file has scaling turned on? Is that disallowed for files with Alpha?

### vi...@chromium.org (2015-01-21)

Scaling on non-keyframes is a VP9 only thing. For VP8, scaling has to happen only on keyframes. And no matter what, width and height of the image and the alpha plane always has to match. Otherwise, the renderer will not be able to overlay the alpha plane and the image.

### wa...@chromium.org (2015-01-21)

Thanks for the details. CL for the proposed changes here: https://codereview.chromium.org/858303002/

### bu...@chromium.org (2015-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1a91a8a6a7132c47a174054f0fb56cc3dc8c069

commit c1a91a8a6a7132c47a174054f0fb56cc3dc8c069
Author: watk <watk@chromium.org>
Date: Wed Jan 21 20:24:58 2015

Reject vp8 video having alpha and image planes of different sizes.

Previously we would accept malformed vp8 video files that had alpha and
image planes with different dimensions. Now they result in a decode error.
Also use the alpha image stride when copying the alpha plane, because it
technically doesn't have to be the same as the image stride.

BUG=449958
TEST=ffmpeg_regression_tests

Review URL: https://codereview.chromium.org/858303002

Cr-Commit-Position: refs/heads/master@{#312420}

[modify] http://crrev.com/c1a91a8a6a7132c47a174054f0fb56cc3dc8c069/media/ffmpeg/ffmpeg_regression_tests.cc
[modify] http://crrev.com/c1a91a8a6a7132c47a174054f0fb56cc3dc8c069/media/filters/vpx_video_decoder.cc


### cl...@chromium.org (2015-01-22)

ClusterFuzz has detected this issue as fixed in range 312321:312458.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4592671661228032

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x7f15446be427
Crash State:
  media::CopyPlane
  media::VpxVideoDecoder::CopyVpxImageTo
  media::VpxVideoDecoder::VpxDecode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=312321:312458

Minimized Testcase (99.51 Kb): https://cluster-fuzz.appspot.com/download/AMIfv960ppuPp6gT0AFZqEB-cskp8UTWXhk1dOMQfzatMW7WlwBIeVtqCP4bvEAbHl3TrakcqCPzGy2oa4GByI4ii13sb32lL8AuS91eVhI0-l5KLkFC6ZbajNDfRswH803K4lqx_Na_7Ccc3681BT8IlkADyE_6JuWtHiRaA_Xt7JNYLnsfnYc

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

Approved for M41 (branch: 2272)

### da...@chromium.org (2015-01-26)

watk@ can you merge this to M41?  Here are the directions:

http://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/git-drover.html

### bu...@chromium.org (2015-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/19e56da295644db647c67070ce9cd3e1251429e7

commit 19e56da295644db647c67070ce9cd3e1251429e7
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Jan 26 20:02:02 2015

Reject vp8 video having alpha and image planes of different sizes.

Previously we would accept malformed vp8 video files that had alpha and
image planes with different dimensions. Now they result in a decode error.
Also use the alpha image stride when copying the alpha plane, because it
technically doesn't have to be the same as the image stride.

BUG=449958
TEST=ffmpeg_regression_tests

Review URL: https://codereview.chromium.org/858303002

Cr-Commit-Position: refs/heads/master@{#312420}
(cherry picked from commit c1a91a8a6a7132c47a174054f0fb56cc3dc8c069)

R=dalecurtis@chromium.org

Review URL: https://codereview.chromium.org/881533002

Cr-Commit-Position: refs/branch-heads/2272@{#116}
Cr-Branched-From: 827a380cfdb31aa54c8d56e63ce2c3fd8c3ba4d4-refs/heads/master@{#310958}

[modify] http://crrev.com/19e56da295644db647c67070ce9cd3e1251429e7/media/ffmpeg/ffmpeg_regression_tests.cc
[modify] http://crrev.com/19e56da295644db647c67070ce9cd3e1251429e7/media/filters/vpx_video_decoder.cc


### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congrats - $2000 for this report.

### ti...@google.com (2015-03-03)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### ti...@google.com (2015-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-30)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/449958?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081216)*
