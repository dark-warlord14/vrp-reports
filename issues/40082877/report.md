# UNKNOWN in vp8_read_mv_component

| Field | Value |
|-------|-------|
| **Issue ID** | [40082877](https://issues.chromium.org/issues/40082877) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2015-09-17 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36

Example URL:

Steps to reproduce the problem:
1. Open repro.webm

What is the expected behavior?

What went wrong?
Render crash 

Did this work before? N/A 

Is it a problem with Flash or HTML5? N/A

Does this work in other browsers? N/A 

Chrome version: 47.0.2511.0  Channel: canary
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 18.0 r0

I couldn't repro this crash under ASAN windows.

Stack Traces
============

Thread 10 CRASHED [EXCEPTION_ACCESS_VIOLATION_READ @ 0xffffffffa0cf3800 ]MAGIC SIGNATURE THREAD
0x605b40d3      [chrome_child.dll -vp8.c:802 ]  vp8_read_mv_component
0x605acdb2      [chrome_child.dll -vp8.c:2396 ] vp8_decode_mb_row_no_filter
0x605b1992      [chrome_child.dll -vp8.c:2509 ] vp8_decode_mb_row_sliced
0x60553059      [chrome_child.dll -pthread_slice.c:100 ]        worker
0x6053b8cb      [chrome_child.dll -w32pthreads.h:79 ]   win32thread_worker
0x60c3fa42      [chrome_child.dll -threadex.c:376 ]     _callthreadstartex
0x60c3fb6a      [chrome_child.dll -threadex.c:354 ]     _threadstartex
0x76e93c44      [kernel32.dll + 0x00053c44 ]    BaseThreadInitThunk
0x770e37f4      [ntdll.dll + 0x000637f4 ]       __RtlUserThreadStart
0x770e37c7      [ntdll.dll + 0x000637c7 ]       _RtlUserThreadStart

## Attachments

- [repro.webm](attachments/repro.webm) (application/octet-stream, 47.0 KB)

## Timeline

### yi...@chromium.org (2015-09-23)

I don't see chrome crash when download repro.webm and oepn is in Chrome. If you still see the crash, can you provide the report id?

### ch...@gmail.com (2015-09-23)

Crash ID 22e5da5f14cf5761 - I'm still able to repro this crash on stable channel  45.0.2454.99 m and canary channel 47.0.2517.0.



### da...@chromium.org (2015-09-24)

Looks like this got misfiled. +inferno for security notify

Are you setting any special allocators for this crash?

### aj...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-09-25)

I get an access violation on canary 47.0.2517.0

eax=43880000 ebx=0000014b ecx=00000008 edx=03fd8444 esi=08000000 edi=00000203
eip=66e4ebaa esp=05a8fa98 ebp=05a8fab4 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010206
chrome_child!vp8_read_mv_component+0x125:
66e4ebaa 0fb688d09fe267  movzx   ecx,byte ptr chrome_child!ff_vp56_norm_shift (67e29fd0)[eax] ds:0023:ab6a9fd0=??
0:010> k
  *** Stack trace for last set context - .thread/.cxr resets it
ChildEBP RetAddr  
05a8fab4 66e47809 chrome_child!vp8_read_mv_component+0x125 [c:\b\build\slave\win\build\src\third_party\ffmpeg\libavcodec\vp8.c @ 804]
05a8fbf4 66e4c451 chrome_child!vp8_decode_mb_row_no_filter+0x1f57 [c:\b\build\slave\win\build\src\third_party\ffmpeg\libavcodec\vp8.c @ 2398]
05a8fc28 66e2050a chrome_child!vp8_decode_mb_row_sliced+0x6b [c:\b\build\slave\win\build\src\third_party\ffmpeg\libavcodec\vp8.c @ 2511]
05a8fc58 66e08174 chrome_child!worker+0xb1 [c:\b\build\slave\win\build\src\third_party\ffmpeg\libavcodec\pthread_slice.c @ 100]
05a8fc68 674c1552 chrome_child!win32thread_worker+0xd [c:\b\build\slave\win\build\src\third_party\ffmpeg\compat\w32pthreads.h @ 79]
05a8fca0 674c167a chrome_child!_callthreadstartex+0x1b [f:\dd\vctools\crt\crtw32\startup\threadex.c @ 376]
05a8fcac 76663c45 chrome_child!_threadstartex+0x7c [f:\dd\vctools\crt\crtw32\startup\threadex.c @ 354]
WARNING: Stack unwind information not available. Following frames may be wrong.
05a8fcb8 77d237f5 kernel32!BaseThreadInitThunk+0x12
05a8fcf8 77d237c8 ntdll!RtlInitializeExceptionChain+0xef
05a8fd10 00000000 ntdll!RtlInitializeExceptionChain+0xc2



### da...@chromium.org (2015-09-29)

Looks legit, I'm able to reproduce this crash -- trying with an ASAN build.  Can we get this test case added to ClusterFuzz?

### da...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5755369714876416

### cl...@chromium.org (2015-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4520864177979392

### es...@chromium.org (2015-09-30)

dalecurtis: it doesn't look like CF could reproduce, but since you were able to repro, could you help find an appropriate owner for this? 

### da...@chromium.org (2015-09-30)

Thanks, yes I'll take a look. As noted on the duped bug this is actually an issue that was reported a long time ago, but had no repro except in asan builds: https://crbug.com/chromium/447860 -- it looks like that was legit after all or msvc now has a similar codegen issue (unlikely).

I've got a workaround, but the root cause is a race of sorts -- I'll try to build tsan and see what I can figure out.

### da...@chromium.org (2015-09-30)

Tsan spits out the following, will take a look tomorrow.

==================
WARNING: ThreadSanitizer: data race (pid=5322)
  Write of size 4 at 0x7fffc17ab124 by thread T2:
    #0 worker third_party/ffmpeg/libavcodec/pthread_slice.c:99:40 (libffmpeg.so+0x000000279cbb)

  Previous write of size 4 at 0x7fffc17ab124 by thread T3:
    #0 worker third_party/ffmpeg/libavcodec/pthread_slice.c:99:40 (libffmpeg.so+0x000000279cbb)

  Location is stack of main thread.

  Thread T2 (tid=5325, running) created by main thread at:
    #0 pthread_create <null> (ffmpeg_regression_tests+0x00000044bcd1)
    #1 ff_slice_thread_init third_party/ffmpeg/libavcodec/pthread_slice.c:232:12 (libffmpeg.so+0x0000002799ce)
    #2 ff_thread_init third_party/ffmpeg/libavcodec/pthread.c:75:16 (libffmpeg.so+0x0000002767dc)
    #3 avcodec_open2 third_party/ffmpeg/libavcodec/autorename_libavcodec_utils.c:1318:15 (libffmpeg.so+0x00000025557c)
    #4 media::FFmpegVideoDecoder::ConfigureDecoder(bool) media/filters/ffmpeg_video_decoder.cc:357:17 (libmedia.so+0x0000001afbc9)
    #5 media::FFmpegVideoDecoder::Initialize(media::VideoDecoderConfig const&, bool, base::Callback<void (bool)> const&, base::Callback<void (scoped_refptr<media::VideoFrame> const&)> const&) media/filters/ffmpeg_video_decoder.cc:179:35 (libmedia.so+0x0000001af757)
    #6 media::DecoderStreamTraits<(media::DemuxerStream::Type)2>::InitializeDecoder(media::VideoDecoder*, media::DemuxerStream*, base::Callback<void (bool)> const&, base::Callback<void (scoped_refptr<media::VideoFrame> const&)> const&) media/filters/decoder_stream_traits.cc:53:3 (libmedia.so+0x0000001910fe)
    #7 media::DecoderSelector<(media::DemuxerStream::Type)2>::InitializeDecoder() media/filters/decoder_selector.cc:178:3 (libmedia.so+0x00000018434b)
    #8 media::DecoderSelector<(media::DemuxerStream::Type)2>::DecoderInitDone(bool) media/filters/decoder_selector.cc:192:5 (libmedia.so+0x000000184a58)
    #9 Run base/bind_internal.h:176:12 (libmedia.so+0x000000185cb7)
    #10 MakeItSo base/bind_internal.h:303 (libmedia.so+0x000000185cb7)
    #11 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::DecoderSelector<(media::DemuxerStream::Type)2>::*)(bool)>, void (media::DecoderSelector<(media::DemuxerStream::Type)2>*, bool), base::internal::TypeList<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > > >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (media::DecoderSelector<(media::DemuxerStream::Type)2>::*)(bool)>, base::internal::TypeList<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > const&, bool const&> >, void (bool const&)>::Run(base::internal::BindStateBase*, bool const&) base/bind_internal.h:343 (libmedia.so+0x000000185cb7)
    #12 Run base/callback.h:396:12 (libmedia.so+0x00000018f7a1)
    #13 MakeItSo base/bind_internal.h:293 (libmedia.so+0x00000018f7a1)
    #14 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::Callback<void (bool)>, void (bool), base::internal::TypeList<bool> >, base::internal::TypeList<base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<false, void, base::Callback<void (bool)>, base::internal::TypeList<bool const&> >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343 (libmedia.so+0x00000018f7a1)
    #15 Run base/callback.h:396:12 (libbase.so+0x000000086882)
    #16 base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51 (libbase.so+0x000000086882)
    #17 base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3 (libbase.so+0x0000000c4e6d)
    #18 DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5 (libbase.so+0x0000000c5922)
    #19 base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602 (libbase.so+0x0000000c5922)
    #20 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:32:21 (libbase.so+0x0000000c7da5)
    #21 base::MessageLoop::RunHandler() base/message_loop/message_loop.cc:445:3 (libbase.so+0x0000000c4690)
    #22 base::RunLoop::Run() base/run_loop.cc:55:3 (libbase.so+0x0000000ee27a)
    #23 base::MessageLoop::Run() base/message_loop/message_loop.cc:288:3 (libbase.so+0x0000000c329b)
    #24 media::PipelineIntegrationTestBase::Start(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, media::CdmContext*) media/test/pipeline_integration_test_base.cc:146:3 (ffmpeg_regression_tests+0x0000004c8e4c)
    #25 Start media/test/pipeline_integration_test_base.cc:107:10 (ffmpeg_regression_tests+0x0000004ca35a)
    #26 media::PipelineIntegrationTestBase::Start(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned char) media/test/pipeline_integration_test_base.cc:154 (ffmpeg_regression_tests+0x0000004ca35a)
    #27 media::FFmpegRegressionTest_BasicPlayback_Test::TestBody() media/ffmpeg/ffmpeg_regression_tests.cc:335:5 (ffmpeg_regression_tests+0x0000004bed1c)
    #28 HandleExceptionsInMethodIfSupported<testing::Test, void> testing/gtest/src/gtest.cc:2458:12 (ffmpeg_regression_tests+0x000000504f0c)
    #29 testing::Test::Run() testing/gtest/src/gtest.cc:2474 (ffmpeg_regression_tests+0x000000504f0c)
    #30 testing::TestInfo::Run() testing/gtest/src/gtest.cc:2656:5 (ffmpeg_regression_tests+0x000000505e13)
    #31 testing::TestCase::Run() testing/gtest/src/gtest.cc:2774:5 (ffmpeg_regression_tests+0x0000005066f2)
    #32 testing::internal::UnitTestImpl::RunAllTests() testing/gtest/src/gtest.cc:4647:11 (ffmpeg_regression_tests+0x00000050f7ac)
    #33 HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> testing/gtest/src/gtest.cc:2458:12 (ffmpeg_regression_tests+0x00000050f1f6)
    #34 testing::UnitTest::Run() testing/gtest/src/gtest.cc:4255 (ffmpeg_regression_tests+0x00000050f1f6)
    #35 RUN_ALL_TESTS testing/gtest/include/gtest/gtest.h:2237:10 (ffmpeg_regression_tests+0x0000004e0adb)
    #36 base::TestSuite::Run() base/test/test_suite.cc:230 (ffmpeg_regression_tests+0x0000004e0adb)
    #37 Run base/bind_internal.h:176:12 (ffmpeg_regression_tests+0x0000004b1e72)
    #38 MakeItSo base/bind_internal.h:286 (ffmpeg_regression_tests+0x0000004b1e72)
    #39 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<int (base::TestSuite::*)()>, int (base::TestSuite*), base::internal::TypeList<base::internal::UnretainedWrapper<TestSuiteNoAtExit> > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::UnretainedWrapper<TestSuiteNoAtExit> > >, base::internal::InvokeHelper<false, int, base::internal::RunnableAdapter<int (base::TestSuite::*)()>, base::internal::TypeList<TestSuiteNoAtExit*> >, int ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343 (ffmpeg_regression_tests+0x0000004b1e72)
    #40 Run base/callback.h:396:12 (ffmpeg_regression_tests+0x0000004dc5ad)
    #41 base::(anonymous namespace)::LaunchUnitTestsInternal(base::Callback<int ()> const&, int, bool, base::Callback<void ()> const&) base/test/launcher/unit_test_launcher.cc:187 (ffmpeg_regression_tests+0x0000004dc5ad)
    #42 base::LaunchUnitTests(int, char**, base::Callback<int ()> const&) base/test/launcher/unit_test_launcher.cc:426:10 (ffmpeg_regression_tests+0x0000004dc437)
    #43 main media/base/run_all_unittests.cc:59:10 (ffmpeg_regression_tests+0x0000004b1cec)

  Thread T3 (tid=5326, running) created by main thread at:
    #0 pthread_create <null> (ffmpeg_regression_tests+0x00000044bcd1)
    #1 ff_slice_thread_init third_party/ffmpeg/libavcodec/pthread_slice.c:232:12 (libffmpeg.so+0x0000002799ce)
    #2 ff_thread_init third_party/ffmpeg/libavcodec/pthread.c:75:16 (libffmpeg.so+0x0000002767dc)
    #3 avcodec_open2 third_party/ffmpeg/libavcodec/autorename_libavcodec_utils.c:1318:15 (libffmpeg.so+0x00000025557c)
    #4 media::FFmpegVideoDecoder::ConfigureDecoder(bool) media/filters/ffmpeg_video_decoder.cc:357:17 (libmedia.so+0x0000001afbc9)
    #5 media::FFmpegVideoDecoder::Initialize(media::VideoDecoderConfig const&, bool, base::Callback<void (bool)> const&, base::Callback<void (scoped_refptr<media::VideoFrame> const&)> const&) media/filters/ffmpeg_video_decoder.cc:179:35 (libmedia.so+0x0000001af757)
    #6 media::DecoderStreamTraits<(media::DemuxerStream::Type)2>::InitializeDecoder(media::VideoDecoder*, media::DemuxerStream*, base::Callback<void (bool)> const&, base::Callback<void (scoped_refptr<media::VideoFrame> const&)> const&) media/filters/decoder_stream_traits.cc:53:3 (libmedia.so+0x0000001910fe)
    #7 media::DecoderSelector<(media::DemuxerStream::Type)2>::InitializeDecoder() media/filters/decoder_selector.cc:178:3 (libmedia.so+0x00000018434b)
    #8 media::DecoderSelector<(media::DemuxerStream::Type)2>::DecoderInitDone(bool) media/filters/decoder_selector.cc:192:5 (libmedia.so+0x000000184a58)
    #9 Run base/bind_internal.h:176:12 (libmedia.so+0x000000185cb7)
    #10 MakeItSo base/bind_internal.h:303 (libmedia.so+0x000000185cb7)
    #11 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (media::DecoderSelector<(media::DemuxerStream::Type)2>::*)(bool)>, void (media::DecoderSelector<(media::DemuxerStream::Type)2>*, bool), base::internal::TypeList<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > > >, base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > > >, base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (media::DecoderSelector<(media::DemuxerStream::Type)2>::*)(bool)>, base::internal::TypeList<base::WeakPtr<media::DecoderSelector<(media::DemuxerStream::Type)2> > const&, bool const&> >, void (bool const&)>::Run(base::internal::BindStateBase*, bool const&) base/bind_internal.h:343 (libmedia.so+0x000000185cb7)
    #12 Run base/callback.h:396:12 (libmedia.so+0x00000018f7a1)
    #13 MakeItSo base/bind_internal.h:293 (libmedia.so+0x00000018f7a1)
    #14 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::Callback<void (bool)>, void (bool), base::internal::TypeList<bool> >, base::internal::TypeList<base::internal::UnwrapTraits<bool> >, base::internal::InvokeHelper<false, void, base::Callback<void (bool)>, base::internal::TypeList<bool const&> >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343 (libmedia.so+0x00000018f7a1)
    #15 Run base/callback.h:396:12 (libbase.so+0x000000086882)
    #16 base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51 (libbase.so+0x000000086882)
    #17 base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3 (libbase.so+0x0000000c4e6d)
    #18 DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5 (libbase.so+0x0000000c5922)
    #19 base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602 (libbase.so+0x0000000c5922)
    #20 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:32:21 (libbase.so+0x0000000c7da5)
    #21 base::MessageLoop::RunHandler() base/message_loop/message_loop.cc:445:3 (libbase.so+0x0000000c4690)
    #22 base::RunLoop::Run() base/run_loop.cc:55:3 (libbase.so+0x0000000ee27a)
    #23 base::MessageLoop::Run() base/message_loop/message_loop.cc:288:3 (libbase.so+0x0000000c329b)
    #24 media::PipelineIntegrationTestBase::Start(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, media::CdmContext*) media/test/pipeline_integration_test_base.cc:146:3 (ffmpeg_regression_tests+0x0000004c8e4c)
    #25 Start media/test/pipeline_integration_test_base.cc:107:10 (ffmpeg_regression_tests+0x0000004ca35a)
    #26 media::PipelineIntegrationTestBase::Start(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, unsigned char) media/test/pipeline_integration_test_base.cc:154 (ffmpeg_regression_tests+0x0000004ca35a)
    #27 media::FFmpegRegressionTest_BasicPlayback_Test::TestBody() media/ffmpeg/ffmpeg_regression_tests.cc:335:5 (ffmpeg_regression_tests+0x0000004bed1c)
    #28 HandleExceptionsInMethodIfSupported<testing::Test, void> testing/gtest/src/gtest.cc:2458:12 (ffmpeg_regression_tests+0x000000504f0c)
    #29 testing::Test::Run() testing/gtest/src/gtest.cc:2474 (ffmpeg_regression_tests+0x000000504f0c)
    #30 testing::TestInfo::Run() testing/gtest/src/gtest.cc:2656:5 (ffmpeg_regression_tests+0x000000505e13)
    #31 testing::TestCase::Run() testing/gtest/src/gtest.cc:2774:5 (ffmpeg_regression_tests+0x0000005066f2)
    #32 testing::internal::UnitTestImpl::RunAllTests() testing/gtest/src/gtest.cc:4647:11 (ffmpeg_regression_tests+0x00000050f7ac)
    #33 HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> testing/gtest/src/gtest.cc:2458:12 (ffmpeg_regression_tests+0x00000050f1f6)
    #34 testing::UnitTest::Run() testing/gtest/src/gtest.cc:4255 (ffmpeg_regression_tests+0x00000050f1f6)
    #35 RUN_ALL_TESTS testing/gtest/include/gtest/gtest.h:2237:10 (ffmpeg_regression_tests+0x0000004e0adb)
    #36 base::TestSuite::Run() base/test/test_suite.cc:230 (ffmpeg_regression_tests+0x0000004e0adb)
    #37 Run base/bind_internal.h:176:12 (ffmpeg_regression_tests+0x0000004b1e72)
    #38 MakeItSo base/bind_internal.h:286 (ffmpeg_regression_tests+0x0000004b1e72)
    #39 base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<int (base::TestSuite::*)()>, int (base::TestSuite*), base::internal::TypeList<base::internal::UnretainedWrapper<TestSuiteNoAtExit> > >, base::internal::TypeList<base::internal::UnwrapTraits<base::internal::UnretainedWrapper<TestSuiteNoAtExit> > >, base::internal::InvokeHelper<false, int, base::internal::RunnableAdapter<int (base::TestSuite::*)()>, base::internal::TypeList<TestSuiteNoAtExit*> >, int ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:343 (ffmpeg_regression_tests+0x0000004b1e72)
    #40 Run base/callback.h:396:12 (ffmpeg_regression_tests+0x0000004dc5ad)
    #41 base::(anonymous namespace)::LaunchUnitTestsInternal(base::Callback<int ()> const&, int, bool, base::Callback<void ()> const&) base/test/launcher/unit_test_launcher.cc:187 (ffmpeg_regression_tests+0x0000004dc5ad)
    #42 base::LaunchUnitTests(int, char**, base::Callback<int ()> const&) base/test/launcher/unit_test_launcher.cc:426:10 (ffmpeg_regression_tests+0x0000004dc437)
    #43 main media/base/run_all_unittests.cc:59:10 (ffmpeg_regression_tests+0x0000004b1cec)

SUMMARY: ThreadSanitizer: data race third_party/ffmpeg/libavcodec/pthread_slice.c:99:40 in worker


### da...@chromium.org (2015-09-30)

I believe that's https://crbug.com/chromium/448215, so I'll see if that's the underlying root cause.

### da...@chromium.org (2015-09-30)

WARNING: ThreadSanitizer: data race (pid=26112)
  Write of size 4 at 0x7d8c00005508 by thread T3:
    #0 vp56_rac_renorm third_party/ffmpeg/libavcodec/vp56.h:232:15 (libffmpeg.so+0x0000001a1b40)
    #1 vp56_rac_get_prob third_party/ffmpeg/libavcodec/x86/vp56_arith.h:31 (libffmpeg.so+0x0000001a1b40)
    #2 decode_mb_mode third_party/ffmpeg/libavcodec/vp8.c:1190 (libffmpeg.so+0x0000001a1b40)
    #3 decode_mb_row_no_filter third_party/ffmpeg/libavcodec/vp8.c:2340 (libffmpeg.so+0x0000001a1b40)
    #4 vp8_decode_mb_row_no_filter third_party/ffmpeg/libavcodec/vp8.c:2407 (libffmpeg.so+0x0000001a1b40)
    #5 vp78_decode_mb_row_sliced third_party/ffmpeg/libavcodec/vp8.c:2496:9 (libffmpeg.so+0x00000019aebd)
    #6 vp8_decode_mb_row_sliced third_party/ffmpeg/libavcodec/vp8.c:2520 (libffmpeg.so+0x00000019aebd)
    #7 worker third_party/ffmpeg/libavcodec/pthread_slice.c:100:52 (libffmpeg.so+0x0000001d8b3b)

  Previous write of size 4 at 0x7d8c00005508 by thread T2:
    #0 vp56_rac_renorm third_party/ffmpeg/libavcodec/vp56.h:232:15 (libffmpeg.so+0x0000001a1b40)
    #1 vp56_rac_get_prob third_party/ffmpeg/libavcodec/x86/vp56_arith.h:31 (libffmpeg.so+0x0000001a1b40)
    #2 decode_mb_mode third_party/ffmpeg/libavcodec/vp8.c:1190 (libffmpeg.so+0x0000001a1b40)
    #3 decode_mb_row_no_filter third_party/ffmpeg/libavcodec/vp8.c:2340 (libffmpeg.so+0x0000001a1b40)
    #4 vp8_decode_mb_row_no_filter third_party/ffmpeg/libavcodec/vp8.c:2407 (libffmpeg.so+0x0000001a1b40)
    #5 vp78_decode_mb_row_sliced third_party/ffmpeg/libavcodec/vp8.c:2496:9 (libffmpeg.so+0x00000019aebd)
    #6 vp8_decode_mb_row_sliced third_party/ffmpeg/libavcodec/vp8.c:2520 (libffmpeg.so+0x00000019aebd)
    #7 worker third_party/ffmpeg/libavcodec/pthread_slice.c:100:52 (libffmpeg.so+0x0000001d8b3b)

After removing some of the vp8 suppressions from TSANv2 from https://crbug.com/chromium/158718 that race appears, which I think is the culprit for this crash. Still unsure where in the threading it's deciding to operate on the same context though.

### cl...@chromium.org (2015-09-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-09-30)

Upstream couldn't repro, but in typical magic fashion, Michael was able to produce a better patch than mine which fixes the racing issue. It looks like the code was making an "is_threading" type decision based on a combination of user data and thread count. It then trusted the user data over the presence of actual threads, so despite having threads operating on the frames synchronization primitives were not effectively used.

Waiting for confirmation on the full patch from Michael, but will land something shortly.

### da...@chromium.org (2015-10-01)

http://git.videolan.org/?p=ffmpeg.git;a=commit;h=dabea74d0e82ea80cd344f630497cafcb3ef872c pulling in now.

Security team: It might be worth reconsidering the award state for https://crbug.com/chromium/447860.

### ch...@gmail.com (2015-10-01)

Is that means this report not qualified for a chromium security reward?


### da...@chromium.org (2015-10-01)

+mbarbella for c#13, c#19, 

### mb...@chromium.org (2015-10-01)

Given the circumstances, I think it makes sense to send both to the panel. It's ultimately up to the reward panel to decide, but I think it seems reasonable to consider them as separate reports, so this may still be valid.

### da...@chromium.org (2015-10-01)

+chcunningham to handle the merge to M46 while I'm out.

### bu...@chromium.org (2015-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/af0e1b03d563844f7691440bb32fd0d90b60bec6

commit af0e1b03d563844f7691440bb32fd0d90b60bec6
Author: dalecurtis <dalecurtis@chromium.org>
Date: Thu Oct 01 21:28:19 2015

Roll ffmpeg DEPS for security fix.

Pulls in:
525a71a avcodec/vp8: Do not use num_coeff_partitions in thread/buffer setup

BUG=532967
TEST=ffmpeg_regression_tests
TBR=chcunningham

Review URL: https://codereview.chromium.org/1376913003

Cr-Commit-Position: refs/heads/master@{#351889}

[modify] http://crrev.com/af0e1b03d563844f7691440bb32fd0d90b60bec6/DEPS
[modify] http://crrev.com/af0e1b03d563844f7691440bb32fd0d90b60bec6/media/ffmpeg/ffmpeg_regression_tests.cc


### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-10-03)

Unable to reproduce this bug in 47.0.2525.0 canary. Verified.

### ch...@chromium.org (2015-10-05)

Fix looks good - not seeing any new crashes since it landed. Requesting merge back to 46.

### ti...@google.com (2015-10-05)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2015-10-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ti...@chromium.org (2015-10-05)

Merge approved for M46 branch (branch: 2490).

### bu...@chromium.org (2015-10-05)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=79237

------------------------------------------------------------------
r79237 | chcunningham@google.com | 2015-10-05T22:56:03.578892Z

-----------------------------------------------------------------

### cl...@chromium.org (2015-10-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

Updating severity

### ti...@google.com (2015-10-13)

Congratulations - $500 for this report. We'll credit you alongside https://crbug.com/chromium/447860 and pay you $500 each.

We'll start payment later this week, so you should receive the cash ~2 weeks from today. I'll update this bug with a CVE shortly. 

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-13)

Reporter wishes to remain anonymous.

### ti...@google.com (2015-10-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-10-13)

Tim - Can you please let me know why you credited me as anonymous in http://googlechromereleases.blogspot.com/2015/10/stable-channel-update.html

### ti...@google.com (2015-10-14)

It was an error - it's now fixed in the release notes.

### ch...@gmail.com (2015-10-14)

Thanks Tim!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2016-01-12)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/532967?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/523653, crbug.com/chromium/535143, crbug.com/chromium/537192]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082877)*
