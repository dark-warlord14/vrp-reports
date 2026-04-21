# heapoverflow in web gpu 

| Field | Value |
|-------|-------|
| **Issue ID** | [40054230](https://issues.chromium.org/issues/40054230) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2020-12-19 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
1.open chromium and enable webgpu
2.put files to sanme dir and run `python -m SimpleHTTPServer`
3.chrome.exe --no-sandbox --user-data-dir=/tmp/xxx http://localhost:8000/crash.html

What is the expected behavior?

What went wrong?
=================================================================
==11076==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12410f5ace98 at pc 0x7ffa9218167e bp 0x003c233fe640 sp 0x003c233fe688
READ of size 8 at 0x12410f5ace98 thread T0
==11076==*** WARNING: Failed to initialize DbgHelp!              ***
==11076==*** Most likely this means that the app is already      ***
==11076==*** using DbgHelp, possibly with incompatible flags.    ***
==11076==*** Due to technical reasons, symbolization might crash ***
==11076==*** or produce wrong results.                           ***
    #0 0x7ffa9218167d in dawn_wire::WireDeserializeAllocator::Reset E:\work\fuzz\chromium\src\third_party\dawn\src\dawn_wire\WireDeserializeAllocator.cpp:51
    #1 0x7ffa92183ebb in dawn_wire::client::Client::HandleCommandsImpl E:\work\fuzz\chromium\src\out\asan\gen\third_party\dawn\src\dawn_wire\client\ClientHandlers_autogen.cpp:162
    #2 0x7ffa842df801 in gpu::webgpu::WebGPUImplementation::OnGpuControlReturnData E:\work\fuzz\chromium\src\gpu\command_buffer\client\webgpu_implementation.cc:445
    #3 0x7ffa80d8dcb9 in gpu::CommandBufferProxyImpl::OnReturnData E:\work\fuzz\chromium\src\gpu\ipc\client\command_buffer_proxy_impl.cc:631
    #4 0x7ffa80d8d976 in IPC::MessageT<GpuCommandBufferMsg_ReturnData_Meta,std::tuple<std::vector<unsigned char> >,void>::Dispatch<gpu::CommandBufferProxyImpl,gpu::CommandBufferProxyImpl,void,void (gpu::CommandBufferProxyImpl::*)(const std::vector<unsigned char> &)> E:\work\fuzz\chromium\src\ipc\ipc_message_templates.h:140
    #5 0x7ffa80d8a299 in gpu::CommandBufferProxyImpl::OnMessageReceived E:\work\fuzz\chromium\src\gpu\ipc\client\command_buffer_proxy_impl.cc:149
    #6 0x7ffa8a334c4e in base::TaskAnnotator::RunTask E:\work\fuzz\chromium\src\base\task\common\task_annotator.cc:163
    #7 0x7ffa8cec9d41 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:351
    #8 0x7ffa8cec909e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:264
    #9 0x7ffa8ce8b68f in base::MessagePumpDefault::Run E:\work\fuzz\chromium\src\base\message_loop\message_pump_default.cc:39
    #10 0x7ffa8cecc83e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\work\fuzz\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:460
    #11 0x7ffa8a2cde7d in base::RunLoop::Run E:\work\fuzz\chromium\src\base\run_loop.cc:131
    #12 0x7ffa8cc69593 in content::RendererMain E:\work\fuzz\chromium\src\content\renderer\renderer_main.cc:260
    #13 0x7ffa89ff2429 in content::ContentMainRunnerImpl::Run E:\work\fuzz\chromium\src\content\app\content_main_runner_impl.cc:902
    #14 0x7ffa89feed8a in content::RunContentProcess E:\work\fuzz\chromium\src\content\app\content_main.cc:372
    #15 0x7ffa89fef400 in content::ContentMain E:\work\fuzz\chromium\src\content\app\content_main.cc:398
    #16 0x7ffa7e21154f in ChromeMain E:\work\fuzz\chromium\src\chrome\app\chrome_main.cc:130
    #17 0x7ff7c7e86b42 in MainDllLoader::Launch E:\work\fuzz\chromium\src\chrome\app\main_dll_loader_win.cc:169
    #18 0x7ff7c7e83025 in main E:\work\fuzz\chromium\src\chrome\app\chrome_exe_main_win.cc:354
    #19 0x7ff7c82e644f in __scrt_common_main_seh D:\agent\_work\9\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #20 0x7ffb2e7e7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #21 0x7ffb2f7fd0d0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004d0d0)

Address 0x12410f5ace98 is a wild pointer.
SUMMARY: AddressSanitizer: heap-buffer-overflow E:\work\fuzz\chromium\src\third_party\dawn\src\dawn_wire\WireDeserializeAllocator.cpp:51 in dawn_wire::WireDeserializeAllocator::Reset
Shadow bytes around the buggy address:
  0x044931435980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044931435990: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0449314359a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0449314359b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0449314359c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0449314359d0: fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa fa fa
  0x0449314359e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0449314359f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044931435a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044931435a10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x044931435a20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==11076==ABORTING

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 445 B)
- [new.html](attachments/new.html) (text/plain, 768 B)
- [test.js](attachments/test.js) (text/plain, 5.8 KB)
- [test.js](attachments/test.js) (text/plain, 7.2 KB)

## Timeline

### [Deleted User] (2020-12-19)

[Empty comment from Monorail migration]

### wx...@gmail.com (2020-12-19)

here is the same asan output but another's test.js to crash chrome

### es...@chromium.org (2020-12-22)

cwallez, PTAL? I'm going to send you several of these; they are all slightly different test cases and stack traces, though perhaps they're related.

Triaging as High severity due to memory corruption in the GPU process, but Security_Impact-None because WebGPU isn't enabled by default.

[Monorail components: Blink>WebGPU]

### cw...@chromium.org (2021-01-04)

Thanks for the CC I'm assigning all of them to Austin as he has been looking at this space recently. The triage looks good and the crash is in the renderer process here, see gpu\command_buffer\client\ that's the "client side" of the WebGPU remoting.

Austin can you TAL? This seems like it could be very related to the fixes you're looking at for dawn_wire.

### en...@chromium.org (2021-01-05)

WebGPUImplementation is destroyed when the iframe is destructed, and then an IPC message for OnGpuControlReturnData happens. The WebGPUImplementation is now garbage memory.

### en...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

The older reward-topanel https://crbug.com/chromium/1154521 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

Congratulations, wxhusst@! The VRP Panel has decided to award you $5,000 for this report. Nice work! 

### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-03-07)

Thanks a lot

### [Deleted User] (2021-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-05-28)

This issue was migrated from crbug.com/chromium/1160414?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1154521, crbug.com/chromium/1160453]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054230)*
