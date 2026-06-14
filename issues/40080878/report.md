# Security: Heap-use-after-free in SupportsUserData::GetUserData

| Field | Value |
|-------|-------|
| **Issue ID** | [40080878](https://issues.chromium.org/issues/40080878) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2014-11-19 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: stable 39.0.2171.65 m  

Operating System: Win7

**VULNERABILITY DETAILS**

1. Open PoC.html
2. Click on the button to open google.com link in new tab and click on the padlock on the URL bar as in "1.png" then after 3000s the page "google.com" will be closed as in 2.png
3. click on "Show cookies and site data" link

eax=0c9bbc80 ebx=0c9bbc84 ecx=10016008 edx=550de502 esi=5ed2ab40 edi=550de502  

eip=5d092455 esp=0025eb08 ebp=0025eb1c iopl=0 nv up ei pl nz na po nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00210202  

chrome\_5cfb0000!base::SupportsUserData::GetUserData+0x1b:  

5d092455 8b4704 mov eax,dword ptr [edi+4] ds:0023:550de506=????????  

0:000> k  

ChildEBP RetAddr  

0025eb1c 5d22ada9 chrome\_5cfb0000!base::SupportsUserData::GetUserData+0x1b [c:\b\build\slave\win\build\src\base\supports\_user\_data.cc @ 16]  

0025eb30 5dc3e187 chrome\_5cfb0000!content::WebContentsUserData<TabSpecificContentSettings>::FromWebContents+0x1a [c:\b\build\slave\win\build\src\content\public\browser\web\_contents\_user\_data.h @ 46]  

0025eb4c 5dc52592 chrome\_5cfb0000!CollectedCookiesViews::CollectedCookiesViews+0xf3 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\collected\_cookies\_views.cc @ 197]  

0025ed60 5e13e8a2 chrome\_5cfb0000!WebsiteSettingsPopupView::LinkClicked+0x53 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\website\_settings\website\_settings\_popup\_view.cc @ 396]  

0025ed80 5e13589b chrome\_5cfb0000!views::Link::OnMouseReleased+0x72 [c:\b\build\slave\win\build\src\ui\views\controls\link.cc @ 86]  

0025ed9c 5d481915 chrome\_5cfb0000!views::View::ProcessMouseReleased+0x6f [c:\b\build\slave\win\build\src\ui\views\view.cc @ 2299]  

0025edb0 5d283aed chrome\_5cfb0000!views::View::OnMouseEvent+0x8e [c:\b\build\slave\win\build\src\ui\views\view.cc @ 988]  

0025edc4 5d284b03 chrome\_5cfb0000!ui::EventHandler::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_handler.cc @ 29]  

0025eddc 5d283a7e chrome\_5cfb0000!ui::EventTarget::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_target.cc @ 64]  

0025edf4 5d28388a chrome\_5cfb0000!ui::EventDispatcher::DispatchEvent+0x3d [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 190]  

0025ee10 5d28378a chrome\_5cfb0000!ui::EventDispatcher::ProcessEvent+0x86 [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 138]  

0025ee44 5d282dd0 chrome\_5cfb0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x2a [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 86]  

0025ee6c 5e152376 chrome\_5cfb0000!ui::EventDispatcherDelegate::DispatchEvent+0x5b [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 57]  

0025f044 5d481006 chrome\_5cfb0000!views::internal::RootView::OnMouseReleased+0x8a [c:\b\build\slave\win\build\src\ui\views\widget\root\_view.cc @ 456]  

0025f074 5e13bed4 chrome\_5cfb0000!views::Widget::OnMouseEvent+0xc3 [c:\b\build\slave\win\build\src\ui\views\widget\widget.cc @ 1233]  

0025f088 5d283aed chrome\_5cfb0000!views::DesktopNativeWidgetAura::OnMouseEvent+0x31 [c:\b\build\slave\win\build\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc @ 1043]  

0025f09c 5d284afa chrome\_5cfb0000!ui::EventHandler::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_handler.cc @ 29]  

