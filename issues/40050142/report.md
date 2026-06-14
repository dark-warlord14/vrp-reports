# Use-after-free in WebM at decode_mb_mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40050142](https://issues.chromium.org/issues/40050142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media |
| **Reporter** | ao...@gmail.com |
| **Assignee** | rb...@google.com |
| **Created** | 2011-10-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASAN reports a use-after-free when the attached video is played. Reporting as a security bug based on bug type.

**VERSION**  

Chrome Version: 16.0.910.0 (Developer Build 105656)  

Operating System: Linux (Debian 6.0.3, x84\_64)

**REPRODUCTION CASE**  

$ chrome uaf.webm

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGILL, Illegal instruction.  

[Switching to Thread 0x7fffd85e2700 (LWP 2789)]  

decode\_mb\_mode (mb\_y=<optimized out>, s=<optimized out>, mb=<optimized out>,  

mb\_x=<optimized out>, mb\_y=<optimized out>, segment=<optimized out>,  

ref=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp8.c:601  

---Type <return> to continue, or q <return> to quit---  

601 \*segment = ref ? \*ref : \*segment;  

(gdb) list  

596 VP56RangeCoder \*c = &s->c;  

597  

598 if (s->segmentation.update\_map)  

599 \*segment = vp8\_rac\_get\_tree(c, vp8\_segmentid\_tree, s->prob->segmentid);  

600 else  

601 \*segment = ref ? \*ref : \*segment;  

602 s->segment = \*segment;  

603  

604 mb->skip = s->mbskip\_enabled ? vp56\_rac\_get\_prob(c, s->prob->mbskip) : 0;  

605  

(gdb) bt 5  

#0 decode\_mb\_mode (mb\_y=<optimized out>, s=<optimized out>,  

mb=<optimized out>, mb\_x=<optimized out>, mb\_y=<optimized out>,  

segment=<optimized out>, ref=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp8.c:601

#1 vp8\_decode\_frame (avctx=Unhandled dwarf expression opcode 0x0  

)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/vp8.c:1654  

#2 0x00007fffdd694e7b in frame\_worker\_thread (arg=Unhandled dwarf expression opcode 0x0  

)  

at third\_party/ffmpeg/patched-ffmpeg/libavcodec/pthread.c:301  

#3 0x00007ffff5d9b6d5 in AsanThread::ThreadStart (this=0x7fffe1085080)  

at asan\_thread.cc:105  

#4 0x00007fffea7e58ba in start\_thread () from /lib/libpthread.so.0  

(More stack frames follow...)

ASAN:  

==2113== ERROR: AddressSanitizer heap-use-after-free on address 0x7faf32ad6080 at pc 0x7faf2f7e4919 bp 0x7faf291abd10 sp 0x7faf291ab3a0  

READ of size 1 at 0x7faf32ad6080 thread T8  

#0 0x7faf2f7e4919 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x2d8919)  

#1 0x7faf2f777e7b (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x26be7b)  

#2 0x7faf44fef6d5 (/home/aki/chromium/src/out/Release/chrome+0x786e6d5)  

#3 0x7faf39a398ba (/lib/libpthread-2.11.2.so+0x68ba)  

#4 0x7faf37bc002d (/lib/libc-2.11.2.so+0xcf02d)  

[2080:2320:24124819084:ERROR:platform\_thread\_posix.cc(253)] Not implemented reached in static void base::PlatformThread::SetThreadPriority(PlatformThreadHandle, base::ThreadPriority)  

CHECK failed: size at asan\_allocator.cc:88  

#0 0x7faf44fe5b50 (/home/aki/chromium/src/out/Release/chrome+0x7864b50)  

#1 0x7faf44fea758 (/home/aki/chromium/src/out/Release/chrome+0x7869758)

## Attachments

