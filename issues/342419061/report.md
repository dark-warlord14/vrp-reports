# UaF in LensOverlayController::~LensOverlayController

| Field | Value |
|-------|-------|
| **Issue ID** | [342419061](https://issues.chromium.org/issues/342419061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Linux, Windows |
| **Chrome Version** | 127.0.6496.0  |
| **Reporter** | ch...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2024-05-24 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Run Chromium
2. Open a new window
3. Right-click in the opened window and select "Search with Google Lens" and move the tab to other window
4. Close the tab

# Problem Description

UaF in LensOverlayController::~LensOverlayController

# Summary

UaF in LensOverlayController::~LensOverlayController

# Custom Questions

#### Type of crash:

Browser

#### Crash state:

=26808==ERROR: AddressSanitizer: heap-use-after-free on address 0x514000124770 at pc 0x55a9f340b300 bp 0x7ffd755478b0 sp 0x7ffd755478a8
READ of size 8 at 0x514000124770 thread T0 (chrome)
==26808==WARNING: invalid path to external symbolizer!
==26808==WARNING: Failed to use and restart external symbolizer!
#0 0x55a9f340b2ff in begin ./../../third\_party/libc++/src/include/vector:1387:28
#1 0x55a9f340b2ff in begin<std::\_\_Cr::vector<base::internal::CheckedObserverAdapter, std::\_\_Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:34:37
#2 0x55a9f340b2ff in begin<std::\_\_Cr::vector<base::internal::CheckedObserverAdapter, std::\_\_Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:80:10
#3 0x55a9f340b2ff in find\_if<std::\_\_Cr::vector<base::internal::CheckedObserverAdapter, std::\_\_Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &, (lambda at ../../base/observer\_list.h:309:21), std::\_\_Cr::identity, std::\_\_Cr::random\_access\_iterator\_tag> ./../../base/ranges/algorithm.h:495:26
#4 0x55a9f340b2ff in base::ObserverList<SidePanelViewStateObserver, false, true, base::internal::CheckedObserverAdapter>::RemoveObserver(SidePanelViewStateObserver const\*) ./../../base/observer\_list.h:308:21
#5 0x55a9f27724a2 in RemoveObserver ./../../chrome/browser/ui/views/side\_panel/side\_panel\_coordinator.h:358:13
#6 0x55a9f27724a2 in Reset ./../../base/scoped\_observation.h:115:7
#7 0x55a9f27724a2 in base::ScopedObservation<SidePanelCoordinator, SidePanelViewStateObserver>::~ScopedObservation() ./../../base/scoped\_observation.h:101:26
#8 0x55a9f27712b7 in LensOverlayController::~LensOverlayController() ./../../chrome/browser/ui/lens/lens\_overlay\_controller.cc:212:1
#9 0x55a9f27726a3 in LensOverlayController::~LensOverlayController() ./../../chrome/browser/ui/lens/lens\_overlay\_controller.cc:196:49
#10 0x55a9f227027a in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#11 0x55a9f227027a in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#12 0x55a9f227027a in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#13 0x55a9f227027a in ~TabFeatures ./../../chrome/browser/ui/tabs/tab\_features.cc:40:27
#14 0x55a9f227027a in tabs::TabFeatures::~TabFeatures() ./../../chrome/browser/ui/tabs/tab\_features.cc:40:27
#15 0x55a9f2268884 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#16 0x55a9f2268884 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#17 0x55a9f2268884 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#18 0x55a9f2268884 in tabs::TabModel::~TabModel() ./../../chrome/browser/ui/tabs/tab\_model.cc:33:21
#19 0x55a9f227d55c in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#20 0x55a9f227d55c in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#21 0x55a9f227d55c in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:599:16
#22 0x55a9f22890c8 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul, content::WebContents\* const\*>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:2184:5
#23 0x55a9f228a5b9 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:796:3
#24 0x55a9f20c61d7 in chrome::CloseWebContents(Browser\*, content::WebContents\*, bool) ./../../chrome/browser/ui/browser\_tabstrip.cc:110:31
#25 0x55a9d5dbdfda in content::WebContentsImpl::Close() ./../../content/browser/web\_contents/web\_contents\_impl.cc:8398:16
#26 0x55a9d55fd6f4 in Invoke<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), const base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);) &, content::RenderFrameHostImpl::ClosePageSource> ./../../base/functional/bind\_internal.h:738:12
#27 0x55a9d55fd6f4 in MakeItSo<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource> > ./../../base/functional/bind\_internal.h:954:5
#28 0x55a9d55fd6f4 in void base::internal::Invoker<base::internal::FunctorTraits<void (content::RenderFrameHostImpl::*&&)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);)&&, content::RenderFrameHostImpl::ClosePageSource&&>, base::internal::BindState<true, true, false, void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, void ()>::RunImpl<void (content::RenderFrameHostImpl::*)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, 0ul, 1ul>(void (content::RenderFrameHostImpl::*&&)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>) ./../../base/functional/bind\_internal.h:1067:14
#29 0x55a9cf051879 in Run ./../../base/functional/callback.h:156:12
#30 0x55a9cf051879 in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:18866:26
#31 0x55a9de61f26d in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1031:41
#32 0x55a9de63aa6a in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19
#33 0x55a9de623cb5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:721:20
#34 0x55a9df41e60e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc\_mojo\_bootstrap.cc:1221:24
#35 0x55a9df41fc73 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind\_internal.h:738:12
#36 0x55a9df41fc73 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind\_internal.h:930:12
#37 0x55a9df41fc73 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::\_\_Cr::tuple<scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1067:14
#38 0x55a9df41fc73 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController\*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped\_refptr[IPC::ChannelAssociatedGroupController](javascript:void(0);), mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind\_internal.h:980:12
#39 0x55a9dcf2cd24 in Run ./../../base/functional/callback.h:156:12
#40 0x55a9dcf2cd24 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#41 0x55a9dcf90046 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#42 0x55a9dcf90046 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#43 0x55a9dcf8ef5d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#44 0x55a9dcf90d8a in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#45 0x55a9dd0f79c9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:694:48
#46 0x55a9dcf919f6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:645:12
#47 0x55a9dcebfd3f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14
#48 0x55a9d43d3002 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1080:18
#49 0x55a9d43da6dc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:159:15
#50 0x55a9d43c9b48 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28
#51 0x55a9da60ad50 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:717:10
#52 0x55a9da60e8ef in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1309:10
#53 0x55a9da60dfa5 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1154:12
#54 0x55a9da6081a0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:332:36
#55 0x55a9da60882b in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:345:10
#56 0x55a9caa343c8 in ChromeMain ./../../chrome/app/chrome\_main.cc:192:12
#57 0x7f38b2a82082 in \_\_libc\_start\_main /build/glibc-e2p3jK/glibc-2.31/csu/../csu/libc-start.c:308:16

0x514000124770 is located 304 bytes inside of 416-byte region [0x514000124640,0x5140001247e0)
freed by thread T0 (chrome) here:
#0 0x55a9caa3244d in operator delete(void\*) *asan\_rtl*:3
#1 0x55a9dcf19ad5 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#2 0x55a9dcf19ad5 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#3 0x55a9dcf19ad5 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#4 0x55a9dcf19ad5 in base::SupportsUserData::RemoveUserData(void const\*) ./../../base/supports\_user\_data.cc:82:3
#5 0x55a9f29a1909 in SidePanelUI::RemoveSidePanelUIForBrowser(Browser\*) ./../../chrome/browser/ui/side\_panel/side\_panel\_ui.cc:24:12
#6 0x55a9f2bf3d9e in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:1059:3
#7 0x55a9f2bf5cfd in ~BrowserView ./../../chrome/browser/ui/views/frame/browser\_view.cc:1009:29
#8 0x55a9f2bf5cfd in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:0:0
#9 0x55a9e4600adb in views::View::~View() ./../../ui/views/view.cc:289:9
#10 0x55a9f3a5bbd2 in ~BrowserFrameViewLinuxNative ./../../chrome/browser/ui/views/frame/browser\_frame\_view\_linux\_native.cc:51:59
#11 0x55a9f3a5bbd2 in BrowserFrameViewLinuxNative::~BrowserFrameViewLinuxNative() ./../../chrome/browser/ui/views/frame/browser\_frame\_view\_linux\_native.cc:51:59
#12 0x55a9e46ba7bb in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#13 0x55a9e46ba7bb in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#14 0x55a9e46ba7bb in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#15 0x55a9e46ba7bb in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:179:1
#16 0x55a9e46ba973 in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:175:33
#17 0x55a9e4605965 in operator() ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:67:5
#18 0x55a9e4605965 in reset ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:278:7
#19 0x55a9e4605965 in ~unique\_ptr ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:248:71
#20 0x55a9e4605965 in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) ./../../ui/views/view.cc:3089:1
#21 0x55a9e4605ccd in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:369:5
#22 0x55a9e4660084 in views::Widget::DestroyRootView() ./../../ui/views/widget/widget.cc:2141:15
#23 0x55a9e465dac5 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:251:3
#24 0x55a9f2be0593 in BrowserFrame::~BrowserFrame() ./../../chrome/browser/ui/views/frame/browser\_frame.cc:128:31
#25 0x55a9e4704c3a in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:0:0
#26 0x55a9f2df116f in ~DesktopBrowserFrameAuraLinux ./../../chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:32:61
#27 0x55a9f2df116f in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() ./../../chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:32:61
#28 0x55a9e470636e in views::DesktopNativeWidgetAura::OnHostClosed() ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:393:5
#29 0x55a9e4743aa1 in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:922:32
#30 0x55a9e473ab91 in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:429:22
#31 0x55a9e4747edd in Invoke<void (views::DesktopWindowTreeHostPlatform::*)(), const base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:738:12
#32 0x55a9e4747edd in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), std::\_\_Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:954:5
#33 0x55a9e4747edd in void base::internal::Invoker<base::internal::FunctorTraits<void (views::DesktopWindowTreeHostPlatform::*&&)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);)&&>, base::internal::BindState<true, true, false, void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, void ()>::RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::\_\_Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, 0ul>(void (views::DesktopWindowTreeHostPlatform::*&&)(), std::\_\_Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul>) ./../../base/functional/bind\_internal.h:1067:14
#34 0x55a9dcf2cd24 in Run ./../../base/functional/callback.h:156:12
#35 0x55a9dcf2cd24 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:203:34
#36 0x55a9dcf90046 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:90:5
#37 0x55a9dcf90046 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23
#38 0x55a9dcf8ef5d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:338:40
#39 0x55a9dcf90d8a in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0
#40 0x55a9dd0f79c9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:694:48
#41 0x55a9dcf919f6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:645:12
#42 0x55a9dcebfd3f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14
#43 0x55a9d43d3002 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1080:18
#44 0x55a9d43da6dc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:159:15
#45 0x55a9d43c9b48 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28

previously allocated by thread T0 (chrome) here:
#0 0x55a9caa31bed in operator new(unsigned long) *asan\_rtl*:3
#1 0x55a9f2bf11fa in make\_unique<SidePanelCoordinator, BrowserView *> ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:620:26
#2 0x55a9f2bf11fa in BrowserView::BrowserView(std::\_\_Cr::unique\_ptr<Browser, std::\_\_Cr::default\_delete<Browser> >) ./../../chrome/browser/ui/views/frame/browser\_view.cc:966:23
#3 0x55a9f2de6517 in BrowserWindow::CreateBrowserWindow(std::\_\_Cr::unique\_ptr<Browser, std::\_\_Cr::default\_delete<Browser> >, bool, bool) ./../../chrome/browser/ui/views/frame/browser\_window\_factory.cc:61:14
#4 0x55a9f2032cb0 in CreateBrowserWindow ./../../chrome/browser/ui/browser.cc:319:10
#5 0x55a9f2032cb0 in Browser::Browser(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:609:29
#6 0x55a9f20314b8 in Browser::Create(Browser::CreateParams const&) ./../../chrome/browser/ui/browser.cc:510:14
#7 0x55a9f207ae76 in chrome::OpenEmptyWindow(Profile*, bool) ./../../chrome/browser/ui/browser\_commands.cc:620:22
#8 0x55a9f207ac13 in chrome::NewEmptyWindow(Profile\*, bool) ./../../chrome/browser/ui/browser\_commands.cc:0:0
#9 0x55a9f2066eb1 in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) ./../../chrome/browser/ui/browser\_command\_controller.cc:467:7
#10 0x55a9e4586e29 in TryProcess ./../../ui/base/accelerators/accelerator\_manager.cc:153:17
#11 0x55a9e4586e29 in ui::AcceleratorManager::Process(ui::Accelerator const&) ./../../ui/base/accelerators/accelerator\_manager.cc:83:27
#12 0x55a9e458257b in views::FocusManager::ProcessAccelerator(ui::Accelerator const&) ./../../ui/views/focus/focus\_manager.cc:480:28
#13 0x55a9f2c0b701 in BrowserView::PreHandleKeyboardEvent(content::NativeWebKeyboardEvent const&) ./../../chrome/browser/ui/views/frame/browser\_view.cc:0:7
#14 0x55a9d5d57e06 in content::WebContentsImpl::PreHandleKeyboardEvent(content::NativeWebKeyboardEvent const&) ./../../content/browser/web\_contents/web\_contents\_impl.cc:3865:33
#15 0x55a9d5753162 in content::RenderWidgetHostImpl::ForwardKeyboardEventWithCommands(content::NativeWebKeyboardEvent const&, ui::LatencyInfo const&, std::\_\_Cr::vector<mojo::InlinedStructPtr[blink::mojom::EditCommand](javascript:void(0);), std::\_\_Cr::allocator<mojo::InlinedStructPtr[blink::mojom::EditCommand](javascript:void(0);) > >, bool\*) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:1762:24
#16 0x55a9d57bb744 in content::RenderWidgetHostViewAura::ForwardKeyboardEventWithLatencyInfo(content::NativeWebKeyboardEvent const&, ui::LatencyInfo const&, bool\*) ./../../content/browser/renderer\_host/render\_widget\_host\_view\_aura.cc:2778:16
#17 0x55a9d617ebf7 in content::RenderWidgetHostViewEventHandler::OnKeyEvent(ui::KeyEvent\*) ./../../content/browser/renderer\_host/render\_widget\_host\_view\_event\_handler.cc:267:14
#18 0x55a9e109f70f in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:187:12
#19 0x55a9e109e08c in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:136:5
#20 0x55a9e109d648 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:82:14
#21 0x55a9e109d255 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:54:15
#22 0x55a9e3f956db in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:72:19
#23 0x55a9e3fb164f in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ./../../ui/aura/window\_tree\_host.cc:309:23
#24 0x55a9e1369f76 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ./../../ui/base/ime/input\_method\_base.cc:137:43
#25 0x55a9e1387458 in ui::InputMethodAuraLinux::DispatchKeyEvent(ui::KeyEvent\*) ./../../ui/base/ime/linux/input\_method\_auralinux.cc:210:15
#26 0x55a9e3f8bb6f in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ./../../ui/aura/window\_event\_dispatcher.cc:1105:54
#27 0x55a9e3f8911d in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/aura/window\_event\_dispatcher.cc:562:15
#28 0x55a9e109d177 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:50:34
#29 0x55a9e3f956db in ui::EventProcessor::OnEventFromSource(ui::Event\*) ./../../ui/events/event\_processor.cc:72:19
#30 0x55a9e3fba64f in ui::EventSource::DeliverEventToSink(ui::Event\*) ./../../ui/events/event\_source.cc:119:16
#31 0x55a9e3fb9c5f in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ./../../ui/events/event\_source.cc:134:12
#32 0x55a9e472cc33 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ./../../ui/aura/window\_tree\_host\_platform.cc:285:38

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan/chrome+0x375ce2ff) (BuildId: 889d72568b41a302)
Shadow bytes around the buggy address:
0x514000124480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x514000124500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x514000124580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x514000124600: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
0x514000124680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x514000124700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd
0x514000124780: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
0x514000124800: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
0x514000124880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x514000124900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x514000124980: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
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

