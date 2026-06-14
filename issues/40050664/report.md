# use-after-poison in webaudio

| Field | Value |
|-------|-------|
| **Issue ID** | [40050664](https://issues.chromium.org/issues/40050664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>WebAudio |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2019-11-12 |
| **Bounty** | $10,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36

Steps to reproduce the problem:
1.Build chrome with asan.(Chromium 80.0.3965.0)
2.Open webserver.
  -- node webserver.js
3./chrome http://127.0.0.1:8605/triger.html
4.Click anywhere on the page to triger  user gesture.
5.Get use-after poison issue.

What is the expected behavior?

What went wrong?
==53207==ERROR: AddressSanitizer: use-after-poison on address 0x7ef2d30e6ca8 at pc 0x55966cca3f2e bp 0x7ffe1301fa50 sp 0x7ffe1301fa48
READ of size 8 at 0x7ef2d30e6ca8 thread T0 (chrome)
    #0 0x55966cca3f2d in operator* ./../../base/memory/scoped_refptr.h:231:13
    #1 0x55966cca3f2d in GetDeferredTaskHandler ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.h:257:12
    #2 0x55966cca3f2d in blink::DeferredTaskHandler::GraphAutoLocker::GraphAutoLocker(blink::BaseAudioContext const*) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:306:25
    #3 0x55966cc53bd3 in blink::BaseAudioContext::PerformCleanupOnMainThread() ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:719:19
    #4 0x55965cc4849e in Run ./../../base/callback.h:98:12
    #5 0x55965cc4849e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #6 0x55965cc82a49 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #7 0x55965cc823c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #8 0x55965cb8f2c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #9 0x55965cc84874 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #10 0x55965cc84874 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #11 0x55965cbf729d in base::RunLoop::Run() ./../../base/run_loop.cc:156:14
    #12 0x55966dc5a59b in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:213:16
    #13 0x55965bbfdc46 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:871:10
    #14 0x55965bda55bf in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:423:29
    #15 0x55965bbf8f86 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #16 0x55965307c934 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #17 0x7fb90a4fbb96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

Address 0x7ef2d30e6ca8 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x228aff2d)
Shadow bytes around the buggy address:
  0x0fdeda614d40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614d50: f7 f7 06 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614d60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614d70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 06
  0x0fdeda614d80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdeda614d90: f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614da0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614db0: f7 f7 f7 f7 f7 f7 06 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614dc0: f7 f7 f7 f7 f7 f7 f7 f7 06 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614dd0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdeda614de0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==53207==ABORTING
Received signal 6
    #0 0x55965300f4db in backtrace /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4101:13
    #1 0x55965cd7a264 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x55965cb3dee2 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x55965cb3dee2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x55965cd78eda in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7fb9117cf890 in __funlockfile ??:?
    #6 0x7fb9117cf890 in ?? ??:0
    #7 0x7fb90a518e97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7fb90a518e97 in raise /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7fb90a51a801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #10 0x559653069227 in __sanitizer::Abort() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:155:3
    #11 0x559653067f41 in __sanitizer::Die() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #12 0x5596530543eb in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:186:7
    #13 0x559653055dce in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:474:1
    #14 0x559653056678 in __asan_report_load8 /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120:1
    #15 0x55966cca3f2e in operator* ./../../base/memory/scoped_refptr.h:231:13
    #16 0x55966cca3f2e in GetDeferredTaskHandler ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.h:257:12
    #17 0x55966cca3f2e in blink::DeferredTaskHandler::GraphAutoLocker::GraphAutoLocker(blink::BaseAudioContext const*) ./../../third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc:306:25
    #18 0x55966cc53bd4 in blink::BaseAudioContext::PerformCleanupOnMainThread() ./../../third_party/blink/renderer/modules/webaudio/base_audio_context.cc:719:19
    #19 0x55965cc4849f in Run ./../../base/callback.h:98:12
    #20 0x55965cc4849f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #21 0x55965cc82a4a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #22 0x55965cc823c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #23 0x55965cb8f2c1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #24 0x55965cc84875 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #25 0x55965cc84875 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #26 0x55965cbf729e in base::RunLoop::Run() ./../../base/run_loop.cc:156:14
    #27 0x55966dc5a59c in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:213:16
    #28 0x55965bbfdc47 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:871:10
    #29 0x55965bda55c0 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:423:29
    #30 0x55965bbf8f87 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #31 0x55965307c935 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #32 0x7fb90a4fbb97 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0
    #33 0x559652fd832a in _start ??:0:0
  r8: 0000000000000000  r9: 00007ffe1301ea90 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffe1301fa48 r13: 00007ffe1301fa50 r14: 00007ffe1301f9f0 r15: 0000559670b93808
  di: 0000000000000002  si: 00007ffe1301ea90  bp: 00007ffe1301fa20  bx: 0000559670b01398
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007fb90a518e97  sp: 00007ffe1301ea90
  ip: 00007fb90a518e97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 80.0.3965.0   Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan.log](attachments/asan.log) (text/plain, 9.1 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 4.3 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 8.7 MB)
