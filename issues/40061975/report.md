# Security:UAF in content::SyntheticMouseDriver::DispatchEvent(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061975](https://issues.chromium.org/issues/40061975) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Input, Internals>Core |
| **Platforms** | Linux |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2022-11-30 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::SyntheticMouseDriver::DispatchEvent in the browser process

**VERSION**  

Chromium 110.0.5450.0 (Developer Build) (64-bit)  

Revision b54b2f50db2faf68b7eb7ca69984fb1b15cc3d22-refs/heads/main@{#1077406}  

OS Linux

**REPRODUCTION CASE**  

This vulnerability can be triggered without an extension.  

However the extension can trigger this issue more stably.

1. unzip the webserver.zip into webserver\_path && run `python3 -m http.server 8000` in the webserver\_path
2. unzip the extension.zip into extension\_path
3. run  
   
   ./chrome --user-data-dir=/tmp/aaa --enable-gpu-benchmarking --load-extension="extension\_path" <http://localhost:8000/pointertest.html> <http://localhost:8000/pointertest.html> <http://localhost:8000/pointertest.html> <http://localhost:8000/pointertest.html> <http://localhost:8000/pointertest.html> <http://localhost:8000/pointertest.html>

The UAF will be triggered.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [browser]

==40175==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e0002f4850 at pc 0x5582a1d4549b bp 0x7ffdaac095f0 sp 0x7ffdaac095e8  

WRITE of size 4 at 0x60e0002f4850 thread T0 (chrome)  

==40175==WARNING: invalid path to external symbolizer!  

==40175==WARNING: Failed to use and restart external symbolizer!  

#0 0x5582a1d4549a in SetType ./../../third\_party/blink/public/common/input/web\_input\_event.h:309:41  

#1 0x5582a1d4549a in content::SyntheticMouseDriver::DispatchEvent(content::SyntheticGestureTarget\*, base::TimeTicks const&) ./../../content/browser/renderer\_host/input/synthetic\_mouse\_driver.cc:25:18  

#2 0x5582a1d48176 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(base::TimeTicks const&, content::SyntheticGestureTarget\*) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:112:32  

#3 0x5582a1d47720 in content::SyntheticPointerAction::ForwardInputEvents(base::TimeTicks const&, content::SyntheticGestureTarget\*) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:44:12  

#4 0x5582a1d3a3a8 in content::SyntheticGestureController::DispatchNextEvent(base::TimeTicks) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:113:48  

#5 0x5582a1d406a6 in operator() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:100:25  

#6 0x5582a1d406a6 in Invoke<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:545:12  

#7 0x5582a1d406a6 in MakeItSo<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const std::Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &> ./../../base/functional/bind\_internal.h:849:12  

#8 0x5582a1d406a6 in RunImpl<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const std::Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &, 0UL> ./../../base/functional/bind\_internal.h:943:12  

#9 0x5582a1d406a6 in base::internal::Invoker<base::internal::BindState<content::SyntheticGestureController::StartTimer(bool)::$\_0, base::WeakPtr[content::SyntheticGestureController](javascript:void(0);)>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:907:12  

#10 0x5582a8f34b5d in Run ./../../base/functional/callback.h:348:12  

#11 0x5582a8f34b5d in base::MetronomeTimer::OnScheduledTaskInvoked() ./../../base/timer/timer.cc:477:19  

#12 0x5582a8f352df in Invoke<void (base::MetronomeTimer::\*)(), base::MetronomeTimer \*> ./../../base/functional/bind\_internal.h:670:12  

#13 0x5582a8f352df in MakeItSo<void (base::MetronomeTimer::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported> > &> ./../../base/functional/bind\_internal.h:849:12  

#14 0x5582a8f352df in RunImpl<void (base::MetronomeTimer::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported> > &, 0UL> ./../../base/functional/bind\_internal.h:943:12  

#15 0x5582a8f352df in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(), base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported>>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:907:12  

#16 0x5582a8e6d439 in Run ./../../base/functional/callback.h:152:12  

#17 0x5582a8e6d439 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:156:32  

#18 0x5582a8eb7c08 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:451:11)> ./../../base/task/common/task\_annotator.h:85:5  

#19 0x5582a8eb7c08 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:449:23  

#20 0x5582a8eb696a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:30  

#21 0x5582a8eb9044 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#22 0x5582a8d6af2e in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:404:48  

#23 0x5582a8eb9a7d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:609:12  

#24 0x5582a8df80c8 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#25 0x5582a101a510 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1050:18  

#26 0x5582a1020666 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15  

#27 0x5582a1013d75 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#28 0x5582a7bee114 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:693:10  

#29 0x5582a7bf10fc in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1231:10  

#30 0x5582a7bf09ec in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1087:12  

#31 0x5582a7be92db in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:344:36  

#32 0x5582a7be99f9 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:372:10  

#33 0x5582987bb0ad in ChromeMain ./../../chrome/app/chrome\_main.cc:174:12  

#34 0x7fd3522c0082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60e0002f4850 is located 48 bytes inside of 152-byte region [0x60e0002f4820,0x60e0002f48b8)  

freed by thread T0 (chrome) here:  

#0 0x5582987b913d in operator delete(void\*) *asan\_rtl*:3  

#1 0x5582a1d474ce in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x5582a1d474ce in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x5582a1d474ce in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x5582a1d474ce in ~SyntheticPointerAction ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:19:52  

#5 0x5582a1d474ce in content::SyntheticPointerAction::~SyntheticPointerAction() ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:19:51  

#6 0x5582a1d38d42 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#7 0x5582a1d38d42 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#8 0x5582a1d38d42 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#9 0x5582a1d38d42 in \_\_destroy\_at<std::Cr::unique\_ptr<content::SyntheticGesture, std::Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:64:13  

#10 0x5582a1d38d42 in destroy\_at<std::Cr::unique\_ptr<content::SyntheticGesture, std::Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:89:5  

#11 0x5582a1d38d42 in destroy<std::Cr::unique\_ptr<content::SyntheticGesture, std::Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:316:9  

#12 0x5582a1d38d42 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:817:9  

#13 0x5582a1d38d42 in \_\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:705:9  

#14 0x5582a1d38d42 in erase ./../../buildtools/third\_party/libc++/trunk/include/vector:1588:11  

#15 0x5582a1d38d42 in content::SyntheticGestureController::GestureAndCallbackQueue::Pop() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.h:105:17  

#16 0x5582a1d38742 in content::SyntheticGestureController::~SyntheticGestureController() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:32:28  

#17 0x5582a1d38ead in content::SyntheticGestureController::~SyntheticGestureController() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:28:59  

#18 0x5582a21487d8 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#19 0x5582a21487d8 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#20 0x5582a21487d8 in SetView ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:573:33  

#21 0x5582a21487d8 in content::RenderWidgetHostImpl::ViewDestroyed() ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:1416:3  

#22 0x5582a21a108a in content::RenderWidgetHostViewAura::~RenderWidgetHostViewAura() ./../../content/browser/renderer\_host/render\_widget\_host\_view\_aura.cc:2178:11  

#23 0x5582a21a1bfd in content::RenderWidgetHostViewAura::~RenderWidgetHostViewAura() ./../../content/browser/renderer\_host/render\_widget\_host\_view\_aura.cc:2174:55  

#24 0x5582af43ed1c in aura::Window::~Window() ./../../ui/aura/window.cc:230:16  

#25 0x5582af440fdd in aura::Window::~Window() ./../../ui/aura/window.cc:185:19  

#26 0x5582a21577df in content::RenderWidgetHostImpl::RendererExited() ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2260:12  

#27 0x5582a2129d2f in RenderProcessExited ./../../content/browser/renderer\_host/render\_view\_host\_impl.cc:771:16  

#28 0x5582a2129d2f in non-virtual thunk to content::RenderViewHostImpl::RenderProcessExited(content::RenderProcessHost\*, content::ChildProcessTerminationInfo const&) ./../../content/browser/renderer\_host/render\_view\_host\_impl.cc:0:0  

#29 0x5582a20d8fde in content::RenderProcessHostImpl::ProcessDied(content::ChildProcessTerminationInfo const&) ./../../content/browser/renderer\_host/render\_process\_host\_impl.cc:4776:14  

#30 0x5582a20d840f in content::RenderProcessHostImpl::FastShutdownIfPossible(unsigned long, bool) ./../../content/browser/renderer\_host/render\_process\_host\_impl.cc:3640:3  

#31 0x5582b96e2240 in TabStripModel::CloseWebContentses(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int, TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1886:19  

#32 0x5582b96c7719 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1841:7  

#33 0x5582b96c8cf2 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:703:10  

#34 0x5582ba4f540c in BrowserTabStripController::CloseTab(int) ./../../chrome/browser/ui/views/tabs/browser\_tab\_strip\_controller.cc:339:11  

#35 0x5582ba55ec6f in TabStrip::CloseTabInternal(int, CloseTabSource) ./../../chrome/browser/ui/views/tabs/tab\_strip.cc:1969:16  

#36 0x5582ba55e65b in TabStrip::CloseTab(Tab\*, CloseTabSource) ./../../chrome/browser/ui/views/tabs/tab\_strip.cc:1433:5  

#37 0x5582ba50f7d0 in Tab::CloseButtonPressed(ui::Event const&) ./../../chrome/browser/ui/views/tabs/tab.cc:1093:16  

#38 0x5582ba518bd5 in Invoke<void (Tab::\*)(const ui::Event &), Tab \*, const ui::Event &> ./../../base/functional/bind\_internal.h:670:12  

#39 0x5582ba518bd5 in MakeItSo<void (Tab::\*const &)(const ui::Event &), const std::Cr::tuple<base::internal::UnretainedWrapper<Tab, base::RawPtrBanDanglingIfSupported> > &, const ui::Event &> ./../../base/functional/bind\_internal.h:849:12  

#40 0x5582ba518bd5 in RunImpl<void (Tab::\*const &)(const ui::Event &), const std::Cr::tuple<base::internal::UnretainedWrapper<Tab, base::RawPtrBanDanglingIfSupported> > &, 0UL> ./../../base/functional/bind\_internal.h:943:12  

#41 0x5582ba518bd5 in base::internal::Invoker<base::internal::BindState<void (Tab::\*)(ui::Event const&), base::internal::UnretainedWrapper<Tab, base::RawPtrBanDanglingIfSupported>>, void (ui::Event const&)>::Run(base::internal::BindStateBase\*, ui::Event const&) ./../../base/functional/bind\_internal.h:907:12  

#42 0x5582b328ae5e in Run ./../../base/functional/callback.h:333:12  

#43 0x5582b328ae5e in Run ./../../ui/views/controls/button/button.h:103:50  

#44 0x5582b328ae5e in views::Button::NotifyClick(ui::Event const&) ./../../ui/views/controls/button/button.cc:648:15  

#45 0x5582b3286238 in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ./../../ui/views/controls/button/button.cc:67:13  

#46 0x5582b32914e9 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/controls/button/button\_controller.cc:0:0  

#47 0x5582b323aeb8 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ./../../ui/events/scoped\_target\_handler.cc:28:24  

#48 0x5582ace1733f in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:187:12  

#49 0x5582ace16627 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:136:5  

#50 0x5582ace15e88 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:82:14  

#51 0x5582ace15b6e in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:54:15

previously allocated by thread T0 (chrome) here:  

#0 0x5582987b88dd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5582a1d489a8 in make\_unique[content::SyntheticMouseDriver](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:26  

#2 0x5582a1d489a8 in Create ./../../content/browser/renderer\_host/input/synthetic\_pointer\_driver.cc:23:14  

#3 0x5582a1d489a8 in content::SyntheticPointerDriver::Create(content::mojom::GestureSourceType, bool) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_driver.cc:37:17  

#4 0x5582a1d47652 in content::SyntheticPointerAction::ForwardInputEvents(base::TimeTicks const&, content::SyntheticGestureTarget\*) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:31:41  

#5 0x5582a1d3a3a8 in content::SyntheticGestureController::DispatchNextEvent(base::TimeTicks) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:113:48  

#6 0x5582a1d406a6 in operator() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:100:25  

#7 0x5582a1d406a6 in Invoke<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:545:12  

#8 0x5582a1d406a6 in MakeItSo<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const std::Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &> ./../../base/functional/bind\_internal.h:849:12  

#9 0x5582a1d406a6 in RunImpl<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:98:11) &, const std::Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &, 0UL> ./../../base/functional/bind\_internal.h:943:12  

#10 0x5582a1d406a6 in base::internal::Invoker<base::internal::BindState<content::SyntheticGestureController::StartTimer(bool)::$\_0, base::WeakPtr[content::SyntheticGestureController](javascript:void(0);)>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:907:12  

#11 0x5582a8f34b5d in Run ./../../base/functional/callback.h:348:12  

#12 0x5582a8f34b5d in base::MetronomeTimer::OnScheduledTaskInvoked() ./../../base/timer/timer.cc:477:19  

#13 0x5582a8f352df in Invoke<void (base::MetronomeTimer::\*)(), base::MetronomeTimer \*> ./../../base/functional/bind\_internal.h:670:12  

#14 0x5582a8f352df in MakeItSo<void (base::MetronomeTimer::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported> > &> ./../../base/functional/bind\_internal.h:849:12  

#15 0x5582a8f352df in RunImpl<void (base::MetronomeTimer::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported> > &, 0UL> ./../../base/functional/bind\_internal.h:943:12  

#16 0x5582a8f352df in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(), base::internal::UnretainedWrapper<base::MetronomeTimer, base::RawPtrBanDanglingIfSupported>>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:907:12  

#17 0x5582a8e6d439 in Run ./../../base/functional/callback.h:152:12  

#18 0x5582a8e6d439 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:156:32  

#19 0x5582a8eb7c08 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:451:11)> ./../../base/task/common/task\_annotator.h:85:5  

#20 0x5582a8eb7c08 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:449:23  

#21 0x5582a8eb696a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:300:30  

#22 0x5582a8eb9044 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#23 0x5582a8d6af2e in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:404:48  

#24 0x5582a8eb9a7d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:609:12  

#25 0x5582a8df80c8 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#26 0x5582a101a510 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1050:18  

#27 0x5582a1020666 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15  

#28 0x5582a1013d75 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#29 0x5582a7bee114 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:693:10  

#30 0x5582a7bf10fc in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1231:10  

#31 0x5582a7bf09ec in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1087:12  

#32 0x5582a7be92db in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:344:36  

#33 0x5582a7be99f9 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:372:10  

#34 0x5582987bb0ad in ChromeMain ./../../chrome/app/chrome\_main.cc:174:12  

#35 0x7fd3522c0082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium\_version/latest\_asan/chrome+0x1581d49a) (BuildId: 8fe550d3b731bc1b)  

Shadow bytes around the buggy address:  

0x60e0002f4580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x60e0002f4600: 00 00 00 fa fa fa fa fa fa fa f7 fa 00 00 00 00  

0x60e0002f4680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

0x60e0002f4700: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x60e0002f4780: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x60e0002f4800: fa fa f7 fa fd fd fd fd fd fd[fd]fd fd fd fd fd  

0x60e0002f4880: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa  

0x60e0002f4900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e0002f4980: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd  

0x60e0002f4a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e0002f4a80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

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

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==40175==ABORTING  

[40214:40249:1130/055926.801505:ERROR:ssl\_client\_socket\_impl.cc(985)] handshake failed; returned -1, SSL error code 1, net\_error -3

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 1.3 KB)
- [webserver.zip](attachments/webserver.zip) (application/octet-stream, 56.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 21.4 KB)
- [newpoc.zip](attachments/newpoc.zip) (application/octet-stream, 56.7 KB)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 1.3 KB)

