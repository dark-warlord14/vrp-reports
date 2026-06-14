# OOB read in OGV at unpack_vlcs

| Field | Value |
|-------|-------|
| **Issue ID** | [40050143](https://issues.chromium.org/issues/40050143) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | rb...@google.com |
| **Created** | 2011-10-15 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

ASAN reports a global-buffer-overflow when the attached OGV video is played. I haven't yet had a look if it seems to have security impact, but filing conservatively as a security bug.

**VERSION**  

Chrome Version: Chromium 16.0.910.0 (Developer Build 105656)  

Operating System: Linux (Debian 6.0.3, x84\_64)

**REPRODUCTION CASE**  

$ chrome oobr.ogv

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGILL, Illegal instruction.  

[Switching to Thread 0x7fffbaa2a700 (LWP 5305)]  

unpack\_vlcs (s=<optimized out>, gb=Unhandled dwarf expression opcode 0x0  

)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp3.c:899  

899 eob\_run = eob\_run\_base[token];  

(gdb) list  

894 while (coeff\_i < num\_coeffs && get\_bits\_left(gb) > 0) {  

895 /\* decode a VLC into a token \*/  

896 token = get\_vlc2(gb, vlc\_table, 11, 3);  

897 /\* use the token to get a zero run, a coefficient, and an eob run \*/  

898 if (token <= 6) {  

899 eob\_run = eob\_run\_base[token];  

900 if (eob\_run\_get\_bits[token])  

901 eob\_run += get\_bits(gb, eob\_run\_get\_bits[token]);  

902  

903 // record only the number of blocks ended in this plane,  

(gdb) bt 5  

#0 unpack\_vlcs (s=<optimized out>, gb=Unhandled dwarf expression opcode 0x0  

)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp3.c:899  

#1 0x00007fffdd6d1d6c in unpack\_dct\_coeffs (s=<optimized out>,  

gb=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp3.c:1042  

#2 vp3\_decode\_frame (avctx=<optimized out>, data=<optimized out>,  

data\_size=<optimized out>, avpkt=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp3.c:1952  

#3 0x00007fffdd6a13f2 in avcodec\_decode\_video2 (avctx=<optimized out>,  

picture=<optimized out>, got\_picture\_ptr=<optimized out>,  

avpkt=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/utils.c:769  

#4 0x00007ffff5cd8ae7 in media::FFmpegVideoDecodeEngine::DecodeFrame (  

this=<optimized out>, buffer=DWARF-2 expression error: DW\_OP\_reg operations must be used either alone or in conjuction with DW\_OP\_piece or DW\_OP\_bit\_piece.  

)  

at media/video/ffmpeg\_video\_decode\_engine.cc:181  

(More stack frames follow...)  

==19248== ERROR: AddressSanitizer global-buffer-overflow on address 0x7f94dbc029dc at pc 0x7f94dbaf52fc bp 0x7f94d61d5d9c sp 0x7f94d61d53c0  

READ of size 4 at 0x7f94dbc029dc thread T7  

#0 0x7f94dbaf52fc (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2b22fc)  

#1 0x7f94dbaebd6c (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2a8d6c)  

#2 0x7f94dbabb3f2 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2783f2)  

#3 0x7f94f1263ae7 (/home/aki/chromium/src/out/Release/chrome+0x77abae7)  

#4 0x7f94f126330e (/home/aki/chromium/src/out/Release/chrome+0x77ab30e)  

#5 0x7f94f12537cf (/home/aki/chromium/src/out/Release/chrome+0x779b7cf)  

#6 0x7f94f12564dc (/home/aki/chromium/src/out/Release/chrome+0x779e4dc)  

#7 0x7f94ebaad6d7 (/home/aki/chromium/src/out/Release/chrome+0x1ff56d7)  

#8 0x7f94ebaade89 (/home/aki/chromium/src/out/Release/chrome+0x1ff5e89)  

#9 0x7f94ebaaf398 (/home/aki/chromium/src/out/Release/chrome+0x1ff7398)  

#10 0x7f94ebab968a (/home/aki/chromium/src/out/Release/chrome+0x200168a)  

#11 0x7f94ebaac1d9 (/home/aki/chromium/src/out/Release/chrome+0x1ff41d9)  

#12 0x7f94ebaaa3a9 (/home/aki/chromium/src/out/Release/chrome+0x1ff23a9)  

#13 0x7f94ebb26928 (/home/aki/chromium/src/out/Release/chrome+0x206e928)  

#14 0x7f94ebb255cc (/home/aki/chromium/src/out/Release/chrome+0x206d5cc)  

#15 0x7f94f13266d5 (/home/aki/chromium/src/out/Release/chrome+0x786e6d5)  

#16 0x7f94e5d708ba (/lib/libpthread-2.11.2.so+0x68ba)  

#17 0x7f94e3ef702d (/lib/libc-2.11.2.so+0xcf02d)  

0x7f94dbc029dc is located 49 bytes to the right of global variable '.str18' (0x7f94dbc02980) of size 43  

'.str18' is ascii string 'Invalid number of coefficents at level %d  

'  

0x7f94dbc029dc is located 4 bytes to the left of global variable 'eob\_run\_base' (0x7f94dbc029e0) of size 28  

'eob\_run\_base' is ascii string '�01'

## Attachments

- [oobr.ogv](attachments/oobr.ogv) (application/ogg; charset=binary, 96.5 KB)
- [0001-vp3-fix-double-free-and-invalid-read.patch](attachments/0001-vp3-fix-double-free-and-invalid-read.patch) (text/x-c; charset=us-ascii, 2.7 KB)
- [0001-vp3-fix-a-series-of-memleaks-and-potential-infloops-.patch](attachments/0001-vp3-fix-a-series-of-memleaks-and-potential-infloops-.patch) (text/x-c; charset=us-ascii, 5.2 KB)

## Timeline

### kc...@chromium.org (2011-10-15)

 aohelin@, just FYI: you can use the script third_party/asan/scripts/asan_symbolize.py to symbolize the asan stack traces. 

In this bug it looks like we are reading minus-one's element (token == 1):
eob_run = eob_run_base[token];

### ao...@gmail.com (2011-10-15)

@kcc: Thanks, I'll use that in the future.

I think all cases of this so far have read -1, which makes this sound less like a security bug.

### sc...@gmail.com (2011-10-16)

@ihf, @rbultje, either of you know anything about the ffmpeg Theora video codec? :) (This probably isn't a regression, so the urgency is lower; we don't necessarily need it for M15)

