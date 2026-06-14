# Read AV in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40092222](https://issues.chromium.org/issues/40092222) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2018-08-18 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/iframer.php?url=PIP.html
2. Open devtool and click "Toggle Picture-in-Picture"
3. Open new tab and close previous tab

What is the expected behavior?
No crash

What went wrong?
I can't tell much without the symbol...

(2ed8.2c88): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Users\jukokats\AppData\Local\Google\Chrome SxS\Application\70.0.3526.0\chrome.dll - 
chrome!ovly_debug_event+0x6b52e9:
00007ff8`07d4a0b9 ff5030          call    qword ptr [rax+30h] ds:00000001`0000006e=????????????????
0:000> r
rax=000000010000003e rbx=00000172df8eaad0 rcx=00000172dd5b7ff0
rdx=0000000000000000 rsi=00000172dd97add0 rdi=00000172dd5b7ff0
rip=00007ff807d4a0b9 rsp=00000028473fdea0 rbp=00000028473fdfa0
 r8=0000000000000038  r9=0000000000000000 r10=00000172df8df4c0
r11=0000000000000000 r12=00000172dd906450 r13=00000172dd9062f0
r14=00000172dfb46940 r15=00000172daa88490
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
chrome!ovly_debug_event+0x6b52e9:
00007ff8`07d4a0b9 ff5030          call    qword ptr [rax+30h] ds:00000001`0000006e=????????????????
0:000> ub
chrome!ovly_debug_event+0x6b52cc:
00007ff8`07d4a09c 7438            je      chrome!ovly_debug_event+0x6b5306 (00007ff8`07d4a0d6)
00007ff8`07d4a09e 488b7e38        mov     rdi,qword ptr [rsi+38h]
00007ff8`07d4a0a2 b938000000      mov     ecx,38h
00007ff8`07d4a0a7 e850bfd601      call    chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x1061d23 (00007ff8`09ab5ffc)
00007ff8`07d4a0ac 4889c3          mov     rbx,rax
00007ff8`07d4a0af 4883c640        add     rsi,40h
00007ff8`07d4a0b3 488b07          mov     rax,qword ptr [rdi]
00007ff8`07d4a0b6 4889f9          mov     rcx,rdi
0:000> k30
 # Child-SP          RetAddr           Call Site
00 00000028`473fdea0 00007ff8`08df2af1 chrome!ovly_debug_event+0x6b52e9
01 00000028`473fdef0 00007ff8`07e47c64 chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x39e818
02 00000028`473fdf20 00007ff8`07e54dbc chrome!ovly_debug_event+0x7b2e94
03 00000028`473fe030 00007ff8`089e5422 chrome!ovly_debug_event+0x7bffec
04 00000028`473fe070 00007ff8`089e811d chrome!GetHandleVerifier+0x3ab212
05 00000028`473fe1d0 00007ff8`089e5f95 chrome!GetHandleVerifier+0x3adf0d
06 00000028`473fe2f0 00007ff8`089e60e6 chrome!GetHandleVerifier+0x3abd85
07 00000028`473fe3c0 00007ff8`08b1a87d chrome!GetHandleVerifier+0x3abed6
08 00000028`473fe410 00007ff8`07da1bc6 chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xc65a4
09 00000028`473fe450 00007ff8`0755625e chrome!ovly_debug_event+0x70cdf6
0a 00000028`473fe550 00007ff8`0755290d chrome!ChromeMain+0x6549ac
0b 00000028`473fe670 00007ff8`075527f2 chrome!ChromeMain+0x65105b
0c 00000028`473fe720 00007ff8`06f26c3c chrome!ChromeMain+0x650f40
0d 00000028`473fe760 00007ff8`06f26737 chrome!ChromeMain+0x2538a
0e 00000028`473fe880 00007ff8`06f1d845 chrome!ChromeMain+0x24e85
0f 00000028`473fe9e0 00007ff8`07030109 chrome!ChromeMain+0x1bf93
10 00000028`473fec10 00007ff8`06f1d53e chrome!ChromeMain+0x12e857
11 00000028`473fecc0 00007ff8`06f1d2a1 chrome!ChromeMain+0x1bc8c
12 00000028`473fed10 00007ff8`073269a6 chrome!ChromeMain+0x1b9ef
13 00000028`473fed40 00007ff8`073267b8 chrome!ChromeMain+0x4250f4
14 00000028`473fee10 00007ff8`07326763 chrome!ChromeMain+0x424f06
15 00000028`473feed0 00007ff8`06f1e100 chrome!ChromeMain+0x424eb1
16 00000028`473fef00 00007ff8`06f1dfc4 chrome!ChromeMain+0x1c84e
17 00000028`473fefe0 00007ff8`06f18c20 chrome!ChromeMain+0x1c712
18 00000028`473ff050 00007ff8`06f04ff8 chrome!ChromeMain+0x1736e
19 00000028`473ff200 00007ff8`06f04bf8 chrome!ChromeMain+0x3746
1a 00000028`473ff580 00007ff8`06f019ca chrome!ChromeMain+0x3346
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Users\jukokats\AppData\Local\Google\Chrome SxS\Application\chrome.exe - 
1b 00000028`473ff610 00007ff6`bf81376c chrome!ChromeMain+0x118
1c 00000028`473ff6f0 00007ff6`bf811699 chrome_exe!Ordinal0+0x376c
1d 00000028`473ff7e0 00007ff6`bf8c47c2 chrome_exe!Ordinal0+0x1699
1e 00000028`473ffbc0 00007ff8`66323034 chrome_exe!GetHandleVerifier+0x88fb2
1f 00000028`473ffc00 00007ff8`665c1431 KERNEL32!BaseThreadInitThunk+0x14
20 00000028`473ffc30 00000000`00000000 ntdll!RtlUserThreadStart+0x21

