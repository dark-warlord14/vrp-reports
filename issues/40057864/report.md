# Security: Heap-use-after-free in ui::EventDispatcher::DispatchEventToEventHandlers()

| Field | Value |
|-------|-------|
| **Issue ID** | [40057864](https://issues.chromium.org/issues/40057864) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-11-09 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 98.0.4696.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: All

**REPRODUCTION CASE**

This is similar to <https://crbug.com/chromium/1244348> (same stack trace).

1. Enable #sharing-desktop-screenshots
2. Open any page
3. Start to screenshot it two times

Received signal 11 <unknown> 03e8000011cf  

#0 0x55fe91896af9 base::debug::CollectStackTrace()  

#1 0x55fe917fdfe3 base::debug::StackTrace::StackTrace()  

#2 0x55fe918965d1 base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#3 0x7fa92202b3c0 (/usr/lib/x86\_64-linux-gnu/libpthread-2.31.so+0x153bf)  

#4 0x55fe922c5e80 ui::EventDispatcher::DispatchEventToEventHandlers()  

#5 0x55fe922c5b86 ui::EventDispatcher::ProcessEvent()  

#6 0x55fe922c5a62 ui::EventDispatcherDelegate::DispatchEventToTarget()  

#7 0x55fe922c59c8 ui::EventDispatcherDelegate::DispatchEvent()  

#8 0x55fe92fb68cf aura::WindowEventDispatcher::DispatchMouseEnterOrExit()  

#9 0x55fe92fb7d08 aura::WindowEventDispatcher::PreDispatchMouseEvent()  

#10 0x55fe92fb78ac aura::WindowEventDispatcher::PreDispatchEvent()  

#11 0x55fe922c5995 ui::EventDispatcherDelegate::DispatchEvent()  

#12 0x55fe92fb969f ui::EventProcessor::OnEventFromSource()  

#13 0x55fe92fc2396 ui::EventSource::DeliverEventToSink()  

#14 0x55fe92fc22ae ui::EventSource::SendEventToSinkFromRewriter()  

#15 0x55fe9421e1eb aura::WindowTreeHostPlatform::DispatchEvent()  

#16 0x55fe9421c912 views::DesktopWindowTreeHostLinux::DispatchEvent()  

#17 0x55fe922c86c8 ui::DispatchEventFromNativeUiEvent()  

#18 0x55fe928b8f67 ui::X11Window::DispatchUiEvent()  

#19 0x55fe928b8cae ui::X11Window::DispatchEvent()  

#20 0x55fe928b8fad ui::X11Window::DispatchEvent()  

#21 0x55fe922bcca9 ui::PlatformEventSource::DispatchEvent()  

#22 0x55fe928524c3 ui::X11EventSource::OnEvent()  

#23 0x55fe8e6d8822 x11::Connection::DispatchEvent()  

#24 0x55fe8e6d860b x11::Connection::ProcessNextEvent()  

#25 0x55fe8e6d837f x11::Connection::Dispatch()  

#26 0x55fe92855e82 ui::(anonymous namespace)::XSourceDispatch()  

#27 0x7fa921edf04e g\_main\_context\_dispatch  

#28 0x7fa921edf400 (/usr/lib/x86\_64-linux-gnu/libglib-2.0.so.0.6400.6+0x523ff)  

#29 0x7fa921edf4a3 g\_main\_context\_iteration  

#30 0x55fe91819d93 base::MessagePumpGlib::Run()  

#31 0x55fe91869a72 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run()  

#32 0x55fe91838e8d base::RunLoop::Run()  

#33 0x55fe8f3da573 content::BrowserMainLoop::RunMainMessageLoop()  

#34 0x55fe8f3dbd22 content::BrowserMainRunnerImpl::Run()  

#35 0x55fe8f3d818b content::BrowserMain()  

#36 0x55fe913971d2 content::ContentMainRunnerImpl::RunBrowser()  

#37 0x55fe91396c97 content::ContentMainRunnerImpl::Run()  

#38 0x55fe91394505 content::RunContentProcess()  

#39 0x55fe91394fde content::ContentMain()  

#40 0x55fe8e12c326 ChromeMain  

#41 0x7fa92115a0b3 \_\_libc\_start\_main  

#42 0x55fe8e12c12a \_start  

r8: 0000000000000006 r9: 0000000000000000 r10: 0000000000000000 r11: 00002a2c01bfbf80  

r12: 00002a2c01c11ea0 r13: 00002a2c01bfbf78 r14: 00007ffe37c4b330 r15: 00002a2c01c11e98  

di: 00002a2c01c11ea0 si: 00002a2c019b79e8 bp: 00007ffe37c4b2b0 bx: 00002a2c01bfbf68  

dx: deadbeef00000001 ax: 0001a75ea3de1070 cx: 00007ffe37c4b318 sp: 00007ffe37c4b270  

ip: 000055fe922c5e80 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000000  

trp: 000000000000000d msk: 0000000000000000 cr2: 0000000000000000  

[end of stack trace]

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 1.5 MB)
- [ASAN](attachments/ASAN) (text/plain, 9.7 KB)
- [ASAN.txt](attachments/ASAN.txt) (text/plain, 15.8 KB)

