# Use after free with fuzzed ogv file

| Field | Value |
|-------|-------|
| **Issue ID** | [40092541](https://issues.chromium.org/issues/40092541) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Media |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome tab displays sad tab with a fuzzed ogv file.

Chrome debug build crashes with this assertion failiure.  

third\_party/WebKit/Source/JavaScriptCore/wtf/RefCounted.h:derefBase()  

ASSERT(!m\_deletionHasBegun)

Get below mentioned segmentation faults and stack traces when assert is removed.

**VERSION**  

Chrome Version: [14.0.817.0 (Developer Build 91971 Linux)] + [dev]  

Operating System: [Ubuntu, 10.04 LTS, 64 bit]

**REPRODUCTION CASE**  

Please open attached test.ogv file with chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:

# Stack Trace 1

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffb1e30700 (LWP 2193)]  

0x00007ffff2cb1fa2 in base::WaitableEvent::SignalOne (this=0x7fffdbe54e30)  

at base/synchronization/waitable\_event\_posix.cc:369  

369 const bool r = (\*kernel\_->waiters\_.begin())->Fire(this);  

(gdb) bt  

#0 0x00007ffff2cb1fa2 in base::WaitableEvent::SignalOne (this=0x7fffdbe54e30)  

at base/synchronization/waitable\_event\_posix.cc:369  

#1 0x00007ffff2cb1197 in base::WaitableEvent::Signal (this=0x7fffdbe54e30)  

at base/synchronization/waitable\_event\_posix.cc:61  

#2 0x00007ffff2c7d5cc in base::MessagePumpDefault::ScheduleWork (this=  

0x7fffdbe54e20) at base/message\_pump\_default.cc:67  

#3 0x00007ffff2c75415 in MessageLoop::AddToIncomingQueue (this=  

0x7fffdbcd8bb0, pending\_task=0x7fffb1e2e270) at base/message\_loop.cc:647  

#4 0x00007ffff2c73aaa in MessageLoop::PostTask (this=0x7fffdbcd8bb0,  

from\_here=..., task=0x7fffde842780) at base/message\_loop.cc:278  

#5 0x00007ffff5394cf6 in webkit\_glue::BufferedDataSource::Read (this=  

0x7fffd5fc2c60, position=32768, size=32768, data=0x7fffdef8c000 "OggS",  

read\_callback=0x7fffd5f0dae0)  

at webkit/glue/media/buffered\_data\_source.cc:174  

#6 0x00007ffff54d8604 in media::FFmpegDemuxer::Read (this=0x7fffde986960,  

size=32768, data=0x7fffdef8c000 "OggS")  

at media/filters/ffmpeg\_demuxer.cc:374  

#7 0x00007ffff517b31b in ReadContext (h=0x7fffd5f89540, buf=  

0x7fffdef8c000 "OggS", size=32768) at media/filters/ffmpeg\_glue.cc:33  

#8 0x00007fffda1acc3c in retry\_transfer\_wrapper (h=0x7fffd5f89540, buf=  

0x7fffdef8c000 "OggS", size=32768)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/avio.c:269  

#9 ffurl\_read (h=0x7fffd5f89540, buf=0x7fffdef8c000 "OggS", size=32768)  

---Type <return> to continue, or q <return> to quit---c  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/avio.c:295  

#10 0x00007fffda1ae6b4 in fill\_buffer (s=0x7fffdef556e0)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/aviobuf.c:568  

#11 0x00007fffda1ae7c5 in avio\_r8 (s=0x7fffdef556e0)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/aviobuf.c:612  

#12 0x00007fffda1b542a in ogg\_read\_page (s=0x7fffdef94000,  

str=<value optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/oggdec.c:226  

#13 0x00007fffda1b6543 in ogg\_get\_length (s=0x7fffdef94000,  

ap=<value optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/oggdec.c:494  

#14 ogg\_read\_header (s=0x7fffdef94000, ap=<value optimized out>)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/oggdec.c:523  

