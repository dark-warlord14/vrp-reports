# Security: heap-buffer-overflow on components/exo/shell_surface_util.cc:230:40 (Lacros)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060321](https://issues.chromium.org/issues/40060321) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell>UIFoundations |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | os...@chromium.org |
| **Created** | 2022-07-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Similar with issue #1330125.

**VERSION**  

Chrome Version: 105.0.5187.0 (Developer Build) Lacros/unknown (64-bit)  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

(1) Open two tabs  

(2) Detach one tab

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==5796==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60d000557700 at pc 0x5571567e765b bp 0x7ffcc271f4d0 sp 0x7ffcc271f4c8  

READ of size 8 at 0x60d000557700 thread T0 (chrome)  

SCARINESS: 23 (8-byte-read-heap-buffer-overflow)  

#0 0x5571567e765a in exo::GetTargetSurfaceForLocatedEvent(ui::LocatedEvent const\*) components/exo/shell\_surface\_util.cc:230:40  

#1 0x5571567cc1c0 in exo::Pointer::GetEffectiveTargetForEvent(ui::LocatedEvent const\*, gfx::PointF\*) const components/exo/pointer.cc:807:14  

#2 0x5571567cd958 in exo::Pointer::OnDragCompleted(ui::DropTargetEvent const&) components/exo/pointer.cc:743:18  

#3 0x55715abe038a in ash::DragDropController::Drop(aura::Window\*, ui::LocatedEvent const&) ash/drag\_drop/drag\_drop\_controller.cc:644:14  

#4 0x55715abdcc41 in ash::DragDropController::OnMouseEvent(ui::MouseEvent\*) ash/drag\_drop/drag\_drop\_controller.cc  

#5 0x5571566d6f22 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#6 0x5571566d6bcb in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#7 0x5571566d606f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#8 0x5571566d5caf in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#9 0x5571566d59ce in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#10 0x55715a38f0c5 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#11 0x5571566db62e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#12 0x5571566dbc14 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#13 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#14 0x5571472c1c5f in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1276:12  

#15 0x5571472c218e in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:758:12  

#16 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#17 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#18 0x55715abf1440 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#19 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#20 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#21 0x55715abec7d1 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#22 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#23 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#24 0x55715a95456d in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#25 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#26 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#27 0x55715a96408e in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#28 0x5571566db24d in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#29 0x55715ac31e76 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#30 0x55715ac3ac89 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#31 0x5571566e82db in Run base/callback.h:145:12  

#32 0x5571566e82db in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:36:25  

#33 0x55714383e4f8 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1361:3  

#34 0x55714383e75a in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1351:36  

#35 0x55714383da45 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1314:3  

#36 0x55714383e979 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#37 0x55715666b605 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#38 0x557156ece7d4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#39 0x5571433ad057 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#40 0x5571433accf7 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#41 0x5571433ac70e in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#42 0x557156ed92e5 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#43 0x557153ce00b4 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#44 0x557154051705 in event\_process\_active third\_party/libevent/event.c:381:4  

#45 0x557154051705 in event\_base\_loop third\_party/libevent/event.c:521:4  

#46 0x557153ce0b56 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:316:5  

#47 0x557153b9649f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:578:12  

#48 0x557153a91e76 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#49 0x55715abdb2ee in ash::DragDropController::StartDragAndDrop(std::Cr::unique\_ptr<ui::OSExchangeData, std::Cr::default\_delete[ui::OSExchangeData](javascript:void(0);)>, aura::Window\*, aura::Window\*, gfx::Point const&, int, ui::mojom::DragEventSource) ash/drag\_drop/drag\_drop\_controller.cc:245:16  

#50 0x5571567e1177 in exo::DragDropOperation::StartDragDropOperation() components/exo/drag\_drop\_operation.cc:407:45  

#51 0x557153b42cdb in Run base/callback.h:145:12  

#52 0x557153b42cdb in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#53 0x557153b94424 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:430:29)> base/task/common/task\_annotator.h:74:5  

#54 0x557153b94424 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:428:21  

#55 0x557153b93436 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:298:41  

#56 0x557153b9567e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#57 0x557153ce0f6d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:294:55  

#58 0x557153b96339 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:581:12  

#59 0x557153a91e76 in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#60 0x5571482abc53 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1042:18  

#61 0x5571482b1b82 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#62 0x5571482a4e88 in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#63 0x5571537df47a in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#64 0x5571537e29fe in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1189:10  

#65 0x5571537e1bb4 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1061:12  

#66 0x5571537daeae in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:406:36  

#67 0x5571537db598 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:434:10  

#68 0x55714204a027 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#69 0x7fa605532082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60d000557700 is located 0 bytes to the right of 144-byte region [0x60d000557670,0x60d000557700)  

allocated by thread T0 (chrome) here:  

