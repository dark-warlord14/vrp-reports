# use-after-free in ColorChooserDialog::DidCloseDialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40077988](https://issues.chromium.org/issues/40077988) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2013-08-26 |
| **Bounty** | $1,000.00 |

## Description

Google Chrome - 29.0.1547.57 m 
Operation System - Window 7

Steps to repro :

1. Open a new tab.

2. Open PoC.html (which means we have two tabs)

3. In PoC.html page click on button color then you gonna see the page which is (PoC.html) it's gone but the color chooser it's still on the previous page (new tab), then click on Ok or Annuler button.


Stack dump :

(1368.1470): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=f95891c6 ebx=072d97d0 ecx=077cd584 edx=00007797 esi=591fcb45 edi=0018f600
eip=58160a49 esp=0018f52c ebp=0018f534 iopl=0 nv up ei pl nz na po nc
cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202
chrome_56b30000!ColorChooserDialog::DidCloseDialog+0x39:
58160a49 ff10 call dword ptr [eax] ds:0023:f95891c6=????????
0:000> k
ChildEBP RetAddr 
0018f534 58160b3a chrome_56b30000!ColorChooserDialog::DidCloseDialog+0x39 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\color_chooser_dialog.cc @ 76]
0018f54c 58160b5d chrome_56b30000!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall ColorChooserDialog::*)(bool,unsigned int,ui::BaseShellDialogImpl::RunState)>,void __cdecl(ColorChooserDialog * const &,bool const &,unsigned int const &,ui::BaseShellDialogImpl::RunState const &)>::MakeItSo+0x22 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 958]
0018f56c 56b5aa6c chrome_56b30000!base::internal::Invoker<4,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall ColorChooserDialog::*)(bool,unsigned int,ui::BaseShellDialogImpl::RunState)>,void __cdecl(ColorChooserDialog *,bool,unsigned int,ui::BaseShellDialogImpl::RunState),void __cdecl(ColorChooserDialog *,bool,unsigned int,ui::BaseShellDialogImpl::RunState)>,void __cdecl(ColorChooserDialog *,bool,unsigned int,ui::BaseShellDialogImpl::RunState)>::Run+0x21 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1568]
0018f5d8 56b5a7a9 chrome_56b30000!base::MessageLoop::RunTask+0x221 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 484]
0018f728 56e3aee3 chrome_56b30000!base::MessageLoop::DoWork+0x301 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 609]
0018f758 56b5a3e0 chrome_56b30000!base::MessagePumpForUI::DoRunLoop+0x5c [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.cc @ 243]
0018f778 56b5a34b chrome_56b30000!base::MessageLoop::RunInternal+0x5f [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 431]
0018f788 570838aa chrome_56b30000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
0018f800 57083793 chrome_56b30000!ChromeBrowserMainParts::MainMessageLoopRun+0xfa [c:\b\build\slave\win\build\src\chrome\browser\chrome_browser_main.cc @ 1637]
0018f814 5708375d chrome_56b30000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser_main_loop.cc @ 672]
0018f824 56dbe66c chrome_56b30000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser_main_runner.cc @ 114]
0018f85c 56b4be18 chrome_56b30000!content::BrowserMain+0x99 [c:\b\build\slave\win\build\src\content\browser\browser_main.cc @ 26]
0018f870 56b4bd9f chrome_56b30000!content::RunNamedProcessTypeMain+0x58 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 443]
0018f8dc 56b3a9ea chrome_56b30000!content::ContentMainRunnerImpl::Run+0x85 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 763]
0018f8ec 56b3a6dc chrome_56b30000!content::ContentMain+0x29 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 35]
0018f924 00414a87 chrome_56b30000!ChromeMain+0x1e [c:\b\build\slave\win\build\src\chrome\app\chrome_main.cc @ 28]
0018f99c 00417983 chrome!MainDllLoader::Launch+0xf5 [c:\b\build\slave\win\build\src\chrome\app\client_util.cc @ 189]
0018f9c0 00417a00 chrome!`anonymous namespace'::RunChrome+0x5e [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 49]
0018fa08 0043648d chrome!wWinMain+0x62 [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 115]
*** ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Windows\system32\kernel32.dll - 
0018fa98 7653ed6c chrome!__tmainCRTStartup+0x11a [f:\dd\vctools\crt_bld\self_x86\crt\src\crt0.c @ 275]




## Attachments

- [PoC.html](attachments/PoC.html) (text/plain; charset=us-ascii, 47 B)
- [2.PNG](attachments/2.PNG) (image/png; charset=binary, 31.3 KB)
- [1.PNG](attachments/1.PNG) (image/png; charset=binary, 10.0 KB)
- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 908 B)

## Timeline

### ts...@chromium.org (2013-08-26)

Specific to ui/views platforms (Windows). @cdn - could you help triage on windows?

### ch...@gmail.com (2013-08-27)

Actually I'm not able to repro the crash on the Linux.


### js...@chromium.org (2013-08-27)

Not reproducible.

### ch...@gmail.com (2013-08-27)

[Comment Deleted]

### ch...@gmail.com (2013-08-27)

Justin, It's working well on Windows.


### ch...@gmail.com (2013-08-27)

I think the explanation is indeed unclear.
So as you can see on screenshots in 1.PNG we have New Tab and PoC.html then when you click on color button you'll get Color Chooser and you'll see PoC.html it's gone after running of winow.close() but the color chooser it's still on than New Tab page as in 2.PNG, then click on OK button.

### js...@chromium.org (2013-08-27)

Okay, looks like it can take several tries to repo, and won't work unless you have a fresh browsing session.

The bug is that ColorChooserDialog::listener_ is a bare pointer referenced in the callback, so when it gets destroyed with the page we're left with a stale reference. It's a browser crash, but to trigger it from the web you need one gesture for the window opener (so the window.close will succeed) and another gesture to pop the color picker. You could also hit it from a compromised renderer, as a potential sandbox escape. So, seems like a high-severity.

@keishi - You originally landed this code, so maybe you can take care of the fix. The best fix might just be to make listener_ a weak pointer.

@mukai - I CC'd you since you've worked in this area recently as well.


### mu...@chromium.org (2013-08-27)

Note that chrome/browser/ui/views/color_chooser_dialog won't be used if it's win-aura.
That code is specific to non-aura Windows, and all of my work was for aura version.

The Aura color chooser doesn't suffer from this issue as far as I quickly see, because it will be closed automatically when the tab is closed.
Windows color chooser should do the same thing, or at least color_chooser_win should invoke ListenerDestroyed() in its dtor?  That's all up to keishi.

### ch...@gmail.com (2013-08-28)

Now looks like easy to repro it.

### js...@chromium.org (2013-08-28)

Thanks @mukai. @keishi can you get this taken care of this week? we'll want it merged for the next stable update.

### ch...@gmail.com (2013-08-28)

[Comment Deleted]

### ch...@gmail.com (2013-08-28)

[Comment Deleted]

### ch...@gmail.com (2013-08-28)

[Comment Deleted]

### js...@chromium.org (2013-08-29)

Khalil, please stop generating so much noise on this bug. Stack traces absent meaningful context (such as register state and the relevant instructions) are not helpful. They're just distracting and confuse anyone actually trying to work on triaging this and getting it fixed.

### js...@chromium.org (2013-08-29)

@keishi - I'm not sure if you're out or you missed this, but seeing as it can be used as a sandbox escape on Windows, we need it fixed and merged to branch as soon as possible.

### ke...@chromium.org (2013-08-29)

I've been working on it. I'll have a patch up for review in a couple of hours.

### ke...@chromium.org (2013-08-30)

I've uploaded a patch. https://codereview.chromium.org/23785003/

### ke...@chromium.org (2013-08-30)

I've landed the patch r220639.

### bu...@chromium.org (2013-08-30)

------------------------------------------------------------------------
r220639 | keishi@chromium.org | 2013-08-30T20:25:57.542228Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/color_chooser_win.cc?r1=220639&r2=220638&pathrev=220639
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/color_chooser_dialog.cc?r1=220639&r2=220638&pathrev=220639

ColorChooserWin::End should act like the dialog has closed

This is only a problem on Windows.

When the page closes itself while the color chooser dialog is open,
ColorChooserDialog::DidCloseDialog was called after the listener has been destroyed.

ColorChooserWin::End() will not actually close the color chooser dialog (because we can't) but act like it did so we can do the necessary cleanup.

BUG=279263
R=jschuh@chromium.org, pkasting@chromium.org

Review URL: https://codereview.chromium.org/23785003
------------------------------------------------------------------------

### js...@chromium.org (2013-08-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-08-30)

Thanks for taking care of it so quickly.

### in...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-13)

------------------------------------------------------------------------
r222976 | keishi@chromium.org | 2013-09-13T03:24:47.799312Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/views/color_chooser_win.cc?r1=222976&r2=222975&pathrev=222976
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/chrome/browser/ui/views/color_chooser_dialog.cc?r1=222976&r2=222975&pathrev=222976

Merge 220639 "ColorChooserWin::End should act like the dialog ha..."

> ColorChooserWin::End should act like the dialog has closed
> 
> This is only a problem on Windows.
> 
> When the page closes itself while the color chooser dialog is open,
> ColorChooserDialog::DidCloseDialog was called after the listener has been destroyed.
> 
> ColorChooserWin::End() will not actually close the color chooser dialog (because we can't) but act like it did so we can do the necessary cleanup.
> 
> BUG=279263
> R=jschuh@chromium.org, pkasting@chromium.org
> 
> Review URL: https://codereview.chromium.org/23785003

TBR=keishi@chromium.org

Review URL: https://codereview.chromium.org/24138002
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

Chromium.khalil, what name would you like us to use when we give you credit for this bug in the release notes on the Chrome blog?

### ch...@gmail.com (2013-09-26)

Please you can credit me as Khalil Zhani.

### mb...@chromium.org (2013-09-26)

Absolutely! Thanks for the quick reply.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

Thanks! $1000 reward.

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/279263?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077988)*