#15 0x00007fffda1c3181 in av\_open\_input\_stream (ic\_ptr=0x7fffb1e2f1d8, pb=  

0x7fffdef556e0, filename=0x7fffde856678 "<http://0x7fffde986978>", fmt=  

0x7fffda318b60, ap=0x7fffb1e2ebc0)  

at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:445  

#16 0x00007fffda1c34cb in av\_open\_input\_file (ic\_ptr=0x7fffb1e2f1d8, filename=  

0x7fffde856678 "<http://0x7fffde986978>", fmt=0x7fffda318b60, buf\_size=0, ap=  

0x0) at third\_party/ffmpeg/patched-ffmpeg/libavformat/utils.c:613  

#17 0x00007ffff54d8c97 in media::FFmpegDemuxer::InitializeTask (this=  

0x7fffde986960, data\_source=0x7fffd5fc2c60, callback=0x7fffd5f64240)  

at media/filters/ffmpeg\_demuxer.cc:447  

---Type <return> to continue, or q <return> to quit---c  

#18 0x00007ffff54dcbb9 in DispatchToMethod<media::FFmpegDemuxer, void (media::FFmpegDemuxer::\*)(media::DataSource\*, CallbackRunner<Tuple1[media::PipelineStatus](javascript:void(0);) >\*), scoped\_refptr[media::DataSource](javascript:void(0);), CallbackRunner<Tuple1[media::PipelineStatus](javascript:void(0);) >\*> (obj=0x7fffde986960,  

method=0x7ffff54d8a7a <media::FFmpegDemuxer::InitializeTask(media::DataSource\*, CallbackRunner<Tuple1[media::PipelineStatus](javascript:void(0);) >\*)>, arg=...)  

at ./base/tuple.h:558  

#19 0x00007ffff54dc53a in RunnableMethod<media::FFmpegDemuxer, void (media::FFmpegDemuxer::\*)(media::DataSource\*, CallbackRunner<Tuple1[media::PipelineStatus](javascript:void(0);) >\*), Tuple2<scoped\_refptr[media::DataSource](javascript:void(0);), CallbackRunner<Tuple1[media::PipelineStatus](javascript:void(0);) >\*> >::Run (this=0x7fffde81daf0) at ./base/task.h:338  

#20 0x00007ffff2c72421 in Run (this=0x7fffda035270) at base/message\_loop.cc:104  

#21 0x00007ffff2c75fe6 in DoInvoke (base=0x7fffd5f87270)  

at ./base/bind\_internal.h:595  

#22 0x00007ffff274635b in base::Callback<void ()()>::Run() const (this=  

0x7fffb1e2f580) at ./base/callback.h:265  

#23 0x00007ffff2c74db7 in MessageLoop::RunTask (this=0x7fffb1e2fbb0,  

pending\_task=...) at base/message\_loop.cc:484  

#24 0x00007ffff2c74eed in MessageLoop::DeferOrRunPendingTask (this=  

0x7fffb1e2fbb0, pending\_task=...) at base/message\_loop.cc:502  

#25 0x00007ffff2c75703 in MessageLoop::DoWork (this=0x7fffb1e2fbb0)  

at base/message\_loop.cc:693  

#26 0x00007ffff2c7d408 in base::MessagePumpDefault::Run (this=0x7fffde8ed7e0,  

---Type <return> to continue, or q <return> to quit---c  

delegate=0x7fffb1e2fbb0) at base/message\_pump\_default.cc:23  

#27 0x00007ffff2c74bab in MessageLoop::RunInternal (this=0x7fffb1e2fbb0)  

at base/message\_loop.cc:451  

#28 0x00007ffff2c74a5e in MessageLoop::RunHandler (this=0x7fffb1e2fbb0)  

at base/message\_loop.cc:424  

#29 0x00007ffff2c74479 in MessageLoop::Run (this=0x7fffb1e2fbb0)  

at base/message\_loop.cc:348  

