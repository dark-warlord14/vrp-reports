# renderer crash when playing a corrupt webm video

| Field | Value |
|-------|-------|
| **Issue ID** | [40086189](https://issues.chromium.org/issues/40086189) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Media |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached webm video causes a renderer crash in Chrome. The crash happens at memcpy() in Linux. Crash addresses are pretty high and move with the stack pointer when reloading the page.

I'll try to minimize the triggering video and have a look at what is the cause of the bug later. Before that, is this the right place to report media-related possible security issues in Chrome, or should they be filed upstream to ffmpeg or elsewhere?

In other players:  

MPlayer 1.0rc4-4.4.5 (C) 2000-2010 MPlayer Team -> no crash  

VLC version 1.1.4 The Luggage (exported) -> segmentation fault also in memcpy with last words:  

[...]  

Failed to decode frame: Corrupt frame detected  

Additional information: Truncated packet or corrupt partition 0 length  

Failed to decode frame: Bitstream not supported by this decoder  

Additional information: Invalid frame sync code

**VERSION**  

Chrome Version: 9.0.597.19 (Official Build 68937) beta  

Operating System: Ubuntu 10.10, x86\_64

**REPRODUCTION CASE**  

$ google-chrome memcpy.webm

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe816b700 (LWP 29521)]  

memcpy () at ../sysdeps/x86\_64/memcpy.S:191  

191 ../sysdeps/x86\_64/memcpy.S: No such file or directory.  

in ../sysdeps/x86\_64/memcpy.S  

(gdb) bt 8  

#0 memcpy () at ../sysdeps/x86\_64/memcpy.S:191  

#1 0x00007ffff61a6895 in media::CopyPlane (plane=<value optimized out>,  

video\_frame=<value optimized out>, frame=<value optimized out>)  

at /usr/include/bits/string3.h:52  

#2 0x00007ffff61a79c5 in media::FFmpegVideoDecodeEngine::DecodeFrame (  

this=0x7ffff874bf00, buffer=<value optimized out>)  

at media/video/ffmpeg\_video\_decode\_engine.cc:283  

#3 0x00007ffff61a7e15 in media::FFmpegVideoDecodeEngine::ConsumeVideoSample (  

this=0x7ffff874bf00, buffer=<value optimized out>)  

at media/video/ffmpeg\_video\_decode\_engine.cc:162  

#4 0x00007ffff61a1464 in media::FFmpegVideoDecoder::OnReadCompleteTask (  

this=<value optimized out>, buffer=<value optimized out>)  

at media/filters/ffmpeg\_video\_decoder.cc:287  

#5 0x00007ffff61a16ee in DispatchToMethod<media::FFmpegVideoDecoder, void (media::FFmpegVideoDecoder::\*)(scoped\_refptr[media::Buffer](javascript:void(0);)), scoped\_refptr[media::Buffer](javascript:void(0);) > (this=<value optimized out>) at ./base/tuple.h:554  

#6 RunnableMethod<media::FFmpegVideoDecoder, void (media::FFmpegVideoDecoder::\*)(scoped\_refptr[media::Buffer](javascript:void(0);)), Tuple1<scoped\_refptr[media::Buffer](javascript:void(0);) > >::Run (  

this=<value optimized out>) at ./base/task.h:330  

#7 0x00007ffff5aec091 in MessageLoop::RunTask (this=0x7fffe816aaa0,  

task=0x7ffff8b5fab0) at base/message\_loop.cc:410  

(More stack frames follow...)  

(gdb) disas $rip-22, $rip+16  

Dump of assembler code from 0x7fffeef3eb4c to 0x7fffeef3eb72:  

0x00007fffeef3eb4c <memcpy+188>: nop  

0x00007fffeef3eb4d <memcpy+189>: nop  

0x00007fffeef3eb4e <memcpy+190>: nop  

0x00007fffeef3eb4f <memcpy+191>: nop  

0x00007fffeef3eb50 <memcpy+192>: cmp $0x400,%rdx  

0x00007fffeef3eb57 <memcpy+199>: ja 0x7fffeef3ebd0 <memcpy+320>  

0x00007fffeef3eb59 <memcpy+201>: mov %edx,%ecx  

0x00007fffeef3eb5b <memcpy+203>: shr $0x5,%ecx  

0x00007fffeef3eb5e <memcpy+206>: je 0x7fffeef3ebc0 <memcpy+304>  

0x00007fffeef3eb60 <memcpy+208>: dec %ecx  

=> 0x00007fffeef3eb62 <memcpy+210>: mov (%rsi),%rax  