- [uaf.webm](attachments/uaf.webm) (application/octet-stream; charset=binary, 250.0 KB)
- [0001-vp8-fix-up-handling-of-segmentation_maps-in-referenc.patch](attachments/0001-vp8-fix-up-handling-of-segmentation_maps-in-referenc.patch) (text/plain; charset=us-ascii, 7.3 KB)
- [0001-vp8-fix-up-handling-of-segmentation_maps-in-referenc.patch](attachments/0001-vp8-fix-up-handling-of-segmentation_maps-in-referenc_53357550.patch) (text/plain; charset=us-ascii, 7.4 KB)

## Timeline

### kc...@chromium.org (2011-10-15)

glider@, could you please check why asan asserts while reporting this bug? 

### sc...@gmail.com (2011-10-16)

@rbultje: do your latest vp8 patches cover this one?

### rb...@google.com (2011-10-16)

No. I believe this can happen when the reference gets free()ed in parallel decoding, because the reference is part of the decoding instance, not the picture.

I can look at this monday, is that early enough?

### rb...@google.com (2011-10-16)

Attached patch is a proof-of-concept of how this should be fixed. I've tested it quickly under valgrind and it works, it also passes the VP8 conformance suite, but it may need some more testing e.g. on all the fuzz-files from previous bug reports (which I don't have at home).

What it does is that it delays free()ing of segmentation_map[] until the next decoding iteration, except on codec-close (otherwise you have a memory leak, and at that point all threads are closed down anyway). I haven't confirmed that it fixes this bug, but it should. :-). I'll work on that monday.

### kc...@chromium.org (2011-10-16)

with asan ToT I don't see the assert: 

==1896== ERROR: AddressSanitizer heap-use-after-free on address 0x7f4bb788a080 at pc 0x7f4bb496118e bp 0x7f4ba9ea63b0 sp 0x7f4ba9ea63a8
READ of size 1 at 0x7f4bb788a080 thread T8
    #0 0x7f4bb496118e in decode_mb_mode third_party/ffmpeg/patched-ffmpeg/libavcodec/vp8.c:601
    #1 0x7f4bb490c114 in frame_worker_thread third_party/ffmpeg/patched-ffmpeg/libavcodec/pthread.c:301
    #2 0x7f4bc9e11bc5 in AsanThread::ThreadStart() /home/kcc/asan/asan/asan_thread.cc:106
    #3 0x7f4bbef199ca in start_thread ??:0
    #4 0x7f4bbd09970d in __clone ??:0
0x7f4bb788a080 is located 0 bytes inside of 300-byte region [0x7f4bb788a080,0x7f4bb788a1ac)
freed by thread T7 here:
    #0 0x7f4bc9e072b6 in free _asan_rtl_
    #1 0x7f4bb49f6308 in av_free third_party/ffmpeg/patched-ffmpeg/libavutil/mem.c:152
    #2 0x7f4bb4917a89 in avcodec_decode_video2 third_party/ffmpeg/patched-ffmpeg/libavcodec/utils.c:766
previously allocated by thread T9 here:
    #0 0x7f4bc9e0782d in posix_memalign _asan_rtl_
    #1 0x7f4bb49f621b in av_malloc third_party/ffmpeg/patched-ffmpeg/libavutil/mem.c:90
    #2 0x7f4bb49f633f in av_mallocz third_party/ffmpeg/patched-ffmpeg/libavutil/mem.c:165
    #3 0x7f4bb490c114 in frame_worker_thread third_party/ffmpeg/patched-ffmpeg/libavcodec/pthread.c:301


### ao...@gmail.com (2011-10-17)

@rbultje I haven't yet tested with the preliminary patch, but http://haltp.org/aoh/misc/webm/100464-vp8/playall.html has a bunch of videos which trigger this before it (r105764).

@kcc fwiw, asan printed lots of overlapping error messages when the issue was filed. I think that only happened when opening the files directly (not via <video ..>). Seems to work also here now.

### rb...@google.com (2011-10-18)

