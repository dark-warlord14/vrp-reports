# Global-buffer-overflow in render_line

| Field | Value |
|-------|-------|
| **Issue ID** | [40052347](https://issues.chromium.org/issues/40052347) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Media |
| **Reporter** | ao...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2011-12-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a global buffer overflow when the attached video is played. It also crashes renderer in current stable version.

**VERSION**  

Chrome Version: 16.0.912.63 and 18.0.979.0  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

$ chrome bof.webm  

$ $ dmesg | grep chrome | tail -n 1  

[11848.789410] chrome[4712]: segfault at 7f8444e6ad10 ip 00007f8444db3d07 sp 00007f8441174358 error 4 in libffmpegsumo.so[7f8444c4b000+21f000]

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==10160== ERROR: AddressSanitizer global-buffer-overflow on address 0x7f40104b1410 at pc 0x7f401034c008 bp 0x7f400c185b00 sp 0x7f400c185af8  

READ of size 4 at 0x7f40104b1410 thread T5  

#0 0x7f401034c008 in render\_line third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:0  

0x7f40104b1410 is located 7 bytes to the right of global variable '.str4 (third\_party/ffmpeg/patched-ffmpeg/libavutil/parseutils.c)' (0x7f40104b13e0) of size 41  

'.str4 (third\_party/ffmpeg/patched-ffmpeg/libavutil/parseutils.c)' is ascii string 'Invalid 0xRRGGBB[AA] color string: '%s'  

'  

==10160== ABORTING  

Stats: 9M malloced (11M for red zones) by 23546 calls  

Stats: 0M realloced by 217 calls  

Stats: 5M freed by 14213 calls  

Stats: 0M really freed by 0 calls  

Stats: 56M (14345 full pages) mmaped in 14 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 19:8; 20:4;  

mallocs by size class: 8:19796; 9:1608; 10:1065; 11:421; 12:182; 13:342; 14:80; 15:14; 16:15; 17:11; 18:5; 19:4; 20:3;  

frees by size class: 8:11529; 9:1041; 10:884; 11:274; 12:108; 13:301; 14:50; 15:8; 16:7; 17:4; 18:3; 19:3; 20:1;  

rfrees by size class:  

Stats: malloc large: 23 small slow: 141  

Shadow byte and word:  

0x1fe802096282: f9  

0x1fe802096280: 00 01 f9 f9 f9 f9 f9 f9  

More shadow bytes:  

0x1fe802096260: f9 f9 f9 f9 07 f9 f9 f9  

0x1fe802096268: f9 f9 f9 f9 00 01 f9 f9  

0x1fe802096270: f9 f9 f9 f9 00 00 07 f9  

0x1fe802096278: f9 f9 f9 f9 00 00 00 00  

=>0x1fe802096280: 00 01 f9 f9 f9 f9 f9 f9  

0x1fe802096288: 00 00 00 f9 f9 f9 f9 f9  

0x1fe802096290: 00 00 00 00 00 04 f9 f9  

0x1fe802096298: f9 f9 f9 f9 00 01 f9 f9  

0x1fe8020962a0: f9 f9 f9 f9 07 f9 f9 f9

## Attachments

- [bof.webm](attachments/bof.webm) (application/octet-stream; charset=binary, 1.0 MB)
- [patch.txt](attachments/patch.txt) (text/x-diff; charset=us-ascii, 407 B)
- [0001-vorbis-fix-overflows-in-floor1-vector-and-inverse-db.patch](attachments/0001-vorbis-fix-overflows-in-floor1-vector-and-inverse-db.patch) (text/x-c; charset=us-ascii, 3.5 KB)

## Timeline

### in...@chromium.org (2011-12-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9299191

Uploader: inferno@chromium.org

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x7f8b4bc0b470
Crash State:
  - crash stack -
  render_line
  

Minimized Testcase (1024.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97ic6h_hln-ctcvggnBc5NlEGiz2d55OMe-dZS2fQM3_DtfTZC9UPpb-0pM_7e1-3S7ksKxjVi02pJcJG-bGMoo0j8vPPJMqveynloBueOo97k85xvANWoW3kw9-QZapPkNRNA9jJnxaZwAQ1QY2KIRjQxjbg

### in...@chromium.org (2011-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-22)

[Empty comment from Monorail migration]

### fi...@chromium.org (2011-12-22)

Sample crash from 17.0.963.12: http://crash/reportdetail?reportid=5daa40d1546d11a0

Backtrace from ToT debug build from gdb:

#0  render_line (x0=39, y0=54868, x1=46, y1=<optimized out>, buf=0x7f70d3bbb200) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:182
#1  0x00007f70d46acf52 in ff_vorbis_floor1_render_list (list=<optimized out>, values=<optimized out>, y_list=<optimized out>, flag=0x7f70d1083520, multiplier=<optimized out>, out=<optimized out>, 
    samples=1024) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:216
#2  0x00007f70d46afff6 in vorbis_floor1_decode (vc=<optimized out>, vfu=<optimized out>, vec=<optimized out>) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1259
#3  0x00007f70d46ad517 in vorbis_parse_audio_packet (vc=<optimized out>) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1520
#4  vorbis_decode_frame (avccontext=<optimized out>, data=<optimized out>, data_size=<optimized out>, avpkt=<optimized out>) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1641
#5  0x00007f70d46aa896 in avcodec_decode_audio3 (avctx=0x7f70d3b2ba00, samples=0xd654, frame_size_ptr=0x2e, avpkt=0x2694) at ../../third_party/ffmpeg/patched-ffmpeg/libavcodec/utils.c:822
#6  0x00007f70dfc1ba51 in media::FFmpegAudioDecoder::DoDecodeBuffer (this=0x7f70d3b5a800, input=...) at ../../media/filters/ffmpeg_audio_decoder.cc:197
#7  0x00007f70dfc1d414 in base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(scoped_refptr<media::Buffer> const&)>::Run (this=0x7f70d10851d0, object=0x7f70d3b5a800, a1=...)
    at ../../base/bind_internal.h:189
#8  0x00007f70dfc1d243 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(scoped_refptr<media::Buffer> const&)>, void (media::FFmpegAudioDecoder* const&, media::Buffer*)>::MakeItSo(base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(scoped_refptr<media::Buffer> const&)>, media::FFmpegAudioDecoder* const&, media::Buffer*) (runnable=..., a1=@0x7f70cd716c60, a2=0x7f70cf6bdae0) at ../../base/bind_internal.h:876
#9  0x00007f70dfc1d07a in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(scoped_refptr<media::Buffer> const&)>, void (media::FFmpegAudioDecoder*, scoped_refptr<media::Buffer> const&), void (media::FFmpegAudioDecoder*, scoped_refptr<media::Buffer>)>, void (media::FFmpegAudioDecoder*, scoped_refptr<media::Buffer> const&)>::Run(base::internal::BindStateBase*) (base=0x7f70cd716c40) at ../../base/bind_internal.h:1214
#10 0x00007f70e3b808fb in base::Callback<void ()>::Run() const (this=0x7f70d1085578) at ../../base/callback.h:276
#11 0x00007f70e3bbc8db in MessageLoop::RunTask (this=0x7f70d1085ba0, pending_task=...) at ../../base/message_loop.cc:491
#12 0x00007f70e3bbc9f5 in MessageLoop::DeferOrRunPendingTask (this=0x7f70d1085ba0, pending_task=...) at ../../base/message_loop.cc:503
#13 0x00007f70e3bbd217 in MessageLoop::DoWork (this=0x7f70d1085ba0) at ../../base/message_loop.cc:693
#14 0x00007f70e3bc5738 in base::MessagePumpDefault::Run (this=0x7f70d3b668d0, delegate=0x7f70d1085ba0) at ../../base/message_pump_default.cc:28
#15 0x00007f70e3bbc533 in MessageLoop::RunInternal (this=0x7f70d1085ba0) at ../../base/message_loop.cc:450
#16 0x00007f70e3bbc3e6 in MessageLoop::RunHandler (this=0x7f70d1085ba0) at ../../base/message_loop.cc:423
#17 0x00007f70e3bbbd1b in MessageLoop::Run (this=0x7f70d1085ba0) at ../../base/message_loop.cc:333
#18 0x00007f70e3c1752e in base::Thread::Run (this=0x7f70d3b64a40, message_loop=0x7f70d1085ba0) at ../../base/threading/thread.cc:126
#19 0x00007f70e3c176ae in base::Thread::ThreadMain (this=0x7f70d3b64a40) at ../../base/threading/thread.cc:161
#20 0x00007f70e3c119fb in base::(anonymous namespace)::ThreadFunc (params=0x7f70d3b81cc0) at ../../base/threading/platform_thread_posix.cc:60
#21 0x00007f70db5229ca in start_thread (arg=<optimized out>) at pthread_create.c:300
#22 0x00007f70d8fb170d in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:112
#23 0x0000000000000000 in ?? ()

The crash is at this line:
182         buf[x0] = ff_vorbis_floor1_inverse_db_table[y0];
where x0==39, y0==54868, and the RHS is failing the read because ff_vorbis_floor1_inverse_db_table is a float[256].
That y0=54868=0xd654 is also the value of |samples| passed to #5 (avcodec_decode_audio3) according to the backtrace, although frame #6 believes it passed a valid pointer in for the second param:
(gdb) down
#6  0x00007f70dfc1ba51 in media::FFmpegAudioDecoder::DoDecodeBuffer (this=0x7f70d3b5a800, input=...) at ../../media/filters/ffmpeg_audio_decoder.cc:197
197           &decoded_audio_size, &packet);
(gdb) p decoded_audio_
$23 = (uint8 *) 0x7f70d3b88000 ""

