# Security: heap-buffer-overflow ui/wm/core/transient_window_stacking_client.cc (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059984](https://issues.chromium.org/issues/40059984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Aura |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2022-06-16 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug requires a crafted html to open YouTube videos and dual display. I also tested with empty browser but the crash didn't happened. So the crafted html plays a role to trigger crash.

When a window on second display spawned and enter overview mode then active screen recorder function on chromeOS, the ash/capture\_mode/capture\_mode\_session will record TransientWindowStackingClient[1] sizes. In order to trigger crash, after capture\_mode\_session actived, we need exit to the overview mode by pressing (F5) then the size of window will be different from original size and it caused Heap buffer overflow.

```
  if (\*direction == Window::STACK_ABOVE &&  
      !HasTransientAncestor(\*child, \*target)) {  
    const Window::Windows& siblings((\*child)->parent()->children());  
    size_t target_i =  
        std::find(siblings.begin(), siblings.end(), \*target) - siblings.begin();  
    while (target_i + 1 < siblings.size() &&  
           HasTransientAncestor(siblings[target_i + 1], \*target)) {  
      ++target_i;  
    }  
    \*target = siblings[target_i]; <-- here  
  }  

```

Looking the code above haven't maintained for long time, and maybe it's worth to take a look.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ui/wm/core/transient_window_stacking_client.cc;l=88-98?q=ui%2Fwm%2Fcore%2Ftransient_window_stacking_client.cc&ss=chromium%2Fchromium%2Fsrc>

**VERSION**  

Chrome Version: 105.0.5124.0 dev + stable  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

\*enable dual display  

(1) Navigate to <https://rhezashan.github.io/pocs/poc2.html>.  

(2) Click me and choose display 2.  

(3) Enter overview mode (F5) and open screen record function ALT + SHIFT + F5  

(4) This point is important, we need to exit the overview mode (F5) than press enter to record in same time.  

(5) Detach second display before screen recorder counter is over.

if it not crash, please remove the --user-data-dir then repeat from point 1-5

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==360793==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6020006f18b8 at pc 0x55f38bede9ca bp 0x7ffdb2cdbdf0 sp 0x7ffdb2cdbde8  

READ of size 8 at 0x6020006f18b8 thread T0 (chrome)  

SCARINESS: 23 (8-byte-read-heap-buffer-overflow)  

#0 0x55f38bede9c9 in wm::TransientWindowStackingClient::AdjustStacking(aura::Window\*\*, aura::Window\*\*, aura::Window::StackDirection\*) ui/wm/core/transient\_window\_stacking\_client.cc:97:15  

#1 0x55f38468738c in aura::Window::StackChildRelativeTo(aura::Window\*, aura::Window\*, aura::Window::StackDirection) ui/aura/window.cc:1087:25  

#2 0x55f384cb0fe1 in ash::CaptureModeSession::RefreshBarWidgetBounds() ash/capture\_mode/capture\_mode\_session.cc:1654:11  

#3 0x55f384cb0b56 in ash::CaptureModeSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ash/capture\_mode/capture\_mode\_session.cc:1251:3  

#4 0x55f3847d2e9e in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ui/display/manager/display\_manager.cc:2203:14  

#5 0x55f3847d344e in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ui/display/manager/display\_manager.cc:508:5  

#6 0x55f384fdd4d0 in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ash/shelf/shelf\_layout\_manager.cc:1680:17  

#7 0x55f384fde399 in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ash/shelf/shelf\_layout\_manager.cc:1385:3  

#8 0x55f384fd9070 in ash::ShelfLayoutManager::UpdateVisibilityState() ash/shelf/shelf\_layout\_manager.cc  

#9 0x55f3856a2a53 in UpdateShelfVisibility ash/wm/workspace/workspace\_layout\_manager.cc:543:37  

#10 0x55f3856a2a53 in ash::WorkspaceLayoutManager::OnWindowAddedToLayout(aura::Window\*) ash/wm/workspace/workspace\_layout\_manager.cc:156:3  

#11 0x55f384687d35 in aura::Window::AddChild(aura::Window\*) ui/aura/window.cc:550:22  

#12 0x55f384f4acbf in ReparentWindow ash/root\_window\_controller.cc:217:15  

#13 0x55f384f4acbf in ReparentAllWindows ash/root\_window\_controller.cc:281:7  

#14 0x55f384f4acbf in ash::RootWindowController::MoveWindowsTo(aura::Window\*) ash/root\_window\_controller.cc:749:3  

#15 0x55f384d9a41a in ash::WindowTreeHostManager::DeleteHost(ash::AshWindowTreeHost\*) ash/display/window\_tree\_host\_manager.cc:601:15  

#16 0x55f384d9adfd in ash::WindowTreeHostManager::OnDisplayRemoved(display::Display const&) ash/display/window\_tree\_host\_manager.cc:655:3  

