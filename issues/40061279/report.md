# Security: Heap-use-after-free in ash::OverviewItem::ShowWindowInOverview

| Field | Value |
|-------|-------|
| **Issue ID** | [40061279](https://issues.chromium.org/issues/40061279) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Views>Desktop |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2022-10-08 |
| **Bounty** | $1,500.00 |

## Description

**VERSION**  

Chrome Version: 108.0.5348.0  

Operating System: ChromeOS

**REPRODUCTION CASE**  

0. ./chrome --enable-features=DesksTemplates

1. Open Chromium browser and open print dialog
2. Press F5 >> Save desk as a template >> Use tamplate

=35833==ERROR: AddressSanitizer: heap-use-after-free on address 0x614000304d40 at pc 0x564f9fbda490 bp 0x7fff24971160 sp 0x7fff24971158  

READ of size 8 at 0x614000304d40 thread T0 (chrome)  

==35833==WARNING: invalid path to external symbolizer!  

==35833==WARNING: Failed to use and restart external symbolizer!  

#0 0x564f9fbda48f in operator bool ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:268:19  

#1 0x564f9fbda48f in ash::OverviewItem::ShowWindowInOverview() ./../../ash/wm/overview/overview\_item.cc:1460:7  

#2 0x564f9fbda136 in ash::OverviewItem::RevertHideForDesksTemplatesGrid(bool) ./../../ash/wm/overview/overview\_item.cc:257:3  

#3 0x564f9fbbdac8 in ash::OverviewGrid::RemoveAllItemsForDesksTemplatesLaunch() ./../../ash/wm/overview/overview\_grid.cc:772:11  

#4 0x564f9fb015b2 in ash::DesksController::CreateNewDeskForTemplate(ash::DeskTemplateType, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t> > const&) ./../../ash/wm/desks/desks\_controller.cc:1143:15  

#5 0x564f9fb70f1a in ash::SavedDeskPresenter::LaunchSavedDesk(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >, aura::Window\*) ./../../ash/wm/desks/templates/saved\_desk\_presenter.cc:419:44  

#6 0x564f9ef03000 in base::RepeatingCallback<void (ui::Event const&)>::Run(ui::Event const&) const & ./../../base/functional/callback.h:267:12  

#7 0x564f9eefdb5a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ./../../ui/views/controls/button/button.cc:67:13  

#8 0x564f9ef05782 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/controls/button/button\_controller.cc:0:0  

#9 0x564f9eecc0f5 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ./../../ui/events/scoped\_target\_handler.cc:28:24  

#10 0x564f9ba24667 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#11 0x564f9ba23b4c in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#12 0x564f9ba23620 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#13 0x564f9ba23390 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#14 0x564f9f06ca57 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/widget/root\_view.cc:499:9  

#15 0x564f9f081ca6 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/widget.cc:1602:20  

#16 0x564f9ba24667 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#17 0x564f9ba23b4c in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#18 0x564f9ba23620 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#19 0x564f9ba23390 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#20 0x564f9ec06e4c in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:56:17  

#21 0x564f9ba28022 in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#22 0x564f9ba2851a in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:66:14  

#23 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#24 0x564f913d433a in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1291:12  

#25 0x564f913d48b1 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:759:12  

#26 0x564f9ba284ca in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#27 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#28 0x564f9f329b30 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#29 0x564f9ba284ca in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#30 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#31 0x564f9f32554a in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/events/accessibility\_event\_rewriter.cc:0:0  

#32 0x564f9ba284ca in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#33 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#34 0x564f9f10aa8e in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc:0:0  

#35 0x564f9ba284ca in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#36 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39  

#37 0x564f9f1181ec in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc:0:0  

#38 0x564f9ba27cc5 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ./../../ui/events/event\_source.cc:144:29  

#39 0x564f9f36039d in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ui/aura/window\_tree\_host\_platform.cc:235:38  

#40 0x564f9f3679a4 in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ash/host/ash\_window\_tree\_host\_platform.cc:206:40  

#41 0x564f9ba325e6 in Run ./../../base/functional/callback.h:145:12  

#42 0x564f9ba325e6 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ./../../ui/events/ozone/events\_ozone.cc:36:25  

#43 0x564f8afb55bc in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1380:3  

#44 0x564f8afb4df0 in ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:1333:3  

#45 0x564f8afb58fc in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ./../../ui/ozone/platform/x11/x11\_window.cc:0:0  

#46 0x564f9b9cc0ab in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ./../../ui/events/platform/platform\_event\_source.cc:99:29  

#47 0x564f9c1849af in ui::X11EventSource::OnEvent(x11::Event const&) ./../../ui/events/platform/x11/x11\_event\_source.cc:287:5  

#48 0x564f8abbd4d9 in x11::Connection::DispatchEvent(x11::Event const&) ./../../ui/gfx/x/connection.cc:457:14  

#49 0x564f8abbd239 in x11::Connection::ProcessNextEvent() ./../../ui/gfx/x/connection.cc:508:3  

#50 0x564f8abbccf3 in x11::Connection::Dispatch() ./../../ui/gfx/x/connection.cc:0:0  

#51 0x564f9c18da5b in ui::X11EventWatcherFdWatch::OnFileCanReadWithoutBlocking(int) ./../../ui/events/platform/x11/x11\_event\_watcher\_fdwatch.cc:64:15  

#52 0x564f996ccb4d in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) ./../../base/message\_loop/message\_pump\_libevent.cc:0:13  

#53 0x564f99a53a4e in event\_process\_active ./../../third\_party/libevent/event.c:381:4  

#54 0x564f99a53a4e in event\_base\_loop ./../../third\_party/libevent/event.c:521:4  

#55 0x564f996cd523 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:316:5  

#56 0x564f995bc8c5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:600:12  

#57 0x564f99509849 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#58 0x564f91ba8e04 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1048:18  

#59 0x564f91badcd8 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:160:15  

#60 0x564f91ba32ba in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#61 0x564f992b8fb5 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:710:10  

#62 0x564f992bb66d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1243:10  

#63 0x564f992bb084 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1103:12  

#64 0x564f992b4fb4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#65 0x564f992b5562 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#66 0x564f89a22a30 in ChromeMain ./../../chrome/app/chrome\_main.cc:175:12  

#67 0x7fd50f88e0b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x614000304d40 is located 256 bytes inside of 416-byte region [0x614000304c40,0x614000304de0)  

freed by thread T0 (chrome) here:  

#0 0x564f89a20abd in operator delete(void\*) *asan\_rtl*:3  

#1 0x564f9fbb64c2 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x564f9fbb64c2 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x564f9fbb64c2 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x564f9fbb64c2 in destroy ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:170:15  

#5 0x564f9fbb64c2 in destroy<std::Cr::unique\_ptr<ash::OverviewItem, std::Cr::default\_delete[ash::OverviewItem](javascript:void(0);) >, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:307:13  

#6 0x564f9fbb64c2 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:811:9  

#7 0x564f9fbb64c2 in \_\_clear ./../../buildtools/third\_party/libc++/trunk/include/vector:805:29  

#8 0x564f9fbb64c2 in std::Cr::vector<std::Cr::unique\_ptr<ash::OverviewItem, std::Cr::default\_delete[ash::OverviewItem](javascript:void(0);) >, std::Cr::allocator<std::Cr::unique\_ptr<ash::OverviewItem, std::Cr::default\_delete[ash::OverviewItem](javascript:void(0);) > > >::clearabi:v160000 ./../../buildtools/third\_party/libc++/trunk/include/vector:618:9  

#9 0x564f9fbb5cb7 in ash::OverviewGrid::Shutdown(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_grid.cc:497:16  

#10 0x564f9fbeb61a in ash::OverviewSession::Shutdown() ./../../ash/wm/overview/overview\_session.cc:353:20  

#11 0x564f9fbaeafb in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:346:24  

#12 0x564f9fbaf28c in ash::OverviewController::EndOverview(ash::OverviewEndAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:143:3  

#13 0x564f9fbefae4 in ash::OverviewSession::OnWindowActivating(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*) ./../../ash/wm/overview/overview\_session.cc:0:0  

#14 0x564f9f633444 in wm::FocusController::SetActiveWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:354:14  

#15 0x564f9f6316f7 in wm::FocusController::FocusAndActivateWindow(wm::ActivationChangeObserver::ActivationReason, aura::Window\*, bool) ./../../ui/wm/core/focus\_controller.cc:235:10  

#16 0x564f9f0c5cf6 in views::NativeWidgetAura::Activate() ./../../ui/views/widget/native\_widget\_aura.cc:690:56  

#17 0x564f9f0c5a02 in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ./../../ui/views/widget/native\_widget\_aura.cc:658:7  

#18 0x564f9f07a765 in views::Widget::Show() ./../../ui/views/widget/widget.cc:745:23  

#19 0x564faa9f9613 in constrained\_window::NativeWebContentsModalDialogManagerViews::Show() ./../../components/constrained\_window/native\_web\_contents\_modal\_dialog\_manager\_views.cc:101:13  

#20 0x564f92c8df7d in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::Visibility), content::Visibility&>(void (content::WebContentsObserver::\*)(content::Visibility), content::Visibility&) ./../../content/browser/web\_contents/web\_contents\_impl.h:1555:9  

#21 0x564f92c7cfad in content::WebContentsImpl::SetVisibilityAndNotifyObservers(content::Visibility) ./../../content/browser/web\_contents/web\_contents\_impl.cc:5224:16  

#22 0x564f92c6ad1b in content::WebContentsImpl::UpdateVisibilityAndNotifyPageAndView(content::Visibility, bool) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3682:5  

#23 0x564f9ebecba4 in aura::Window::SetOcclusionInfo(aura::Window::OcclusionState, SkRegion const&) ./../../ui/aura/window.cc:1021:16  

#24 0x564f9ec14907 in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window\_occlusion\_change\_builder.cc:35:15  

#25 0x564f9ec14a4b in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window\_occlusion\_change\_builder.cc:26:51  

#26 0x564f9ec0a20c in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#27 0x564f9ec0a20c in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#28 0x564f9ec0a20c in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#29 0x564f9ec0a20c in aura::WindowOcclusionTracker::MaybeComputeOcclusion() ./../../ui/aura/window\_occlusion\_tracker.cc:345:3  

#30 0x564f9ebe5973 in aura::Window::SetVisibleInternal(bool) ./../../ui/aura/window.cc:1010:1  

#31 0x564f9fc0218b in ash::ScopedOverviewHideWindows::RemoveWindow(aura::Window\*) ./../../ash/wm/overview/scoped\_overview\_hide\_windows.cc:50:13  

#32 0x564f9fbda410 in ash::OverviewItem::ShowWindowInOverview() ./../../ash/wm/overview/overview\_item.cc:1459:19  

#33 0x564f9fbda136 in ash::OverviewItem::RevertHideForDesksTemplatesGrid(bool) ./../../ash/wm/overview/overview\_item.cc:257:3  

#34 0x564f9fbbdac8 in ash::OverviewGrid::RemoveAllItemsForDesksTemplatesLaunch() ./../../ash/wm/overview/overview\_grid.cc:772:11  

#35 0x564f9fb015b2 in ash::DesksController::CreateNewDeskForTemplate(ash::DeskTemplateType, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t> > const&) ./../../ash/wm/desks/desks\_controller.cc:1143:15  

#36 0x564f9fb70f1a in ash::SavedDeskPresenter::LaunchSavedDesk(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >, aura::Window\*) ./../../ash/wm/desks/templates/saved\_desk\_presenter.cc:419:44  

#37 0x564f9ef03000 in base::RepeatingCallback<void (ui::Event const&)>::Run(ui::Event const&) const & ./../../base/functional/callback.h:267:12  

#38 0x564f9eefdb5a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ./../../ui/views/controls/button/button.cc:67:13  

#39 0x564f9ef05782 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/controls/button/button\_controller.cc:0:0

previously allocated by thread T0 (chrome) here:  

#0 0x564f89a2025d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x564f9fbb47ec in make\_unique<ash::OverviewItem, aura::Window \*&, ash::OverviewSession \*&, ash::OverviewGrid \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:26  

#2 0x564f9fbb47ec in ash::OverviewGrid::OverviewGrid(aura::Window\*, std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, ash::OverviewSession\*) ./../../ash/wm/overview/overview\_grid.cc:451:9  

#3 0x564f9fbe9ec9 in make\_unique<ash::OverviewGrid, aura::Window \*&, const std::Cr::vector<aura::Window \*, std::Cr::allocator<aura::Window \*> > &, ash::OverviewSession \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:30  

#4 0x564f9fbe9ec9 in ash::OverviewSession::Init(std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&, std::Cr::vector<aura::Window\*, std::Cr::allocator[aura::Window\\*](javascript:void(0);) > const&) ./../../ash/wm/overview/overview\_session.cc:211:17  

#5 0x564f9fbae4ca in ash::OverviewController::ToggleOverview(ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:435:24  

#6 0x564f9fbad9aa in ash::OverviewController::StartOverview(ash::OverviewStartAction, ash::OverviewEnterExitType) ./../../ash/wm/overview/overview\_controller.cc:129:3  

#7 0x564f9f3b2504 in ash::AcceleratorControllerImpl::PerformAction(ash::AcceleratorAction, ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:1221:7  

#8 0x564f9f3b439f in ash::AcceleratorControllerImpl::AcceleratorPressed(ui::Accelerator const&) ./../../ash/accelerators/accelerator\_controller\_impl.cc:462:3  

#9 0x564f9efe7eda in TryProcess ./../../ui/base/accelerators/accelerator\_manager.cc:153:17  

#10 0x564f9efe7eda in ui::AcceleratorManager::Process(ui::Accelerator const&) ./../../ui/base/accelerators/accelerator\_manager.cc:83:27  

#11 0x564f9f63692f in ash::PreTargetAcceleratorHandler::ProcessAccelerator(ui::KeyEvent const&, ui::Accelerator const&) ./../../ash/accelerators/pre\_target\_accelerator\_handler.cc:74:45  

#12 0x564f9f636f8f in wm::AcceleratorFilter::OnKeyEvent(ui::KeyEvent\*) ./../../ui/wm/core/accelerator\_filter.cc:51:18  

#13 0x564f9ba24667 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#14 0x564f9ba24360 in ui::EventDispatcher::DispatchEventToEventHandlers(std::Cr::vector<ui::EventHandler\*, std::Cr::allocator[ui::EventHandler\\*](javascript:void(0);) >\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:177:7  

#15 0x564f9ba23999 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:125:3  

#16 0x564f9ba23620 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#17 0x564f9ba23390 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#18 0x564f9ec06e4c in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:56:17  

#19 0x564f9ec1d473 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ./../../ui/aura/window\_tree\_host.cc:366:23  

#20 0x564f9c2e04a7 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ./../../ui/base/ime/input\_method\_base.cc:134:43  

#21 0x564f9c3d928f in ui::InputMethodAsh::ProcessUnfilteredKeyPressEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:646:38  

#22 0x564f9c3d8af0 in ui::InputMethodAsh::DispatchKeyEvent(ui::KeyEvent\*) ./../../ui/base/ime/ash/input\_method\_ash.cc:146:14  

#23 0x564f9ec0130f in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ./../../ui/aura/window\_event\_dispatcher.cc:1079:54  

#24 0x564f9ebffe46 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/aura/window\_event\_dispatcher.cc:567:15  

#25 0x564f9ba23344 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:51:34  

#26 0x564f9ec06e4c in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:56:17  

#27 0x564f9ba28022 in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:118:16  

#28 0x564f9ba26daf in ui::EventRewriter::SendEventFinally(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:94:39  

#29 0x564f913d657b in ui::EventRewriterChromeOS::RewriteKeyEventInContext(ui::KeyEvent const&, std::Cr::unique\_ptr<ui::Event, std::Cr::default\_delete[ui::Event](javascript:void(0);) >, ui::EventRewriteStatus, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1840:9  

#30 0x564f913d4a95 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ./../../ui/chromeos/events/event\_rewriter\_chromeos.cc:753:12  

#31 0x564f9ba284ca in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ./../../ui/events/event\_source.cc:67:32  

#32 0x564f9ba26bf3 in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ./../../ui/events/event\_rewriter.cc:88:39

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1056661/chrome+0x251b948f) (BuildId: 4d69127b5fe032a2)  