Ronald: ideas?

### in...@chromium.org (2012-01-06)

We have a stable patch in two weeks, can you please try to fix it before that ?

### rb...@google.com (2012-01-07)

This fixes it for me, and doesn't break normal vorbis file playback.

If the patch is OK with chrome-media folks, I can submit a full patch that includes all the patch/deps/stuff, but I don't have deps checked out on this computer.

### fi...@chromium.org (2012-01-07)

#6 patch looks fine for hiding the problem, but isn't the real problem that the stack is being corrupted somewhere (see my https://crbug.com/chromium/108416#c4)?  At the very least, isn't it a problem that y0 is being set to such a large value?

### sc...@gmail.com (2012-01-07)

FWIW, there was another instance of this that I fixed in a very similar manner. I agree it would be nice to understand how this value gets so big but am supportive of applying this bandaid to limit the security impact.

### rb...@google.com (2012-01-09)

I don't think it's memory corruption, seems like an unsigned integer overflow in generating floor1_Y_final (uint16_t):

Adapted[2]: 75 +/- 65444 <--- this one
Predicted[3]: 16260
Predicted[4]: 45906
Adapted[5]: 4297 +/- -6
Adapted[6]: 32445 +/- -11
Adapted[7]: 58982 +/- -4
Adapted[8]: 19333 +/- -21
Adapted[9]: 9923 +/- -3
Predicted[10]: 23292
Predicted[11]: 45808
Predicted[12]: 62917
Adapted[13]: 53778 +/- -2
Adapted[14]: 32961 +/- 3
Predicted[15]: 2183
Adapted[16]: 7105 +/- 3
Adapted[17]: 12737 +/- 3
Predicted[18]: 19776
Predicted[19]: 27511
Predicted[20]: 38769
Predicted[21]: 55663
Predicted[22]: 64254
Adapted[23]: 60948 +/- -2
Predicted[24]: 56588
Adapted[25]: 50123 +/- -5
Predicted[26]: 39435
Adapted[27]: 26350 +/- -8
Adapted[28]: 12290 +/- 7
Inputs: 75 70 65519 16260 45906 4291 32434 58978 19312 9920 23292 45808 62917 53776 32964 2183 7108 12740 19776 27511 38769 55663 64254 60946 56588 50118 39435 26342 12297