#17 0x55f3847dc62a in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display\_manager.cc:2213:14  

#18 0x55f3847d61ae in display::DisplayManager::UpdateDisplaysWith(std::Cr::vector<display::ManagedDisplayInfo, std::Cr::allocator[display::ManagedDisplayInfo](javascript:void(0);)> const&) ui/display/manager/display\_manager.cc:1054:5  

#19 0x55f3847df0a0 in display::DisplayManager::AddRemoveDisplay(std::Cr::vector<display::ManagedDisplayMode, std::Cr::allocator[display::ManagedDisplayMode](javascript:void(0);)>) ui/display/manager/display\_manager.cc:1439:3  

#20 0x55f384b68664 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2159:40  

#21 0x55f384b68f57 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1729:3  

#22 0x55f384a48eec in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#23 0x55f384a48eec in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#24 0x55f38506788f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#25 0x55f38116ec19 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#26 0x55f38116e93d in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#27 0x55f38116df9f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#28 0x55f38116dc26 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#29 0x55f38116d9b6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#30 0x55f3846a7469 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#31 0x55f3846be42c in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:373:23  

#32 0x55f3819e9ec7 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#33 0x55f381b3871d in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:614:38  

#34 0x55f381b37f7e in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#35 0x55f3846a1f5f in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#36 0x55f3846a0906 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#37 0x55f38116d966 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#38 0x55f3846a7469 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#39 0x55f3846b8327 in aura::WindowTargeter::ProcessEventIfTargetsDifferentRootWindow(aura::Window\*, aura::Window\*, ui::Event\*) ui/aura/window\_targeter.cc:178:54  

#40 0x55f3846b8491 in aura::WindowTargeter::FindTargetForEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_targeter.cc:189:7  

#41 0x55f3846a73d1 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc  

#42 0x55f38117237e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#43 0x55f381172876 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#44 0x55f381170fcb in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#45 0x55f3746c5310 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::Cr::unique\_ptr<ui::Event, std::Cr::default\_delete[ui::Event](javascript:void(0);)>, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc  

#46 0x55f3746c3437 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:752:12  

#47 0x55f381172826 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#48 0x55f381170fcb in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#49 0x55f384db5860 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#50 0x55f381172826 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#51 0x55f381170fcb in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#52 0x55f384db1846 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#53 0x55f381172021 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#54 0x55f384dec60f in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#55 0x55f384df3bd8 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:207:40  

#56 0x55f3811806df in Run base/callback.h:143:12  

#57 0x55f3811806df in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:28:25  

#58 0x55f37176f6a1 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1342:3  

#59 0x55f37176eef3 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1295:3  

#60 0x55f37176f9dc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#61 0x55f381117829 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#62 0x55f38188c41f in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#63 0x55f371381da5 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#64 0x55f371381ab3 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#65 0x55f371381583 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#66 0x55f381895333 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#67 0x55f37eeb8cba in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#68 0x55f37f1d629b in event\_process\_active base/third\_party/libevent/event.c:381:4  

#69 0x55f37f1d629b in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#70 0x55f37eeb95d6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#71 0x55f37edb0ad0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:535:12  

#72 0x55f37ecdd26f in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#73 0x55f3753e5682 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1039:18  

#74 0x55f3753e9a6b in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#75 0x55f3753df88a in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#76 0x55f37eab0684 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#77 0x55f37eab31e5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#78 0x55f37eab263d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#79 0x55f37eaabf86 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#80 0x55f37eaad2f2 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#81 0x55f3703397c0 in ChromeMain chrome/app/chrome\_main.cc:177:12  

#82 0x7f1c1b250082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6020006f18b8 is located 0 bytes to the right of 8-byte region [0x6020006f18b0,0x6020006f18b8)  

allocated by thread T0 (chrome) here:  

#0 0x55f370336ffd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x55f384687ba2 in \_\_libcpp\_operator\_new<unsigned long> buildtools/third\_party/libc++/trunk/include/new:245:10  

#2 0x55f384687ba2 in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:271:10  

#3 0x55f384687ba2 in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:105:38  

#4 0x55f384687ba2 in allocate buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:262:20  

#5 0x55f384687ba2 in \_\_split\_buffer buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:322:29  

#6 0x55f384687ba2 in \_\_push\_back\_slow\_path<aura::Window \*const &> buildtools/third\_party/libc++/trunk/include/vector:1536:49  

#7 0x55f384687ba2 in push\_back buildtools/third\_party/libc++/trunk/include/vector:1553:9  

#8 0x55f384687ba2 in aura::Window::AddChild(aura::Window\*) ui/aura/window.cc:548:13  

#9 0x55f3856758e0 in ash::SetBoundsInScreen(aura::Window\*, gfx::Rect const&, display::Display const&) ash/wm/window\_positioning\_utils.cc:282:22  