Here is a Crash Report ID: 7aa02066d876b4c1

Did this work before? N/A 

Chrome version: 69  Channel: dev
OS Version: 10.0
Flash Version: 

You might need to enable following flag
chrome://flags/#enable-surfaces-for-videos

## Timeline

### s....@gmail.com (2018-08-19)

I sometimes see different call stack. Not sure why, but here is another one.

(3d98.3d94): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!content::PictureInPictureWindowControllerImpl::OnLeavingPictureInPicture+0x75:
00007ff8`07d49f69 ff5030          call    qword ptr [rax+30h] ds:00000156`ed74e6b0=f9b5c14854b0b136
0:000> r
rax=00000156ed74e680 rbx=00000156ed700c60 rcx=00000156ea6a2800
rdx=0000000000000803 rsi=00000156ed093000 rdi=00000156ea6a2800
rip=00007ff807d49f69 rsp=000000275abfdcb0 rbp=000000275abfddb0
 r8=000000000000002d  r9=00000000000002b5 r10=00000156ed6f5dd0
r11=0000000000000000 r12=00000156ea340f70 r13=00000156ea340e10
r14=00000156ea55c060 r15=00000156ea5baa50
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome!content::PictureInPictureWindowControllerImpl::OnLeavingPictureInPicture+0x75:
00007ff8`07d49f69 ff5030          call    qword ptr [rax+30h] ds:00000156`ed74e6b0=f9b5c14854b0b136
0:000> ub
chrome!content::PictureInPictureWindowControllerImpl::OnLeavingPictureInPicture+0x58 [C:\b\c\b\win64_clang\src\content\browser\picture_in_picture\picture_in_picture_window_controller_impl.cc @ 198]:
00007ff8`07d49f4c 7438            je      chrome!content::PictureInPictureWindowControllerImpl::OnLeavingPictureInPicture+0x92 (00007ff8`07d49f86)
00007ff8`07d49f4e 488b7e38        mov     rdi,qword ptr [rsi+38h]
00007ff8`07d49f52 b938000000      mov     ecx,38h
00007ff8`07d49f57 e8e0ccd601      call    chrome!operator new (00007ff8`09ab6c3c)
00007ff8`07d49f5c 4889c3          mov     rbx,rax
00007ff8`07d49f5f 4883c640        add     rsi,40h
00007ff8`07d49f63 488b07          mov     rax,qword ptr [rdi]
00007ff8`07d49f66 4889f9          mov     rcx,rdi
0:000> k20
 # Child-SP          RetAddr           Call Site