Shadow bytes around the buggy address:  

0x614000304a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x614000304b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x614000304b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x614000304c00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x614000304c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x614000304d00: fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd  

0x614000304d80: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x614000304e00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x614000304e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x614000304f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x614000304f80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

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

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 1.3 MB)

## Timeline

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-10-09)

Good Build : 108.0.5329.0 (Revision - 1052483)
Bad Build : 108.0.5329.0 (Revision - 1052501)

### lz...@google.com (2022-10-10)

I will the TL of desk templates to take a look. Thank you!

[Monorail components: Internals>Views>Desktop]

### lz...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### ad...@google.com (2022-10-10)

(auto-cc on security bug)

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-10-18)

Any update here? Thanks!

### yz...@google.com (2022-10-18)

The data structure affected is `ash::OverviewItem`. 

Daniel, could you please take a look?

### lz...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-10-18)

This is high severity.

### [Deleted User] (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2022-10-19)

I've reproduced on head.

### da...@chromium.org (2022-10-19)

This generalizes to having launching any template while a browser window with a print dialog is showing on the desk from which the template is launched from.

### da...@chromium.org (2022-10-19)

So it seems that in this case, when ShowWindowInOverview is doing its thing, it ends up shutting down overview mode, which means the object is destroyed.

ScopedOverviewHideWindows::RemoveWindow, through a roundabout way, ends up activating a window and this causes overview mode to exit.