#10 0x55f384b2338c in views::NativeWidgetAura::SetBounds(gfx::Rect const&) ui/views/widget/native\_widget\_aura.cc:535:31  

#11 0x55f384cb0f95 in ash::CaptureModeSession::RefreshBarWidgetBounds() ash/capture\_mode/capture\_mode\_session.cc:1651:29  

#12 0x55f384cb0b56 in ash::CaptureModeSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ash/capture\_mode/capture\_mode\_session.cc:1251:3  

#13 0x55f3847d2e9e in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ui/display/manager/display\_manager.cc:2203:14  

#14 0x55f3847d344e in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ui/display/manager/display\_manager.cc:508:5  

#15 0x55f384fdd4d0 in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ash/shelf/shelf\_layout\_manager.cc:1680:17  

#16 0x55f384fde399 in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ash/shelf/shelf\_layout\_manager.cc:1385:3  

#17 0x55f384fd9070 in ash::ShelfLayoutManager::UpdateVisibilityState() ash/shelf/shelf\_layout\_manager.cc  

#18 0x55f3856a2a53 in UpdateShelfVisibility ash/wm/workspace/workspace\_layout\_manager.cc:543:37  

#19 0x55f3856a2a53 in ash::WorkspaceLayoutManager::OnWindowAddedToLayout(aura::Window\*) ash/wm/workspace/workspace\_layout\_manager.cc:156:3  

#20 0x55f384687d35 in aura::Window::AddChild(aura::Window\*) ui/aura/window.cc:550:22  

#21 0x55f384f4acbf in ReparentWindow ash/root\_window\_controller.cc:217:15  

#22 0x55f384f4acbf in ReparentAllWindows ash/root\_window\_controller.cc:281:7  

#23 0x55f384f4acbf in ash::RootWindowController::MoveWindowsTo(aura::Window\*) ash/root\_window\_controller.cc:749:3  

#24 0x55f384d9a41a in ash::WindowTreeHostManager::DeleteHost(ash::AshWindowTreeHost\*) ash/display/window\_tree\_host\_manager.cc:601:15  

#25 0x55f384d9adfd in ash::WindowTreeHostManager::OnDisplayRemoved(display::Display const&) ash/display/window\_tree\_host\_manager.cc:655:3  

#26 0x55f3847dc62a in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display\_manager.cc:2213:14  

#27 0x55f3847d61ae in display::DisplayManager::UpdateDisplaysWith(std::Cr::vector<display::ManagedDisplayInfo, std::Cr::allocator[display::ManagedDisplayInfo](javascript:void(0);)> const&) ui/display/manager/display\_manager.cc:1054:5  

#28 0x55f3847df0a0 in display::DisplayManager::AddRemoveDisplay(std::Cr::vector<display::ManagedDisplayMode, std::Cr::allocator[display::ManagedDisplayMode](javascript:void(0);)>) ui/display/manager/display\_manager.cc:1439:3  

#29 0x55f384b68664 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2159:40  

#30 0x55f384b68f57 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1729:3  

#31 0x55f384a48eec in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#32 0x55f384a48eec in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#33 0x55f38506788f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#34 0x55f38116ec19 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#35 0x55f38116e93d in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);)>\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#36 0x55f38116df9f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#37 0x55f38116dc26 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#38 0x55f38116d9b6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#39 0x55f3846a7469 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#40 0x55f3846be42c in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:373:23

SUMMARY: AddressSanitizer: heap-buffer-overflow ui/wm/core/transient\_window\_stacking\_client.cc:97:15 in wm::TransientWindowStackingClient::AdjustStacking(aura::Window\*\*, aura::Window\*\*, aura::Window::StackDirection\*)  

Shadow bytes around the buggy address:  

0x0c04800d62c0: fa fa 00 00 fa fa fd fa fa fa fd fd fa fa 00 00  

0x0c04800d62d0: fa fa fd fd fa fa fd fd fa fa 00 00 fa fa fd fd  

0x0c04800d62e0: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa  

0x0c04800d62f0: fa fa fd fa fa fa fd fa fa fa 00 fa fa fa 00 fa  

0x0c04800d6300: fa fa 00 fa fa fa fd fa fa fa fa fa fa fa fa fa  

=>0x0c04800d6310: fa fa 00 fa fa fa 00[fa]fa fa 00 fa fa fa fd fa  

0x0c04800d6320: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800d6330: fa fa fd fa fa fa 00 fa fa fa 00 00 fa fa 00 00  

0x0c04800d6340: fa fa fd fd fa fa fd fa fa fa fd fd fa fa 00 00  

0x0c04800d6350: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c04800d6360: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

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

==360793==ABORTING

## Attachments