#30 0x00007ffff2cbd726 in base::Thread::Run (this=0x7fffde8f1600, message\_loop=  

0x7fffb1e2fbb0) at base/threading/thread.cc:128  

#31 0x00007ffff2cbd8e1 in base::Thread::ThreadMain (this=0x7fffde8f1600)  

at base/threading/thread.cc:164  

#32 0x00007ffff2cbcc6f in ThreadFunc (params=0x7fffd5fd9330)  

at base/threading/platform\_thread\_posix.cc:51  

#33 0x00007fffecc0c9ca in start\_thread (arg=<value optimized out>)  

at pthread\_create.c:300  

#34 0x00007fffea1d870d in clone ()  

at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:112  

#35 0x0000000000000000 in ?? ()

# Stack Trace 2 (Null Pointer)

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffb12b1700 (LWP 2151)]  

0x00007ffff2bbbdcd in tcmalloc::SLL\_Next (t=0x0)  

at third\_party/tcmalloc/chromium/src/linked\_list.h:44  

44 return \*(reinterpret\_cast<void\*\*>(t));  

(gdb) bt  

#0 0x00007ffff2bbbdcd in tcmalloc::SLL\_Next (t=0x0)  

at third\_party/tcmalloc/chromium/src/linked\_list.h:44  

#1 0x00007ffff2bbf57c in tcmalloc::SLL\_PopRange (head=0x7ffff136ba78, N=9,  

start=0x7fffb12af770, end=0x7fffb12af778)  

at third\_party/tcmalloc/chromium/src/linked\_list.h:75  

#2 0x00007ffff2bbf785 in tcmalloc::ThreadCache::FreeList::PopRange (this=  

0x7ffff136ba78, N=9, start=0x7fffb12af770, end=0x7fffb12af778)  

at third\_party/tcmalloc/chromium/src/thread\_cache.h:218  

#3 0x00007ffff2bbe7db in tcmalloc::ThreadCache::ReleaseToCentralCache (this=  

0x7ffff136ba00, src=0x7ffff136ba78, cl=3, N=9)  

at third\_party/tcmalloc/chromium/src/thread\_cache.cc:220  

#4 0x00007ffff2bbe54e in tcmalloc::ThreadCache::ListTooLong (this=  

0x7ffff136ba00, list=0x7ffff136ba78, cl=3)  

at third\_party/tcmalloc/chromium/src/thread\_cache.cc:182  

#5 0x00007ffff2bbc3d2 in tcmalloc::ThreadCache::Deallocate (this=  

0x7ffff136ba00, ptr=0x7fffde2928e0, cl=3)  

at third\_party/tcmalloc/chromium/src/thread\_cache.h:361  

#6 0x00007ffff2bbaef4 in do\_free\_with\_callback (ptr=0x7fffde2928e0,  

invalid\_free\_fn=0x7ffff2bb96e9 <InvalidFree>)  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1227  

#7 0x00007ffff2bbb0a1 in do\_free (ptr=0x7fffde2928e0)  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1249  

#8 0x00007ffff7ff4ca6 in tc\_delete (p=0x7fffde2928e0)  

---Type <return> to continue, or q <return> to quit---c  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1646  

#9 0x00007ffff51727fe in \_\_gnu\_cxx::new\_allocator<std::\_List\_node<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) > > >::deallocate (this=0x7fffde292e80, \_\_p=0x7fffde2928e0)  

at /usr/include/c++/4.4/ext/new\_allocator.h:95  

#10 0x00007ffff5172726 in std::\_List\_base<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) >, std::allocator<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) > > >::\_M\_put\_node (this=  

0x7fffde292e80, \_\_p=0x7fffde2928e0)  

at /usr/include/c++/4.4/bits/stl\_list.h:320  

#11 0x00007ffff5172646 in std::list<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) >, std::allocator<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) > > >::\_M\_erase (this=  

0x7fffde292e80, \_\_position=...)  

at /usr/include/c++/4.4/bits/stl\_list.h:1431  