## Timeline

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-11-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### ts...@chromium.org (2021-11-09)

Although the UaF is on top of UI, by the time that happens, the culprit is long gone. The important info from the attached ASAN.txt is that this is freed in sharing_hub::ScreenshotCapturedBubbleController::Capture  at screenshot_captured_bubble_controller.cc:52

### rs...@chromium.org (2021-11-23)

skare: Can you please look at this since kmilka@ has left?

It looks like this feature is behind a flag but is currently experimentally on at 50/50 canary & dev.

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-11-23)

skare's out this week, I'll take a look :)

### [Deleted User] (2021-11-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-11-23)

I can't repro this on Mac, for what it's worth. The Mac version of this feature has its own event-handling code with different lifetimes so that's not surprising.

The object being used after free is an image_editor::ScreenshotFlow according to the allocation trace, and the UAF path is an event delivery:

    #0 0x7ffaa25f381f in base::circular_deque<ui::EventDispatcher *>::ExpandCapacityIfNecessary C:\b\s\w\ir\cache\builder\src\base\containers\circular_deque.h:962
    #1 0x7ffaa25f3679 in base::circular_deque<ui::EventDispatcher *>::emplace_back<ui::EventDispatcher *> C:\b\s\w\ir\cache\builder\src\base\containers\circular_deque.h:852
    #2 0x7ffaa25f30d6 in ui::EventDispatcher::DispatchEventToEventHandlers C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:166
    #3 0x7ffaa25f28ac in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:126

ScreenshotFlow receives this in its role as a PreTargetHandler, which is registered in CreateAndAddUIOverlay() and removed in RemoveUIOverlay().



### el...@chromium.org (2021-11-23)

I also can't repro this on Linux, despite following the steps from the video. I wonder if this is either Windows-specific or some sort of race?

In any case, since this is a lifetime problem with ScreenshotFlow, the logical starting point is where ScreenshotFlow is created and destroyed. It's created and owned by a ScreenshotCapturedBubbleController, in ::Capture(), and the lifetime looks honestly fairly simple to me. The ScreenshotFlow could also be destroyed by ~ScreenshotCapturedBubbleController, but the ASAN stack trace shows that it isn't.

I wonder if the same mouse event can cause both ScreenshotFlow to be destroyed *and* ScreenshotFlow to receive an event?

### ch...@gmail.com (2021-11-23)

I'm no longer able to reproduce on Canary 98.0.4724.0 on MacOS and Windows.

### el...@chromium.org (2021-11-23)

Well, if it is, I can't figure out how to make it happen. Unfortunately I am basically stumped here.

That said, there is at least one thing that isn't obviously correct to me: it's not clear that the PreTargetHandler that ScreenshotFlow installs is *always* unregistered during destruction. I'll land a change to fix that, and then maybe ask the reporter to retry. :\

### el...@chromium.org (2021-11-23)

Ah!

https://chromium.googlesource.com/chromium/src/+log/98.0.4696.0..98.0.4724.0?pretty=fuller&n=10000

r942388 is in that range, so perhaps this is another manifestation of https://crbug.com/chromium/1268761.

Either way, Fixed, although I'm still going to do the PreTargetHandler change I mentioned.

### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4dff4980d6fb677f7141aa752620f7f7592c921a

commit 4dff4980d6fb677f7141aa752620f7f7592c921a
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Wed Nov 24 22:30:05 2021

screenshots: make lifetime more obviously correct

Currently, it should be the case that a ScreenshotFlow always
removes itself from the browser window's PreTargetHandler list.
I can't find any code paths that would lead to this not happening,
but it's certainly not obvious that it does always happen. To make
it obvious, this change:

1. Reworks the EventTarget API slightly to allow use of
   base::ScopedObservation with PreTargetHandlers, and
2. Has ScreenshotFlow use a base::ScopedObservation instead of
   manually calling {Add,Remove}PreTargetHandler.

Change (1) is required because ScopedObservation doesn't work unless
the type signature of the Add function is exactly:

  void (*AddFn)(Handler* handler);

so having it be:

  void (*AddFn)(Handler* handler, Priority p = default);

is incompatible, even though the optional argument usually allows
the add function to be called with only a Handler*.

Fixed: 1268400
Change-Id: I4c12a096ead6e1585954cc335d1484e93c89cce6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3299179
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Commit-Queue: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Commit-Position: refs/heads/main@{#945154}

[modify] https://crrev.com/4dff4980d6fb677f7141aa752620f7f7592c921a/chrome/browser/image_editor/screenshot_flow.cc
[modify] https://crrev.com/4dff4980d6fb677f7141aa752620f7f7592c921a/ui/events/event_target.cc
[modify] https://crrev.com/4dff4980d6fb677f7141aa752620f7f7592c921a/chrome/browser/image_editor/screenshot_flow.h
[modify] https://crrev.com/4dff4980d6fb677f7141aa752620f7f7592c921a/ui/events/event_target.h


### [Deleted User] (2021-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-01)

Congratulations, Khalil - the VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

Not requesting merge to dev (M98) because latest trunk commit (945154) appears to be prior to dev branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1268400?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057864)*
