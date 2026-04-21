# Security: Heap-use-after-free in ash::SavedDeskDialogController::CreateDialogWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [40059699](https://issues.chromium.org/issues/40059699) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2022-05-18 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release-chromeos%2Fasan-linux-release-999995.zip?generation=1651778152805505&alt=media>  

Operating System: Linux

==16228==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700023c198 at pc 0x5574c2dfd1c0 bp 0x7ffc680269d0 sp 0x7ffc680269c8  

WRITE of size 8 at 0x60700023c198 thread T0 (chrome)  

==16228==WARNING: invalid path to external symbolizer!  

==16228==WARNING: Failed to use and restart external symbolizer!  

#0 0x5574c2dfd1bf in ash::SavedDeskDialogController::CreateDialogWidget(std::\_\_1::unique\_ptr<ash::SavedDeskDialog, std::\_\_1::default\_delete[ash::SavedDeskDialog](javascript:void(0);) >, aura::Window\*) ./../../ash/wm/desks/templates/saved\_desk\_dialog\_controller.cc:294:18  

#1 0x5574c2dfd6af in ash::SavedDeskDialogController::ShowReplaceDialog(aura::Window\*, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, base::OnceCallback<void ()>, base::OnceCallback<void ()>) ./../../ash/wm/desks/templates/saved\_desk\_dialog\_controller.cc:238:3  

#2 0x5574c2e14189 in ash::SavedDeskItemView::MaybeShowReplaceDialog(ash::SavedDeskItemView\*) ./../../ash/wm/desks/templates/saved\_desk\_item\_view.cc:483:37  

#3 0x5574bc6a9816 in Run ./../../base/callback.h:143:12  

#4 0x5574bc6a9816 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#5 0x5574bc6eaac7 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:387:29)> ./../../base/task/common/task\_annotator.h:74:5  

#6 0x5574bc6eaac7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#7 0x5574bc6ea0d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#8 0x5574bc6eb851 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#9 0x5574bc7f5239 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#10 0x5574bc6ec125 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#11 0x5574bc62801f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#12 0x5574b2fa5fa2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1059:18  

#13 0x5574b2faa407 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#14 0x5574b2fa03ca in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#15 0x5574bc403ed9 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:659:10  

#16 0x5574bc4069d6 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1166:10  

#17 0x5574bc405e20 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1038:12  

#18 0x5574bc4006cb in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#19 0x5574bc400d29 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#20 0x5574adf47994 in ChromeMain ./../../chrome/app/chrome\_main.cc:177:12  

#21 0x7fe5fcd960b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60700023c198 is located 24 bytes inside of 80-byte region [0x60700023c180,0x60700023c1d0)  

freed by thread T0 (chrome) here:  

#0 0x5574adf45a1d in operator delete(void\*) *asan\_rtl*:3  

#1 0x5574c2e77eac in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x5574c2e77eac in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x5574c2e77eac in ash::OverviewSession::Shutdown() ./../../ash/wm/overview/overview\_session.cc:305:33  

#4 0x5574c2e3bcb3 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:341:24  

#5 0x5574c2e3c51b in ash::OverviewController::EndOverview(ash::OverviewEndAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:143:3  

#6 0x5574c2e7c91f in ash::OverviewSession::OnWindowActivating(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*) ./../../ash/wm/overview/overview\_session.cc:0:0  

#7 0x5574c2937a7f in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:354:14  

#8 0x5574c2936bf9 in wm::FocusController::WindowLostFocusFromDispositionChange(aura::Window\*, aura::Window\*) ./../../ui/wm/core/focus\_controller.cc:442:10  

#9 0x5574c2936ddf in wm::FocusController::OnWindowDestroying(aura::Window\*) ./../../ui/wm/core/focus\_controller.cc:167:3  

#10 0x5574c1f79a93 in aura::Window::~Window() ./../../ui/aura/window.cc:195:14  

#11 0x5574c1f7af17 in aura::Window::~Window() ./../../ui/aura/window.cc:184:19  

#12 0x5574c23ca257 in views::Widget::CloseNow() ./../../ui/views/widget/widget.cc:705:19  

#13 0x5574c2dfd05e in ash::SavedDeskDialogController::CreateDialogWidget(std::\_\_1::unique\_ptr<ash::SavedDeskDialog, std::\_\_1::default\_delete[ash::SavedDeskDialog](javascript:void(0);) >, aura::Window\*) ./../../ash/wm/desks/templates/saved\_desk\_dialog\_controller.cc:289:21  

#14 0x5574c2dfd6af in ash::SavedDeskDialogController::ShowReplaceDialog(aura::Window\*, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, base::OnceCallback<void ()>, base::OnceCallback<void ()>) ./../../ash/wm/desks/templates/saved\_desk\_dialog\_controller.cc:238:3  

