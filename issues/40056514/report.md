# Security: UaF in TabGroupEditorBubbleView::UpdateGroup()

| Field | Value |
|-------|-------|
| **Issue ID** | [40056514](https://issues.chromium.org/issues/40056514) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2021-07-13 |
| **Bounty** | $10,000.00 |

## Description

**VERSION**  

Chrome Version: 93.0.4573.0 (Official Build) canary (x86\_64) and stable  

Operating System: Windows and Linux

**REPRODUCTION CASE**

Similar to <https://crbug.com/chromium/1184954>.

enable #top-chrome-touch-ui

1. Install the extension.
2. At the top of chrome, click on the colored dot and wait 2 seconds than try to choose any color

Received signal 11 <unknown> 03e800001099  

#0 0x55d5a3fa36d9 base::debug::CollectStackTrace()  

#1 0x55d5a3f0e6f3 base::debug::StackTrace::StackTrace()  

#2 0x55d5a3fa3201 base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#3 0x7f21dbef03c0 (/usr/lib/x86\_64-linux-gnu/libpthread-2.31.so+0x153bf)  

#4 0x55d5a720c936 TabGroupEditorBubbleView::UpdateGroup()  

#5 0x55d5a6afebad base::internal::Invoker<>::Run()  

#6 0x55d5a6afb121 views::Button::DefaultButtonControllerDelegate::NotifyClick()  

#7 0x55d5a6aff784 views::ButtonController::OnMouseReleased()  

#8 0x55d5a4dc9e14 ui::EventHandler::OnEvent()  

#9 0x55d5a6af601f ui::ScopedTargetHandler::OnEvent()  

#10 0x55d5a4dc981b ui::EventDispatcher::ProcessEvent()  

#11 0x55d5a4dc9652 ui::EventDispatcherDelegate::DispatchEventToTarget()  

#12 0x55d5a4dc95b2 ui::EventDispatcherDelegate::DispatchEvent()  

#13 0x55d5a6b773a5 views::internal::RootView::OnMouseReleased()  

#14 0x55d5a6b7f61d views::Widget::OnMouseEvent()  

#15 0x55d5a4dc9e14 ui::EventHandler::OnEvent()  

#16 0x55d5a4dc981b ui::EventDispatcher::ProcessEvent()  

#17 0x55d5a4dc9652 ui::EventDispatcherDelegate::DispatchEventToTarget()  

#18 0x55d5a4dc95b2 ui::EventDispatcherDelegate::DispatchEvent()  

#19 0x55d5a5a185cf ui::EventProcessor::OnEventFromSource()  

#20 0x55d5a5a21186 ui::EventSource::DeliverEventToSink()  

#21 0x55d5a5a2109e ui::EventSource::SendEventToSinkFromRewriter()  

#22 0x55d5a6bb6afb aura::WindowTreeHostPlatform::DispatchEvent()  

#23 0x55d5a6bb53b0 views::DesktopWindowTreeHostLinux::DispatchEvent()  

#24 0x55d5a53792b0 ui::X11Window::DispatchUiEvent()  

#25 0x55d5a5378fe4 ui::X11Window::DispatchEvent()  

#26 0x55d5a53792ed ui::X11Window::DispatchEvent()  

#27 0x55d5a4cdf9c9 ui::PlatformEventSource::DispatchEvent()  

#28 0x55d5a4e2b2f3 ui::X11EventSource::OnEvent()  

#29 0x55d5a12f0672 x11::Connection::DispatchEvent()  

#30 0x55d5a12f045b x11::Connection::ProcessNextEvent()  

#31 0x55d5a12f01ef x11::Connection::Dispatch()  

#32 0x55d5a4e2edc2 ui::(anonymous namespace)::XSourceDispatch()  

#33 0x7f21dbda404e g\_main\_context\_dispatch  

#34 0x7f21dbda4400 (/usr/lib/x86\_64-linux-gnu/libglib-2.0.so.0.6400.6+0x523ff)  

#35 0x7f21dbda44a3 g\_main\_context\_iteration  

#36 0x55d5a3f28523 base::MessagePumpGlib::Run()  

#37 0x55d5a3f78655 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run()  

#38 0x55d5a3f497db base::RunLoop::Run()  

#39 0x55d5a1ffbb43 content::BrowserMainLoop::RunMainMessageLoop()  

#40 0x55d5a1ffd422 content::BrowserMainRunnerImpl::Run()  

#41 0x55d5a1ff942b content::BrowserMain()  

#42 0x55d5a3eaab1a content::ContentMainRunnerImpl::RunBrowser()  

#43 0x55d5a3eaa68d content::ContentMainRunnerImpl::Run()  

#44 0x55d5a3ea7e6b content::RunContentProcess()  

#45 0x55d5a3ea876d content::ContentMain()  

#46 0x55d5a0d74251 ChromeMain  

#47 0x7f21dae210b3 \_\_libc\_start\_main  

#48 0x55d5a0d7406a \_start  

r8: 0000000100000000 r9: 000030d803567740 r10: 0000000000000037 r11: 000000007fffffff  

r12: 000030d8026b6000 r13: 000030d8030dda00 r14: deadbeefdeadbeef r15: 000030d803512300  

di: 000030d802c31660 si: 000030d8026b6598 bp: 00007ffe3cfecb30 bx: 0000000500000001  

dx: 9f67a8d28663f811 ax: deadbeefdeadbeef cx: 496bb19186cf0203 sp: 00007ffe3cfecab0  

ip: 000055d5a720c936 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000000  

trp: 000000000000000d msk: 0000000000000000 cr2: 0000000000000000  

[end of stack trace]  

Segmentation fault (core dumped)

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 791.9 KB)
- [background.js](attachments/background.js) (text/plain, 336 B)
- [manifest.json](attachments/manifest.json) (text/plain, 389 B)