65519 is also known as the signed number -17. I suppose the number should be clipped or so to prevent it from going out of range (I don't think negative numbers make sense). I'll have to ask the vorbis experts to know for sure.

### rb...@google.com (2012-01-10)

I had a chat with the xiph/vorbis people and our libav/ffmpeg vorbis expert, and it is preferred if we clamp (rather than wrap) inverse db table values in the 8bit [0,255] range. They wrap the floor1[] vector to 15bits [0,0x7fff], but they're now looking into whether clamping would be better. (It probably doesn't matter much in practice, because it should never go negative; it's purely theoretical.) Once we've figured that out, I'll submit a patch that should fix all of this once and for all.

I also found another 2 problems with a test set of zuf'ed files from mozilla (kindly provided by Tim Terriberry):
http://bugzilla.libav.org/show_bug.cgi?id=198
http://bugzilla.libav.org/show_bug.cgi?id=199
I'll see if they cause issues and submit fixes for them also.

### rb...@google.com (2012-01-10)

This patch is what the vorbis developers suggest and fixes this file, plus the floor1[] overflows, for me (in asan). Ami, OK? Note that I remove the uint8_t casts for the inverse db and replace them by a clamp, Chris please object if you're not OK with that.

I'll add a deps patch if the idea of the patch is OK.

### fi...@chromium.org (2012-01-10)

#11: LGTM.

### in...@chromium.org (2012-01-20)

@rbultje - can you please get the fischman@ reviewed patch landed :):)

### rb...@google.com (2012-01-22)

I don't have commit access, someone else needs to actually commit it for me, I think?