#12 0x00007ffff51722cf in std::list<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) >, std::allocator<std::pair<media::FilterCollection::FilterType, scoped\_refptr[media::Filter](javascript:void(0);) > > >::erase (this=  

0x7fffde292e80, \_\_position=...) at /usr/include/c++/4.4/bits/list.tcc:111  

#13 0x00007ffff5171da7 in media::FilterCollection::SelectFilter (this=  

0x7fffde292e80, filter\_type=media::FilterCollection::VIDEO\_DECODER,  

filter\_out=0x7fffb12afad0) at media/base/filter\_collection.cc:93  

#14 0x00007ffff5171f67 in media::FilterCollection::SelectFilter<(media::FilterCo---Type <return> to continue, or q <return> to quit---c  

llection::FilterType)1, media::VideoDecoder> (this=0x7fffde292e80, filter\_out=  

0x7fffb12afe50) at media/base/filter\_collection.cc:76  

#15 0x00007ffff5171bf1 in media::FilterCollection::SelectVideoDecoder (this=  

0x7fffde292e80, filter\_out=0x7fffb12afe50)  

at media/base/filter\_collection.cc:50  

#16 0x00007ffff54a6aa2 in media::PipelineImpl::InitializeVideoDecoder (this=  

0x7fffb1d4ddc0, demuxer=...) at media/base/pipeline\_impl.cc:1180  

#17 0x00007ffff54a3fc7 in media::PipelineImpl::InitializeTask (this=  

0x7fffb1d4ddc0) at media/base/pipeline\_impl.cc:687  

#18 0x00007ffff54aa645 in DispatchToMethod<media::PipelineImpl, void (media::PipelineImpl::\*)()> (obj=0x7fffb1d4ddc0,  

method=0x7ffff54a3ce8 [media::PipelineImpl::InitializeTask()](javascript:void(0);), arg=...)  

at ./base/tuple.h:541  

#19 0x00007ffff54a9c64 in RunnableMethod<media::PipelineImpl, void (media::PipelineImpl::\*)(), Tuple0>::Run (this=0x7fffb2422ac0) at ./base/task.h:338  

#20 0x00007ffff2c72421 in Run (this=0x7fffb1db7780) at base/message\_loop.cc:104  

#21 0x00007ffff2c75fe6 in DoInvoke (base=0x7fffb1db7750)  

at ./base/bind\_internal.h:595  

#22 0x00007ffff274635b in base::Callback<void ()()>::Run() const (this=  

0x7fffb12b0580) at ./base/callback.h:265  

#23 0x00007ffff2c74db7 in MessageLoop::RunTask (this=0x7fffb12b0bb0,  

pending\_task=...) at base/message\_loop.cc:484  

#24 0x00007ffff2c74eed in MessageLoop::DeferOrRunPendingTask (this=  

---Type <return> to continue, or q <return> to quit---c  

0x7fffb12b0bb0, pending\_task=...) at base/message\_loop.cc:502  

#25 0x00007ffff2c75703 in MessageLoop::DoWork (this=0x7fffb12b0bb0)  

at base/message\_loop.cc:693  

#26 0x00007ffff2c7d408 in base::MessagePumpDefault::Run (this=0x7fffde4118c0,  

delegate=0x7fffb12b0bb0) at base/message\_pump\_default.cc:23  

#27 0x00007ffff2c74bab in MessageLoop::RunInternal (this=0x7fffb12b0bb0)  

at base/message\_loop.cc:451  

#28 0x00007ffff2c74a5e in MessageLoop::RunHandler (this=0x7fffb12b0bb0)  

at base/message\_loop.cc:424  

#29 0x00007ffff2c74479 in MessageLoop::Run (this=0x7fffb12b0bb0)  

at base/message\_loop.cc:348  

#30 0x00007ffff2cbd726 in base::Thread::Run (this=0x7fffde2ee480, message\_loop=  

0x7fffb12b0bb0) at base/threading/thread.cc:128  