==26808==ADDITIONAL INFO

==26808==Note: Please include this section with the ASan report.
Task trace:
#0 0x55a9df4124f2 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message\*) ./../../ipc/ipc\_mojo\_bootstrap.cc:1160:13
#1 0x55a9de6a1af7 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

MiraclePtr Status: MANUAL ANALYSIS REQUIRED
A pointer to the same region was extracted from a raw\_ptr<T> object prior to this crash.
To determine the protection status, enable extraction warnings and check whether the raw\_ptr<T> object can be destroyed or overwritten between the extraction and use.
Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 24.2 KB)
- [Screencast from 24 ماي, 2024 +01 01:50:15.webm](attachments/Screencast from 24 ماي, 2024 +01 01_50_15.webm) (application/octet-stream, 3.6 MB)

## Timeline

### bo...@google.com (2024-05-24)

Confirming repro on 127.0.6485.0 (canary/ToT) Linux x64. Something similar is afoot in 126.0.6478.17, so setting FoundIn=126. This bug does not appear to be present in M125 (stable).

Browser process memory corruption would normally be Severity Critical, but dropping to High due to requirement of multi-step precise user interaction.

I'm still looking for the right component, but I'm passing on to relevant OWNERS for assessment.

### hu...@google.com (2024-05-24)

This does not happen if you move the overlay tab from one window to the other, if the original window with the overlay tab still has tabs open. It only happens if you close that window (or if the overlay tab was the only window). Somehow, the side panel state observer (i think) is referring to the wrong tab strip model or something after the overlay tab gets moved.