#15 0x5574c2e14189 in ash::SavedDeskItemView::MaybeShowReplaceDialog(ash::SavedDeskItemView\*) ./../../ash/wm/desks/templates/saved\_desk\_item\_view.cc:483:37  

#16 0x5574bc6a9816 in Run ./../../base/callback.h:143:12  

#17 0x5574bc6a9816 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:135:32  

#18 0x5574bc6eaac7 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:387:29)> ./../../base/task/common/task\_annotator.h:74:5  

#19 0x5574bc6eaac7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:385:21  

#20 0x5574bc6ea0d9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:290:41  

#21 0x5574bc6eb851 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#22 0x5574bc7f5239 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#23 0x5574bc6ec125 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:497:12  

#24 0x5574bc62801f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#25 0x5574b2fa5fa2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1059:18  

#26 0x5574b2faa407 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#27 0x5574b2fa03ca in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#28 0x5574bc403ed9 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:659:10  

#29 0x5574bc4069d6 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1166:10  

#30 0x5574bc405e20 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1038:12  

#31 0x5574bc4006cb in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:407:36  

#32 0x5574bc400d29 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:435:10  

#33 0x5574adf47994 in ChromeMain ./../../chrome/app/chrome\_main.cc:177:12

previously allocated by thread T0 (chrome) here:  

#0 0x5574adf451bd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5574c2e765f5 in make\_unique[ash::SavedDeskDialogController](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x5574c2e765f5 in ash::OverviewSession::Init(std::\_\_1::vector<aura::Window\*, std::\_\_1::allocator[aura::Window\\*](javascript:void(0);) > const&, std::\_\_1::vector<aura::Window\*, std::\_\_1::allocator[aura::Window\\*](javascript:void(0);) > const&) ./../../ash/wm/overview/overview\_session.cc:191:9  

#3 0x5574c2e3b612 in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:431:24  

#4 0x5574c2e3aa0d in ash::OverviewController::StartOverview(ash::OverviewStartAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:129:3  

#5 0x5574c245f6e4 in ash::(anonymous namespace)::HandleToggleOverview() ./../../ash/accelerators/accelerator\_controller\_impl.cc:882:26  

#6 0x5574c2456d3d in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:2469:7  

#7 0x5574c24583a3 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:1733:3  

#8 0x5574c233348c in TryProcess ./../../ui/base/accelerators/accelerator\_manager.cc:153:17  

#9 0x5574c233348c in ui::AcceleratorManager::Process(ui::Accelerator const&) ./../../ui/base/accelerators/accelerator\_manager.cc:83:27  

#10 0x5574c293b86f in ash::PreTargetAcceleratorHandler::ProcessAccelerator(ui::KeyEvent const&, ui::Accelerator const&) ./../../ash/accelerators/pre\_target\_accelerator\_handler.cc:74:45  

#11 0x5574c293becf in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ./../../ui/wm/core/accelerator\_filter.cc:51:18  

#12 0x5574beab4897 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#13 0x5574beab45bb in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_1::vector<ui::EventHandler\*, std::\_\_1::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:177:7  

#14 0x5574beab3c1d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:125:3  

#15 0x5574beab38a4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#16 0x5574beab3610 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#17 0x5574c1f9f1e9 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#18 0x5574c1fb5e62 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ./../../ui/aura/window\_tree\_host.cc:383:23  

#19 0x5574bf311dc9 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ./../../ui/base/ime/input\_method\_base.cc:140:33  

#20 0x5574bf457565 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:616:38  

#21 0x5574bf456dc6 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:139:14  

#22 0x5574c1f99acb in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ./../../ui/aura/window\_event\_dispatcher.cc:1080:54  

#23 0x5574c1f98472 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/aura/window\_event\_dispatcher.cc:568:15  

#24 0x5574beab35c4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:51:34  

#25 0x5574c1f9f1e9 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:49:17  

#26 0x5574beab7ffe in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#27 0x5574beab6e07 in ui::EventRewriter::SendEventFinally(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:94:39  

#28 0x5574b21cf6c4 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1837:9  

#29 0x5574b21cdb17 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#30 0x5574beab84a6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#31 0x5574beab6c4b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-999995/chrome+0x233471bf) (BuildId: e1faf4ab14b96383)  

Shadow bytes around the buggy address:  

0x0c0e8003f7e0: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

0x0c0e8003f7f0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0e8003f800: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x0c0e8003f810: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c0e8003f820: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

=>0x0c0e8003f830: fd fd fd[fd]fd fd fd fd fd fd fa fa fa fa fd fd  