- [1336979_screencast.webm](attachments/1336979_screencast.webm) (video/webm, 4.8 MB)
- [1336979_patch_applied.webm](attachments/1336979_patch_applied.webm) (video/webm, 1.9 MB)
- [1336979.patch](attachments/1336979.patch) (text/plain, 880 B)
- [1336979_screencast_00013.webm](attachments/1336979_screencast_00013.webm) (video/webm, 5.3 MB)
- [1336979_versions_1017797.webm](attachments/1336979_versions_1017797.webm) (video/webm, 6.4 MB)

## Timeline

### rh...@gmail.com (2022-06-16)

uploading screencast 

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-16)

I also upload suggestion fix for this issue. It's not best approach to fix the issue but had no longer crashes.


### xi...@chromium.org (2022-06-16)

Thanks for the report! +sky@ based on git blame. Thanks! 

[Monorail components: Internals>Aura UI>Shell>ScreenCapture]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### af...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3

commit b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3
Author: Scott Violet <sky@chromium.org>
Date: Thu Jun 23 19:30:22 2022

ash: ensure CaptureModeSession updates state when display removed

CaptureModeSession maintains state per display. When the display
is removed CaptureModeSession needs to update internal state. In
order to update the state CaptureModeSession makes use of the root
Window of the display being removed.

This moves updating state to before the display has actually been
removed (and ash has started removing state). In order to do this
ShellObserver gets a new function that is called when displays
will be removed, but before they have actually been removed.

BUG=1336979

Change-Id: I1e198e6c23eb2108ea3c541ad84d1fa9bf918b08
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3719239
Reviewed-by: Ahmed Fakhry <afakhry@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1017298}

[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/shell.h
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/capture_mode/capture_mode_unittests.cc
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/display/window_tree_host_manager.h
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/capture_mode/capture_mode_session.h
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/shell_observer.h
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/shell.cc
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/capture_mode/capture_mode_session.cc
[modify] https://crrev.com/b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3/ash/root_window_controller.cc


### sk...@chromium.org (2022-06-23)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-23)

Thank you for quick fix.

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

Requesting merge to extended stable M102 because latest trunk commit (1017298) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1017298) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1017298) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

Merge review required: M103 is already shipping to stable.

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

### [Deleted User] (2022-06-24)

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

### sk...@chromium.org (2022-06-24)

To trigger this requires removing a monitor at a specific time. This is *extremely* rare. Is it really worth merging this?

### rh...@gmail.com (2022-06-24)

>> To trigger this requires removing a monitor at a specific time. This is *extremely* rare. Is it really worth merging this?
FYI: Sorry, from my perspective it's not about detaching second display at a specific time. The necessary step to trigger this need to exit the overview mode (F5) and then press enter to record simultaneously.

For example, I retested on the same version as on comment https://crbug.com/chromium/1336979#c0, and got a crash when the counter time was 2 seconds, while the video in https://crbug.com/chromium/1336979#c1 was in 1 second.

Hope this helps


### rh...@gmail.com (2022-06-24)

I also can confirm the CL in https://crbug.com/chromium/1336979#c9 is not complete fix this issue. I tested on 1017797 the heap buffer overflow is still there.

### sk...@chromium.org (2022-06-24)

Ah, ok. In that case there is likely two bugs here. Reopenning.

### rh...@gmail.com (2022-06-24)

Thanks for looking into this issue and sorry didn't mean to give extra works on Friday.

### sk...@chromium.org (2022-06-28)

rhezashan, can you past the stack of the crash you get?

### rh...@gmail.com (2022-06-29)