#31 0x00007ffff2cbd8e1 in base::Thread::ThreadMain (this=0x7fffde2ee480)  

at base/threading/thread.cc:164  

#32 0x00007ffff2cbcc6f in ThreadFunc (params=0x7fffb2424150)  

at base/threading/platform\_thread\_posix.cc:51  

#33 0x00007fffecc0c9ca in start\_thread (arg=<value optimized out>)  

at pthread\_create.c:300  

#34 0x00007fffea1d870d in clone ()  

at ../sysdeps/unix/sysv/linux/x86\_64/clone.S:112  

#35 0x0000000000000000 in ?? ()

## Attachments

- [test.ogv](attachments/test.ogv) (application/ogg; charset=binary, 2.9 MB)

## Timeline

### in...@chromium.org (2011-07-10)

Frank, Andrew, can you please help with an owner.

### in...@chromium.org (2011-07-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-10)

I'll take a quick look.

### ih...@chromium.org (2011-07-11)

This should be fixed with this patch
http://patches.ffmpeg.org/patch/5184/
but I have to roll it first. For this I am waiting for
http://codereview.chromium.org/7189006/
to land.

### in...@chromium.org (2011-07-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-13)

Seems to be different to http://code.google.com/p/chromium/issues/detail?id=88436 (which the patched ffmpeg takes care of)

### sc...@gmail.com (2011-07-13)

This one is pretty unique:
==18929== Invalid write of size 8
==18929==    at 0x7E447B3: memcpy (mc_replace_strmem.c:635)
==18929==    by 0x14BCCD46: T.69 (string3.h:52)
==18929==    by 0x14BCD54F: ogg_read_header (oggdec.c:491)
==18929==    by 0x14BDA1B0: av_open_input_stream (utils.c:445)
==18929==    by 0x14BDA4FA: av_open_input_file (utils.c:613)
==18929==    by 0x41E562E: media::FFmpegDemuxer::InitializeTask(media::DataSource*, CallbackRunner<Tuple1<media::PipelineStatus> >*) (ffmpeg_demuxer.cc:447)
==18929==    by 0x41E973A: void DispatchToMethod<media::FFmpegDemuxer, void (media::FFmpegDemuxer::*)(media::DataSource*, CallbackRunner<Tuple1<media::PipelineStatus> >*), scoped_refptr<media::DataSource>, CallbackRunner<Tuple1<media::PipelineStatus> >*>(media::FFmpegDemuxer*, void (media::FFmpegDemuxer::*)(media::DataSource*, CallbackRunner<Tuple1<media::PipelineStatus> >*), Tuple2<scoped_refptr<media::DataSource>, CallbackRunner<Tuple1<media::PipelineStatus> >*> const&) (tuple.h:558)
==18929==    by 0x41E90BB: RunnableMethod<media::FFmpegDemuxer, void (media::FFmpegDemuxer::*)(media::DataSource*, CallbackRunner<Tuple1<media::PipelineStatus> >*), Tuple2<scoped_refptr<media::DataSource>, CallbackRunner<Tuple1<media::PipelineStatus> >*> >::Run() (task.h:338)
==18929==    by 0x194D5C8: (anonymous namespace)::TaskClosureAdapter::Run() (message_loop.cc:104)
==18929==    by 0x195118D: base::internal::Invoker1<false, base::internal::InvokerStorage1<void ((anonymous namespace)::TaskClosureAdapter::*)(), (anonymous namespace)::TaskClosureAdapter*>, void ((anonymous namespace)::TaskClosureAdapter::*)()>::DoInvoke(base::internal::InvokerStorageBase*) (bind_internal.h:595)
==18929==    by 0x1426A12: base::Callback<void ()()>::Run() const (callback.h:265)
==18929==    by 0x194FF5E: MessageLoop::RunTask(MessageLoop::PendingTask const&) (message_loop.cc:484)
==18929==    by 0x1950094: MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) (message_loop.cc:502)
==18929==    by 0x19508AA: MessageLoop::DoWork() (message_loop.cc:693)
==18929==    by 0x19585AF: base::MessagePumpDefault::Run(base::MessagePump::Delegate*) (message_pump_default.cc:23)
==18929==    by 0x194FD52: MessageLoop::RunInternal() (message_loop.cc:451)
==18929==    by 0x194FC05: MessageLoop::RunHandler() (message_loop.cc:424)
==18929==    by 0x194F620: MessageLoop::Run() (message_loop.cc:348)
==18929==    by 0x19988CD: base::Thread::Run(MessageLoop*) (thread.cc:128)
==18929==    by 0x1998A88: base::Thread::ThreadMain() (thread.cc:164)
==18929==    by 0x1997E16: base::(anonymous namespace)::ThreadFunc(void*) (platform_thread_posix.cc:51)
==18929==    by 0xC4379C9: start_thread (pthread_create.c:300)
==18929==    by 0xEEC570C: clone (clone.S:112)
==18929==  Address 0x1625e3a8 is 40 bytes inside a block of size 65,307 free'd
==18929==    at 0x7E40146: free (vg_replace_malloc.c:913)
==18929==    by 0x14BCCD0E: T.69 (oggdec.c:107)
==18929==    by 0x14BCD54F: ogg_read_header (oggdec.c:491)
==18929==    by 0x14BDA1B0: av_open_input_stream (utils.c:445)
==18929==    by 0x14BDA4FA: av_open_input_file (utils.c:613)

