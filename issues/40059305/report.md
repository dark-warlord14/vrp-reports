# Security: heap-buffer-overflow on ash/wm/window_animations.cc (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059305](https://issues.chromium.org/issues/40059305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Cast |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | zx...@chromium.org |
| **Created** | 2022-04-06 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

The issue needs dual virtual display on linux-chromeos, enable --ash-dev-shortcuts from command line

**VERSION**  

Chrome Version: 102.0.4988.0 + dev  

Operating System: chromeOS on linux-chromeOS

**REPRODUCTION CASE**  

Host poc3.html with python3 http.server

(1) Click me on button in display one and select display 2.  

(2) Wait until browser on display 1 closes then hit F5 (overview)  

(3) Detach second display

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==121448==ERROR: AddressSanitizer: heap-use-after-free on address 0x6180001cf5f0 at pc 0x559eb06fbf6d bp 0x7ffeaa999ca0 sp 0x7ffeaa999c98  

READ of size 8 at 0x6180001cf5f0 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x559eb06fbf6c in operator bool base/memory/scoped\_refptr.h:261:43  

#1 0x559eb06fbf6c in ui::Layer::GetAnimator() ui/compositor/layer.cc:473:8  

#2 0x559eb15c48b7 in ash::(anonymous namespace)::CrossFadeAnimationInternal(aura::Window\*, std::\_\_1::unique\_ptr<ui::LayerTreeOwner, std::\_\_1::default\_delete[ui::LayerTreeOwner](javascript:void(0);) >, bool, absl::optional[base::TimeDelta](javascript:void(0);), absl::optional[gfx::Tween::Type](javascript:void(0);), absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >) ash/wm/window\_animations.cc:355:58  

#3 0x559eb15c3aee in ash::CrossFadeAnimation(aura::Window\*, std::\_\_1::unique\_ptr<ui::LayerTreeOwner, std::\_\_1::default\_delete[ui::LayerTreeOwner](javascript:void(0);) >) ash/wm/window\_animations.cc:607:3  

#4 0x559eb15f5234 in ash::WindowState::SetBoundsDirectCrossFade(gfx::Rect const&) ash/wm/window\_state.cc:919:3  

#5 0x559eb16018c1 in ash::DefaultState::UpdateBoundsFromState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:590:19  

#6 0x559eb16010c9 in ash::DefaultState::EnterToNextState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:462:5  

#7 0x559eb1600af8 in ash::DefaultState::HandleTransitionEvents(ash::WindowState\*, ash::WMEvent const\*) ash/wm/default\_state.cc:376:3  

#8 0x559eb15f3b97 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:435:19  

#9 0x559eb15fbb0e in ash::WindowState::OnWindowPropertyChanged(aura::Window\*, void const\*, long) ash/wm/window\_state.cc:1090:7  

#10 0x559eb069990c in aura::Window::AfterPropertyChange(void const\*, long) ui/aura/window.cc:949:14  

#11 0x559eac7f438a in ui::PropertyHandler::SetPropertyInternal(void const\*, char const\*, void (\*)(long), long, long) ui/base/class\_property.cc:43:3  

#12 0x559eb067e9ce in void ui::subtle::PropertyHelper::Set[ui::WindowShowState](javascript:void(0);)(ui::PropertyHandler\*, ui::ClassProperty[ui::WindowShowState](javascript:void(0);) const\*, ui::WindowShowState) ui/base/class\_property.h:204:28  

#13 0x559eb0b56c73 in wm::SetWindowFullscreen(aura::Window\*, bool) ui/wm/core/window\_util.cc:119:13  

#14 0x559eb0ae7282 in views::Widget::SetFullscreen(bool, base::TimeDelta, long) ui/views/widget/widget.cc:819:19  

#15 0x559eb614b077 in media\_router::WiredDisplayMediaRouteProvider::OnDisplayRemoved(display::Display const&) chrome/browser/media/router/providers/wired\_display/wired\_display\_media\_route\_provider.cc:263:28  

#16 0x559eb07e6405 in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display\_manager.cc:2201:14  

#17 0x559eb07e0134 in display::DisplayManager::UpdateDisplaysWith(std::\_\_1::vector<display::ManagedDisplayInfo, std::\_\_1::allocator[display::ManagedDisplayInfo](javascript:void(0);) > const&) ui/display/manager/display\_manager.cc:1053:5  

#18 0x559eb07e8d0e in display::DisplayManager::AddRemoveDisplay(std::\_\_1::vector<display::ManagedDisplayMode, std::\_\_1::allocator[display::ManagedDisplayMode](javascript:void(0);) >) ui/display/manager/display\_manager.cc:1438:3  

#19 0x559eb0b72286 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2131:40  

#20 0x559eb0b72b91 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1705:3  

#21 0x559eb0a4483e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#22 0x559eb0a4483e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#23 0x559eb103cd9f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#24 0x559eacff3b6b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#25 0x559eacff3959 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_1::vector<ui::EventHandler\*, std::\_\_1::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#26 0x559eacff2f7d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#27 0x559eacff2c04 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#28 0x559eacff2970 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#29 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#30 0x559eb06cb046 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:375:23  

#31 0x559ead848711 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#32 0x559ead98c0e9 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:616:38  

#33 0x559ead98b949 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#34 0x559eb06af309 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#35 0x559eb06adcfe in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#36 0x559eacff2924 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#37 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#38 0x559eacff713e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#39 0x559eacff7636 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#40 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#41 0x559ea0b5d419 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc  