here's the stack trace from the crash
=================================================================
==393213==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000436df8 at pc 0x55bab25ad66a bp 0x7ffc78de7630 sp 0x7ffc78de7628
READ of size 8 at 0x602000436df8 thread T0 (chrome)
SCARINESS: 23 (8-byte-read-heap-buffer-overflow)
2022-06-28T23:58:43.292170Z ERROR chrome[393213:393228]: [object_proxy.cc(623)] Failed to call method: org.chromium.debugd.GetPerfOutputV2: object_path= /org/chromium/debugd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.debugd was not provided by any .service files
    #0 0x55bab25ad669 in wm::TransientWindowStackingClient::AdjustStacking(aura::Window**, aura::Window**, aura::Window::StackDirection*) ui/wm/core/transient_window_stacking_client.cc:97:15
    #1 0x55baaade254c in aura::Window::StackChildRelativeTo(aura::Window*, aura::Window*, aura::Window::StackDirection) ui/aura/window.cc:1087:25
    #2 0x55baab40d56b in ash::CaptureModeSession::RefreshBarWidgetBounds() ash/capture_mode/capture_mode_session.cc:1662:11
    #3 0x55baab40d0e0 in ash::CaptureModeSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ash/capture_mode/capture_mode_session.cc:1259:3
    #4 0x55baaaf2e91c in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ui/display/manager/display_manager.cc:2203:14
    #5 0x55baaaf2eecc in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ui/display/manager/display_manager.cc:508:5
    #6 0x55baab7398c0 in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ash/shelf/shelf_layout_manager.cc:1689:17
    #7 0x55baab73a789 in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ash/shelf/shelf_layout_manager.cc:1394:3
    #8 0x55baab735460 in ash::ShelfLayoutManager::UpdateVisibilityState() ash/shelf/shelf_layout_manager.cc
    #9 0x55baabe04f7b in UpdateShelfVisibility ash/wm/workspace/workspace_layout_manager.cc:543:37
    #10 0x55baabe04f7b in ash::WorkspaceLayoutManager::OnWindowAddedToLayout(aura::Window*) ash/wm/workspace/workspace_layout_manager.cc:156:3
    #11 0x55baaade2ef5 in aura::Window::AddChild(aura::Window*) ui/aura/window.cc:550:22
    #12 0x55baab6a7547 in ReparentWindow ash/root_window_controller.cc:217:15
    #13 0x55baab6a7547 in ReparentAllWindows ash/root_window_controller.cc:281:7
    #14 0x55baab6a7547 in ash::RootWindowController::MoveWindowsTo(aura::Window*) ash/root_window_controller.cc:751:3
    #15 0x55baab4f6d80 in ash::WindowTreeHostManager::DeleteHost(ash::AshWindowTreeHost*) ash/display/window_tree_host_manager.cc:601:15
    #16 0x55baab4f7763 in ash::WindowTreeHostManager::OnDisplayRemoved(display::Display const&) ash/display/window_tree_host_manager.cc:655:3
    #17 0x55baaaf3808e in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display_manager.cc:2213:14
    #18 0x55baaaf31c18 in display::DisplayManager::UpdateDisplaysWith(std::Cr::vector<display::ManagedDisplayInfo, std::Cr::allocator<display::ManagedDisplayInfo>> const&) ui/display/manager/display_manager.cc:1054:5
    #19 0x55baaaf3ab0f in display::DisplayManager::AddRemoveDisplay(std::Cr::vector<display::ManagedDisplayMode, std::Cr::allocator<display::ManagedDisplayMode>>) ui/display/manager/display_manager.cc:1439:3
    #20 0x55baab2c4202 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2096:40
    #21 0x55baab2c4af5 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1666:3
    #22 0x55baab1a4e8c in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #23 0x55baab1a4e8c in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #24 0x55baab7c4eaf in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent*) ui/wm/core/accelerator_filter.cc:51:18
    #25 0x55baa78c7109 in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #26 0x55baa78c6e2d in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler*, std::Cr::allocator<ui::EventHandler*>>*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #27 0x55baa78c648f in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #28 0x55baa78c6116 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #29 0x55baa78c5ea6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #30 0x55baaae02629 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #31 0x55baaae195ec in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:373:23
    #32 0x55baa814dee7 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent*) const ui/base/ime/input_method_base.cc:140:33
    #33 0x55baa829c7ad in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:617:38
    #34 0x55baa829c00e in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/ash/input_method_ash.cc:139:14
    #35 0x55baaadfd11f in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1080:54
    #36 0x55baaadfbac6 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:568:15
    #37 0x55baa78c5e56 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #38 0x55baaae02629 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #39 0x55baaae134e7 in aura::WindowTargeter::ProcessEventIfTargetsDifferentRootWindow(aura::Window*, aura::Window*, ui::Event*) ui/aura/window_targeter.cc:178:54
    #40 0x55baaae13651 in aura::WindowTargeter::FindTargetForEvent(ui::EventTarget*, ui::Event*) ui/aura/window_targeter.cc:189:7
    #41 0x55baaae02591 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc
    #42 0x55baa78ca86e in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #43 0x55baa78cad66 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14
    #44 0x55baa78c94bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #45 0x55ba9adbe898 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::Cr::unique_ptr<ui::Event, std::Cr::default_delete<ui::Event>>, ui::EventRewriteStatus, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc
    #46 0x55ba9adbca07 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ui/chromeos/events/event_rewriter_chromeos.cc:752:12
    #47 0x55baa78cad16 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #48 0x55baa78c94bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #49 0x55baab5121d0 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/keyboard_driven_event_rewriter.cc:31:12
    #50 0x55baa78cad16 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:67:32
    #51 0x55baa78c94bb in ui::EventRewriter::SendEvent(base::WeakPtr<ui::EventRewriterContinuation>, ui::Event const*) ui/events/event_rewriter.cc:88:39
    #52 0x55baab50e1b6 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr<ui::EventRewriterContinuation>) ash/events/accessibility_event_rewriter.cc
    #53 0x55baa78ca511 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:144:29
    #54 0x55baab548f6f in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:229:38
    #55 0x55baab550538 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event*) ash/host/ash_window_tree_host_platform.cc:207:40
    #56 0x55baa78d8bcf in Run base/callback.h:143:12
    #57 0x55baa78d8bcf in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:28:25
    #58 0x55ba97d55c9b in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/ozone/platform/x11/x11_window.cc:1361:3
    #59 0x55ba97d554ed in ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc:1314:3
    #60 0x55ba97d55fd6 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc
    #61 0x55baa78701b9 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:99:29
    #62 0x55baa7fefcaf in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #63 0x55ba97966283 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14
    #64 0x55ba97965f91 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3
    #65 0x55ba97965a61 in x11::Connection::Dispatch() ui/gfx/x/connection.cc
    #66 0x55baa7ff8bb3 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11_event_watcher_fdwatch.cc:64:15
    #67 0x55baa56143e9 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void*) base/message_loop/message_pump_libevent.cc
    #68 0x55baa593cddb in event_process_active third_party/libevent/event.c:381:4
    #69 0x55baa593cddb in event_base_loop third_party/libevent/event.c:521:4
    #70 0x55baa5614d4b in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:220:5
    #71 0x55baa550d700 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:554:12
    #72 0x55baa543967f in base::RunLoop::Run(base::Location const&) base/run_loop.cc:141:14
    #73 0x55ba9baf0852 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1036:18
    #74 0x55ba9baf4c3b in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:157:15
    #75 0x55ba9baeaa4a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #76 0x55baa520b074 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:678:10
    #77 0x55baa520dbd5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1188:10
    #78 0x55baa520d02d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1059:12
    #79 0x55baa5206976 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:407:36
    #80 0x55baa5207ce2 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:435:10
    #81 0x55ba96947110 in ChromeMain chrome/app/chrome_main.cc:182:12
    #82 0x7f2250f1d082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x602000436df8 is located 0 bytes to the right of 8-byte region [0x602000436df0,0x602000436df8)
