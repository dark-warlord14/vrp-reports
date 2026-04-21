# Security: heap-use-after-free ash/host/ash_window_tree_host_unified.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40059254](https://issues.chromium.org/issues/40059254) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | os...@chromium.org |
| **Created** | 2022-03-31 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
Repro on linux-chromeOS

1. Enable --ash-dev-shortcuts and dual display
2. Ctrl + Shift + U (wait 2s) Ctrl + Shift + U

What is the expected behavior?
not crash

What went wrong?
=================================================================
==192421==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070002f31f0 at pc 0x5583f439d0ce bp 0x7ffff047a710 sp 0x7ffff047a708
READ of size 8 at 0x6070002f31f0 thread T0 (chrome)
    #0 0x5583f439d0cd in ash::UnifiedEventTargeter::FindTargetForEvent(ui::EventTarget*, ui::Event*) ash/host/ash_window_tree_host_unified.cc:51:7
    #1 0x5583f3c7d357 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc
    #2 0x5583f04c67be in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #3 0x5583f04c6cb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #4 0x5583f04c53db in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #5 0x5583e40bab11 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >, ui::EventRewriteStatus, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc
    #6 0x5583e40b8c09 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:751:12
    #7 0x5583f04c6c66 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #8 0x5583f04c53db in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #9 0x5583f435ec20 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #10 0x5583f04c6c66 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #11 0x5583f04c53db in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #12 0x5583f435a88a in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/accessibility_event_rewriter.cc
    #13 0x5583f04c6466 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:144:29
    #14 0x5583f43943c3 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:232:38
    #15 0x5583f439b8ae in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ash/host/ash_window_tree_host_platform.cc:200:40
    #16 0x5583f04d0def in Run base/callback.h:142:12
    #17 0x5583f04d0def in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:28:25
    #18 0x5583e1494467 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/ozone/platform/x11/x11_window.cc:1292:3
    #19 0x5583e1493cbd in ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc:1245:3
    #20 0x5583e14947b8 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc
    #21 0x5583f046efd1 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:99:29
    #22 0x5583f0bb17c7 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #23 0x5583e10d03d3 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14
    #24 0x5583e10d00fd in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3
    #25 0x5583e10cfbc3 in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #26 0x5583f0bba803 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11_event_watcher_fdwatch.cc:64:15
    #27 0x5583ee409ce5 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #28 0x5583ee768f1c in event_process_active base/third_party/libevent/event.c:381:4
    #29 0x5583ee768f1c in event_base_loop base/third_party/libevent/event.c:521:4
    #30 0x5583ee40a816 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:246:5
    #31 0x5583ee303c7a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #32 0x5583ee238f8c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #33 0x5583e4b0b99a in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1067:18
    #34 0x5583e4b0fe81 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #35 0x5583e4b05b7a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #36 0x5583ee01701f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #37 0x5583ee019b7f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1148:10
    #38 0x5583ee018fb8 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1020:12
    #39 0x5583ee013781 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #40 0x5583ee013e08 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #41 0x5583dfce356a in ChromeMain chrome/app/chrome_main.cc:176:12
    #42 0x7f24a85340b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6070002f31f0 is located 64 bytes inside of 72-byte region [0x6070002f31b0,0x6070002f31f8)
freed by thread T0 (chrome) here:
    #0 0x5583dfce15ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5583f439b3b2 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x5583f439b3b2 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x5583f439b3b2 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x5583f439b3b2 in ash::AshWindowTreeHostPlatform::PrepareForShutdown() ash/host/ash_window_tree_host_platform.cc:146:3
    #5 0x5583f433a78d in ash::MirrorWindowController::CloseAndDeleteHost(ash::MirrorWindowController::MirroringHostInfo*, bool) ash/display/mirror_window_controller.cc:423:24
    #6 0x5583f43388a4 in ash::MirrorWindowController::Close(bool) ash/display/mirror_window_controller.cc:342:5
    #7 0x5583f4344e0d in ash::WindowTreeHostManager::CloseMirroringDisplayIfNotNecessary() ash/display/window_tree_host_manager.cc:715:30
    #8 0x5583f3da6b32 in display::DisplayManager::UpdateDisplaysWith(std::__1::vector<display::ManagedDisplayInfo, std::__1::allocator<display::ManagedDisplayInfo> > const&) ui/display/manager/display_manager.cc:921:16
    #9 0x5583f3daab4e in display::DisplayManager::ReconfigureDisplays() ui/display/manager/display_manager.cc:1610:3
    #10 0x5583f4138a7f in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2137:7
    #11 0x5583f4139431 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1705:3
    #12 0x5583f400bc8e in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #13 0x5583f400bc8e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #14 0x5583f45fdb2f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent*) ui/wm/core/accelerator_filter.cc:51:18
    #15 0x5583f04c31eb in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #16 0x5583f04c2fd9 in ui::EventDispatcher::DispatchEventToEventHandlers(std::__1::vector<ui::EventHandler*, std::__1::allocator<ui::EventHandler*> >*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #17 0x5583f04c25fd in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #18 0x5583f04c2284 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #19 0x5583f04c1ff0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #20 0x5583f3c7d3ef in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #21 0x5583f3c93926 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:375:23
    #22 0x5583f0d15a01 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent*) const ui/base/ime/input_method_base.cc:140:33
    #23 0x5583f0e592d3 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:135:16
    #24 0x5583f3c783eb in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1067:54
    #25 0x5583f3c76de0 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:555:15
    #26 0x5583f04c1fa4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #27 0x5583f3c7d3ef in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #28 0x5583f439d027 in ash::UnifiedEventTargeter::FindTargetForEvent(ui::EventTarget*, ui::Event*) ash/host/ash_window_tree_host_unified.cc:48:49
    #29 0x5583f3c7d357 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc
    #30 0x5583f04c67be in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #31 0x5583f04c6cb6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #32 0x5583f04c53db in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #33 0x5583e40bab11 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >, ui::EventRewriteStatus, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc

