# Security: Out of Bound Write/Invalid Pointer Write while parsing PDF

| Field | Value |
|-------|-------|
| **Issue ID** | [40086082](https://issues.chromium.org/issues/40086082) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Windows |
| **Reporter** | mo...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2016-11-25 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://www.chromium.org/Home>**  

**/chromium-security/security-faq**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**  

Chrome Browser is vulnerable to Out of Bound Write/Invalid Pointer Write vulnerability due to improper pointer arithmetic while parsing malformed PDF file due incorrect validation.

The exploitability of the bug has not been determined due to scarcity of time. Seeing the nature of the bug, I believe this bug could be used to gain Remote Code Execution.

**VERSION**  

Chrome Version: [54.0.2840.99] + [stable release]  

Operating System: Windows 10 Pro x86 Version: 1607 OS Build 14393.447

**REPRODUCTION CASE**  

1.Enable Application Verifier and make sure Full option in Heap section is turned ON  

2.Launch chrome.exe --no-sandbox --disable-seccomp-filter-sandbox --disable-seccomp-sandbox --disable-popup-blocking --disable-default-apps --disable-extensions --no-first-run --disable-session-crashed-bubble --allow-file-access-from-files --noerrdialogs --disable-hang-monitor --js-flags="–expose-gc" --disable-prompt-on-repost --force-renderer-accessibility --disable-infobars --disable-plugins --disable-plugins-discovery --disable-translate file:///C:/Users/Srishti/Desktop/crash\_57b76df0d1b74dbb86d0bbb592b59a37eb9da399.pdf inside a debugger (make sure you do childdbg 1;g; for each chrome.exe process)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:

5:061> r  

eax=00000004 ebx=00000000 ecx=0ddeeff0 edx=00000001 esi=00000001 edi=0b3b0d70  

eip=555fb233 esp=00b3f3ac ebp=00b3f460 iopl=0 nv up ei pl nz na po nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202  

chrome\_child!chrome\_pdf::OutOfProcessInstance::SendNextAccessibilityPage+0x1e4:  

555fb233 f20f1144c1f8 movsd mmword ptr [ecx+eax\*8-8],xmm0 ds:0023:0ddef008=????????????????

5:061> kb  

00b3f460 555fb462 00000001 00b3f4a8 00b3f484 chrome\_child!chrome\_pdf::OutOfProcessInstance::SendNextAccessibilityPage+0x1e4 [c:\b\build\slave\win-pgo\build\src\pdf\out\_of\_process\_instance.cc @ 684]  

00b3f470 559cb765 09a28ff8 00000001 570246b3 chrome\_child!pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome\_pdf::OutOfProcessInstance,pp::ThreadSafeThreadTraits>::Dispatcher0<void (\_\_thiscall chrome\_pdf::OutOfProcessInstance::\*)(int)> >::Thunk+0x27 [c:\b\build\slave\win-pgo\build\src\ppapi\utility\completion\_callback\_factory.h @ 586]  

00b3f484 559cba59 00b3f4c4 09b88ffc 00000000 chrome\_child!ppapi::CallWhileUnlocked<void,PP\_CompletionCallback \*,int,PP\_CompletionCallback \*,int>+0x17 [c:\b\build\slave\win-pgo\build\src\ppapi\shared\_impl\proxy\_lock.h @ 135]  

00b3f4b0 559cbbdd 555fb43b 09a28ff8 00000000 chrome\_child!ppapi::proxy::`anonymous namespace'::CallbackWrapper+0x70 [c:\b\build\slave\win-pgo\build\src\ppapi\proxy\ppb\_core\_proxy.cc @ 52]  

00b3f4d0 559b9ed4 09b88fe0 09d1cff8 00b3f4f0 chrome\_child!base::internal::Invoker<base::internal::BindState<void (\_\_cdecl\*)(PP\_CompletionCallback,int),PP\_CompletionCallback,int>,void \_\_cdecl(void)>::Run+0x19 [c:\b\build\slave\win-pgo\build\src\base\bind\_internal.h @ 324]  

00b3f4e0 55f84063 09c70ff8 00000000 00b3f548 chrome\_child!ppapi::internal::RunWhileLockedHelper<void \_\_cdecl(void)>::CallWhileLocked+0x1d [c:\b\build\slave\win-pgo\build\src\ppapi\shared\_impl\proxy\_lock.h @ 199]  

00b3f4f0 548122c6 09dbcfe8 5481227c 00b3f5f0 chrome\_child!base::internal::Invoker<base::internal::BindState<void (\_\_cdecl\*)(std::unique\_ptr<base::Callback<void \_\_cdecl(scoped\_refptr[media::VideoFrame](javascript:void(0);) const &,base::TimeTicks),1>,std::default\_delete<base::Callback<void \_\_cdecl(scoped\_refptr[media::VideoFrame](javascript:void(0);) const &,base::TimeTicks),1> > >),base::internal::PassedWrapper<std::unique\_ptr<base::Callback<void \_\_cdecl(scoped\_refptr[media::VideoFrame](javascript:void(0);) const &,base::TimeTicks),1>,std::default\_delete<base::Callback<void \_\_cdecl(scoped\_refptr[media::VideoFrame](javascript:void(0);) const &,base::TimeTicks),1> > > > >,void \_\_cdecl(void)>::Run+0x29 [c:\b\build\slave\win-pgo\build\src\base\bind\_internal.h @ 324]  

00b3f4f8 5481227c 00b3f5f0 00b3f728 00b3f7c0 chrome\_child!base::Callback<void \_\_cdecl(void),1>::Run+0x5 [c:\b\build\slave\win-pgo\build\src\base\callback.h @ 388]  

00b3f548 54811f6a 5654f514 00b3f5f0 00b3f600 chrome\_child!base::debug::TaskAnnotator::RunTask+0x6a [c:\b\build\slave\win-pgo\build\src\base\debug\task\_annotator.cc @ 56]  

00b3f5a4 54811e2d 00b3f5f0 08916ff8 08916fe8 chrome\_child!base::MessageLoop::RunTask+0x78 [c:\b\build\slave\win-pgo\build\src\base\message\_loop\message\_loop.cc @ 489]  

00b3f664 548117fc 08916ff8 00000000 00b3f728 chrome\_child!base::MessageLoop::DoDelayedWork+0x1ff [c:\b\build\slave\win-pgo\build\src\base\message\_loop\message\_loop.cc @ 660]  

00b3f6a4 549f08a4 00b3f728 565bf270 00b3f808 chrome\_child!base::MessagePumpDefault::Run+0x36 [c:\b\build\slave\win-pgo\build\src\base\message\_loop\message\_pump\_default.cc @ 39]  

00b3f6f0 549f085c 0751afe0 0a353a05 00000000 chrome\_child!base::MessageLoop::RunHandler+0x34 [c:\b\build\slave\win-pgo\build\src\base\message\_loop\message\_loop.cc @ 452]  

00b3f710 54b6ff9e 00b3f8d8 00000000 00b3f8e4 chrome\_child!base::RunLoop::Run+0x2c [c:\b\build\slave\win-pgo\build\src\base\run\_loop.cc @ 36]  

00b3f894 5495373c 00b3f8d8 07510fd0 088d2fe0 chrome\_child!content::PpapiPluginMain+0x194 [c:\b\build\slave\win-pgo\build\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 146]  

00b3f8b4 549536b9 00b3f920 07510fd0 ffffffff chrome\_child!content::RunNamedProcessTypeMain+0x4d [c:\b\build\slave\win-pgo\build\src\content\app\content\_main\_runner.cc @ 418]  

00b3f904 5495307f 06c28fe0 06e28fd8 54cd43fa chrome\_child!content::ContentMainRunnerImpl::Run+0x98 [c:\b\build\slave\win-pgo\build\src\content\app\content\_main\_runner.cc @ 786]  

00b3f910 54cd43fa 06e28fd8 06e28fe0 565dbb68 chrome\_child!content::ContentMain+0x54 [c:\b\build\slave\win-pgo\build\src\content\app\content\_main.cc @ 20]  

00b3f950 00f2529a 00f20000 00b3f970 06e28ffc chrome\_child!ChromeMain+0x6d [c:\b\build\slave\win-pgo\build\src\chrome\app\chrome\_main.cc @ 91]  

00b3fa0c 00f21d59 00f20000 00000000 00fd8984 chrome!MainDllLoader::Launch+0x2a1 [c:\b\build\slave\win-pgo\build\src\chrome\app\main\_dll\_loader\_win.cc @ 182]  

00b3fb44 00f85d6e 00f20000 00000000 00b77d88 chrome!wWinMain+0x179 [c:\b\build\slave\win-pgo\build\src\chrome\app\chrome\_exe\_main\_win.cc @ 253]  

00b3fb90 77718e94 009c3000 77718e70 8c76e4f6 chrome!\_\_scrt\_common\_main\_seh+0xfd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 255]  

00b3fba4 779be9f2 009c3000 8caeef8d 00000000 KERNEL32!BaseThreadInitThunk+0x24  

00b3fbec 779be9c1 ffffffff 77a05d00 00000000 ntdll!\_\_RtlUserThreadStart+0x2b  

00b3fbfc 00000000 00f85de7 009c3000 00000000 ntdll!\_RtlUserThreadStart+0x1b

5:061> !heap -p -a 0xddef008  

address 0ddef008 found in  

\_DPH\_HEAP\_ROOT @ b61000  

in busy allocation ( DPH\_HEAP\_BLOCK: UserAddr UserSize - VirtAddr VirtSize)  

dc92888: ddeeff0 10 - ddee000 2000  

5cee9c2c verifier!AVrfDebugPageHeapAllocate+0x0000023c  

77a4fff0 ntdll!RtlDebugAllocateHeap+0x0000003c  

77999032 ntdll!RtlpAllocateHeap+0x00001642  

7799673f ntdll!RtlpAllocateHeapInternal+0x0000042f  

779962da ntdll!RtlAllocateHeap+0x0000002a  

692ea792 vrfcore!VfCoreRtlAllocateHeap+0x00000016  

5cdd0196 vfbasics!AVrfpRtlAllocateHeap+0x000000e2  

5462eae0 chrome\_child!malloc+0x00000030  

54d84021 chrome\_child!operator new+0x0000002c  

546cb217 chrome\_child!std::\_Allocate+0x00000028  

559d9d38 chrome\_child!std::vector<PP\_PictureBuffer\_Dev,std::allocator<PP\_PictureBuffer\_Dev> >::\_Buy+0x00000038  

562ba8e5 chrome\_child!std::vector<gpu::gles2::TransformFeedbackVaryingInfo,std::allocator[gpu::gles2::TransformFeedbackVaryingInfo](javascript:void(0);) >::vector<gpu::gles2::TransformFeedbackVaryingInfo,std::allocator[gpu::gles2::TransformFeedbackVaryingInfo](javascript:void(0);) >+0x0000001a  

555fb0d7 chrome\_child!chrome\_pdf::OutOfProcessInstance::SendNextAccessibilityPage+0x00000088  

555fb462 +0x00000027  

559cb765 chrome\_child!ppapi::CallWhileUnlocked<void,PP\_CompletionCallback \*,int,PP\_CompletionCallback \*,int>+0x00000017  

559cba59 chrome\_child!ppapi::proxy::`anonymous namespace'::CallbackWrapper+0x00000070  

559cbbdd chrome\_child!base::internal::Invoker<base::internal::BindState<void (\_\_cdecl\*)(PP\_CompletionCallback,int),PP\_CompletionCallback,int>,void \_\_cdecl(void)>::Run+0x00000019  

559b9ed4 chrome\_child!ppapi::internal::RunWhileLockedHelper<void \_\_cdecl(void)>::CallWhileLocked+0x0000001d  

55f84063 +0x00000029  

548122c6 chrome\_child!base::Callback<void \_\_cdecl(void),1>::Run+0x00000005  

54811f6a chrome\_child!base::MessageLoop::RunTask+0x00000078  

54811e2d chrome\_child!base::MessageLoop::DoDelayedWork+0x000001ff  

548117fc chrome\_child!base::MessagePumpDefault::Run+0x00000036  

549f08a4 chrome\_child!base::MessageLoop::RunHandler+0x00000034  

549f085c chrome\_child!base::RunLoop::Run+0x0000002c  

54b6ff9e chrome\_child!content::PpapiPluginMain+0x00000194  

5495373c chrome\_child!content::RunNamedProcessTypeMain+0x0000004d  

549536b9 chrome\_child!content::ContentMainRunnerImpl::Run+0x00000098  

5495307f chrome\_child!content::ContentMain+0x00000054  

00f2529a chrome!MainDllLoader::Launch+0x000002a1  

00f21d59 chrome!wWinMain+0x00000179  

00f85d6e chrome!\_\_scrt\_common\_main\_seh+0x000000fd

## Attachments

- [Google Chrome - Invalid Pointer Write.html](attachments/Google Chrome - Invalid Pointer Write.html) (text/plain, 90.1 KB)
- [crash_57b76df0d1b74dbb86d0bbb592b59a37eb9da399.pdf](attachments/crash_57b76df0d1b74dbb86d0bbb592b59a37eb9da399.pdf) (application/pdf, 677.2 KB)

## Timeline

### do...@chromium.org (2016-11-25)

Hi PDF folks, can you please take a look at this? I can't reproduce it since I don't have a Windows machine to hand.

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2016-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### mo...@gmail.com (2016-11-30)

make sure, you set CHROME_ALLOCATOR=winheap

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### mo...@gmail.com (2016-12-08)

hey guys, any update on this bug?

### sh...@chromium.org (2016-12-10)

dsinclair: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### ds...@chromium.org (2016-12-15)

raymes@ this looks like it's in the chrome pdf code, something to do with sending accessiblity pages? Would you be the right person to look into this?

### ra...@chromium.org (2016-12-15)

This looks like it's in the SendNextAccessibilityPage function. We are operating on a bunch of arrays here, and reaching into arrays in the PDF engine, so I wouldn't be surprised if we were getting something wrong there.

dmazzoni: could you ptal at this crash? Thanks!

### mo...@gmail.com (2016-12-19)

I was able to reproduce this issue using ASAN build for Linux.

ashfaq@hacksys:~/asan-linux-release-439448$ ./chrome --no-sandbox --disable-seccomp-filter-sandbox --disable-seccomp-sandbox --disable-popup-blocking --disable-default-apps --disable-extensions --no-first-run --disable-session-crashed-bubble --allow-file-access-from-files --noerrdialogs --disable-hang-monitor --force-renderer-accessibility ~/crash_57b76df0d1b74dbb86d0bbb592b59a37eb9da399.pdf =================================================================
==323==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200001bfa8 at pc 0x7f882243ff8d bp 0x7ffd7f5a73b0 sp 0x7ffd7f5a73a8
WRITE of size 8 at 0x60200001bfa8 thread T0 (chrome)
    #0 0x7f882243ff8c in chrome_pdf::OutOfProcessInstance::SendNextAccessibilityPage(int) pdf/out_of_process_instance.cc:789:58
    #1 0x7f8822453ac9 in operator() ppapi/utility/completion_callback_factory.h:607:9
    #2 0x7f8822453ac9 in pp::CompletionCallbackFactory<chrome_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome_pdf::OutOfProcessInstance::*)(int)> >::Thunk(void*, int) ppapi/utility/completion_callback_factory.h:584
    #3 0x7f88272da33e in PP_RunCompletionCallback ppapi/c/pp_completion_callback.h:240:3
    #4 0x7f88272da33e in CallWhileUnlocked<void, PP_CompletionCallback *, int, PP_CompletionCallback *, int> ppapi/shared_impl/proxy_lock.h:135
    #5 0x7f88272da33e in ppapi::proxy::(anonymous namespace)::CallbackWrapper(PP_CompletionCallback, int) ppapi/proxy/ppb_core_proxy.cc:52
    #6 0x7f88272da8aa in Invoke<const PP_CompletionCallback &, const int &> base/bind_internal.h:164:12
    #7 0x7f88272da8aa in MakeItSo<void (*const &)(PP_CompletionCallback, int), const PP_CompletionCallback &, const int &> base/bind_internal.h:285
    #8 0x7f88272da8aa in RunImpl<void (*const &)(PP_CompletionCallback, int), const std::__1::tuple<PP_CompletionCallback, int> &, 0, 1> base/bind_internal.h:361
    #9 0x7f88272da8aa in base::internal::Invoker<base::internal::BindState<void (*)(PP_CompletionCallback, int), PP_CompletionCallback, int>, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:339
    #10 0x7f88272c28f9 in Run base/callback.h:85:12
    #11 0x7f88272c28f9 in ppapi::internal::RunWhileLockedHelper<void ()>::CallWhileLocked(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >) ppapi/shared_impl/proxy_lock.h:199
    #12 0x7f88272c2b50 in Invoke<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind_internal.h:164:12
    #13 0x7f88272c2b50 in MakeItSo<void (*const &)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind_internal.h:285
    #14 0x7f88272c2b50 in RunImpl<void (*const &)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), const std::__1::tuple<base::internal::PassedWrapper<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > > &, 0> base/bind_internal.h:361
    #15 0x7f88272c2b50 in base::internal::Invoker<base::internal::BindState<void (*)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), base::internal::PassedWrapper<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:339
    #16 0x7f882350f17d in Run base/callback.h:68:12
    #17 0x7f882350f17d in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:52
    #18 0x7f8823306b2f in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:413:19
    #19 0x7f88233079bf in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:422:5
    #20 0x7f882330977b in base::MessageLoop::DoDelayedWork(base::TimeTicks*) base/message_loop/message_loop.cc:554:10
    #21 0x7f8823314f62 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:37:27
    #22 0x7f8823305a43 in base::MessageLoop::RunHandler() base/message_loop/message_loop.cc:378:10
    #23 0x7f88233a2724 in base::RunLoop::Run() base/run_loop.cc:37:10
    #24 0x7f8821cd9926 in content::PpapiPluginMain(content::MainFunctionParams const&) content/ppapi_plugin/ppapi_plugin_main.cc:157:19
    #25 0x7f88223cb0af in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:344:14
    #26 0x7f88223cf3b3 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:793:12
    #27 0x7f88223ca12d in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:20:28
    #28 0x7f881c380750 in ChromeMain chrome/app/chrome_main.cc:112:12
    #29 0x7f8810f1cf44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

0x60200001bfa8 is located 8 bytes to the right of 16-byte region [0x60200001bf90,0x60200001bfa0)
allocated by thread T0 (chrome) here:
    #0 0x7f881c37d41b in operator new(unsigned long) (/home/ashfaq/asan-linux-release-439448/chrome+0x2fd441b)
    #1 0x7f8822440271 in __allocate buildtools/third_party/libc++/trunk/include/new:168:10
    #2 0x7f8822440271 in allocate buildtools/third_party/libc++/trunk/include/memory:1729
    #3 0x7f8822440271 in allocate buildtools/third_party/libc++/trunk/include/memory:1488
    #4 0x7f8822440271 in allocate buildtools/third_party/libc++/trunk/include/vector:930
    #5 0x7f8822440271 in std::__1::vector<PP_PrivateAccessibilityCharInfo, std::__1::allocator<PP_PrivateAccessibilityCharInfo> >::vector(unsigned long) buildtools/third_party/libc++/trunk/include/vector:1072
    #6 0x7f882243f2b1 in chrome_pdf::OutOfProcessInstance::SendNextAccessibilityPage(int) pdf/out_of_process_instance.cc:755:48
    #7 0x7f8822453ac9 in operator() ppapi/utility/completion_callback_factory.h:607:9
    #8 0x7f8822453ac9 in pp::CompletionCallbackFactory<chrome_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome_pdf::OutOfProcessInstance, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome_pdf::OutOfProcessInstance::*)(int)> >::Thunk(void*, int) ppapi/utility/completion_callback_factory.h:584
    #9 0x7f88272da33e in PP_RunCompletionCallback ppapi/c/pp_completion_callback.h:240:3
    #10 0x7f88272da33e in CallWhileUnlocked<void, PP_CompletionCallback *, int, PP_CompletionCallback *, int> ppapi/shared_impl/proxy_lock.h:135
    #11 0x7f88272da33e in ppapi::proxy::(anonymous namespace)::CallbackWrapper(PP_CompletionCallback, int) ppapi/proxy/ppb_core_proxy.cc:52
    #12 0x7f88272da8aa in Invoke<const PP_CompletionCallback &, const int &> base/bind_internal.h:164:12
    #13 0x7f88272da8aa in MakeItSo<void (*const &)(PP_CompletionCallback, int), const PP_CompletionCallback &, const int &> base/bind_internal.h:285
    #14 0x7f88272da8aa in RunImpl<void (*const &)(PP_CompletionCallback, int), const std::__1::tuple<PP_CompletionCallback, int> &, 0, 1> base/bind_internal.h:361
    #15 0x7f88272da8aa in base::internal::Invoker<base::internal::BindState<void (*)(PP_CompletionCallback, int), PP_CompletionCallback, int>, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:339
    #16 0x7f88272c28f9 in Run base/callback.h:85:12
    #17 0x7f88272c28f9 in ppapi::internal::RunWhileLockedHelper<void ()>::CallWhileLocked(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >) ppapi/shared_impl/proxy_lock.h:199
    #18 0x7f88272c2b50 in Invoke<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind_internal.h:164:12
    #19 0x7f88272c2b50 in MakeItSo<void (*const &)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind_internal.h:285
    #20 0x7f88272c2b50 in RunImpl<void (*const &)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), const std::__1::tuple<base::internal::PassedWrapper<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > > &, 0> base/bind_internal.h:361
    #21 0x7f88272c2b50 in base::internal::Invoker<base::internal::BindState<void (*)(std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > >), base::internal::PassedWrapper<std::__1::unique_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::__1::default_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:339
    #22 0x7f882350f17d in Run base/callback.h:68:12
    #23 0x7f882350f17d in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:52
    #24 0x7f8823306b2f in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:413:19
    #25 0x7f88233079bf in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:422:5
    #26 0x7f882330977b in base::MessageLoop::DoDelayedWork(base::TimeTicks*) base/message_loop/message_loop.cc:554:10
    #27 0x7f8823314f62 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:37:27
    #28 0x7f8823305a43 in base::MessageLoop::RunHandler() base/message_loop/message_loop.cc:378:10
    #29 0x7f88233a2724 in base::RunLoop::Run() base/run_loop.cc:37:10
    #30 0x7f8821cd9926 in content::PpapiPluginMain(content::MainFunctionParams const&) content/ppapi_plugin/ppapi_plugin_main.cc:157:19
    #31 0x7f88223cb0af in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:344:14
    #32 0x7f88223cf3b3 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:793:12
    #33 0x7f88223ca12d in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:20:28
    #34 0x7f881c380750 in ChromeMain chrome/app/chrome_main.cc:112:12
    #35 0x7f8810f1cf44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

SUMMARY: AddressSanitizer: heap-buffer-overflow pdf/out_of_process_instance.cc:789:58 in chrome_pdf::OutOfProcessInstance::SendNextAccessibilityPage(int)
Shadow bytes around the buggy address:
  0x0c047fffb7a0: fa fa 00 fa fa fa 05 fa fa fa fd fa fa fa fd fd
  0x0c047fffb7b0: fa fa 00 00 fa fa fd fa fa fa 00 00 fa fa fd fd
  0x0c047fffb7c0: fa fa 00 00 fa fa 00 04 fa fa fd fd fa fa 00 fa
  0x0c047fffb7d0: fa fa 00 fa fa fa 04 fa fa fa fd fd fa fa 00 fa
  0x0c047fffb7e0: fa fa fd fd fa fa 00 fa fa fa fd fa fa fa 04 fa
=>0x0c047fffb7f0: fa fa 00 00 fa[fa]fa fa fa fa fa fa fa fa fa fa
  0x0c047fffb800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffb810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffb820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffb830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffb840: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==323==ABORTING


### mo...@gmail.com (2016-12-22)

it's almost a month this bug is open

### sh...@chromium.org (2016-12-24)

dmazzoni: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2017-01-09)