0x0c0e8003f840: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0e8003f850: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

0x0c0e8003f860: fd fd fd fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c0e8003f870: 00 fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c0e8003f880: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==16228==ABORTING

## Attachments

- [Screencast from 19 ماي, 2022 +01 00:33:50.webm](attachments/Screencast from 19 ماي, 2022 +01 00_33_50.webm) (video/webm, 2.0 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 1.4 MB)

## Timeline

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-05-19)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### ch...@gmail.com (2022-05-20)

Steps to reproduce : 

1) Launch Chromium
2) Press F5 >> Save desk as a template 
3) Back to Desk_1
4) Press F5 >> Save desk as a template
5) Delete the last template 

### am...@chromium.org (2022-05-25)

assigning to current Chrome OS security sheriff aashay@ for chrome OS triage 

### aa...@google.com (2022-05-26)

I was able to repro the crash on an older M103 build after flipping the feature flag. I _think_ the feature launched to users in M101 stable.

### [Deleted User] (2022-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2022-05-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d4699f12772406edfbb74c3931de904adf48bb5

commit 2d4699f12772406edfbb74c3931de904adf48bb5
Author: Daniel Andersson <dandersson@chromium.org>
Date: Tue May 31 17:24:29 2022

saved_desks: Bail early on showing a dialog if one is already active.

This takes care of a UAF with a complicated call chain. Repro steps can
be found in the bug. What happens is that when the close button on one
saved desk item is clicked, this will:

* Trigger ShowDeleteDialog.
* Un-blur the name entry on the other desk item.
** Which will in turn trigger ShowReplaceDialog.

This cases the dialog controller to try to close the first dialog, which
will for some window activation reason cause overview mode to exit. This
will in turn destroy the SavedDeskDialogController that is currently
executing code, which eventually leads to the UAF.

This change sidesteps this mess by bailing early on showing a dialog if
one is already active. What happens when the repro steps are followed is
that the delete dialog will be shown, and the newly created desk item
with the duplicate name will have "(1)" tacked on at the end.

Bug: 1327087
Change-Id: I365e207b0e176027a0dc039915d5028461882dea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3674408
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1009145}

[modify] https://crrev.com/2d4699f12772406edfbb74c3931de904adf48bb5/ash/wm/desks/templates/saved_desk_unittest.cc
[modify] https://crrev.com/2d4699f12772406edfbb74c3931de904adf48bb5/ash/wm/desks/templates/saved_desk_dialog_controller.cc
[modify] https://crrev.com/2d4699f12772406edfbb74c3931de904adf48bb5/ash/wm/desks/templates/saved_desk_dialog_controller.h


### da...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-06-01)

Verified on linux-release-chromeos_asan-linux-release-1009331.zip - Fixed!

### ch...@gmail.com (2022-06-02)

Should this be marked as fixed? Thanks!

### ch...@gmail.com (2022-06-08)

Friendly ping :)

### da...@chromium.org (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

Requesting merge to stable M102 because latest trunk commit (1009145) appears to be after stable branch point (992738).

Requesting merge to beta M103 because latest trunk commit (1009145) appears to be after beta branch point (1002911).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-08)

Merge review required: M103 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-08)

Merge review required: M102 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-06-09)

Please complete the merge questionnaire.

If you'd like to try and merge this to 102, please ping me after completing the merge questionnaire. The CP would need to be completed before EOD PDT.

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### dg...@google.com (2022-06-13)

dandersson@ - can you please provide the info requested in https://crbug.com/chromium/1327087#c18?

### ce...@google.com (2022-06-13)

This missed our build cutoff (last thursday) for M102s stable respin. We haven't been able to finish auto-test results due to a lab outage, but our manual regression test team has finished their work and moved on to other channels. 

I'm going to mark this merge rejected for 102, since we're ~10days out from 103.

### am...@google.com (2022-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-16)

Congratulations, Khalil! The VRP Panel has decided to award you $3,000 for this report. The reward amount was decided due to the mitigations of not being remote exploitable and requiring significant user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-06-16)

Not sure why this has been labeled as "security severity high". It's in a feature that is by default disabled and still sees extremely little external use. Additionally to trigger the bug, one has to follow some steps that people are unlikely to stumble upon. It is nevertheless something that can trigger a crash, so here are some answers:

1) I believe the purported severity means that we're still in the merge window.
2) https://chromium-review.googlesource.com/c/chromium/src/+/3674408
3) I've only tested on ToT.
4) This is a bug fix, not a feature.
5) Added dhaddock@ to check.
6) I don't think it does, but one can test by running with the flag "DesksTemplates" and follow the repro steps in #3

### da...@chromium.org (2022-06-16)

