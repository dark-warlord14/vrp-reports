# Security: UAF in content::NavigationRequest::SetViewTransitionState  in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40061915](https://issues.chromium.org/issues/40061915) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>ViewTransitions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | vm...@chromium.org |
| **Created** | 2022-11-25 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::NavigationRequest::SetViewTransitionState in browser process

**VERSION**

Chromium 110.0.5440.0 (Developer Build) (64-bit)  

Revision aae16b01ed3ff0b2fb0aabdfdb96ef883ef316c8-refs/heads/main@{#1075749}  

OS Windows 10 Version 22H2 (Build 19045.2251)

**REPRODUCTION CASE**  

Run the command:  

chrome.exe --user-data-dir=c:/tmp/any --enable-features=ViewTransitionOnNavigation <http://localhost/poc.html>

This issue can also reproduce in Linux.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

=================================================================  

==22384==ERROR: AddressSanitizer: heap-use-after-free on address 0x132f26ec2190 at pc 0x7ff8698bf9ec bp 0x00fe2dffe770 sp 0x00fe2dffe7b8  

READ of size 8 at 0x132f26ec2190 thread T0  

==22384==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8698bf9eb in content::NavigationRequest::SetViewTransitionState C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:8294  

#1 0x7ff869ae82a2 in content::`anonymous namespace'::OnSnapshotAck C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\view_transition_commit_deferring_condition.cc:21 #2 0x7ff869ae8599 in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<void ()>, content::NavigationRequest \*, const blink::ViewTransitionState &),base::OnceCallback<void ()>,base::internal::UnretainedWrapper<content::NavigationRequest,base::RawPtrBanDanglingIfSupported> >,void (const blink::ViewTransitionState &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:894 #3 0x7ff8649b44e7 in blink::mojom::LocalFrame_SnapshotDocumentForViewTransition_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\frame\frame.mojom.cc:13723 #4 0x7ff86e6cad82 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1002 #5 0x7ff87158154a in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #6 0x7ff86e6cf28b in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:694 #7 0x7ff86ec99ce7 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1080  

#8 0x7ff86ec92127 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#9 0x7ff86e3fa679 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#10 0x7ff871416f31 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#11 0x7ff871415a22 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#12 0x7ff86e4ac342 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#13 0x7ff86e4aa4c0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#14 0x7ff871419363 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#15 0x7ff86e386bbe in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#16 0x7ff868bd6ddd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#17 0x7ff868bdd67b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#18 0x7ff868bcfb11 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#19 0x7ff86df3bf1d in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:692  

#20 0x7ff86df3f715 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1230  

#21 0x7ff86df3ee86 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1086  

#22 0x7ff86df39fa6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#23 0x7ff86df3ae01 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#24 0x7ff8618214a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#25 0x7ff7f94d6288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#26 0x7ff7f94d2c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#27 0x7ff7f990166b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#28 0x7ff942e374b3 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x1800174b3)  

#29 0x7ff9431e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x132f26ec2190 is located 144 bytes inside of 5760-byte region [0x132f26ec2100,0x132f26ec3780)  

freed by thread T0 here:  

#0 0x7ff7f9583ffd in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8698bfa09 in content::NavigationRequest::~NavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1886  

#2 0x7ff8696cb317 in content::FrameTreeNode::ResetNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:573  

#3 0x7ff8698dc316 in content::Navigator::CancelNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:1091  

#4 0x7ff8698c5785 in base::internal::Invoker<base::internal::BindState<void (content::NavigationRequest::\*)(),base::internal::UnretainedWrapper[content::NavigationRequest,base::RawPtrBanDanglingIfSupported](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#5 0x7ff86e6cf85e in mojo::InterfaceEndpointClient::NotifyError C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:730  

#6 0x7ff86ec98259 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::NotifyEndpointOfError C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:884 #7 0x7ff86ec9873e in IPC::`anonymous namespace'::ChannelAssociatedGroupController::NotifyEndpointOfErrorOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:904  

#8 0x7ff86ec9895f in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(unsigned int, IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint \*),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,unsigned int,base::internal::UnretainedWrapper<IPC::(anonymous namespace)::ChannelAssociatedGroupController::Endpoint,base::RawPtrMayDangle> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#9 0x7ff86e3fa679 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#10 0x7ff871416f31 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#11 0x7ff871415a22 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#12 0x7ff86e4ac342 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#13 0x7ff86e4aa4c0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#14 0x7ff871419363 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#15 0x7ff86e386bbe in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#16 0x7ff868bd6ddd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#17 0x7ff868bdd67b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#18 0x7ff868bcfb11 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#19 0x7ff86df3bf1d in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:692  

#20 0x7ff86df3f715 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1230  

#21 0x7ff86df3ee86 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1086  

#22 0x7ff86df39fa6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#23 0x7ff86df3ae01 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#24 0x7ff8618214a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#25 0x7ff7f94d6288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#26 0x7ff7f94d2c0a in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#27 0x7ff7f990166b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288

previously allocated by thread T0 here:  

#0 0x7ff7f95840fd in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff882b3935e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff86987ade7 in content::NavigationRequest::CreateRendererInitiated C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1285  

#3 0x7ff8698dc882 in content::Navigator::OnBeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:1016  

#4 0x7ff869950063 in content::RenderFrameHostImpl::BeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:7829  

#5 0x7ff8652e7e0b in content::mojom::FrameHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:5540  

#6 0x7ff86e6caa37 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:1007  

#7 0x7ff871581444 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#8 0x7ff86e6cf28b in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:694  

#9 0x7ff86ec99ce7 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1080  

#10 0x7ff86ec92127 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:894  

#11 0x7ff86e3fa679 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:156  

#12 0x7ff871416f31 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:449  

#13 0x7ff871415a22 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:300  

#14 0x7ff86e4ac342 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#15 0x7ff86e4aa4c0 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#16 0x7ff871419363 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:609  

#17 0x7ff86e386bbe in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#18 0x7ff868bd6ddd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1050  

#19 0x7ff868bdd67b in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:162  

#20 0x7ff868bcfb11 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:32  

#21 0x7ff86df3bf1d in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:692  

#22 0x7ff86df3f715 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1230  

#23 0x7ff86df3ee86 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1086  

#24 0x7ff86df39fa6 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:344  

#25 0x7ff86df3ae01 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#26 0x7ff8618214a5 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:174  

#27 0x7ff7f94d6288 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:8294 in content::NavigationRequest::SetViewTransitionState  

Shadow bytes around the buggy address:  

0x132f26ec1f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x132f26ec1f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x132f26ec2000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x132f26ec2080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

0x132f26ec2100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x132f26ec2180: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x132f26ec2200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x132f26ec2280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x132f26ec2300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x132f26ec2380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x132f26ec2400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

MiraclePtr Status: PROTECTED  

This crash occurred inside a callback where a raw\_ptr<T> pointing to the same region was bound to one of the arguments.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==22384==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 87 B)