### hu...@google.com (2024-05-24)

Hey Erik, hope you are well! Assigning this to you since I believe you've dealt with UaF and window/tab closing behaviour in LensOverlayController before. Let me know if you don't think you're the right person to look at this and feel free to assign it back to me. Thanks!

### er...@google.com (2024-05-24)

deleted

### er...@google.com (2024-05-24)

deleted

### er...@google.com (2024-05-25)

This is quite tricky, there are several different issues.

### pe...@google.com (2024-05-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-05-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2024-05-28)

hi erikchen@ I see a draft change here, however, despite this being a fairly mitigated issue this is still a security issue that was seemingly introduced in m126. As of right now, this is considered a Stable Release Blocker and M126 Stable is being cut for early release in one week. Please update with a statue to resolve this issue as soon as possible.

### am...@chromium.org (2024-05-28)

<https://crrev.com/c/5572858> is out for review at present, should hopefully be landed in the next few hours (per off-bug chat with erikchen@)

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: main

commit 3354113bd081986cc0d134a8453e32c2a2d483e7
Author: Erik Chen <erikchen@chromium.org>
Date:   Tue May 28 23:02:32 2024

    [lensoverlay] Many improvements to the close flow.
    
    There are several bugs related to how lens overlay closes. There are
    many paths that result in closing the overlay, and several of these
    paths have different requirements. Many of these paths that had
    different requirements were going through the same logic flow. This
    resulted in bugs.
    
    This CL makes several changes:
    
    (1) Add a new callback subscription to TabInterface to allow listeners
    to determine when a tab is about to be removed from a window. This is
    now a distinct closing flow.
    
    (2) Expose SidePanelCoordinator::Close(bool supress_animations) to allow
    synchronous closing of the side panel by lens overlay.
    
    (3) Separate the close flow of LensOverlayController into two flows: a
    synchronous close and an asynchronous close. Most error handling and
    unusual flows are switched to the synchronous close.
    
    (4) Close the overlay when the tab is dragged into a new window.
    
    (5) Add a missing early return to
    LensOverlayController::CaptureScreenshot. This was responsible for flaky
    test failures.
    
    (6) Remove copy-pasted parts of
    LensOverlayControllerBrowserTest.RecordInvocationAndDismissalHistograms.
    Break the exiting test into two tests. Reenable the test on all
    platforms. Add missing waits to the code.
    
    (7) Simplify LensOverlaySidePanelCoordinator to always close through
    LensOverlayController. flow. Previously, close could be started by
    either LensOverlaySidePanelCoordinator or LensOverlayController, with
    re-entrancy.
    
    (8) Document the members of LensOverlayController that have
    window-affine state.
    
    (9) RealboxHandler must be destroyed before
    LensOverlaySidePanelCoordinator. This was previously not the case and
    papered over with re-entrant logic from the destructor of
    LensOverlaySidePanelCoordinator.
    
    Change-Id: I358d51fb3db7399288cbfaac195fe84c354c7a77
    Bug: 342921671, 342419061
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5572858
    Reviewed-by: Juan Mojica <juanmojica@google.com>
    Commit-Queue: Erik Chen <erikchen@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1307109}