## Timeline

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5913702240026624.

### ad...@google.com (2022-12-06)

Unfortunately I can't reproduce this manually. I've tried builds either side of the version you specified:
linux-release/asan-linux-release-1070086.zip
linux-release/asan-linux-release-1079366.zip

but to no avail. The site loads, multiple tabs open of course, and the browser notes that it's being debugged by the extension, but no UaF occurs.

### ad...@google.com (2022-12-07)

I can't reproduce this, but the ASAN trace is convincing that there is some case where this code can UaF.

It looks to me like the most plausible candidate would be synthetic_gesture_controller.cc; it is destroying gestures while they're still in flight.

A recent change here is https://source.chromium.org/chromium/chromium/src/+/0f1038c0d3fa7102baf5066664ab3175173ab8ef. It might not be the culprit but bokan@, I hope you don't mind having a look?

Setting FoundIn-107 on the assumption that the above CL might be the culprit. Setting Security_Severity-High, because this is a browser process UaF that's mitigated by the need to install an extension. Reporter, you say this code path can be triggered somehow without an extension - please provide details of how - if there aren't mitigating factors on that code path we might want to bump this up to Critical.

[Monorail components: Blink>Input Internals>Core]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2022-12-07)

Similar to https://crbug.com/chromium/1395354 though different - I had a hard time reproducing that one yesterday...