Patch is easy

Index: oggdec.c
===================================================================
--- oggdec.c	(revision 90064)
+++ oggdec.c	(working copy)
@@ -109,6 +109,8 @@
         avio_seek (bc, ost->pos, SEEK_SET);
         ogg->curidx = ost->curidx;
         ogg->nstreams = ost->nstreams;
+        ogg->streams = av_realloc (ogg->streams,
+                                   ogg->nstreams * sizeof (*ogg->streams));
         memcpy(ogg->streams, ost->streams,
                ost->nstreams * sizeof(*ogg->streams));
     }


### sc...@gmail.com (2011-07-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-13)

Using WillMerge for lack of a better status. We're waiting for the commit of the 2-liner, plus roll to include that and 33_fix_theora_double_free.patch

### sc...@chromium.org (2011-07-20)

any updates?

### ih...@chromium.org (2011-07-26)

I just rolled ffmpeg again. I hope it sticks:
http://src.chromium.org/viewvc/chrome?view=rev&revision=94027

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### sc...@gmail.com (2011-07-29)

Confirm that this made it into the M14 branch.

@chamal: does this affect older versions of Chrome at all? (Chrome 12, Chrome 13)?

### ch...@gmail.com (2011-07-30)

[Comment Deleted]

### ch...@gmail.com (2011-07-30)

[Comment Deleted]

### ch...@gmail.com (2011-07-30)

Does not reproduce in these versions.

windows 7 home 64 bit
Chrome version - 12.0.742.122

ubuntu 10.04 64 bit
chrome version - 12.0.742.124
chrome version - 13.0.782.107 beta


### sc...@gmail.com (2011-08-02)

@chamal.desilva: thanks for your help. And thanks for finding a bug that would have been a Chrome 14 regression. It is much appreciated.

And this is a fairly clear $1000 Chromium Security Reward, congrats!

One brief note so that your next report can be even better:
- For cases where memory corruption is indicated (e.g. crash in tcmalloc), have you considered running under valgrind? Chromium integrates really well with valgrind and valgrind is really good at giving the exact faulty stack trace for out-of-bounds writes such as this.

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

### ch...@gmail.com (2011-08-02)

@scarybeasts Thanks a lot for the reward :) I will definitely try valgrind next time and provide a better report.

### kc...@chromium.org (2011-08-02)

asan would be another choice for out-of-bound and use-after-free bugs :) 
https://sites.google.com/a/chromium.org/dev/developers/testing/addresssanitizer

### sc...@gmail.com (2011-08-04)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/88850?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092541)*
