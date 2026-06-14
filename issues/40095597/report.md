# Security: Memory corruption in BrowserList::NotifyBrowserNoLongerActive(Browser*) ()

| Field | Value |
|-------|-------|
| **Issue ID** | [40095597](https://issues.chromium.org/issues/40095597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-07-03 |
| **Bounty** | $500.00 |

## Description

Chrome Version: Chromium 77.0.3843.0 (Developer Build) (64-bit)  

Operating System: All

**REPRODUCTION CASE**

1. Open <http://permission.site>
2. Open again on another tab <http://permission.site>
3. On the first tab, click on “Share screen” and switch Chrome Tab and try to share the second tab of <http://permission.site>
4. On the second tab, click on “Share screen” and switch Chrome Tab and try to share the first tab of <http://permission.site>
5. Close the first tab >> crash

(gdb) x/1i $rip  

=> 0x55555c7585df <\_ZN11BrowserList27NotifyBrowserNoLongerActiveEP7Browser+447>: callq \*0x20(%rax)  

(gdb) i r  

rax 0x7fff00000000 140733193388032  

rbx 0x2e47de079bc0 50886202596288  

rcx 0x2e47de079b00 50886202596096  

rdx 0x18 24  

rsi 0x2e47ddcee8c0 50886198880448  

rdi 0x2e47de2849b0 50886204737968  

rbp 0x7fffffffcf40 0x7fffffffcf40  

rsp 0x7fffffffcf00 0x7fffffffcf00  

r8 0x1 1  

r9 0x0 0  

r10 0x7fffffffc7f0 140737488340976  

r11 0x31a7884d23bda 873529856900058  

r12 0x0 0  

r13 0x2e47ddc8fe00 50886198492672  

r14 0x2e47ddcee8c0 50886198880448  

r15 0x0 0  

rip 0x55555c7585df 0x55555c7585df [BrowserList::NotifyBrowserNoLongerActive(Browser\\*)+447](javascript:void(0);)  

eflags 0x10293 [ CF AF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) tb  

Temporary breakpoint 1 at 0x55555c7585df  

(gdb) bt  

#0 0x000055555c7585df in BrowserList::NotifyBrowserNoLongerActive(Browser\*) ()  

#1 0x000055555c8c5a55 in BrowserView::OnWidgetActivationChanged(views::Widget\*, bool) ()  

#2 0x000055555bd7ddbe in views::Widget::OnNativeWidgetActivationChanged(bool) ()  

#3 0x000055555bdad350 in views::DesktopNativeWidgetAura::HandleActivationChanged(bool) ()  

#4 0x000055555bda3bf5 in views::DesktopWindowTreeHostX11::AfterActivationStateChanged() ()  

#5 0x000055555bdaac41 in views::DesktopWindowTreeHostX11::DispatchEvent(\_XEvent\* const&) ()  

#6 0x000055555bdab2e0 in non-virtual thunk to views::DesktopWindowTreeHostX11::DispatchEvent(\_XEvent\* const&) ()  

#7 0x000055555ad8d705 in ui::PlatformEventSource::DispatchEvent(\_XEvent\*) ()  

#8 0x000055555ae5432f in ui::X11EventSource::DispatchXEvents() ()  

#9 0x000055555b5eb13c in ui::(anonymous namespace)::XSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ()  

#10 0x00007ffff5aee04a in g\_main\_context\_dispatch () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#11 0x00007ffff5aee3f0 in ?? () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#12 0x00007ffff5aee49c in g\_main\_context\_iteration () from /lib/x86\_64-linux-gnu/libglib-2.0.so.0  

#13 0x000055555a3e5542 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ()  

#14 0x000055555a427e49 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ()  

#15 0x000055555a400b67 in base::RunLoop::RunWithTimeout(base::TimeDelta) ()  

#16 0x000055555a060ec7 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) ()  

#17 0x0000555558981c8b in content::BrowserMainLoop::RunMainMessageLoopParts() ()  

#18 0x0000555558983a42 in content::BrowserMainRunnerImpl::Run() ()  

#19 0x000055555897eccf in content::BrowserMain(content::MainFunctionParams const&) ()  

#20 0x0000555559ff5e47 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ()  

#21 0x0000555559ff5b16 in content::ContentMainRunnerImpl::Run(bool) ()  

#22 0x000055555a04183d in service\_manager::Main(service\_manager::MainParams const&) ()  

#23 0x0000555559ff3e21 in content::ContentMain(content::ContentMainParams const&) ()  

#24 0x0000555557e631bf in ChromeMain ()  

#25 0x00007ffff184f830 in \_\_libc\_start\_main (main=0x555557e63130 <main>, argc=1, argv=0x7fffffffddc8, init=<optimized out>, fini=<optimized out>,  

rtld\_fini=<optimized out>, stack\_end=0x7fffffffddb8) at ../csu/libc-start.c:291

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.3 MB)

## Timeline

### ch...@gmail.com (2019-07-04)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-07-04)

Another screen share related bug, marinaciocea would you be able to help take a look? Thanks!

[Monorail components: Blink>GetUserMedia>Tab]

### sh...@chromium.org (2019-07-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cd7e21456fcf4fec0783a97be651f36bd2a3435b

commit cd7e21456fcf4fec0783a97be651f36bd2a3435b
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Mon Jul 08 15:57:46 2019

Fix tab sharing UI crash on multiple sharing sessions.

When starting multiple sharing sessions, don't override infobars associated with
other UIs. Instead, create infobars on all tabs for each sharing session. This
makes it possible to have multiple sharing sessions at the same time, as it was
the case with previous UI.

This also changes how tab dragging is implemented: don't override pre-existing
infobars, instead don't re-create infobars if they already exist on a tab in
the UI associated with a sharing sessions;  multiple infobars can exist on the
same tab if they correspond to different tab sharing UIs.

Bug: 976286, 981202, 981826
Change-Id: I81de59b3487d40b3769b684cb90c496df2653d93
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1690948
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#675231}

[modify] https://crrev.com/cd7e21456fcf4fec0783a97be651f36bd2a3435b/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate.cc
[modify] https://crrev.com/cd7e21456fcf4fec0783a97be651f36bd2a3435b/chrome/browser/ui/tab_sharing/tab_sharing_ui.cc
[modify] https://crrev.com/cd7e21456fcf4fec0783a97be651f36bd2a3435b/chrome/browser/ui/tab_sharing/tab_sharing_ui.h


### ma...@chromium.org (2019-07-09)

Fixed by change in https://crbug.com/chromium/981202#c4.

### sh...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2020-11-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>GetUserMedia]

### be...@google.com (2020-11-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink>GetUserMedia>Tab]

### is...@google.com (2020-11-05)

This issue was migrated from crbug.com/chromium/981202?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095597)*
