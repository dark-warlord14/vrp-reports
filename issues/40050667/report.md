# use after poison in rtc_rtp_sender_impl.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40050667](https://issues.chromium.org/issues/40050667) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2019-11-12 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36

Steps to reproduce the problem:
1.Build chrome with asan(Chromium 80.0.3965.0).
2../chrome --js-flags="--expose-gc" crash.html

What is the expected behavior?

What went wrong?
==37919==ERROR: AddressSanitizer: use-after-poison on address 0x7ec04ac936e8 at pc 0x560982d5b29e bp 0x7ffecf3b5490 sp 0x7ffecf3b5488
READ of size 8 at 0x7ec04ac936e8 thread T0 (chrome)
    #0 0x560982d5b29d in blink::(anonymous namespace)::OnSetParametersCompleted(blink::RTCVoidRequest*, webrtc::RTCError) ./../../third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender_impl.cc:36:14
    #1 0x560982d62cf1 in Invoke<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), blink::RTCVoidRequest *, webrtc::RTCError> ./../../base/bind_internal.h:398:12
    #2 0x560982d62cf1 in MakeItSo<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), blink::RTCVoidRequest *, webrtc::RTCError> ./../../base/bind_internal.h:598:12
    #3 0x560982d62cf1 in RunImpl<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), std::__1::tuple<blink::RTCVoidRequest *>, 0> ./../../base/bind_internal.h:671:12
    #4 0x560982d62cf1 in base::internal::Invoker<base::internal::BindState<void (*)(blink::RTCVoidRequest*, webrtc::RTCError), blink::RTCVoidRequest*>, void (webrtc::RTCError)>::RunOnce(base::internal::BindStateBase*, webrtc::RTCError&&) ./../../base/bind_internal.h:640:12
    #5 0x560982d610a2 in Run ./../../base/callback.h:98:12
    #6 0x560982d610a2 in blink::RTCRtpSenderImpl::RTCRtpSenderInternal::SetParametersCallback(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>) ./../../third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender_impl.cc:356:25
    #7 0x560982d61374 in Invoke<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> > ./../../base/bind_internal.h:498:12
    #8 0x560982d61374 in MakeItSo<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> > ./../../base/bind_internal.h:598:12
    #9 0x560982d61374 in RunImpl<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), std::__1::tuple<scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> >, 0, 1, 2> ./../../base/bind_internal.h:671:12
    #10 0x560982d61374 in base::internal::Invoker<base::internal::BindState<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:640:12
    #11 0x5609748e649e in Run ./../../base/callback.h:98:12
    #12 0x5609748e649e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #13 0x560974920a49 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #14 0x5609749203c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #15 0x56097482d2c0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #16 0x560974922874 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #17 0x560974922874 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #18 0x56097489529d in base::RunLoop::Run() ./../../base/run_loop.cc:156:14
    #19 0x5609858f859b in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:213:16
    #20 0x56097389bc46 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:871:10
    #21 0x560973a435bf in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:423:29
    #22 0x560973896f86 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #23 0x56096ad1a934 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #24 0x7fefa296bb96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0

Address 0x7ec04ac936e8 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/home/cowboy/chromium/src/out/chrome_asan_shared/chrome+0x20cc929d)
Shadow bytes around the buggy address:
  0x0fd88958a680: 00 06 00 00 00 00 00 06 00 00 00 00 00 06 00 00
  0x0fd88958a690: 00 00 00 06 00 00 00 00 00 06 00 00 00 00 00 06
  0x0fd88958a6a0: 00 00 00 00 00 06 00 00 00 00 00 06 00 00 00 00
  0x0fd88958a6b0: 00 f7 f7 f7 f7 f7 f7 f7 f7 06 00 00 00 00 06 00
  0x0fd88958a6c0: 00 00 00 00 06 00 00 00 00 00 f7 f7 f7 f7 f7 f7