#0 0x5571420477fd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x5571566c88e4 in ui::Event::Clone(ui::Event const&) ui/events/event.cc:195:27  

#2 0x5571567e7027 in exo::GetTargetSurfaceForLocatedEvent(ui::LocatedEvent const\*) components/exo/shell\_surface\_util.cc:226:17  

#3 0x5571567cc1c0 in exo::Pointer::GetEffectiveTargetForEvent(ui::LocatedEvent const\*, gfx::PointF\*) const components/exo/pointer.cc:807:14  

#4 0x5571567cd958 in exo::Pointer::OnDragCompleted(ui::DropTargetEvent const&) components/exo/pointer.cc:743:18  

#5 0x55715abe038a in ash::DragDropController::Drop(aura::Window\*, ui::LocatedEvent const&) ash/drag\_drop/drag\_drop\_controller.cc:644:14  

#6 0x55715abdcc41 in ash::DragDropController::OnMouseEvent(ui::MouseEvent\*) ash/drag\_drop/drag\_drop\_controller.cc  

#7 0x5571566d6f22 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#8 0x5571566d6bcb in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#9 0x5571566d606f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#10 0x5571566d5caf in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#11 0x5571566d59ce in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#12 0x55715a38f0c5 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#13 0x5571566db62e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#14 0x5571566dbc14 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#15 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#16 0x5571472c1c5f in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1276:12  

#17 0x5571472c218e in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:758:12  

#18 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#19 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#20 0x55715abf1440 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#21 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#22 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#23 0x55715abec7d1 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#24 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#25 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#26 0x55715a95456d in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#27 0x5571566dbbaa in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#28 0x5571566d9e11 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#29 0x55715a96408e in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc

SUMMARY: AddressSanitizer: heap-buffer-overflow components/exo/shell\_surface\_util.cc:230:40 in exo::GetTargetSurfaceForLocatedEvent(ui::LocatedEvent const\*)  

Shadow bytes around the buggy address:  

0x0c1a800a2e90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1a800a2ea0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1a800a2eb0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1a800a2ec0: 00 00 00 00 00 fa fa fa fa fa fa fa fa fa 00 00  

0x0c1a800a2ed0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0c1a800a2ee0:[fa]fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c1a800a2ef0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c1a800a2f00: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1a800a2f10: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x0c1a800a2f20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c1a800a2f30: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

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

==5796==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### rh...@gmail.com (2022-07-18)

uploading screencast

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-07-18)

Assigning as per https://crbug.com/chromium/1330125. From my cursory look, the code hasn't changed in a while, so I'm going to mark FoundIn as an arbitrarily old release.

+aluh, can you please take a look?

[Monorail components: UI>Shell>UIFoundations]

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-07-20)

It's my CL and I know why. Let me fix it quickly.

### os...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0dfaf9875db96b1d79be58d5938fb078fbcbe862

commit 0dfaf9875db96b1d79be58d5938fb078fbcbe862
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Thu Jul 21 22:15:56 2022

Stop-gap fix to clone issue with DropTargetEvent

Real fix will be worked on in crbug.com/1346400

Bug: 1345245, 1346400

Change-Id: Ibf92ea412de89d202a9eba2ecadc4fe178554363
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779057
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Reviewed-by: Addison Luh <aluh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1026998}

[modify] https://crrev.com/0dfaf9875db96b1d79be58d5938fb078fbcbe862/components/exo/shell_surface_util.cc


### os...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### os...@chromium.org (2022-07-22)

This is 105

### rh...@gmail.com (2022-07-22)

Thanks oshima-san for the quick fix.

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

Not requesting merge to dev (M105) because latest trunk commit (1026998) appears to be prior to dev branch point (1027018). If this is incorrect, please replace the Merge-NA-105 label with Merge-Request-105. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report. The reward amount was decided up based on this issue resulting in a read and being substantially mitigated by not being remote exploitable and required user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-31)

1. Just https://crrev.com/c/3867505
2. Low, no conflicts
3. 105
4. Yes

### gm...@google.com (2022-09-01)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0071fb0df816e528d92640f7e7890ba4c3f21129

commit 0071fb0df816e528d92640f7e7890ba4c3f21129
Author: Mitsuru Oshima <oshima@chromium.org>
Date: Tue Sep 13 12:14:38 2022

[M102-LTS] Stop-gap fix to clone issue with DropTargetEvent

Real fix will be worked on in crbug.com/1346400

Bug: 1345245, 1346400

(cherry picked from commit 0dfaf9875db96b1d79be58d5938fb078fbcbe862)

Change-Id: Ibf92ea412de89d202a9eba2ecadc4fe178554363
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3779057
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1026998}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3867505
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1347}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/0071fb0df816e528d92640f7e7890ba4c3f21129/components/exo/shell_surface_util.cc


### rz...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1345245?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1346458]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060321)*