0025f0b4 5d283a7e chrome\_5cfb0000!ui::EventTarget::OnEvent+0x29 [c:\b\build\slave\win\build\src\ui\events\event\_target.cc @ 63]  

0025f0cc 5d28388a chrome\_5cfb0000!ui::EventDispatcher::DispatchEvent+0x3d [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 190]  

0025f0e8 5d28378a chrome\_5cfb0000!ui::EventDispatcher::ProcessEvent+0x86 [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 138]

## Attachments

- deleted (application/octet-stream, 0 B)
- [2.png](attachments/2.png) (image/png, 67.2 KB)
- [1.png](attachments/1.png) (image/png, 84.6 KB)
- [PoC.html](attachments/PoC.html) (text/html, 170 B)
- [Screen Shot 2014-11-19 at 11.24.13.png](attachments/Screen Shot 2014-11-19 at 11.24.13.png) (image/png, 159.9 KB)

## Timeline

### ch...@gmail.com (2014-11-19)

[Empty comment from Monorail migration]

### lg...@chromium.org (2014-11-19)

Can't reproduce in Chrome Canary on OSX.
I won't be able to try on Windows until tomorrow.

### ke...@chromium.org (2014-11-19)

I can reproduce.

Crash ID: 3f8d9bbeb453f8e0

Not a UAF when I tried it, but a null pointer crash with the same stack, and a UAF looks plausible given what appears to be happening.

avi@: Do you have time to investigate this, or else do you know anyone who would be good to look?

### ch...@gmail.com (2014-11-19)

Yes, sometimes it hits a null pointer.

### av...@chromium.org (2014-11-19)

CollectedCookiesViews::CollectedCookiesViews is calling TabSpecificContentSettings::FromWebContents() on a NULL WebContents. 

### av...@chromium.org (2014-11-19)

The OP makes it clear that at the end of step 2 you have to wait for the google.com tab to close. I understand the repro as:

