# Security: heap-buffer-overflow  in network::ThrottlingNetworkInterceptor::UpdateThrottledRecords

| Field | Value |
|-------|-------|
| **Issue ID** | [40061636](https://issues.chromium.org/issues/40061636) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Network, Platform>DevTools>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-11-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-buffer-overflow in network::ThrottlingNetworkInterceptor::UpdateThrottledRecords

**VERSION**  

Chromium 109.0.5407.0 (Developer Build) (64-bit)  

Revision 9e95417b416074f8703958dcc1ca45108411406f-refs/heads/main@{#1068047}  

OS Windows 10 Version 22H2 (Build 19045.2130)

It can also been reproduced in Linux-ChromiumOS

**REPRODUCTION CASE**

1. Run `python3 -m http.server 80` in any folder.
2. put the attachments into the extension\_path
3. Run  
   
   chrome --user-data-dir=c:/any --load-extension="extension\_path" <http://localhost>

After a while it will trigger the heap-buffer-overflow

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

=================================================================  

==6876==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x11660edf0d98 at pc 0x7ff7b51c51cc bp 0x003eb41fe170 sp 0x003eb41fe1b8  

READ of size 25 at 0x11660edf0d98 thread T6  

==6876==WARNING: Failed to use and restart external symbolizer!  

==6876==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==6876==\*\*\* Most likely this means that the app is already \*\*\*  

==6876==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==6876==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==6876==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff7b51c51cb in \_\_asan\_memcpy C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22  

#1 0x7fff40a3b34b in std::Cr::\_IterOps[std::Cr::\_ClassicAlgPolicy](javascript:void(0);)::iter\_swap<std::Cr::\_\_wrap\_iter<network::ThrottlingNetworkInterceptor::ThrottleRecord \*> &,std::Cr::\_\_wrap\_iter<network::ThrottlingNetworkInterceptor::ThrottleRecord \*> &> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_algorithm\iterator\_operations.h:138  

#2 0x7fff40a3afc2 in std::Cr::\_\_rotate\_forward<std::Cr::\_ClassicAlgPolicy,std::Cr::\_\_wrap\_iter<network::ThrottlingNetworkInterceptor::ThrottleRecord \*> > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_algorithm\rotate.h:63  

#3 0x7fff40a39534 in network::ThrottlingNetworkInterceptor::UpdateThrottledRecords C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling\_network\_interceptor.cc:119  

#4 0x7fff40a38a30 in network::ThrottlingNetworkInterceptor::UpdateThrottled C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling\_network\_interceptor.cc:126  

#5 0x7fff40a3a0e4 in network::ThrottlingNetworkInterceptor::OnTimer C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling\_network\_interceptor.cc:166  

#6 0x7fff40a3b8dd in base::internal::Invoker<base::internal::BindState<void (network::ThrottlingNetworkInterceptor::\*)(),base::internal::UnretainedWrapper[network::ThrottlingNetworkInterceptor,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:870  

#7 0x7fff34afa3f5 in base::OneShotTimer::RunUserTask C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:278  

#8 0x7fff34af983c in base::internal::DelayTimerBase::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:240  

#9 0x7fff34afd345 in base::internal::Invoker<base::internal::BindState<void (base::internal::DelayTimerBase::\*)(),base::internal::UnretainedWrapper[base::internal::DelayTimerBase,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:883  

#10 0x7fff34a9e5d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:154  

#11 0x7fff37a2ed03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:448  

#12 0x7fff37a2da72 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:299  

#13 0x7fff34b4eba9 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:710  

#14 0x7fff34b48ab0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#15 0x7fff37a30fd3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:608  

#16 0x7fff34a2dffe in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#17 0x7fff34af0fad in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:338  

#18 0x7fff3701bdec in content::`anonymous namespace'::ChildIOThread::Run C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:56 #19 0x7fff34af13c5 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:408 #20 0x7fff34b6c9a1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:134  

#21 0x7ff7b51d02e3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#22 0x7fffefb77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#23 0x7ffff0d026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x11660edf0d98 is located 40 bytes before 320-byte region [0x11660edf0dc0,0x11660edf0f00)  

allocated by thread T6 here:  

#0 0x7ff7b51c5a3d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff48f41e9e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff280afd64 in std::Cr::\_\_split\_buffer<absl::strings\_internal::ViableSubstitution,std::Cr::allocator[absl::strings\_internal::ViableSubstitution](javascript:void(0);) &>::\_\_split\_buffer C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_split\_buffer:324  

#3 0x7fff40a39c26 in std::Cr::vector<network::ThrottlingNetworkInterceptor::ThrottleRecord,std::Cr::allocator[network::ThrottlingNetworkInterceptor::ThrottleRecord](javascript:void(0);) >::push\_back C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1512  

#4 0x7fff40a39e94 in network::ThrottlingNetworkInterceptor::CollectFinished C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling\_network\_interceptor.cc:155  

#5 0x7fff40a3a11e in network::ThrottlingNetworkInterceptor::OnTimer C:\b\s\w\ir\cache\builder\src\services\network\throttling\throttling\_network\_interceptor.cc:169  

#6 0x7fff40a3b8dd in base::internal::Invoker<base::internal::BindState<void (network::ThrottlingNetworkInterceptor::\*)(),base::internal::UnretainedWrapper[network::ThrottlingNetworkInterceptor,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:870  

#7 0x7fff34afa3f5 in base::OneShotTimer::RunUserTask C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:278  

#8 0x7fff34af983c in base::internal::DelayTimerBase::OnScheduledTaskInvoked C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc:240  

#9 0x7fff34afd345 in base::internal::Invoker<base::internal::BindState<void (base::internal::DelayTimerBase::\*)(),base::internal::UnretainedWrapper[base::internal::DelayTimerBase,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:883  

#10 0x7fff34a9e5d9 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:154  

#11 0x7fff37a2ed03 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:448  

#12 0x7fff37a2da72 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:299  

#13 0x7fff34b4eba9 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:710  

#14 0x7fff34b48ab0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#15 0x7fff37a30fd3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:608  

#16 0x7fff34a2dffe in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#17 0x7fff34af0fad in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:338  

#18 0x7fff3701bdec in content::`anonymous namespace'::ChildIOThread::Run C:\b\s\w\ir\cache\builder\src\content\child\child_process.cc:56 #19 0x7fff34af13c5 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:408 #20 0x7fff34b6c9a1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:134  

#21 0x7ff7b51d02e3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#22 0x7fffefb77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#23 0x7ffff0d026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

Thread T6 created by T0 here:  

#0 0x7ff7b51d0d72 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7fff34b6ba3e in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:199  

#2 0x7fff34af01f4 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:211  

#3 0x7fff3701b623 in content::ChildProcess::ChildProcess C:\b\s\w\ir\cache\builder\src\content\child\child\_process.cc:145  

#4 0x7fff322a742f in content::UtilityMain C:\b\s\w\ir\cache\builder\src\content\utility\utility\_main.cc:226  

#5 0x7fff345ace13 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:753  

#6 0x7fff345af6ba in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1105  

#7 0x7fff345aa795 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:342  

#8 0x7fff345ab5f0 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:370  

#9 0x7fff280914a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#10 0x7ff7b5116288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#11 0x7ff7b5112c07 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#12 0x7ff7b554464b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#13 0x7fffefb77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#14 0x7ffff0d026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

# SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:22 in \_\_asan\_memcpy Shadow bytes around the buggy address: 0x11660edf0b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd 0x11660edf0b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd 0x11660edf0c00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd 0x11660edf0c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd 0x11660edf0d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd =>0x11660edf0d80: fa fa fa[fa]fa fa f7 fa 00 00 00 00 00 00 00 00 0x11660edf0e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0x11660edf0e80: 00 fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc 0x11660edf0f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa 0x11660edf0f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa 0x11660edf1000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa Shadow byte legend (one shadow byte represents 8 application bytes): Addressable: 00 Partially addressable: 01 02 03 04 05 06 07 Heap left redzone: fa Freed heap region: fd Stack left redzone: f1 Stack mid redzone: f2 Stack right redzone: f3 Stack after return: f5 Stack use after scope: f8 Global redzone: f9 Global init order: f6 Poisoned by user: f7 Container overflow: fc Array cookie: ac Intra object redzone: bb ASan internal: fe Left alloca redzone: ca Right alloca redzone: cb ==6876==ABORTING [3424:3340:1107/202922.953:ERROR:network\_service\_instance\_impl.cc(539)] Network service crashed, restarting service.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 385 B)
- [background.js](attachments/background.js) (text/plain, 871 B)

## Timeline

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-08)

Thank you for your bug. I can reproduce this. This does appear to be indirectly related to the screenshot call in your background.js as removing it stops the crash, but it's not clear what that link is.

[Monorail components: Internals>Media>ScreenCapture Internals>Services>Network]

### wf...@chromium.org (2022-11-08)

This reproduces back to 106 (at least).

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-08)