#42 0x559ea0b5b559 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#43 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#44 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#45 0x559eb0d9bbb0 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#46 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#47 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#48 0x559eb0d9781a in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#49 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#50 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#51 0x559eb0b901de in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#52 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#53 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#54 0x559eb0b9df19 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#55 0x559eacff6de6 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#56 0x559eb0dd14bf in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#57 0x559eb0dd89c2 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:202:40  

#58 0x559ead00176f in Run base/callback.h:142:12  

#59 0x559ead00176f in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:28:25  

#60 0x559e9ded9ea7 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1292:3  

#61 0x559e9ded96fd in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1245:3  

#62 0x559e9deda1f8 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#63 0x559eacf9f661 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#64 0x559ead6e4bb7 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#65 0x559e9db14103 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#66 0x559e9db13e2d in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#67 0x559e9db138f3 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#68 0x559ead6edc13 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#69 0x559eaaf445a5 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#70 0x559eab2a2d0c in event\_process\_active base/third\_party/libevent/event.c:381:4  

#71 0x559eab2a2d0c in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#72 0x559eaaf44d7d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#73 0x559eaae3e5fa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:498:12  

#74 0x559eaad732fc in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#75 0x559ea15b310a in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1067:18  

#76 0x559ea15b75f1 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:155:15  

#77 0x559ea15ad2ea in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#78 0x559eaab5089f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:640:10  

#79 0x559eaab533ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1147:10  

#80 0x559eaab52838 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1019:12  

#81 0x559eaab4d001 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#82 0x559eaab4d688 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#83 0x559e9c733c3a in ChromeMain chrome/app/chrome\_main.cc:176:12  

#84 0x7f8ddc07e0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6180001cf5f0 is located 368 bytes inside of 776-byte region [0x6180001cf480,0x6180001cf788)  

freed by thread T0 (chrome) here:  

#0 0x559e9c731cbd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x559eb074d04b in ui::(anonymous namespace)::DeepDeleteLayers(ui::Layer\*) ui/compositor/layer\_tree\_owner.cc:22:3  

#2 0x559ea07c7954 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#3 0x559ea07c7954 in std::\_\_1::unique\_ptr<ui::LayerTreeOwner, std::\_\_1::default\_delete[ui::LayerTreeOwner](javascript:void(0);) >::reset(ui::LayerTreeOwner\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#4 0x559eb0733b4c in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ui/compositor/layer\_animation\_observer.cc:55:5  

#5 0x559eb07340c6 in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ui/compositor/layer\_animation\_observer.cc:89:13  

#6 0x559eb0737163 in ui::LayerAnimationSequence::NotifyEnded() ui/compositor/layer\_animation\_sequence.cc:290:14  

#7 0x559eb0742438 in ProgressAnimationToEnd ui/compositor/layer\_animator.cc:480:13  

#8 0x559eb0742438 in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ui/compositor/layer\_animator.cc:632:5  

#9 0x559eb073bbef in ui::LayerAnimator::StopAnimatingProperty(ui::LayerAnimationElement::AnimatableProperty) ui/compositor/layer\_animator.cc:372:5  

#10 0x559eb073c793 in ui::LayerAnimator::SetOpacity(float) ui/compositor/layer\_animator.cc:114:1  

#11 0x559eb15c44da in ash::(anonymous namespace)::CrossFadeAnimationInternal(aura::Window\*, std::\_\_1::unique\_ptr<ui::LayerTreeOwner, std::\_\_1::default\_delete[ui::LayerTreeOwner](javascript:void(0);) >, bool, absl::optional[base::TimeDelta](javascript:void(0);), absl::optional[gfx::Tween::Type](javascript:void(0);), absl::optional<std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > >) ash/wm/window\_animations.cc:340:16  

#12 0x559eb15c3aee in ash::CrossFadeAnimation(aura::Window\*, std::\_\_1::unique\_ptr<ui::LayerTreeOwner, std::\_\_1::default\_delete[ui::LayerTreeOwner](javascript:void(0);) >) ash/wm/window\_animations.cc:607:3  

#13 0x559eb15f5234 in ash::WindowState::SetBoundsDirectCrossFade(gfx::Rect const&) ash/wm/window\_state.cc:919:3  

#14 0x559eb16018c1 in ash::DefaultState::UpdateBoundsFromState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:590:19  

#15 0x559eb16010c9 in ash::DefaultState::EnterToNextState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:462:5  

#16 0x559eb1600af8 in ash::DefaultState::HandleTransitionEvents(ash::WindowState\*, ash::WMEvent const\*) ash/wm/default\_state.cc:376:3  

#17 0x559eb15f3b97 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:435:19  

#18 0x559eb15fbb0e in ash::WindowState::OnWindowPropertyChanged(aura::Window\*, void const\*, long) ash/wm/window\_state.cc:1090:7  

#19 0x559eb069990c in aura::Window::AfterPropertyChange(void const\*, long) ui/aura/window.cc:949:14  

#20 0x559eac7f438a in ui::PropertyHandler::SetPropertyInternal(void const\*, char const\*, void (\*)(long), long, long) ui/base/class\_property.cc:43:3  

#21 0x559eb067e9ce in void ui::subtle::PropertyHelper::Set[ui::WindowShowState](javascript:void(0);)(ui::PropertyHandler\*, ui::ClassProperty[ui::WindowShowState](javascript:void(0);) const\*, ui::WindowShowState) ui/base/class\_property.h:204:28  

