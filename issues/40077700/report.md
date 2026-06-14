# ASSERTION FAILED: isMainThread(), Heap-use-after-free in WebCore::WaveShaperDSPKernel::lazyInitializeOversampling

| Field | Value |
|-------|-------|
| **Issue ID** | [40077700](https://issues.chromium.org/issues/40077700) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Media>Audio |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-06-24 |
| **Bounty** | $500.00 |

## Description

Repro-file as attachment.

Tested on:

OS: Windows 7 x64

Chrome: 29.0.1546.0 (Official Build 208092) canary

You need to use page-heap /full to be able to reproduce this issue.

WinDBG report snippet from chrome crash-dump:

0:000> .ecxr
eax=2a500f90 ebx=00000000 ecx=27261fd8 edx=00000002 esi=27261fd8 edi=00000000
eip=564a0cd7 esp=0015ebdc ebp=0015ebf4 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
chrome_54f40000!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+0x6:
564a0cd7 395e0c          cmp     dword ptr [esi+0Ch],ebx ds:002b:27261fe4=c0c0c0c0

0:000> !analyze -v
.
.
.
FAULTING_IP: 
chrome_54f40000!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+6 [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshaperdspkernel.cpp @ 53]
564a0cd7 395e0c          cmp     dword ptr [esi+0Ch],ebx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 564a0cd7 (chrome_54f40000!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+0x00000006)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 27261fe4
Attempt to read from address 27261fe4

DEFAULT_BUCKET_ID:  INVALID_POINTER_READ

PROCESS_NAME:  chrome.exe

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%08lx referenced memory at 0x%08lx. The memory could not be %s.

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%08lx referenced memory at 0x%08lx. The memory could not be %s.

EXCEPTION_PARAMETER1:  00000000

EXCEPTION_PARAMETER2:  27261fe4

READ_ADDRESS:  27261fe4 

FOLLOWUP_IP: 
chrome_54f40000!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+6 [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshaperdspkernel.cpp @ 53]
564a0cd7 395e0c          cmp     dword ptr [esi+0Ch],ebx

MOD_LIST: <ANALYSIS/>

NTGLOBALFLAG:  2000000

FAULTING_THREAD:  00002f14

PRIMARY_PROBLEM_CLASS:  INVALID_POINTER_READ

BUGCHECK_STR:  APPLICATION_FAULT_INVALID_POINTER_READ

LAST_CONTROL_TRANSFER:  from 5649fd5b to 564a0cd7

STACK_TEXT:  
0015ebe0 5649fd5b 27ec4f80 0015ec28 0015ecf4 chrome_54f40000!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+0x6 [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshaperdspkernel.cpp @ 53]
0015ebf4 56497ba6 00000001 00000000 0e496fe8 chrome_54f40000!WebCore::WaveShaperProcessor::setOversample+0x29 [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshaperprocessor.cpp @ 70]
0015ec08 55d44a08 0015ec28 0015ec2c 00000000 chrome_54f40000!WebCore::WaveShaperNode::setOversample+0x55 [c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshapernode.cpp @ 65]
0015ec40 55d44ab7 0015ecf8 0015ecf4 0015ec70 chrome_54f40000!WebCore::WaveShaperNodeV8Internal::oversampleAttrSetter+0x198 [c:\b\build\slave\win\build\src\build\release\obj\global_intermediate\webcore\bindings\v8waveshapernode.cpp @ 114]
0015ec54 5537108f 0015ecf8 0015ecf4 0015ec70 chrome_54f40000!WebCore::WaveShaperNodeV8Internal::oversampleAttrSetterCallback+0x14 [c:\b\build\slave\win\build\src\build\release\obj\global_intermediate\webcore\bindings\v8waveshapernode.cpp @ 122]
.
.
.


STACK_COMMAND:  ~0s; .ecxr ; kb

FAULTING_SOURCE_CODE:  
No source found for 'c:\b\build\slave\win\build\src\third_party\webkit\source\modules\webaudio\waveshaperdspkernel.cpp'

SYMBOL_STACK_INDEX:  0

SYMBOL_NAME:  chrome!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+6

FOLLOWUP_NAME:  MachineOwner

MODULE_NAME: chrome_54f40000

IMAGE_NAME:  chrome.dll

DEBUG_FLR_IMAGE_TIMESTAMP:  51c68b35

FAILURE_BUCKET_ID:  INVALID_POINTER_READ_c0000005_chrome.dll!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling

BUCKET_ID:  APPLICATION_FAULT_INVALID_POINTER_READ_chrome!WebCore::WaveShaperDSPKernel::lazyInitializeOversampling+6


## Attachments

- [WebCoreWaveShaperDSPKernellazyInitializeOversampling.html](attachments/WebCoreWaveShaperDSPKernellazyInitializeOversampling.html) (text/html; charset=us-ascii, 670 B)

## Timeline

### gl...@chromium.org (2013-06-26)

google-chrome-asan crashes on this file as well in both 29.0.1547.0 (https://crash/d9acc204f9e5f139) and 29.0.1535.3 (https://crash/779fa07b2dd29271)

=================================================================
==588==ERROR: AddressSanitizer: heap-use-after-free on address 0x607000199838 at pc 0x7f2805f49281 bp 0x7fff89acd280 sp 0x7fff89acd278
READ of size 8 at 0x607000199838 thread T0 (chrome)
    #0 0x7f2805f49280 in operator! /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/wtf/OwnPtr.h:74
    #1 0x7f2805ee4c4a in setOversample /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/WaveShaperProcessor.cpp:70
    #2 0x7f28052537d3 in oversampleAttrSetter /usr/local/google/chrome-asan-build-clean/src/out/Release/obj/gen/webcore/bindings/V8WaveShaperNode.cpp:114
    #3 0x7f2802edb3e2 in Call /usr/local/google/chrome-asan-build-clean/src/v8/src/arguments.cc:186
    #4 0x7f280361a8e9 in __RT_impl_StoreCallbackProperty /usr/local/google/chrome-asan-build-clean/src/v8/src/stub-cache.cc:1115
    #5 0x7f27cb00688d
0x607000199838 is located 24 bytes inside of 72-byte region [0x607000199820,0x607000199868)
freed by thread T242 (AudioOutputDevi) here:
    #0 0x7f28002f5c11 in operator delete _asan_rtl_
    #1 0x7f280916eafc in deleteOwnedPtr<WebCore::AudioDSPKernel> /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/wtf/OwnPtrCommon.h:47
    #2 0x7f2805f4558e in uninitialize /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorNode.cpp:65
    #3 0x7f2805f45961 in checkNumberOfChannelsForInput /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorNode.cpp:119
    #4 0x7f2805ecaa8f in updateRenderingState /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/AudioSummingJunction.cpp:74
previously allocated by thread T242 (AudioOutputDevi) here:
    #0 0x7f28002f5991 in operator new _asan_rtl_
    #1 0x7f2805ee4a29 in createKernel /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/WaveShaperProcessor.cpp:49
    #2 0x7f280916e677 in initialize /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/core/platform/audio/AudioDSPKernelProcessor.cpp:57
    #3 0x7f2805f454f5 in initialize /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorNode.cpp:54
    #4 0x7f2805f45a12 in checkNumberOfChannelsForInput /usr/local/google/chrome-asan-build-clean/src/third_party/WebKit/Source/modules/webaudio/AudioBasicProcessorNode.cpp:128
Thread T242 (AudioOutputDevi) created by T41 (Chrome_ChildIOT) here:
    #0 0x7f28002f1118 in __interceptor_pthread_create _asan_rtl_
    #1 0x7f280132a0a7 in CreateThread /usr/local/google/chrome-asan-build-clean/src/base/threading/platform_thread_posix.cc:120
    #2 0x7f280132a298 in CreateWithPriority /usr/local/google/chrome-asan-build-clean/src/base/threading/platform_thread_posix.cc:208
    #3 0x7f2808b21a6f in operator-> /usr/local/google/chrome-asan-build-clean/src/media/audio/audio_device_thread.cc:111
    #4 0x7f2808a263b4 in OnStreamCreated /usr/local/google/chrome-asan-build-clean/src/media/audio/audio_output_device.cc:248
    #5 0x7f28075bedb8 in OnStreamCreated /usr/local/google/chrome-asan-build-clean/src/content/renderer/media/audio_message_filter.cc:184
    #6 0x7f2801cc35dd in TryFilters /usr/local/google/chrome-asan-build-clean/src/ipc/ipc_channel_proxy.cc:79
    #7 0x7f2801cd12b4 in OnMessageReceived /usr/local/google/chrome-asan-build-clean/src/ipc/ipc_sync_channel.cc:330
    #8 0x7f2801cc9aab in DispatchInputData /usr/local/google/chrome-asan-build-clean/src/ipc/ipc_channel_reader.cc:90
    #9 0x7f2801cc936a in ProcessIncomingMessages /usr/local/google/chrome-asan-build-clean/src/ipc/ipc_channel_reader.cc:32
    #10 0x7f2801cbff6a in OnFileCanReadWithoutBlocking /usr/local/google/chrome-asan-build-clean/src/ipc/ipc_channel_posix.cc:641
    #11 0x7f2801265b61 in operator-> /usr/local/google/chrome-asan-build-clean/src/base/message_loop/message_pump_libevent.cc:99
    #12 0x7f28013a0424 in event_process_active /usr/local/google/chrome-asan-build-clean/src/third_party/libevent/event.c:385
    #13 0x7f2801266290 in Run /usr/local/google/chrome-asan-build-clean/src/base/message_loop/message_pump_libevent.cc:259
    #14 0x7f28012fe923 in Run /usr/local/google/chrome-asan-build-clean/src/base/run_loop.cc:45
    #15 0x7f28012c878d in Run /usr/local/google/chrome-asan-build-clean/src/base/message_loop/message_loop.cc:321
    #16 0x7f2801334ed8 in ThreadMain /usr/local/google/chrome-asan-build-clean/src/base/threading/thread.cc:203
    #17 0x7f280132a528 in ThreadFunc /usr/local/google/chrome-asan-build-clean/src/base/threading/platform_thread_posix.cc:80
    #18 0x7f28002fbd83 in ThreadStart _asan_rtl_
Thread T41 (Chrome_ChildIOT) created by T0 (chrome) here:
    #0 0x7f28002f1118 in __interceptor_pthread_create _asan_rtl_
    #1 0x7f280132a0a7 in CreateThread /usr/local/google/chrome-asan-build-clean/src/base/threading/platform_thread_posix.cc:120
    #2 0x7f2801329dfc in Create /usr/local/google/chrome-asan-build-clean/src/base/threading/platform_thread_posix.cc:199
    #3 0x7f28013348be in StartWithOptions /usr/local/google/chrome-asan-build-clean/src/base/threading/thread.cc:92
    #4 0x7f28076bfd9f in ChildProcess /usr/local/google/chrome-asan-build-clean/src/content/child/child_process.cc:41
    #5 0x7f2807435e5d in RenderProcess /usr/local/google/chrome-asan-build-clean/src/./content/renderer/render_process.h:28
    #6 0x7f28074d6ec3 in RendererMain /usr/local/google/chrome-asan-build-clean/src/content/renderer/renderer_main.cc:222
    #7 0x7f28010423fc in RunZygote /usr/local/google/chrome-asan-build-clean/src/content/app/content_main_runner.cc:385
    #8 0x7f2801044c52 in Run /usr/local/google/chrome-asan-build-clean/src/content/app/content_main_runner.cc:754
    #9 0x7f2801041c71 in ContentMain /usr/local/google/chrome-asan-build-clean/src/content/app/content_main.cc:35
    #10 0x7f2800305916 in ChromeMain /usr/local/google/chrome-asan-build-clean/src/chrome/app/chrome_main.cc:32
    #11 0x7f280030582a in main /usr/local/google/chrome-asan-build-clean/src/chrome/app/chrome_exe_main_gtk.cc:43
    #12 0x7f27f6e5876c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
Shadow bytes around the buggy address:
  0x0c0e8002b2b0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd
  0x0c0e8002b2c0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x0c0e8002b2d0: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd
  0x0c0e8002b2e0: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e8002b2f0: fd fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
=>0x0c0e8002b300: fa fa fa fa fd fd fd[fd]fd fd fd fd fd fa fa fa
  0x0c0e8002b310: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0e8002b320: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
  0x0c0e8002b330: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
  0x0c0e8002b340: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd
  0x0c0e8002b350: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe


### cl...@chromium.org (2013-06-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6475518165647360

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6070000268d0
Crash State:
  - crash stack -
  WebCore::WaveShaperDSPKernel::lazyInitializeOversampling
  WebCore::WaveShaperProcessor::setOversample
  - free stack -
  WebCore::AudioDSPKernelProcessor::uninitialize
  WebCore::AudioBasicProcessorNode::uninitialize
  




### in...@chromium.org (2013-06-28)

xingnan.wang@, can you please help to fix it.

Don't know why  james.wei@intel.com is not showing in system ?

### [Deleted User] (2013-06-30)

All right, let me have a look at it.

James Wei has left Intel, so the email is invalidate.

### [Deleted User] (2013-07-01)

Patch was uploaded for review.

https://codereview.chromium.org/18317002

### in...@chromium.org (2013-07-01)

This regressed in http://src.chromium.org/viewvc/blink?view=rev&revision=151686. We have reliable repro in CF. Thanks Xingnan for the fix.

### cl...@chromium.org (2013-07-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4655935943344128

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60700001e258
Crash State:
  - crash stack -
  WebCore::WaveShaperDSPKernel::lazyInitializeOversampling
  WebCore::WaveShaperProcessor::setOversample
  - free stack -
  WebCore::AudioDSPKernelProcessor::uninitialize
  WebCore::AudioBasicProcessorNode::uninitialize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=203936:203948

Minimized Testcase (6.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94vp22eygFNoLsfCO4gaGLUpsvzuC1ZbQ-FloT02AG1YzJOoegJPpYdGv6elIw3oV4yJS8EF_UcRsVthnLnVx_DkFzKwq_3mzxwx-spbWZCQ8XIZiKHf-2y-Bpsvnc8pRyxvcIUSzMmtCUkzE1QuyNy8IUXaQ



### in...@chromium.org (2013-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-07-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-07-09)

@xingnan.wang: Assigning to you since you already have a patch.

### [Deleted User] (2013-07-09)

Sorry for the late response, I updated the patch as reviewer`s comments.

### in...@chromium.org (2013-07-09)

Chris, can you please review Xingnan's patch so that we can get rid of the regression from r151686.

### cr...@google.com (2013-07-09)

done - patch looks good

### bu...@chromium.org (2013-07-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=153852

------------------------------------------------------------------------
r153852 | xingnan.wang@chromium.org | 2013-07-10T05:40:47.685094Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/WaveShaperNode.cpp?r1=153852&r2=153851&pathrev=153852
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/WaveShaperDSPKernel.cpp?r1=153852&r2=153851&pathrev=153852

Heap-use-after-free in WaveShaperDSPKernel::lazyInitializeOversampling

BUG=253550

Review URL: https://chromiumcodereview.appspot.com/18317002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-07-19)

ClusterFuzz has detected this issue as fixed in range 210904:210911.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4655935943344128

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60700001e258
Crash State:
  - crash stack -
  WebCore::WaveShaperDSPKernel::lazyInitializeOversampling
  WebCore::WaveShaperProcessor::setOversample
  - free stack -
  WebCore::AudioDSPKernelProcessor::uninitialize
  WebCore::AudioBasicProcessorNode::uninitialize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=203936:203948
Fixed: https://cluster-fuzz.appspot.com/revisions?range=210904:210911

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94vp22eygFNoLsfCO4gaGLUpsvzuC1ZbQ-FloT02AG1YzJOoegJPpYdGv6elIw3oV4yJS8EF_UcRsVthnLnVx_DkFzKwq_3mzxwx-spbWZCQ8XIZiKHf-2y-Bpsvnc8pRyxvcIUSzMmtCUkzE1QuyNy8IUXaQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-07-31)

M29: http://src.chromium.org/viewvc/blink?view=rev&rev=155214

### bu...@chromium.org (2013-07-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=155214

------------------------------------------------------------------------
r155214 | cevans@chromium.org | 2013-07-31T03:05:43.028435Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/modules/webaudio/WaveShaperNode.cpp?r1=155214&r2=155213&pathrev=155214
   M http://src.chromium.org/viewvc/blink/branches/chromium/1547/Source/modules/webaudio/WaveShaperDSPKernel.cpp?r1=155214&r2=155213&pathrev=155214

Merge 153852 "Heap-use-after-free in WaveShaperDSPKernel::lazyIn..."

> Heap-use-after-free in WaveShaperDSPKernel::lazyInitializeOversampling
> 
> BUG=253550
> 
> Review URL: https://chromiumcodereview.appspot.com/18317002

TBR=xingnan.wang@chromium.org

Review URL: https://codereview.chromium.org/21150017
------------------------------------------------------------------------

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-10-22)

Thanks for the report! $500

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### pa...@chromium.org (2013-12-18)

Payment process kicked off! As you know, this can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/253550?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Media>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077700)*
