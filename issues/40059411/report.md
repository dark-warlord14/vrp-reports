# Security: webgl2 CompileShader Heap Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40059411](https://issues.chromium.org/issues/40059411) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | kh...@gmail.com |
| **Assignee** | jm...@chromium.org |
| **Created** | 2022-04-19 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

I fuzz with my fuzzing and found a vulnerability relative webgl2, and a Heap Corruption vulnerability occurs in the GL\_CompileShader function in libGLESv2.dll.

**VERSION**  

Chrome Version: 102.0.4997.0 dev  

Operating System: Windows 10 Professional Version 21H2 (OS Build 19044.1645)

**REPRODUCTION CASE**

1. Execute chrome.exe with Windbg with arguments: the path of poc.html file and enable "debug child processes "
2. Result: the exception occurs in libglesv2!ANGLEResetDisplayPlatform+0x3ebe0c

NOTE: You can run with poc\_primitive.html if not exceptions do not occur when poc.html runs or run repeat a few times.

**CREDIT INFORMATION**  

Reporter credit: khangkito - Tran Van Khang (VinCSS)

## Attachments

- [bugcheck.txt](attachments/bugcheck.txt) (text/plain, 44.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 3.4 KB)
- [poc_primitive.html](attachments/poc_primitive.html) (text/plain, 85.2 KB)
- [HeapFree_exceptions.PNG](attachments/HeapFree_exceptions.PNG) (image/png, 67.3 KB)
- [run_poc.mp4](attachments/run_poc.mp4) (video/mp4, 13.5 MB)

## Timeline

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Will - Since I don't have a windows box readily available, could you be kind enough to check if poc.html above reproduces for you? Thanks.

### ts...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### wf...@chromium.org (2022-04-19)

I get

2:039> k
 # Child-SP          RetAddr           Call Site
