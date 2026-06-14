# Security: Heap-use-after-free in autofill::SaveCardBubbleViews::WindowClosing	

| Field | Value |
|-------|-------|
| **Issue ID** | [40087262](https://issues.chromium.org/issues/40087262) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2017-04-05 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 59.0.3063.0 (Official Build) canary (64-bit) + stable  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Lunch the index.html.
2. Click on the button.
3. On card.html try click on the button (submit) three or four or... clicks to submit the form to trigger the save bubble and the wait until the page (card.html) is closed.
4. Then as you can see the save credit card bubbles can appear over the wrong tab (index.html), now click on "Save" or "No thnaks" >> Crash.

## Attachments

- [PoC.rar](attachments/PoC.rar) (application/octet-stream, 873 B)
- [Recording #10.mp4](attachments/Recording #10.mp4) (video/mp4, 454.8 KB)
- [heap-use-after-free on address 0x20adfb00.txt](attachments/heap-use-after-free on address 0x20adfb00.txt) (text/plain, 11.9 KB)

## Timeline

### ch...@gmail.com (2017-04-05)

Crash/c9c03369e0000000.

### do...@chromium.org (2017-04-06)

I'm guessing that the SaveCardBubbleViews is trying to call a method on its controller_ after that controller_ has been freed.

jdonnelly, can you take a look at this please?

[Monorail components: UI>Browser>Autofill>Payments]

### sh...@chromium.org (2017-04-06)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-04-13)

[Comment Deleted]

### ch...@gmail.com (2017-04-13)

[Comment Deleted]

### ch...@gmail.com (2017-04-14)

[Comment Deleted]

### ch...@gmail.com (2017-04-18)

Attaching ASan output.

### sh...@chromium.org (2017-04-20)

jdonnelly: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2017-04-22)

WinDBG output:

rax=000000003f800062 rbx=000000001e467700 rcx=0000000018995e40
rdx=0000000020921400 rsi=0000000018e6bf40 rdi=00000000166ced40
rip=000007fee1868477 rsp=000000000019de80 rbp=000000000019df80
 r8=0000000000000000  r9=000007fedeef0000 r10=0000000020921400
r11=000000000019dea0 r12=000000000019e000 r13=0000000000000000
r14=0000000018f673c0 r15=0000000000000001
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010202
*** WARNING: Unable to verify checksum for chrome.dll
chrome_7fedeef0000!autofill::SaveCardBubbleViews::WindowClosing+0x13:
000007fe`e1868477 ff5038          call    qword ptr [rax+38h] ds:00000000`3f80009a=????????????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
Child-SP          RetAddr           Call Site
00000000`0019de80 000007fe`e135ef4c chrome_7fedeef0000!autofill::SaveCardBubbleViews::WindowClosing+0x13 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\ui\views\autofill\save_card_bubble_views.cc @ 139]
00000000`0019deb0 000007fe`e137b260 chrome_7fedeef0000!views::DesktopWindowTreeHostWin::HandleDestroying+0x44 [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc @ 766]
00000000`0019dee0 000007fe`e13786be chrome_7fedeef0000!views::HWNDMessageHandler::OnDestroy+0x5c [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.cc @ 1382]
00000000`0019df10 000007fe`e1379fa3 chrome_7fedeef0000!views::HWNDMessageHandler::_ProcessWindowMessage+0x5fa [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.h @ 400]
00000000`0019dfc0 000007fe`e035e3aa chrome_7fedeef0000!views::HWNDMessageHandler::OnWndProc+0xc7 [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.cc @ 914]
00000000`0019e060 000007fe`e035e3d3 chrome_7fedeef0000!gfx::WindowImpl::WndProc+0x92 [c:\b\build\slave\win64-pgo\build\src\ui\gfx\win\window_impl.cc @ 303]
*** WARNING: Unable to verify checksum for USER32.dll
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for USER32.dll - 
00000000`0019e0a0 00000000`772ac3c1 chrome_7fedeef0000!base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc>+0xf [c:\b\build\slave\win64-pgo\build\src\base\win\wrapped_window_proc.h @ 76]
00000000`0019e0f0 00000000`772aa01b USER32!GetSystemMetrics+0x2b1
00000000`0019e1b0 00000000`772aa061 USER32!IsDialogMessageW+0x19b
00000000`0019e210 00000000`773dfdf5 USER32!IsDialogMessageW+0x1e1
00000000`0019e270 00000000`7729f5ba ntdll!KiUserCallbackDispatcher+0x1f
00000000`0019e2f8 000007fe`e13795f9 USER32!DestroyWindow+0xa
00000000`0019e300 000007fe`df07c4be chrome_7fedeef0000!views::HWNDMessageHandler::CloseNow+0x25 [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.cc @ 444]
00000000`0019e330 000007fe`df9d014c chrome_7fedeef0000!base::internal::Invoker<base::internal::BindState<void (__cdecl gpu::CommandBufferProxyImpl::*)(void) __ptr64,base::WeakPtr<gpu::CommandBufferProxyImpl> >,void __cdecl(void)>::Run+0x4a [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0019e370 000007fe`dffc97c2 chrome_7fedeef0000!base::internal::RunMixin<base::Callback<void __cdecl(void),0,0> >::Run+0x24 [c:\b\build\slave\win64-pgo\build\src\base\callback.h @ 68]
00000000`0019e3a0 000007fe`dff75c74 chrome_7fedeef0000!base::debug::TaskAnnotator::RunTask+0x1c2 [c:\b\build\slave\win64-pgo\build\src\base\debug\task_annotator.cc @ 54]
00000000`0019e4c0 000007fe`dff768bd chrome_7fedeef0000!base::MessageLoop::RunTask+0x294 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 422]
00000000`0019f3a0 000007fe`dffc9dc1 chrome_7fedeef0000!base::MessageLoop::DoWork+0x42d [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 523]
00000000`0019f540 000007fe`dffc99f4 chrome_7fedeef0000!base::MessagePumpForUI::DoRunLoop+0x71 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_pump_win.cc @ 174]
00000000`0019f5b0 000007fe`dff9fff4 chrome_7fedeef0000!base::MessagePumpWin::Run+0x54 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_pump_win.cc @ 58]


### oc...@chromium.org (2017-05-01)

+autofill payments folks.

Could someone please take a look and/or help get it assigned to the right person?

Thanks!

### ma...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### oc...@chromium.org (2017-05-02)

rogerm, friendly ping here. We'd like to get this fixed this week if possible as part of the Security fixit (see chromium-dev email). Thanks!

### ro...@google.com (2017-05-02)

Ack.

### ro...@chromium.org (2017-05-04)

I think the controller is allowing multiple save bubbles to be instantiated and it's only keeping track of the last one. The last one gets cleaned up when the underlying page goes away, leaving all previous ones dangling.

### ro...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### ro...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### oc...@chromium.org (2017-05-04)

(Lowering severity here because of the user interaction).

### ro...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### os...@google.com (2017-05-04)

Looks like this problem predates https://codereview.chromium.org/2789843004, meaning it may have existed since the launch of Upstream in June 2016...

SaveCardBubbleViews is tied to WebContents, but the controller doesn't seem to be.  Roger's https://crbug.com/chromium/708819#c14 makes sense to me.

### bu...@chromium.org (2017-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8b457840e3512ef8c2af8d966a3edce5c653a835

commit 8b457840e3512ef8c2af8d966a3edce5c653a835
Author: rogerm <rogerm@chromium.org>
Date: Fri May 05 21:08:15 2017

[autofill] Avoid duplicate instances of the SaveCardBubble.

autofill::SaveCardBubbleControllerImpl::ShowBubble() expects
(via DCHECK) to only be called when the save card bubble is
not already visible. This constraint is violated if the user
clicks multiple times on a submit button.

If the underlying page goes away, the last SaveCardBubbleView
created by the controller will be automatically cleaned up,
but any others are left visible on the screen... holding a
refence to a possibly-deleted controller.

This CL early exits the ShowBubbleFor*** and ReshowBubble logic
if the bubble is already visible.

BUG=708819

Review-Url: https://codereview.chromium.org/2862933002
Cr-Commit-Position: refs/heads/master@{#469768}

[modify] https://crrev.com/8b457840e3512ef8c2af8d966a3edce5c653a835/chrome/browser/ui/autofill/save_card_bubble_controller_impl.cc
[modify] https://crrev.com/8b457840e3512ef8c2af8d966a3edce5c653a835/chrome/browser/ui/autofill/save_card_bubble_controller_impl_unittest.cc


### oc...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-09)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e5c96b4f08745497680d6f85f40f16ed158dc001

commit e5c96b4f08745497680d6f85f40f16ed158dc001
Author: Roger McFarlane <rogerm@chromium.org>
Date: Tue May 09 18:47:26 2017

[autofill] Avoid duplicate instances of the SaveCardBubble.

autofill::SaveCardBubbleControllerImpl::ShowBubble() expects
(via DCHECK) to only be called when the save card bubble is
not already visible. This constraint is violated if the user
clicks multiple times on a submit button.

If the underlying page goes away, the last SaveCardBubbleView
created by the controller will be automatically cleaned up,
but any others are left visible on the screen... holding a
refence to a possibly-deleted controller.

This CL early exits the ShowBubbleFor*** and ReshowBubble logic
if the bubble is already visible.

BUG=708819

Review-Url: https://codereview.chromium.org/2862933002
Cr-Commit-Position: refs/heads/master@{#469768}
(cherry picked from commit 8b457840e3512ef8c2af8d966a3edce5c653a835)

Review-Url: https://codereview.chromium.org/2870013003 .
Cr-Commit-Position: refs/branch-heads/3071@{#484}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/e5c96b4f08745497680d6f85f40f16ed158dc001/chrome/browser/ui/autofill/save_card_bubble_controller_impl.cc
[modify] https://crrev.com/e5c96b4f08745497680d6f85f40f16ed158dc001/chrome/browser/ui/autofill/save_card_bubble_controller_impl_unittest.cc


### aw...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-15)

The panel decided to award $500 for this one, thanks!

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### ro...@chromium.org (2017-06-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2017-06-19)

[Empty comment from Monorail migration]

### la...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Autofill>Payments UI>Browser>Payments]

### sh...@chromium.org (2017-08-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/708819?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/677936, crbug.com/chromium/711227]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087262)*