I'd guess this is to do with the Network.emulateNetworkConditions api. This is old code though. I'm assigning to caseq@ to take a look at. It's possible it's some kind of strange interaction with network service as well (+speculative morlovich@)

[Monorail components: -Internals>Media>ScreenCapture Platform>DevTools>Network]

### mo...@chromium.org (2022-11-08)

From scanning the code, negative downloadThroughput will result in negative download_tick_length_ here: 
https://source.chromium.org/chromium/chromium/src/+/main:services/network/throttling/throttling_network_interceptor.cc;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c;l=84

and then in ThrottlingNetworkInterceptor::UpdateThrottledRecords it probably results in a negative ticks, and therefore negative shift? (I should probably verify that..)

NetworkHandler code:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/network_handler.cc;drc=0fe00db18df0b148c8835ddfba63c52dd34904cb;l=1700

At root of this all there seems to a mismatch between devtools API and mojo APIs here:

DevTools: https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-emulateNetworkConditions
"-1 disables download throttling"

mojo: 
https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/mojom/network_context.mojom;drc=f96cd6abdcc6fc334d4105c07f062b811a65169b;l=558
" 0 disables download throttling."

(Also compare the NetworkHandler conditions with:
https://source.chromium.org/chromium/chromium/src/+/main:services/network/throttling/network_conditions.cc;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c;l=26

It feels like it may make sense to align them, and then maybe change CalculateTickLength computation to handle < 0 the same as 0?

(https://source.chromium.org/chromium/chromium/src/+/main:services/network/throttling/throttling_network_interceptor.cc;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c;l=24)

Latency appears to already handle negatives correct..


### wf...@chromium.org (2022-11-08)

I agree there does seem to be somewhat of a mismatch here between the api and mojo, but I tried the same poc with "downloadThroughput": 1024 (non negative) and it still crashes with the same asan stack.

### wf...@chromium.org (2022-11-08)

Actually, I take that https://crbug.com/chromium/1382033#c7 back. I cannot reproduce without the -1024...

### bm...@chromium.org (2022-11-09)

Danil, please take a look.

### mo...@chromium.org (2022-11-09)

FYI Will uploaded https://chromium-review.googlesource.com/c/chromium/src/+/4014891 


### [Deleted User] (2022-11-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-16)

[security marshal] Looks like the CL in https://crbug.com/chromium/1382033#c10 has not yet landed. Updating as started to reflect ongoing investigation and effort. 

### mo...@chromium.org (2022-11-18)

+ Eric for context of code review.  

### mo...@chromium.org (2022-11-18)

+ Ken for context of code review.


### gi...@appspot.gserviceaccount.com (2022-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e

commit ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e
Author: Maks Orlovich <morlovich@chromium.org>
Date: Fri Nov 18 21:51:45 2022

Align NetworkContext::SetNetworkConditions better with devtools emulateNetworkConditions

The former used values of 0 to disable particular throttles, while the
later documents -1, and looks to be pretty much a direct client, and the
only one. So make NetworkService handle everything <= 0 as a disable,
clamping at intake of config.

Bug: 1382033


Change-Id: I2fd3f075d5071cb0cf647838782115b5c00405bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035891
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1073566}

[modify] https://crrev.com/ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e/services/network/throttling/network_conditions.h
[modify] https://crrev.com/ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e/services/network/public/mojom/network_context.mojom
[modify] https://crrev.com/ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e/services/network/throttling/throttling_controller_unittest.cc
[modify] https://crrev.com/ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e/services/network/throttling/network_conditions.cc


### mo...@chromium.org (2022-11-22)

Anyway, this is in 110.0.5427.0; I would appreciated independent confirmation that it helps since I had trouble seeing the testcase failure.

If works, this definitely should be backported to 109, I am not sure of 108?


### wf...@chromium.org (2022-11-22)

I can confirm this is fixed. I verified the PoC no longer crashes on 110.0.5434.0 r1074589.

### mo...@chromium.org (2022-11-22)

(Not sure the severity justifies backport to 108, but I think it's not my call anyway?)


### [Deleted User] (2022-11-22)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43637378b14ef081503faed86b1606658d82501c

commit 43637378b14ef081503faed86b1606658d82501c
Author: Maks Orlovich <morlovich@chromium.org>
Date: Tue Nov 22 22:18:55 2022

Align NetworkContext::SetNetworkConditions better with devtools emulateNetworkConditions

The former used values of 0 to disable particular throttles, while the
later documents -1, and looks to be pretty much a direct client, and the
only one. So make NetworkService handle everything <= 0 as a disable,
clamping at intake of config.

Bug: 1382033


(cherry picked from commit ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e)

Change-Id: I2fd3f075d5071cb0cf647838782115b5c00405bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035891
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1073566}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4048289
Cr-Commit-Position: refs/branch-heads/5414@{#188}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/43637378b14ef081503faed86b1606658d82501c/services/network/throttling/network_conditions.h
[modify] https://crrev.com/43637378b14ef081503faed86b1606658d82501c/services/network/public/mojom/network_context.mojom
[modify] https://crrev.com/43637378b14ef081503faed86b1606658d82501c/services/network/throttling/throttling_controller_unittest.cc
[modify] https://crrev.com/43637378b14ef081503faed86b1606658d82501c/services/network/throttling/network_conditions.cc


### [Deleted User] (2022-11-22)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mo...@chromium.org (2022-11-23)

The bug dates to M64 [1]; so it's not a regression or anything new.  (Is this the right criterion for a security fix, though?)

[1] Notice the max on LHS of https://chromium-review.googlesource.com/c/chromium/src/+/703674/13/content/browser/devtools/protocol/network_handler.cc#b864 getting lost in all the complicated reshuffling.


### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-11-24)

[Empty comment from Monorail migration]

### rz...@google.com (2022-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-11-25)

1. Just https://crrev.com/c/4055550
2. Low, no conflicts
3. 109
4. Yes

### gm...@google.com (2022-11-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, asnine! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### gm...@google.com (2023-01-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/11ea73006b2efaae6bf3bb74562e4cf9258ca204

commit 11ea73006b2efaae6bf3bb74562e4cf9258ca204
Author: Maks Orlovich <morlovich@chromium.org>
Date: Thu Jan 26 20:12:36 2023

[M102-LTS] Align NetworkContext::SetNetworkConditions better with devtools emulateNetworkConditions

The former used values of 0 to disable particular throttles, while the
later documents -1, and looks to be pretty much a direct client, and the
only one. So make NetworkService handle everything <= 0 as a disable,
clamping at intake of config.

Bug: 1382033


(cherry picked from commit ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e)

Change-Id: I2fd3f075d5071cb0cf647838782115b5c00405bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035891
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1073566}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4055550
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1425}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/11ea73006b2efaae6bf3bb74562e4cf9258ca204/services/network/throttling/network_conditions.h
[modify] https://crrev.com/11ea73006b2efaae6bf3bb74562e4cf9258ca204/services/network/public/mojom/network_context.mojom
[modify] https://crrev.com/11ea73006b2efaae6bf3bb74562e4cf9258ca204/services/network/throttling/throttling_controller_unittest.cc
[modify] https://crrev.com/11ea73006b2efaae6bf3bb74562e4cf9258ca204/services/network/throttling/network_conditions.cc


