# global-buffer-overflow at vp56_rac_get_prob_branchy

| Field | Value |
|-------|-------|
| **Issue ID** | [40081152](https://issues.chromium.org/issues/40081152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2015-01-10 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.3.0

Steps to reproduce the problem:
1. $ chrome-asan ch-segv-unknown-renorm.webm

What is the expected behavior?

What went wrong?
ASan spots an error.

Did this work before? N/A 

Chrome version: 42.0.2273.0 (Developer Build)   Channel: dev
OS Version: 3.2.0-4-amd64
Flash Version: 

Opening the movie seems to cause one of two different traces, one with random looking addresses, which doesn't sound good.

==30219==AddressSanitizer: while reporting a bug found another one. Ignoring.
==30219==ERROR: AddressSanitizer: SEGV on unknown address 0x7fffe85836ae (pc 0x7fffe81a8e39 bp 0x7fff841ddab0 sp 0x7fff841dd2c0 T73)
    #0 0x7fffe81a8e38 in vp56_rac_renorm /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:229
    #1 0x7fffe81d0f75 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2479
    #2 0x7fffe815f17e in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
    #3 0x7ffff1feab4f in start_thread ??:0

==22767==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fffe82b0880 at pc 0x7fffe81bc742 bp 0x7fffb920e2b0 sp 0x7fffb920e2a8
READ of size 1 at 0x7fffe82b0880 thread T9
    #0 0x7fffe81bc741 in vp56_rac_get_prob_branchy /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7fffe81d0f75 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2479
    #2 0x7fffe815f17e in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
    #3 0x7ffff1feab4f in start_thread ??:0

## Attachments

- [ch-segv-unknown-renorm.webm](attachments/ch-segv-unknown-renorm.webm) (application/octet-stream, 47.0 KB)

## Timeline

### cl...@chromium.org (2015-01-10)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6242551706157056

### cl...@chromium.org (2015-01-10)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4584007378403328

### cl...@chromium.org (2015-01-10)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6616604610658304

### cl...@chromium.org (2015-01-10)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5731617699004416

### in...@chromium.org (2015-01-13)

Can't reproduce on CF. CF says

[22855:22855:0110/163444:ERROR:gpu_video_decode_accelerator.cc(268)] Not implemented reached in void content::GpuVideoDecodeAccelerator::Initialize(const media::VideoCodecProfile, IPC::Message *)HW video decode acceleration not available.

Let me try on the shiny physical bot.

### cl...@chromium.org (2015-01-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5751283792216064

### ao...@gmail.com (2015-01-13)

I checked with https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-311055.zip?generation=1421101204969000&alt=media again on my desktop and test machine (Debian Wheezy/A10-6800K and Ubuntu 14.04.1/AMD Phenom II X6 w/ some AMD graphics card). Both of them happen to have AMD GPUs and are using Gallium 0.4, but video decoding seems to be software only for me, and this seems to reproduce also when running in Xvfb. Audio does play also when using Xvfb.

The issue should happen every time immediately when opening the window, or after playing for about two seconds. Here are two more traces that I got from playing the video in 311055. New ones didn't seem to come up.

==24302==AddressSanitizer: while reporting a bug found another one. Ignoring.
==24302==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f63ee069a80 at pc 0x7f63f174865a bp 0x7f63c26fd2b0 sp 0x7f63c26fd2a8
READ of size 1 at 0x7f63ee069a80 thread T9
    #0 0x7f63f1748659 in read_mv_component /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7f63f175cf75 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2479
    #2 0x7f63f16eb17e in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
    #3 0x7f63fb506b4f in start_thread ??:0

==9535==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fdfbb14d2d9 at pc 0x7fdfbb024002 bp 0x7fdf8b8cb270 sp 0x7fdf8b8cb268
==9535==AddressSanitizer: while reporting a bug found another one. Ignoring.
READ of size 1 at 0x7fdfbb14d2d9 thread T10
    #0 0x7fdfbb024001 in decode_mb_mode /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7fdfbb037f75 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2479
    #2 0x7fdfbafc617e in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
    #3 0x7fdfc587b181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312 (discriminator 2)


### da...@chromium.org (2015-01-13)

Hmm, maybe related to AMD specific optimizations which could be why CF can't reproduce. I'll glance over the code.

### cl...@chromium.org (2015-01-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-01-15)

I'm not able to reproduce this, the code doesn't seem AMD specific and the stack traces don't seem to not make sense or are inlined in an odd way.

Are you able to reproduce this using ffmpeg/ffplay if you build ffmpeg from http://git.videolan.org/?p=ffmpeg.git with the configure option --toolchain=clang-asan ?

### cl...@chromium.org (2015-01-15)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### da...@chromium.org (2015-01-15)

I don't think this should be RBB until we can verify it's reproducible.

### in...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### ao...@gmail.com (2015-01-16)

These might help:
 - seems to have appeared between 267414 and 267516. https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-267516.zip?generation=1398962094401000&alt=media is the first build in which this reproduces. 
 - reproduces every time with asan-symbolized-linux-release-311689, including on one machine with Debian and Intel CPU and GPU, also when running in Xvfb with --single-process
 - reproduces rarely with content shell of asan-symbolized-linux-release-311689
 - does not reproduce with asan-linux-debug-311689 (neigher chrome nor content shell)
 - does not reproduce with ffmpeg trunk built with clang-asan

### da...@chromium.org (2015-01-16)

Reproduced on the linked build, but that was a pre-39-stable build and does not reproduce on 39 stable. Will retry on M40 and M41.  Still can't reproduce it locally.

### da...@chromium.org (2015-01-16)

Hmm, I can't reproduce on M40 beta. I can reproduce on the latest builds. On my local build I can't repro, but I can if I drop in the libffmpegsumo.so from the ToT builds...

inferno: Do you have the build settings used for that bot? It doesn't look like they're the same as http://build.chromium.org/p/chromium.memory/builders/Linux%20ASan%20LSan%20Builder

### da...@chromium.org (2015-01-16)

Found them and can repro now:
https://code.google.com/p/chromium/codesearch#chromium/build/masters/master.chromium.lkgr/master_lkgr_cfg.py&l=152

Digging in.

### da...@chromium.org (2015-01-17)

Hmm, this might be a code gen issue, either in ASAN or Clang, I'm not sure.  Still trying to piece it together, but swapping out this (seemingly correct) assembly function for its c equivalent resolves the issue:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/ffmpeg/libavcodec/x86/vp56_arith.h

The C equivalent function can be seen here:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/ffmpeg/libavcodec/vp56.h&l=251

This would jive with the reproduction difficulties on release builds.

### da...@chromium.org (2015-01-17)

Actually, looks like it happens with the C version as well, but far more rarely, with those compile flags we end up with a race condition while operating on the VP56RangeCoder structure; sometimes the values get corrupted and record a negative c->high value which blows up the table access at:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/ffmpeg/libavcodec/vp56.h&l=228

With a few asserts within the vp56_rac_get_prob() function it's easy to see that the values are being changed by other threads:

$ ./out2/Release/ffmpeg_regression_tests --video-threads=1 --single-process-tests --gtest_filter=Cr447860* 
Note: Google Test filter = Cr447860*
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from Cr447860/FFmpegRegressionTest
[ RUN      ] Cr447860/FFmpegRegressionTest.BasicPlayback/0
[matroska,webm @ 0x61b00001b980] Unknown entry 0x97
Truncating packet of size 6446 to 6143
[matroska,webm @ 0x61b00001b980] Unknown entry 0x97
Truncating packet of size 6446 to 6143
[       OK ] Cr447860/FFmpegRegressionTest.BasicPlayback/0 (113 ms)
[----------] 1 test from Cr447860/FFmpegRegressionTest (113 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (113 ms total)
[  PASSED  ] 1 test.


dalecurtis@xorax /d/code/chrome/src $ ./out2/Release/ffmpeg_regression_tests --video-threads=2 --single-process-tests --gtest_filter=Cr447860* 
Note: Google Test filter = Cr447860*
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from Cr447860/FFmpegRegressionTest
[ RUN      ] Cr447860/FFmpegRegressionTest.BasicPlayback/0
Assertion c->high == (old_high - low) failed at ../../third_party/ffmpeg/libavcodec/x86/vp56_arith.h:56

This happens with both the C and assembly versions. Notably I'm not able to trigger any kind of race condition when building the code w/o the additional flags used for the symbolized release bot: release_extra_cflags="-gline-tables-only -O1 -fno-inline-functions -fno-inline".

The threading story is incredibly complicated with this code though, so it's hard to say if there's a real issue here or something with the codegen which wrecks ffmpeg's relatively fragile threading story. Notably I can't reproduce this with the ffmpeg command line even with the extra cflags...

Given the limited scope of reproduction, I recommend reducing the severity and priority of this issue. I'll try a little more to figure out if there's a repro case I can pass upstream, but I don't expect to make much progress here.

### cl...@chromium.org (2015-02-02)

dalecurtis@: Uh oh! This issue is still open and hasn't been updated in the last 16 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### da...@chromium.org (2015-02-03)

Dan is rolling ffmpeg right now, over him to see if this still repros after the roll.

### cl...@chromium.org (2015-02-18)

sandersd@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ao...@gmail.com (2015-02-19)

I assume it's rolled by now. The repro still crashes here every time. Reloading it a few times with https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-316949.zip?generation=1424323997534000&alt=media gives:

$ opt/chrome-asan/chrome --disable-setuid-sandbox ch-segv-unknown-renorm.webm 2>&1 | symbolize | c++filt | grep -A 4 "ERROR: AddressSani"
==7==ERROR: AddressSanitizer: SEGV on unknown address 0x7f4c2db4c495 (pc 0x7f4c2e001239 bp 0x7f4c03670a80 sp 0x7f4c03670280 T7)
==7==AddressSanitizer: while reporting a bug found another one. Ignoring.
    #0 0x7f4c2e001238 in vp56_rac_renorm /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:230
    #1 0x7f4c2e0295a5 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2485
    #2 0x7f4c2dfb6fee in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
--
==24==ERROR: AddressSanitizer: SEGV on unknown address 0x7f4bae13ca40 (pc 0x7f4c2e002479 bp 0x7f4c03480a80 sp 0x7f4c03480280 T7)
    #0 0x7f4c2e002478 in vp56_rac_renorm /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:230
    #1 0x7f4c2e0295a5 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2485
    #2 0x7f4c2dfb6fee in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
    #3 0x7f4c3872b181 in start_thread /build/buildd/eglibc-2.19/nptl/pthread_create.c:312 (discriminator 2)
--
==37==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7f4c2e13c96b at pc 0x7f4c2e014c22 bp 0x7f4c03680270 sp 0x7f4c03680268
READ of size 1 at 0x7f4c2e13c96b thread T7
    #0 0x7f4c2e014c21 in read_mv_component /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7f4c2e0295a5 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2485
    #2 0x7f4c2dfb6fee in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
--
==50==ERROR: AddressSanitizer: unknown-crash on address 0x7fff0f45bd20 at pc 0x7f4c461ecd0a bp 0x7fff0f45bc90 sp 0x7fff0f45bc88
WRITE of size 8 at 0x7fff0f45bd20 thread T0 (chrome)
    #0 0x7f4c461ecd09 in FillLayer /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/layout/style/FillLayer.cpp:110 (discriminator 4)
    #1 0x7f4c4592ef88 in blink::authorStyleInfo(blink::StyleResolverState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:537
    #2 0x7f4c4592ed43 in blink::StyleResolver::adjustLayoutStyle(blink::StyleResolverState&, blink::Element*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:554
--
==63==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7f4c2e13c9cf at pc 0x7f4c2e01513e bp 0x7f4c0342a270 sp 0x7f4c0342a268
READ of size 1 at 0x7f4c2e13c9cf thread T7
    #0 0x7f4c2e01513d in read_mv_component /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7f4c2e0295a5 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2485
    #2 0x7f4c2dfb6fee in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100
--
==76==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7f4c2e13c4ea at pc 0x7f4c2e014cf2 bp 0x7f4c0352a270 sp 0x7f4c0352a268
READ of size 1 at 0x7f4c2e13c4ea thread T7
    #0 0x7f4c2e014cf1 in read_mv_component /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp56.h:228
    #1 0x7f4c2e0295a5 in vp78_decode_mb_row_sliced /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/vp8.c:2485
    #2 0x7f4c2dfb6fee in worker /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavcodec/pthread_slice.c:100


### da...@chromium.org (2015-02-19)

Yeah, there's something about the asan code gen flags which is turning the vp8 decoder into a racy minefield.  Neither Dan nor I have had time to track this down further yet, but it appears limited to asan builds only as far as I can tell.

### in...@chromium.org (2015-02-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-10)

sandersd@: Uh oh! This issue is still open and hasn't been updated in the last 18 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### da...@chromium.org (2015-03-10)

AFICT there's no impact in release builds.

### in...@chromium.org (2015-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-24)

No merge required (#30 mentions no impact in release builds)

### sc...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-07)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

Adding reward-na based on c#26.

### cl...@chromium.org (2015-08-13)

Bulk update: removing view restriction from closed bugs.

### mb...@chromium.org (2015-10-01)

Sending this back to the panel based on the information in https://crbug.com/chromium/532967.

### ti...@google.com (2015-10-13)

Updating severity

### ti...@google.com (2015-10-13)

[Comment Deleted]

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

[Comment Deleted]

### ti...@google.com (2015-10-13)

Congratulations - $500 for this report. We'll credit you alongside  https://crbug.com/chromium/532967  and pay you $500 each.

We'll start payment later this week, so you should receive the cash ~2 weeks from today. I'll update this bug with a CVE shortly

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/447860?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081152)*