(Also I'm on vacation this week.)

### in...@chromium.org (2012-01-23)

Ami, can you please help to commit Ronald's patch. We will merge it to the necessary branches later.

### fi...@chromium.org (2012-01-23)

Ronald: you don't need to be a committer to push the commit-queue checkbox on rietveld, as long as a committer (and OWNER, as appropriate) has LGTM'd your change.  I've checked the box for you now.

inferno: do you want to also roll chromium DEPS for it when it lands?

### bu...@chromium.org (2012-01-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=118716

------------------------------------------------------------------------
r118716 | rbultje@chromium.org | Mon Jan 23 11:51:09 PST 2012

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/52_vorbis_fix_floor1_vector_int_overflow.patch?r1=118716&r2=118715&pathrev=118716
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vorbis.c?r1=118716&r2=118715&pathrev=118716
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vorbisdec.c?r1=118716&r2=118715&pathrev=118716
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=118716&r2=118715&pathrev=118716
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=118716&r2=118715&pathrev=118716

Fix vorbis floor1[] vector integer overflow and subsequent overflows in
the inverse db lookup table, causing stack overreads.

BUG=108416

Review URL: http://codereview.chromium.org/9169023
------------------------------------------------------------------------

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### fi...@chromium.org (2012-01-23)

Dale: the ffmpeg DEPS roll is in the CQ (http://codereview.chromium.org/9200020/)
Once it lands you're good to go to create windows binaries for HEAD.
Once that all works, please drover Ronald's fix CL (118716), the DEPS roll (currently in CQ) and your new win binaries into branch 963.

### sc...@gmail.com (2012-01-23)

@dalecurtis / @fischman: I don't know how much hassle Windows binaries are, but we've definitely got more ffmpeg fixes on the way. Maybe they could be batched into one Windows binary update?

Or perhaps not, if the merge deadline for M17 is very close?

### bu...@chromium.org (2012-01-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=118751

------------------------------------------------------------------------
r118751 | fischman@chromium.org | Mon Jan 23 14:45:22 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=118751&r2=118750&pathrev=118751

Roll ffmpeg 117977:118716

TBR=scherkus
BUG=108416
TEST=none


Review URL: http://codereview.chromium.org/9200020
------------------------------------------------------------------------

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-01-24)

Reassigning to scherkus as we need this by 7pm tonight and my ticket for Windows access is sadly not moving.



### bu...@chromium.org (2012-01-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=118948

------------------------------------------------------------------------
r118948 | scherkus@chromium.org | Tue Jan 24 16:05:05 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avformat-53.dll?r1=118948&r2=118947&pathrev=118948
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avcodec-53.dll?r1=118948&r2=118947&pathrev=118948
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avutil-51.dll?r1=118948&r2=118947&pathrev=118948

Windows Chromium FFmpeg binaries for r118716.

BUG=108416

------------------------------------------------------------------------

### bu...@chromium.org (2012-01-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=118985

------------------------------------------------------------------------
r118985 | scherkus@chromium.org | Tue Jan 24 18:37:24 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=118985&r2=118984&pathrev=118985

Rolling FFmpeg DEPS 118716:118948.

TBR=inferno
BUG=108416

Review URL: https://chromiumcodereview.appspot.com/9234011
------------------------------------------------------------------------

### in...@chromium.org (2012-01-25)

Andrew confirms that everything is merged to 963.

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

Nice one Aki. Seems like the OOB content might be recoverable so $500!

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

### ao...@gmail.com (2012-02-07)

@scarybeasts Most excellent :) Could you forward this one to Red Cross.

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### si...@gmail.com (2012-02-09)

Just FYI, libvorbis patch for the issue:
https://trac.xiph.org/changeset/18183
https://trac.xiph.org/changeset/18184

### sc...@gmail.com (2012-03-06)

Ok, web site is accepting my credit card. 2 x $1337 donations at a time :)
This $500 was upped to $1337 and sent to American Red Cross.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=21505

------------------------------------------------------------------------
r21505 | scherkus@google.com | 2012-01-25T00:03:08.369041Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=21506

------------------------------------------------------------------------
r21506 | scherkus@google.com | 2012-01-25T02:41:39.209859Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=21508

------------------------------------------------------------------------
r21508 | scherkus@google.com | 2012-01-25T02:57:36.322568Z

------------------------------------------------------------------------

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 118748:118760.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9299191

Uploader: inferno@chromium.org

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x7f8b4bc0b470
Crash State:
  - crash stack -
  render_line
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=118748:118760

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97ic6h_hln-ctcvggnBc5NlEGiz2d55OMe-dZS2fQM3_DtfTZC9UPpb-0pM_7e1-3S7ksKxjVi02pJcJG-bGMoo0j8vPPJMqveynloBueOo97k85xvANWoW3kw9-QZapPkNRNA9jJnxaZwAQ1QY2KIRjQxjbg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/108416?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052347)*
