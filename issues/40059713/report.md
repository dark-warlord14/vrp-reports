# Security: WebM heap-buffer-overflow in matroskadec.c:matroska_parse_block()

| Field | Value |
|-------|-------|
| **Issue ID** | [40059713](https://issues.chromium.org/issues/40059713) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media>FFmpeg |
| **Reporter** | as...@ut.ee |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-06-14 |
| **Bounty** | $1,000.00 |

## Description

Here is some code from matroskadec.c:matroska\_parse\_block() :

```
int offset = 0, pkt_size = lace_size[n];  

...  

if (pkt_size > size) {  
	av_log(matroska->ctx, AV_LOG_ERROR, "Invalid packet size\n");  
	break;  
}  

...  

if (av_new_packet(pkt, pkt_size+offset) < 0) {  

...  

memcpy (pkt->data+offset, pkt_data, pkt_size);  

```

The problem is that lace\_size[n] is attacker controlled. Also, the pkt\_size >  

size comparision is signed.

The attacker can create a situation where lace\_size[0]=0xffffffff, pkt\_size=-1  

and offset=2. Then av\_new\_packet() will malloc() 1-byte buffer (-1 + 2) and 4GB  

is copied there with memcpy(..., ..., -1).

**VERSION**  

Chrome Version: 18.0.969.0 (Developer Build 113953)  

Operating System: Ubuntu 10.04, i686  

Ubuntu 12.04, x86\_64  

Windows 7, x86\_64

**REPRODUCTION CASE**  

Open bad.webm in chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xaed25b70 (LWP 3168)]  

\_\_memcpy\_ssse3 () at ../sysdeps/i386/i686/multiarch/memcpy-ssse3.S:1282  

1282 ../sysdeps/i386/i686/multiarch/memcpy-ssse3.S: No such file or directory.  

in ../sysdeps/i386/i686/multiarch/memcpy-ssse3.S  

(gdb) x/10i $eip  

=> 0xb1481d32 <\_\_memcpy\_ssse3+3410>: movdqu 0x50(%eax),%xmm5  

0xb1481d37 <\_\_memcpy\_ssse3+3415>: movdqu 0x60(%eax),%xmm6  

0xb1481d3c <\_\_memcpy\_ssse3+3420>: movdqu 0x70(%eax),%xmm7  

0xb1481d41 <\_\_memcpy\_ssse3+3425>: lea 0x80(%eax),%eax  

0xb1481d47 <\_\_memcpy\_ssse3+3431>: sub $0x80,%ecx  

0xb1481d4d <\_\_memcpy\_ssse3+3437>: movntdq %xmm0,(%edx)  

0xb1481d51 <\_\_memcpy\_ssse3+3441>: movntdq %xmm1,0x10(%edx)  

0xb1481d56 <\_\_memcpy\_ssse3+3446>: movntdq %xmm2,0x20(%edx)  

0xb1481d5b <\_\_memcpy\_ssse3+3451>: movntdq %xmm3,0x30(%edx)  

0xb1481d60 <\_\_memcpy\_ssse3+3456>: movntdq %xmm4,0x40(%edx)  

(gdb) info reg  

eax 0xb8a9bfa5 -1196834907  

ecx 0xffba2f60 -4575392  

edx 0xb8a9bd40 -1196835520  

ebx 0xb14c5ff4 -1320394764  

esp 0xaed241d8 0xaed241d8  

ebp 0xb85ce400 0xb85ce400  

esi 0xb85bb660 -1201949088  

edi 0xb863ed20 -1201410784  

eip 0xb1481d32 0xb1481d32 <\_\_memcpy\_ssse3+3410>  

eflags 0x10286 [ PF SF IF RF ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51  

(gdb) bt  

#0 \_\_memcpy\_ssse3 () at ../sysdeps/i386/i686/multiarch/memcpy-ssse3.S:1282  

#1 0xaf87e520 in matroska\_parse\_block (matroska=<value optimized out>,  

data=<value optimized out>, size=<value optimized out>, pos=104,  

cluster\_time=0, duration=0, is\_keyframe=1, cluster\_pos=92)  