I'm a bit more puzzled by this one as it looks like the UAF happens inside a the timer task posted from  SyntheticGestureController::StartTimer. However, the UAF'd pointer is deleted in the SyntheticGestureController destructor which should also destruct the timer which cancels the timer task...

I believe this stack (unlike https://crbug.com/chromium/1395354) relies on --enable-gpu-benchmarking being set so I don't think this affects general users in the wild. Reporter, please correct me if I'm wrong here.

I also can't reproduce the UAF crash locally - I'm using an ASAN build with gn args:

dcheck_always_on = true
is_asan = true
is_component_build = false
is_debug = false
symbol_level = 1
use_goma = true

Reporter, can you please help me reproduce this?

### an...@chromium.org (2022-12-15)

Hi 0xasnine@gmail.com, can you provide any more information to help reproduce this bug on our end? Thanks!

### [Deleted User] (2022-12-22)

bokan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2023-01-03)

ping 0xasnine@ - do I have the steps in #7 correct?

### [Deleted User] (2023-01-18)

bokan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-01-27)

marshal here -
@reporter, another friendly ping! (: please take a look at https://crbug.com/chromium/1394736#c7 to help us repro the bug 

### [Deleted User] (2023-01-29)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### 0x...@gmail.com (2023-01-30)

Hi, I download the latest asan build gs://chromium-browser-asan/linux-release/asan-linux-release-1098545.zip
This issue can been reproduced in this version.
I reproduced this issue in a Linux Virtual Machine. 
It seems than it is more stable to reproduce this issue with more http://localhost:8000/pointertest.html tabs.
./chrome --user-data-dir=/tmp/aaa --enable-gpu-benchmarking --load-extension="extension_path" http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html  http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html http://localhost:8000/pointertest.html

### 0x...@gmail.com (2023-01-31)

Hi, I submit a new poc to reproduce in Windows stably.
Download the latest asan windows build.

chrome.exe --user-data-dir=C:/tmp/any--enable-gpu-benchmarking --load-extension="extensionpath" http://localhost:8000/newpoc.html

### bo...@chromium.org (2023-02-06)

Thank you - I'm still unable to reproduce on Linux but I was able to reproduce on a personal Windows box with a downloaded ASAN binary. I'm now reproduce on a development machine where I can build and verify a fix.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-02-10)