#22 0x559eb0b56c73 in wm::SetWindowFullscreen(aura::Window\*, bool) ui/wm/core/window\_util.cc:119:13  

#23 0x559eb0ae7282 in views::Widget::SetFullscreen(bool, base::TimeDelta, long) ui/views/widget/widget.cc:819:19  

#24 0x559eb614b077 in media\_router::WiredDisplayMediaRouteProvider::OnDisplayRemoved(display::Display const&) chrome/browser/media/router/providers/wired\_display/wired\_display\_media\_route\_provider.cc:263:28  

#25 0x559eb07e6405 in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display\_manager.cc:2201:14  

#26 0x559eb07e0134 in display::DisplayManager::UpdateDisplaysWith(std::\_\_1::vector<display::ManagedDisplayInfo, std::\_\_1::allocator[display::ManagedDisplayInfo](javascript:void(0);) > const&) ui/display/manager/display\_manager.cc:1053:5  

#27 0x559eb07e8d0e in display::DisplayManager::AddRemoveDisplay(std::\_\_1::vector<display::ManagedDisplayMode, std::\_\_1::allocator[display::ManagedDisplayMode](javascript:void(0);) >) ui/display/manager/display\_manager.cc:1438:3  

#28 0x559eb0b72286 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2131:40  

#29 0x559eb0b72b91 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1705:3  

#30 0x559eb0a4483e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#31 0x559eb0a4483e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#32 0x559eb103cd9f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#33 0x559eacff3b6b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#34 0x559eacff3959 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_1::vector<ui::EventHandler\*, std::\_\_1::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#35 0x559eacff2f7d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#36 0x559eacff2c04 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#37 0x559eacff2970 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#38 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#39 0x559eb06cb046 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:375:23  

#40 0x559ead848711 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#41 0x559ead98c0e9 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:616:38  

#42 0x559ead98b949 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#43 0x559eb06af309 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#44 0x559eb06adcfe in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#45 0x559eacff2924 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#46 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#47 0x559eacff713e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#48 0x559eacff7636 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#49 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#50 0x559ea0b5d419 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc  

#51 0x559ea0b5b559 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#52 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#53 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#54 0x559eb0d9bbb0 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#55 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#56 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#57 0x559eb0d9781a in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#58 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#59 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#60 0x559eb0b901de in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#61 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#62 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#63 0x559eb0b9df19 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#64 0x559eacff6de6 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#65 0x559eb0dd14bf in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#66 0x559eb0dd89c2 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:202:40  

#67 0x559ead00176f in Run base/callback.h:142:12  

#68 0x559ead00176f in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:28:25  

#69 0x559e9ded9ea7 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1292:3  

#70 0x559e9ded96fd in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1245:3  

#71 0x559e9deda1f8 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#72 0x559eacf9f661 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#73 0x559ead6e4bb7 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#74 0x559e9db14103 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#75 0x559e9db13e2d in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#76 0x559e9db138f3 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#77 0x559ead6edc13 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#78 0x559eaaf445a5 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#79 0x559eab2a2d0c in event\_process\_active base/third\_party/libevent/event.c:381:4  

#80 0x559eab2a2d0c in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#81 0x559eaaf44d7d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#82 0x559eaae3e5fa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:498:12  

#83 0x559eaad732fc in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#84 0x559ea15b310a in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1067:18  

#85 0x559ea15b75f1 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:155:15  

#86 0x559ea15ad2ea in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#87 0x559eaab5089f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:640:10  

#88 0x559eaab533ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1147:10  

#89 0x559eaab52838 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1019:12  

#90 0x559eaab4d001 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#91 0x559eaab4d688 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#92 0x559e9c733c3a in ChromeMain chrome/app/chrome\_main.cc:176:12  

#93 0x7f8ddc07e0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x559e9c73145d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x559eb06f5655 in make\_unique<ui::Layer, const ui::LayerType &> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x559eb06f5655 in ui::Layer::Clone() const ui/compositor/layer.cc:249:16  

#3 0x559eb074c0f3 in ui::LayerOwner::RecreateLayer() ui/compositor/layer\_owner.cc:66:23  

#4 0x559eb069f9b4 in aura::Window::RecreateLayer() ui/aura/window.cc:1567:54  

#5 0x559eb0b57025 in Run base/callback.h:241:12  

#6 0x559eb0b57025 in wm::RecreateLayersWithClosure(ui::LayerOwner\*, base::RepeatingCallback<std::\_\_1::unique\_ptr<ui::Layer, std::\_\_1::default\_delete[ui::Layer](javascript:void(0);) > (ui::LayerOwner\*)> const&) ui/wm/core/window\_util.cc:174:25  

#7 0x559eb0b56f81 in wm::RecreateLayers(ui::LayerOwner\*) ui/wm/core/window\_util.cc:165:10  

#8 0x559eb15f520a in ash::WindowState::SetBoundsDirectCrossFade(gfx::Rect const&) ash/wm/window\_state.cc:914:7  

#9 0x559eb16018c1 in ash::DefaultState::UpdateBoundsFromState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:590:19  

#10 0x559eb16010c9 in ash::DefaultState::EnterToNextState(ash::WindowState\*, chromeos::WindowStateType) ash/wm/default\_state.cc:462:5  