at /usr/include/bits/string3.h:52  

#2 0xaf87fbed in matroska\_parse\_cluster\_incremental (s=0xb863fa00,  

pkt=0xaed2443c)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:2073  

#3 matroska\_read\_packet (s=0xb863fa00, pkt=0xaed2443c)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:2094  

#4 0xaf88f857 in av\_read\_packet (s=0xb863fa00, pkt=0xaed2443c)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:730  

#5 0xaf88fd80 in av\_read\_frame\_internal (s=<value optimized out>,  

pkt=<value optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:1188  

#6 0xaf890f80 in avformat\_find\_stream\_info (ic=0xb863fa00, options=0x0)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:2360  

#7 0xaf8926c9 in av\_find\_stream\_info (ic=0xb863fa00)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:2249  

#8 0xb44275f3 in av\_find\_stream\_info (ic=0xb863fa00)  

at out/Debug/obj.target/ffmpeg/geni/ffmpeg\_stubs.cc:440  

#9 0xb5fc064e in media::FFmpegDemuxer::InitializeTask(media::DataSource\*, base::Callback<void ()(media::PipelineStatus)> const&) (this=0xb85b8d90,  

---Type <return> to continue, or q <return> to quit---

## Attachments

- [bad.webm](attachments/bad.webm) (application/octet-stream; charset=binary, 110 B)

## Timeline

### sc...@gmail.com (2012-06-14)

Thanks!

@dalecurtis -- looks like we're going to need to update ffmpeg. The fix is probably simple, if you had any interest in taking it on?

### sc...@gmail.com (2012-06-14)

Or, @asd@ut.ee, you are of course at liberty to propose a patch and run the possibility of a better reward :)

### da...@chromium.org (2012-06-14)

I'll notify Michael Niedermayer upstream instead, he usually cranks out a patch for these less than a couple hours.

We're trying to go upstream first these days :) If I don't get a quick response I'll take it over.

### da...@chromium.org (2012-06-14)

Err, the local patch seemed simple enough that I have it ready to go already. Will still coordinate with upstream to see if that's the proper way to go.

### da...@chromium.org (2012-06-14)

True to my word, Michael cranked out 4 patches + landed my fix! I'll pull these in shortly.

commit 59c122b3b0a00808e3c4f534927755d89e7baa62
Author: Michael Niedermayer <michaelni@gmx.at>
Date:   Fri Jun 15 01:35:52 2012 +0200

    matroskadec: add assert on lack of overflow in pkt_size+offset
    
    currently a overflow there should be impossible but future changes to
    the code could easily introduce a bug that no longer limits the 2
    values sufficiently so better protect it via av_assert.
    
    Signed-off-by: Michael Niedermayer <michaelni@gmx.at>

commit 4b7c52346a2e3cb2d47f8af0b2f036fb9317f502
Author: Michael Niedermayer <michaelni@gmx.at>
Date:   Fri Jun 15 01:29:30 2012 +0200

    matroskadec: change size check in matroska_decode_buffer() to unsigned
    
    Signed-off-by: Michael Niedermayer <michaelni@gmx.at>

commit 08169fc3d2038af4d3b47cc0a9d7d731b5619877
Author: Michael Niedermayer <michaelni@gmx.at>
Date:   Fri Jun 15 01:28:40 2012 +0200

    matroskadec: move lace_size check up so it catches all code pathes
    
    Signed-off-by: Michael Niedermayer <michaelni@gmx.at>

commit 88a740afde048f1c5ce3795a1136e0d6c9d2f289
Author: Michael Niedermayer <michaelni@gmx.at>
Date:   Fri Jun 15 01:27:56 2012 +0200

    matroskadec: change assert to av_assert0()
    
    Signed-off-by: Michael Niedermayer <michaelni@gmx.at>