dmazzoni: Could you please take a look? This is marked high severity. Thanks!

### mo...@gmail.com (2017-01-16)

you are about to reach 90 days

### sh...@chromium.org (2017-01-25)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-30)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/src-internal.git/+/7acbd12d090ad52e9ff57327d8f8957f5760ec62

commit 7acbd12d090ad52e9ff57327d8f8957f5760ec62
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Mon Jan 30 23:33:50 2017


### mo...@gmail.com (2017-02-22)

What happened to this bug report? Any CVE assigned for the same?

### ra...@chromium.org (2017-02-22)

dmazzoni: this is fixed now right?

This is an OOB read in a renderer process which is classes as medium severity as per https://www.chromium.org/developers/severity-guidelines

+awhalley for CVE/reward info.

### dm...@chromium.org (2017-02-22)

For the record, here's the change that fixed it. Not sure why it didn't end up in the bug.

commit e4e4b0140002c58d760bf8d9f3fcfd7d29343486
Author:     dmazzoni <dmazzoni@chromium.org>
AuthorDate: Tue Jan 31 22:12:33 2017
Commit:     Commit bot <commit-bot@chromium.org>
CommitDate: Tue Jan 31 22:12:33 2017

    Fix buffer overrun in PDF accessibility code.

    GetTextRunInfo scans until it finds the start of the next text run,
    then increments the character index by 1 in order to scan to the end of
    the text run. That was resulting in a buffer ovverun if the first scan
    reached the end of the array of characters without finding a non-whitespace
    character. Fix it by ensuring we never increment past the char count.

    BUG=668724

    Review-Url: https://codereview.chromium.org/2650513002
    Cr-Commit-Position: refs/heads/master@{#447344}


### mo...@gmail.com (2017-02-23)

I don't think this is OOB Read, if you look at the crash log/ASAN log it's OOB Write. I'm not sure if OOB Writes are Medium priority? :-)

### sh...@chromium.org (2017-02-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-24)

Now that it's marked as fixed it's entered the queue for reward consideration. And it looks to be CVE eligible, I'll include it in the next run for M57.

### ra...@chromium.org (2017-02-27)

My understanding is that OOB writes in the renderer fall under Medium too. Memory corruption of the browser process is what tends to be regarded as high severity.

### th...@chromium.org (2017-02-27)

Looks like we should request a merge for M57.

### js...@chromium.org (2017-02-27)

OOB writes in the renderer are high-severity. And this should definitely be merged, assuming the patch is reasonably low rix.

### th...@chromium.org (2017-02-27)

~1 line fix: https://codereview.chromium.org/2650513002/diff/60001/pdf/pdfium/pdfium_page.cc so requesting merge.

### th...@chromium.org (2017-02-27)

Pending merge: https://codereview.chromium.org/2720933002

### js...@chromium.org (2017-02-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2da67ac9be739d36752e4b0c52c409d0a3bfec2d

commit 2da67ac9be739d36752e4b0c52c409d0a3bfec2d
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Feb 27 23:38:00 2017

M57: Fix buffer overrun in PDF accessibility code.

GetTextRunInfo scans until it finds the start of the next text run,
then increments the character index by 1 in order to scan to the end of
the text run. That was resulting in a buffer ovverun if the first scan
reached the end of the array of characters without finding a non-whitespace
character. Fix it by ensuring we never increment past the char count.

BUG=668724

Review-Url: https://codereview.chromium.org/2650513002
Cr-Commit-Position: refs/heads/master@{#447344}
(cherry picked from commit e4e4b0140002c58d760bf8d9f3fcfd7d29343486)

Review-Url: https://codereview.chromium.org/2720933002 .
Cr-Commit-Position: refs/branch-heads/2987@{#707}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[modify] https://crrev.com/2da67ac9be739d36752e4b0c52c409d0a3bfec2d/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/2da67ac9be739d36752e4b0c52c409d0a3bfec2d/pdf/pdfium/pdfium_page.cc


### th...@chromium.org (2017-02-27)

Merged. Do we still need the Deadline-Exceeded label?

### aw...@chromium.org (2017-02-28)

Thanks! Re D-E - keep it on for now and I'll double check how it's currently used for stats gathering.

### aw...@chromium.org (2017-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-05)

Congratulations! The panel awarded $3,000 for this bug. Note that the reward might well have been higher if there'd been a demonstration of exploitatablilty. A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/668724?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086082)*