https://source.chromium.org/chromium/chromium/src/+/main:ash/wm/overview/overview_item.cc;l=1459;drc=fe9bb2cbc239b5aa37a4b59bc38f1f022b6f36b8


### da...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### yo...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aca00c63fdbf7d795929207bdb5aa25ddf73db3d

commit aca00c63fdbf7d795929207bdb5aa25ddf73db3d
Author: Yongshun Liu <yongshun@chromium.org>
Date: Mon Oct 24 22:22:33 2022

saved_desks: Fix hide/show for overview item window and app window

This fixes 2 issues.

1. Wrong shadow and header for the overview item when launching a
template.

During the launch process of a template, a new `OverviewItem` will be
added to the `OverviewGrid`. Since the library widget fade out animation
takes precedence, the overview item window is hidden until the fade out
animation is done, then the hide will be reverted. The problem is its
shadow and header might not be sync'ed with the overview item window.

The fix is to make sure the header and shadow show up only when the
overview item window is visible, and update the header and shadow when
reverting after the fade out animation.

2. Overview session unexpectedly being turned off when launching a
template

So now we hide the real application window when in library view, this is
to make sure dark/light change does not make it visible. However, when
we are reverting the hide, and still want to stay in overview, like when
launching a template, since overview session detects a window activation
event, the session would be soon turned off.