allocated by thread T0 (chrome) here:
    #0 0x55ba9694494d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55baaade2d62 in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:245:10
    #2 0x55baaade2d62 in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:271:10
    #3 0x55baaade2d62 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:105:38
    #4 0x55baaade2d62 in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:262:20
    #5 0x55baaade2d62 in __split_buffer buildtools/third_party/libc++/trunk/include/__split_buffer:322:29
    #6 0x55baaade2d62 in __push_back_slow_path<aura::Window *const &> buildtools/third_party/libc++/trunk/include/vector:1536:49
    #7 0x55baaade2d62 in push_back buildtools/third_party/libc++/trunk/include/vector:1553:9
    #8 0x55baaade2d62 in aura::Window::AddChild(aura::Window*) ui/aura/window.cc:548:13
    #9 0x55baabdd7c60 in ash::SetBoundsInScreen(aura::Window*, gfx::Rect const&, display::Display const&) ash/wm/window_positioning_utils.cc:282:22
    #10 0x55baab27f3fc in views::NativeWidgetAura::SetBounds(gfx::Rect const&) ui/views/widget/native_widget_aura.cc:535:31
    #11 0x55baab40d51f in ash::CaptureModeSession::RefreshBarWidgetBounds() ash/capture_mode/capture_mode_session.cc:1659:29
    #12 0x55baab40d0e0 in ash::CaptureModeSession::OnDisplayMetricsChanged(display::Display const&, unsigned int) ash/capture_mode/capture_mode_session.cc:1259:3
    #13 0x55baaaf2e91c in display::DisplayManager::NotifyMetricsChanged(display::Display const&, unsigned int) ui/display/manager/display_manager.cc:2203:14
    #14 0x55baaaf2eecc in display::DisplayManager::UpdateWorkAreaOfDisplay(long, gfx::Insets const&) ui/display/manager/display_manager.cc:508:5
    #15 0x55baab7398c0 in ash::ShelfLayoutManager::UpdateBoundsAndOpacity(bool) ash/shelf/shelf_layout_manager.cc:1689:17
    #16 0x55baab73a789 in ash::ShelfLayoutManager::SetState(ash::ShelfVisibilityState) ash/shelf/shelf_layout_manager.cc:1394:3
    #17 0x55baab735460 in ash::ShelfLayoutManager::UpdateVisibilityState() ash/shelf/shelf_layout_manager.cc
    #18 0x55baabe04f7b in UpdateShelfVisibility ash/wm/workspace/workspace_layout_manager.cc:543:37
    #19 0x55baabe04f7b in ash::WorkspaceLayoutManager::OnWindowAddedToLayout(aura::Window*) ash/wm/workspace/workspace_layout_manager.cc:156:3
    #20 0x55baaade2ef5 in aura::Window::AddChild(aura::Window*) ui/aura/window.cc:550:22
    #21 0x55baab6a7547 in ReparentWindow ash/root_window_controller.cc:217:15
    #22 0x55baab6a7547 in ReparentAllWindows ash/root_window_controller.cc:281:7
    #23 0x55baab6a7547 in ash::RootWindowController::MoveWindowsTo(aura::Window*) ash/root_window_controller.cc:751:3
    #24 0x55baab4f6d80 in ash::WindowTreeHostManager::DeleteHost(ash::AshWindowTreeHost*) ash/display/window_tree_host_manager.cc:601:15
    #25 0x55baab4f7763 in ash::WindowTreeHostManager::OnDisplayRemoved(display::Display const&) ash/display/window_tree_host_manager.cc:655:3
    #26 0x55baaaf3808e in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display_manager.cc:2213:14
    #27 0x55baaaf31c18 in display::DisplayManager::UpdateDisplaysWith(std::Cr::vector<display::ManagedDisplayInfo, std::Cr::allocator<display::ManagedDisplayInfo>> const&) ui/display/manager/display_manager.cc:1054:5
    #28 0x55baaaf3ab0f in display::DisplayManager::AddRemoveDisplay(std::Cr::vector<display::ManagedDisplayMode, std::Cr::allocator<display::ManagedDisplayMode>>) ui/display/manager/display_manager.cc:1439:3
    #29 0x55baab2c4202 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:2096:40
    #30 0x55baab2c4af5 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator_controller_impl.cc:1666:3
    #31 0x55baab1a4e8c in TryProcess ui/base/accelerators/accelerator_manager.cc:153:17
    #32 0x55baab1a4e8c in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator_manager.cc:83:27
    #33 0x55baab7c4eaf in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent*) ui/wm/core/accelerator_filter.cc:51:18
    #34 0x55baa78c7109 in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #35 0x55baa78c6e2d in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler*, std::Cr::allocator<ui::EventHandler*>>*, ui::Event*) ui/events/event_dispatcher.cc:177:7
    #36 0x55baa78c648f in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:125:3
    #37 0x55baa78c6116 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #38 0x55baa78c5ea6 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #39 0x55baaae02629 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #40 0x55baaae195ec in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent*) ui/aura/window_tree_host.cc:373:23