- [uap-repro-1023810.html](attachments/uap-repro-1023810.html) (text/plain, 744 B)

## Timeline

### do...@chromium.org (2019-11-12)

+WebAudio/media folks, can you please follow up on this?

[Monorail components: Blink>WebAudio]

### sh...@chromium.org (2019-11-13)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2019-11-13)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-11-13)

This can't be verified by ClusterFuzz because the repro case requires a custom web server.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9f90ec1a53f56aa20030257499618d3486c8e604

commit 9f90ec1a53f56aa20030257499618d3486c8e604
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Nov 13 19:44:32 2019

Check if ExecutionContext is valid in BaseAudioContext::PerformCleanupOnMainThread

When the tear-down process of BaseAudioContext occurs rapidly along with
the destruction of an associated ExecutionContext, a scheduled task from
the audio rendering thread can attempt to access `this` pointer of
BaseAudioContext.

This CL add a check to verify the validity of an ExecutionContext before
the function accesses the `this` pointer for the audio graph lock.

Test: Ran the repro case locally with this patch for 20 minutes and no UAP occurred.
Bug: 1023810
Change-Id: I8e5b960b50aca5b0dcee52b5886804af2515806e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1913872
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#715021}

[modify] https://crrev.com/9f90ec1a53f56aa20030257499618d3486c8e604/third_party/blink/renderer/modules/webaudio/base_audio_context.cc


### ho...@chromium.org (2019-11-14)

The patch is landed in 80.0.3967.0. So Canary will pick it up by tomorrow.

cdsrc2016@ Can you verify when Canary with the patch becomes available?

### cd...@gmail.com (2019-11-15)

I tested it in two ways, and I still can reproduce the crash.
1. Patch diff to my local source(Chromium 80.0.3964.0).
2. Download Win_x64_715201_chrome-win and Win_x64_715556_chrome-win.

### ho...@chromium.org (2019-11-15)

Thanks. The same stack trace?

### cd...@gmail.com (2019-11-15)

a little different.

### ho...@chromium.org (2019-11-15)

Very interesting. Now UAP happens in non-WebAudio code, which is:
https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/lifecycle_observer.h?l=46

haraken@ I can see that |lifecycle_context_| is a WeakMember. Can it be somehow relevant with this crash? Just in case, I am adding the GC component to this bug.

cdsrc2016@ How long did you have to run the repro to get the crash? Also I assume this is a Windows-specific crash because I don't see the crash on MacOS and Linux wit the fix.