00 0000005d`6dffd5d0 00007ffe`42b17f92 ntdll!RtlReportCriticalFailure+0x56
01 0000005d`6dffd6c0 00007ffe`42b1827a ntdll!RtlpHeapHandleError+0x12
02 0000005d`6dffd6f0 00007ffe`42b1df01 ntdll!RtlpHpHeapHandleError+0x7a
03 0000005d`6dffd720 00007ffe`42a35bf0 ntdll!RtlpLogHeapFailure+0x45
04 0000005d`6dffd750 00007ffe`42a347b1 ntdll!RtlpFreeHeapInternal+0x4e0
*** WARNING: Unable to verify checksum for C:\src\chromium\src\out\goma64\libglesv2.dll
05 0000005d`6dffd810 00007ffd`928908ec ntdll!RtlFreeHeap+0x51
06 0000005d`6dffd850 00007ffd`9202a718 libglesv2!_free_base+0x1c [c:\src\chromium\src\out\goma64\minkernel\crts\ucrt\src\appcrt\heap\free_base.cpp @ 105] 
07 (Inline Function) --------`-------- libglesv2!std::__1::__libcpp_operator_delete+0xa [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\new @ 245] 
08 (Inline Function) --------`-------- libglesv2!std::__1::__do_deallocate_handle_size+0xa [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\new @ 269] 
09 (Inline Function) --------`-------- libglesv2!std::__1::__libcpp_deallocate+0xa [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\new @ 279] 
0a (Inline Function) --------`-------- libglesv2!std::__1::allocator<char>::deallocate+0xa [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator.h @ 91] 
0b (Inline Function) --------`-------- libglesv2!std::__1::allocator_traits<std::__1::allocator<char> >::deallocate+0xa [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h @ 281] 
0c 0000005d`6dffd880 00007ffd`92068f95 libglesv2!std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >::__grow_by_and_replace+0x22a [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\string @ 2268] 
0d 0000005d`6dffd930 00007ffd`9211dbad libglesv2!std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >::__assign_no_alias<0>+0xcd [c:\src\chromium\src\buildtools\third_party\libc++\trunk\include\string @ 2321] 
0e 0000005d`6dffd9d0 00007ffd`9211ec1b libglesv2!gl::Shader::resolveCompile+0x331 [c:\src\chromium\src\third_party\angle\src\libANGLE\Shader.cpp @ 472] 
0f 0000005d`6dffdbd0 00007ffd`92035461 libglesv2!gl::Shader::compile+0x37 [c:\src\chromium\src\third_party\angle\src\libANGLE\Shader.cpp @ 318] 
*** WARNING: Unable to verify checksum for C:\src\chromium\src\out\goma64\chrome.dll
10 0000005d`6dffdda0 00007ffd`9916023d libglesv2!GL_CompileShader+0x81 [c:\src\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp @ 549] 
11 0000005d`6dffddf0 00007ffd`9bfaedb4 chrome!gl::GLApiBase::glCompileShaderFn+0xcd [c:\src\chromium\src\ui\gl\gl_bindings_autogen_gl.cc @ 3367] 
12 0000005d`6dffde40 00007ffd`9a80816b chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCompileShader+0x38 [c:\src\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc @ 776] 
13 0000005d`6dffde70 00007ffd`9a807cfc chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>+0xd9 [c:\src\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 870] 
14 0000005d`6dffdee0 00007ffd`994d60f6 chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands+0x2c [c:\src\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 811] 
15 0000005d`6dffdf10 00007ffd`983a1852 chrome!gpu::CommandBufferService::Flush+0x1a4 [c:\src\chromium\src\gpu\command_buffer\service\command_buffer_service.cc @ 73] 
16 0000005d`6dffdff0 00007ffd`983a11a1 chrome!gpu::CommandBufferStub::OnAsyncFlush+0x3fa [c:\src\chromium\src\gpu\ipc\service\command_buffer_stub.cc @ 501] 
17 0000005d`6dffe250 00007ffd`983a6a9f chrome!gpu::CommandBufferStub::ExecuteDeferredRequest+0xb9 [c:\src\chromium\src\gpu\ipc\service\command_buffer_stub.cc @ 152] 
18 0000005d`6dffe320 00007ffd`94ad73dc chrome!gpu::GpuChannel::ExecuteDeferredRequest+0xef [c:\src\chromium\src\gpu\ipc\service\gpu_channel.cc @ 673] 
19 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (content::BackgroundSyncManager::*)(base::OnceCallback<void ()>),void>::Invoke+0x28 [c:\src\chromium\src\base\bind_internal.h @ 542] 
1a (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<1,void>::MakeItSo+0x3f [c:\src\chromium\src\base\bind_internal.h @ 726] 
1b (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncManager::*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncManager>,base::OnceCallback<void ()> >,void ()>::RunImpl+0x3f [c:\src\chromium\src\base\bind_internal.h @ 779] 
1c 0000005d`6dffe4d0 00007ffd`9822e744 chrome!base::internal::Invoker<base::internal::BindState<void (content::BackgroundSyncManager::*)(base::OnceCallback<void ()>),base::WeakPtr<content::BackgroundSyncManager>,base::OnceCallback<void ()> >,void ()>::RunOnce+0x5c [c:\src\chromium\src\base\bind_internal.h @ 752] 
1d (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x34 [c:\src\chromium\src\base\callback.h @ 143] 
1e 0000005d`6dffe520 00007ffd`979e3eb0 chrome!gpu::Scheduler::RunNextTask+0x584 [c:\src\chromium\src\gpu\command_buffer\service\scheduler.cc @ 691] 
1f (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x52 [c:\src\chromium\src\base\callback.h @ 143] 
20 0000005d`6dffe640 00007ffd`98bc0683 chrome!base::TaskAnnotator::RunTaskImpl+0x180 [c:\src\chromium\src\base\task\common\task_annotator.cc @ 135] 
21 (Inline Function) --------`-------- chrome!base::TaskAnnotator::RunTask+0x1a [c:\src\chromium\src\base\task\common\task_annotator.h @ 74] 
22 0000005d`6dffe6f0 00007ffd`98bbfc62 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x483 [c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 386] 
23 0000005d`6dffe8d0 00007ffd`98baaa8b chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0xa2 [c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 297] 
24 0000005d`6dffe9c0 00007ffd`98bc1bfe chrome!base::MessagePumpDefault::Run+0x9b [c:\src\chromium\src\base\message_loop\message_pump_default.cc @ 41] 
25 0000005d`6dffea70 00007ffd`979bfdb7 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x38e [c:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 501] 
26 0000005d`6dffeaf0 00007ffd`988d98b6 chrome!base::RunLoop::Run+0x367 [c:\src\chromium\src\base\run_loop.cc @ 143] 
27 0000005d`6dffec00 00007ffd`97829e44 chrome!content::GpuMain+0x586 [c:\src\chromium\src\content\gpu\gpu_main.cc @ 404] 
28 0000005d`6dffef50 00007ffd`9782b608 chrome!content::RunOtherNamedProcessTypeMain+0x2d7 [c:\src\chromium\src\content\app\content_main_runner_impl.cc @ 682] 
29 0000005d`6dfff090 00007ffd`9782958e chrome!content::ContentMainRunnerImpl::Run+0x2f8 [c:\src\chromium\src\content\app\content_main_runner_impl.cc @ 1021] 
2a 0000005d`6dfff1b0 00007ffd`9782969c chrome!content::RunContentProcess+0x65b [c:\src\chromium\src\content\app\content_main.cc @ 407] 
2b 0000005d`6dfff410 00007ffd`931612a3 chrome!content::ContentMain+0x54 [c:\src\chromium\src\content\app\content_main.cc @ 435] 
*** WARNING: Unable to verify checksum for chrome.exe
2c 0000005d`6dfff490 00007ff6`568f2dbd chrome!ChromeMain+0x203 [c:\src\chromium\src\chrome\app\chrome_main.cc @ 177] 
2d 0000005d`6dfff620 00007ff6`568f1c84 chrome_exe!MainDllLoader::Launch+0x151 [c:\src\chromium\src\chrome\app\main_dll_loader_win.cc @ 167] 
2e 0000005d`6dfff6f0 00007ff6`56b01162 chrome_exe!wWinMain+0xc65 [c:\src\chromium\src\chrome\app\chrome_exe_main_win.cc @ 382] 
2f (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
30 0000005d`6dfffb40 00007ffe`40a87034 chrome_exe!__scrt_common_main_seh+0x106 [d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
31 0000005d`6dfffb80 00007ffe`42a62651 KERNEL32!BaseThreadInitThunk+0x14
32 0000005d`6dfffbb0 00000000`00000000 ntdll!RtlUserThreadStart+0x21


chrome version 103.0.5012.0 dcb7467824362dc1fb5b6dcad5ef78160e4ba737

### ts...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### ts...@chromium.org (2022-04-19)

Assigning per angle/OWNERS. Please feel free to re-assign as appropriate.

### ad...@google.com (2022-04-19)

(auto-cc on security bug)

### ts...@chromium.org (2022-04-21)

Setting high severity based on presumed heap corruption.

### ts...@chromium.org (2022-04-21)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-03)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-05-04)

geofflang@, syoussefi@, jmadill@: Friendly ping about the status of this bug. There has been no movement on this issue for a while.

### jm...@chromium.org (2022-05-05)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-05-09)

This may be a race condition between CompileShader and LinkProgram. During a Link call, we can still re-compile the shaders attached to the program IIUC. There should be some kind of mutex applied to the shaders to ensure they don't get modified during a link call.

### jm...@chromium.org (2022-05-09)

Yang: Is there anyone on the Intel team who worked on the parallel shader compilation feature? Can they confirm if my theory in https://crbug.com/chromium/1317673#c14 is correct?

### [Deleted User] (2022-05-10)

[Empty comment from Monorail migration]

### ji...@intel.com (2022-05-10)

Jamie: I am not exactly sure about the race condition. But the design assumption was that, for the Shader class, "compile()" is the only method to have the write access, and all other read "get*()" used by LinkProgram, and etc. are checked by resolveCompile, which in turn uses std::unique_lock as protection. In this sense, we should not have that race condition.

### me...@google.com (2022-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-10)

[Empty comment from Monorail migration]

### ji...@intel.com (2022-05-10)

Is it reproducible on the current stable build like 101.0.4951.54? If this is a 102 dev build regression. Maybe we can try to bisect the issue.

### [Deleted User] (2022-05-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-05-11)

Reading through the implementation of Shader, Program, and so forth, it does look like every time the program queries any of its attached shaders, it goes through an accessor which calls Shader::resolveCompile. Even though there's no guard on the creation of Shader::mCompilingState, since the user's access to the shaders and program is single-threaded, waiting on the WaitableEvent should ensure that program linking doesn't race with compiles. Again since the user's access is single-threaded, changing the attached shaders on the program won't happen in the middle of linking.

I wonder how crucial the periodic window.location.reload() calls are in the test cases, and whether those could potentially cause ANGLE's context to be destroyed while shader compiles are still happening in a worker thread.


### jm...@chromium.org (2022-05-11)

jie: This should be reproducible on many versions of Chrome including stable/beta/dev/canary. Can you take a look at the repro case in the description? Thanks if you can help.

### jm...@chromium.org (2022-05-11)

Actually, I am not sure it repros in stable.. at least it didn't when I just tried it. It would require a more careful check to ensure there's no corruption happening despite no obvious crash.

### ji...@intel.com (2022-05-11)

Jamie: No problem, I will take a look.

### ji...@intel.com (2022-05-12)

Jamie: I was able to reproduce the issue on my laptop with my local chromium(102.0.4997.0) build. Fortunately ASAN caught the suspicious double-free below:

=================================================================
==23992==ERROR: AddressSanitizer: attempting double-free on 0x12a4c1a5de80 in thread T15:
==23992==WARNING: Failed to use and restart external symbolizer!
==23992==*** WARNING: Failed to initialize DbgHelp!              ***
==23992==*** Most likely this means that the app is already      ***
==23992==*** using DbgHelp, possibly with incompatible flags.    ***
==23992==*** Due to technical reasons, symbolization might crash ***
==23992==*** or produce wrong results.                           ***
    #0 0x7ff7545e094b in free+0x8b (c:\workspace\bugs\1317673\asan\Chrome-bin\chrome.exe+0x1400c094b)
    #1 0x7ffc43abbcc1 in Ordinal0+0x1bcc1 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x18001bcc1)
    #2 0x7ffc43b29ae9 in glFramebufferTextureMultiviewOVR+0xe65e (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180089ae9)
    #3 0x7ffc43d487a2 in ANGLEResetDisplayPlatform+0xc4735 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802a87a2)
    #4 0x7ffc43d4d8d0 in ANGLEResetDisplayPlatform+0xc9863 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802ad8d0)
    #5 0x7ffc44599bc6 in ANGLEResetDisplayPlatform+0x915b59 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180af9bc6)
    #6 0x7ffc445b8867 in ANGLEResetDisplayPlatform+0x9347fa (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180b18867)
    #7 0x7ffc445b7195 in ANGLEResetDisplayPlatform+0x933128 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180b17195)
    #8 0x7ffc43df81c3 in ANGLEResetDisplayPlatform+0x174156 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1803581c3)
    #9 0x7ffc1121ce92 in GetMainTargetServices+0x3efce5 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e2ace92)
    #10 0x7ffc18ccd61d in GetHandleVerifier+0x436660d (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x195d5d61d)
    #11 0x7ffc18cce112 in GetHandleVerifier+0x4367102 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x195d5e112)
    #12 0x7ffc18ccbfe2 in GetHandleVerifier+0x4364fd2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x195d5bfe2)
    #13 0x7ffc18ccad7f in GetHandleVerifier+0x4363d6f (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x195d5ad7f)
    #14 0x7ffc1e142c8f in GetHandleVerifier+0x97dbc7f (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19b1d2c8f)
    #15 0x7ffc1e141d9b in GetHandleVerifier+0x97dad8b (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19b1d1d9b)
    #16 0x7ffc1133ed70 in GetMainTargetServices+0x511bc3 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e3ced70)
    #17 0x7ff7545eb203 in _asan_print_accumulated_stats+0x1523 (c:\workspace\bugs\1317673\asan\Chrome-bin\chrome.exe+0x1400cb203)
    #18 0x7ffcd6327033 in BaseThreadInitThunk+0x13 (C:\windows\System32\KERNEL32.DLL+0x180017033)
    #19 0x7ffcd79a2650 in RtlUserThreadStart+0x20 (C:\windows\SYSTEM32\ntdll.dll+0x180052650)

0x12a4c1a5de80 is located 0 bytes inside of 768-byte region [0x12a4c1a5de80,0x12a4c1a5e180)
freed by thread T0 here:
    #0 0x7ff7545e094b in free+0x8b (c:\workspace\bugs\1317673\asan\Chrome-bin\chrome.exe+0x1400c094b)
    #1 0x7ffc43abbcc1 in Ordinal0+0x1bcc1 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x18001bcc1)
    #2 0x7ffc43b29ae9 in glFramebufferTextureMultiviewOVR+0xe65e (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180089ae9)
    #3 0x7ffc43d487a2 in ANGLEResetDisplayPlatform+0xc4735 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802a87a2)
    #4 0x7ffc43d4bdc9 in ANGLEResetDisplayPlatform+0xc7d5c (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802abdc9)
    #5 0x7ffc43ad54e8 in GL_CompileShader+0xbd (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1800354e8)
    #6 0x7ffc1eb55be4 in GetHandleVerifier+0xa1eebd4 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19bbe5be4)
    #7 0x7ffc19fa845d in GetHandleVerifier+0x564144d (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19703845d)
    #8 0x7ffc19fa78b2 in GetHandleVerifier+0x56408a2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1970378b2)
    #9 0x7ffc163c9630 in GetHandleVerifier+0x1a62620 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x193459630)
    #10 0x7ffc12f908d4 in GetMainTargetServices+0x2163727 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1900208d4)
    #11 0x7ffc12f8f620 in GetMainTargetServices+0x2162473 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19001f620)
    #12 0x7ffc12fa0a8c in GetMainTargetServices+0x21738df (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x190030a8c)
    #13 0x7ffc12fac11d in GetMainTargetServices+0x217ef70 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19003c11d)
    #14 0x7ffc12ad3571 in GetMainTargetServices+0x1ca63c4 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18fb63571)
    #15 0x7ffc1121ce92 in GetMainTargetServices+0x3efce5 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e2ace92)
    #16 0x7ffc1492f422 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3a8e44 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919bf422)
    #17 0x7ffc1492dcb7 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3a76d9 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919bdcb7)
    #18 0x7ffc148f9a09 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x37342b (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x191989a09)
    #19 0x7ffc149319b3 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3ab3d5 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919c19b3)
    #20 0x7ffc11192f8f in GetMainTargetServices+0x365de2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e222f8f)
    #21 0x7ffc14085234 in GetMainTargetServices+0x3258087 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x191115234)
    #22 0x7ffc10d03612 in CrashForExceptionInNonABICompliantCodeRange+0x2af9ed2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18dd93612)
    #23 0x7ffc10d05762 in CrashForExceptionInNonABICompliantCodeRange+0x2afc022 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18dd95762)
    #24 0x7ffc10d0188d in CrashForExceptionInNonABICompliantCodeRange+0x2af814d (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18dd9188d)
    #25 0x7ffc10d02026 in CrashForExceptionInNonABICompliantCodeRange+0x2af88e6 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18dd92026)
    #26 0x7ffc02f714b8 in ChromeMain+0x3b4 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1800014b8)
    #27 0x7ff754527aca in GetPakFileHashes+0x6aca (c:\workspace\bugs\1317673\asan\Chrome-bin\chrome.exe+0x140007aca)

previously allocated by thread T0 here:
    #0 0x7ff7545e0a4b in malloc+0x8b (c:\workspace\bugs\1317673\asan\Chrome-bin\chrome.exe+0x1400c0a4b)
    #1 0x7ffc4534244a in ANGLEResetDisplayPlatform+0x16be3dd (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1818a244a)
    #2 0x7ffc43abb949 in Ordinal0+0x1b949 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x18001b949)
    #3 0x7ffc43b29779 in glFramebufferTextureMultiviewOVR+0xe2ee (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x180089779)
    #4 0x7ffc43d487a2 in ANGLEResetDisplayPlatform+0xc4735 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802a87a2)
    #5 0x7ffc43d4d706 in ANGLEResetDisplayPlatform+0xc9699 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1802ad706)
    #6 0x7ffc43c9ba5f in ANGLEResetDisplayPlatform+0x179f2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1801fba5f)
    #7 0x7ffc43c99e09 in ANGLEResetDisplayPlatform+0x15d9c (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1801f9e09)
    #8 0x7ffc43c99872 in ANGLEResetDisplayPlatform+0x15805 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x1801f9872)
    #9 0x7ffc43bac5b4 in glFramebufferTextureMultiviewOVR+0x91129 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x18010c5b4)
    #10 0x7ffc43add07b in GL_LinkProgram+0xbd (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\libglesv2.dll+0x18003d07b)
    #11 0x7ffc1eb6a52b in GetHandleVerifier+0xa20351b (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19bbfa52b)
    #12 0x7ffc19fa845d in GetHandleVerifier+0x564144d (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19703845d)
    #13 0x7ffc19fa78b2 in GetHandleVerifier+0x56408a2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1970378b2)
    #14 0x7ffc163c9630 in GetHandleVerifier+0x1a62620 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x193459630)
    #15 0x7ffc12f908d4 in GetMainTargetServices+0x2163727 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1900208d4)
    #16 0x7ffc12f8f620 in GetMainTargetServices+0x2162473 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19001f620)
    #17 0x7ffc12fa0a8c in GetMainTargetServices+0x21738df (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x190030a8c)
    #18 0x7ffc12fac11d in GetMainTargetServices+0x217ef70 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x19003c11d)
    #19 0x7ffc12ad3571 in GetMainTargetServices+0x1ca63c4 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18fb63571)
    #20 0x7ffc1121ce92 in GetMainTargetServices+0x3efce5 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e2ace92)
    #21 0x7ffc1492f422 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3a8e44 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919bf422)
    #22 0x7ffc1492dcb7 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3a76d9 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919bdcb7)
    #23 0x7ffc148f9a09 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x37342b (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x191989a09)
    #24 0x7ffc149319b3 in RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x3ab3d5 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x1919c19b3)
    #25 0x7ffc11192f8f in GetMainTargetServices+0x365de2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18e222f8f)
    #26 0x7ffc14085234 in GetMainTargetServices+0x3258087 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x191115234)
    #27 0x7ffc10d03612 in CrashForExceptionInNonABICompliantCodeRange+0x2af9ed2 (c:\workspace\bugs\1317673\asan\Chrome-bin\102.0.4997.0\chrome.dll+0x18dd93612)

Let me know if you have any idea on this. I will continue work on it.

### jm...@chromium.org (2022-05-12)

Those stacks look incorrect. ANGLEResetDisplayPlatform shouldn't show up like that. Not sure how the symbolizer is getting so confused.

### ji...@intel.com (2022-05-12)

The chromium was built from my Win11 desktop, not sure whether this matters.
I am setting up the build environment on my laptop. But It takes very long time to build chromium on laptops. I will retry once it's done.

### sr...@google.com (2022-05-12)

M102 stable RC is next week and this is marked as RBS for M102 . Is this confirmed a M102 regression and must be fixed for M102?

### ji...@intel.com (2022-05-13)

Jamie: I managed to get the right log below. According to that, I think the root cause is that we shouldn't have allowed Shader to start another compile(), when the Programs, that are using the Shader, haven't finished the linking. The fixing CL is https://chromium-review.googlesource.com/c/angle/angle/+/3646590


=================================================================
==27508==ERROR: AddressSanitizer: attempting double-free on 0x11d92ce1dd00 in thread T15:
    #0 0x7ff76b6a094b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc5229bcc1 in std::__1::__libcpp_operator_delete c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:245
    #2 0x7ffc5229bcc1 in std::__1::__do_deallocate_handle_size c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:269
    #3 0x7ffc5229bcc1 in std::__1::__libcpp_deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:279
    #4 0x7ffc5229bcc1 in std::__1::allocator<char>::deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator.h:91
    #5 0x7ffc5229bcc1 in std::__1::allocator_traits<std::__1::allocator<char> >::deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h:281
    #6 0x7ffc5229bcc1 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__grow_by_and_replace(unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, char const *) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2267:9
    #7 0x7ffc52309ae9 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__assign_no_alias<0>(char const *, unsigned __int64) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2319:5
    #8 0x7ffc525287a2 in gl::Shader::resolveCompile(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:439:34
    #9 0x7ffc5252d8d0 in gl::Shader::getActiveAttributes(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:686:5
    #10 0x7ffc52d79bc6 in rx::`anonymous namespace'::GetDefaultInputLayoutFromShader c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\ProgramD3D.cpp:53
    #11 0x7ffc52d79bc6 in rx::ProgramD3D::updateCachedInputLayoutFromShader(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\ProgramD3D.cpp:1701:5
    #12 0x7ffc52d98867 in rx::ProgramD3D::GetVertexExecutableTask::run(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\ProgramD3D.cpp:1691:19
    #13 0x7ffc52d97195 in rx::ProgramD3D::GetExecutableTask::operator()(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\renderer\d3d\ProgramD3D.cpp:550:44
    #14 0x7ffc525d81c3 in angle::DelegateWorkerTask::RunTask(void *) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\WorkerThread.cpp:283:9
    #15 0x7ffc1120ce92 in base::OnceCallback<void ()>::Run c:\workspace\chromium\chromium\src\base\callback.h:143
    #16 0x7ffc1120ce92 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) c:\workspace\chromium\chromium\src\base\task\common\task_annotator.cc:135:32
    #17 0x7ffc18cbd65d in base::TaskAnnotator::RunTask c:\workspace\chromium\chromium\src\base\task\common\task_annotator.h:75
    #18 0x7ffc18cbd65d in base::internal::TaskTracker::RunTaskImpl(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::SequenceToken const &) c:\workspace\chromium\chromium\src\base\task\thread_pool\task_tracker.cc:709:19
    #19 0x7ffc18cbe152 in base::internal::TaskTracker::RunSkipOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::SequenceToken const &) c:\workspace\chromium\chromium\src\base\task\thread_pool\task_tracker.cc:694:3
    #20 0x7ffc18cbc022 in base::internal::TaskTracker::RunTaskWithShutdownBehavior c:\workspace\chromium\chromium\src\base\task\thread_pool\task_tracker.cc:727
    #21 0x7ffc18cbc022 in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) c:\workspace\chromium\chromium\src\base\task\thread_pool\task_tracker.cc:551:5
    #22 0x7ffc18cbadbf in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) c:\workspace\chromium\chromium\src\base\task\thread_pool\task_tracker.cc:469:5
    #23 0x7ffc1e132ccf in base::internal::WorkerThread::RunWorker(void) c:\workspace\chromium\chromium\src\base\task\thread_pool\worker_thread.cc:381:34
    #24 0x7ffc1e131ddb in base::internal::WorkerThread::RunPooledWorker(void) c:\workspace\chromium\chromium\src\base\task\thread_pool\worker_thread.cc:268:3
    #25 0x7ffc1132ed70 in base::`anonymous namespace'::ThreadFunc c:\workspace\chromium\chromium\src\base\threading\platform_thread_win.cc:129:13
    #26 0x7ff76b6ab203 in __asan::AsanThread::ThreadStart(unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:277
    #27 0x7ffcd6327033  (C:\windows\System32\KERNEL32.DLL+0x180017033)
    #28 0x7ffcd79a2650  (C:\windows\SYSTEM32\ntdll.dll+0x180052650)

0x11d92ce1dd00 is located 0 bytes inside of 768-byte region [0x11d92ce1dd00,0x11d92ce1e000)
freed by thread T0 here:
    #0 0x7ff76b6a094b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffc5229bcc1 in std::__1::__libcpp_operator_delete c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:245
    #2 0x7ffc5229bcc1 in std::__1::__do_deallocate_handle_size c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:269
    #3 0x7ffc5229bcc1 in std::__1::__libcpp_deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:279
    #4 0x7ffc5229bcc1 in std::__1::allocator<char>::deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator.h:91
    #5 0x7ffc5229bcc1 in std::__1::allocator_traits<std::__1::allocator<char> >::deallocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h:281
    #6 0x7ffc5229bcc1 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__grow_by_and_replace(unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, char const *) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2267:9
    #7 0x7ffc52309ae9 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__assign_no_alias<0>(char const *, unsigned __int64) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2319:5
    #8 0x7ffc525287a2 in gl::Shader::resolveCompile(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:439:34
    #9 0x7ffc5252bdc9 in gl::Shader::compile(class gl::Context const *) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:316:5
    #10 0x7ffc522b54e8 in GL_CompileShader c:\workspace\chromium\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:555:22
    #11 0x7ffc1eb45c24 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCompileShader(unsigned int) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:775:10
    #12 0x7ffc19f9849d in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int, void const volatile *, int, int *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:870:20
    #13 0x7ffc19f978f2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int, void const volatile *, int, int *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:808:12
    #14 0x7ffc163b9670 in gpu::CommandBufferService::Flush(int, class gpu::AsyncAPIInterface *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:70:18
    #15 0x7ffc12f80914 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, class std::__1::vector<struct gpu::SyncToken, class std::__1::allocator<struct gpu::SyncToken>> const &) c:\workspace\chromium\chromium\src\gpu\ipc\service\command_buffer_stub.cc:500:22
    #16 0x7ffc12f7f660 in gpu::CommandBufferStub::ExecuteDeferredRequest(class gpu::mojom::DeferredCommandBufferRequestParams &) c:\workspace\chromium\chromium\src\gpu\ipc\service\command_buffer_stub.cc:152:7
    #17 0x7ffc12f90acc in gpu::GpuChannel::ExecuteDeferredRequest(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>) c:\workspace\chromium\chromium\src\gpu\ipc\service\gpu_channel.cc:670:13
    #18 0x7ffc12f9c15d in base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),void>::Invoke c:\workspace\chromium\chromium\src\base\bind_internal.h:542
    #19 0x7ffc12f9c15d in base::internal::InvokeHelper<1,void>::MakeItSo c:\workspace\chromium\chromium\src\base\bind_internal.h:726
    #20 0x7ffc12f9c15d in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunImpl c:\workspace\chromium\chromium\src\base\bind_internal.h:779
    #21 0x7ffc12f9c15d in base::internal::Invoker<struct base::internal::BindState<void (__cdecl gpu::GpuChannel::*)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>), class base::WeakPtr<class gpu::GpuChannel>, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>>, (void)>::RunOnce(class base::internal::BindStateBase *) c:\workspace\chromium\chromium\src\base\bind_internal.h:748:12
    #22 0x7ffc12ac35b1 in base::OnceCallback<void ()>::Run c:\workspace\chromium\chromium\src\base\callback.h:143
    #23 0x7ffc12ac35b1 in gpu::Scheduler::RunNextTask(void) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\scheduler.cc:691:26
    #24 0x7ffc1120ce92 in base::OnceCallback<void ()>::Run c:\workspace\chromium\chromium\src\base\callback.h:143
    #25 0x7ffc1120ce92 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) c:\workspace\chromium\chromium\src\base\task\common\task_annotator.cc:135:32
    #26 0x7ffc1491f462 in base::TaskAnnotator::RunTask c:\workspace\chromium\chromium\src\base\task\common\task_annotator.h:75
    #27 0x7ffc1491f462 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:386:21
    #28 0x7ffc1491dcf7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:291:41
    #29 0x7ffc148e9a49 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) c:\workspace\chromium\chromium\src\base\message_loop\message_pump_default.cc:39:55
    #30 0x7ffc149219f3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:498:12
    #31 0x7ffc11182f8f in base::RunLoop::Run(class base::Location const &) c:\workspace\chromium\chromium\src\base\run_loop.cc:141:14
    #32 0x7ffc14075274 in content::GpuMain(struct content::MainFunctionParams) c:\workspace\chromium\chromium\src\content\gpu\gpu_main.cc:405:14
    #33 0x7ffc10cf3612 in content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) c:\workspace\chromium\chromium\src\content\app\content_main_runner_impl.cc:682:14
    #34 0x7ffc10cf5762 in content::ContentMainRunnerImpl::Run(void) c:\workspace\chromium\chromium\src\content\app\content_main_runner_impl.cc:1021:10
    #35 0x7ffc10cf188d in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) c:\workspace\chromium\chromium\src\content\app\content_main.cc:407:36
    #36 0x7ffc10cf2026 in content::ContentMain(struct content::ContentMainParams) c:\workspace\chromium\chromium\src\content\app\content_main.cc:435:10
    #37 0x7ffc02f614b8 in ChromeMain c:\workspace\chromium\chromium\src\chrome\app\chrome_main.cc:176:12
    #38 0x7ff76b5e7aca in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) c:\workspace\chromium\chromium\src\chrome\app\main_dll_loader_win.cc:167:12

previously allocated by thread T0 here:
    #0 0x7ff76b6a0a4b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffc53b2244a in operator new(unsigned __int64) d:\a01\_work\43\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffc5229b949 in std::__1::__libcpp_operator_new c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:235
    #3 0x7ffc5229b949 in std::__1::__libcpp_allocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\new:261
    #4 0x7ffc5229b949 in std::__1::allocator<char>::allocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator.h:82
    #5 0x7ffc5229b949 in std::__1::allocator_traits<std::__1::allocator<char> >::allocate c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h:261
    #6 0x7ffc5229b949 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__grow_by_and_replace(unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, unsigned __int64, char const *) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2255:19
    #7 0x7ffc52309779 in std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>>::__assign_no_alias<1>(char const *, unsigned __int64) c:\workspace\chromium\chromium\src\buildtools\third_party\libc++\trunk\include\string:2319:5
    #8 0x7ffc525287a2 in gl::Shader::resolveCompile(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:439:34
    #9 0x7ffc5252d706 in gl::Shader::isCompiled(void) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Shader.cpp:639:5
    #10 0x7ffc5247ba5f in gl::Program::linkValidateShaders(class gl::InfoLog &) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Program.cpp:2866:22
    #11 0x7ffc52479e09 in gl::Program::linkImpl(class gl::Context const *) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Program.cpp:1212:10
    #12 0x7ffc52479872 in gl::Program::link(class gl::Context const *) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Program.cpp:1182:28
    #13 0x7ffc5238c5b4 in gl::Context::linkProgram(struct gl::ShaderProgramID) c:\workspace\chromium\chromium\src\third_party\angle\src\libANGLE\Context.cpp:7263:5
    #14 0x7ffc522bd07b in GL_LinkProgram c:\workspace\chromium\chromium\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:2478:22
    #15 0x7ffc1eb5a56b in gpu::gles2::GLES2DecoderPassthroughImpl::DoLinkProgram(unsigned int) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc:2364:10
    #16 0x7ffc19f9849d in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<0>(unsigned int, void const volatile *, int, int *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:870:20
    #17 0x7ffc19f978f2 in gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands(unsigned int, void const volatile *, int, int *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc:808:12
    #18 0x7ffc163b9670 in gpu::CommandBufferService::Flush(int, class gpu::AsyncAPIInterface *) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\command_buffer_service.cc:70:18
    #19 0x7ffc12f80914 in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, class std::__1::vector<struct gpu::SyncToken, class std::__1::allocator<struct gpu::SyncToken>> const &) c:\workspace\chromium\chromium\src\gpu\ipc\service\command_buffer_stub.cc:500:22
    #20 0x7ffc12f7f660 in gpu::CommandBufferStub::ExecuteDeferredRequest(class gpu::mojom::DeferredCommandBufferRequestParams &) c:\workspace\chromium\chromium\src\gpu\ipc\service\command_buffer_stub.cc:152:7
    #21 0x7ffc12f90acc in gpu::GpuChannel::ExecuteDeferredRequest(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>) c:\workspace\chromium\chromium\src\gpu\ipc\service\gpu_channel.cc:670:13
    #22 0x7ffc12f9c15d in base::internal::FunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),void>::Invoke c:\workspace\chromium\chromium\src\base\bind_internal.h:542
    #23 0x7ffc12f9c15d in base::internal::InvokeHelper<1,void>::MakeItSo c:\workspace\chromium\chromium\src\base\bind_internal.h:726
    #24 0x7ffc12f9c15d in base::internal::Invoker<base::internal::BindState<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>),base::WeakPtr<gpu::GpuChannel>,mojo::StructPtr<gpu::mojom::DeferredRequestParams> >,void ()>::RunImpl c:\workspace\chromium\chromium\src\base\bind_internal.h:779
    #25 0x7ffc12f9c15d in base::internal::Invoker<struct base::internal::BindState<void (__cdecl gpu::GpuChannel::*)(class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>), class base::WeakPtr<class gpu::GpuChannel>, class mojo::StructPtr<class gpu::mojom::DeferredRequestParams>>, (void)>::RunOnce(class base::internal::BindStateBase *) c:\workspace\chromium\chromium\src\base\bind_internal.h:748:12
    #26 0x7ffc12ac35b1 in base::OnceCallback<void ()>::Run c:\workspace\chromium\chromium\src\base\callback.h:143
    #27 0x7ffc12ac35b1 in gpu::Scheduler::RunNextTask(void) c:\workspace\chromium\chromium\src\gpu\command_buffer\service\scheduler.cc:691:26
    #28 0x7ffc1120ce92 in base::OnceCallback<void ()>::Run c:\workspace\chromium\chromium\src\base\callback.h:143
    #29 0x7ffc1120ce92 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) c:\workspace\chromium\chromium\src\base\task\common\task_annotator.cc:135:32
    #30 0x7ffc1491f462 in base::TaskAnnotator::RunTask c:\workspace\chromium\chromium\src\base\task\common\task_annotator.h:75
    #31 0x7ffc1491f462 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence_manager::LazyNow *) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:386:21
    #32 0x7ffc1491dcf7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:291:41
    #33 0x7ffc148e9a49 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) c:\workspace\chromium\chromium\src\base\message_loop\message_pump_default.cc:39:55
    #34 0x7ffc149219f3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) c:\workspace\chromium\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:498:12
    #35 0x7ffc11182f8f in base::RunLoop::Run(class base::Location const &) c:\workspace\chromium\chromium\src\base\run_loop.cc:141:14
    #36 0x7ffc14075274 in content::GpuMain(struct content::MainFunctionParams) c:\workspace\chromium\chromium\src\content\gpu\gpu_main.cc:405:14
    #37 0x7ffc10cf3612 in content::RunOtherNamedProcessTypeMain(class std::__1::basic_string<char, struct std::__1::char_traits<char>, class std::__1::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) c:\workspace\chromium\chromium\src\content\app\content_main_runner_impl.cc:682:14


### sr...@google.com (2022-05-16)

any update on this RBS issue marked for M102? we have stable RC cut tomorrow 

### ji...@intel.com (2022-05-17)

It's still under reviewing.

### sr...@google.com (2022-05-17)

amyressler@ this is marked as RBS and we still dont have a fix that landed on trunk to merge to m102, can you help review this and see if this indeed should block M102? 

### am...@chromium.org (2022-05-17)

Hi Jie and Jamie, I see the fixing CL https://chromium-review.googlesource.com/c/angle/angle/+/3646590 but it looks like this is in an active state and there are a number of comments from three days ago. Can you please provide a status and ETA for resolution? 
From all information above this appears to be a high severity security regression for 102. M102 is being cut for stable release today to be QAed and tested for release next week. As of right now, with no additional information this would block that release from being cut and delay its release next week as we cannot ship a security regression. 
Any update you can provide would be most appreciate and is greatly needed so we security can coordinate with the release team and we can determine any appropriate change in release plan.

### am...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-05-19)

This is not a recent regression. The problem discovered by the reporter has been present for many Chrome releases - likely three years or more, with the many changes associated with https://crbug.com/chromium/849576 and follow-on issues.

Would it be possible to remove the ReleaseBlock-Stable label for M102? We would like to make sure we carefully review and test the fix that Jie has developed.

The fix can be backported to Chrome's release channels once well tested on Canary.


### am...@chromium.org (2022-05-19)

Thanks, Ken, I appreciate this insight. Yes, since this is not a regression, this can be considered to not a release blocker. Thank you for the review and analysis you all are putting into the fix. 
Setting foundin-100 since this is presently the oldest active release channel.


### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/4a20c9143abbf29c649cf643182735e8952089e3

commit 4a20c9143abbf29c649cf643182735e8952089e3
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri May 20 14:26:15 2022

D3D: Fix race condition with parallel shader compile.

Bug: chromium:1317673
Change-Id: I0fb7c9a66248852e41e8700e80c295393ef941e8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3651153
Reviewed-by: Jie A Chen <jie.a.chen@intel.com>
Reviewed-by: Lingfeng Yang <lfy@google.com>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/4a20c9143abbf29c649cf643182735e8952089e3/src/tests/gl_tests/ParallelShaderCompileTest.cpp
[modify] https://crrev.com/4a20c9143abbf29c649cf643182735e8952089e3/src/libANGLE/renderer/d3d/ProgramD3D.cpp


### gi...@appspot.gserviceaccount.com (2022-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ed5ae9ceb6a999e8c92d707905f795fe9e76994d

commit ed5ae9ceb6a999e8c92d707905f795fe9e76994d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu May 26 04:09:05 2022

Roll ANGLE from 7a243dbe2495 to 7ad48b846545 (15 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/7a243dbe2495..7ad48b846545

2022-05-26 kainino@chromium.org Revert "Add Vulkan backend support for texture labels"
2022-05-25 abdolrashidi@google.com Vulkan: Remove removeEarlyFragmentTestsOpt flag
2022-05-25 jmadill@chromium.org Vulkan: Remove invalid ASSERT in DescriptorSetDesc.
2022-05-25 antonio.caggiano@collabora.com Vulkan: Support Wayland EGL_DEFAULT_DISPLAY
2022-05-25 jmadill@chromium.org D3D: Fix race condition with parallel shader compile.
2022-05-25 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 82a65519c521 to c8893896acff (10 revisions)
2022-05-25 gert.wollny@collabora.com libANGLE: Fix evaluating the sample count
2022-05-25 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from d624307d6d25 to 1f342b327faa (484 revisions)
2022-05-25 gert.wollny@collabora.com Capture/Replay: Override eglCreateImage and eglDestroyImage
2022-05-25 ffz@google.com Code Cleanup
2022-05-25 lfy@google.com Add ffz@google.com to OWNERS
2022-05-25 senorblanco@chromium.org D3D: implement whole-struct assignment in SSBOs.
2022-05-24 lexa.knyazev@gmail.com Fix ValidCompressedSubImageSize for 3D uploads
2022-05-24 m.maiya@samsung.com Vulkan: Bug fix in GL_QCOM_shading_rate
2022-05-24 mark@lunarg.com Add Vulkan backend support for texture labels

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1317673
Tbr: geofflang@google.com
Change-Id: I901d1fbdcd2df506a1387d5d80fbf3e5ce150261
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3670336
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1007719}

[modify] https://crrev.com/ed5ae9ceb6a999e8c92d707905f795fe9e76994d/DEPS


### [Deleted User] (2022-05-26)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-06-01)

Do the commits in https://crbug.com/chromium/1317673#c40 and https://crbug.com/chromium/1317673#c41 fully fix this bug? If so, could you please update the status?

### jm...@chromium.org (2022-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-02)

Requesting merge to stable M102 because latest trunk commit (1007719) appears to be after stable branch point (992738).

Requesting merge to beta M103 because latest trunk commit (1007719) appears to be after beta branch point (1002911).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-02)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-02)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-06-03)