I think my patches makes the VP8 decoder clean on all files in this bug report (rad-*.webm) and the ones from 99652. The original patch has a brainfart which makes it fix the bug but not the crash (uhm, ...), so attached patch is a slight modification to actually fix the crash also.

rad-22.webm, rad-29.webm, rad-48.webm, rad-55.webm still trigger valgrind errors in the vorbis decoder, and (when running using the ffmpeg executable), I get libavfilter errors also, but I don't think we care about these (rad-55.webm actually crashes inside libavfilter with -threads 2). In short, Andrew I think this patch should be OK to submit for M15.

### bu...@chromium.org (2011-10-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=105977

------------------------------------------------------------------------
r105977 | scherkus@chromium.org | Mon Oct 17 17:34:20 PDT 2011

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/42_vp8_fix_segmentation_maps.patch?r1=105977&r2=105976&pathrev=105977
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vp8.c?r1=105977&r2=105976&pathrev=105977
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vp8.h?r1=105977&r2=105976&pathrev=105977
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=105977&r2=105976&pathrev=105977

VP8: fix up handling of segmentation_maps in reference frames.

Associate segmentation_map[] with reference frame, rather than decoding instance. This fixes cases where the map would be free()'ed on e.g. a size change in one thread, whereas the other thread was still accessing it. Also, it fixes cases where threads overwrite data that is still being referenced by the previous thread, who thinks that it's part of the frame previously decoded by the next thread.

Patch by rbultje@chromium.org.

BUG=100464
TEST=run file in bug report
TBR=rbultje

Review URL: http://codereview.chromium.org/8341002
------------------------------------------------------------------------

### in...@chromium.org (2011-10-18)

Is this a m15 regression. Is a safe merge for m15.

### bu...@chromium.org (2011-10-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=106016

------------------------------------------------------------------------
r106016 | scherkus@chromium.org | Mon Oct 17 20:02:05 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avformat-53.dll?r1=106016&r2=106015&pathrev=106016
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avcodec-53.dll?r1=106016&r2=106015&pathrev=106016
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/binaries/win/avutil-51.dll?r1=106016&r2=106015&pathrev=106016

Windows Chromium FFmpeg binaries for r105977.

BUG=100464

------------------------------------------------------------------------

### sc...@chromium.org (2011-10-18)

Fixed in trunk -- request merge but will leave it up to kareng / security folks to sort it out.

### in...@chromium.org (2011-10-18)

Is it a regression and how risky is the merge. If a regression, we should definitely merge by today.

### bu...@chromium.org (2011-10-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=106019

------------------------------------------------------------------------
r106019 | scherkus@chromium.org | Mon Oct 17 20:20:16 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=106019&r2=106018&pathrev=106019

Update FFmpeg to r106016.

BUG=100464
------------------------------------------------------------------------

### sc...@chromium.org (2011-10-18)

Do we need to wait a day for the requisite canary build (i.e., I'll merge it tomorrow?)

### in...@chromium.org (2011-10-18)

ok, please remember to merge it before 7 pm tmrw. better to do it early so Karen can see a nice shiny green waterfall.also can you please check out http://code.google.com/p/chromium/issues/detail?id=99480

### in...@chromium.org (2011-10-18)

Andrew, ping ! pong ! ding ! Just a remember for the merge and verifying the canary :)

### sc...@chromium.org (2011-10-18)

merged

### in...@chromium.org (2011-10-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

Thank you for catching this regression, Aki. $1000

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

### ao...@gmail.com (2011-10-20)

@scarybeasts: excellent \o/

### sc...@gmail.com (2011-10-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18672

------------------------------------------------------------------------
r18672 | scherkus@google.com | 2011-10-18T03:20:00.655848Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18673

------------------------------------------------------------------------
r18673 | scherkus@google.com | 2011-10-18T03:21:56.055527Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18702

------------------------------------------------------------------------
r18702 | scherkus@google.com | 2011-10-18T20:37:46.448679Z

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

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/100464?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail mergedwith: crbug.com/chromium/101027]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050142)*