previously allocated by thread T0 (chrome) here:
    #0 0x5583dfce0d4d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5583f439c4a8 in make_unique<ash::UnifiedEventTargeter, aura::Window *&, aura::Window *, ash::AshWindowTreeHostDelegate *&> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x5583f439c4a8 in ash::AshWindowTreeHostUnified::RegisterMirroringHost(ash::AshWindowTreeHost*) ash/host/ash_window_tree_host_unified.cc:92:7
    #3 0x5583f43395ef in ash::MirrorWindowController::UpdateWindow(std::__1::vector<display::ManagedDisplayInfo, std::__1::allocator<display::ManagedDisplayInfo> > const&) ash/display/mirror_window_controller.cc:224:27
    #4 0x5583f4344d7e in ash::WindowTreeHostManager::CreateOrUpdateMirroringDisplay(std::__1::vector<display::ManagedDisplayInfo, std::__1::allocator<display::ManagedDisplayInfo> > const&) ash/display/window_tree_host_manager.cc:707:32
    #5 0x5583f3db2ce9 in display::DisplayManager::CreateMirrorWindowIfAny() ui/display/manager/display_manager.cc:2161:14
    #6 0x5583ee2c15e6 in Run base/callback.h:142:12
    #7 0x5583ee2c15e6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #8 0x5583ee3028ed in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:388:29)> base/task/common/task_annotator.h:74:5
    #9 0x5583ee3028ed in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:386:21
    #10 0x5583ee302007 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:291:41
    #11 0x5583ee3035c1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #12 0x5583ee40a42c in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #13 0x5583ee303c7a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:498:12
    #14 0x5583ee238f8c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #15 0x5583e4b0b99a in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1067:18
    #16 0x5583e4b0fe81 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #17 0x5583e4b05b7a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #18 0x5583ee01701f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #19 0x5583ee019b7f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1148:10
    #20 0x5583ee018fb8 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1020:12
    #21 0x5583ee013781 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #22 0x5583ee013e08 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #23 0x5583dfce356a in ChromeMain chrome/app/chrome_main.cc:176:12
    #24 0x7f24a85340b2 in __libc_start_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free ash/host/ash_window_tree_host_unified.cc:51:7 in ash::UnifiedEventTargeter::FindTargetForEvent(ui::EventTarget*, ui::Event*)
Shadow bytes around the buggy address:
  0x0c0e800565e0: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0e800565f0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa 00 00
  0x0c0e80056600: 00 00 00 00 00 00 00 00 fa fa fa fa fd fd fd fd
  0x0c0e80056610: fd fd fd fd fd fd fa fa fa fa 00 00 00 00 00 00
  0x0c0e80056620: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00
=>0x0c0e80056630: 00 00 fa fa fa fa fd fd fd fd fd fd fd fd[fd]fa
  0x0c0e80056640: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x0c0e80056650: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c0e80056660: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fd fd
  0x0c0e80056670: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd
  0x0c0e80056680: fd fd fd fd fd fd fa fa fa fa fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
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
==192421==ABORTING

Did this work before? N/A 

Chrome version: 102.0.4974.0   Channel: dev
OS Version: linux-chromeos

Enabling ash-dev-shortcuts are reflected like physical devices, so I'm submitting a report like this instead. If needed I can test it on the actual device.

## Attachments