0x00007fffeef3eb65 <memcpy+213>: mov 0x8(%rsi),%r8  

0x00007fffeef3eb69 <memcpy+217>: mov 0x10(%rsi),%r9  

0x00007fffeef3eb6d <memcpy+221>: mov 0x18(%rsi),%r10  

0x00007fffeef3eb71 <memcpy+225>: mov %rax,(%rdi)  

End of assembler dump.  

(gdb) info registers  

rax 0x0 0  

rbx 0x7ffff9314d00 140737374145792  

rcx 0xb 11  

rdx 0x280 640  

rsi 0x7ffffaaed000 140737399148544  

rdi 0x7ffff9314b80 140737374145408  

rbp 0x7ffffaaecf00 0x7ffffaaecf00  

rsp 0x7fffe816a588 0x7fffe816a588  

r8 0x0 0  

r9 0x0 0  

r10 0x0 0  

r11 0x1 1  

r12 0x10b2 4274  

r13 0x1168 4456  

r14 0x280 640  

r15 0x280 640  

rip 0x7fffeef3eb62 0x7fffeef3eb62 <memcpy+210>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

## Attachments

- [memcpy.webm](attachments/memcpy.webm) (application/octet-stream; charset=binary, 616.0 KB)
- [memcpy.webm](attachments/memcpy_52888101.webm) (application/octet-stream; charset=binary, 616.0 KB)
- [uninitialize.webm](attachments/uninitialize.webm) (application/octet-stream; charset=binary, 616.0 KB)

## Timeline

### ao...@gmail.com (2010-12-17)

Narrowed required changes to:
 $ curl http://people.opera.com/shwetankd/webm/sunflower.webm \
   | base64 \
   | sed -e 's/aWSJODgQGIgQCGhVZfVlA4I+ODhAJiWgBTboVWaWRlb+CSsIICgLqCA/YWSJODgQGIgQCGhVZfVlA4I+ODhAJiWgBTboVWaWRlb+CSsIICgLqCE/' \
   | base64 -d > memcpy.webm

There seems to be some nondeterminism. In addition to the usual crash place I got a few "Dec 17 18:42:49 ni kernel: [37351.078588] chrome[2708]: segfault at ffffffff ip 00000000ffffffff sp 00007fffc2135558 error 14 in libnssckbi.so[7f981f89a000+6a000]", and sometimes the player shows garbage without crashing.

### sc...@gmail.com (2010-12-17)

[Empty comment from Monorail migration]

### ao...@gmail.com (2010-12-17)

I was going to have a look at the cause, but got another crash and minimized it instead. Its minimal mutation ended up looking so much like this one that this might be just a different manifestation of the same bug.

To reproduce, use the same instructions but with sed -e 's/CSsIICgLqCAWhUsIICgFS6ggFo/CSsIICgLqDAWhUsIICgFS6ggFo/'.

This causes here:
Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fffe816b700 (LWP 18513)]
media::FFmpegVideoDecodeEngine::Uninitialize (this=<value optimized out>)
    at media/video/ffmpeg_video_decode_engine.cc:303
303     media/video/ffmpeg_video_decode_engine.cc: No such file or directory.
        in media/video/ffmpeg_video_decode_engine.cc
(gdb) bt 5
#0  media::FFmpegVideoDecodeEngine::Uninitialize (this=<value optimized out>)
    at media/video/ffmpeg_video_decode_engine.cc:303
#1  0x002df6378c6662c4 in ?? ()
#2  0x00007ffff5b0e957 in ~Lock (this=0x7fffe816aaa0, 
    max_time=<value optimized out>) at ./base/lock.h:19
#3  ~SyncWaiter (this=0x7fffe816aaa0, max_time=<value optimized out>)
    at base/waitable_event_posix.cc:82
#4  base::WaitableEvent::TimedWait (this=0x7fffe816aaa0, 
    max_time=<value optimized out>) at base/waitable_event_posix.cc:204
(More stack frames follow...)

where frame #1 is clearly in trouble. During minimization sometimes the crash came after returning to the broken frame and getting a bogus rip, though I think this only happened while tracing with GDB.

### sc...@gmail.com (2010-12-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-22)

There seem to be at least two different types of crash: one in memcpy() from the memcpy.webm and memcpy2.webm sample files, and the other a possible NULL crash with uninitialize.webm.