commit 71529bd8c512bdb47d8d57fc27ff295bc635a561
Author: Dale Curtis <dalecurtis@chromium.org>
Date:   Thu Jun 14 15:22:25 2012 -0700

    Fix incorrect unsigned->signed conversion.
    
    Signed-off-by: Dale Curtis <dalecurtis@chromium.org>
    Signed-off-by: Michael Niedermayer <michaelni@gmx.at>


### da...@chromium.org (2012-06-15)

@cevans, do you want me to land this for M20 as well? We'll need to branch FFmpeg off in that case. I'll land it for M21 today, so let me know.

### da...@chromium.org (2012-06-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-06-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=142328

------------------------------------------------------------------------
r142328 | dalecurtis@google.com | Thu Jun 14 19:35:27 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=142328&r2=142327&pathrev=142328
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_regression_tests.cc?r1=142328&r2=142327&pathrev=142328

Roll FFmpeg to pick up security fixes.

Pulls in the following security fixes:
59c122b matroskadec: add assert on lack of overflow in pkt_size+offset
4b7c523 matroskadec: change size check in matroska_decode_buffer() to unsigned
08169fc matroskadec: move lace_size check up so it catches all code pathes
88a740a matroskadec: change assert to av_assert0()
71529bd Fix incorrect unsigned->signed conversion.

Adds a new test for the issue.

BUG=132779
TEST=ffmpeg_regression_tests, video test matrix.
TBR=scherkus

Review URL: https://chromiumcodereview.appspot.com/10546180
------------------------------------------------------------------------

### sc...@gmail.com (2012-06-15)

Thanks!! That was quick. Yes, we do want this in M20. There's just one M20 beta left, though, so we'd have to move quickly. How safe is this to merge? Do we have good test coverage of different types of Matroska files generated by different programs?

### da...@chromium.org (2012-06-15)

Should be harmless to merge.  It passed all of our regression tests and video test matrix.  I'll start the branching process and get this landed in the next couple hours.

### bu...@chromium.org (2012-06-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=142420

------------------------------------------------------------------------
r142420 | dalecurtis@google.com | Fri Jun 15 10:42:16 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1132/libavformat/matroskadec.c?r1=142420&r2=142419&pathrev=142420

Cherry-picked security fixes. BUG=132779
------------------------------------------------------------------------

### bu...@chromium.org (2012-06-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=142424

------------------------------------------------------------------------
r142424 | dalecurtis@google.com | Fri Jun 15 11:00:50 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1132/chromium/binaries/Chromium/win/ia32/avcodec-54.dll?r1=142424&r2=142423&pathrev=142424
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1132/chromium/patches/README?r1=142424&r2=142423&pathrev=142424
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1132/chromium/binaries/Chromium/win/ia32/avformat-54.dll?r1=142424&r2=142423&pathrev=142424
 M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1132/chromium/binaries/Chromium/win/ia32/avutil-51.dll?r1=142424&r2=142423&pathrev=142424

Update FFmpeg binaries and README. BUG=132779
------------------------------------------------------------------------

### da...@chromium.org (2012-06-15)

All changes should be landed. Fingers crossed :)

### sc...@gmail.com (2012-06-15)

Nice job Dale!

### sc...@gmail.com (2012-06-22)

Memory corruption, $1000, thanks you :)

### as...@ut.ee (2012-06-22)

Thanks :)

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=25875

------------------------------------------------------------------------
r25875 | dalecurtis@google.com | 2012-06-15T02:35:33.912851Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=25887

------------------------------------------------------------------------
r25887 | dalecurtis@google.com | 2012-06-15T18:02:00.681827Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=25888

------------------------------------------------------------------------
r25888 | dalecurtis@google.com | 2012-06-15T18:13:53.097455Z

------------------------------------------------------------------------

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/132779?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media>FFmpeg]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059713)*