- [screencast_1311885.webm](attachments/screencast_1311885.webm) (video/webm, 2.4 MB)
- [Notes_ Issue 1311885 - unified_desktop_stacktrace_ctrl_shift_u.pdf](attachments/Notes_ Issue 1311885 - unified_desktop_stacktrace_ctrl_shift_u.pdf) (application/pdf, 95.4 KB)

## Timeline

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-03-31)

[Empty comment from Monorail migration]

### ps...@google.com (2022-04-06)

@xdai - this looks like a window manager issue in ash. Can you help route it to the right owner?

[Monorail components: UI>Shell]

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-07)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xd...@google.com (2022-04-08)

Looks like it crashed when it tries to create mirror display. I can repro the crash on the emulator. 
zentaro@ not sure if your team is the right owner here. +cc afakhry@ as the display owner as well

### [Deleted User] (2022-04-15)

zentaro: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ze...@chromium.org (2022-04-15)

I didn't see this assigned to me. Even though it's trigger by a shortcut it looks like the cause is target not unregistering itself.

Also if this can only repro with this flag then I don't think it should be release blocking.  --ash-dev-shortcuts

The use is in ash/host/ash_window_tree_host_unified.cc and the free was via ash/display/mirror_window_controller.cc

I'll get ashleydp@ to take an initial look at it and remove the release block flag. If there's a repro that doesn't require enabling dev debug flags then let us know.

### [Deleted User] (2022-04-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

ashleydp: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2022-05-12)

Hi there, I'm reaching out because this issue is marked as a Stable channel release blocker for CrOS M102.

Stable cut is Tuesday, May 17. If the requisite merges are not submitted prior to or on this date, your fixes will go straight to Stable and miss an opportunity to soak on Beta for a week.

If this issue does not have a clear path to resolution by Tuesday, 5/24, please put time on my calendar (ceb@) to discuss contingencies. 

Thanks,

Cole (M102 milestone owner)

### rh...@gmail.com (2022-05-12)

zentaro@,

>> If there's a repro that doesn't require enabling dev debug flags then let us know.
I really not sure if the above statement/question for me.

(0) Pass command with --ash-enable-unified-desktop
(1) Setup dual monitor with tablet mode (so it's enabled by default mirrored displays)
(2) Go to settings -> devices -> display: unchecked mirror display then there's menu about "Allow window to span display" appeared. This is because we pass arguments "--ash-enable-unified-desktop"
(3) Click/move the button to active the menu  "Allow window to span display".
(4) Close Chrombook lid.

### ze...@chromium.org (2022-05-12)

OK so just to help with prioritizing...

- this requires enabling unified desktop flag (which is disabled by default)
- it does *not* require enabling debug flags eg. --ash-dev-shortcuts

### [Deleted User] (2022-05-16)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-16)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@google.com (2022-05-18)

I tested this a few times and was only able to reproduce when using the developer shortcut of "CTRL + SHIFT + U". The steps from https://crbug.com/chromium/1311885#c15 did not reproduce the issue, with or without tablet mode enabled. From testing it appears to need the --ash-dev-shortcuts to be enabled to reproduce I do not think this should be release blocking.

From the stack trace it appears that the WindowTargeter is still processing events after being deleted, I have not found what is causing that to hang around after being deleted.

### ce...@google.com (2022-05-18)

Based on the reproduction requiring dev flags enabled in combination with a keyboard shortcut, I agree that this shouldn't block promotion. We can merge this fix to 102 whenever it is ready.

### [Deleted User] (2022-05-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-19)

This release blocker is now considered 'urgent' and therefore subject to the following SLOs:
Assigned Owner: 1 day
Comment SLO: Every day
Fix SLO: Within 3 days.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@google.com (2022-05-19)

Adding Zen's google email

### ps...@google.com (2022-05-19)

Changing security severity to Low since a non-default flag and possibly also a developer flag is required to trigger the crash.

### ce...@google.com (2022-05-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-05-20)

If this needs a non-default flag we can label this as Security_Impact-None to stop it from being urgent.

### th...@google.com (2022-06-16)

Assigning Pri-1 to match with Impact and Severity flags

### rh...@gmail.com (2022-10-07)

hi,

This heap uaf is no longer crash on latest ToT version 108 or after commit https://chromium-review.googlesource.com/c/chromium/src/+/3466954. It seems oshima@ recently made change on ash/host/ash_window_tree_host_unified.cc. Please double check on your side ashleydp@.

Thanks

### rh...@gmail.com (2022-10-17)

hello,

any updates on this issue?

### al...@google.com (2022-12-06)

oshima@ can you confirm your CL fixes this issue?

### rh...@gmail.com (2023-01-09)

Sorry for the ping. Any chance I can get the update for the bug?

### os...@chromium.org (2023-01-24)

yes

### [Deleted User] (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### rh...@gmail.com (2023-02-03)

Thanks for the reward!

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1311885?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059254)*
