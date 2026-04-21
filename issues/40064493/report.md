# Security: another UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40064493](https://issues.chromium.org/issues/40064493) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Input |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2023-05-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Another UAF in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents in browser process.  

The <https://crbug.com/chromium/1427918> has been fixed and cannot been reproduced.  

However the new issue can also trigger the same UAF crash.

**VERSION**  

Chromium 115.0.5760.0 (Developer Build) (64-bit)  

Revision df0117ba83b79179bf0077bf5c65ee69a8e68057-refs/heads/main@{#1141141}  

OS Linux

**REPRODUCTION CASE**

1. put the attachements into webserver and run `python3 -m http.server 8000`
2. run `chrome --user-data-dir=/tmp/any --start-maximized --enable-gpu-benchmarking about:blank about:blank about:blank http:/localhost:8000/poc.html`

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [browser]

==9930==ERROR: AddressSanitizer: heap-use-after-free on address 0x50b0003bdc50 at pc 0x5622b37111d3 bp 0x7ffe8f999050 sp 0x7ffe8f999048  

READ of size 8 at 0x50b0003bdc50 thread T0 (chrome)  

[9966:9996:0509/104328.660686:ERROR:display.cc(294)] Frame latency is negative: -10.051 ms  

==9930==WARNING: invalid path to external symbolizer!  

==9930==WARNING: Failed to use and restart external symbolizer!  

#0 0x5622b37111d2 in content::SyntheticPointerAction::ForwardTouchOrMouseInputEvents(base::TimeTicks const&, content::SyntheticGestureTarget\*) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:145:26  

#1 0x5622b370ff05 in content::SyntheticPointerAction::ForwardInputEvents(base::TimeTicks const&, content::SyntheticGestureTarget\*) ./../../content/browser/renderer\_host/input/synthetic\_pointer\_action.cc:48:24  

#2 0x5622b36fedc1 in content::SyntheticGestureController::DispatchNextEvent(base::TimeTicks) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:116:48  

#3 0x5622b370835c in operator() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:103:25  

#4 0x5622b370835c in Invoke<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:101:11) &, const base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:621:12  

#5 0x5622b370835c in MakeItSo<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:101:11) &, const std::\_\_Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &> ./../../base/functional/bind\_internal.h:925:12  

#6 0x5622b370835c in RunImpl<const (lambda at ../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:101:11) &, const std::\_\_Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#7 0x5622b370835c in base::internal::Invoker<base::internal::BindState<content::SyntheticGestureController::StartTimer(bool)::$\_0, base::WeakPtr[content::SyntheticGestureController](javascript:void(0);)>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:989:12  

#8 0x5622bb284a2b in Run ./../../base/functional/callback.h:348:12  

#9 0x5622bb284a2b in base::MetronomeTimer::OnScheduledTaskInvoked() ./../../base/timer/timer.cc:374:19  

#10 0x5622bb2852a1 in Invoke<void (base::MetronomeTimer::\*)(), base::MetronomeTimer \*> ./../../base/functional/bind\_internal.h:746:12  

#11 0x5622bb2852a1 in MakeItSo<void (base::MetronomeTimer::\*const &)(), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &> ./../../base/functional/bind\_internal.h:925:12  

#12 0x5622bb2852a1 in RunImpl<void (base::MetronomeTimer::\*const &)(), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<base::MetronomeTimer, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#13 0x5622bb2852a1 in base::internal::Invoker<base::internal::BindState<void (base::MetronomeTimer::\*)(), base::internal::UnretainedWrapper<base::MetronomeTimer, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:989:12  

#14 0x5622bb179937 in Run ./../../base/functional/callback.h:152:12  

#15 0x5622bb179937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#16 0x5622bb1e3b95 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#17 0x5622bb1e3b95 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#18 0x5622bb1e2ab5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#19 0x5622bb1e4bd4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#20 0x5622bb35d164 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:670:48  

#21 0x5622bb1e5909 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#22 0x5622bb0f84be in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#23 0x5622b2677693 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18  

#24 0x5622b267f476 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#25 0x5622b266e2ea in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28  

#26 0x5622b8514a14 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:706:10  

#27 0x5622b8519014 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1276:10  

#28 0x5622b851885d in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1130:12  

#29 0x5622b851179f in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#30 0x5622b8511d10 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#31 0x5622a9475366 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#32 0x7ff926513082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x50b0003bdc50 is located 96 bytes inside of 104-byte region [0x50b0003bdbf0,0x50b0003bdc58)  

freed by thread T0 (chrome) here:  

#0 0x5622a947310d in operator delete(void\*) *asan\_rtl*:3  

#1 0x5622b36fcb42 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#2 0x5622b36fcb42 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#3 0x5622b36fcb42 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#4 0x5622b36fcb42 in \_\_destroy\_at<std::\_\_Cr::unique\_ptr<content::SyntheticGesture, std::\_\_Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#5 0x5622b36fcb42 in destroy\_at<std::\_\_Cr::unique\_ptr<content::SyntheticGesture, std::\_\_Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#6 0x5622b36fcb42 in destroy<std::\_\_Cr::unique\_ptr<content::SyntheticGesture, std::\_\_Cr::default\_delete[content::SyntheticGesture](javascript:void(0);) >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#7 0x5622b36fcb42 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:838:9  

#8 0x5622b36fcb42 in \_\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:726:9  

#9 0x5622b36fcb42 in erase ./../../buildtools/third\_party/libc++/trunk/include/vector:1633:11  

#10 0x5622b36fcb42 in content::SyntheticGestureController::GestureAndCallbackQueue::Pop() ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.h:111:17  

#11 0x5622b36ff80e in content::SyntheticGestureController::GestureCompleted(content::SyntheticGesture::Result) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:202:26  

#12 0x5622b37089b9 in Invoke<void (content::SyntheticGestureController::\*)(content::SyntheticGesture::Result), const base::WeakPtr[content::SyntheticGestureController](javascript:void(0);) &, content::SyntheticGesture::Result> ./../../base/functional/bind\_internal.h:746:12  

#13 0x5622b37089b9 in MakeItSo<void (content::SyntheticGestureController::\*)(content::SyntheticGesture::Result), std::\_\_Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);), content::SyntheticGesture::Result> > ./../../base/functional/bind\_internal.h:953:5  

#14 0x5622b37089b9 in RunImpl<void (content::SyntheticGestureController::\*)(content::SyntheticGesture::Result), std::\_\_Cr::tuple<base::WeakPtr[content::SyntheticGestureController](javascript:void(0);), content::SyntheticGesture::Result>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1025:12  

#15 0x5622b37089b9 in base::internal::Invoker<base::internal::BindState<void (content::SyntheticGestureController::\*)(content::SyntheticGesture::Result), base::WeakPtr[content::SyntheticGestureController](javascript:void(0);), content::SyntheticGesture::Result>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#16 0x5622adf1d516 in Run ./../../base/functional/callback.h:152:12  

#17 0x5622adf1d516 in blink::mojom::WidgetInputHandler\_WaitForInputProcessed\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/input/input\_handler.mojom.cc:7303:26  

#18 0x5622bdaf141c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1011:41  

#19 0x5622bdb0e7c2 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#20 0x5622bdaf6aa8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#21 0x5622bdb1c93e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#22 0x5622bdb1ace2 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#23 0x5622bdb0e7c2 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#24 0x5622bdae7204 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#25 0x5622bdae8e13 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#26 0x5622bdaebcb0 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#27 0x5622bdaebcb0 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#28 0x5622bdaebcb0 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#29 0x5622bdaebcb0 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#30 0x5622ae3429fe in Run ./../../base/functional/callback.h:333:12  

#31 0x5622ae3429fe in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#32 0x5622ae342c15 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#33 0x5622ae342c15 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#34 0x5622ae342c15 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#35 0x5622ae342c15 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#36 0x5622bdb80b2f in Run ./../../base/functional/callback.h:333:12  

#37 0x5622bdb80b2f in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#38 0x5622bdb819ec in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#39 0x5622bdb819ec in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#40 0x5622bdb819ec in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1025:12  

#41 0x5622bdb819ec in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#42 0x5622bb179937 in Run ./../../base/functional/callback.h:152:12  

#43 0x5622bb179937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#44 0x5622bb1e3b95 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#45 0x5622bb1e3b95 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#46 0x5622bb1e2ab5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#47 0x5622bb1e4bd4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#48 0x5622bb35d164 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:670:48  

#49 0x5622bb1e5b5e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:648:12  

#50 0x5622bb0f84be in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#51 0x5622bf7e7d4c in ui::X11WholeScreenMoveLoop::RunMoveLoop(bool, scoped\_refptr[ui::X11Cursor](javascript:void(0);), scoped\_refptr[ui::X11Cursor](javascript:void(0);)) ./../../ui/base/x/x11\_whole\_screen\_move\_loop.cc:183:12  

#52 0x5622c67ab837 in views::DesktopWindowTreeHostPlatform::RunMoveLoop(gfx::Vector2d const&, views::Widget::MoveLoopSource, views::Widget::MoveLoopEscapeBehavior) ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:660:47  

#53 0x5622c67dcfdf in views::DesktopWindowTreeHostLinux::RunMoveLoop(gfx::Vector2d const&, views::Widget::MoveLoopSource, views::Widget::MoveLoopEscapeBehavior) ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:160:66  

#54 0x5622c66e3928 in views::Widget::RunMoveLoop(gfx::Vector2d const&, views::Widget::MoveLoopSource, views::Widget::MoveLoopEscapeBehavior) ./../../ui/views/widget/widget.cc:693:26  

#55 0x5622d17ea39d in TabDragController::RunMoveLoop(gfx::Vector2d const&) ./../../chrome/browser/ui/views/tabs/tab\_drag\_controller.cc:1614:61

previously allocated by thread T0 (chrome) here:  

#0 0x5622a94728ad in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5622b36fb7b4 in CreateGesture<content::SyntheticPointerAction, content::SyntheticPointerActionListParams> ./../../content/browser/renderer\_host/input/synthetic\_gesture.cc:22:7  

#2 0x5622b36fb7b4 in content::SyntheticGesture::Create(content::SyntheticGestureParams const&) ./../../content/browser/renderer\_host/input/synthetic\_gesture.cc:47:14  

#3 0x5622b36c48d8 in content::InputInjectorImpl::QueueSyntheticPointerAction(content::SyntheticPointerActionListParams const&, base::OnceCallback<void ()>) ./../../content/browser/renderer\_host/input/input\_injector\_impl.cc:77:7  

#4 0x5622ae91d0a2 in content::mojom::InputInjectorStubDispatch::AcceptWithResponder(content::mojom::InputInjector\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) ./gen/content/common/input/input\_injector.mojom.cc:1735:13  

#5 0x5622bdaf1058 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:970:56  

#6 0x5622bdb0e7c2 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#7 0x5622bdaf6aa8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#8 0x5622bdb1c93e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#9 0x5622bdb1ace2 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#10 0x5622bdb0e7c2 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#11 0x5622bdae7204 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#12 0x5622bdae8e13 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#13 0x5622bdaebcb0 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#14 0x5622bdaebcb0 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, unsigned int> ./../../base/functional/bind\_internal.h:925:12  

#15 0x5622bdaebcb0 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#16 0x5622bdaebcb0 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) ./../../base/functional/bind\_internal.h:989:12  

#17 0x5622ae3429fe in Run ./../../base/functional/callback.h:333:12  

#18 0x5622ae3429fe in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.h:192:14  

#19 0x5622ae342c15 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:636:12  

#20 0x5622ae342c15 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> ./../../base/functional/bind\_internal.h:925:12  

#21 0x5622ae342c15 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::\_\_Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#22 0x5622ae342c15 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) ./../../base/functional/bind\_internal.h:989:12  

#23 0x5622bdb80b2f in Run ./../../base/functional/callback.h:333:12  

#24 0x5622bdb80b2f in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#25 0x5622bdb819ec in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:746:12  

#26 0x5622bdb819ec in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:953:5  

#27 0x5622bdb819ec in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> ./../../base/functional/bind\_internal.h:1025:12  

#28 0x5622bdb819ec in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#29 0x5622bb179937 in Run ./../../base/functional/callback.h:152:12  

#30 0x5622bb179937 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#31 0x5622bb1e3b95 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#32 0x5622bb1e3b95 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#33 0x5622bb1e2ab5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#34 0x5622bb1e4bd4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#35 0x5622bb35c7ca in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:625:46  

#36 0x5622bb35f682 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43  

#37 0x7ff927c2e17c in g\_main\_context\_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/cmos/chromium\_version/latest\_asan/chrome+0x179ff1d2) (BuildId: 6cbfca2de266d821)  

Shadow bytes around the buggy address:  

0x50b0003bd980: fd fd fd fd fa fa fa fa fa fa f7 fa fd fd fd fd  

0x50b0003bda00: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x50b0003bda80: f7 fa fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x50b0003bdb00: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00  

0x50b0003bdb80: 00 00 00 00 00 fa fa fa fa fa fa fa f7 fa fd fd  

=>0x50b0003bdc00: fd fd fd fd fd fd fd fd fd fd[fd]fa fa fa fa fa  

0x50b0003bdc80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x50b0003bdd00: fd fa fa fa fa fa fa fa f7 fa fd fd fd fd fd fd  

0x50b0003bdd80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa  

0x50b0003bde00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x50b0003bde80: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd  

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

==9930==ADDITIONAL INFO

==9930==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x5622b36fe42b in content::SyntheticGestureController::StartTimer(bool) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:99:7  

#1 0x5622b36fe42b in content::SyntheticGestureController::StartTimer(bool) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:99:7  

#2 0x5622b36fe42b in content::SyntheticGestureController::StartTimer(bool) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:99:7  

#3 0x5622b36fe42b in content::SyntheticGestureController::StartTimer(bool) ./../../content/browser/renderer\_host/input/synthetic\_gesture\_controller.cc:99:7

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==9930==END OF ADDITIONAL INFO  

==9930==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [input-types.js](attachments/input-types.js) (text/plain, 273 B)
- [testdriver.js](attachments/testdriver.js) (text/plain, 32.6 KB)
- [testdriver-actions.js](attachments/testdriver-actions.js) (text/plain, 18.4 KB)
- [testdriver-vendor.js](attachments/testdriver-vendor.js) (text/plain, 18.2 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.4 KB)

## Timeline

### [Deleted User] (2023-05-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-05-11)

Thanks for the report.

bokan: could you PTAL?

[Monorail components: Blink>Input]

### me...@chromium.org (2023-05-11)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-05-11)

Thanks for the report. This looks like a different path from the previous reports (yey?).

I'll take a look.

+Security_Impact-None since this is in SyntheticGestureController which isn't exposed on the drive-by web (accessible only with command-line flag or DevTools protocol).

### ma...@chromium.org (2023-06-16)

Hi bokan, any updates on this security issue?

### an...@chromium.org (2023-06-30)

Another ping from the current secondary shepherd - any update?

### bo...@chromium.org (2023-07-04)

Sorry for the delay - I finally started looking at this today.

I've narrowed this down to the fact that we're dispatching a gesture to a background tab. The RenderWidgetHost's bounds aren't updated since it's never foregrounded so the event location is incorrect, causing it to be handled by UI widgets.

I need a bit more time to figure out the right fix.

### gi...@appspot.gserviceaccount.com (2023-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f38fff2f0e26eb6f53f900a71c59334caf2c7b30

commit f38fff2f0e26eb6f53f900a71c59334caf2c7b30
Author: David Bokan <bokan@chromium.org>
Date: Fri Jul 07 19:08:54 2023

Mark enable-gpu-benchmarking flag as unsafe

This flag allows injecting input at the UI layer and can be used to fake
user input anywhere in the web content area without origin boundaries.

Bug: 1444597,1453110
Change-Id: I101f3e32aafba8fc81155c943869a6d2a6ff7a43
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4661440
Reviewed-by: Brian Sheedy <bsheedy@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1167572}