Apologies for the delay - after several days of waiting on a Windows-capable build machine it didn't reproduce there so I had to build - slowly - on my personal box. But I think I see the problem. The default ASAN malloc context stack size hides the issue but expanding that a bit makes it clear:

=================================================================
==202572==ERROR: AddressSanitizer: heap-use-after-free on address 0x12368d50d438 at pc 0x7ff92ab1bc6d bp 0x007aff7fe140 sp 0x007aff7fe188
WRITE of size 4 at 0x12368d50d438 thread T0
    #0 0x7ff92ab1bc6c in blink::WebInputEvent::SetType C:\chrome\src\third_party\blink\public\common\input\web_input_event.h:309
    #1 0x7ff92ab1bc6c in content::SyntheticMouseDriver::DispatchEvent(class content::SyntheticGestureTarget *, class base::TimeTicks const &) C:\chrome\src\content\browser\renderer_host\input\synthetic_mouse_driver.cc:25:18
    #2 0x7ff92ab1fb04 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(class base::TimeTicks const &, class content::SyntheticGestureTarget *) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:115:22
    #3 0x7ff92ab1ee82 in content::SyntheticPointerAction::ForwardInputEvents(class base::TimeTicks const &, class content::SyntheticGestureTarget *) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:41:12
    #4 0x7ff92ab118e5 in content::SyntheticGestureController::DispatchNextEvent(class base::TimeTicks) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:122:48
    #5 0x7ff92ab163b3 in content::SyntheticGestureController::StartTimer::<lambda_1>::operator() C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:105
    #6 0x7ff92ab163b3 in base::internal::FunctorTraits<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',void>::Invoke C:\chrome\src\base\functional\bind_internal.h:620
    #7 0x7ff92ab163b3 in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #8 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #9 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::Run C:\chrome\src\base\functional\bind_internal.h:983:12
    #10 0x7ff9305d236f in base::RepeatingCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:348
    #11 0x7ff9305d236f in base::MetronomeTimer::OnScheduledTaskInvoked(void) C:\chrome\src\base\timer\timer.cc:474:19
    #12 0x7ff9305d2bfe in base::internal::FunctorTraits<void (base::DeadlineTimer::*)(),void>::Invoke C:\chrome\src\base\functional\bind_internal.h:745
    #13 0x7ff9305d2bfe in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #14 0x7ff9305d2bfe in base::internal::Invoker<base::internal::BindState<void (base::DeadlineTimer::*)(),base::internal::UnretainedWrapper<base::DeadlineTimer,base::unretained_traits::MayNotDangle> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #15 0x7ff9305d2bfe in base::internal::Invoker<struct base::internal::BindState<void (__cdecl base::MetronomeTimer::*)(void), class base::internal::UnretainedWrapper<class base::MetronomeTimer, struct base::unretained_traits::MayNotDangle>>, (void)>::Run(class base::internal::BindStateBase *) C:\chrome\src\base\functional\bind_internal.h:983:12
    #16 0x7ff930531653 in base::OnceCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:152
    #17 0x7ff930531653 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\chrome\src\base\task\common\task_annotator.cc:165:32
    #18 0x7ff933ef5e36 in base::TaskAnnotator::RunTask C:\chrome\src\base\task\common\task_annotator.h:87
    #19 0x7ff933ef5e36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489:23
    #20 0x7ff933ef3b60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340:30
    #21 0x7ff930634ae4 in base::MessagePumpForUI::DoRunLoop(void) C:\chrome\src\base\message_loop\message_pump_win.cc:212:67
    #22 0x7ff93063191b in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\chrome\src\base\message_loop\message_pump_win.cc:78:3
    #23 0x7ff933ef9646 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649:12
    #24 0x7ff9304a7218 in base::RunLoop::Run(class base::Location const &) C:\chrome\src\base\run_loop.cc:140:14
    #25 0x7ff929cb1487 in content::BrowserMainLoop::RunMainMessageLoop(void) C:\chrome\src\content\browser\browser_main_loop.cc:1066:18
    #26 0x7ff929cb920c in content::BrowserMainRunnerImpl::Run(void) C:\chrome\src\content\browser\browser_main_runner_impl.cc:162:15
    #27 0x7ff929ca8e81 in content::BrowserMain(struct content::MainFunctionParams) C:\chrome\src\content\browser\browser_main.cc:32:28
    #28 0x7ff92eb7dbd0 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\chrome\src\content\app\content_main_runner_impl.cc:715:10
    #29 0x7ff92eb8287f in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\chrome\src\content\app\content_main_runner_impl.cc:1266:10
    #30 0x7ff92eb819c3 in content::ContentMainRunnerImpl::Run(void) C:\chrome\src\content\app\content_main_runner_impl.cc:1120:12
    #31 0x7ff92eb7be3c in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\chrome\src\content\app\content_main.cc:335:36
    #32 0x7ff92eb7c8dc in content::ContentMain(struct content::ContentMainParams) C:\chrome\src\content\app\content_main.cc:363:10
    #33 0x7ff9208216a4 in ChromeMain C:\chrome\src\chrome\app\chrome_main.cc:190:12
    #34 0x7ff7736e6a29 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\chrome\src\chrome\app\main_dll_loader_win.cc:166:12
    #35 0x7ff7736e3061 in main C:\chrome\src\chrome\app\chrome_exe_main_win.cc:391:20
    #36 0x7ff773c1ef7b in invoke_main d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #37 0x7ff773c1ef7b in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ff9d5927033  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #39 0x7ff9d6102650  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x12368d50d438 is located 56 bytes inside of 160-byte region [0x12368d50d400,0x12368d50d4a0)
