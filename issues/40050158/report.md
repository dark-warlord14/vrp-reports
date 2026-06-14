# OOB read in WebM/vorbis at render_line()

| Field | Value |
|-------|-------|
| **Issue ID** | [40050158](https://issues.chromium.org/issues/40050158) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-10-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Asan reports a global-buffer-overflow when the attached video is played. Probably worth checking if there is any useful control and range in it.

**VERSION**  

Chrome Version: 16.0.911.10 (dev)  

Operating System: Linux

**REPRODUCTION CASE**  

$ chrome oobr-vorbis.webm

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGILL, Illegal instruction.  

[Switching to Thread 0x7fffdb204700 (LWP 31404)]  

render\_line (x0=<optimized out>, y0=<optimized out>, x1=<optimized out>,  

y1=<optimized out>, buf=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:198  

198 buf[x] = ff\_vorbis\_floor1\_inverse\_db\_table[y];  

(gdb) list  

193 err += ady;  

194 if (err >= 0) {  

195 err -= adx;  

196 y += sy;  

197 }  

198 buf[x] = ff\_vorbis\_floor1\_inverse\_db\_table[y];  

199 }  

200 }  

201 }  

202  

(gdb) bt 5  

#0 render\_line (x0=<optimized out>, y0=<optimized out>, x1=<optimized out>,  

y1=<optimized out>, buf=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:198  

#1 0x00007fffdd67c9d5 in ff\_vorbis\_floor1\_render\_list (list=<optimized out>,  

values=<optimized out>, y\_list=<optimized out>, flag=<optimized out>,  

multiplier=<optimized out>, out=<optimized out>, samples=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbis.c:216  

#2 0x00007fffdd6960a3 in vorbis\_floor1\_decode (vc=<optimized out>,  

vfu=<optimized out>, vec=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1259  

#3 0x00007fffdd6800f3 in vorbis\_parse\_audio\_packet (vc=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1507  

#4 vorbis\_decode\_frame (avccontext=<optimized out>, data=<optimized out>,  

data\_size=<optimized out>, avpkt=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1620  

(More stack frames follow...)

# (no symbols again due to slowness of swapping via usb2) ASAN:SIGILL

==31470== ERROR: AddressSanitizer global-buffer-overflow on address 0x7f4e0996b840 at pc 0x7f4e09835d0a bp 0xae sp 0x7f4e04923980  

READ of size 4 at 0x7f4e0996b840 thread T6  

#0 0x7f4e09835d0a (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x27cd0a)  

#1 0x7f4e098359d5 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x27c9d5)  

#2 0x7f4e0984f0a3 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2960a3)  

#3 0x7f4e098390f3 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2800f3)  

#4 0x7f4e09831cb1 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x278cb1)  

#5 0x7f4e1efdf2e4 (/home/aki/chromium/src/out/Release/chrome+0x77b22e4)  

#6 0x7f4e1efe0b8c (/home/aki/chromium/src/out/Release/chrome+0x77b3b8c)  

#7 0x7f4e198340f7 (/home/aki/chromium/src/out/Release/chrome+0x20070f7)  

#8 0x7f4e198348a9 (/home/aki/chromium/src/out/Release/chrome+0x20078a9)  

#9 0x7f4e19835db8 (/home/aki/chromium/src/out/Release/chrome+0x2008db8)  

#10 0x7f4e198400aa (/home/aki/chromium/src/out/Release/chrome+0x20130aa)  

#11 0x7f4e19832bf9 (/home/aki/chromium/src/out/Release/chrome+0x2005bf9)  

#12 0x7f4e19830dc9 (/home/aki/chromium/src/out/Release/chrome+0x2003dc9)  

#13 0x7f4e198ad358 (/home/aki/chromium/src/out/Release/chrome+0x2080358)  

#14 0x7f4e198abffc (/home/aki/chromium/src/out/Release/chrome+0x207effc)  

#15 0x7f4e1f0bb135 (/home/aki/chromium/src/out/Release/chrome+0x788e135)  

#16 0x7f4e13ae58ba (/lib/libpthread-2.11.2.so+0x68ba)  

#17 0x7f4e11c6c02d (/lib/libc-2.11.2.so+0xcf02d)  

0x7f4e0996b840 is located 0 bytes to the right of global variable 'ff\_vorbis\_floor1\_inverse\_db\_table' (0x7f4e0996b440) of size 1024  