[modify] https://crrev.com/f38fff2f0e26eb6f53f900a71c59334caf2c7b30/content/test/gpu/gpu_tests/trace_integration_test.py
[modify] https://crrev.com/f38fff2f0e26eb6f53f900a71c59334caf2c7b30/chrome/browser/ui/startup/bad_flags_prompt.cc


### bo...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824

commit 6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824
Author: David Bokan <bokan@chromium.org>
Date: Fri Jul 14 21:13:38 2023

refactor: SyntheticGesture holds params.

This is a non-functional refactor from https://crrev.com/c/4666793.

This CL makes the SyntheticGesture base class hold the pointer to the
gesture params, rather than having each descendant class storing its own
pointer. This makes it more straightforward to access common params in a
gesture-agnostic way, as was needed by the above CL.

However, since each gesture takes its own type of params, all derived
from SyntheticGestureParams, there's some hoops to jump through with
type conversions. A new intermediate base class is introduced, templated
on the final type, to avoid type conversion boilerplate in each derived
class.

Change-Id: Idc5cf83d8190bfd1578c143b3524a61ed9642b11
Bug: 1444597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4678897
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1170705}

[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_pointer_action.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/mouse_latency_browsertest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/actions_parser.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_pinch_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_tap_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/site_per_process_layout_browsertest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_pinch_gesture_params.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/devtools/protocol/input_handler.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/actions_parser_unittest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/renderer/gpu_benchmarking_extension.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_touchpad_pinch_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_pointer_action_list_params.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_smooth_drag_gesture_params.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_smooth_scroll_gesture_params.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_pinch_gesture_params.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/actions_parser_test_driver_unittest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/actions_parser.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/input_injector_impl.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/devtools/protocol/input_handler.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_tap_gesture_params.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_tap_gesture_params.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/touch_action_browsertest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_pointer_action_list_params.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_smooth_drag_gesture_params.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_tap_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_touchscreen_pinch_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_move_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_gesture_params.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_pointer_action.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_pinch_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_scroll_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_gesture.h
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_drag_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/browser/renderer_host/input/synthetic_smooth_move_gesture.cc
[modify] https://crrev.com/6d776aa667e2a85e5dce73ed2a6eebd0ee0a9824/content/common/input/synthetic_smooth_scroll_gesture_params.h


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/def83e505f5464d0c0b5f41866fd21fb5063881e

commit def83e505f5464d0c0b5f41866fd21fb5063881e
Author: David Bokan <bokan@chromium.org>
Date: Tue Jul 18 14:21:17 2023

Synthetic gestures only dispatch to visible widget

This UAF is caused by a synthetic pointer being routed to browser UI. In
this case, it starts dragging a tab which starts a nested message loop
Further events and gestures are processed in this nested loop and
cleaned up. When the message loop returns the stack contains the cleaned
up pointers.

Synthetic gestures shouldn't be able to target UI outside the web
contents area. The event location is intersected with the web contents'
RenderWidget's view bounds to prevent this [1]. However, the bounds will
be inaccurate if the widget is in a background tab; it won't receive
resizes until it's foregrounded (it's also bad that we can dispatch
events to a different tab).