freed by thread T0 here:
    #0 0x7ff77379914d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff92ab1d865 in content::SyntheticMouseDriver::`scalar deleting dtor'(unsigned int) C:\chrome\src\content\browser\renderer_host\input\synthetic_mouse_driver.cc:18:47
    #2 0x7ff92ab1ea33 in std::Cr::default_delete<content::SyntheticPointerDriver>::operator() C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:65
    #3 0x7ff92ab1ea33 in std::Cr::unique_ptr<content::SyntheticPointerDriver,std::Cr::default_delete<content::SyntheticPointerDriver> >::reset C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:297
    #4 0x7ff92ab1ea33 in std::Cr::unique_ptr<content::SyntheticPointerDriver,std::Cr::default_delete<content::SyntheticPointerDriver> >::~unique_ptr C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:263
    #5 0x7ff92ab1ea33 in content::SyntheticPointerAction::~SyntheticPointerAction(void) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:16:52
    #6 0x7ff92ab21385 in content::SyntheticPointerAction::`scalar deleting dtor'(unsigned int) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.h:16
    #7 0x7ff924b56a02 in std::Cr::destroy_at C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\construct_at.h:91
    #8 0x7ff924b56a02 in std::Cr::allocator_traits<std::Cr::allocator<std::Cr::unique_ptr<policy::DeviceManagementService::Job,std::Cr::default_delete<policy::DeviceManagementService::Job> > > >::destroy C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\allocator_traits.h:323
    #9 0x7ff924b56a02 in std::Cr::vector<std::Cr::unique_ptr<policy::DeviceManagementService::Job,std::Cr::default_delete<policy::DeviceManagementService::Job> >,std::Cr::allocator<std::Cr::unique_ptr<policy::DeviceManagementService::Job,std::Cr::default_delete<policy::DeviceManagementService::Job> > > >::__base_destruct_at_end C:\chrome\src\buildtools\third_party\libc++\trunk\include\vector:836
    #10 0x7ff924b56a02 in std::Cr::vector<class std::Cr::unique_ptr<class content::WebContents, struct std::Cr::default_delete<class content::WebContents>>, class std::Cr::allocator<class std::Cr::unique_ptr<class content::WebContents, struct std::Cr::default_delete<class content::WebContents>>>>::__destruct_at_end(class std::Cr::unique_ptr<class content::WebContents, struct std::Cr::default_delete<class content::WebContents>> *) C:\chrome\src\buildtools\third_party\libc++\trunk\include\vector:724:9
    #11 0x7ff92ab0fae4 in std::Cr::vector<std::Cr::unique_ptr<content::SyntheticGesture,std::Cr::default_delete<content::SyntheticGesture> >,std::Cr::allocator<std::Cr::unique_ptr<content::SyntheticGesture,std::Cr::default_delete<content::SyntheticGesture> > > >::erase C:\chrome\src\buildtools\third_party\libc++\trunk\include\vector:1631
    #12 0x7ff92ab0fae4 in content::SyntheticGestureController::GestureAndCallbackQueue::Pop(void) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.h:105:17
    #13 0x7ff92ab0f230 in content::SyntheticGestureController::~SyntheticGestureController(void) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:33:28
    #14 0x7ff92ab124e7 in content::SyntheticGestureController::`scalar deleting dtor'(unsigned int) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.h:28
    #15 0x7ff92af99992 in std::Cr::default_delete<content::SyntheticGestureController>::operator() C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:65
    #16 0x7ff92af99992 in std::Cr::unique_ptr<content::SyntheticGestureController,std::Cr::default_delete<content::SyntheticGestureController> >::reset C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:297
    #17 0x7ff92af99992 in content::RenderWidgetHostImpl::SetView C:\chrome\src\content\browser\renderer_host\render_widget_host_impl.cc:573
    #18 0x7ff92af99992 in content::RenderWidgetHostImpl::ViewDestroyed(void) C:\chrome\src\content\browser\renderer_host\render_widget_host_impl.cc:1391:3
    #19 0x7ff92affaf5f in content::RenderWidgetHostViewAura::~RenderWidgetHostViewAura(void) C:\chrome\src\content\browser\renderer_host\render_widget_host_view_aura.cc:2177:11
    #20 0x7ff92b000313 in content::RenderWidgetHostViewAura::`scalar deleting dtor'(unsigned int) C:\chrome\src\content\browser\renderer_host\render_widget_host_view_aura.h:2173
    #21 0x7ff932427d34 in aura::Window::~Window(void) C:\chrome\src\ui\aura\window.cc:229:16
    #22 0x7ff93243fd8d in aura::Window::`scalar deleting dtor'(unsigned int) C:\chrome\src\ui\aura\window.cc:184:19
    #23 0x7ff92afa6d41 in content::RenderWidgetHostImpl::RendererExited(void) C:\chrome\src\content\browser\renderer_host\render_widget_host_impl.cc:2213:12
    #24 0x7ff92af7ce42 in content::RenderViewHostImpl::RenderProcessExited(class content::RenderProcessHost *, struct content::ChildProcessTerminationInfo const &) C:\chrome\src\content\browser\renderer_host\render_view_host_impl.cc:745:16
    #25 0x7ff92af3d2b6 in content::RenderProcessHostImpl::ProcessDied(struct content::ChildProcessTerminationInfo const &) C:\chrome\src\content\browser\renderer_host\render_process_host_impl.cc:4795:14
    #26 0x7ff92af3c82e in content::RenderProcessHostImpl::FastShutdownIfPossible(unsigned __int64, bool) C:\chrome\src\content\browser\renderer_host\render_process_host_impl.cc:3657:3
    #27 0x7ff93362b0f6 in TabStripModel::CloseWebContentses(class base::span<class content::WebContents *const, -1>, unsigned int, struct TabStripModel::DetachNotifications *) C:\chrome\src\chrome\browser\ui\tabs\tab_strip_model.cc:1885:19
    #28 0x7ff933615aed in TabStripModel::CloseTabs(class base::span<class content::WebContents *const, -1>, unsigned int) C:\chrome\src\chrome\browser\ui\tabs\tab_strip_model.cc:1840:7
    #29 0x7ff9336166a2 in TabStripModel::CloseWebContentsAt(int, unsigned int) C:\chrome\src\chrome\browser\ui\tabs\tab_strip_model.cc:702:10
    #30 0x7ff93d197d2e in BrowserTabStripController::CloseTab(int) C:\chrome\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:344:11
    #31 0x7ff93d1a95b6 in TabStrip::CloseTabInternal(int, enum CloseTabSource) C:\chrome\src\chrome\browser\ui\views\tabs\tab_strip.cc:1975:16
    #32 0x7ff93d1a8f64 in TabStrip::CloseTab(class Tab *, enum CloseTabSource) C:\chrome\src\chrome\browser\ui\views\tabs\tab_strip.cc:1445:5
    #33 0x7ff9418469e5 in Tab::OnMouseReleased(class ui::MouseEvent const &) C:\chrome\src\chrome\browser\ui\views\tabs\tab.cc:535:20
    #34 0x7ff9301a3711 in views::View::ProcessMouseReleased(class ui::MouseEvent const &) C:\chrome\src\ui\views\view.cc:3181:5
    #35 0x7ff931b10dc4 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:187:12
    #36 0x7ff931b0fe3e in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:136:5
    #37 0x7ff931b0f519 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:82:14
    #38 0x7ff931b0f0e5 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:54:15
    #39 0x7ff9339048c1 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\chrome\src\ui\views\widget\root_view.cc:528:9
    #40 0x7ff9301d6122 in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\chrome\src\ui\views\widget\widget.cc:1729:20
    #41 0x7ff93d89a371 in views::DesktopNativeWidgetAura::OnMouseEvent(class ui::MouseEvent *) C:\chrome\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1294:30
    #42 0x7ff931b10dc4 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:187:12
    #43 0x7ff931b0fe3e in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:136:5
    #44 0x7ff931b0f519 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:82:14
    #45 0x7ff931b0f0e5 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\chrome\src\ui\events\event_dispatcher.cc:54:15
    #46 0x7ff937b1443b in ui::EventProcessor::OnEventFromSource(class ui::Event *) C:\chrome\src\ui\events\event_processor.cc:56:17
    #47 0x7ff932425bb3 in aura::EventInjector::Inject(class aura::WindowTreeHost *, class ui::Event *) C:\chrome\src\ui\aura\event_injector.cc:35:32
    #48 0x7ff92ab191bd in content::SyntheticGestureTargetAura::DispatchWebMouseEventToPlatform(class blink::WebMouseEvent const &, class ui::LatencyInfo const &) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_target_aura.cc:204:25
    #49 0x7ff92ab1a740 in content::SyntheticGestureTargetBase::DispatchInputEventToPlatform(class blink::WebInputEvent const &) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_target_base.cc:71:7
    #50 0x7ff92ab1bc2b in content::SyntheticMouseDriver::DispatchEvent(class content::SyntheticGestureTarget *, class base::TimeTicks const &) C:\chrome\src\content\browser\renderer_host\input\synthetic_mouse_driver.cc:24:13
    #51 0x7ff92ab1fb04 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(class base::TimeTicks const &, class content::SyntheticGestureTarget *) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:115:22
    #52 0x7ff92ab1ee82 in content::SyntheticPointerAction::ForwardInputEvents(class base::TimeTicks const &, class content::SyntheticGestureTarget *) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:41:12
    #53 0x7ff92ab118e5 in content::SyntheticGestureController::DispatchNextEvent(class base::TimeTicks) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:122:48
    #54 0x7ff92ab163b3 in content::SyntheticGestureController::StartTimer::<lambda_1>::operator() C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:105
    #55 0x7ff92ab163b3 in base::internal::FunctorTraits<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',void>::Invoke C:\chrome\src\base\functional\bind_internal.h:620
    #56 0x7ff92ab163b3 in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #57 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #58 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::Run C:\chrome\src\base\functional\bind_internal.h:983:12
    #59 0x7ff9305d236f in base::RepeatingCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:348
    #60 0x7ff9305d236f in base::MetronomeTimer::OnScheduledTaskInvoked(void) C:\chrome\src\base\timer\timer.cc:474:19
    #61 0x7ff9305d2bfe in base::internal::FunctorTraits<void (base::DeadlineTimer::*)(),void>::Invoke C:\chrome\src\base\functional\bind_internal.h:745
    #62 0x7ff9305d2bfe in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #63 0x7ff9305d2bfe in base::internal::Invoker<base::internal::BindState<void (base::DeadlineTimer::*)(),base::internal::UnretainedWrapper<base::DeadlineTimer,base::unretained_traits::MayNotDangle> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #64 0x7ff9305d2bfe in base::internal::Invoker<struct base::internal::BindState<void (__cdecl base::MetronomeTimer::*)(void), class base::internal::UnretainedWrapper<class base::MetronomeTimer, struct base::unretained_traits::MayNotDangle>>, (void)>::Run(class base::internal::BindStateBase *) C:\chrome\src\base\functional\bind_internal.h:983:12
    #65 0x7ff930531653 in base::OnceCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:152
    #66 0x7ff930531653 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\chrome\src\base\task\common\task_annotator.cc:165:32
    #67 0x7ff933ef5e36 in base::TaskAnnotator::RunTask C:\chrome\src\base\task\common\task_annotator.h:87
    #68 0x7ff933ef5e36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489:23
    #69 0x7ff933ef3b60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340:30
    #70 0x7ff930634ae4 in base::MessagePumpForUI::DoRunLoop(void) C:\chrome\src\base\message_loop\message_pump_win.cc:212:67
    #71 0x7ff93063191b in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\chrome\src\base\message_loop\message_pump_win.cc:78:3
    #72 0x7ff933ef9646 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649:12
    #73 0x7ff9304a7218 in base::RunLoop::Run(class base::Location const &) C:\chrome\src\base\run_loop.cc:140:14
    #74 0x7ff929cb1487 in content::BrowserMainLoop::RunMainMessageLoop(void) C:\chrome\src\content\browser\browser_main_loop.cc:1066:18
    #75 0x7ff929cb920c in content::BrowserMainRunnerImpl::Run(void) C:\chrome\src\content\browser\browser_main_runner_impl.cc:162:15
    #76 0x7ff929ca8e81 in content::BrowserMain(struct content::MainFunctionParams) C:\chrome\src\content\browser\browser_main.cc:32:28
    #77 0x7ff92eb7dbd0 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\chrome\src\content\app\content_main_runner_impl.cc:715:10