SUMMARY: AddressSanitizer: heap-buffer-overflow ui/wm/core/transient_window_stacking_client.cc:97:15 in wm::TransientWindowStackingClient::AdjustStacking(aura::Window**, aura::Window**, aura::Window::StackDirection*)
Shadow bytes around the buggy address:
  0x0c048007ed60: fa fa 00 fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c048007ed70: fa fa 00 fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c048007ed80: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x0c048007ed90: fa fa fd fd fa fa fd fa fa fa fd fd fa fa 00 fa
  0x0c048007eda0: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa
=>0x0c048007edb0: fa fa fa fa fa fa 00 fa fa fa fa fa fa fa 00[fa]
  0x0c048007edc0: fa fa 00 fa fa fa 00 fa fa fa fd fa fa fa fd fa
  0x0c048007edd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048007ede0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048007edf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048007ee00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==393213==ABORTING


### dg...@google.com (2022-06-29)

Once a fix is ready, please provide the info requested in https://crbug.com/chromium/1336979#c15 for release branch merge review. Thanks

### sk...@chromium.org (2022-06-29)

rhezashan@gmail.com, are you sure that is the stack trace without removing a display? The stack trace indicates a display is being removed.

Also, what are the exact sequence you are doing when not removing a display?

### rh...@gmail.com (2022-06-29)

sky@,

Sorry but I didn't say without removing second display. From repro steps in https://crbug.com/chromium/1336979#c0,  it requires remove second display at the end. 

REPRODUCTION CASE
*enable dual display
(1) Navigate to https://rhezashan.github.io/pocs/poc2.html.
(2) Click me and choose display 2.
(3) Enter overview mode (F5) and open screen record function ALT + SHIFT + F5
(4) This point is important, we need to exit the overview mode (F5) than press enter to record in same time.
(5) Detach second display before screen recorder counter is over.

It was hard to give the visibility by words but my assumption:
(1) after https://rhezashan.github.io/pocs/poc2.html and then click to display 2.
(2) enter overview mode (F5) then call screencapture functions, in this time CaptureModeSession record overview screen then next hit F5 to exit overview mode. Then the CaptureModeSession didn't catch the refresh state between CaptureModeSession with exit/enter overview mode (F5). Detach the second display then the  aura::Window::StackChildRelativeTo got buffer overflow. Please see screencast on comment https://crbug.com/chromium/1336979#c19 at time 00:11 - 00:18

I also provided unsophisticated codes to fix this issue and no crash happened after the patch applied with that codes on https://crbug.com/chromium/1336979#c3.

### gi...@appspot.gserviceaccount.com (2022-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2

commit ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2
Author: Scott Violet <sky@chromium.org>
Date: Thu Jun 30 23:16:16 2022

ash: change when OnRootWindowWillShutdown() is called

This moves OnRootWindowWillShutdown() to be called before windows
are moved from the display being removed. This is important as moving
windows may trigger display metrics to change, which would then be sent
before OnRootWindowWillShutdown(). Having OnRootWindowWillShutdown()
called before OnDisplayMetricsChanged() is important for capture
mode as it maintains state per root window, so that if it receives
OnDisplayMetricsChanged() part way through, it gets confused
(leading to crashing).