This CL fixes the issue by ensuring events are dispatched only to a
foregrounded widget. If a synthetic gesture is started while the widget
is in a background tab, its start is deferred until it comes into the
foreground. If the widget is backgrounded while a gestuere is in
progress, the gesture is aborted.

Note: we don't do this for DevTools injected events as those skip event
routing and go straight to the injecting renderer. The comment in [2]
makes me think this is a common use case.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/input/synthetic_gesture_target_base.cc;l=155;drc=ac872e771ce001fef191848bab4167d60dfda403
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/input/synthetic_gesture_target_aura.cc;l=140;drc=ac872e771ce001fef191848bab4167d60dfda403

Bug: 1444597
Change-Id: I2955ce60357f7f03e62f44fd1497bd4ea598f660
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4666793
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1171732}

[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_pointer_action_unittest.cc
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_gesture_controller_unittest.cc
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/third_party/blink/web_tests/external/wpt/event-timing/event-click-visibilitychange.html
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_gesture.cc
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/third_party/blink/web_tests/external/wpt/payment-request/payment-request-disallowed-when-hidden.https.html
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_gesture_controller.h
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_gesture.h
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/def83e505f5464d0c0b5f41866fd21fb5063881e/content/browser/renderer_host/input/synthetic_gesture_controller.cc


### dr...@chromium.org (2023-08-07)

[security shepherd] I realize this is SecurityImpact-None, so we don't actually need to fix this any time soon, but I see several CLs here that sound like they fix the issue. In the interest of having less security bugs open, can we mark this fixed?

### bo...@chromium.org (2023-08-14)

Sorry for the delay - the fix above caused https://crbug.com/chromium/1466518 so was waiting on that to resolve then went OOO.

1466518 was marked WontFix so this should be good to go.

Reporter, could you confirm whether the issue is fixed after build 1171732?

### ah...@google.com (2023-09-19)

[secondary security shepherd] @0xasnine@gmail.com, could you confirm whether the issue is now  fixed?


### bo...@chromium.org (2023-09-29)

This fixed the issue for me locally so I'm going to mark this fixed. It'd still be good to get external verification though.

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-05)

Thank you for the report, asnine! The Chrome VRP Panel has decided to award you $2,000 for this report due to reliance on gpu benchmarking, which is an engineering / test feature. As such, we consider this issue to be significantly mitigated by reliance on a non-standard workflow and engineering specific feature. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/1444597?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1453110]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064493)*