[Empty comment from Monorail migration]

### dg...@google.com (2022-06-16)

Approved for M103 pending lgtm from dhaddock@

### [Deleted User] (2022-06-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/600b729641e51545d65bb8d5d939cef3a96b42ee

commit 600b729641e51545d65bb8d5d939cef3a96b42ee
Author: Daniel Andersson <dandersson@chromium.org>
Date: Tue Jun 21 19:50:17 2022

saved_desks: Bail early on showing a dialog if one is already active.

This takes care of a UAF with a complicated call chain. Repro steps can
be found in the bug. What happens is that when the close button on one
saved desk item is clicked, this will:

* Trigger ShowDeleteDialog.
* Un-blur the name entry on the other desk item.
** Which will in turn trigger ShowReplaceDialog.

This cases the dialog controller to try to close the first dialog, which
will for some window activation reason cause overview mode to exit. This
will in turn destroy the SavedDeskDialogController that is currently
executing code, which eventually leads to the UAF.

This change sidesteps this mess by bailing early on showing a dialog if
one is already active. What happens when the repro steps are followed is
that the delete dialog will be shown, and the newly created desk item
with the duplicate name will have "(1)" tacked on at the end.

(cherry picked from commit 2d4699f12772406edfbb74c3931de904adf48bb5)

Bug: 1327087
Change-Id: I8aa65815c02940e8de24d0651faaedff072dedfc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3674408
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1009145}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3717283
Cr-Commit-Position: refs/branch-heads/5060@{#1016}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/600b729641e51545d65bb8d5d939cef3a96b42ee/ash/wm/desks/templates/saved_desk_unittest.cc
[modify] https://crrev.com/600b729641e51545d65bb8d5d939cef3a96b42ee/ash/wm/desks/templates/saved_desk_dialog_controller.h
[modify] https://crrev.com/600b729641e51545d65bb8d5d939cef3a96b42ee/ash/wm/desks/templates/saved_desk_dialog_controller.cc


### [Deleted User] (2022-06-21)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-06-21)

1. Probably not. It was likely broken before the milestone it was found in.
2. No, I believe the feature was there before 102.

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

Changed files doesn't exist in M96

### am...@chromium.org (2022-07-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-03)

[Empty comment from Monorail migration]

### gm...@google.com (2022-07-14)

@rzanoni we need this in LTC-102, please evaluate.

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-12)

1. Just https://crrev.com/c/3822723
2. Low, only a few conflicting calls
3. 104
4. Yes

### gm...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ceb68576fde2f50d52cdef645c56bfd1309f8408

commit ceb68576fde2f50d52cdef645c56bfd1309f8408
Author: Daniel Andersson <dandersson@chromium.org>
Date: Wed Aug 17 12:59:10 2022

[M102-LTS] saved_desks: Bail early on showing a dialog if one is already active.

M102 merge issues:
  ash/wm/desks/templates/desks_templates_dialog_controller.cc:
    ShowReplaceDialog():
      Conflicting declarations of dialog.

  ash/wm/desks/templates/desks_templates_unittest.cc:
    Conflicting calls after WaitForDesksTemplatesUI().

This takes care of a UAF with a complicated call chain. Repro steps can
be found in the bug. What happens is that when the close button on one
saved desk item is clicked, this will:

* Trigger ShowDeleteDialog.
* Un-blur the name entry on the other desk item.
** Which will in turn trigger ShowReplaceDialog.

This cases the dialog controller to try to close the first dialog, which
will for some window activation reason cause overview mode to exit. This
will in turn destroy the SavedDeskDialogController that is currently
executing code, which eventually leads to the UAF.

This change sidesteps this mess by bailing early on showing a dialog if
one is already active. What happens when the repro steps are followed is
that the delete dialog will be shown, and the newly created desk item
with the duplicate name will have "(1)" tacked on at the end.

(cherry picked from commit 2d4699f12772406edfbb74c3931de904adf48bb5)

Bug: 1327087
Change-Id: I365e207b0e176027a0dc039915d5028461882dea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3674408
Commit-Queue: Daniel Andersson <dandersson@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1009145}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3822723
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1309}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ceb68576fde2f50d52cdef645c56bfd1309f8408/ash/wm/desks/templates/desks_templates_dialog_controller.cc
[modify] https://crrev.com/ceb68576fde2f50d52cdef645c56bfd1309f8408/ash/wm/desks/templates/desks_templates_unittest.cc
[modify] https://crrev.com/ceb68576fde2f50d52cdef645c56bfd1309f8408/ash/wm/desks/templates/desks_templates_dialog_controller.h


### rz...@google.com (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1327087?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1328933, crbug.com/chromium/1329747]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059699)*