[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### cd...@gmail.com (2019-11-15)

Crash will appear soon in my local PC.And I can  get crash in Linux with the patch(Chromium 80.0.3964.0 with the patch https://chromium-review.googlesource.com/c/chromium/src/+/1913872/4/third_party/blink/renderer/modules/webaudio/base_audio_context.cc).
I tested it in two ways.
1. Without Any other chrome options.This case,need to click page.
2. With Chrome options.This case,no user interaction required.
	-autoplay-policy=no-user-gesture-required --user-data-dir=/tmp/8888/chrome-prof

The attachment is a video that I reproduced in two ways locally.

### ho...@chromium.org (2019-11-19)

The repro case has an echo server; it simply replicates the message and send it back to the client. When the client receives the message, it replaces the source code of the iframe. Hence the previous execution context is thrown away, and repeat. So this is technically an equivalent of a rapid-refresh attack.

I am not really sure how GC should behave after an iframe is swept away. I can make an AudioContext alive longer, but that won't really hold when the entire iframe is shot down. I also noticed that ExecutionContext:ContextDestroyed() doesn't get called when the iframe is going away.

haraken@ Can some one from GC team take a look at this? Like I pointed out, now it is crashed at:
https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/lifecycle_observer.h?l=46

### ho...@chromium.org (2019-11-19)

mlippautz@ Would you mind taking a look at this?

### ml...@chromium.org (2019-11-19)

I am OOO, as my status, teams page, and calendar indicate...

+omerkatz as GC sheriff.

It would really help if there's a design doc for WebAudio because multi-threaded Blink only has limited support.

### ho...@chromium.org (2019-11-19)

I might be wrong, but I don't think this is a WebAudio issue. A scheduled task in the main thread task runner gets fired after the associated object is gone. (Not by GC, but the iframe teardown)

I've tried with BaseAudioContext::HasPendingActivity() returning always true - but it still crashes with UAP. Also there's no call from ExecutionContext::ContextDestroyed().

### ha...@google.com (2019-11-20)

> haraken@ Can some one from GC team take a look at this? Like I pointed out, now it is crashed at:
https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/lifecycle_observer.h?l=46

This means that the BaseAudioContext object is gone.

How is it guaranteed that the BaseAudioContext object is alive when BaseAudioContext::PerformCleanupOnMainThread gets called?


### ho...@chromium.org (2019-11-20)

Thanks for the response - I also have few questions:

- When the ExecutionContext is gone, how can BaseAudioContext be alive?
- BaseAudioContext::PerformCleanupOnMainThread is scheduled by the audio thread with WrapCrossThreadPersistent(BaseAudioContext). But this is not good enough to make the context survive the shutdown process.
- Like I pointed out, I can see BaseAudioContext() is still going away even with HasPendingActivity() returns always true. (with the given repro case)


### ha...@google.com (2019-11-20)

- When the ExecutionContext is gone, how can BaseAudioContext be alive?

Their lifetime is independent. It's possible that BaseAudioContext outlives ExecutionContext. Then BaseAudioContext::lifecycle_context_ returns false.

- BaseAudioContext::PerformCleanupOnMainThread is scheduled by the audio thread with WrapCrossThreadPersistent(BaseAudioContext). But this is not good enough to make the context survive the shutdown process.

Ah, it should be enough.

Hmm, I'm confused. Are we really observing BaseAudioContext is gone when BaseAudioContext::PerformCleanupOnMainThread is called? It should not happen as long as you use the cross-thread persistent.

- Like I pointed out, I can see BaseAudioContext() is still going away even with HasPendingActivity() returns always true.

This looks strange. It should not happen...

One clarification:

The stack trace in #0 is saying it's crashing at DeferredTaskHandler::GraphAutoLocker::GraphAutoLocker. However, now you're saying it's crashing at LifecycleObserver::GetContext() (with what stack trace?). Which is the current status?


### ho...@chromium.org (2019-11-22)

> Their lifetime is independent. It's possible that BaseAudioContext outlives ExecutionContext. Then BaseAudioContext::lifecycle_context_ returns false.

This seems also problematic. In several places, the WebAudio code checks if EC is alive to determine the lifecycle of the main thread.

> Hmm, I'm confused. Are we really observing BaseAudioContext is gone when BaseAudioContext::PerformCleanupOnMainThread is called? It should not happen as long as you use the cross-thread persistent.

It's here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/base_audio_context.cc?l=752

> The stack trace in #0 is saying it's crashing at DeferredTaskHandler::GraphAutoLocker::GraphAutoLocker. However, now you're saying it's crashing at LifecycleObserver::GetContext() (with what stack trace?). Which is the current status?

After the CL in #7, now it crashes on the GetExecutionContext() check because it is already gone.

One more question: the problem here is that the main thread task runner is firing a scheduled task in its queue even when both EC and BAC are gone. As long as the task runner is doing this, I don't think we can fix this problem properly. WDYT?



### ho...@chromium.org (2019-11-22)

I have a new simplified repro case (1 HTML file). See the attached file.

78.0.3904.108 (Stable): an instant crash
80.0.3975.0 (Canary): keeps running without a crash
80.0.3975.0 (ToT ASAN): an UAP crash after 5~7 seconds

The stack trace from ToT ASAN below (MacOS):

#0 0x138cfd7ea in blink::BaseAudioContext::PerformCleanupOnMainThread() (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0x1dd527ea)
    #1 0x12714e9bf in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc1a39bf)
    #2 0x12718df70 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc1e2f70)
    #3 0x12718f00e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoDelayedWork(base::TimeTicks*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc1e400e)
    #4 0x1272e145f in base::MessagePumpCFRunLoopBase::RunWork() (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc33645f)
    #5 0x1272cb1c9 in base::mac::CallWithEHFrame(void () block_pointer) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc3201c9)
    #6 0x1272df655 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc334655)
    #7 0x7fff43d71b2a in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__ (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64+0x57b2a)
    #8 0x7fff43d71ad0 in __CFRunLoopDoSource0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64+0x57ad0)
    #9 0x7fff43d559da in __CFRunLoopDoSources0 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64+0x3b9da)
    #10 0x7fff43d54fa2 in __CFRunLoopRun (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64+0x3afa2)
    #11 0x7fff43d548a4 in CFRunLoopRunSpecific (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64+0x3a8a4)
    #12 0x7fff45fd72fe in -[NSRunLoop(NSRunLoop) runMode:beforeDate:] (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x1c2fe)
    #13 0x1272e3220 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc338220)
    #14 0x1272ddf32 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc332f32)
    #15 0x12718fd29 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc1e4d29)
    #16 0x1270efd49 in base::RunLoop::Run() (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xc144d49)
    #17 0x13a2e12ac in content::RendererMain(content::MainFunctionParams const&) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0x1f3362ac)
    #18 0x1259bb353 in content::ContentMainRunnerImpl::Run(bool) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xaa10353)
    #19 0x130c76a56 in service_manager::Main(service_manager::MainParams const&) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0x15ccba56)
    #20 0x1259b918c in content::ContentMain(content::ContentMainParams const&) (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0xaa0e18c)
    #21 0x11afaffa9 in ChromeMain (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Chromium Framework:x86_64+0x4fa9)
    #22 0x10c674d0d in main (/Users/hongchan/chromium/src/out/ASAN/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/80.0.3975.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):x86_64+0x100001d0d)
    #23 0x7fff6fd543d4 in start (/usr/lib/system/libdyld.dylib:x86_64+0x163d4)

### ha...@google.com (2019-11-25)

>> Their lifetime is independent. It's possible that BaseAudioContext outlives ExecutionContext. Then BaseAudioContext::lifecycle_context_ returns false.
>
> This seems also problematic. In several places, the WebAudio code checks if EC is alive to determine the lifecycle of the main thread.

It is not a problem as long as the EC check is done on the main thread. BaseAudioContext::GetExecutionContext() returns nullptr after EC is detached.

> After the CL in #7, now it crashes on the GetExecutionContext() check because it is already gone.

I don't understand this part. If EC is gone, GetExecutionContext() just returns nullptr (because the LifecycleContext::context_ is a weak pointer).

The fact that GetExecutionContext() is crashing means that the |this| pointer (i.e., the BAC object) is gone. This should not happen because you're using CrossThreadPersistent to pass the BAC object...

Is it possible that the audio thread is shut down before the main thread runs the task? Then the BAC object will be gone.


### ml...@chromium.org (2019-11-25)

Since we have a repro, I'd suggest to just go through it and see why the context is gone.

### om...@chromium.org (2019-11-25)

I tried reproducing this crash today.
I ran it on both Linux and MacOs.
On 78.0.3904.108 (Stable) I get an instant crash on both systems, same as hongchan@.
On ToT (80.0.3978.0, http://crrev.com/718650) I'm not seeing the UaP hongchan@ observed (on Linux I get nothing, on MacOs I get the same crash as on stable).

hongchan@ can you confirm that you get the same results (preferably on Linux)?
If you are, we can use that to bisect and check whether this issue was already fixed.
If y

### om...@chromium.org (2019-12-06)

Reassigning to hongchan@ to get his attention.

### sh...@chromium.org (2019-12-07)

hongchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2019-12-09)

Still reproduces for me on Linux, ToT this morning.


### ho...@chromium.org (2019-12-09)

rtoy@ Could you post the latest stack trace here?

Also per #28, I am reassigning this to omerkatz@. Sorry but I am also handling the other P1 UAF issue at the moment, so I would appreciate if GC team can help with this issue. Thanks!

### om...@chromium.org (2019-12-09)

rtoy@, instead of posting the stack trace, it would be better if you could post exact reproduction instructions.
As stated above, when I tried to reproduce it on ToT, I couldn't.

### rt...@chromium.org (2019-12-09)

Possibly caused by AudioContext::HasPendingActivity  returning false because the context is suspended (not running), but BaseAudioContext::HasPendingActivity returns true.  (See https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/audio_context.cc?rcl=a1c15f10d000605ed76b6766223453c0c1d3967d&l=556)

But the the context still has activity because the suspended context in the test is resumed, causing the resume resolvers to fire.  But there's no activity, so the execution context was deleted before the resolvers can fire.  (Resolvers fire when the audio destination starts running again, which can take many millisec from the time it's requested to resume until it does resume).

### rt...@chromium.org (2019-12-09)

For the repro, I just used a linux asan build and load up the repro case from c#22 (from a web server).  This crashes in a couple of sec.  Also set the following envvars:

export G_SLICE=always-malloc
export NSS_DISABLE_ARENA_FREE_LIST=1
export NSS_DISABLE_UNLOAD=1
export ASAN_OPTIONS="detect_odr_violation=0"


### rt...@chromium.org (2019-12-09)

Changing line 556 to be:

  return (ContextState() != kClosed) && BaseAudioContext::HasPendingActivity();

makes the crash go away for me.  The comments say suspended contexts have no activity, which is true, but that doesn't account for the fact that they can be resumed at any time.  Thus checking for not closed might be the right thing to do here.

More testing required.  

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-12-11)