00 00000027`5abfdcb0 00007ff8`08df3231 chrome!content::PictureInPictureWindowControllerImpl::OnLeavingPictureInPicture+0x75 [C:\b\c\b\win64_clang\src\content\browser\picture_in_picture\picture_in_picture_window_controller_impl.cc @ 199] 
01 00000027`5abfdd00 00007ff8`07e47fb4 chrome!PictureInPictureWindowManager::ContentsObserver::WebContentsDestroyed+0x2d [C:\b\c\b\win64_clang\src\chrome\browser\picture_in_picture\picture_in_picture_window_manager.cc @ 32] 
02 00000027`5abfdd30 00007ff8`07e5510c chrome!content::WebContentsImpl::~WebContentsImpl+0x5d8 [C:\b\c\b\win64_clang\src\content\browser\web_contents\web_contents_impl.cc @ 681] 
03 00000027`5abfde40 00007ff8`089e5c3a chrome!content::WebContentsImpl::~WebContentsImpl+0x10 [C:\b\c\b\win64_clang\src\content\browser\web_contents\web_contents_impl.cc @ 583] 
04 00000027`5abfde80 00007ff8`089e8935 chrome!TabStripModel::SendDetachWebContentsNotifications+0x404 [C:\b\c\b\win64_clang\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 521] 
05 00000027`5abfdfe0 00007ff8`089e67ad chrome!TabStripModel::CloseWebContentses+0x325 [C:\b\c\b\win64_clang\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 1467] 
06 00000027`5abfe100 00007ff8`089e68fe chrome!TabStripModel::InternalCloseTabs+0x111 [C:\b\c\b\win64_clang\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 1377] 
07 00000027`5abfe1d0 00007ff8`08b1b1fd chrome!TabStripModel::CloseWebContentsAt+0x56 [C:\b\c\b\win64_clang\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 672] 
08 00000027`5abfe220 00007ff8`07da1a76 chrome!chrome::CloseWebContents+0x32 [C:\b\c\b\win64_clang\src\chrome\browser\ui\browser_tabstrip.cc @ 84] 
09 00000027`5abfe260 00007ff8`07555e9e chrome!IPC::MessageT<ViewHostMsg_ClosePage_ACK_Meta,std::tuple<>,void>::Dispatch<content::RenderViewHostImpl,content::RenderViewHostImpl,void,void (content::RenderViewHostImpl::*)()>+0x74 [C:\b\c\b\win64_clang\src\ipc\ipc_message_templates.h @ 146] 
0a 00000027`5abfe360 00007ff8`07552547 chrome!content::RenderViewHostImpl::OnMessageReceived+0x1b2 [C:\b\c\b\win64_clang\src\content\browser\renderer_host\render_view_host_impl.cc @ 795] 
0b 00000027`5abfe480 00007ff8`0755242c chrome!content::RenderProcessHostImpl::OnMessageReceived+0xf5 [C:\b\c\b\win64_clang\src\content\browser\renderer_host\render_process_host_impl.cc @ 3144] 
0c 00000027`5abfe530 00007ff8`06f269ac chrome!IPC::ChannelProxy::Context::OnDispatchMessage+0x24 [C:\b\c\b\win64_clang\src\ipc\ipc_channel_proxy.cc @ 321] 
0d 00000027`5abfe570 00007ff8`06f264a7 chrome!base::debug::TaskAnnotator::RunTask+0x12c [C:\b\c\b\win64_clang\src\base\debug\task_annotator.cc @ 101] 
0e 00000027`5abfe690 00007ff8`06f1d5b5 chrome!base::MessageLoop::RunTask+0x247 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 433] 
0f 00000027`5abfe7f0 00007ff8`0702fe89 chrome!base::MessageLoop::DoWork+0x185 [C:\b\c\b\win64_clang\src\base\message_loop\message_loop.cc @ 514] 
10 00000027`5abfea20 00007ff8`06f1d2ae chrome!base::MessagePumpForUI::DoRunLoop+0xa9 [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 180] 
11 00000027`5abfead0 00007ff8`06f1d011 chrome!base::MessagePumpWin::Run+0x4e [C:\b\c\b\win64_clang\src\base\message_loop\message_pump_win.cc @ 54] 
12 00000027`5abfeb20 00007ff8`073265b6 chrome!base::RunLoop::Run+0x31 [C:\b\c\b\win64_clang\src\base\run_loop.cc @ 108] 
13 00000027`5abfeb50 00007ff8`073263c8 chrome!ChromeBrowserMainParts::MainMessageLoopRun+0x84 [C:\b\c\b\win64_clang\src\chrome\browser\chrome_browser_main.cc @ 2069] 
14 00000027`5abfec20 00007ff8`07326373 chrome!content::BrowserMainLoop::RunMainMessageLoopParts+0x48 [C:\b\c\b\win64_clang\src\content\browser\browser_main_loop.cc @ 1042] 
15 00000027`5abfece0 00007ff8`06f1de70 chrome!content::BrowserMainRunnerImpl::Run+0x11 [C:\b\c\b\win64_clang\src\content\browser\browser_main_runner_impl.cc @ 163] 
16 00000027`5abfed10 00007ff8`06f1dd34 chrome!content::BrowserMain+0xc6 [C:\b\c\b\win64_clang\src\content\browser\browser_main.cc @ 47] 
17 00000027`5abfedf0 00007ff8`06f18990 chrome!content::RunBrowserProcessMain+0x6f [C:\b\c\b\win64_clang\src\content\app\content_main_runner_impl.cc @ 536] 
18 00000027`5abfee60 00007ff8`06f04ff8 chrome!content::ContentMainRunnerImpl::Run+0x25e [C:\b\c\b\win64_clang\src\content\app\content_main_runner_impl.cc @ 893] 
19 00000027`5abff010 00007ff8`06f04bf8 chrome!service_manager::Main+0x333 [C:\b\c\b\win64_clang\src\services\service_manager\embedder\main.cc @ 472] 
1a 00000027`5abff390 00007ff8`06f019ca chrome!content::ContentMain+0x41 [C:\b\c\b\win64_clang\src\content\app\content_main.cc @ 19] 
1b 00000027`5abff420 00007ff7`44c1376c chrome!ChromeMain+0x118 [C:\b\c\b\win64_clang\src\chrome\app\chrome_main.cc @ 104] 
1c 00000027`5abff500 00007ff7`44c11699 chrome_exe!MainDllLoader::Launch+0x26c [C:\b\c\b\win64_clang\src\chrome\app\main_dll_loader_win.cc @ 201] 
1d 00000027`5abff5f0 00007ff7`44cc47c2 chrome_exe!wWinMain+0x699 [C:\b\c\b\win64_clang\src\chrome\app\chrome_exe_main_win.cc @ 230] 
1e 00000027`5abff9d0 00007ff8`66323034 chrome_exe!__scrt_common_main_seh+0x106 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 283] 
1f 00000027`5abffa10 00007ff8`665c1431 KERNEL32!BaseThreadInitThunk+0x14 [base\win32\client\thread.c @ 64] 
 