### rz...@google.com (2023-01-26)

[Empty comment from Monorail migration]

### gm...@google.com (2023-01-31)

@rzanoni, please evaluate for 108.

### gm...@google.com (2023-01-31)

[Comment Deleted]

### rz...@google.com (2023-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-02-01)

1. Just https://crrev.com/c/4213051
2. Low, no conflicts
3. 109
4. Yes

### gm...@google.com (2023-02-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/471e5b79ba1850ba327cd19d54b008da70ba2578

commit 471e5b79ba1850ba327cd19d54b008da70ba2578
Author: Maks Orlovich <morlovich@chromium.org>
Date: Thu Feb 09 13:47:41 2023

[M108-LTS] Align NetworkContext::SetNetworkConditions better with devtools emulateNetworkConditions

The former used values of 0 to disable particular throttles, while the
later documents -1, and looks to be pretty much a direct client, and the
only one. So make NetworkService handle everything <= 0 as a disable,
clamping at intake of config.

Bug: 1382033


(cherry picked from commit ce463c2c939818a12bbcec5e2c91c35f2a0a1f0e)

Change-Id: I2fd3f075d5071cb0cf647838782115b5c00405bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035891
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1073566}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4213051
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1381}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/471e5b79ba1850ba327cd19d54b008da70ba2578/services/network/throttling/network_conditions.h
[modify] https://crrev.com/471e5b79ba1850ba327cd19d54b008da70ba2578/services/network/public/mojom/network_context.mojom
[modify] https://crrev.com/471e5b79ba1850ba327cd19d54b008da70ba2578/services/network/throttling/throttling_controller_unittest.cc
[modify] https://crrev.com/471e5b79ba1850ba327cd19d54b008da70ba2578/services/network/throttling/network_conditions.cc


### rz...@google.com (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382033?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Services>Network, Platform>DevTools>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061636)*