## Timeline

### [Deleted User] (2022-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4844505682608128.

### cl...@chromium.org (2022-11-29)

ClusterFuzz testcase 4844505682608128 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2022-11-29)

Detailed Report: https://clusterfuzz.com/testcase?key=4844505682608128

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1076254

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4844505682608128

Additional requirements: Requires HTTP

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### ct...@chromium.org (2022-11-29)

Thanks for your report! Clusterfuzz is having difficulties reproducing this -- I'll test manually and update the bug.

### ct...@chromium.org (2022-11-29)

Confirmed that I can reproduce this on Linux ASAN r1070077 (M109) and r1076097 (M110). Can't repro on r1036826 (M106), r1047724 (M107), r1058931 (M108). 

It looks like the ViewTransition feature was renamed from DocumentTransition (https://chromium-review.googlesource.com/c/chromium/src/+/3993505), but the ViewTransitionOnNavigation feature was added after that rename in https://chromium-review.googlesource.com/c/chromium/src/+/3979953 and is likely the culprit.

Based on crrev.com/c/3979953, cc'ing khushalsagar@ who is OOO and assigning this to vmpstr@.

Setting security labels: Severity-Critical (zero interaction browser-process UAF) but Security_Impact-None due to this feature not being enabled anywhere yet as far as I can tell.

[Monorail components: Blink>ViewTransitions]

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4200b3628f3bf45133fefe67d0947f0f6899eb29

commit 4200b3628f3bf45133fefe67d0947f0f6899eb29
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Wed Nov 30 18:36:00 2022

VTOnNav: Fix UAF that happens if the navigation request is deleted

We wait for the capture to ack before setting capture parameters.
However, during this, the navigation request can be deleted.

This patch fixes that by using a weak ptr on the navigation request.

Also fixes a couple of other DCHECKs that happened as a result of
testing this.

R=khushalsagar@chromium.org, alexmos@chromium.org

Bug: 1393564
Change-Id: I71e225eaa03fe8e74f9c07cc6deeee0da9a46c8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4061374
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077590}

[add] https://crrev.com/4200b3628f3bf45133fefe67d0947f0f6899eb29/third_party/blink/web_tests/wpt_internal/view-transition-on-navigation/reload-crash.html
[modify] https://crrev.com/4200b3628f3bf45133fefe67d0947f0f6899eb29/third_party/blink/renderer/core/view_transition/view_transition_supplement.cc
[modify] https://crrev.com/4200b3628f3bf45133fefe67d0947f0f6899eb29/content/browser/renderer_host/view_transition_commit_deferring_condition.cc
[modify] https://crrev.com/4200b3628f3bf45133fefe67d0947f0f6899eb29/third_party/blink/renderer/core/view_transition/view_transition.cc


### vm...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, asnine! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-10)

This issue was migrated from crbug.com/chromium/1393564?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061915)*