#11 0x559eb1600af8 in ash::DefaultState::HandleTransitionEvents(ash::WindowState\*, ash::WMEvent const\*) ash/wm/default\_state.cc:376:3  

#12 0x559eb15f3b97 in ash::WindowState::OnWMEvent(ash::WMEvent const\*) ash/wm/window\_state.cc:435:19  

#13 0x559eb15fbb0e in ash::WindowState::OnWindowPropertyChanged(aura::Window\*, void const\*, long) ash/wm/window\_state.cc:1090:7  

#14 0x559eb069990c in aura::Window::AfterPropertyChange(void const\*, long) ui/aura/window.cc:949:14  

#15 0x559eac7f438a in ui::PropertyHandler::SetPropertyInternal(void const\*, char const\*, void (\*)(long), long, long) ui/base/class\_property.cc:43:3  

#16 0x559eb067e9ce in void ui::subtle::PropertyHelper::Set[ui::WindowShowState](javascript:void(0);)(ui::PropertyHandler\*, ui::ClassProperty[ui::WindowShowState](javascript:void(0);) const\*, ui::WindowShowState) ui/base/class\_property.h:204:28  

#17 0x559eb0b56c73 in wm::SetWindowFullscreen(aura::Window\*, bool) ui/wm/core/window\_util.cc:119:13  

#18 0x559eb0ae7282 in views::Widget::SetFullscreen(bool, base::TimeDelta, long) ui/views/widget/widget.cc:819:19  

#19 0x559eb614b077 in media\_router::WiredDisplayMediaRouteProvider::OnDisplayRemoved(display::Display const&) chrome/browser/media/router/providers/wired\_display/wired\_display\_media\_route\_provider.cc:263:28  

#20 0x559eb07e6405 in display::DisplayManager::NotifyDisplayRemoved(display::Display const&) ui/display/manager/display\_manager.cc:2201:14  

#21 0x559eb07e0134 in display::DisplayManager::UpdateDisplaysWith(std::\_\_1::vector<display::ManagedDisplayInfo, std::\_\_1::allocator[display::ManagedDisplayInfo](javascript:void(0);) > const&) ui/display/manager/display\_manager.cc:1053:5  

#22 0x559eb07e8d0e in display::DisplayManager::AddRemoveDisplay(std::\_\_1::vector<display::ManagedDisplayMode, std::\_\_1::allocator[display::ManagedDisplayMode](javascript:void(0);) >) ui/display/manager/display\_manager.cc:1438:3  

#23 0x559eb0b72286 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:2131:40  

#24 0x559eb0b72b91 in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ash/accelerators/accelerator\_controller\_impl.cc:1705:3  

#25 0x559eb0a4483e in TryProcess ui/base/accelerators/accelerator\_manager.cc:153:17  

#26 0x559eb0a4483e in ui::AcceleratorManager::Process(ui::Accelerator const&) ui/base/accelerators/accelerator\_manager.cc:83:27  

#27 0x559eb103cd9f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ui/wm/core/accelerator\_filter.cc:51:18  

#28 0x559eacff3b6b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:190:12  

#29 0x559eacff3959 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_1::vector<ui::EventHandler\*, std::\_\_1::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ui/events/event\_dispatcher.cc:177:7  

#30 0x559eacff2f7d in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:125:3  

#31 0x559eacff2c04 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:83:14  

#32 0x559eacff2970 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:55:15  

#33 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#34 0x559eb06cb046 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:375:23  

#35 0x559ead848711 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:140:33  

#36 0x559ead98c0e9 in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:616:38  

#37 0x559ead98b949 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/ash/input\_method\_ash.cc:139:14  

#38 0x559eb06af309 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1080:54  

#39 0x559eb06adcfe in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:568:15  

#40 0x559eacff2924 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:51:34  

#41 0x559eb06b4aff in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#42 0x559eacff713e in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#43 0x559eacff7636 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:14  

#44 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#45 0x559ea0b5d419 in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc  

#46 0x559ea0b5b559 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:751:12  

#47 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#48 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#49 0x559eb0d9bbb0 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#50 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#51 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#52 0x559eb0d9781a in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/accessibility\_event\_rewriter.cc  

#53 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#54 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#55 0x559eb0b901de in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#56 0x559eacff75e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:67:32  

#57 0x559eacff5d5b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ui/events/event\_rewriter.cc:88:39  

#58 0x559eb0b9df19 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#59 0x559eacff6de6 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:144:29  

#60 0x559eb0dd14bf in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:229:38  

#61 0x559eb0dd89c2 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:202:40  

#62 0x559ead00176f in Run base/callback.h:142:12  

#63 0x559ead00176f in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:28:25  

#64 0x559e9ded9ea7 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1292:3  

#65 0x559e9ded96fd in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1245:3  

#66 0x559e9deda1f8 in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc  

#67 0x559eacf9f661 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:99:29  

#68 0x559ead6e4bb7 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#69 0x559e9db14103 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:457:14  

#70 0x559e9db13e2d in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:508:3  

#71 0x559e9db138f3 in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#72 0x559ead6edc13 in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#73 0x559eaaf445a5 in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#74 0x559eab2a2d0c in event\_process\_active base/third\_party/libevent/event.c:381:4  

#75 0x559eab2a2d0c in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#76 0x559eaaf44d7d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:204:7  

#77 0x559eaae3e5fa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:498:12  

#78 0x559eaad732fc in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#79 0x559ea15b310a in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1067:18  

