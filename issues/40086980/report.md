# Security: Tab Crash is seen on closing chooser bubbles (USB/Bluetooth)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086980](https://issues.chromium.org/issues/40086980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-03-07 |
| **Bounty** | $500.00 |

## Description

Chrome Version: Chromium 59.0.3033.0 
Operating System: Windows 7

1. Visit https://permission.site
2. Click on USB/Bluetooth
3. Try to cancel the chooser bubble

Please Cc to reillyg@ who should be more aware about recent changes.

## Attachments

- [Rec.mp4](attachments/Rec.mp4) (video/mp4, 420.8 KB)
- [heap-use-after-free-on-address-0x04041b70.txt](attachments/heap-use-after-free-on-address-0x04041b70.txt) (text/plain, 11.4 KB)

## Timeline

### va...@chromium.org (2017-03-07)

I am unable to reproduce this on Windows (via Remote Desktop) or Mac using Canary. Can you please share the call stack on crash?

### ch...@gmail.com (2017-03-07)

Bad build: 59.0.3033.0 
Good build: 59.0.3032.0 

I couldn't get the call stack symbolized for now since it doesn't repro on Canary (59.0.3032.0),  so it's probably a recent change. Looks like it was last edited by reillyg@ in this commit https://chromium.googlesource.com/chromium/src/+/692db28a688889a7946b04debfd890673ae2269f

### sh...@chromium.org (2017-03-07)

Thank you for providing more feedback. Adding requester "vakh@chromium.org" to the cc list and removing "Needs-Feedback" label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2017-03-07)

[Comment Deleted]

### ch...@gmail.com (2017-03-07)

Able to repro this crash on Canary 59.0.3033.0. 

Windbg output:

rax=feeefeeefeeefeee rbx=000000000b16dc00 rcx=000000000b16dc00
rdx=0000000000000000 rsi=000000000b0ed8d0 rdi=000000000b16ddd8
rip=000007fee198b8ff rsp=00000000002fe080 rbp=00000000002fe230
 r8=0000000000008000  r9=0000000000000008 r10=0000000000000004