merge to M102 and M103 approved, please merge this fix to branch 5005 (M102) and branch 5060 (M103) at your earliest convenience

### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1d795a6171328aa4c0ceeb065ac5c07be247666a

commit 1d795a6171328aa4c0ceeb065ac5c07be247666a
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri May 20 14:26:15 2022

[M103] D3D: Fix race condition with parallel shader compile.

Bug: chromium:1317673
Change-Id: I0fb7c9a66248852e41e8700e80c295393ef941e8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3651153
Reviewed-by: Jie A Chen <jie.a.chen@intel.com>
Reviewed-by: Lingfeng Yang <lfy@google.com>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4a20c9143abbf29c649cf643182735e8952089e3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3691049
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/1d795a6171328aa4c0ceeb065ac5c07be247666a/src/libANGLE/renderer/d3d/ProgramD3D.cpp
[modify] https://crrev.com/1d795a6171328aa4c0ceeb065ac5c07be247666a/src/tests/gl_tests/ParallelShaderCompileTest.cpp


### gi...@appspot.gserviceaccount.com (2022-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/801b904aea7de49234dcd99114e01cb77e21bc52

commit 801b904aea7de49234dcd99114e01cb77e21bc52
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri May 20 14:26:15 2022

[M102] D3D: Fix race condition with parallel shader compile.

Bug: chromium:1317673
Change-Id: I0fb7c9a66248852e41e8700e80c295393ef941e8
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3651153
Reviewed-by: Jie A Chen <jie.a.chen@intel.com>
Reviewed-by: Lingfeng Yang <lfy@google.com>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 4a20c9143abbf29c649cf643182735e8952089e3)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3691050
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/801b904aea7de49234dcd99114e01cb77e21bc52/src/tests/gl_tests/ParallelShaderCompileTest.cpp
[modify] https://crrev.com/801b904aea7de49234dcd99114e01cb77e21bc52/src/libANGLE/renderer/d3d/ProgramD3D.cpp


### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations, Tran Van Khang! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch shortly to arrange payment. Thank you for your efforts and reporting this issue to us - great work! 

### kh...@gmail.com (2022-06-14)

Thanks everyone. Thanks for reward.

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1317673?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/chromium/849576]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059411)*