#80 0x559ea15b75f1 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:155:15  

#81 0x559ea15ad2ea in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#82 0x559eaab5089f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:640:10  

#83 0x559eaab533ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1147:10  

#84 0x559eaab52838 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1019:12  

#85 0x559eaab4d001 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#86 0x559eaab4d688 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#87 0x559e9c733c3a in ChromeMain chrome/app/chrome\_main.cc:176:12  

#88 0x7f8ddc07e0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/scoped\_refptr.h:261:43 in operator bool  

Shadow bytes around the buggy address:  

0x0c3080031e60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3080031e70: 00 fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3080031e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3080031e90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080031ea0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c3080031eb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd  

0x0c3080031ec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080031ed0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080031ee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080031ef0: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3080031f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==121448==ABORTING

## Attachments

- [screencast_1313977.webm](attachments/screencast_1313977.webm) (video/webm, 4.7 MB)
- [poc3.html](attachments/poc3.html) (text/plain, 1.5 KB)
- [1313977_symbolized.log](attachments/1313977_symbolized.log) (text/plain, 15.8 KB)
- [1313977_un-symbolized.log](attachments/1313977_un-symbolized.log) (text/plain, 12.4 KB)
- [screencast_1313977_device.webm](attachments/screencast_1313977_device.webm) (video/webm, 3.7 MB)
- [screencast__00041.webm](attachments/screencast_00041.webm) (video/webm, 6.4 MB)
- [1313977_asan.log](attachments/1313977_asan.log) (text/plain, 28.3 KB)
- [Screen recording 2022-04-20 3.33.33 PM.webm](attachments/Screen recording 2022-04-20 3.33.33 PM.webm) (video/webm, 6.6 MB)

## Timeline

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-04-06)

cd to src/chrome$ ./chrome --user-data-dir=/tmp/chromeos --ash-dev-shortcuts --ash-host-window-bounds="0+0-1000x1000,1010+0-1000x1000" --use-system-clipboard  http://localhost:8000/poc3.html

### rs...@chromium.org (2022-04-06)

Thanks for the report. Sev-Low because of the required developer flag --ash-dev-shortcuts.

Does this reproduce for you on v100? I could only get it to go on v101/102.

[Monorail components: UI>Shell>WindowManager]

### [Deleted User] (2022-04-06)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-04-06)

ressek@,

Thanks for setting up the label. I have a question, I can demonstrate on the actual device but to turn off second display on Chromebook needs to close the lid[1]. Does the severity will be low as well? Actual devices does not need --ash-dev-shortcuts.

[1] https://support.google.com/chromebook/thread/1282340?hl=en&msgid=1288253

### rh...@gmail.com (2022-04-06)

Fyi I was not able to reproduced the issue on M100.


### rs...@chromium.org (2022-04-06)

Yes, if you can demonstrate this without flags on a real device that would bump up the severity. I don’t have a device to test with, but the developers on the bug should be able to verify.

### rh...@gmail.com (2022-04-06)

Thanks alot for the explanation.

### xd...@google.com (2022-04-08)

Looks like the crash happened when a display is removed from media route and the presentation receiver window tries to exit fullscreen.
To media router owner to take a look or further route. 

[Monorail components: Internals>Cast]

### rh...@gmail.com (2022-04-12)

rsesek@,

Regarding the statement on https://crbug.com/chromium/1313977#c7: 
I was able to demonstrate on real device, but I'm getting different stack trace. I believe I did same steps https://crbug.com/chromium/1313977#c0. 
I'm uploading the symbolized, un-symbolized and the screencast for reference. 

Thanks


### rh...@gmail.com (2022-04-13)

here's the correct asan log. 

### rs...@chromium.org (2022-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-15)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-18)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2022-04-18)

The repro steps require an elaborate setup (multiple monitors, user interacting with browser native UI, user physically detaching the second monitor). Given that, I question whether this should really be a P0 / stable release blocker. rsesek@ WDYT?

In general, Cast UI related functionalities have been getting many of these security bugs with obscure repro steps, and I wonder how valuable it is that we eliminate them, given their obscurity and that it is quite time consuming for us to keep up. If it is important to eliminate them, then we may want to decide that the maintenance cost is not worth the usage some of these features get. For the Wired Display Presentation API feature used in this bug, we're already planning on retiring it in favor of the Multi-Screen Window Placement API, and we may want to speed that up.


### ad...@google.com (2022-04-18)

rsesek@ is OOO so I'll answer.

It's a release blocker because it's a regression introduced in M101. We simply don't ship high severity security regressions, so this does need to be fixed before M101 ships, or please remove the feature/change which introduced this bug.

Regarding severity, a browser process UaF gives an attacker full access to *all* browsing state across all sites, and allows users to escape the sandbox. A browser process UaF is therefore critical severity, and would normally merit a special release of Chrome within a couple of days. Fortunately, as you note, this is mitigated by the need to entice the user to do some clicks in specific places, and therefore this has been graded as only "high" severity.

I agree the steps are hard to persuade a user to take, but they're not impossible. Even if we decided that the steps were so unlikely that this was "medium" severity, we'd still block M101 release to await your fix - again because it's a regression - we don't ship medium severity security regressions either.

### ad...@google.com (2022-04-18)