M       chrome/browser/ui/lens/lens_overlay_controller.cc
M       chrome/browser/ui/lens/lens_overlay_controller.h
M       chrome/browser/ui/lens/lens_overlay_controller_browsertest.cc
M       chrome/browser/ui/lens/lens_overlay_dismissal_source.h
M       chrome/browser/ui/lens/lens_overlay_side_panel_coordinator.cc
M       chrome/browser/ui/lens/lens_overlay_side_panel_coordinator.h
M       chrome/browser/ui/tabs/public/tab_interface.h
M       chrome/browser/ui/tabs/tab_model.cc
M       chrome/browser/ui/tabs/tab_model.h
M       chrome/browser/ui/tabs/tab_strip_model.cc
M       chrome/browser/ui/views/side_panel/lens/lens_overlay_side_panel_web_view.cc
M       chrome/browser/ui/views/side_panel/lens/lens_overlay_side_panel_web_view.h
M       chrome/browser/ui/views/side_panel/side_panel_coordinator.h
M       tools/metrics/histograms/metadata/lens/enums.xml

https://chromium-review.googlesource.com/5572858


### ch...@gmail.com (2024-05-29)

I just verified this on 127.0.6509.0. Fixed.

### pe...@google.com (2024-05-29)

Bumping the priority of this issue since it will affect an upcoming release.