==31470== ABORTING  

Shadow byte and word:  

0x1fe9c132d708: f9  

0x1fe9c132d708: f9 f9 f9 f9 00 00 00 00  

More shadow bytes:  

0x1fe9c132d6e8: 00 00 00 00 00 00 00 00  

0x1fe9c132d6f0: 00 00 00 00 00 00 00 00  

0x1fe9c132d6f8: 00 00 00 00 00 00 00 00  

0x1fe9c132d700: 00 00 00 00 00 00 00 00  

=>0x1fe9c132d708: f9 f9 f9 f9 00 00 00 00  

0x1fe9c132d710: 00 00 00 00 00 00 00 00  

0x1fe9c132d718: 00 00 00 00 00 00 00 00  

0x1fe9c132d720: f9 f9 f9 f9 00 00 00 00  

0x1fe9c132d728: 00 00 00 00 00 00 00 00

## Attachments

- [oobr-vorbis.webm](attachments/oobr-vorbis.webm) (application/octet-stream; charset=binary, 234.5 KB)

## Timeline

### sc...@gmail.com (2011-10-18)

It's in vorbis.c aka. aaaarghhh.c so I will take it.

### ts...@chromium.org (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-20)

Starting to look at this one too...

### sc...@gmail.com (2011-10-20)

I have to say, ASAN is kicking valgrind's ass here. valgrind just can't see it, but there's obviously an error if I add these lines just before the derefence:


Index: vorbis.c
===================================================================
--- vorbis.c	(revision 106517)
+++ vorbis.c	(working copy)
@@ -195,6 +195,8 @@
                 err -= adx;
                 y   += sy;
             }
+if (y < 0 || y >= sizeof(ff_vorbis_floor1_inverse_db_table)/sizeof(ff_vorbis_floor1_inverse_db_table[0]))
+    av_log(NULL, AV_LOG_ERROR, "OOB READ: %d\n", y);
             buf[x] = ff_vorbis_floor1_inverse_db_table[y];
         }


### bu...@chromium.org (2011-10-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=106621

------------------------------------------------------------------------
r106621 | cevans@chromium.org | Thu Oct 20 16:11:04 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vorbis.c?r1=106621&r2=106620&pathrev=106621
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/44_vorbis_oob_read.patch?r1=106621&r2=106620&pathrev=106621
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=106621&r2=106620&pathrev=106621
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=106621&r2=106620&pathrev=106621

Avoid the possibility to read out-of-bounds of a static global array in Vorbis
decoding.

BUG=100543
Review URL: http://codereview.chromium.org/8365014
------------------------------------------------------------------------

### sc...@gmail.com (2011-10-20)

Still needs a DEPS roll on trunk, but fixed in a defensive manner.
Action item for cevans: send the stream to ffmpeg-devel@ffmpeg.org and libav-devel@libav.org to see if there's an additional higher level validation / fix that the Vorbis experts want to apply.

Sending to panel as the OOB data is rendered as a float to an output buffer. If any static global data contained pointer values, there's a change of ASLR bypass.

### sc...@gmail.com (2011-11-02)

This should go to 15 as it might be an infoleak.

### sc...@gmail.com (2011-11-05)

Nice bug Aki! I think this might feasibly be used to leak pointer values (i.e. a possible ASLR bypass) so this qualifies at the $500 level for reward.

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

### sc...@gmail.com (2011-11-05)

DEPS rolled on M15 branch @19346
DEPS rolled on M16 branch @19347


### ao...@gmail.com (2011-11-05)

@scarybeasts Excellent :) This bounty is aimed at Red Cross.

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-11-09)

Should the CVE be 3894? *3 was in the preceding video issue and *5 is in the next one.

### ke...@chromium.org (2011-11-09)

Aki, MITRE has asked us to start grouping bugs of the same type and by the same finder under single CVEs.

### ao...@gmail.com (2011-11-09)

@kenrb Ok, makes sense. Just checked that for internal bookkeeping.

### ke...@chromium.org (2011-11-09)

No problem, thanks for double-checking. We _do_ make mistakes on those numbers sometimes.

### sc...@gmail.com (2011-11-09)

What Ken means: Chris royally screws up from time to time.

### sc...@gmail.com (2011-11-10)

$1337 send to Red Cross

### sc...@chromium.org (2012-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

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

This issue was migrated from crbug.com/chromium/100543?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050158)*
