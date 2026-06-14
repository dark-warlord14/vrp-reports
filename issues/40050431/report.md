# OOB read in WebM/vorbis vorbis_decode_frame()

| Field | Value |
|-------|-------|
| **Issue ID** | [40050431](https://issues.chromium.org/issues/40050431) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-10-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports an heap buffer overflow (read) when the attached video is played in Chromium. The read is 384 past the end of an object. This appears to also affect the stable version, where the renderer often crashes with a general protection error.

**VERSION**  

Chrome Version: 17.0.918.0 (dev, also stable)  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

$ chrome oobr-vorbis-2.webm

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

I don't have enough memory to symbolize ASan traces with full debugging data, but thanks to a tip form kcc at least the symbols are here.

=================================================================  

==26270== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f4d053a6200 at pc 0x7f4d819e44f8 bp 0x7f4d28a3b430 sp 0x7f4d28a3b428  

READ of size 4 at 0x7f4d053a6200 thread T92  

#0 0x7f4d819e44f8 in vorbis\_decode\_frame third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:0  

#1 0x7f4d819d6f91 in avcodec\_decode\_audio3 ??:0  

#2 0x7f4d9697d476 in \_ZN5media18FFmpegAudioDecoder14DoDecodeBufferERK13scoped\_refptrINS\_6BufferEE sysinfo.cc:0  

#3 0x7f4d9697eafc in \_ZN4base8internal8Invoker2ILb0ENS0\_15InvokerStorage2IMN5media18FFmpegAudioDecoderEFvRK13scoped\_refptrINS3\_6BufferEEEPS4\_S7\_EESB\_E8DoInvokeEPNS0\_18InvokerStorageBaseE sysinfo.cc:0  

#4 0x7f4d917935de in \_ZN11MessageLoop7RunTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#5 0x7f4d91793cc9 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#6 0x7f4d91794e8a in \_ZN11MessageLoop6DoWorkEv sysinfo.cc:0  

#7 0x7f4d9179e997 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE sysinfo.cc:0  

#8 0x7f4d9179230b in \_ZN11MessageLoop11RunInternalEv sysinfo.cc:0  

#9 0x7f4d917907c9 in \_ZN11MessageLoop3RunEv sysinfo.cc:0  

#10 0x7f4d918090c8 in \_ZN4base6Thread10ThreadMainEv sysinfo.cc:0  

#11 0x7f4d91807efc in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv base/threading/platform\_thread\_posix.cc:0  

#12 0x7f4d96a51f75 in \_ZN10AsanThread11ThreadStartEv /usr/local/google/asan/address-sanitizer/asan/asan\_thread.cc:102  

#13 0x7f4d8bc518ba in start\_thread /home/aurel32/eglibc/eglibc-2.11.2/nptl/pthread\_create.c:300  

#14 0x7f4d89dd802d in ?? /home/aurel32/eglibc/eglibc-2.11.2/misc/../sysdeps/unix/sysv/linux/x86\_64/clone.S:114  

[26270:26440:29543271666:ERROR:platform\_thread\_posix.cc(253)] Not implemented reached in static void base::PlatformThread::SetThreadPriority(PlatformThreadHandle, base::ThreadPriority)  

0x7f4d053a6200 is located 384 bytes to the right of 4096-byte region [0x7f4d053a5080,0x7f4d053a6080)  

allocated by thread T92 here:  

#0 0x7f4d96a47bcd in posix\_memalign *asan\_rtl*  

#1 0x7f4d81ab290b in av\_malloc ??:0  

#2 0x7f4d819dc4cb in vorbis\_decode\_init third\_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:0  

#3 0x7f4d819d5c8b in avcodec\_open2 ??:0  

#4 0x7f4d9697c31d in \_ZN5media18FFmpegAudioDecoder12DoInitializeERK13scoped\_refptrINS\_13DemuxerStreamEERKN4base8CallbackIFvvEEERKNS7\_IFvRKNS\_18PipelineStatisticsEEEE sysinfo.cc:0  

#5 0x7f4d9697f175 in \_ZN4base8internal8Invoker4ILb0ENS0\_15InvokerStorage4IMN5media18FFmpegAudioDecoderEFvRK13scoped\_refptrINS3\_13DemuxerStreamEERKNS\_8CallbackIFvvEEERKNSA\_IFvRKNS3\_18PipelineStatisticsEEEEEPS4\_S7\_SC\_SJ\_EESN\_E8DoInvokeEPNS0\_18InvokerStorageBaseE sysinfo.cc:0  

#6 0x7f4d917935de in \_ZN11MessageLoop7RunTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#7 0x7f4d91793cc9 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#8 0x7f4d91794e8a in \_ZN11MessageLoop6DoWorkEv sysinfo.cc:0  

#9 0x7f4d9179e997 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE sysinfo.cc:0  

#10 0x7f4d9179230b in \_ZN11MessageLoop11RunInternalEv sysinfo.cc:0  

#11 0x7f4d917907c9 in \_ZN11MessageLoop3RunEv sysinfo.cc:0  

#12 0x7f4d918090c8 in \_ZN4base6Thread10ThreadMainEv sysinfo.cc:0  

#13 0x7f4d91807efc in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv base/threading/platform\_thread\_posix.cc:0  

#14 0x7f4d96a51f75 in \_ZN10AsanThread11ThreadStartEv /usr/local/google/asan/address-sanitizer/asan/asan\_thread.cc:102  

Thread T92 created by T0 here:  

#0 0x7f4d96a47274 in pthread\_create *asan\_rtl*  

#1 0x7f4d91807cc9 in \_ZN4base12\_GLOBAL\_\_N\_112CreateThreadEmbPNS\_14PlatformThread8DelegateEPm base/threading/platform\_thread\_posix.cc:0  

#2 0x7f4d91807bca in \_ZN4base14PlatformThread6CreateEmPNS0\_8DelegateEPm sysinfo.cc:0  

#3 0x7f4d9180890d in \_ZN4base6Thread16StartWithOptionsERKNS0\_7OptionsE sysinfo.cc:0  

#4 0x7f4d91808693 in \_ZN4base6Thread5StartEv sysinfo.cc:0  

#5 0x7f4d963aaade in \_ZN5media22MessageLoopFactoryImpl14GetMessageLoopERKSs sysinfo.cc:0  

#6 0x7f4d967c8a09 in \_ZN11webkit\_glue18WebMediaPlayerImpl10InitializeEPN6WebKit8WebFrameEb13scoped\_refptrINS\_16WebVideoRendererEE sysinfo.cc:0  

#7 0x7f4d95ee3c0a in \_ZN14RenderViewImpl17createMediaPlayerEPN6WebKit8WebFrameEPNS0\_20WebMediaPlayerClientE sysinfo.cc:0  

#8 0x7f4d92f4b6a0 in \_ZN6WebKit24WebMediaPlayerClientImpl12loadInternalEv sysinfo.cc:0  

#9 0x7f4d93719045 in \_ZN7WebCore11MediaPlayer23loadWithNextMediaEngineEPNS\_18MediaPlayerFactoryE sysinfo.cc:0  

#10 0x7f4d937181e1 in \_ZN7WebCore11MediaPlayer4loadERKN3WTF6StringERKNS\_11ContentTypeE sysinfo.cc:0  

#11 0x7f4d9347ece6 in \_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE sysinfo.cc:0  

#12 0x7f4d9347d707 in \_ZN7WebCore16HTMLMediaElement19selectMediaResourceEv sysinfo.cc:0  

#13 0x7f4d9347bc4a in \_ZN7WebCore16HTMLMediaElement12loadInternalEv sysinfo.cc:0  

#14 0x7f4d936938d8 in \_ZN7WebCore12ThreadTimers24sharedTimerFiredInternalEv sysinfo.cc:0  

#15 0x7f4d91805cf9 in \_ZN4base6subtle18TaskClosureAdapter3RunEv sysinfo.cc:0  

#16 0x7f4d917935de in \_ZN11MessageLoop7RunTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#17 0x7f4d91793cc9 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKNS\_11PendingTaskE sysinfo.cc:0  

#18 0x7f4d91794e8a in \_ZN11MessageLoop6DoWorkEv sysinfo.cc:0  

#19 0x7f4d9179e997 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE sysinfo.cc:0  

#20 0x7f4d9179230b in \_ZN11MessageLoop11RunInternalEv sysinfo.cc:0  

#21 0x7f4d917907c9 in \_ZN11MessageLoop3RunEv sysinfo.cc:0  

#22 0x7f4d95f36563 in \_Z12RendererMainRK18MainFunctionParams sysinfo.cc:0  

#23 0x7f4d915bab23 in \_ZN12\_GLOBAL\_\_N\_123RunNamedProcessTypeMainERKSsRK18MainFunctionParamsPN7content19ContentMainDelegateE content/app/content\_main.cc:0  

#24 0x7f4d915ba070 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE sysinfo.cc:0  

#25 0x7f4d8ff093f7 in ChromeMain ??:0  

#26 0x7f4d8ff0864b in main sysinfo.cc:0  

#27 0x7f4d89d27c4d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.2/csu/libc-start.c:260  

==26270== ABORTING  

Shadow byte and word:  

0x1fe9a0a74c40: fa  

0x1fe9a0a74c40: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1fe9a0a74c20: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c28: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c30: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c38: fa fa fa fa fa fa fa fa  

=>0x1fe9a0a74c40: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c48: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c50: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c58: fa fa fa fa fa fa fa fa  

0x1fe9a0a74c60: fa fa fa fa fa fa fa fa

## Attachments

- [oobr-vorbis-2.webm](attachments/oobr-vorbis-2.webm) (application/octet-stream; charset=binary, 766.3 KB)

## Timeline

### ao...@gmail.com (2011-10-25)

I'm actually not sure if the patch of http://code.google.com/p/chromium/issues/detail?id=100543 was on the test machine yet. Better check with it before looking further because this might be another manifestation of the same bug.

### sc...@gmail.com (2011-10-25)

[Empty comment from Monorail migration]

### kc...@chromium.org (2011-10-25)

Aki, you may also want to run the log through c++filt to get human readable function names. 

The log with line numbers: 

READ of size 4 at 0x7fa6c4e76200 thread T5                                                                                                                                                          
    #0 0x7fa6c55bd3c5 in vorbis_residue_decode_internal third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:1406                                                                               
    #1 0x7fa6c55b0101 in avcodec_decode_audio3 third_party/ffmpeg/patched-ffmpeg/libavcodec/utils.c:823                                                                                             
    #2 0x7fa6daaf7cd6 in media::FFmpegAudioDecoder::DoDecodeBuffer(scoped_refptr<media::Buffer> const&) media/filters/ffmpeg_audio_decoder.cc:193   

0x7fa6c4e76200 is located 384 bytes to the right of 4096-byte region [0x7fa6c4e75080,0x7fa6c4e76080)                                                                                                
allocated by thread T5 here:                                                                                                                                                                        
    #0 0x7fa6dabd032d in posix_memalign _asan_rtl_                                                                                                                                                  
    #1 0x7fa6c568ef3b in av_malloc third_party/ffmpeg/patched-ffmpeg/libavutil/mem.c:90                                                                                                             
    #2 0x7fa6c55b561b in vorbis_parse_id_hdr third_party/ffmpeg/patched-ffmpeg/libavcodec/vorbisdec.c:938                                                                                           
    #3 0x7fa6c55aedfb in avcodec_open2 third_party/ffmpeg/patched-ffmpeg/libavcodec/utils.c:645                                           

### sc...@gmail.com (2011-10-26)

Ugly.

    vec[voffs + k + l * step] += codebook.codevectors[coffs + l];  // FPMATH

So the OOB read is followed immediately by an OOB write, courtesy of the += operator. That's a nasty heap corruption and definitely a different bug.

Investigating.

### sc...@gmail.com (2011-10-28)

Nice catch Aki!
crrev.com/107662

### sc...@gmail.com (2011-10-28)

Still needs DEPS roll etc.

### bu...@chromium.org (2011-10-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=107662

------------------------------------------------------------------------
r107662 | cevans@chromium.org | Thu Oct 27 17:13:50 PDT 2011

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/48_vorbis_residue_buffer.patch?r1=107662&r2=107661&pathrev=107662
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vorbisdec.c?r1=107662&r2=107661&pathrev=107662
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=107662&r2=107661&pathrev=107662
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=107662&r2=107661&pathrev=107662

Fix vorbis decoder bug.

BUG=101458
Review URL: http://codereview.chromium.org/8413019
------------------------------------------------------------------------

### bu...@chromium.org (2011-10-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=107826

------------------------------------------------------------------------
r107826 | cevans@chromium.org | Fri Oct 28 16:33:24 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/source/patched-ffmpeg/libavcodec/vorbisdec.c?r1=107826&r2=107825&pathrev=107826
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/to_upstream/49_vorbis_buffer_defense.patch?r1=107826&r2=107825&pathrev=107826
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/README.chromium?r1=107826&r2=107825&pathrev=107826
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/patches/README?r1=107826&r2=107825&pathrev=107826

An additional defense in the Vorbis codec.

BUG=101458
Review URL: http://codereview.chromium.org/8414025
------------------------------------------------------------------------

### bu...@chromium.org (2011-11-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=108385

------------------------------------------------------------------------
r108385 | scherkus@chromium.org | Wed Nov 02 18:14:16 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=108385&r2=108384&pathrev=108385

Rolling FFmpeg to r108357.

TBR=cevans
BUG=101458

Review URL: http://codereview.chromium.org/8439065
------------------------------------------------------------------------

### sc...@gmail.com (2011-11-05)

As I mentioned earlier: great bug Aki! Reliable repro and a nasty heap buffer overflow which we're really glad to be without. A clear $1000 Chromium Security Reward.

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

@scarybeasts Excellent \o/ I was in a hurry to find as many video-handling bugs as possible, and thought these would only be rewarded on the $500-level due to large repros.

### sc...@gmail.com (2011-11-05)

@aohelin: hehe. We're less strict about the size of video files. They're not nearly as feasible to reduce. So as long as the file reliably demonstrates the issue, that's fine. Video bugs / fixes also tend to be less state-induced than WebKit bugs so the large repro typically doesn't hamper diagnosis.

### sc...@gmail.com (2011-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-11-23)

Payment in system.

### bu...@chromium.org (2011-12-21)

[Comment Deleted]

### sc...@gmail.com (2012-01-08)

Opening access as requested.

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/101458?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050431)*