I'll add my debugging notes here so that someone has a good start. It appears that the memcpy-related videos have a large canvas size in the container -- e.g. 640x4000. However, the VP8 header overrides the excessive height with a more sensible one such as 300 or so.
Unfortunately, the VideoFrame object in FFmpegVideoDecodeEngine::DecodeFrame() comes out at 640x4000, but the AVFrame object only has a size of 640x300. This leads to a crash in CopyPlane() due to trying to copy 4000 lines where only 300 are available.
I'm also very worried about the inverse case where the container might declare itself to be small, but the VP8 header declares a larger canvas. Might this cause a really serious buffer overflow??

This feels like a regression -- I could be on drugs, but I swear we used to handle these cases where there was a mismatch between container size and codec frame sizes. (And, can't a video change size half-way through)?

### sc...@gmail.com (2010-12-22)

[Empty comment from Monorail migration]

### fb...@chromium.org (2010-12-22)

using vp8 v0.9.5-107-g6cb708d (dec 21, 2010)
This reproduces the crash
ffmpeg -i memcpy.webm bob.yuv
but this does not
vpxdec memcpy.webm -o bob.yuv
and it decodes ok
media_bench --stream=video bob.webm
* Stream #0: libvpx (libvpx VP8)

     Frames:        210
      Total:     323.30 ms
  Summation:     321.75 ms
    Average:       1.53 ms
     StdDev:       0.53 ms
        FPS:     652.68

ffmpeg says
[libvpx @ 01fc8bc0] dimension change! 640x4456 -> 640x360
Stream #0.0(eng): Video: vp8, yuv420p, 640x4456, PAR 99:8 DAR 990:557, 1k fps, 25 tbr, 1k tbn, 1k tbc
Weird aspect ratio.
I dont think its a regression.


### sc...@chromium.org (2010-12-22)

updating labels -- fairly certain it's not a regression

### sc...@chromium.org (2010-12-22)

[Empty comment from Monorail migration]

### sc...@chromium.org (2010-12-23)

Looks like we have a DCHECK that should catch this :\

Working on a fix

### sc...@chromium.org (2010-12-23)

Fixes for memcpy and uninitialize crashes:
http://codereview.chromium.org/6034007/
http://codereview.chromium.org/6046006/



### bu...@chromium.org (2010-12-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70077

------------------------------------------------------------------------
r70077 | scherkus@chromium.org | Thu Dec 23 11:11:19 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70077&r2=70076&pathrev=70077
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.cc?r1=70077&r2=70076&pathrev=70077
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.h?r1=70077&r2=70076&pathrev=70077

Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006
------------------------------------------------------------------------

### bu...@chromium.org (2010-12-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70092

------------------------------------------------------------------------
r70092 | skerner@chromium.org | Thu Dec 23 12:52:52 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70092&r2=70091&pathrev=70092
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.cc?r1=70092&r2=70091&pathrev=70092
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.h?r1=70092&r2=70091&pathrev=70092

Revert 70077 - Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/5970011
------------------------------------------------------------------------

### sc...@gmail.com (2010-12-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-29)

[Empty comment from Monorail migration]

### sc...@chromium.org (2011-01-06)

Updates!

70077 was mistakenly reverted and then never un-reverted.  Turned out it was due to something else.

I'm going to re-land it right now + do the merge dance.

### bu...@chromium.org (2011-01-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70669

------------------------------------------------------------------------
r70669 | scherkus@chromium.org | Thu Jan 06 14:26:57 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70669&r2=70668&pathrev=70669
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.cc?r1=70669&r2=70668&pathrev=70669
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_video_decoder.h?r1=70669&r2=70668&pathrev=70669

Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

This was originally commited as r70077 but was accidentally reverted.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006
------------------------------------------------------------------------

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70703

------------------------------------------------------------------------
r70703 | scherkus@chromium.org | Thu Jan 06 18:08:11 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/video/ffmpeg_video_decode_engine_unittest.cc?r1=70703&r2=70702&pathrev=70703
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/video/ffmpeg_video_decode_engine.cc?r1=70703&r2=70702&pathrev=70703

Handle changes in video frame size.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6034007
------------------------------------------------------------------------

### sc...@chromium.org (2011-01-07)

Assigning to cevans for merging r70669 and r70703 into 552, 552d, and 597.

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70789

------------------------------------------------------------------------
r70789 | cevans@chromium.org | Fri Jan 07 14:14:30 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/filters/ffmpeg_video_decoder.cc?r1=70789&r2=70788&pathrev=70789
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70789&r2=70788&pathrev=70789
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/filters/ffmpeg_video_decoder.h?r1=70789&r2=70788&pathrev=70789

Merge 70669 - Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

This was originally commited as r70077 but was accidentally reverted.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6161002
------------------------------------------------------------------------

### sc...@gmail.com (2011-01-07)

552: r70789 and r70790
552d: r70792 and r70793

I'll take care of 597 when it re-opens.

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70790

------------------------------------------------------------------------
r70790 | cevans@chromium.org | Fri Jan 07 14:15:10 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/video/ffmpeg_video_decode_engine.cc?r1=70790&r2=70789&pathrev=70790
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/video/ffmpeg_video_decode_engine_unittest.cc?r1=70790&r2=70789&pathrev=70790

Merge 70703 - Handle changes in video frame size.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6034007

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6194002
------------------------------------------------------------------------

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70793

------------------------------------------------------------------------
r70793 | cevans@chromium.org | Fri Jan 07 14:17:52 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/media/video/ffmpeg_video_decode_engine.cc?r1=70793&r2=70792&pathrev=70793
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/media/video/ffmpeg_video_decode_engine_unittest.cc?r1=70793&r2=70792&pathrev=70793

Merge 70703 - Handle changes in video frame size.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6034007

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6104007
------------------------------------------------------------------------

### bu...@chromium.org (2011-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70792

------------------------------------------------------------------------
r70792 | cevans@chromium.org | Fri Jan 07 14:16:47 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/media/filters/ffmpeg_video_decoder.cc?r1=70792&r2=70791&pathrev=70792
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70792&r2=70791&pathrev=70792
 M http://src.chromium.org/viewvc/chrome/branches/552d/src/media/filters/ffmpeg_video_decoder.h?r1=70792&r2=70791&pathrev=70792

Merge 70669 - Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

This was originally commited as r70077 but was accidentally reverted.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6198001
------------------------------------------------------------------------

### sc...@gmail.com (2011-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-07)

Marking severity as high; I don't see why the frame size might cause a buffer overflow by getting larger. (Aki's initial test case causes an OOB read due to a shrinking frame size).