### pg...@google.com (2024-05-29)

Thank you for fixing this vulnerability!

Marking this bug as fixed(=fixed in main, may need merges) - this is necessary for security bug workflow automation (:

### pg...@google.com (2024-05-30)

Unsure why automation hasnt yet put merge review labels, but getting ahead of automation and rejecting the merge for M126 and accordingly removing the release block field.

The issue is introduced in M126, but given the mitigations for the vulnerability, the size of the fix, and the short turnaround for getting this fix into the M126 early stable cut, I don't think this fix should be back merged to M126 at the moment in favor of stability.

### pe...@google.com (2024-05-30)

Requesting merge to beta (M126) because latest trunk commit (1307109) appears to be after beta branch point (1300313).
Merge review required: M126 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ap...@google.com (2024-05-31)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 83d78425e92b9696f67c697f45cc0c460a19ce1d
Author: Erik Chen <erikchen@chromium.org>
Date:   Fri May 31 16:23:10 2024

    [lensoverlay] Many improvements to the close flow.
    
    There are several bugs related to how lens overlay closes. There are
    many paths that result in closing the overlay, and several of these
    paths have different requirements. Many of these paths that had
    different requirements were going through the same logic flow. This
    resulted in bugs.
    
    This CL makes several changes:
    
    (1) Add a new callback subscription to TabInterface to allow listeners
    to determine when a tab is about to be removed from a window. This is
    now a distinct closing flow.
    
    (2) Expose SidePanelCoordinator::Close(bool supress_animations) to allow
    synchronous closing of the side panel by lens overlay.
    
    (3) Separate the close flow of LensOverlayController into two flows: a
    synchronous close and an asynchronous close. Most error handling and
    unusual flows are switched to the synchronous close.
    
    (4) Close the overlay when the tab is dragged into a new window.
    
    (5) Add a missing early return to
    LensOverlayController::CaptureScreenshot. This was responsible for flaky
    test failures.
    
    (6) Remove copy-pasted parts of
    LensOverlayControllerBrowserTest.RecordInvocationAndDismissalHistograms.
    Break the exiting test into two tests. Reenable the test on all
    platforms. Add missing waits to the code.
    
    (7) Simplify LensOverlaySidePanelCoordinator to always close through
    LensOverlayController. flow. Previously, close could be started by
    either LensOverlaySidePanelCoordinator or LensOverlayController, with
    re-entrancy.
    
    (8) Document the members of LensOverlayController that have
    window-affine state.
    
    (9) RealboxHandler must be destroyed before
    LensOverlaySidePanelCoordinator. This was previously not the case and
    papered over with re-entrant logic from the destructor of
    LensOverlaySidePanelCoordinator.
    
    (cherry picked from commit 3354113bd081986cc0d134a8453e32c2a2d483e7)
    
    Change-Id: I358d51fb3db7399288cbfaac195fe84c354c7a77
    Bug: 342921671, 342419061
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5572858
    Reviewed-by: Juan Mojica <juanmojica@google.com>
    Commit-Queue: Erik Chen <erikchen@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1307109}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5586282
    Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#940}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/ui/lens/lens_overlay_controller.cc
M       chrome/browser/ui/lens/lens_overlay_controller.h
M       chrome/browser/ui/lens/lens_overlay_controller_browsertest.cc
M       chrome/browser/ui/lens/lens_overlay_dismissal_source.h
M       chrome/browser/ui/lens/lens_overlay_side_panel_coordinator.cc
M       chrome/browser/ui/lens/lens_overlay_side_panel_coordinator.h
M       chrome/browser/ui/tabs/public/tab_interface.h
M       chrome/browser/ui/tabs/tab_model.cc
M       chrome/browser/ui/tabs/tab_model.h
M       chrome/browser/ui/tabs/tab_strip_model.cc
M       chrome/browser/ui/views/side_panel/lens/lens_overlay_side_panel_web_view.cc
M       chrome/browser/ui/views/side_panel/lens/lens_overlay_side_panel_web_view.h
M       chrome/browser/ui/views/side_panel/side_panel_coordinator.h
M       tools/metrics/histograms/metadata/lens/enums.xml

https://chromium-review.googlesource.com/5586282


### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations Khalil! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342419061)*