### s....@gmail.com (2018-08-19)

Another call stack.

(2d40.3b04): Access violation - code c0000005 (!!! second chance !!!)
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\SYSTEM32\ntdll.dll - 
00000293`df32a3d0 0000            add     byte ptr [rax],al ds:00000293`df155090=40
0:000> k20
 # Child-SP          RetAddr           Call Site
00 000000b7`081fe050 00000293`df210920 0x00000293`df32a3d0
01 000000b7`081fe058 00007ff8`08df3231 0x00000293`df210920
02 000000b7`081fe060 00007ff8`07e47fb4 chrome!PictureInPictureWindowManager::ContentsObserver::WebContentsDestroyed+0x2d [C:\b\c\b\win64_clang\src\chrome\browser\picture_in_picture\picture_in_picture_window_manager.cc @ 32] 
03 000000b7`081fe090 00000000`00000000 chrome!content::WebContentsImpl::~WebContentsImpl+0x5d8 [C:\b\c\b\win64_clang\src\content\browser\web_contents\web_contents_impl.cc @ 681] 
0:000> r
rax=00000293df155090 rbx=00007ff807d49f6c rcx=00000293df2caa10
rdx=0000000000000822 rsi=00007ff80a002d90 rdi=00007ff807d4a149
rip=00000293df32a3d0 rsp=000000b7081fe050 rbp=00000293dd4fe980
 r8=0000000000000023  r9=0000000000000164 r10=00000293df514620
r11=0000000000000000 r12=00007ff806f26875 r13=00000293df210920
r14=00007ff80a002d90 r15=000000b7081fe0c8
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010204
00000293`df32a3d0 0000            add     byte ptr [rax],al ds:00000293`df155090=40


### ca...@chromium.org (2018-08-19)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-08-19)

Picture in Picture is not in stable.

### ca...@chromium.org (2018-08-19)

Looks like the picture in picture mode is available behind a flag on 68.

[Monorail components: Blink>Media>PictureInPicture]

### ca...@chromium.org (2018-08-19)

mlamouri: Could you take a look at this issue with PIP? Thanks.

Since this only happens when the PIP feature and enable-surfaces-for-videos are enabled, setting this to low severity.

### ca...@chromium.org (2018-08-19)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-08-20)

PiP only works with enable-surfaces-for-videos flag. Though following says it’s enabled by default in Chrome 69. Really confusing.
https://www.chromestatus.com/feature/5729206566649856

