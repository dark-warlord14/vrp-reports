# Use after free in WebM/matroska at matroska_execute_seekhead()

| Field | Value |
|-------|-------|
| **Issue ID** | [40050148](https://issues.chromium.org/issues/40050148) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-10-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASAN reports a use-after-free when the attached video is played. Reporting as a security vulnerability based on bug type. The cause might be the same as in <https://crbug.com/chromium/100464>, but reporting separately since the crash traces don't seem to have anything in common.

**VERSION**  

Chrome Version: Chromium 16.0.910.0 (Developer Build 105656)  

Operating System: Linux (Debian 6.0.3, x84\_64)

**REPRODUCTION CASE**  

$ chrome uaf-matroska.webm

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

I would have symbolized the ASAN trace, but that seems to require more memory than I have available, so I aborted the attempt after some rather heavy swapping. Sorry about that :(

Program received signal SIGILL, Illegal instruction.  

[Switching to Thread 0x7fffdb946700 (LWP 30309)]  

matroska\_execute\_seekhead (matroska=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:1254  

1254 if (seekhead[i].pos <= before\_pos)  

(gdb) list  

1249 if (!matroska->ctx->pb->seekable ||  

1250 (matroska->ctx->flags & AVFMT\_FLAG\_IGNIDX))  

1251 return;  

1252  

1253 for (i = 0; i < seekhead\_list->nb\_elem; i++) {  

1254 if (seekhead[i].pos <= before\_pos)  

1255 continue;  

1256  

1257 // defer cues parsing until we actually need cue data.  

1258 if (seekhead[i].id == MATROSKA\_ID\_CUES) {  

(gdb) bt 5  

#0 matroska\_execute\_seekhead (matroska=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:1254  

#1 matroska\_read\_header (s=<optimized out>, ap=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:1373  

#2 0x00007fffdd75b283 in avformat\_open\_input (ps=<optimized out>,  

filename=<optimized out>, fmt=<optimized out>, options=<optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:668  

#3 0x00007fffdd75be52 in av\_open\_input\_file (ic\_ptr=<optimized out>, filename=Unhandled dwarf expression opcode 0x0

) at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:583  

#4 0x00007ffff5cf0ca7 in media::FFmpegDemuxer::InitializeTask(media::DataSource\*, base::Callback<void (media::PipelineStatus)> const&) (this=<optimized out>,  

data\_source=<optimized out>, callback=<optimized out>)  

at media/filters/ffmpeg\_demuxer.cc:459  

(More stack frames follow...)

=================================================================  

==30377== ERROR: AddressSanitizer heap-use-after-free on address 0x7f33322258c8 at pc 0x7f3334d2a268 bp 0x7f33314b4af0 sp 0x7f33314b4760  

READ of size 8 at 0x7f33322258c8 thread T19  

#0 0x7f3334d2a268 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x30c268)  

#1 0x7f3334d50283 (/home/aki/chromium/src/out/Release/libffmpegsumo.so+0x332283)  

[...]

## Attachments

- [uaf-matroska.webm](attachments/uaf-matroska.webm) (application/octet-stream; charset=binary, 10.7 KB)

## Timeline

### kc...@chromium.org (2011-10-16)

>>  would have symbolized the ASAN trace, but that seems to require more memory than I have available

Yea. this is due to http://llvm.org/bugs/show_bug.cgi?id=7554 , which is being worked on. 

Here you go (having 24G RAM really helps :)
==2779== ERROR: AddressSanitizer heap-use-after-free on address 0x7f7be051fcc8 at pc 0x7f7be4f96808 bp 0x7f7be00f3ab0 sp 0x7f7be00f3720
READ of size 8 at 0x7f7be051fcc8 thread T5
    #0 0x7f7be4f96808 in matroska_execute_seekhead third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:1254
    #1 0x7f7be4fbc823 in avformat_open_input third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:668
    #2 0x7f7be4fbd3f2 in av_open_input_file third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:583
    #3 0x7f7bfaa813a7 in media::FFmpegDemuxer::InitializeTask(media::DataSource*, base::Callback<void ()(media::PipelineStatus)> const&) media/filters/ffmpeg_demuxer.cc:459
    #4 0x7f7bfaa868fe in base::Callback<void ()(media::PipelineStatus)>::Callback(base::Callback<void ()(media::PipelineStatus)> const&) ./base/callback.h:234
    #5 0x7f7bf52a4cb7 in base::Callback<void ()()>::Run() const ./base/callback.h:269
    #6 0x7f7bf52a5469 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:499
    #7 0x7f7bf52a6978 in MessageLoop::DoWork() base/message_loop.cc:689
    #8 0x7f7bf52b0c6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #9 0x7f7bf52a37b9 in MessageLoop::RunInternal() base/message_loop.cc:444
    #10 0x7f7bf52a1989 in MessageLoop::RunHandler() base/message_loop.cc:417
    #11 0x7f7bf531de18 in base::Thread::ThreadMain() base/threading/thread.cc:163
    #12 0x7f7bf531cabc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:54
    #13 0x7f7bfab2bd85 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer-check/asan/asan_thread.cc:106
    #14 0x7f7bef5109ca in start_thread ??:0
    #15 0x7f7bed69070d in __clone ??:0
0x7f7be051fcc8 is located 8 bytes to the right of 64-byte region [0x7f7be051fc80,0x7f7be051fcc0)
freed by thread T5 here:
    #0 0x7f7bfab21966 in realloc _asan_rtl_
    #1 0x7f7be4fa032e in ebml_parse_elem third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:877
    #2 0x7f7be4fa1466 in ebml_parse third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:828
    #3 0x7f7be4fa0b2f in ebml_parse_elem third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:905
    #4 0x7f7be4fa197b in matroska_parse_seekhead_entry third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:828
    #5 0x7f7be4f968bd in matroska_execute_seekhead third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:1263
    #6 0x7f7be4fbc823 in avformat_open_input third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:668
    #7 0x7f7be4fbd3f2 in av_open_input_file third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:583
    #8 0x7f7bfaa813a7 in media::FFmpegDemuxer::InitializeTask(media::DataSource*, base::Callback<void ()(media::PipelineStatus)> const&) media/filters/ffmpeg_demuxer.cc:459
    #9 0x7f7bfaa868fe in base::Callback<void ()(media::PipelineStatus)>::Callback(base::Callback<void ()(media::PipelineStatus)> const&) ./base/callback.h:234
    #10 0x7f7bf52a4cb7 in base::Callback<void ()()>::Run() const ./base/callback.h:269
    #11 0x7f7bf52a5469 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:499
    #12 0x7f7bf52a6978 in MessageLoop::DoWork() base/message_loop.cc:689
    #13 0x7f7bf52b0c6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #14 0x7f7bf52a37b9 in MessageLoop::RunInternal() base/message_loop.cc:444
    #15 0x7f7bf52a1989 in MessageLoop::RunHandler() base/message_loop.cc:417
    #16 0x7f7bf531de18 in base::Thread::ThreadMain() base/threading/thread.cc:163
    #17 0x7f7bf531cabc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:54
    #18 0x7f7bfab2bd85 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer-check/asan/asan_thread.cc:106
previously allocated by thread T5 here:
    #0 0x7f7bfab21966 in realloc _asan_rtl_
    #1 0x7f7be4fa032e in ebml_parse_elem third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:877
    #2 0x7f7be4fa1466 in ebml_parse third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:828
    #3 0x7f7be4fa0b2f in ebml_parse_elem third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:905
    #4 0x7f7be4fa1466 in ebml_parse third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:828
    #5 0x7f7be4fa0b2f in ebml_parse_elem third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:905
    #6 0x7f7be4f9668f in ebml_parse third_party/ffmpeg/patched-ffmpeg/libavformat/matroskadec.c:828
    #7 0x7f7be4fbc823 in avformat_open_input third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:668
    #8 0x7f7be4fbd3f2 in av_open_input_file third_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:583
    #9 0x7f7bfaa813a7 in media::FFmpegDemuxer::InitializeTask(media::DataSource*, base::Callback<void ()(media::PipelineStatus)> const&) media/filters/ffmpeg_demuxer.cc:459
    #10 0x7f7bfaa868fe in base::Callback<void ()(media::PipelineStatus)>::Callback(base::Callback<void ()(media::PipelineStatus)> const&) ./base/callback.h:234
    #11 0x7f7bf52a4cb7 in base::Callback<void ()()>::Run() const ./base/callback.h:269
    #12 0x7f7bf52a5469 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) base/message_loop.cc:499
    #13 0x7f7bf52a6978 in MessageLoop::DoWork() base/message_loop.cc:689
    #14 0x7f7bf52b0c6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_pump_default.cc:23
    #15 0x7f7bf52a37b9 in MessageLoop::RunInternal() base/message_loop.cc:444
    #16 0x7f7bf52a1989 in MessageLoop::RunHandler() base/message_loop.cc:417
    #17 0x7f7bf531de18 in base::Thread::ThreadMain() base/threading/thread.cc:163
    #18 0x7f7bf531cabc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:54
    #19 0x7f7bfab2bd85 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer-check/asan/asan_thread.cc:106



### sc...@gmail.com (2011-10-17)

I'll take this one. Looks near-identical to something I fixed in OGG.

### sc...@gmail.com (2011-10-17)

[Empty comment from Monorail migration]

### ao...@gmail.com (2011-10-17)

@scarybeasts Some more testcases are at http://haltp.org/aoh/misc/webm/100492-matroska/playall.html. Tested against 105764.

### ts...@chromium.org (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-20)

Confirmed and started. Easy fix.
Use is strictly a simple non-pointer property read so I don't think the security impact is particularly bad.

### sc...@gmail.com (2011-10-20)

Fixed in trunk deps at r106599
Can roll into M17

### bu...@chromium.org (2011-10-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=106599

------------------------------------------------------------------------
r106599 | cevans@chromium.org | Thu Oct 20 15:01:27 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavformat/matroskadec.c?r1=106599&r2=106598&pathrev=106599
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=106599&r2=106598&pathrev=106599
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=106599&r2=106598&pathrev=106599
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/43_mkv_seekahead_revalidate.patch?r1=106599&r2=106598&pathrev=106599

Fix a bug where a pointer was cached to an array that might later move due to
a realloc()

BUG=100492
Review URL: http://codereview.chromium.org/8366004
------------------------------------------------------------------------

### sc...@gmail.com (2011-11-05)

This went to M15 in the end, thanks to the way we handled the ffmpeg changes as a single unit.
Aki -- I don't think the OOB content can be usefully retrieved in this case.

### sc...@gmail.com (2011-11-05)

DEPS rolled on M15 branch @19346
DEPS rolled on M16 branch @19347


### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-16)

We're going over old bugs that might have missed going in front of the VRP panel.  The panel decided to award $3,000 for this bug!

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/100492?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050148)*