=>0x0fd88958a6d0: f7 f7 06 00 00 00 00 f7 f7 f7 f7 f7 f7[f7]f7 f7
  0x0fd88958a6e0: f7 f7 06 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd88958a6f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 06
  0x0fd88958a700: 00 00 00 00 00 00 06 00 00 00 00 00 00 06 00 00
  0x0fd88958a710: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 06 00 00 00
  0x0fd88958a720: 00 06 00 00 00 00 00 00 00 06 00 00 00 00 06 00
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
==37919==ABORTING
Received signal 6
    #0 0x56096acad4db in backtrace /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4101:13
    #1 0x560974a18264 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x5609747dbee2 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x5609747dbee2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x560974a16eda in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7fefa9c3f890 in __funlockfile ??:?
    #6 0x7fefa9c3f890 in ?? ??:0
    #7 0x7fefa2988e97 in __libc_signal_restore_set /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/nptl-signals.h:80:0
    #8 0x7fefa2988e97 in raise /build/glibc-OTsEL5/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:48:0
    #9 0x7fefa298a801 in abort /build/glibc-OTsEL5/glibc-2.27/stdlib/abort.c:79:0
    #10 0x56096ad07227 in __sanitizer::Abort() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_posix_libcdep.cpp:155:3
    #11 0x56096ad05f41 in __sanitizer::Die() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/sanitizer_common/sanitizer_termination.cpp:58:5
    #12 0x56096acf23eb in __asan::ScopedInErrorReport::~ScopedInErrorReport() /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:186:7
    #13 0x56096acf3dce in __asan::ReportGenericError(unsigned long, unsigned long, unsigned long, unsigned long, bool, unsigned long, unsigned int, bool) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_report.cpp:474:1
    #14 0x56096acf4678 in __asan_report_load8 /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_rtl.cpp:120:1
    #15 0x560982d5b29e in blink::(anonymous namespace)::OnSetParametersCompleted(blink::RTCVoidRequest*, webrtc::RTCError) ./../../third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender_impl.cc:36:14
    #16 0x560982d62cf2 in Invoke<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), blink::RTCVoidRequest *, webrtc::RTCError> ./../../base/bind_internal.h:398:12
    #17 0x560982d62cf2 in MakeItSo<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), blink::RTCVoidRequest *, webrtc::RTCError> ./../../base/bind_internal.h:598:12
    #18 0x560982d62cf2 in RunImpl<void (*)(blink::RTCVoidRequest *, webrtc::RTCError), std::__1::tuple<blink::RTCVoidRequest *>, 0> ./../../base/bind_internal.h:671:12
    #19 0x560982d62cf2 in base::internal::Invoker<base::internal::BindState<void (*)(blink::RTCVoidRequest*, webrtc::RTCError), blink::RTCVoidRequest*>, void (webrtc::RTCError)>::RunOnce(base::internal::BindStateBase*, webrtc::RTCError&&) ./../../base/bind_internal.h:640:12
    #20 0x560982d610a3 in Run ./../../base/callback.h:98:12
    #21 0x560982d610a3 in blink::RTCRtpSenderImpl::RTCRtpSenderInternal::SetParametersCallback(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>) ./../../third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender_impl.cc:356:25
    #22 0x560982d61375 in Invoke<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> > ./../../base/bind_internal.h:498:12
    #23 0x560982d61375 in MakeItSo<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> > ./../../base/bind_internal.h:598:12
    #24 0x560982d61375 in RunImpl<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), std::__1::tuple<scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> >, 0, 1, 2> ./../../base/bind_internal.h:671:12
    #25 0x560982d61375 in base::internal::Invoker<base::internal::BindState<void (blink::RTCRtpSenderImpl::RTCRtpSenderInternal::*)(webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)>), scoped_refptr<blink::RTCRtpSenderImpl::RTCRtpSenderInternal>, webrtc::RTCError, base::OnceCallback<void (webrtc::RTCError)> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:640:12
    #26 0x5609748e649f in Run ./../../base/callback.h:98:12
    #27 0x5609748e649f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #28 0x560974920a4a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #29 0x5609749203c3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #30 0x56097482d2c1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #31 0x560974922875 in Run ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #32 0x560974922875 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #33 0x56097489529e in base::RunLoop::Run() ./../../base/run_loop.cc:156:14
    #34 0x5609858f859c in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:213:16
    #35 0x56097389bc47 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:871:10
    #36 0x560973a435c0 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:423:29
    #37 0x560973896f87 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #38 0x56096ad1a935 in ChromeMain ./../../chrome/app/chrome_main.cc:110:12
    #39 0x7fefa296bb97 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310:0
    #40 0x56096ac7632a in _start ??:0:0
  r8: 0000000000000000  r9: 00007ffecf3b44d0 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffecf3b5488 r13: 00007ffecf3b5490 r14: 00007ffecf3b5430 r15: 0000560988831808
  di: 0000000000000002  si: 00007ffecf3b44d0  bp: 00007ffecf3b5460  bx: 000056098879f398
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007fefa2988e97  sp: 00007ffecf3b44d0
  ip: 00007fefa2988e97 efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Did this work before? N/A 

Chrome version: Chromium 80.0.3965.0   Channel: dev
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### do...@chromium.org (2019-11-12)

+WebRTC folks, can you please follow up on this?

[Monorail components: Blink>WebRTC>PeerConnection]

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

### to...@chromium.org (2019-11-13)

Could this be because of https://chromium-review.googlesource.com/c/chromium/src/+/1899786 ?

### to...@chromium.org (2019-11-13)

[Empty comment from Monorail migration]

### ht...@chromium.org (2019-11-13)

To me this looks (smells?) like a WTF::Bind vs base::BindOnce issue - passing around pointers to garbage collected objects - want to add tonikitoo@igalia.com to the CC list, since he moved this stuff from content/ to blink/, but failed, probably due to Restrict-View-SecurityTeam.

### ht...@chromium.org (2019-11-13)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-11-14)

[Comment Deleted]

### ht...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1256477348d771d7e3ad4e0d9238d48ba03befc4

commit 1256477348d771d7e3ad4e0d9238d48ba03befc4
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Nov 14 19:14:39 2019

[peerconnection] Bind RTCVoidRequest* using WrapPersistent in RTCRtpSenderImpl.

Bug: 1023853
Change-Id: Ie4c250b4193dac8872476a2e7a45075c923969bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1917500
Auto-Submit: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Armando Miraglia <armax@chromium.org>
Reviewed-by: Armando Miraglia <armax@chromium.org>
Cr-Commit-Position: refs/heads/master@{#715351}

[modify] https://crrev.com/1256477348d771d7e3ad4e0d9238d48ba03befc4/third_party/blink/renderer/modules/peerconnection/rtc_rtp_sender_impl.cc


### gu...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### to...@igalia.com (2019-11-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1023853?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1024566]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050667)*