The fix is to let `OverviewSession` ignore the activation for such
window in `OnWindowActivating`. This also fixes the heap-use-after-free
security bug caused by overview session being turned off unexpectedly.

Test: Manual
Bug: b/254338856
Bug: 1372757
Change-Id: Ib326f84dd4aa96b0ba9417dc3217c70f3cedcf95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965350
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Commit-Queue: Yongshun Liu <yongshun@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1063035}

[modify] https://crrev.com/aca00c63fdbf7d795929207bdb5aa25ddf73db3d/ash/wm/overview/overview_item.cc
[modify] https://crrev.com/aca00c63fdbf7d795929207bdb5aa25ddf73db3d/ash/wm/overview/overview_session.h


### yo...@chromium.org (2022-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

Requesting merge to dev M108 because latest trunk commit (1063035) appears to be after dev branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-25)

Merge review required: M108 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2022-10-26)

As we migrated to use buganizer, therefore I requested the merge back through buganizer here - b/255411100. The request just got approved, I'm going to merge back the fix to M108 today. Updates can be found at the buganizer link.

### gi...@appspot.gserviceaccount.com (2022-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/308dc4497d5925d27f219939e1b6876f5e33764e

commit 308dc4497d5925d27f219939e1b6876f5e33764e
Author: Yongshun Liu <yongshun@chromium.org>
Date: Wed Oct 26 21:05:38 2022