(if you can demonstrate that this is a pre-existing bug, not newly introduced in M101, then we won't consider it a release blocker. We would still like a rapid fix of course!)

### [Deleted User] (2022-04-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-18)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2022-04-18)

Thanks for the explanation adetaylor@. In general our UI features that deal with multiple windows or the OS file picker have been susceptible to these issues, so I look forward to Chrome-wide UAF mitigation initiatives making progress.

We haven't touched the Wired Display Presentation code in the M101 timeframe so it's not obvious to me where the regression is coming from. IIUC the allocation, free, and UAF all happen within an ash::DefaultState::UpdateBoundsFromState() call, inside a views::Widget::SetFullscreen() call [1] from Wired Display.

xdai@, are we calling views::Widget::SetFullscreen() when we're not supposed to? Or do you think there's been a change internal to WindowState/Layers code that could be the cause?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/media_router/presentation_receiver_window_view.cc;l=315;drc=d138bd5bee710c5d3befd0c08f1949b99a837e06

### sa...@chromium.org (2022-04-18)

+zxdan, could you help take a look? Thanks!

### sa...@chromium.org (2022-04-18)

my repro steps

0) build with args is_lsan=true and is_asan=true

1) ./chrome -ash-dev-shortcuts --ash-host-window-bounds="0+0-1000x1000,1010+0-1000x1000"
2) launch poc3.html from https://crbug.com/chromium/1313977#c2 (i dragged it to the downloads folder and double clicked it from files)
3) press click me and chose display 2
4) wait for original browser window to close, close files window as well
5) enter overview
6) press ctrl+shift+D (debug accelerator to remove display)

### zx...@chromium.org (2022-04-19)

 rhezashan@, thanks for reporting this issue.  sammiequon@, thanks for showing the reporduce steps.

I can reproduce this issue. I will fix it right now.

### pb...@google.com (2022-04-19)

We are cutting stable RC for M101 today pls review this is indeed RBS for M101, If not, please remove the RBS label. If so, please make sure to land the fix and request a merge to M101 release branch(go/chromebranches) ASAP. Thank you.

### mp...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-19)

This issue requires a bit of set up as well as user interaction, this is not considered a release blocking issue or critical/pri-0 issue, removing RBS label accordingly and lowering to pri-1. 

Thank you zxdan@ for following up here and promptly working on a fix. 


### zx...@chromium.org (2022-04-19)

While investigation, I found when we close the presentation receiver window, there will be a crash. The reason is that the auto state change notify the presentation receiver window after it is terminated: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/media_router/presentation_receiver_window_controller.cc;drc=c4b56465e4821b2a357367c76e72bc96b8acb65a;l=160

Seems these two crashes are not related. Still finding the reason for current issue.

### zx...@chromium.org (2022-04-20)

Update:

The UAF is because the pre-cached window layer[1] is freed by FrameAnimatorView::OnImplicitAnimationsCompleted[2].

In CrossFadeAnimationInternal, after first set the new_layer's Opacity[3], FrameAnimatorView::StartAnimation is triggered and the window's layer is recreated[4]. Therefore, the pre-cached new_layer is no longer the current window's layer. When FrameAnimatorView::OnImplicitAnimationsCompleted[2] is called, the new_layer is freed.

This happens because we detach the display in OverviewMode and ash::ExitAnimationObserver::OnImplicitAnimationsCompleted would somehow call FrameAnimatorView::StartAnimation. The stack trace is like below:

~~~~~~~~~~~~~FrameAnimatorView::StartAnimation~~~~~~~~~~~~~
#0 0x7fd9f5a6c819 base::debug::CollectStackTrace()
#1 0x7fd9f596b503 base::debug::StackTrace::StackTrace()
#2 0x5582611ce94d chromeos::FrameHeader::FrameAnimatorView::StartAnimation()
#3 0x5582611cf657 chromeos::FrameHeader::SetPaintAsActive()
#4 0x7fd9efd967b2 ash::NonClientFrameViewAsh::PaintAsActiveChanged()
#5 0x7fd9f0555463 base::internal::CallbackListBase<>::Notify<>()
#6 0x7fd9f060ac89 views::Widget::UnlockPaintAsActive()
#7 0x7fd9f060b4b5 views::Widget::PaintAsActiveLockImpl::~PaintAsActiveLockImpl()
#8 0x7fd9f060b4d2 views::Widget::PaintAsActiveLockImpl::~PaintAsActiveLockImpl()
#9 0x7fd9effc8de3 ash::OverviewController::OnEndingAnimationComplete()
#10 0x7fd9effc8c32 ash::OverviewController::RemoveAndDestroyExitAnimationObserver()
#11 0x7fd9effc7223 ash::ExitAnimationObserver::OnImplicitAnimationsCompleted() 

[1] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/window_animations.cc;drc=09533404dc063341e5c962413bdb49c775883b9d;l=256
[2] https://source.chromium.org/chromium/chromium/src/+/main:chromeos/ui/frame/frame_header.cc;drc=542c5d7a61aadbb82e40b105eedf989f35cde4dc;l=167
[3] https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/window_animations.cc;drc=09533404dc063341e5c962413bdb49c775883b9d;l=340
[4] https://source.chromium.org/chromium/chromium/src/+/main:chromeos/ui/frame/frame_header.cc;drc=542c5d7a61aadbb82e40b105eedf989f35cde4dc;l=107

### [Deleted User] (2022-04-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-20)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-04-20)

[BULK EDIT] 

