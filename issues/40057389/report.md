# Security: negative-size-param in image_editor::ScreenshotFlow::RemoveUIOverlay

| Field | Value |
|-------|-------|
| **Issue ID** | [40057389](https://issues.chromium.org/issues/40057389) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2021-09-25 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version: 96.0.4652.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

Enable #sharing-desktop-screenshots and #sharing-hub-desktop-omnibox

1. Open two tabs
2. In the second tab, start to screenshot it.
3. Move the current tab to new window then start to screenshot it again.

=================================================================  

==3696==ERROR: AddressSanitizer: negative-size-param: (size=-8)  

#0 0x106c50b7c in \_\_asan\_memmove+0x7c (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x45b7c)  

#1 0x12b6f8f8f in ui::Layer::Remove(ui::Layer\*) vector:1719  

#2 0x12eda188f in image\_editor::ScreenshotFlow::RemoveUIOverlay() screenshot\_flow.cc:110  

#3 0x12eda14de in image\_editor::ScreenshotFlow::~ScreenshotFlow() screenshot\_flow.cc:55  

#4 0x12eda19fd in image\_editor::ScreenshotFlow::~ScreenshotFlow() screenshot\_flow.cc:54  

#5 0x12e05de6e in sharing\_hub::ScreenshotCapturedBubbleController::Capture(Browser\*) unique\_ptr.h:54  

#6 0x12d97fbc9 in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) browser\_command\_controller.cc:584  

#7 0x12e81ad09 in sharing\_hub::SharingHubBubbleViewImpl::OnActionSelected(sharing\_hub::SharingHubBubbleActionButton\*) sharing\_hub\_bubble\_view\_impl.cc:109  

#8 0x12cd50f59 in base::internal::Invoker<base::internal::BindState<views::Button::PressedCallback::PressedCallback(base::RepeatingCallback<void ()>)::$\_0, base::RepeatingCallback<void ()> >, void (ui::Event const&)>::Run(base::internal::BindStateBase\*, ui::Event const&) callback.h:167  

#9 0x12e3ac93d in HoverButtonController::OnMouseReleased(ui::MouseEvent const&) callback.h:167  

#10 0x12cd327e6 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) scoped\_target\_handler.cc:28  

#11 0x125f9d37f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191  

#12 0x125f9cc20 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:84  

#13 0x12ceeeaa7 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) root\_view.cc:480  

#14 0x12cf0df48 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1549  

#15 0x12cfafbac in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:854  

#16 0x1294488f9 in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:595  

#17 0x129445db4 in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:308  

#18 0x129477f7b in \_\_\_ZN12remote\_cocoa17CocoaMouseCapture14ActiveEventTap4InitEv\_block\_invoke mouse\_capture.mm:93  

#19 0x7fff8a90c7f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#20 0x7fff8af0523e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#21 0x122b15ad4 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:335  

#22 0x123d80689 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xd471689)  

#23 0x122b14e4e in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:319  

#24 0x7fff8a7803d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6)  

#25 0x123d9519a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:743  

#26 0x123d90f18 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:161  

#27 0x123cb17a3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:462  

#28 0x123bec7c8 in base::RunLoop::Run(base::Location const&) run\_loop.cc:134  

#29 0x11b0696c3 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:989  

#30 0x11b06db31 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:152  

#31 0x11b06344c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:49  

#32 0x12295ab7a in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:609  

#33 0x122959c65 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:972  

#34 0x122955ad0 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:390  

#35 0x12295799a in content::ContentMain(content::ContentMainParams const&) content\_main.cc:418  

#36 0x116913b64 in ChromeMain chrome\_main.cc:172  

#37 0x106b00bff in main chrome\_exe\_main\_mac.cc:115  

#38 0x7fffa28e0234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x6060002c3a08 is located 8 bytes to the right of 64-byte region [0x6060002c39c0,0x6060002c3a00)  

allocated by thread T0 here:  

#0 0x106c526d0 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x476d0)  

#1 0x1169114e7 in operator new(unsigned long) new.cpp:67  

#2 0x12b709b4b in void std::\_\_1::vector<ui::Layer\*, std::\_\_1::allocator[ui::Layer\\*](javascript:void(0);) >::\_\_push\_back\_slow\_path<ui::Layer\* const&>(ui::Layer\* const&&&) allocator.h:82  

#3 0x12b700617 in ui::Layer::Add(ui::Layer\*) vector:1642  

#4 0x12cec01e4 in views::View::ReparentLayer(ui::Layer\*) view.cc:2965  

#5 0x12cebffa3 in views::View::UpdateParentLayer() view.cc:2002  

#6 0x12cec9bc7 in views::View::UpdateParentLayers() view.cc:2924  

#7 0x12cec7be3 in views::View::AddChildViewAtImpl(views::View\*, int) view.cc:2539  

#8 0x12ea52285 in ToolbarView::Init() view.h:423  

#9 0x12e36cf74 in BrowserView::AddedToWidget() browser\_view.cc:3114  

#10 0x12ceca98f in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) view.cc:2679  

#11 0x12cec812e in views::View::AddChildViewAtImpl(views::View\*, int) view.cc:2565  

#12 0x12cf9a51a in views::NonClientView::ViewHierarchyChanged(views::ViewHierarchyChangedDetails const&) non\_client\_view.cc:310  

#13 0x12cec9dd7 in views::View::ViewHierarchyChangedImpl(views::ViewHierarchyChangedDetails const&) view.cc:2696  

#14 0x12ceca94a in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) view.cc:2677  

#15 0x12cec812e in views::View::AddChildViewAtImpl(views::View\*, int) view.cc:2565  

#16 0x12cef990c in views::Widget::Init(views::Widget::InitParams) widget.cc:422  

#17 0x12e1d351f in BrowserFrame::InitBrowserFrame() browser\_frame.cc:121  

#18 0x12e3846c7 in BrowserWindow::CreateBrowserWindow(std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >, bool, bool) browser\_window\_factory.cc:54  

#19 0x12d95de23 in Browser::Browser(Browser::CreateParams const&) browser.cc:530  

#20 0x12d95c7cc in Browser::Create(Browser::CreateParams const&) browser.cc:450  

#21 0x12e8d8afe in TabDragController::CreateBrowserForDrag(TabDragContext\*, gfx::Point const&, gfx::Vector2d\*, std::\_\_1::vector<gfx::Rect, std::\_\_1::allocator[gfx::Rect](javascript:void(0);) >\*) tab\_drag\_controller.cc:2161  

#22 0x12e8d3083 in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) tab\_drag\_controller.cc:1413  

#23 0x12e8d0cba in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) tab\_drag\_controller.cc:890  

#24 0x12e8cf0cb in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:856  

#25 0x12e8c7a80 in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:613  

#26 0x12e961ccc in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:462  

#27 0x12e96e96b in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:3789  

#28 0x12ceb93b2 in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:3045  

#29 0x125f9d37f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 4.4 MB)

## Timeline

### [Deleted User] (2021-09-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-09-25)

I think skare@ could be the right owner for this issue.

### aj...@google.com (2021-09-27)

Thanks - I'm not able to repro this on Windows at e0a13a7.

CC'ing some sharing folks to take a look

[Monorail components: UI>Browser>Sharing]

### [Deleted User] (2021-09-27)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@google.com (2021-09-28)

I don't know how I can help with this one.  Re-add and ping with details if someone sees how I can.

### [Deleted User] (2021-09-29)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-10-05)

taking a look. Details: this would be Mac-only. 

behind a flag for Screenshots. only accessible via about://flags however we will finch on for canary+dev soon. 

Might be in scope for Lens Region Search though, which is looking to experiment/launch soon, so leaving labels.

### sk...@chromium.org (2021-10-07)

working on a fix, as an update, still able to repro at HEAD

### sk...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-10-07)

moved off iteration since it was added in the middle and I don't believe this affects Lens.

However looking now and fixing ASAP; desktop screenshots will be finched on for Canary soon.

### sk...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-10-12)

As a status update

Google Chrome	97.0.4668.0 (Developer Build) (x86_64)
Revision	refs/heads/main@{#930532}
OS	macOS Version 11.6 (Build 20G165)

Still able to repro with desktop screenshot functionality, which will be in canary in M96 timeframe but no further. Adding to this iteration to address.

NOT able to repro with Lens Region Search labs feature, which will be an experiment and possibly launch around 95-96-97.


### sk...@chromium.org (2021-10-13)

Verified this does not affect lens, which might go to stable in M96. 

Desktop screenshots will not be proceeding past dev/canary in M96. Removing RBS.


### [Deleted User] (2021-10-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b79ddf659096248fc9cc6ddcc9ed9c241ac2d27

commit 1b79ddf659096248fc9cc6ddcc9ed9c241ac2d27
Author: Travis Skare <skare@chromium.org>
Date: Wed Oct 20 01:05:40 2021

[DesktopScreenshots] Close capture on WebContentsObserver notification.

Bug: 1261268,1253038
Change-Id: Ibfac95c7f1261fd780aae1481ec7a1d06f40843b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3230461
Commit-Queue: Travis Skare <skare@chromium.org>
Reviewed-by: Kristi Park <kristipark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#933267}

[modify] https://crrev.com/1b79ddf659096248fc9cc6ddcc9ed9c241ac2d27/chrome/browser/image_editor/screenshot_flow.cc
[modify] https://crrev.com/1b79ddf659096248fc9cc6ddcc9ed9c241ac2d27/chrome/browser/image_editor/screenshot_flow.h


### sk...@chromium.org (2021-10-20)

This was marked M-96; if the prior change fixes it then we can merge. 

However the screenshots feature is not complete, off by default / experimental, and while the second, larger, piece is in development will not be on beta/stable in M96-M98. Possibly M99. Lens uses this code but closes their feature down in a way that does not run into the trace mentioned here (tested this a bit).

This will only affect 50% dev/canary through 2021. So removing releaseblock-stable, setting M-99 vs M-96, adjusting labels for off-by-default, leaving severity-medium.

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Congratulations, Khalil! The VRP Panel has decided to award you $5000 for this report. Thank you for your report and efforts!

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-01-26)

This issue was migrated from crbug.com/chromium/1253038?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057389)*