[Merge to M108] saved_desks: Fix hide/show for overview item window and app window

This fixes 2 issues.

1. Wrong shadow and header for the overview item when launching a
template.

During the launch process of a template, a new `OverviewItem` will be
added to the `OverviewGrid`. Since the library widget fade out animation
takes precedence, the overview item window is hidden until the fade out
animation is done, then the hide will be reverted. The problem is its
shadow and header might not be sync'ed with the overview item window.

The fix is to make sure the header and shadow show up only when the
overview item window is visible, and update the header and shadow when
reverting after the fade out animation.

2. Overview session unexpectedly being turned off when launching a
template

So now we hide the real application window when in library view, this is
to make sure dark/light change does not make it visible. However, when
we are reverting the hide, and still want to stay in overview, like when
launching a template, since overview session detects a window activation
event, the session would be soon turned off.

The fix is to let `OverviewSession` ignore the activation for such
window in `OnWindowActivating`. This also fixes the heap-use-after-free
security bug caused by overview session being turned off unexpectedly.

(cherry picked from commit aca00c63fdbf7d795929207bdb5aa25ddf73db3d)

Test: Manual
Bug: b/254338856
Bug: 1372757
Change-Id: Ib326f84dd4aa96b0ba9417dc3217c70f3cedcf95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965350
Reviewed-by: Sammie Quon <sammiequon@chromium.org>
Commit-Queue: Yongshun Liu <yongshun@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1063035}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3976774
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#330}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/308dc4497d5925d27f219939e1b6876f5e33764e/ash/wm/overview/overview_item.cc
[modify] https://crrev.com/308dc4497d5925d27f219939e1b6876f5e33764e/ash/wm/overview/overview_session.h


### [Deleted User] (2022-10-26)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2022-10-26)

I'm not very sure about the LTS channel, but please take a look at the following questionnaire answers.

1. Was this issue a regression for the milestone it was found in?
The issue was introduced/found in M-108. It's not a regression.
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
Yes, it was introduced in M-108 which I think is after the latest LTS milestone.

### rz...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-10-27)

Hide/ShowWindowInOverview aren't present in 102

### ob...@google.com (2022-11-02)

Is there a duplicate issue where this was approved? @yongshun@chromium.org @yongshun@google.com

cc: @dgagnon@google.com

### yo...@chromium.org (2022-11-02)

re https://crbug.com/chromium/1372757#c34, yes, it's approved here - b/255411100

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, Khalil! The VRP Panel has decided to award you $1,500 for this high quality report of a very heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### ob...@google.com (2022-11-04)

Thank you yongshun@google.com

### ch...@google.com (2022-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-25)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1372757?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061279)*