M101 Stable promotion date is next week (Apr 28th), we need to start resolving this issue as it is marked ReleaseBlock-Stable. Please update with a plan for resolution.

### zx...@chromium.org (2022-04-20)

Based on https://crbug.com/chromium/1313977#c28, I agree that this is not a very common case and shouldn't block the branch cut. Low down the severity to median and priority to P1. Still working on fixing this issue.

### zx...@chromium.org (2022-04-20)

Have a quick fix now. To avoid new_layer uses the outdated window layer, we could update the new layer before performing animation just like old_layer did. The fixed record is attached.

### zx...@chromium.org (2022-04-21)

[Comment Deleted]

### zx...@chromium.org (2022-04-21)

drafted: crrev.com/c/3598633

### [Deleted User] (2022-04-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-21)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-21)

This release blocker is now considered 'urgent' and therefore subject to the following SLOs:
Assigned Owner: 1 day
Comment SLO: Every day
Fix SLO: Within 3 days.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@chromium.org (2022-04-21)

REmoving RBS and P0 based on https://crbug.com/chromium/1313977#c34 and https://crbug.com/chromium/1313977#c28. Dan has a fix and it should landed by EOD.

### gi...@appspot.gserviceaccount.com (2022-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9152528c3fd0819080ec2b778c35bf4da4b541cb

commit 9152528c3fd0819080ec2b778c35bf4da4b541cb
Author: Xiaodan Zhu <zxdan@chromium.org>
Date: Thu Apr 21 20:19:31 2022

cros: fix the crash of the cross fade animation

This CL fixs the crash of cross fade animation when using dual display.

The crash is mainly caused by
`FrameHeader::FrameAnimatorView::StartAnimation` that
recreates the window layer when setting the cross fade animation.

When setting the old layer animation, it will stops all the running
animations. If ExitAnimation of Overview is in the sequence, the
OverviewController will destroy the ExitAnimation and set the window
paint as active. Then, `FrameHeader::FrameAnimatorView::StartAnimation`
is triggered and the window's layer is recreated. In this case, the
precached new layer is no longer the window layer and is set up an
opacity animation.

Later, when the new layer sets opacity, the current opacity animation is
stopped and
`FrameHeader::FrameAnimatorView::OnImplicitAnimationCompleted` is
triggered which will destroy the precached new layer which causes
the crash.

To solve this, we should update the new layer after the old layer stops
animation.

The unittest simulates this case.

Test: WindowAnimationsTest.RecreateWhenSettingCrossFade
Bug: 1313977
Change-Id: Ifc22a616fe4790544f79846b5fee3220fec04fc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3598633
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Commit-Queue: Xiaodan Zhu <zxdan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#994872}

[modify] https://crrev.com/9152528c3fd0819080ec2b778c35bf4da4b541cb/ash/wm/window_animations.cc
[modify] https://crrev.com/9152528c3fd0819080ec2b778c35bf4da4b541cb/ash/wm/window_animations_unittest.cc


### zx...@chromium.org (2022-04-21)

crrev.com/c/3598633 fixed the issue.  Please reopen the issue if the crash still remains.

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

Requesting merge to beta M101 because latest trunk commit (994872) appears to be after beta branch point (982481).

Requesting merge to dev M102 because latest trunk commit (994872) appears to be after dev branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-22)

Merge approved: your change passed merge requirements and is auto-approved for M102. Please go ahead and merge the CL to branch 5005 (refs/branch-heads/5005) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-22)

Merge review required: M101 has already been cut for stable release.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-04-25)

Please answer the merge survey in https://crbug.com/chromium/1313977#c48

### zx...@chromium.org (2022-04-25)

1. Why does your merge fit within the merge criteria for these milestones?
Because my change fix a use after free issue in M101.

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3598633

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
Yes

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Yes. I added an unit test: WindowAnimationsTest.RecreateWhenSettingCrossFade but a manual test will be great.

Follow the repro steps in https://crbug.com/chromium/1313977#c24

0) build with args is_lsan=true and is_asan=true

1) ./chrome -ash-dev-shortcuts --ash-host-window-bounds="0+0-1000x1000,1010+0-1000x1000"
2) launch poc3.html from https://crbug.com/chromium/1313977#c2 (i dragged it to the downloads folder and double clicked it from files)
3) press click me and chose display 2
4) wait for original browser window to close, close files window as well
5) enter overview
6) press ctrl+shift+D (debug accelerator to remove display)

Expect result: there should be no crash.

### ma...@google.com (2022-04-26)

Approved, M-101

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9dea56f4d962894452700587046017cac0a1643d

commit 9dea56f4d962894452700587046017cac0a1643d
Author: Xiaodan Zhu <zxdan@chromium.org>
Date: Tue Apr 26 19:07:47 2022

[Merge to M102] cros: fix the crash of the cross fade animation

This CL fixs the crash of cross fade animation when using dual display.

The crash is mainly caused by
`FrameHeader::FrameAnimatorView::StartAnimation` that
recreates the window layer when setting the cross fade animation.

When setting the old layer animation, it will stops all the running
animations. If ExitAnimation of Overview is in the sequence, the
OverviewController will destroy the ExitAnimation and set the window
paint as active. Then, `FrameHeader::FrameAnimatorView::StartAnimation`
is triggered and the window's layer is recreated. In this case, the
precached new layer is no longer the window layer and is set up an
opacity animation.