## Timeline

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-14)

This looks like trunk churn, as I can't reproduce it on ToT. Out of an abundance of caution, I'll forward it along so that someone closer to the code can take a look.

tbergquist@ / solomonkinard@: was this crash and subsequent lack of repro expected? If this is just churn, feel free to WontFix this bug.

[Monorail components: Platform>Extensions>API UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-07-21)

This is in the webui tabstrip, which I don't have much/any involvement with.

That said, the desktop tabstrip would I believe dismiss the dialog when the extension does its operations in this case, and the webui tabstrip should probably do something similar.

Connie, do you know who to hand this off to for tab groups x webui tabstrip?

### co...@chromium.org (2021-07-26)

Thanks for taking a look Taylor! Passing to John for the WebUI tabstrip+group bubble, CCIng Tom for WebUI tabstrip in general

### [Deleted User] (2021-07-27)

johntlee: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aff1dce7943a6b6969821dfd9ea6456a833f034b

commit aff1dce7943a6b6969821dfd9ea6456a833f034b
Author: John Lee <johntlee@chromium.org>
Date: Wed Aug 04 20:25:53 2021

WebUI Tab Strip: Close edit dialog for groups when group is removed

Bug: 1228557
Change-Id: Ibe6a0cf0ea0449d5d6c6e5d7b58828932dac7ac5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057297
Commit-Queue: John Lee <johntlee@chromium.org>
Reviewed-by: Charlene Yan <cyan@chromium.org>
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#908595}

[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/views/frame/webui_tab_strip_container_view.h
[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_browsertest.cc
[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_embedder.h
[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler.cc
[modify] https://crrev.com/aff1dce7943a6b6969821dfd9ea6456a833f034b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler_unittest.cc


### ch...@gmail.com (2021-08-04)

Verified on Chromium 94.0.4598.0 refs/heads/master@{#908635}. Fixed.

### jo...@chromium.org (2021-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations, Khalil - The VRP Panel has decided to award you $10,000 for this report. Thank you for reporting this issue! 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### co...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a5f9c80b3c4925df00f51b1397ec74c50569fd0b

commit a5f9c80b3c4925df00f51b1397ec74c50569fd0b
Author: John Lee <johntlee@chromium.org>
Date: Wed Sep 29 09:27:00 2021

[M90-LTS] WebUI Tab Strip: Close edit dialog for groups when group is removed

M90 merge issues:
  WebUITabStripContainerView doesn't inherit from WebContentsObserver.
  Removed it and kept the addition of WidgetObserver from the original change.

(cherry picked from commit aff1dce7943a6b6969821dfd9ea6456a833f034b)

Bug: 1228557
Change-Id: Ibe6a0cf0ea0449d5d6c6e5d7b58828932dac7ac5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057297
Commit-Queue: John Lee <johntlee@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#908595}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3182300
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1626}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_browsertest.cc
[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler.cc
[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/views/frame/webui_tab_strip_container_view.cc
[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/views/frame/webui_tab_strip_container_view.h
[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_embedder.h
[modify] https://crrev.com/a5f9c80b3c4925df00f51b1397ec74c50569fd0b/chrome/browser/ui/webui/tab_strip/tab_strip_ui_handler_unittest.cc


### rz...@google.com (2021-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1228557?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>TopChrome>TabStrip>TabGroups]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056514)*