### rb...@google.com (2011-10-16)

Not specifically, but I can look...

### rb...@google.com (2011-10-16)

I think we can simply change the token <= 6 check to (unsigned) token <= 6U, so that it catches the -1. It's an invalid bitstream either way so we just want to error out at that point (similar to if token were >6), and changing that check does exactly that.

### sc...@gmail.com (2011-10-19)

If negatives are generally undesired for "token", we could also change the variable type to be unsigned.

@aohelin: I presume this is an old bug that affects Chrome 15 beta too?

### ao...@gmail.com (2011-10-19)

@scarybeasts: I don't know but suspect so. This doesn't crash because the read is valid, just past the object, so not sure until my beta pull&build is done.

### ao...@gmail.com (2011-10-20)

@scarybeasts: This affects my build of r104978, which was the revision of google-chrome-beta yesterday. I used gclient sync --revision src@... because I didn't find a way yet to ask gclient to follow beta or stable.

### sc...@gmail.com (2011-10-20)

Hey Ronald, I can productionize up this change and land it.

### rb...@google.com (2011-10-21)

See attached. There's tons of memleaks and I'm not quite sure how to fix them, the decoder looks a little orphaned. Since those are not crashers, I think we can safely fix them later.

### sc...@gmail.com (2011-10-21)

Yeah, we're not worried about memleaks upon invalid streams. Not a security concern.
You want me to pull the patch into Chrome or had you already started?

### rb...@google.com (2011-10-23)

Hi,

attached patch fixes all memleaks that I could find in the VP3 decoder, plus a potential infloop that I saw while testing on x86-32 (I normally develop on x86-64 and there it didn't happen; no idea why). The sample in this bug report is a good trigger. :-).

Ronald

### la...@google.com (2011-10-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-26)

Ronald has a patch up for review. Assigning to him. It's not too serious an issue so letting it roll into M17 is fine.

### bu...@chromium.org (2011-10-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=107489

------------------------------------------------------------------------
r107489 | scherkus@chromium.org | Wed Oct 26 17:38:14 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/42_vp8_fix_segmentation_maps.patch?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vp3.c?r1=107489&r2=107488&pathrev=107489
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/45_mkv_fix_segmap_cache_overflow.patch?r1=107489&r2=107488&pathrev=107489
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/47_vp3_fix_infloop_and_memleak.patch?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/39_VP8_fix_oob_read_writes.patch?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vp8.c?r1=107489&r2=107488&pathrev=107489
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/46_vp3_fix_double_free_invalid_read.patch?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/ugly/41_matroska_cluster_incremental.patch?r1=107489&r2=107488&pathrev=107489
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=107489&r2=107488&pathrev=107489

Apply patches from 101172, 100465.

Update some patches so they apply with make_src_tree.sh.

Patch by rbultje@chromium.org:
http://codereview.chromium.org/8392015/

BUG=101172,100465
------------------------------------------------------------------------

### bu...@chromium.org (2011-10-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=107500

------------------------------------------------------------------------
r107500 | scherkus@chromium.org | Wed Oct 26 18:09:22 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avformat-53.dll?r1=107500&r2=107499&pathrev=107500
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avcodec-53.dll?r1=107500&r2=107499&pathrev=107500
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avutil-51.dll?r1=107500&r2=107499&pathrev=107500

Windows Chromium FFmpeg binaries for r107489.

BUG=101172,100465

------------------------------------------------------------------------

### bu...@chromium.org (2011-10-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=107508

------------------------------------------------------------------------
r107508 | scherkus@chromium.org | Wed Oct 26 18:41:02 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=107508&r2=107507&pathrev=107508

Rolling FFmpeg to r107500.

BUG=101172,100465
------------------------------------------------------------------------

### sc...@gmail.com (2011-10-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-02)

Bumping up severity due to the double-free aspect.
Also, might as well fix it in M15 with the other ffmpeg fixes.

### sc...@gmail.com (2011-11-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-05)

Thanks for the report, Aki! There was a double-free hiding behind the relatively harmless OOB read, so therefore a $500 Chromium Security Reward!

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

@scarybeasts thanks for spotting the double-free :)

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-23)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=19010

------------------------------------------------------------------------
r19010 | scherkus@google.com | 2011-10-27T01:11:20.629115Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=19011

------------------------------------------------------------------------
r19011 | scherkus@google.com | 2011-10-27T01:42:10.797392Z

------------------------------------------------------------------------

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

### bu...@chromium.org (2013-04-01)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/100465?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050143)*