previously allocated by thread T0 here:
    #0 0x7ff77379924d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff948dab79e in operator new(unsigned __int64) d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff92ab21504 in std::Cr::make_unique C:\chrome\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:686
    #3 0x7ff92ab21504 in content::SyntheticPointerDriver::Create(enum content::mojom::GestureSourceType) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_driver.cc:23:14
    #4 0x7ff92ab2160c in content::SyntheticPointerDriver::Create(enum content::mojom::GestureSourceType, bool) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_driver.cc:37:17
    #5 0x7ff92ab1ec99 in content::SyntheticPointerAction::ForwardInputEvents(class base::TimeTicks const &, class content::SyntheticGestureTarget *) C:\chrome\src\content\browser\renderer_host\input\synthetic_pointer_action.cc:29:44
    #6 0x7ff92ab118e5 in content::SyntheticGestureController::DispatchNextEvent(class base::TimeTicks) C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:122:48
    #7 0x7ff92ab163b3 in content::SyntheticGestureController::StartTimer::<lambda_1>::operator() C:\chrome\src\content\browser\renderer_host\input\synthetic_gesture_controller.cc:105
    #8 0x7ff92ab163b3 in base::internal::FunctorTraits<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',void>::Invoke C:\chrome\src\base\functional\bind_internal.h:620
    #9 0x7ff92ab163b3 in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #10 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #11 0x7ff92ab163b3 in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/renderer_host/input/synthetic_gesture_controller.cc:101:11',base::WeakPtr<content::SyntheticGestureController> >,void ()>::Run C:\chrome\src\base\functional\bind_internal.h:983:12
    #12 0x7ff9305d236f in base::RepeatingCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:348
    #13 0x7ff9305d236f in base::MetronomeTimer::OnScheduledTaskInvoked(void) C:\chrome\src\base\timer\timer.cc:474:19
    #14 0x7ff9305d2bfe in base::internal::FunctorTraits<void (base::DeadlineTimer::*)(),void>::Invoke C:\chrome\src\base\functional\bind_internal.h:745
    #15 0x7ff9305d2bfe in base::internal::InvokeHelper<0,void,0>::MakeItSo C:\chrome\src\base\functional\bind_internal.h:924
    #16 0x7ff9305d2bfe in base::internal::Invoker<base::internal::BindState<void (base::DeadlineTimer::*)(),base::internal::UnretainedWrapper<base::DeadlineTimer,base::unretained_traits::MayNotDangle> >,void ()>::RunImpl C:\chrome\src\base\functional\bind_internal.h:1019
    #17 0x7ff9305d2bfe in base::internal::Invoker<struct base::internal::BindState<void (__cdecl base::MetronomeTimer::*)(void), class base::internal::UnretainedWrapper<class base::MetronomeTimer, struct base::unretained_traits::MayNotDangle>>, (void)>::Run(class base::internal::BindStateBase *) C:\chrome\src\base\functional\bind_internal.h:983:12
    #18 0x7ff930531653 in base::OnceCallback<void ()>::Run C:\chrome\src\base\functional\callback.h:152
    #19 0x7ff930531653 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\chrome\src\base\task\common\task_annotator.cc:165:32
    #20 0x7ff933ef5e36 in base::TaskAnnotator::RunTask C:\chrome\src\base\task\common\task_annotator.h:87
    #21 0x7ff933ef5e36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:489:23
    #22 0x7ff933ef3b60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:340:30
    #23 0x7ff930634ae4 in base::MessagePumpForUI::DoRunLoop(void) C:\chrome\src\base\message_loop\message_pump_win.cc:212:67
    #24 0x7ff93063191b in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\chrome\src\base\message_loop\message_pump_win.cc:78:3
    #25 0x7ff933ef9646 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\chrome\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:649:12
    #26 0x7ff9304a7218 in base::RunLoop::Run(class base::Location const &) C:\chrome\src\base\run_loop.cc:140:14
    #27 0x7ff929cb1487 in content::BrowserMainLoop::RunMainMessageLoop(void) C:\chrome\src\content\browser\browser_main_loop.cc:1066:18
    #28 0x7ff929cb920c in content::BrowserMainRunnerImpl::Run(void) C:\chrome\src\content\browser\browser_main_runner_impl.cc:162:15
    #29 0x7ff929ca8e81 in content::BrowserMain(struct content::MainFunctionParams) C:\chrome\src\content\browser\browser_main.cc:32:28
    #30 0x7ff92eb7dbd0 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\chrome\src\content\app\content_main_runner_impl.cc:715:10
    #31 0x7ff92eb8287f in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\chrome\src\content\app\content_main_runner_impl.cc:1266:10
    #32 0x7ff92eb819c3 in content::ContentMainRunnerImpl::Run(void) C:\chrome\src\content\app\content_main_runner_impl.cc:1120:12
    #33 0x7ff92eb7be3c in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\chrome\src\content\app\content_main.cc:335:36
    #34 0x7ff92eb7c8dc in content::ContentMain(struct content::ContentMainParams) C:\chrome\src\content\app\content_main.cc:363:10
    #35 0x7ff9208216a4 in ChromeMain C:\chrome\src\chrome\app\chrome_main.cc:190:12
    #36 0x7ff7736e6a29 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\chrome\src\chrome\app\main_dll_loader_win.cc:166:12
    #37 0x7ff7736e3061 in main C:\chrome\src\chrome\app\chrome_exe_main_win.cc:391:20
    #38 0x7ff773c1ef7b in invoke_main d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #39 0x7ff773c1ef7b in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ff9d5927033  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #41 0x7ff9d6102650  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