BUG=1336979
TEST=covered by test

Change-Id: I66e83d7ba3e6a37b4e2b8f74b494119b5e43a99d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736777
Commit-Queue: Scott Violet <sky@chromium.org>
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019873}

[modify] https://crrev.com/ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2/ash/capture_mode/capture_mode_unittests.cc
[modify] https://crrev.com/ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2/ash/display/window_tree_host_manager.cc
[modify] https://crrev.com/ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2/ash/root_window_controller.cc


### sk...@chromium.org (2022-06-30)

Ok, I'm hoping latest patch truly fixes this. As triggering this requires removing a display at a particular point I don't think this needs to be merged.

### dg...@google.com (2022-07-06)

Marking merge-rejected for all channels per https://crbug.com/chromium/1336979#c29

### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report + $1,000 bonus for a total of $3,000. The original amount was decided on due to these issues being not web accessible and are substantially mitigated information disclosure bugs. We wanted to provide a $1,000 reward for you testing the patch and informing us this issue was not resolved after the initial patch. We greatly appreciate your efforts and reporting these issues to us! 

### rh...@gmail.com (2022-07-07)

Thanks amy@ and developers

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-01)

 gmpritchard, the bot isn't adding the questionnaire, but here are the answers:

1. Just https://crrev.com/c/3865496
2. Low, one minor conflict with a call that isn't present in 102
3. 105
4. Yes

### gm...@google.com (2022-09-06)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ffb8880a88ec185d7140d3220599c8c6530e2a6

commit 8ffb8880a88ec185d7140d3220599c8c6530e2a6
Author: Scott Violet <sky@chromium.org>
Date: Mon Sep 12 16:03:27 2022

[M102-LTS] ash: ensure CaptureModeSession updates state when display removed

M102 merge issues:
  ash/capture_mode/capture_mode_session.cc:
    user_nudge_controller_.reset() isn't called in Shutdown() on M102

CaptureModeSession maintains state per display. When the display
is removed CaptureModeSession needs to update internal state. In
order to update the state CaptureModeSession makes use of the root
Window of the display being removed.

This moves updating state to before the display has actually been
removed (and ash has started removing state). In order to do this
ShellObserver gets a new function that is called when displays
will be removed, but before they have actually been removed.

BUG=1336979

(cherry picked from commit b4c5cebd4e25f4a1aa6cab2ba04c886d53d562a3)

Change-Id: I1e198e6c23eb2108ea3c541ad84d1fa9bf918b08
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3719239
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1017298}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865496
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1341}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/shell.h
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/capture_mode/capture_mode_unittests.cc
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/display/window_tree_host_manager.h
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/capture_mode/capture_mode_session.h
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/shell_observer.h
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/shell.cc
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/capture_mode/capture_mode_session.cc
[modify] https://crrev.com/8ffb8880a88ec185d7140d3220599c8c6530e2a6/ash/root_window_controller.cc


### rz...@google.com (2022-09-13)

Requesting merge again because I skipped one CL

### [Deleted User] (2022-09-13)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-13)

1. https://crrev.com/c/3893851
2. 105
3. Low, no conflicts
4. Yes

### gm...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a48ab4117673f7f9499bb6f07536d38cecff4360

commit a48ab4117673f7f9499bb6f07536d38cecff4360
Author: Scott Violet <sky@chromium.org>
Date: Wed Sep 14 13:24:39 2022

[M102-LTS] ash: change when OnRootWindowWillShutdown() is called

This moves OnRootWindowWillShutdown() to be called before windows
are moved from the display being removed. This is important as moving
windows may trigger display metrics to change, which would then be sent
before OnRootWindowWillShutdown(). Having OnRootWindowWillShutdown()
called before OnDisplayMetricsChanged() is important for capture
mode as it maintains state per root window, so that if it receives
OnDisplayMetricsChanged() part way through, it gets confused
(leading to crashing).

BUG=1336979
TEST=covered by test

(cherry picked from commit ea26a2069d84e01c96e0bf5df8abb2b0b4b8efb2)

Change-Id: I66e83d7ba3e6a37b4e2b8f74b494119b5e43a99d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736777
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1019873}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3893851
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1351}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/a48ab4117673f7f9499bb6f07536d38cecff4360/ash/capture_mode/capture_mode_unittests.cc
[modify] https://crrev.com/a48ab4117673f7f9499bb6f07536d38cecff4360/ash/display/window_tree_host_manager.cc
[modify] https://crrev.com/a48ab4117673f7f9499bb6f07536d38cecff4360/ash/root_window_controller.cc


### rz...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-21)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1336979?no_tracker_redirect=1

[Multiple monorail components: Internals>Aura, UI>Shell>ScreenCapture]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059984)*
