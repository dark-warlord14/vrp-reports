# Negative-size-param in vp9_dec_setup_mi

| Field | Value |
|-------|-------|
| **Issue ID** | [40081236](https://issues.chromium.org/issues/40081236) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-01-22 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
The attached webm file crash the latest 32-bit ASAN build of chromium as follows:

=================================================================
==9999==ERROR: AddressSanitizer: negative-size-param: (size=-4206592)
    #0 0xe4540861 in __asan_memset ??:?
    #1 0xf2124317 in vp9_dec_setup_mi /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decoder.c:49
    #2 0xf218eeda in vp9_init_context_buffers /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/common/vp9_alloccommon.c:161
    #3 0xf211d74b in resize_context_buffers /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decodeframe.c:699
    #4 0xf211b430 in setup_frame_size /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decodeframe.c:712
    #5 0xf21115a6 in read_uncompressed_header /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decodeframe.c:1310
    #6 0xf21103f5 in vp9_decode_frame /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decodeframe.c:1544
    #7 0xf2125164 in vp9_receive_compressed_data /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/decoder/vp9_decoder.c:300
    #8 0xf2076959 in decode_one /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/vp9_dx_iface.c:319
    #9 0xf2075ed8 in decoder_decode /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vp9/vp9_dx_iface.c:418
    #10 0xf207b1fe in vpx_codec_decode /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/libvpx/source/libvpx/vpx/src/vpx_decoder.c:122
    #11 0xf1e9a5b4 in media::VpxVideoDecoder::VpxDecode(scoped_refptr<media::DecoderBuffer> const&, scoped_refptr<media::VideoFrame>*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:374
    #12 0xf1e99f1e in media::VpxVideoDecoder::DecodeBuffer(scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:351
    #13 0xf1e999a9 in media::VpxVideoDecoder::Decode(scoped_refptr<media::DecoderBuffer> const&, base::Callback<void (media::VideoDecoder::Status)> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../media/filters/vpx_video_decoder.cc:324
    #14 0xf1eff1ca in media::DecoderStream<(media::DemuxerStream::Type)2>::Decode(scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../media/filters/decoder_stream.cc:296
    #15 0xf1f0085b in media::DecoderStream<(media::DemuxerStream::Type)2>::OnBufferReady(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../media/filters/decoder_stream.cc:483
    #16 0xf1f0cfac in base::internal::RunnableAdapter<void (media::DecoderStream<(media::DemuxerStream::Type)2>::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>::Run(media::DecoderStream<(media::DemuxerStream::Type)2>*, media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/bind_internal.h:185
    #17 0xf1f0ceb9 in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (media::DecoderStream<(media::DemuxerStream::Type)2>::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, void (base::WeakPtr<media::DecoderStream<(media::DemuxerStream::Type)2> > const&, media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&)>::MakeItSo(base::internal::RunnableAdapter<void (media::DecoderStream<(media::DemuxerStream::Type)2>::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, base::WeakPtr<media::DecoderStream<(media::DemuxerStream::Type)2> > const&, media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/bind_internal.h:391
    #18 0xf1f0cd8f in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (media::DecoderStream<(media::DemuxerStream::Type)2>::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, void (media::DecoderStream<(media::DemuxerStream::Type)2>*, media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&), void (base::WeakPtr<media::DecoderStream<(media::DemuxerStream::Type)2> >)>, void (media::DecoderStream<(media::DemuxerStream::Type)2>*, media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>::Run(base::internal::BindStateBase*, media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/bind_internal.h:619
    #19 0xf1de6fde in base::Callback<void (media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>::Run(media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&) const /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/callback.h:396
...

Thread T5 (Media) created by T0 (chrome) here:
    #0 0xe453f44f in pthread_create ??:?
    #1 0xe5ceabd8 in base::(anonymous namespace)::CreateThread(unsigned int, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:120
    #2 0xe5cea94c in base::PlatformThread::Create(unsigned int, base::PlatformThread::Delegate*, base::PlatformThreadHandle*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:206
    #3 0xe5cfdb19 in base::Thread::StartWithOptions(base::Thread::Options const&) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/threading/thread.cc:108
    #4 0xe5cfd97a in base::Thread::Start() /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../base/threading/thread.cc:93
    #5 0xee445698 in GetMediaThreadTaskRunner /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../content/renderer/render_thread_impl.cc:1733
    #6 0xee3f3f94 in content::RenderFrameImpl::createMediaPlayer(blink::WebLocalFrame*, blink::WebURL const&, blink::WebMediaPlayerClient*, blink::WebContentDecryptionModule*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../content/renderer/render_frame_impl.cc:1868
    #7 0xee3f585b in non-virtual thunk to content::RenderFrameImpl::createMediaPlayer(blink::WebLocalFrame*, blink::WebURL const&, blink::WebMediaPlayerClient*, blink::WebContentDecryptionModule*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../content/renderer/render_frame_impl.cc:1895
    #8 0xe9081c9a in blink::createWebMediaPlayer(blink::WebMediaPlayerClient*, blink::WebURL const&, blink::LocalFrame*, blink::WebContentDecryptionModule*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/web/WebMediaPlayerClientImpl.cpp:58
    #9 0xe9081651 in blink::WebMediaPlayerClientImpl::load(blink::WebMediaPlayer::LoadType, WTF::String const&, blink::WebMediaPlayer::CORSMode) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/web/WebMediaPlayerClientImpl.cpp:208
    #10 0xe972f932 in blink::HTMLMediaElement::startPlayerLoad() /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1058
    #11 0xe972e04e in loadResource /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:1023
    #12 0xe97289a1 in blink::HTMLMediaElement::loadNextSourceChild() /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:959
    #13 0xe972d585 in blink::HTMLMediaElement::selectMediaResource() /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:942
    #14 0xe9728daa in loadInternal /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:875
    #15 0xe9723389 in blink::HTMLMediaElement::loadTimerFired(blink::Timer<blink::HTMLMediaElement>*) /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLMediaElement.cpp:689
    #16 0xe9756efd in blink::Timer<blink::HTMLMediaElement>::fired() /mnt/data/b/build/slave/ASan_Release__32-bit_x86_with_V8-ARM__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/Timer.h:147 (discriminator 4)
    ...

SUMMARY: AddressSanitizer: negative-size-param ??:0 ??
==9999==ABORTING



VERSION
Chrome Version: asan-symbolized-v8-arm-linux-release-312321
Operating System: Linux

REPRODUCTION CASE
Attached as repro.webm

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab



## Attachments

- [repro.webm](attachments/repro.webm) (application/octet-stream, 1.2 KB)

## Timeline

### cl...@chromium.org (2015-01-22)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5162675410567168

### in...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5162675410567168

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  vp9_dec_setup_mi
  vp9_init_context_buffers
  resize_context_buffers
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=296165:296530

Minimized Testcase (1.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94etmm4xm-bp43EUEhJHBLFDSoYztjDvoF8FGNIwK8_JkxGuK-VpjxUAilsX4t23iOD-TDQ8gFVtwcYGiPIK94_chHx0rOZHPNGbeehhcm_wlimPcsw4Eqy8C9tG5ndPjher3PtXGYe5jnTbs0JyFbWIzyu9g



### in...@chromium.org (2015-01-22)

Author: johannkoenig@chromium.org 
Component: libvpx
Changelist: https://chromium.googlesource.com/chromium/deps/libvpx.git/+/87997d490ae52aa962a985c95b3cddf7f8832641
Time: Mon Sep 22 21:40:59 2014
Files vp9_alloccommon.c, vp9_decodeframe.c, vp9_decoder.c are changed in this cl (and is part of stack frame #2, "vp9_init_context_buffers")
Minimum distance from crash line to modified line: 7. (file: vp9_decodeframe.c, crashed on: 714, modified: 721).

Suspected component: libvpx

### ri...@chromium.org (2015-01-24)

This is just from glancing over the code a bit, but it looks like:

In setup_frame_size, vp9_read_frame_size is called, which reads a (presumably user-controlled) width and height as 16 bit integers
It then calls resize_context_buffers(cm, width, height), which calls vp9_alloc_context_buffers -> vp9_set_mb_mi. vp9_set_mb_mi does:

...

  cm->mi_cols = aligned_width >> MI_SIZE_LOG2;
  cm->mi_rows = aligned_height >> MI_SIZE_LOG2;
  cm->mi_stride = calc_mi_size(cm->mi_cols);
...

The end result is that cm->mi_rows and cm->mi_stride can both be as big as approximately 1<<13. Then vp9_init_context_buffers is called from resize_context_buffers, which calls vp9_dec_setup_mi.

vp9_dec_setup_mi does:

vpx_memset(cm->mip, 0, cm->mi_stride * (cm->mi_rows + 1) * sizeof(*cm->mip));

where *cm->mip is a structure that's larger than 64 bytes long, so signed overflow can happen.

Some other things about the code also look a little iffy in general - for example, vpx_calloc also does an unchecked multiplication.

This specific bug would probably be quite difficult to exploit (not that we haven't seen tricks with negative copies :-))

### cl...@chromium.org (2015-01-26)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-01-27)

Erring on the side of caution and marking this one high, though I have not looked deeply into how reasonable it is to exploit this.

### cl...@chromium.org (2015-02-05)

johannkoenig@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

johannkoenig@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-24)

johannkoenig: Wondering if you had a chance to take a look at this so far? Thanks!

### cl...@chromium.org (2015-03-03)

ClusterFuzz has detected this issue as fixed in range 318771:318772.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5162675410567168

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  vp9_dec_setup_mi
  vp9_init_context_buffers
  resize_context_buffers
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=296165:296530
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=318771:318772

Minimized Testcase (1.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94etmm4xm-bp43EUEhJHBLFDSoYztjDvoF8FGNIwK8_JkxGuK-VpjxUAilsX4t23iOD-TDQ8gFVtwcYGiPIK94_chHx0rOZHPNGbeehhcm_wlimPcsw4Eqy8C9tG5ndPjher3PtXGYe5jnTbs0JyFbWIzyu9g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-03)

ClusterFuzz has detected this issue as fixed in range 318771:318772.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5162675410567168

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  vp9_dec_setup_mi
  vp9_init_context_buffers
  resize_context_buffers
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=296165:296530
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=318771:318772

Minimized Testcase (1.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94etmm4xm-bp43EUEhJHBLFDSoYztjDvoF8FGNIwK8_JkxGuK-VpjxUAilsX4t23iOD-TDQ8gFVtwcYGiPIK94_chHx0rOZHPNGbeehhcm_wlimPcsw4Eqy8C9tG5ndPjher3PtXGYe5jnTbs0JyFbWIzyu9g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-03-10)

johannkoenig@: Uh oh! This issue is still open and hasn't been updated in the last 47 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-24)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-21)

johannkoenig: This still seems to be reproducing, and we're past the deadline we try to hold ourselves to for externally reported vulnerabilities. Could you please take a look or help us by suggesting another owner?

### mb...@chromium.org (2015-04-27)

tomfinegan: Any idea who the right owner for this would be? We've gone for a pretty long time without any progress here.

### to...@chromium.org (2015-04-27)

Shouldn't this be closed per #13? Or is #15 the one we should look at? clusterfuzz@ is being a little confusing in this bug.

Anyway, +yaowu for reassignment/verification.

### ya...@chromium.org (2015-04-27)

The issue appeared to have been fixed as of #13. 

### mb...@chromium.org (2015-04-27)

Reopening since this has still be reproducing as recently as yesterday. The fixed reports on this bug were incorrect.

### ya...@chromium.org (2015-04-27)

we should have built libvpx with --size-limit=WxH  where W and H set at a reasonable size such as 16384x16384. 

This would prevent the overflow issue.

### mb...@chromium.org (2015-04-27)

Seems like that would be a big win from the security side. Are you the right owner to set this up?

### jo...@chromium.org (2015-04-27)

Not sure why this didn't get an update when I submitted the issue:
https://codereview.chromium.org/1106303002/

libvpx is in DEPS so there is still another step to get this merged. Will update when it's in.

### mb...@chromium.org (2015-04-27)

Awesome, thanks! Any idea if this will also take care of https://crbug.com/chromium/462300?

### jo...@chromium.org (2015-04-27)

Unlikely? Similar to 449591 I have had a lot of trouble reproducing that.

### bu...@chromium.org (2015-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89a36094df177a7fb50cfab571409b7bf91202a2

commit 89a36094df177a7fb50cfab571409b7bf91202a2
Author: johannkoenig <johannkoenig@google.com>
Date: Tue Apr 28 23:50:43 2015

Roll libvpx c600ca:471ce8

Restrict vp9 decoder to 16384x16384
https://codereview.chromium.org/1106303002
BUG=450939

Fix arm/LTO build
https://codereview.chromium.org/1085023004

Hopefully fix AVX2 detection once and for all
https://codereview.chromium.org/1104213004
BUG=480586

R=tomfinegan@chromium.org

Review URL: https://codereview.chromium.org/1115503002

Cr-Commit-Position: refs/heads/master@{#327392}

[modify] http://crrev.com/89a36094df177a7fb50cfab571409b7bf91202a2/DEPS


### cl...@chromium.org (2015-04-29)

ClusterFuzz has detected this issue as fixed in range 327364:327408.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5162675410567168

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  vp9_dec_setup_mi
  vp9_init_context_buffers
  resize_context_buffers
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=296165:296530
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=327364:327408

Minimized Testcase (1.23 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94etmm4xm-bp43EUEhJHBLFDSoYztjDvoF8FGNIwK8_JkxGuK-VpjxUAilsX4t23iOD-TDQ8gFVtwcYGiPIK94_chHx0rOZHPNGbeehhcm_wlimPcsw4Eqy8C9tG5ndPjher3PtXGYe5jnTbs0JyFbWIzyu9g

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-04-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### jo...@chromium.org (2015-05-04)

Merge requested for M43:
https://chromereviews.googleplex.com/184557014

This cherry picks this change:
https://codereview.chromium.org/1106303002
on top of the version of libvpx in M43:
https://codereview.chromium.org/1124723002/

See the branch here:
https://chromium.googlesource.com/chromium/deps/libvpx/+/m43-2357
with the current change and the parent change, which are the same as the versions in the roll request.

This change forces the decoder to reject any input stream purporting to be greater than 16384x16384. This fixes this particular issues (poor handling of a malformed stream, which purports itself to be larger than that size) and gives the decoder the same size restriction that vp8 has. Given that we are just getting smooth playback for 4k video (anywhere from 3840x2160 to 5120x3200 depending on what marketing you're looking at) it will be some time before we reach the 16kx16k limit.

### la...@google.com (2015-05-04)

Approved for M43 (branch: 2357)

### bu...@chromium.org (2015-05-04)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=72954

------------------------------------------------------------------
r72954 | johannkoenig@google.com | 2015-05-04T17:35:17.143025Z

-----------------------------------------------------------------

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

Updating severity - closer to medium than high.

### ti...@google.com (2015-05-28)

As mentioned in the release notes - $1000 for this report. Congrats!

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-06)

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

This issue was migrated from crbug.com/chromium/450939?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081236)*