The memory is freed while DispatchNextEvent is on the stack - meaning the SyntheticGestureController dispatches an event that causes the RenderView and itself to be destroyed. This is unexpected and SyntheticGestureController has code that comes after that call which is where we get the UAF. I should have a fix shortly.

### bo...@chromium.org (2023-02-13)

+mustaq@ who I've added as reviewer on the fix.

### gi...@appspot.gserviceaccount.com (2023-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9af981b177594955572bf61afcc15006ba59808d

commit 9af981b177594955572bf61afcc15006ba59808d
Author: David Bokan <bokan@chromium.org>
Date: Thu Feb 16 15:29:00 2023

Fix UAF in SyntheticGesture

A synthetic gesture can lead to synchronously closing the tab that owns
the controller. This can happen with e.g. a click mouse gesture over the
tab close button. This is a problem with the current controller,
gesture, target code since they read/write local memory after
dispatching input events.

This CL adds a WeakPtr from the SyntheticGesture back to the controller
so it can detect when the controller was destructed and avoid touching
any local memory.

There's no test as this behavior depends on OS specific UI so writing
so writing a reliable test is tricky. I was only able to repro the
steps given in https://crbug.com/1394736#c15 on 1/4 computers but
I've verified this CL in an ASAN build on that machine.

Bug: 1394736
Change-Id: If76447728e7e63a85da7ddbf1610482ec8be7fa2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4241725
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1106204}