### ml...@chromium.org (2018-08-20)

The confusion comes from the API being enabled in 69 but VideoSurfaceLayer, which is needed for the feature to fully work not making it. We decided to leave the API as "launched" but without the VideoSurfaceLayer feature, the API will reject all calls.

The crash appears to be reproducible on Dev and trunk.

### ml...@chromium.org (2018-08-20)

+lushnikov@ FYI

It seems that the main difference with or without devtools open is that WebContentsImpl::RenderViewTerminated isn't called whet devtools is opened so we ended up in a state where the PIPWindowManager notifies the controller. Unfortunately, that happens *after* the frames were deleted and we try to notify them that the video is now paused. The fix is simple but I wonder if we could avoid this difference in behaviour to start with.

### ml...@chromium.org (2018-08-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/282f95191a6917a3ed2138f76e8d6b2608e852e2

commit 282f95191a6917a3ed2138f76e8d6b2608e852e2
Author: Mounir Lamouri <mlamouri@chromium.org>
Date: Mon Aug 27 20:43:54 2018

Picture-in-Picture: bail early when closing window while WebContents is being destroyed.

The issue happens when the timing of destruction is different from the
usual one. For example, when Dev Tools are open.

Bug: 875621
Change-Id: I734b010a80e6926c5429fec79f93d63612673d09
Reviewed-on: https://chromium-review.googlesource.com/1187002
Commit-Queue: Mounir Lamouri <mlamouri@chromium.org>
Reviewed-by: apacible <apacible@chromium.org>
Cr-Commit-Position: refs/heads/master@{#586404}
[modify] https://crrev.com/282f95191a6917a3ed2138f76e8d6b2608e852e2/chrome/browser/picture_in_picture/picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/282f95191a6917a3ed2138f76e8d6b2608e852e2/content/browser/picture_in_picture/picture_in_picture_window_controller_impl.cc


### ml...@chromium.org (2018-08-27)

The feature is behind a Finch flag in 69 but we intend to have a 1% experiment so I think it would be good to merge this 2-line fix.

### sh...@chromium.org (2018-08-27)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-27)

This change is not yet baked/verified in canary. Pls update bug with canary result tomorrow.

+awhalley@ (Security TPM) for M69 merge review.

### s....@gmail.com (2018-08-28)

Is this really a low severity bug? OOB read in browser process doesn't sound low.

### ml...@chromium.org (2018-08-28)

I'm not part of the security team but given that it applies to a feature that did not launch, the impact on user is fairly small at least.

### aw...@google.com (2018-08-28)

re https://crbug.com/chromium/875621#c16, yep, this is at least a high.

govind@ - good for 69

### sh...@chromium.org (2018-08-28)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-28)

Approving merge to M69 branch 3497 based on comments #13 and #19. Please merge now. Thank you.

### bu...@chromium.org (2018-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb5a5252fe7ac0161dc66b500aac74f4890e7a17

commit fb5a5252fe7ac0161dc66b500aac74f4890e7a17
Author: Mounir Lamouri <mlamouri@chromium.org>
Date: Tue Aug 28 17:26:55 2018

Picture-in-Picture: bail early when closing window while WebContents is being destroyed.

The issue happens when the timing of destruction is different from the
usual one. For example, when Dev Tools are open.

(cherry picked from commit 282f95191a6917a3ed2138f76e8d6b2608e852e2)

Bug: 875621
Change-Id: I734b010a80e6926c5429fec79f93d63612673d09
Reviewed-on: https://chromium-review.googlesource.com/1187002
Commit-Queue: Mounir Lamouri <mlamouri@chromium.org>
Reviewed-by: apacible <apacible@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#586404}
Reviewed-on: https://chromium-review.googlesource.com/1194260
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Cr-Commit-Position: refs/branch-heads/3497@{#827}
Cr-Branched-From: 271eaf50594eb818c9295dc78d364aea18c82ea8-refs/heads/master@{#576753}
[modify] https://crrev.com/fb5a5252fe7ac0161dc66b500aac74f4890e7a17/chrome/browser/picture_in_picture/picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/fb5a5252fe7ac0161dc66b500aac74f4890e7a17/content/browser/picture_in_picture/picture_in_picture_window_controller_impl.cc


### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

$5,000 for this report - thanks as ever!

### s....@gmail.com (2018-09-11)

Wow, thanks!

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/875621?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092222)*
