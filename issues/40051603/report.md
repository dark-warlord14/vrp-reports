# UAF in chrome chrome!content::BrowserAccessibilityManager::GetFromAXNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40051603](https://issues.chromium.org/issues/40051603) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | UI>Accessibility |
| **Platforms** | Windows |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2020-02-24 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

Use-After-Free vulnerability related to accessibility affecting browser process in chrome!std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<int,content::BrowserAccessibility \*>,std::\_\_1::\_\_map\_value\_compare<int,std::\_\_1::\_\_value\_type<int,content::BrowserAccessibility \*>,std::\_\_1::less<int>,1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<int,content::BrowserAccessibility \*> > >::\_\_lower\_bound+0x5 (Inline Function @ 00007ff8`4383a23c) [c:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree @ 2652]

For reproducing the case run chrome with the following flags:  

chrome.exe --force-renderer-accessibility --no-sandbox

**VERSION**  

Chrome Version: 82.0.4062.3 dev  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

Minimized testcase together with windbg logs attached.

**CREDIT INFORMATION**

Reporter credit: Pawel Wylecial of REDTEAM.PL

## Attachments

- [cm_access22.html](attachments/cm_access22.html) (text/plain, 593 B)
- [windbg.txt](attachments/windbg.txt) (text/plain, 5.7 KB)

## Timeline

### aj...@google.com (2020-02-24)

Thanks for the report. This reproduces on TOT (ish) with ASAN:-

C:\src\chromium\src [icon]> .\out\asan\chrome.exe --no-sandbox --force-renderer-accessibility C:\src\pocs\1055393\cm_access22.html
=================================================================
==2312==ERROR: AddressSanitizer: heap-use-after-free on address 0x118d1be5db50 at pc 0x7fff66a98c2b bp 0x0015b31fe620 sp 0x0015b31fe668
READ of size 4 at 0x118d1be5db50 thread T0
    #0 0x7fff66a98c2a in content::BrowserAccessibilityManager::GetFromAXNode C:\src\chromium\src\content\browser\accessibility\browser_accessibility_manager.cc:312
    #1 0x7fff66a99c2c in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\src\chromium\src\content\browser\accessibility\browser_accessibility_manager.cc:439
    #2 0x7fff671b35e2 in content::RenderFrameHostImpl::OnAccessibilityEvents C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:3867
    #3 0x7fff671b2f2c in IPC::MessageT<AccessibilityHostMsg_EventBundle_Meta,std::__1::tuple<AccessibilityHostMsg_EventBundleParams,int,int>,void>::Dispatch<content::RenderFrameHostImpl,content::RenderFrameHostImpl,void,void (content::RenderFrameHostImpl::*)(const AccessibilityHostMsg_EventBundleParams &, int, int)> C:\src\chromium\src\ipc\ipc_message_templates.h:146
    #4 0x7fff671add60 in content::RenderFrameHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:1712
    #5 0x7fff677ca9ae in content::RenderProcessHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\renderer_host\render_process_host_impl.cc:3521
    #6 0x7fff6d37782d in IPC::ChannelProxy::Context::OnDispatchMessage C:\src\chromium\src\ipc\ipc_channel_proxy.cc:327
    #7 0x7fff6ca73933 in base::TaskAnnotator::RunTask C:\src\chromium\src\base\task\common\task_annotator.cc:142
    #8 0x7fff6efdc73b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:365
    #9 0x7fff6efdbeea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:219
    #10 0x7fff6cb5fe54 in base::MessagePumpForUI::DoRunLoop C:\src\chromium\src\base\message_loop\message_pump_win.cc:217
    #11 0x7fff6cb5d82a in base::MessagePumpWin::Run C:\src\chromium\src\base\message_loop\message_pump_win.cc:74
    #12 0x7fff6efde669 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #13 0x7fff6ca26e51 in base::RunLoop::Run C:\src\chromium\src\base\run_loop.cc:124
    #14 0x7fff71805e57 in ChromeBrowserMainParts::MainMessageLoopRun C:\src\chromium\src\chrome\browser\chrome_browser_main.cc:1691
    #15 0x7fff66d27af0 in content::BrowserMainLoop::RunMainMessageLoopParts C:\src\chromium\src\content\browser\browser_main_loop.cc:1056
    #16 0x7fff66d2e0db in content::BrowserMainRunnerImpl::Run C:\src\chromium\src\content\browser\browser_main_runner_impl.cc:150
    #17 0x7fff66d1fb28 in content::BrowserMain C:\src\chromium\src\content\browser\browser_main.cc:47
    #18 0x7fff6c749644 in content::RunBrowserProcessMain C:\src\chromium\src\content\app\content_main_runner_impl.cc:527
    #19 0x7fff6c74be3f in content::ContentMainRunnerImpl::RunServiceManager C:\src\chromium\src\content\app\content_main_runner_impl.cc:952
    #20 0x7fff6c74b30f in content::ContentMainRunnerImpl::Run C:\src\chromium\src\content\app\content_main_runner_impl.cc:859
    #21 0x7fff6c80a060 in service_manager::Main C:\src\chromium\src\services\service_manager\embedder\main.cc:423
    #22 0x7fff6c74940e in content::ContentMain C:\src\chromium\src\content\app\content_main.cc:19
    #23 0x7fff63c41431 in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:110
    #24 0x7ff67f205bbe in MainDllLoader::Launch C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:177
    #25 0x7ff67f202a45 in main C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:265
    #26 0x7ff67f5ce46f in __scrt_common_main_seh d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #27 0x7ffff8787bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)
    #28 0x7ffff984ced0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006ced0)

0x118d1be5db50 is located 80 bytes inside of 336-byte region [0x118d1be5db00,0x118d1be5dc50)
freed by thread T0 here:
    #0 0x7ff67f29cfde in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7fff6db17902 in ui::AXTree::DestroyNodeAndSubtree C:\src\chromium\src\ui\accessibility\ax_tree.cc:1755
    #2 0x7fff6db1ba79 in ui::AXTree::Unserialize C:\src\chromium\src\ui\accessibility\ax_tree.cc:931
    #3 0x7fff66a9956d in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\src\chromium\src\content\browser\accessibility\browser_accessibility_manager.cc:386
    #4 0x7fff671b35e2 in content::RenderFrameHostImpl::OnAccessibilityEvents C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:3867
    #5 0x7fff671b2f2c in IPC::MessageT<AccessibilityHostMsg_EventBundle_Meta,std::__1::tuple<AccessibilityHostMsg_EventBundleParams,int,int>,void>::Dispatch<content::RenderFrameHostImpl,content::RenderFrameHostImpl,void,void (content::RenderFrameHostImpl::*)(const AccessibilityHostMsg_EventBundleParams &, int, int)> C:\src\chromium\src\ipc\ipc_message_templates.h:146
    #6 0x7fff671add60 in content::RenderFrameHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:1712
    #7 0x7fff677ca9ae in content::RenderProcessHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\renderer_host\render_process_host_impl.cc:3521
    #8 0x7fff6d37782d in IPC::ChannelProxy::Context::OnDispatchMessage C:\src\chromium\src\ipc\ipc_channel_proxy.cc:327
    #9 0x7fff6ca73933 in base::TaskAnnotator::RunTask C:\src\chromium\src\base\task\common\task_annotator.cc:142
    #10 0x7fff6efdc73b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:365
    #11 0x7fff6efdbeea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:219
    #12 0x7fff6cb5fe54 in base::MessagePumpForUI::DoRunLoop C:\src\chromium\src\base\message_loop\message_pump_win.cc:217
    #13 0x7fff6cb5d82a in base::MessagePumpWin::Run C:\src\chromium\src\base\message_loop\message_pump_win.cc:74
    #14 0x7fff6efde669 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #15 0x7fff6ca26e51 in base::RunLoop::Run C:\src\chromium\src\base\run_loop.cc:124
    #16 0x7fff71805e57 in ChromeBrowserMainParts::MainMessageLoopRun C:\src\chromium\src\chrome\browser\chrome_browser_main.cc:1691
    #17 0x7fff66d27af0 in content::BrowserMainLoop::RunMainMessageLoopParts C:\src\chromium\src\content\browser\browser_main_loop.cc:1056
    #18 0x7fff66d2e0db in content::BrowserMainRunnerImpl::Run C:\src\chromium\src\content\browser\browser_main_runner_impl.cc:150
    #19 0x7fff66d1fb28 in content::BrowserMain C:\src\chromium\src\content\browser\browser_main.cc:47
    #20 0x7fff6c749644 in content::RunBrowserProcessMain C:\src\chromium\src\content\app\content_main_runner_impl.cc:527
    #21 0x7fff6c74be3f in content::ContentMainRunnerImpl::RunServiceManager C:\src\chromium\src\content\app\content_main_runner_impl.cc:952
    #22 0x7fff6c74b30f in content::ContentMainRunnerImpl::Run C:\src\chromium\src\content\app\content_main_runner_impl.cc:859
    #23 0x7fff6c80a060 in service_manager::Main C:\src\chromium\src\services\service_manager\embedder\main.cc:423
    #24 0x7fff6c74940e in content::ContentMain C:\src\chromium\src\content\app\content_main.cc:19
    #25 0x7fff63c41431 in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:110
    #26 0x7ff67f205bbe in MainDllLoader::Launch C:\src\chromium\src\chrome\app\main_dll_loader_win.cc:177
    #27 0x7ff67f202a45 in main C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc:265
    #28 0x7ff67f5ce46f in __scrt_common_main_seh d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288

previously allocated by thread T0 here:
    #0 0x7ff67f29d0ce in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7fff7c59010a in operator new d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7fff6db29fed in ui::AXTree::CreateNode C:\src\chromium\src\ui\accessibility\ax_tree.cc:1147
    #3 0x7fff6db2fc91 in ui::AXTree::CreateNewChildVector C:\src\chromium\src\ui\accessibility\ax_tree.cc:1800
    #4 0x7fff6db20f74 in ui::AXTree::UpdateNode C:\src\chromium\src\ui\accessibility\ax_tree.cc:1393
    #5 0x7fff6db1c2ec in ui::AXTree::Unserialize C:\src\chromium\src\ui\accessibility\ax_tree.cc:952
    #6 0x7fff66a9956d in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\src\chromium\src\content\browser\accessibility\browser_accessibility_manager.cc:386
    #7 0x7fff671b35e2 in content::RenderFrameHostImpl::OnAccessibilityEvents C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:3867
    #8 0x7fff671b2f2c in IPC::MessageT<AccessibilityHostMsg_EventBundle_Meta,std::__1::tuple<AccessibilityHostMsg_EventBundleParams,int,int>,void>::Dispatch<content::RenderFrameHostImpl,content::RenderFrameHostImpl,void,void (content::RenderFrameHostImpl::*)(const AccessibilityHostMsg_EventBundleParams &, int, int)> C:\src\chromium\src\ipc\ipc_message_templates.h:146
    #9 0x7fff671add60 in content::RenderFrameHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\frame_host\render_frame_host_impl.cc:1712
    #10 0x7fff677ca9ae in content::RenderProcessHostImpl::OnMessageReceived C:\src\chromium\src\content\browser\renderer_host\render_process_host_impl.cc:3521
    #11 0x7fff6d37782d in IPC::ChannelProxy::Context::OnDispatchMessage C:\src\chromium\src\ipc\ipc_channel_proxy.cc:327
    #12 0x7fff6ca73933 in base::TaskAnnotator::RunTask C:\src\chromium\src\base\task\common\task_annotator.cc:142
    #13 0x7fff6efdc73b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:365
    #14 0x7fff6efdbeea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:219
    #15 0x7fff6cb5fe54 in base::MessagePumpForUI::DoRunLoop C:\src\chromium\src\base\message_loop\message_pump_win.cc:217
    #16 0x7fff6cb5d82a in base::MessagePumpWin::Run C:\src\chromium\src\base\message_loop\message_pump_win.cc:74
    #17 0x7fff6efde669 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #18 0x7fff6ca26e51 in base::RunLoop::Run C:\src\chromium\src\base\run_loop.cc:124
    #19 0x7fff71805e57 in ChromeBrowserMainParts::MainMessageLoopRun C:\src\chromium\src\chrome\browser\chrome_browser_main.cc:1691
    #20 0x7fff66d27af0 in content::BrowserMainLoop::RunMainMessageLoopParts C:\src\chromium\src\content\browser\browser_main_loop.cc:1056
    #21 0x7fff66d2e0db in content::BrowserMainRunnerImpl::Run C:\src\chromium\src\content\browser\browser_main_runner_impl.cc:150
    #22 0x7fff66d1fb28 in content::BrowserMain C:\src\chromium\src\content\browser\browser_main.cc:47
    #23 0x7fff6c749644 in content::RunBrowserProcessMain C:\src\chromium\src\content\app\content_main_runner_impl.cc:527
    #24 0x7fff6c74be3f in content::ContentMainRunnerImpl::RunServiceManager C:\src\chromium\src\content\app\content_main_runner_impl.cc:952
    #25 0x7fff6c74b30f in content::ContentMainRunnerImpl::Run C:\src\chromium\src\content\app\content_main_runner_impl.cc:859
    #26 0x7fff6c80a060 in service_manager::Main C:\src\chromium\src\services\service_manager\embedder\main.cc:423
    #27 0x7fff6c74940e in content::ContentMain C:\src\chromium\src\content\app\content_main.cc:19
    #28 0x7fff63c41431 in ChromeMain C:\src\chromium\src\chrome\app\chrome_main.cc:110

SUMMARY: AddressSanitizer: heap-use-after-free C:\src\chromium\src\content\browser\accessibility\browser_accessibility_manager.cc:312 in content::BrowserAccessibilityManager::GetFromAXNode
Shadow bytes around the buggy address:
  0x0398bf14bb10: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0398bf14bb20: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0398bf14bb30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0398bf14bb40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0398bf14bb50: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0398bf14bb60: fd fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd
  0x0398bf14bb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0398bf14bb80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0398bf14bb90: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0398bf14bba0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0398bf14bbb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==2312==ABORTING

### aj...@google.com (2020-02-24)

This also crashes if the sandbox is enabled. Marking as High not Critical as accessibility must be enabled.

dmazzoni@ this is perhaps similar to https://crbug.com/1038660 so I'm assigning to you. Please feel free to assign to someone else if they are better qualified to fix/investigate this security issue.



[Monorail components: UI>Accessibility]

### ad...@google.com (2020-02-25)

I'm going to bump this up to Critical. Our past precedent has been: those users who need to use accessibility, *need* to use accessibility, so disabling accessibility is not a mitigation.

### cl...@chromium.org (2020-02-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5677143167139840.

### ad...@google.com (2020-02-25)

[Empty comment from Monorail migration]

### aj...@google.com (2020-02-25)

Adding some CC's.

### dm...@chromium.org (2020-02-25)

Looks like it was my bad patch.

The UAF goes away if I revert r737100: https://chromium-review.googlesource.com/c/chromium/src/+/1988742 - first landed in 81.0.4044.0.

We need to first revert r738876 (dependent change), though that revert does not need to be merged to 81.

First revert going in now: https://chromium-review.googlesource.com/c/chromium/src/+/2071785



### dm...@chromium.org (2020-02-25)

First revert is done. Second one: https://chromium-review.googlesource.com/c/chromium/src/+/2071593


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5f8592f7c985a5fd89d59537d4b016ffca242f12

commit 5f8592f7c985a5fd89d59537d4b016ffca242f12
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Tue Feb 25 08:52:31 2020

Revert "Re-land: Fire live region events when a node is removed."

This reverts commit 16ce044f817f76400ae738157bb4b7d855c80932.

Reason for revert: crbug.com/1055393

Original change's description:
> Re-land: Fire live region events when a node is removed.
>
> Adds an AXLiveRegionTracker class to keep track of live regions
> in an AXTree. Uses it to fix a bug where we weren't firing the
> LIVE_REGION_CHANGED event on the live root when a node was removed,
> only when a node was added or changed.
>
> I'm going to follow this up with code that optionally computes
> the text of a live region change, that we can use on Android,
> Chrome OS, and some older versions of macOS. So AXLiveRegionTracker
> is simple now, but it will be a convenient place to put that
> logic.
>
> Originally landed as https://crrev.com/c/1464325, but reverted
> due to a UAF. The issue was that in LiveRegionTracker we were
> keeping track of a mapping from node to live region root, and
> when a node was deleted from the tree we were deleting it from
> the key of that map, but we also needed to delete it from the
> value. We do that now by temporarily keeping track of a set of
> deleted node IDs.
>
> Bug: 560599, 930763
> Change-Id: I2005656fb50a208b00f744def828ce8db2134be1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1988742
> Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
> Reviewed-by: Kevin Babbitt <kbabbitt@microsoft.com>
> Cr-Commit-Position: refs/heads/master@{#737100}

TBR=dmazzoni@chromium.org,kbabbitt@microsoft.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 560599, 930763, 1055393
Tbr: kbabbitt@microsoft.com
Change-Id: I444faccaa5e444ec4093967f2d974045c4a84b47
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2071593
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#744218}

[modify] https://crrev.com/5f8592f7c985a5fd89d59537d4b016ffca242f12/ui/accessibility/BUILD.gn
[modify] https://crrev.com/5f8592f7c985a5fd89d59537d4b016ffca242f12/ui/accessibility/ax_event_generator.cc
[modify] https://crrev.com/5f8592f7c985a5fd89d59537d4b016ffca242f12/ui/accessibility/ax_event_generator.h
[modify] https://crrev.com/5f8592f7c985a5fd89d59537d4b016ffca242f12/ui/accessibility/ax_event_generator_unittest.cc
[delete] https://crrev.com/2b1664a9d37a6fd9f5ac7a19936ae8d48814b29e/ui/accessibility/ax_live_region_tracker.cc
[delete] https://crrev.com/2b1664a9d37a6fd9f5ac7a19936ae8d48814b29e/ui/accessibility/ax_live_region_tracker.h


### cl...@chromium.org (2020-02-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Sandbox>SiteIsolation]

### cl...@chromium.org (2020-02-25)

Detailed Report: https://clusterfuzz.com/testcase?key=5677143167139840

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x6140001baed0
Crash State:
  content::BrowserAccessibilityManager::OnAccessibilityEvents
  content::RenderFrameHostImpl::OnAccessibilityEvents
  bool IPC::MessageT<AccessibilityHostMsg_EventBundle_Meta, std::__1::tuple<Access
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=727588:727589

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5677143167139840

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5677143167139840 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-02-25)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-25)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-02-25)

Dominic, thanks for jumping on it!

I don't understand why ClusterFuzz has decided that this is Security_Impact-Head, rather than Security_Impact-Beta. +mbarbella@, could you look into it?

Great that this doesn't affect stable. No need for yet another sudden release!

### [Deleted User] (2020-02-25)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-25)

ClusterFuzz testcase 5677143167139840 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=744217:744218

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-02-25)

[Empty comment from Monorail migration]

### dm...@chromium.org (2020-02-26)

[Empty comment from Monorail migration]

### dm...@chromium.org (2020-02-26)

Requesting to merge this change to M-81:
https://chromium-review.googlesource.com/c/chromium/src/+/2071593

It's a revert of the patch that caused the UAF. Please approve ASAP, thanks.


### ad...@google.com (2020-02-26)

Approving merge of the revert to M81 (branch 4044).

### [Deleted User] (2020-03-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2020-03-03)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Sandbox>SiteIsolation]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/070a9cd134ade3d2d8ab5e41ece89924daf5fa79

commit 070a9cd134ade3d2d8ab5e41ece89924daf5fa79
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Tue Mar 03 17:58:23 2020

Merge to M81: Revert "Re-land: Fire live region events when a node is removed."

This reverts commit 16ce044f817f76400ae738157bb4b7d855c80932.

Reason for revert: crbug.com/1055393

Original change's description:
> Re-land: Fire live region events when a node is removed.
>
> Adds an AXLiveRegionTracker class to keep track of live regions
> in an AXTree. Uses it to fix a bug where we weren't firing the
> LIVE_REGION_CHANGED event on the live root when a node was removed,
> only when a node was added or changed.
>
> I'm going to follow this up with code that optionally computes
> the text of a live region change, that we can use on Android,
> Chrome OS, and some older versions of macOS. So AXLiveRegionTracker
> is simple now, but it will be a convenient place to put that
> logic.
>
> Originally landed as https://crrev.com/c/1464325, but reverted
> due to a UAF. The issue was that in LiveRegionTracker we were
> keeping track of a mapping from node to live region root, and
> when a node was deleted from the tree we were deleting it from
> the key of that map, but we also needed to delete it from the
> value. We do that now by temporarily keeping track of a set of
> deleted node IDs.
>
> Bug: 560599, 930763
> Change-Id: I2005656fb50a208b00f744def828ce8db2134be1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1988742
> Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
> Reviewed-by: Kevin Babbitt <kbabbitt@microsoft.com>
> Cr-Commit-Position: refs/heads/master@{#737100}

TBR=dmazzoni@chromium.org,kbabbitt@microsoft.com

# Not skipping CQ checks because original CL landed > 1 day ago.

(cherry picked from commit 5f8592f7c985a5fd89d59537d4b016ffca242f12)

Bug: 560599, 930763, 1055393
Tbr: kbabbitt@microsoft.com
Change-Id: I444faccaa5e444ec4093967f2d974045c4a84b47
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2071593
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#744218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2082316
Cr-Commit-Position: refs/branch-heads/4044@{#595}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/070a9cd134ade3d2d8ab5e41ece89924daf5fa79/ui/accessibility/BUILD.gn
[modify] https://crrev.com/070a9cd134ade3d2d8ab5e41ece89924daf5fa79/ui/accessibility/ax_event_generator.cc
[modify] https://crrev.com/070a9cd134ade3d2d8ab5e41ece89924daf5fa79/ui/accessibility/ax_event_generator.h
[modify] https://crrev.com/070a9cd134ade3d2d8ab5e41ece89924daf5fa79/ui/accessibility/ax_event_generator_unittest.cc
[delete] https://crrev.com/e375164098f3404dc700e54b296b2033d6977002/ui/accessibility/ax_live_region_tracker.cc
[delete] https://crrev.com/e375164098f3404dc700e54b296b2033d6977002/ui/accessibility/ax_live_region_tracker.h


### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

CONGRATS! The Panel decided to award $20,000 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### mm...@google.com (2020-03-06)

dmazzoni@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-03-09)

Pawel, awesome work here (as well as in https://crbug.com/chromium/1041406). Did you run any fuzzers to find these? If so, let me invite you to Chrome Fuzzer Program. In a nutshell, we can run you fuzzer(s) on ClusterFuzz and you'll automatically get rewarded for the security bugs (plus $1,000 bonus on each finding). You can read more in https://www.google.com/about/appsecurity/chrome-rewards/#fuzzerprogram

Please reach out to me if you have any questions.

### pa...@blackowlsec.com (2020-03-09)

thank you! I did use fuzzing to find these bugs, I will check the program rules and contact you directly via e-mail if im interested / have questions.

### mm...@google.com (2020-03-10)

dmazzoni@, friendly ping re c#29.

### ad...@google.com (2020-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1055393?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1059952]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051603)*