FWIW, the fix for another UAF (https://chromium-review.googlesource.com/c/chromium/src/+/1960083) was not helpful for this case. I think we should patch this per #33.

### rt...@chromium.org (2019-12-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5efc951230de524c2b6787e25ec651c46f2652b4

commit 5efc951230de524c2b6787e25ec651c46f2652b4
Author: Raymond Toy <rtoy@chromium.org>
Date: Thu Dec 12 22:28:07 2019

AudioContext HasPendingActivity unless it's closed

An AudioContext is considered to have activity if it's not closed.
Previously, suspended contexts were considered has having no activity,
but that's not quite true since the context can be resumed at any time
after.  This would allow contexts to be collected prematurely even
though the context was resumed.  This causes the audio thread to
access objects that are possibly deleted.

Manually tested against test case from the bug; no issues seen.

Bug: 1023810
Change-Id: I81cc0aff57bf4701b3ef9c36dd72b7e8922af5b9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1955339
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#724364}

[modify] https://crrev.com/5efc951230de524c2b6787e25ec651c46f2652b4/third_party/blink/renderer/modules/webaudio/audio_context.cc


### rt...@chromium.org (2019-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-14)

Your change meets the bar and is auto-approved for M80. Please go ahead and merge the CL to branch 3987 (refs/branch-heads/3987) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd211b44535c09af58353f0799a624f076e98dda

commit fd211b44535c09af58353f0799a624f076e98dda
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Dec 16 17:06:28 2019

AudioContext HasPendingActivity unless it's closed

An AudioContext is considered to have activity if it's not closed.
Previously, suspended contexts were considered has having no activity,
but that's not quite true since the context can be resumed at any time
after.  This would allow contexts to be collected prematurely even
though the context was resumed.  This causes the audio thread to
access objects that are possibly deleted.

Manually tested against test case from the bug; no issues seen.

TBR=hongchan@chromium.org
(cherry picked from commit 5efc951230de524c2b6787e25ec651c46f2652b4)

Bug: 1023810
Change-Id: I81cc0aff57bf4701b3ef9c36dd72b7e8922af5b9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1955339
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#724364}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1969044
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#158}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/fd211b44535c09af58353f0799a624f076e98dda/third_party/blink/renderer/modules/webaudio/audio_context.cc


### na...@google.com (2019-12-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-18)

Adjusting the severity to High because this could potentially lead to RCE in the renderer. It does need a gesture per https://crbug.com/chromium/1023810#c13, but the gesture is just a click, so we think High is appropriate.

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $10,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-07)

rtoy@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### [Deleted User] (2020-03-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1023810?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050664)*
