# chrome!std::_Tree<std::_Tmap_traits<tracked_objects::Location,tracked_objects::Births *,std::less<tracked_objects::Location>,std::allocator<std::pair<tracked_objects::Location const ,tracked_objects::Births *> >,0> >::find+15 - crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40076363](https://issues.chromium.org/issues/40076363) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media>FFmpeg |
| **Reporter** | sl...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-09-27 |
| **Bounty** | $2,000.00 |

## Description

Crashes on linux stable 21.0.1180.89 (154005), windows dev 23.0.1271.6 (158449) and canary 24.0.1279.0 (158985).

To reproduce open crash1.mp3 in chrome.

(b78.1074): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00000012 ebx=01a201a2 ecx=00000002 edx=000011ff esi=01a201a2 edi=01a201a2
eip=01a201a2 esp=03c4f460 ebp=01a201a2 iopl=0         nv up ei pl nz ac pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010216
01a201a2 ??              ???

ExceptionAddress: 01a201a2
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 01a201a2
Attempt to execute non-executable address 01a201a2

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
03c4f45c 038e0060 0x1a201a2
03c4f474 582fb0f4 0x38e0060
03c4f4a0 038e0060 chrome_582e0000!std::_Tree<std::_Tmap_traits<tracked_objects::Location,tracked_objects::Births *,std::less<tracked_objects::Location>,std::allocator<std::pair<tracked_objects::Location const ,tracked_objects::Births *> >,0> >::find+0x15
03c4f4a8 582fb801 0x38e0060
03c4f528 582fab79 chrome_582e0000!MessageLoop::AddToIncomingQueue+0x144
03c4f594 582faafe chrome_582e0000!MessageLoop::PostDelayedTask+0x60
03c4f604 582fc6ff chrome_582e0000!base::MessageLoopProxyImpl::PostDelayedTask+0x37
03c4f61c 59c25f84 chrome_582e0000!base::internal::CallbackBase::~CallbackBase+0x13
03c4f778 59c24473 chrome_582e0000!media::FFmpegAudioDecoder::DoDecodeBuffer+0x24c
03c4f788 59c2457c chrome_582e0000!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall media::FFmpegVideoDecoder::*)(enum media::Decryptor::Status,scoped_refptr<media::DecoderBuffer> const &)>,void __cdecl(media::FFmpegVideoDecoder * const &,enum media::Decryptor::Status const &,media::DecoderBuffer *)>::MakeItSo+0x29
03c4f7a4 58307d54 chrome_582e0000!base::internal::Invoker<3,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall media::FFmpegVideoDecoder::*)(enum media::Decryptor::Status,scoped_refptr<media::DecoderBuffer> const &)>,void __cdecl(media::FFmpegVideoDecoder *,enum media::Decryptor::Status,scoped_refptr<media::DecoderBuffer> const &),void __cdecl(media::FFmpegVideoDecoder *,enum media::Decryptor::Status,scoped_refptr<media::DecoderBuffer>)>,void __cdecl(media::FFmpegVideoDecoder *,enum media::Decryptor::Status,scoped_refptr<media::DecoderBuffer> const &)>::Run+0x1c
03c4f800 58307ad1 chrome_582e0000!MessageLoop::RunTask+0x1eb
03c4f918 583080e0 chrome_582e0000!MessageLoop::DoWork+0x271
03c4f944 5830779c chrome_582e0000!base::MessagePumpDefault::Run+0xc1
03c4f968 583076f4 chrome_582e0000!MessageLoop::RunInternal+0x72
03c4f97c 583085d9 chrome_582e0000!base::RunLoop::Run+0x59
03c4f9a4 5830846b chrome_582e0000!base::Thread::Run+0x34
03c4fad4 583083cd chrome_582e0000!base::Thread::ThreadMain+0x97
03c4fae0 773eed6c chrome_582e0000!base::`anonymous namespace'::ThreadFunc+0x1a
03c4faec 778a377b kernel32!BaseThreadInitThunk+0xe
03c4fb2c 778a374e ntdll!__RtlUserThreadStart+0x70
03c4fb44 00000000 ntdll!_RtlUserThreadStart+0x1b

## Attachments

- [crash1.mp3](attachments/crash1.mp3) (application/octet-stream; charset=binary, 49.0 KB)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 3.1 KB)

## Timeline

### [Deleted User] (2012-09-27)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-09-27)

Looking.

### da...@chromium.org (2012-09-27)

ASAN trace from ToT Linux Debug:

=================================================================
==10083== ERROR: AddressSanitizer stack-buffer-overflow on address 0x7f84141deaa0 at pc 0x7f8414cdef6f bp 0x7f84141dd130 sp 0x7f84141dd128
WRITE of size 2 at 0x7f84141deaa0 thread T3
    #0 0x7f8414cdef6e in exponents_from_scale_factors /out/Debug/../../third_party/ffmpeg/libavcodec/mpegaudiodec.c:810
    #1 0x7f8414ccf556 in decode_frame /out/Debug/../../third_party/ffmpeg/libavcodec/mpegaudiodec.c:1690
    #2 0x7f8414f89a8b in avcodec_decode_audio4 /out/Debug/../../third_party/ffmpeg/libavcodec/utils.c:1640
    #3 0x7f842d97ad88 in media::FFmpegAudioDecoder::DoDecodeBuffer(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&) /out/Debug/../../media/filters/ffmpeg_audio_decoder.cc:249
    #4 0x7f842d986803 in base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>::Run(media::FFmpegAudioDecoder*, media::DemuxerStream::Status const&, scoped_refptr<media::DecoderBuffer> const&) /out/Debug/../../base/bind_internal.h:248
    #5 0x7f842d98626b in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, void (media::FFmpegAudioDecoder* const&, media::DemuxerStream::Status const&, media::DecoderBuffer*)>::MakeItSo(base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, media::FFmpegAudioDecoder* const&, media::DemuxerStream::Status const&, media::DecoderBuffer*) /out/Debug/../../base/bind_internal.h:928
    #6 0x7f842d985da9 in base::internal::Invoker<3, base::internal::BindState<base::internal::RunnableAdapter<void (media::FFmpegAudioDecoder::*)(media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>, void (media::FFmpegAudioDecoder*, media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&), void (media::FFmpegAudioDecoder*, media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer>)>, void (media::FFmpegAudioDecoder*, media::DemuxerStream::Status, scoped_refptr<media::DecoderBuffer> const&)>::Run(base::internal::BindStateBase*) /out/Debug/../../base/bind_internal.h:1386
    #7 0x7f842c9a36ac in base::Callback<void ()>::Run() const /out/Debug/../../base/callback.h:389
    #8 0x7f842cbc5b2d in MessageLoop::RunTask(base::PendingTask const&) /out/Debug/../../base/message_loop.cc:470
    #9 0x7f842cbc799a in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /out/Debug/../../base/message_loop.cc:482
    #10 0x7f842cbc8055 in MessageLoop::DoWork() /out/Debug/../../base/message_loop.cc:661
    #11 0x7f842cc1b22b in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /out/Debug/../../base/message_pump_default.cc:28
    #12 0x7f842cbc3d59 in MessageLoop::RunInternal() /out/Debug/../../base/message_loop.cc:427
    #13 0x7f842cbc37e6 in MessageLoop::RunHandler() /out/Debug/../../base/message_loop.cc:400
    #14 0x7f842cd8c571 in base::RunLoop::Run() /out/Debug/../../base/run_loop.cc:45
    #15 0x7f842cbc146a in MessageLoop::Run() /out/Debug/../../base/message_loop.cc:307
    #16 0x7f842cfd0d4c in base::Thread::Run(MessageLoop*) /out/Debug/../../base/threading/thread.cc:133
    #17 0x7f842cfd14b7 in base::Thread::ThreadMain() /out/Debug/../../base/threading/thread.cc:169
    #18 0x7f842cf6d00e in base::(anonymous namespace)::ThreadFunc(void*) /out/Debug/../../base/threading/platform_thread_posix.cc:65
    #19 0x685dfa in __asan::AsanThread::ThreadStart() ??:0
Address 0x7f84141deaa0 is located at offset 4096 in frame <mp_decode_frame> of T3's stack:
  This frame has 8 object(s):
    [32, 224) 'scale_factors.i61'
    [256, 320) 'allocation.i'
    [352, 416) 'scale_factors.i'
    [448, 460) 'non_zero_found_short.i.i'
    [512, 2816) 'tmp.i.i'
    [2848, 2896) 'out2.i.i'
    [2944, 4096) 'exponents.i'
    [4128, 4144) 'slen406.i'
HINT: this may be a false positive if your program uses some custom stack unwind mechanism
      (longjmp and C++ exceptions *are* supported)
Thread T3 created by T0 here:
    #0 0x67f454 in __interceptor_pthread_create ??:0
    #1 0x7f842cf6bddc in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) /out/Debug/../../base/threading/platform_thread_posix.cc:127
    #2 0x7f842cf6b5b7 in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) /out/Debug/../../base/threading/platform_thread_posix.cc:247
    #3 0x7f842cfcfe89 in base::Thread::StartWithOptions(base::Thread::Options const&) /out/Debug/../../base/threading/thread.cc:74
    #4 0x7f842cfcf800 in base::Thread::Start() /out/Debug/../../base/threading/thread.cc:63
    #5 0x7f842d77347a in media::MessageLoopFactory::GetThread(media::MessageLoopFactory::Type) /out/Debug/../../media/base/message_loop_factory.cc:46
    #6 0x7f842d772bf2 in media::MessageLoopFactory::GetMessageLoop(media::MessageLoopFactory::Type) /out/Debug/../../media/base/message_loop_factory.cc:25
    #7 0x4a9f78 in base::internal::RunnableAdapter<scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory::*)(media::MessageLoopFactory::Type)>::Run(media::MessageLoopFactory*, media::MessageLoopFactory::Type const&) /out/Debug/../../base/bind_internal.h:190
    #8 0x4a9989 in base::internal::InvokeHelper<false, scoped_refptr<base::MessageLoopProxy>, base::internal::RunnableAdapter<scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory::*)(media::MessageLoopFactory::Type)>, void (media::MessageLoopFactory*, media::MessageLoopFactory::Type const&)>::MakeItSo(base::internal::RunnableAdapter<scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory::*)(media::MessageLoopFactory::Type)>, media::MessageLoopFactory*, media::MessageLoopFactory::Type const&) /out/Debug/../../base/bind_internal.h:890
    #9 0x4a94ce in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory::*)(media::MessageLoopFactory::Type)>, scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory*, media::MessageLoopFactory::Type), void (base::internal::UnretainedWrapper<media::MessageLoopFactory>, media::MessageLoopFactory::Type)>, scoped_refptr<base::MessageLoopProxy> (media::MessageLoopFactory*, media::MessageLoopFactory::Type)>::Run(base::internal::BindStateBase*) /out/Debug/../../base/bind_internal.h:1256
    #10 0x7f842d980197 in base::Callback<scoped_refptr<base::MessageLoopProxy> ()>::Run() const /out/Debug/../../base/callback.h:389
    #11 0x7f842d973a53 in media::FFmpegAudioDecoder::Initialize(scoped_refptr<media::DemuxerStream> const&, base::Callback<void (media::PipelineStatus)> const&, base::Callback<void (media::PipelineStatistics const&)> const&) /out/Debug/../../media/filters/ffmpeg_audio_decoder.cc:60
    #12 0x7f842d7ada3b in media::Pipeline::InitializeAudioDecoder(base::Callback<void (media::PipelineStatus)> const&) /out/Debug/../../media/base/pipeline.cc:898
    #13 0x7f842d7ab822 in media::Pipeline::StateTransitionTask(media::PipelineStatus) /out/Debug/../../media/base/pipeline.cc:468
    #14 0x7f842d7f656a in base::internal::RunnableAdapter<void (media::Pipeline::*)(media::PipelineStatus)>::Run(media::Pipeline*, media::PipelineStatus const&) /out/Debug/../../base/bind_internal.h:190
    #15 0x7f842d7f6187 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (media::Pipeline::*)(media::PipelineStatus)>, void (media::Pipeline* const&, media::PipelineStatus const&)>::MakeItSo(base::internal::RunnableAdapter<void (media::Pipeline::*)(media::PipelineStatus)>, media::Pipeline* const&, media::PipelineStatus const&) /out/Debug/../../base/bind_internal.h:898
    #16 0x7f842d7fa4d4 in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (media::Pipeline::*)(media::PipelineStatus)>, void (media::Pipeline*, media::PipelineStatus), void (media::Pipeline*, media::PipelineStatus)>, void (media::Pipeline*, media::PipelineStatus)>::Run(base::internal::BindStateBase*) /out/Debug/../../base/bind_internal.h:1256
    #17 0x7f842c9a36ac in base::Callback<void ()>::Run() const /out/Debug/../../base/callback.h:389
    #18 0x7f842cbc5b2d in MessageLoop::RunTask(base::PendingTask const&) /out/Debug/../../base/message_loop.cc:470
    #19 0x7f842cbc799a in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /out/Debug/../../base/message_loop.cc:482
    #20 0x7f842cbc8055 in MessageLoop::DoWork() /out/Debug/../../base/message_loop.cc:661
    #21 0x7f842cc1b22b in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /out/Debug/../../base/message_pump_default.cc:28
    #22 0x7f842cbc3d59 in MessageLoop::RunInternal() /out/Debug/../../base/message_loop.cc:427
    #23 0x7f842cbc37e6 in MessageLoop::RunHandler() /out/Debug/../../base/message_loop.cc:400
    #24 0x7f842cd8c571 in base::RunLoop::Run() /out/Debug/../../base/run_loop.cc:45
    #25 0x7f842cbc146a in MessageLoop::Run() /out/Debug/../../base/message_loop.cc:307
    #26 0x48e545 in media::PipelineIntegrationTestBase::Start(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, media::PipelineStatus) /out/Debug/../../media/filters/pipeline_integration_test_base.cc:100
    #27 0x48f11f in media::PipelineIntegrationTestBase::Start(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, media::PipelineStatus, bool) /out/Debug/../../media/filters/pipeline_integration_test_base.cc:108
    #28 0x424ca7 in media::FFmpegRegressionTest_BasicPlayback_Test::TestBody() /out/Debug/../../media/ffmpeg/ffmpeg_regression_tests.cc:336
    #29 0x5c0df2 in void testing::internal::HandleSehExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) /out/Debug/../../testing/gtest/src/gtest.cc:2071
    #30 0x56bef7 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) /out/Debug/../../testing/gtest/src/gtest.cc:2123
    #31 0x5373cd in testing::Test::Run() /out/Debug/../../testing/gtest/src/gtest.cc:2142
    #32 0x539c19 in testing::TestInfo::Run() /out/Debug/../../testing/gtest/src/gtest.cc:2319
    #33 0x53bda7 in testing::TestCase::Run() /out/Debug/../../testing/gtest/src/gtest.cc:2426
    #34 0x55266c in testing::internal::UnitTestImpl::RunAllTests() /out/Debug/../../testing/gtest/src/gtest.cc:4249
    #35 0x5a2092 in bool testing::internal::HandleSehExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl*, bool (testing::internal::UnitTestImpl::*)(), char const*) /out/Debug/../../testing/gtest/src/gtest.cc:2071
    #36 0x578096 in bool testing::internal::HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool>(testing::internal::UnitTestImpl*, bool (testing::internal::UnitTestImpl::*)(), char const*) /out/Debug/../../testing/gtest/src/gtest.cc:2123
    #37 0x550ec2 in testing::UnitTest::Run() /out/Debug/../../testing/gtest/src/gtest.cc:3882
    #38 0x662e46 in base::TestSuite::Run() /out/Debug/../../base/test/test_suite.cc:199
    #39 0x419abd in main /out/Debug/../../media/base/run_all_unittests.cc:27
    #40 0x7f842840776c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
Shadow byte and word:
  0x1ff08283bd54: f2
  0x1ff08283bd50: 00 00 00 00 f2 f2 f2 f2
More shadow bytes:
  0x1ff08283bd30: 00 00 00 00 00 00 00 00
  0x1ff08283bd38: 00 00 00 00 00 00 00 00
  0x1ff08283bd40: 00 00 00 00 00 00 00 00
  0x1ff08283bd48: 00 00 00 00 00 00 00 00
=>0x1ff08283bd50: 00 00 00 00 f2 f2 f2 f2
  0x1ff08283bd58: 00 00 f4 f4 f3 f3 f3 f3
  0x1ff08283bd60: 00 00 00 00 00 00 00 00
  0x1ff08283bd68: 00 00 00 00 00 00 00 00
  0x1ff08283bd70: 00 00 00 00 00 00 00 00
Stats: 2M malloced (6M for red zones) by 20145 calls
Stats: 0M realloced by 3533 calls
Stats: 1M freed by 13844 calls
Stats: 0M really freed by 0 calls
Stats: 48M (12295 full pages) mmaped in 12 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16;
  mallocs by size class: 8:17951; 9:830; 10:869; 11:243; 12:154; 13:56; 14:24; 15:10; 16:6; 17:1; 18:1;
  frees   by size class: 8:12372; 9:495; 10:748; 11:140; 12:28; 13:40; 14:13; 15:2; 16:4; 17:1; 18:1;
  rfrees  by size class:
Stats: malloc large: 2 small slow: 86
==10083== ABORTING


### da...@chromium.org (2012-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-27)

Eh, a stack corruption in the core mpeg decode routines? You've got to be kidding me :)

Nice bug @slaweck.

### da...@chromium.org (2012-09-27)

I have a fix, but it's pretty gnarly since unfortunately the array in question is passed all over the place without any bounds checks.

I've passed on the bug to FFmpeg and LibAV upstream and will see if they come back with something less offensive :) ETA is usually < 24 hours.

+rbultje as an FYI since I forgot to include him on the libav mail.

### [Deleted User] (2012-09-27)

In ff_compute_band_indexes():

            /* if switched mode, we handle the 36 first samples as
                long blocks.  For 8000Hz, we handle the 72 first
                exponents as long blocks */
            if (s->sample_rate_index <= 2)
                g->long_end = 8;
            else
                g->long_end = 6;

            g->short_start = 2 + (s->sample_rate_index != 8);

If sample_rate_index == 8, then short_start = 2 and long_end= 6.

static void exponents_from_scale_factors(MPADecodeContext *s, GranuleDef *g,
                                         int16_t *exponents)
{
    const uint8_t *bstab, *pretab;
    int len, i, j, k, l, v0, shift, gain, gains[3];
    int16_t *exp_ptr;

    exp_ptr = exponents;
    gain    = g->global_gain - 210;
    shift   = g->scalefac_scale + 1;

    bstab  = band_size_long[s->sample_rate_index];
    pretab = mpa_pretab[g->preflag];
    for (i = 0; i < g->long_end; i++) {
        v0 = gain - ((g->scale_factors[i] + pretab[i]) << shift) + 400;
        len = bstab[i];
        for (j = len; j > 0; j--)
            *exp_ptr++ = v0;
    }

    if (g->short_start < 13) {
        bstab    = band_size_short[s->sample_rate_index];
        gains[0] = gain - (g->subblock_gain[0] << 3);
        gains[1] = gain - (g->subblock_gain[1] << 3);
        gains[2] = gain - (g->subblock_gain[2] << 3);
        k        = g->long_end;
        for (i = g->short_start; i < 13; i++) {
            len = bstab[i];
            for (l = 0; l < 3; l++) {
                v0 = gains[l] - (g->scale_factors[k++] << shift) + 400;
                for (j = len; j > 0; j--)
                    *exp_ptr++ = v0;
            }
        }
    }
}

band_size_long[8][0-5] is 6x12, so that's 72, and band_size_short[8][2-12] is a sum of 176, but (576-72)/3=168, i.e. it overflows by 8x3=24shorts=48bytes. It looks like the table values or the indices set in ff_compute_band_indexes() are wrong, and this looks related to the recent fixing of 8kHz MP3, since sample_rate_index==8 means 8kHz. I'll ask Kostya if he can give any insight in this.

### [Deleted User] (2012-09-27)

bash-3.2$ git diff
diff --git a/libavcodec/mpegaudiodec.c b/libavcodec/mpegaudiodec.c
index 03094f6..ead0e1d 100644
--- a/libavcodec/mpegaudiodec.c
+++ b/libavcodec/mpegaudiodec.c
@@ -211,7 +211,7 @@ static void ff_compute_band_indexes(MPADecodeContext *s, Gra
             else
                 g->long_end = 6;
 
-            g->short_start = 2 + (s->sample_rate_index != 8);
+            g->short_start = 3;
         } else {
             g->long_end    = 0;
             g->short_start = 0;


That fixes the overrun and doesn't break any part of the mp3 testsuite that I can find. I'm not sure if it's functionally correct, trying to get Kostya's opinion on that.

### da...@chromium.org (2012-09-28)

That is the same fix that Michael just committed to FFmpeg. Did you ever hear back from Kostya?

### da...@chromium.org (2012-09-28)

FTR the mp3 from https://crbug.com/chromium/69730 sounds fine with that fix.

### [Deleted User] (2012-09-28)

I tested that, and the problem is that that file doesn't actually trigger the codepath at all (block_type == 2 && switch_point). So I can't say for sure if that is actually correct or not, and don't have access to the specs to confirm. I was hoping Kostya could clear that up for me (he apparently has specs), but no response so far. If you want to commit that fix, go for it. I can submit it also, let me know if you prefer that and I'll get on it tonight.

### da...@chromium.org (2012-09-28)

Looks like Luca, Kostya, Michael, and you all agree this is the right fix according to the latest emails.  I'll merge that fix into trunk. Luckily FFmpeg didn't get rolled for M23, so I can rebuild the binaries for M22, M23, M24 in one go.

@inferno: I assume yes due to pwnium, but to confirm you want this in M22?

### sc...@gmail.com (2012-09-28)

@dalecurtis: I think the M22 patch for Pwnium has already been closed down, but no harm merging the fix to some subsequent M22 patch, assuming the fix doesn't regress anything in the M23 beta builds.

### [Deleted User] (2012-09-28)

Wouldn't it be nice if you didn't have to roll binaries anymore and the Windows build just worked automagically? :-).

### bu...@chromium.org (2012-09-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=159352

------------------------------------------------------------------------
r159352 | dalecurtis@google.com | 2012-09-28T22:28:18.340596Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=159352&r2=159351&pathrev=159352
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/pipeline_integration_test_base.cc?r1=159352&r2=159351&pathrev=159352
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_regression_tests.cc?r1=159352&r2=159351&pathrev=159352
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/pipeline_integration_test.cc?r1=159352&r2=159351&pathrev=159352
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/audio/null_audio_sink.cc?r1=159352&r2=159351&pathrev=159352

Roll FFmpeg DEPS + Fixup FFmpeg tests.

Pulls in the security fix for https://crbug.com/chromium/152691 and adds a test for the
problematic file.  Additionally fixes a few issues which have led
to rusting:
- Updates hashes after AudioBus::ToInterleaved() changes.
- Fixes a bunch of EXPECT_CALL failures and log spam since not all
tests will satisfy these expectations due to invalid files.
- Fixes a bug in the hashing code when NullAudioSink is never
initialized.

BUG=152691
TEST=unit tests.

Review URL: https://codereview.chromium.org/10989089
------------------------------------------------------------------------

### da...@chromium.org (2012-09-28)

Landed in M23, M24. Will keep an eye on it and merge to M22 on Monday if all looks good. Since the change only affects 8kHz MP3 audio, and we never really got any complaints when we didn't support it, I don't expect any issues :)

### sc...@gmail.com (2012-09-28)

Thanks Dale, awesome. Actually, can we not merge anything to M22 just now, I think Kerz is in the middle of another M22 release :)
cc: Kerz

### da...@chromium.org (2012-09-28)

Sure thing, I'll keep an eye on the bug if it needs to be merged later.

### sc...@gmail.com (2012-10-02)

Thank you slaweck for this report!
And some good news.
We're rewarding it at $1000 base reward, plus under the new rules, $1000 bonus for finding a bug in an area where we don't see so many bugs any more :)
$2000 total.

### sc...@gmail.com (2012-10-11)

Paid as part of $3000 batch.

@dalecurtis: I believe we're good to merge to M22 now.

### da...@chromium.org (2012-10-11)

This made it in with https://crbug.com/chromium/154200 yesterday.

### in...@chromium.org (2012-10-18)

Can you please merge it to m23 this week.

### da...@chromium.org (2012-10-18)

It's already in M22 and M23. 

### in...@chromium.org (2012-10-18)

Thanks Dale for confirming.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29182

------------------------------------------------------------------------
r29182 | dalecurtis@google.com | 2012-09-28T20:05:03.348401Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29189

------------------------------------------------------------------------
r29189 | dalecurtis@google.com | 2012-09-28T22:28:41.734074Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29191

------------------------------------------------------------------------
r29191 | dalecurtis@google.com | 2012-09-28T22:45:40.977716Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29239

------------------------------------------------------------------------
r29239 | dalecurtis@google.com | 2012-10-01T17:57:10.256547Z

------------------------------------------------------------------------

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/152691?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media>FFmpeg]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076363)*