Later, when the new layer sets opacity, the current opacity animation is
stopped and
`FrameHeader::FrameAnimatorView::OnImplicitAnimationCompleted` is
triggered which will destroy the precached new layer which causes
the crash.

To solve this, we should update the new layer after the old layer stops
animation.

The unittest simulates this case.

(cherry picked from commit 9152528c3fd0819080ec2b778c35bf4da4b541cb)

Test: WindowAnimationsTest.RecreateWhenSettingCrossFade
Bug: 1313977
Change-Id: Ifc22a616fe4790544f79846b5fee3220fec04fc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3598633
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Commit-Queue: Xiaodan Zhu <zxdan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#994872}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3607814
Cr-Commit-Position: refs/branch-heads/5005@{#179}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/9dea56f4d962894452700587046017cac0a1643d/ash/wm/window_animations.cc
[modify] https://crrev.com/9dea56f4d962894452700587046017cac0a1643d/ash/wm/window_animations_unittest.cc


### [Deleted User] (2022-04-26)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3356eead5a784527e45999f6937da15fa13ad990

commit 3356eead5a784527e45999f6937da15fa13ad990
Author: Xiaodan Zhu <zxdan@chromium.org>
Date: Tue Apr 26 19:21:47 2022

[Merge to M101] cros: fix the crash of the cross fade animation

This CL fixs the crash of cross fade animation when using dual display.

The crash is mainly caused by
`FrameHeader::FrameAnimatorView::StartAnimation` that
recreates the window layer when setting the cross fade animation.

When setting the old layer animation, it will stops all the running
animations. If ExitAnimation of Overview is in the sequence, the
OverviewController will destroy the ExitAnimation and set the window
paint as active. Then, `FrameHeader::FrameAnimatorView::StartAnimation`
is triggered and the window's layer is recreated. In this case, the
precached new layer is no longer the window layer and is set up an
opacity animation.

Later, when the new layer sets opacity, the current opacity animation is
stopped and
`FrameHeader::FrameAnimatorView::OnImplicitAnimationCompleted` is
triggered which will destroy the precached new layer which causes
the crash.

To solve this, we should update the new layer after the old layer stops
animation.

The unittest simulates this case.

(cherry picked from commit 9152528c3fd0819080ec2b778c35bf4da4b541cb)

Test: WindowAnimationsTest.RecreateWhenSettingCrossFade
Bug: 1313977
Change-Id: Ifc22a616fe4790544f79846b5fee3220fec04fc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3598633
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Commit-Queue: Xiaodan Zhu <zxdan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#994872}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3608618
Cr-Commit-Position: refs/branch-heads/4951@{#1072}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/3356eead5a784527e45999f6937da15fa13ad990/ash/wm/window_animations.cc
[modify] https://crrev.com/3356eead5a784527e45999f6937da15fa13ad990/ash/wm/window_animations_unittest.cc


### zx...@chromium.org (2022-04-26)

1. Was this issue a regression for the milestone it was found in?
No, I think this was a potential issue when first implemented CrossFadeAnimation.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No.

### rz...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### rz...@google.com (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-04-27)

1. Just https://crrev.com/c/3609052
2. Low, no conflicts
3. 101, 102
4. Yes

### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Congratulations, Rheza on another one! The VRP Panel has decided to award you $3,000 for this report. The reward amount is based on this issue not being web accessible and being fairly mitigated by significant user interaction required. Thank you for your efforts and reporting this issue to us.

### gm...@google.com (2022-04-28)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df2896b8185b95a84507ee55a54054203416cf6b

commit df2896b8185b95a84507ee55a54054203416cf6b
Author: Xiaodan Zhu <zxdan@chromium.org>
Date: Tue May 03 13:23:26 2022

[M96-LTS] cros: fix the crash of the cross fade animation

This CL fixs the crash of cross fade animation when using dual display.

The crash is mainly caused by
`FrameHeader::FrameAnimatorView::StartAnimation` that
recreates the window layer when setting the cross fade animation.

When setting the old layer animation, it will stops all the running
animations. If ExitAnimation of Overview is in the sequence, the
OverviewController will destroy the ExitAnimation and set the window
paint as active. Then, `FrameHeader::FrameAnimatorView::StartAnimation`
is triggered and the window's layer is recreated. In this case, the
precached new layer is no longer the window layer and is set up an
opacity animation.

Later, when the new layer sets opacity, the current opacity animation is
stopped and
`FrameHeader::FrameAnimatorView::OnImplicitAnimationCompleted` is
triggered which will destroy the precached new layer which causes
the crash.

To solve this, we should update the new layer after the old layer stops
animation.

The unittest simulates this case.

(cherry picked from commit 9152528c3fd0819080ec2b778c35bf4da4b541cb)

Test: WindowAnimationsTest.RecreateWhenSettingCrossFade
Bug: 1313977
Change-Id: Ifc22a616fe4790544f79846b5fee3220fec04fc9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3598633
Commit-Queue: Xiaodan Zhu <zxdan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#994872}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3609052
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Xiaodan Zhu <zxdan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1613}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/df2896b8185b95a84507ee55a54054203416cf6b/ash/wm/window_animations.cc
[modify] https://crrev.com/df2896b8185b95a84507ee55a54054203416cf6b/ash/wm/window_animations_unittest.cc


### rz...@google.com (2022-05-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1313977?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Cast, UI>Shell>WindowManager]
[Monorail mergedwith: crbug.com/chromium/1316842]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059305)*