### sc...@gmail.com (2011-01-07)

@aohelin: congratulations! We're provisionally rewarding this bug at the $1000 level, thanks to the interesting condition, good reliable repro and code / stack / register analysis.

Additional credit for independent discovery to David Warren of CERT and SkyLined.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-01-08)

Merged to m9 (r70816, r70818).
All merges done.

### bu...@chromium.org (2011-01-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70818

------------------------------------------------------------------------
r70818 | cevans@chromium.org | Fri Jan 07 16:56:37 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/597/src/media/video/ffmpeg_video_decode_engine.cc?r1=70818&r2=70817&pathrev=70818
 M http://src.chromium.org/viewvc/chrome/branches/597/src/media/video/ffmpeg_video_decode_engine_unittest.cc?r1=70818&r2=70817&pathrev=70818

Merge 70703 - Handle changes in video frame size.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6034007

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6156002
------------------------------------------------------------------------

### bu...@chromium.org (2011-01-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=70816

------------------------------------------------------------------------
r70816 | cevans@chromium.org | Fri Jan 07 16:55:03 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/597/src/media/filters/ffmpeg_video_decoder.cc?r1=70816&r2=70815&pathrev=70816
 M http://src.chromium.org/viewvc/chrome/branches/597/src/media/filters/ffmpeg_video_decoder_unittest.cc?r1=70816&r2=70815&pathrev=70816
 M http://src.chromium.org/viewvc/chrome/branches/597/src/media/filters/ffmpeg_video_decoder.h?r1=70816&r2=70815&pathrev=70816

Merge 70669 - Don't uninitialize FFmpegVideoDecodeEngine if we haven't initialized it.

This was originally commited as r70077 but was accidentally reverted.

BUG=67303
TEST=media_unittests

Review URL: http://codereview.chromium.org/6046006

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/6206001
------------------------------------------------------------------------

### ao...@gmail.com (2011-01-08)

@scarybeasts: Most excellent :) This one is going to Red Cross.

@dwarren@cert.org: Have you had a look if other programs have issues with frame resizing? At least VLC had this problem earlier.

### [Deleted User] (2011-01-12)

Works fine with Google Chrome 8.0.552.237 (Official Build 70801) on Windows and Linux.

### sc...@gmail.com (2011-01-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-13)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-01-19)

Current stable VLC still crashes on the original repro. I'm not sure if CERT has already done this, so will add a bug to their tracker.

### sc...@gmail.com (2011-01-24)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-01-27)

This should be fixed in VLC in 1.1.6. Ubuntu is currently at 1.1.4.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/67303?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Media]
[Monorail mergedwith: crbug.com/chromium/68070]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086189)*