1. Load PoC.html (from https://crbug.com/chromium/434569#c1).
2. Click the "here" button. This will open google.com in a new tab.
3. In that new tab, click the padlock button. This will open a bubble with security info for google.com.
4. After 3s, the google.com tab will close.
>> The OP's "step 3" implies that the security info bubble remains open after the google.com tab closes, as the OP's "step 3" instructs to click on the "Show cookies and site data" link.
5. The security info bubble remains open; click on a link to crash.

It is very clear that this is the OP's repro; their second image shows the google.com security info bubble open after the google.com tab is gone.

I cannot reproduce this. I am running Version 39.0.2171.65 m, but in step 4, when the google.com tab closes, the security info bubble goes away.

kenrb@, can you share your secrets? How are you reproducing this?

### ch...@gmail.com (2014-11-19)

I didn't try this crash before on another OS to see if that the security info bubble goes away or not except on Windows.

### av...@chromium.org (2014-11-19)

Khalil, that's fine.

My questions for you are:
- Is my restatement of your repro accurate? In particular, is it true that when the google.com tab disappears, the security info bubble stays open?
- Can you clarify how you're doing it? I'm using the same version of Chrome and I can't make it happen; on my Chrome, the security info bubble closes when the google.com tab closes. What's going on for you that isn't going on for me?

### ch...@gmail.com (2014-11-19)

[Comment Deleted]

### ch...@gmail.com (2014-11-19)

- Absolutely yes, the security info bubble stays open.
I've uploaded this video http://youtu.be/xHpJjRPzma0 to see how I repro this crash.

### av...@chromium.org (2014-11-19)

+cpu, beng

### av...@chromium.org (2014-11-19)

Can anyone else (other than the original poster) repro? Please make sure that you're reproducing according to the instructions in https://crbug.com/chromium/434569#c6: the security info bubble must stay open even though the google.com tab closes. Make sure it matches up with the video provided in https://crbug.com/chromium/434569#c10.

kenrb@ in particular, can you provide more info on your reproduction?

### av...@chromium.org (2014-11-19)

I can repro this on my Pixel with 40.0.2194.3 dev channel. This is a Views issue.

### av...@chromium.org (2014-11-20)

Peter, you know Views more than I do. This is very reproducible for me on a Pixel, and not at all on Windows, but the OP can repro on Windows.

The problem is that if a tab is closed via JavaScript, the security info bubble isn't closing (which is spoof-ish maybe?) but also there's a UaF when people start clicking random stuff in there that refers to long-gone objects.

### av...@chromium.org (2014-11-20)

Gah, wrong Peter.

### pk...@chromium.org (2014-11-20)

Markus, blame suggests that the website_settings_popup_view.cc code is mostly yours?  See https://crbug.com/chromium/434569#c14.

I worry that this might apply to the star bubble as well.  Offhand I didn't see anything to close that when the active tab changes.

### ch...@gmail.com (2014-12-08)

[Comment Deleted]

### ch...@gmail.com (2015-01-27)

==4876==ERROR: AddressSanitizer: heap-use-after-free on address 0x0d1d988c at pc 0x514247ff bp 0xdeadbeef sp 0x002ba9b8
READ of size 4 at 0x0d1d988c thread T0
    #0 0x514247fe in base::SupportsUserData::GetUserData C:\b\depot_tools\win_toolchain\vs2013_files\VC\include\xtree:2153
    #1 0x5b4d20fe in CollectedCookiesViews::CollectedCookiesViews C:\b\build\slave\Win_ASan_Release\build\src\content\public\browser\web_contents_user_data.h:46
    #2 0x551627c3 in WebsiteSettingsPopupView::LinkClicked C:\b\build\slave\Win_ASan_Release\build\src\chrome\browser\ui\views\website_settings\website_settings_popup_vi
ew.cc:396
    #3 0x5918792c in views::Link::OnMouseReleased C:\b\build\slave\Win_ASan_Release\build\src\ui\views\controls\link.cc:86
    #4 0x5911782b in views::View::ProcessMouseReleased C:\b\build\slave\Win_ASan_Release\build\src\ui\views\view.cc:2306
    #5 0x59116512 in views::View::OnMouseEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\views\view.cc:984
    #6 0x5999da37 in ui::EventHandler::OnEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_handler.cc:37
    #7 0x5999af14 in ui::EventTarget::OnEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_target.cc:64
    #8 0x599ab353 in ui::EventDispatcher::ProcessEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:189
    #9 0x599aac43 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:85
    #10 0x599aa6df in ui::EventDispatcherDelegate::DispatchEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:57
    #11 0x592c615b in views::internal::RootView::OnMouseReleased C:\b\build\slave\Win_ASan_Release\build\src\ui\views\widget\root_view.cc:444
    #12 0x59168b48 in views::Widget::OnMouseEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\views\widget\widget.cc:1239
    #13 0x59182803 in views::DesktopNativeWidgetAura::OnMouseEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc
:1063
    #14 0x5999da37 in ui::EventHandler::OnEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_handler.cc:37
    #15 0x5999af05 in ui::EventTarget::OnEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_target.cc:62
    #16 0x599ab353 in ui::EventDispatcher::ProcessEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:189
    #17 0x599aac43 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:85
    #18 0x599aa6df in ui::EventDispatcherDelegate::DispatchEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_dispatcher.cc:57
    #19 0x599bad9b in ui::EventProcessor::OnEventFromSource C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_processor.cc:35
    #20 0x599bf32e in ui::EventSource::SendEventToProcessor C:\b\build\slave\Win_ASan_Release\build\src\ui\events\event_source.cc:73
    #21 0x592e874f in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\build\slave\Win_ASan_Release\build\src\ui\views\widget\desktop_aura\desktop_window_tree_host
_win.cc:836
    #22 0x593499e9 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\build\slave\Win_ASan_Release\build\src\ui\views\win\hwnd_message_handler.cc:2782
    #23 0x593422b9 in views::HWNDMessageHandler::_ProcessWindowMessage C:\b\build\slave\Win_ASan_Release\build\src\ui\views\win\hwnd_message_handler.cc:1762
    #24 0x593413bc in views::HWNDMessageHandler::OnWndProc C:\b\build\slave\Win_ASan_Release\build\src\ui\views\win\hwnd_message_handler.cc:955
    #25 0x5ceda16f in gfx::WindowImpl::WndProc c:\b\build\slave\win_asan_release\build\src\ui\gfx\win\window_impl.cc:314
    #26 0x77b386ee in IsThreadDesktopComposited+0x11e (C:\Windows\system32\USER32.dll+0x186ee)
    #27 0x77b38875 in IsThreadDesktopComposited+0x2a5 (C:\Windows\system32\USER32.dll+0x18875)
    #28 0x77b389b4 in IsThreadDesktopComposited+0x3e4 (C:\Windows\system32\USER32.dll+0x189b4)
    #29 0x77b38e9b in DispatchMessageW+0xe (C:\Windows\system32\USER32.dll+0x18e9b)


SUMMARY: AddressSanitizer: heap-use-after-free C:\b\depot_tools\win_toolchain\vs2013_files\VC\include\xtree:2153 base::SupportsUserData::GetUserData
Shadow bytes around the buggy address:
  0x31a3b2c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x31a3b2d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x31a3b2e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x31a3b2f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x31a3b300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x31a3b310: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x31a3b320: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x31a3b330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x31a3b340: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x31a3b350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x31a3b360: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==4876==ABORTING

### ch...@gmail.com (2015-01-30)

[Comment Deleted]

### ch...@gmail.com (2015-01-30)

Is there anybody else can takes a look at this?


### ch...@gmail.com (2015-02-23)

[Comment Deleted]

### ch...@gmail.com (2015-02-23)

Markus, Any updates on this bug?

### jo...@chromium.org (2015-03-05)

Any updates on this?

### ch...@gmail.com (2015-03-06)

Markus, Could you please take a look at this or find someone else to own it?

### ch...@gmail.com (2015-03-11)

Can someone else takes a look at this bug?

### wf...@chromium.org (2015-03-17)

I spoke to markusheintz and he will provide an update on this bug.

### ma...@chromium.org (2015-03-17)

Sorry about the delay. Somehow this did not appear on my radar.

I can't reproduce this on tot build. The dialog is automatically closed when the tab is closed.

I created a CL that prevents the Collected Cookies dialog from opening if the web_contents is null
https://codereview.chromium.org/1017683003/

### ma...@chromium.org (2015-03-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-03-30)

I think the fix is done in https://codereview.chromium.org/1017683003/ it should be closed.

### in...@chromium.org (2015-03-30)

Fix is not committed yet. markusheintz@, can you please commit and close this.

### ch...@gmail.com (2015-05-11)

markusheintz@ Could you please commit https://codereview.chromium.org/1017683003/

### bu...@chromium.org (2015-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/56de5c361e59b039c7347441da6fb5f5b8ee32ee

commit 56de5c361e59b039c7347441da6fb5f5b8ee32ee
Author: markusheintz <markusheintz@chromium.org>
Date: Thu May 14 23:11:36 2015

Don't open the Collected Cookies dialog if the related web contents is null because the tab was already closed.

BUG=434569

Review URL: https://codereview.chromium.org/1017683003

Cr-Commit-Position: refs/heads/master@{#329969}

[modify] http://crrev.com/56de5c361e59b039c7347441da6fb5f5b8ee32ee/chrome/browser/ui/views/website_settings/website_settings_popup_view.cc


### in...@chromium.org (2015-05-14)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

This may roll in with M44 unless we get an additional M43 and some decent bake time (note to future me: this is already in M44).

### ti...@google.com (2015-06-12)

Congrats - $500 for this report. 

We'll start payment via our new process (should take 1-2 weeks) from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

We'll process this reward via our new payment process which should only take ~1-2 weeks.  

### pa...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-21)

Bulk update: removing view restriction from closed bugs.

### pa...@chromium.org (2015-08-24)

[Empty comment from Monorail migration]

### kr...@chromium.org (2015-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/434569?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080878)*