r11=00000000002fda58 r12=00000000002fe2b0 r13=0000000000000000
r14=000000000b0ed940 r15=0000000000000000
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
chrome_7fedfbc0000!views::DialogClientView::CancelWindow+0x3f:
000007fe`e198b8ff ff5028          call    qword ptr [rax+28h] ds:feeefeee`feeeff16=????????????????
0:000> k
Child-SP          RetAddr           Call Site
00000000`002fe080 000007fe`e198bcf5 chrome_7fedfbc0000!views::DialogClientView::CancelWindow+0x3f [c:\b\build\slave\win64-pgo\build\src\ui\views\window\dialog_client_view.cc @ 101]
00000000`002fe0b0 000007fe`e19884c3 chrome_7fedfbc0000!views::DialogClientView::ButtonPressed+0x55 [c:\b\build\slave\win64-pgo\build\src\ui\views\window\dialog_client_view.cc @ 233]
00000000`002fe0e0 000007fe`e1987bed chrome_7fedfbc0000!views::CustomButton::NotifyClick+0x63 [c:\b\build\slave\win64-pgo\build\src\ui\views\controls\button\custom_button.cc @ 487]
00000000`002fe110 000007fe`e196d6bd chrome_7fedfbc0000!views::CustomButton::OnMouseReleased+0x9d [c:\b\build\slave\win64-pgo\build\src\ui\views\controls\button\custom_button.cc @ 214]
00000000`002fe140 000007fe`e0d3639f chrome_7fedfbc0000!views::View::OnMouseEvent+0x14d [c:\b\build\slave\win64-pgo\build\src\ui\views\view.cc @ 1118]
00000000`002fe170 000007fe`e0d36ac0 chrome_7fedfbc0000!ui::EventHandler::OnEvent+0x12f [c:\b\build\slave\win64-pgo\build\src\ui\events\event_handler.cc @ 36]
00000000`002fe1a0 000007fe`e0d365cb chrome_7fedfbc0000!ui::EventDispatcher::DispatchEvent+0x58 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 192]
00000000`002fe1d0 000007fe`e0d36445 chrome_7fedfbc0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x123 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 86]
00000000`002fe270 000007fe`e19a135e chrome_7fedfbc0000!ui::EventDispatcherDelegate::DispatchEvent+0x61 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 58]
00000000`002fe2b0 000007fe`e19669ec chrome_7fedfbc0000!views::internal::RootView::OnMouseReleased+0x7e [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\root_view.cc @ 442]
00000000`002fe640 000007fe`e0d3639f chrome_7fedfbc0000!views::Widget::OnMouseEvent+0xec [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\widget.cc @ 1226]
00000000`002fe680 000007fe`e0d36ac0 chrome_7fedfbc0000!ui::EventHandler::OnEvent+0x12f [c:\b\build\slave\win64-pgo\build\src\ui\events\event_handler.cc @ 36]
00000000`002fe6b0 000007fe`e0d365cb chrome_7fedfbc0000!ui::EventDispatcher::DispatchEvent+0x58 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 192]
00000000`002fe6e0 000007fe`e0d36445 chrome_7fedfbc0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x123 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 86]
00000000`002fe780 000007fe`e1a6326b chrome_7fedfbc0000!ui::EventDispatcherDelegate::DispatchEvent+0x61 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_dispatcher.cc @ 58]
00000000`002fe7c0 000007fe`e1a63448 chrome_7fedfbc0000!ui::EventProcessor::OnEventFromSource+0xfb [c:\b\build\slave\win64-pgo\build\src\ui\events\event_processor.cc @ 46]
00000000`002fe820 000007fe`e19aafdd chrome_7fedfbc0000!ui::EventSource::SendEventToProcessor+0xa0 [c:\b\build\slave\win64-pgo\build\src\ui\events\event_source.cc @ 52]
00000000`002fe890 000007fe`e19ca1f5 chrome_7fedfbc0000!views::DesktopWindowTreeHostWin::HandleMouseEvent+0x1d [c:\b\build\slave\win64-pgo\build\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc @ 835]
00000000`002fe8c0 000007fe`e19c4938 chrome_7fedfbc0000!views::HWNDMessageHandler::HandleMouseEventInternal+0x38d [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.cc @ 2549]
00000000`002ff070 000007fe`e19c67a4 chrome_7fedfbc0000!views::HWNDMessageHandler::_ProcessWindowMessage+0xa0 [c:\b\build\slave\win64-pgo\build\src\ui\views\win\hwnd_message_handler.h @ 335]


### ch...@gmail.com (2017-03-07)

Also able to repro this under ASan windows build, this looks like a heap-use-after-free vulnerability.

### re...@chromium.org (2017-03-07)

I'm reverting my last patch.

### bu...@chromium.org (2017-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5e296353d65aef23ed1b524a4c1b01e568f6c3cd

commit 5e296353d65aef23ed1b524a4c1b01e568f6c3cd
Author: reillyg <reillyg@chromium.org>
Date: Tue Mar 07 16:06:21 2017

Revert of Force chooser bubbles to close synchronously. (patchset #3 id:40001 of https://codereview.chromium.org/2724903008/ )

Reason for revert:
Reverting this patchset because it was insufficiently tested and introduced a new bug.

Original issue's description:
> Force chooser bubbles to close synchronously.
>
> This fixes a potential use-after-free because UsbChooserController holds
> a raw pointer to the RenderFrameHost and so must be destroyed as part of
> RenderFrameHost destruction.
>
> BUG=697486
>
> Review-Url: https://codereview.chromium.org/2724903008
> Cr-Commit-Position: refs/heads/master@{#454989}
> Committed: https://chromium.googlesource.com/chromium/src/+/692db28a688889a7946b04debfd890673ae2269f

TBR=msw@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=697486,698927

Review-Url: https://codereview.chromium.org/2736793003
Cr-Commit-Position: refs/heads/master@{#455086}

[modify] https://crrev.com/5e296353d65aef23ed1b524a4c1b01e568f6c3cd/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.cc
[modify] https://crrev.com/5e296353d65aef23ed1b524a4c1b01e568f6c3cd/chrome/browser/ui/views/website_settings/chooser_bubble_ui_view.h


### re...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### lg...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Permissions>Prompts]

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-15)

Nice one! The panel decided to award $500 for this report, noting that we weren't able to reproduce ourselves.  Many thanks as ever!

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/698927?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086980)*