[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_pinch_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_gesture_controller.h
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_touch_driver.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_mouse_driver.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_gesture.h
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_gesture_controller.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.cc
[modify] https://crrev.com/9af981b177594955572bf61afcc15006ba59808d/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc


### bo...@chromium.org (2023-02-16)

The fix above worked for me locally - 0xasnine@: could you verify the fix on your end once this is in Canary/ASAN builds (expect tomorrow)?

The landed revision is r1106204 - should be in Canary version 112.0.5560.0

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-17)

Requesting merge to stable M110 because latest trunk commit (1106204) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1106204) appears to be after beta branch point (1097615).

Merge review required: M110 is already shipping to stable.

Merge review required: M111 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-18)

Requesting merge to stable M110 because latest trunk commit (1106204) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1106204) appears to be after beta branch point (1097615).

Merge review required: M110 is already shipping to stable.

Merge review required: M111 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-20)

Requesting merge to stable M110 because latest trunk commit (1106204) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1106204) appears to be after beta branch point (1097615).

Merge review required: M110 is already shipping to stable.

Merge review required: M111 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-21)

This CL adds weakptr as well as some DCHECKs, however, there's been 5 days of bake time on Canary and I'm not seeing any issues so far. 
M111 merge approved, please merge this fix to branch 5563 at soonest so this fix can be included in M111 beta tomorrow. 

Not yet approving for M110 merge, as M110/Stable release is today and some Critical severity fixes are being included into that last minute. Will re-assess for m110 merge tomorrow or Thursday. TY. 

### bo...@chromium.org (2023-02-21)

Should have noted - this doesn't affect typical users as it requires a command line flag (--enable-gpu-benchmarking) to be enabled or a connection via DevTools protocol. OTOH, this also means the fix is low risk as it mainly affects testing code paths.

+amyressler@: I'd be comfortable merging to M111 if you think there's value but wondering if this changes your assessment.



### am...@chromium.org (2023-02-23)

Thanks for calling that out bokan@. Based on https://crbug.com/chromium/1394736#c4 I wasn't sure if --enable-gpu-benchmarking was required; which appears based on my limited spelunking, to be enabled primarily (or solely) for testing. 
While (as you mention) this is a low risk fix, if the above is correct, I'd consider this issue SI-None and not requiring a backmerge and we should let this fix naturally matriculate from canary -> stable without backmerge.  

### bo...@chromium.org (2023-02-23)

Yes, as far as I can tell this code is only reachable when

a) --enable-gpu-benchmarking is set, typically used for tests and performance telemetry
b) DevTools protocol

### am...@chromium.org (2023-02-23)

Thank you for the confirmation; updating as SI-None and removing merge labels accordingly. 

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, asnine! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. The reward amount was decided based on this requiring an extension, but more importantly the reliance on --enable-gpu-benchmarking, which would only be leveraged in testing. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47138b0cb0581eb54dbdf2baf648eb86a82bd8a4

commit 47138b0cb0581eb54dbdf2baf648eb86a82bd8a4
Author: David Bokan <bokan@chromium.org>
Date: Wed Mar 29 19:11:25 2023

Fix UAF in SyntheticPointerAction

https://crrev.com/c/4241725 fixed a UAF where a gesture action causes
the browser window to be closed and the gesture controller to be
destroyed. It did so by checking for the controller's destruction after
any click-type event dispatch and early returning to ensure we're not
touching any of the gesture's members after destroying it.

That CL missed one case in SyntheticPointerAction. While
ForwardInputEvents does check for destruction and return GESTURE_ABORT,
the call to ForwardTouchOrMouseInputEvents has some code after dispatch
that will read memory belonging to |this|. This CL adds an early return
in this case as well.

Bug: 1427918,1394736
Change-Id: I08bf3a42f0bcaa44b2a795021fb5f8e32b35a67a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375537
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123742}

[modify] https://crrev.com/47138b0cb0581eb54dbdf2baf648eb86a82bd8a4/content/browser/renderer_host/input/synthetic_pointer_action.cc


### gi...@appspot.gserviceaccount.com (2023-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/865adbfec6b41286880068cd28d8efee482bd565

commit 865adbfec6b41286880068cd28d8efee482bd565
Author: David Bokan <bokan@chromium.org>
Date: Thu Apr 13 20:12:19 2023

Synthetic Gestures: Checks of weak ptr happen on stack

https://crrev.com/c/4241725 added a WeakPtr to the
SyntheticGestureController so gestures could tell when they caused
deletion of the controller and return without touching deleted memory.

Unfortunately, that CL (and a followup in https://crrev.com/c/4375537)
made the silly mistake (in some callsites) of checking the WeakPtr
member directly. If the object was deleted, this is itself a UAF.

This CL changes those call sites to place the WeakPtr into a stack
variable before dispatching an event. When event dispatch returns,
check this stack variable rather than the (possibly deleted) member.

Also change related DCHECKs to CHECK as per [1]

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/styleguide/c++/checks.md

Bug: 1427918,1394736
Change-Id: I1835eaeeafb2c75fca4034556d9bced342d9d5f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387914
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1130058}

[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc
[modify] https://crrev.com/865adbfec6b41286880068cd28d8efee482bd565/content/browser/renderer_host/render_widget_host_impl.h


### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1394736?no_tracker_redirect=1

[Multiple monorail components: Blink>Input, Internals>Core]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061975)*
