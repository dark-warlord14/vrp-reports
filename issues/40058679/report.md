# Security: Heap-use-after-free in NearbyShareAction::HandleKeyboardEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058679](https://issues.chromium.org/issues/40058679) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebShare |
| **Platforms** | Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2022-02-04 |
| **Bounty** | $7,000.00 |

## Description

Chrome Version: 100.0.4867.0  

Operating System: ChromeOS

**REPRODUCTION CASE**

1. Open the testcase in two windows (window A and B)
2. In the window A, click on the button and choose "Nearby Share"
3. In the window B, click on the button and choose "Nearby Share"
4. Move any window of them to the other window
5. Press any key (Enter or Esc...)

==67126==ERROR: AddressSanitizer: heap-use-after-free on address 0x618000085480 at pc 0x558749d6c6d2 bp 0x7ffd900cb3c0 sp 0x7ffd900cb3b8  

READ of size 8 at 0x618000085480 thread T0 (chrome)  

==67126==WARNING: invalid path to external symbolizer!  

==67126==WARNING: Failed to use and restart external symbolizer!  

#0 0x558749d6c6d1 in views::View::GetFocusManager() ././../../ui/views/view.cc:1711:20  

#1 0x55874c16f1fc in HandleKeyboardEvent ././../../chrome/browser/nearby\_sharing/sharesheet/nearby\_share\_action.cc:258:25  

#2 0x55874c16f1fc in non-virtual thunk to NearbyShareAction::HandleKeyboardEvent(content::WebContents\*, content::NativeWebKeyboardEvent const&) ././../../chrome/browser/nearby\_sharing/sharesheet/nearby\_share\_action.cc:0:0  

#3 0x55873b5f6f5e in content::RenderWidgetHostImpl::OnKeyboardEventAck(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState) ././../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2501:16  

#4 0x55873b2e7ecc in Run ./../../base/callback.h:142:12  

#5 0x55873b2e7ecc in content::InputRouterImpl::KeyboardEventHandled(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)) ././../../content/browser/renderer\_host/input/input\_router\_impl.cc:585:36  

#6 0x55873b2ef916 in void base::internal::FunctorTraits<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), void>::Invoke<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);) >(void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);)&&, content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);)&&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>&&, blink::mojom::InputEventResultSource&&, ui::LatencyInfo const&, blink::mojom::InputEventResultState&&, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&) ./../../base/bind\_internal.h:542:12  

#7 0x55873b2ef5e0 in MakeItSo<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);) > ./../../base/bind\_internal.h:726:5  

#8 0x55873b2ef5e0 in RunImpl<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), std::\_\_1::tuple<base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >, 0UL, 1UL, 2UL> ./../../base/bind\_internal.h:779:12  

#9 0x55873b2ef5e0 in base::internal::Invoker<base::internal::BindState<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >, void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&) ./../../base/bind\_internal.h:748:12  

#10 0x55873b2f42ac in Run ./../../base/callback.h:142:12  

#11 0x55873b2f42ac in operator() ././../../content/browser/renderer\_host/input/input\_router\_impl.cc:552:35  

#12 0x55873b2f42ac in Invoke<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:537:13), base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);), blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);) > ./../../base/bind\_internal.h:423:12  

#13 0x55873b2f42ac in MakeItSo<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:537:13), base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);), blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);) > ./../../base/bind\_internal.h:706:12  

#14 0x55873b2f42ac in RunImpl<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:537:13), std::\_\_1::tuple<base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >, 0UL, 1UL> ./../../base/bind\_internal.h:779:12  

#15 0x55873b2f42ac in base::internal::Invoker<base::internal::BindState<content::InputRouterImpl::FilterAndSendWebInputEvent(blink::WebInputEvent const&, ui::LatencyInfo const&, base::OnceCallback<void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>)::$\_1, base::OnceCallback<void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >, void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&) ./../../base/bind\_internal.h:748:12  

#16 0x5587392db842 in Run ./../../base/callback.h:142:12  

#17 0x5587392db842 in blink::mojom::WidgetInputHandler\_DispatchEvent\_ForwardToCallback::Accept(mojo::Message\*) ././gen/third\_party/blink/public/mojom/input/input\_handler.mojom.cc:5461:26  

#18 0x5587455a2a07 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ././../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:896:23  

#19 0x5587455b5307 in mojo::MessageDispatcher::Accept(mojo::Message\*) ././../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#20 0x5587455a5696 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ././../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:658:20  

#21 0x5587455bee5c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ././../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1104:42  

#22 0x5587455bddd3 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ././../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:724:7  

#23 0x5587455b5307 in mojo::MessageDispatcher::Accept(mojo::Message\*) ././../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#24 0x55874559aaf4 in mojo::Connector::DispatchMessage(mojo::Message) ././../../mojo/public/cpp/bindings/lib/connector.cc:556:49  

#25 0x55874559c43e in mojo::Connector::ReadAllAvailableMessages() ././../../mojo/public/cpp/bindings/lib/connector.cc:614:14  

#26 0x5587455870b6 in Run ./../../base/callback.h:241:12  

#27 0x5587455870b6 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ././../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#28 0x558743dffb66 in Run ./../../base/callback.h:142:12  

#29 0x558743dffb66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ././../../base/task/common/task\_annotator.cc:135:32  

#30 0x558743e3fba3 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:29)> ./../../base/task/common/task\_annotator.h:74:5  

#31 0x558743e3fba3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:356:21  

#32 0x558743e3f3f2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#33 0x558743e40761 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#34 0x558743f7df4d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ././../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#35 0x558743e40e1a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:468:12  

#36 0x558743d7a65c in base::RunLoop::Run(base::Location const&) ././../../base/run\_loop.cc:140:14  

#37 0x55873aa226a2 in content::BrowserMainLoop::RunMainMessageLoop() ././../../content/browser/browser\_main\_loop.cc:1053:18  

#38 0x55873aa26c25 in content::BrowserMainRunnerImpl::Run() ././../../content/browser/browser\_main\_runner\_impl.cc:155:15  

#39 0x55873aa1c9fa in content::BrowserMain(content::MainFunctionParams) ././../../content/browser/browser\_main.cc:30:28  

#40 0x558743b57d0f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ././../../content/app/content\_main\_runner\_impl.cc:641:10  

#41 0x558743b5a848 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ././../../content/app/content\_main\_runner\_impl.cc:1174:10  

#42 0x558743b59c98 in content::ContentMainRunnerImpl::Run() ././../../content/app/content\_main\_runner\_impl.cc:1041:12  

#43 0x558743b54484 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ././../../content/app/content\_main.cc:399:36  

#44 0x558743b54b00 in content::ContentMain(content::ContentMainParams) ././../../content/app/content\_main.cc:427:10  

#45 0x55873605744a in ChromeMain ././../../chrome/app/chrome\_main.cc:176:12  

#46 0x55873605721f in main ././../../chrome/app/chrome\_exe\_main\_aura.cc:17:10  

#47 0x7f478c5060b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x618000085480 is located 0 bytes inside of 800-byte region [0x618000085480,0x6180000857a0)  

freed by thread T0 (chrome) here:  

#0 0x55873605548d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x558749d5860d in views::View::~View() ././../../ui/views/view.cc:253:9  

#2 0x558749d591c5 in views::View::~View() ././../../ui/views/view.cc:226:15  

#3 0x558749d5860d in views::View::~View() ././../../ui/views/view.cc:253:9  

#4 0x558749c09eab in views::BubbleDialogDelegateView::~BubbleDialogDelegateView() ././../../ui/views/bubble/bubble\_dialog\_delegate\_view.cc:476:1  

#5 0x5587505cd27b in ash::sharesheet::SharesheetBubbleView::~SharesheetBubbleView() ././../../chrome/browser/ui/ash/sharesheet/sharesheet\_bubble\_view.cc:189:1  

#6 0x5587505cd409 in ash::sharesheet::SharesheetBubbleView::~SharesheetBubbleView() ././../../chrome/browser/ui/ash/sharesheet/sharesheet\_bubble\_view.cc:183:47  

#7 0x558749da710b in views::WidgetDelegate::DeleteDelegate() ././../../ui/views/widget/widget\_delegate.cc:243:5  

#8 0x558749d9c2e6 in views::Widget::OnNativeWidgetDestroyed() ././../../ui/views/widget/widget.cc:1396:21  

#9 0x558749de16fa in OnWindowDestroyed ././../../ui/views/widget/native\_widget\_aura.cc:967:14  

#10 0x558749de16fa in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroyed(aura::Window\*) ././../../ui/views/widget/native\_widget\_aura.cc:0:0  

#11 0x55874994e797 in aura::Window::~Window() ././../../ui/aura/window.cc:228:16  

#12 0x55874994f8af in aura::Window::~Window() ././../../ui/aura/window.cc:183:19  

#13 0x558749e01c5a in wm::TransientWindowManager::OnWindowDestroying(aura::Window\*) ././../../ui/wm/core/transient\_window\_manager.cc:262:5  

#14 0x55874994e5b7 in aura::Window::~Window() ././../../ui/aura/window.cc:194:14  

#15 0x55874994f8af in aura::Window::~Window() ././../../ui/aura/window.cc:183:19  

#16 0x558743dffb66 in Run ./../../base/callback.h:142:12  

#17 0x558743dffb66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ././../../base/task/common/task\_annotator.cc:135:32  

#18 0x558743e3fba3 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:29)> ./../../base/task/common/task\_annotator.h:74:5  

#19 0x558743e3fba3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:356:21  

#20 0x558743e3f3f2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#21 0x558743e40761 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#22 0x558743f7df4d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ././../../base/message\_loop/message\_pump\_libevent.cc:195:55  

#23 0x558743e40e1a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ././../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:468:12  

#24 0x558743d7a65c in base::RunLoop::Run(base::Location const&) ././../../base/run\_loop.cc:140:14  

#25 0x55873aa226a2 in content::BrowserMainLoop::RunMainMessageLoop() ././../../content/browser/browser\_main\_loop.cc:1053:18  

#26 0x55873aa26c25 in content::BrowserMainRunnerImpl::Run() ././../../content/browser/browser\_main\_runner\_impl.cc:155:15  

#27 0x55873aa1c9fa in content::BrowserMain(content::MainFunctionParams) ././../../content/browser/browser\_main.cc:30:28  

#28 0x558743b57d0f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ././../../content/app/content\_main\_runner\_impl.cc:641:10  

#29 0x558743b5a848 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ././../../content/app/content\_main\_runner\_impl.cc:1174:10  

#30 0x558743b59c98 in content::ContentMainRunnerImpl::Run() ././../../content/app/content\_main\_runner\_impl.cc:1041:12  

#31 0x558743b54484 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ././../../content/app/content\_main.cc:399:36  

#32 0x558743b54b00 in content::ContentMain(content::ContentMainParams) ././../../content/app/content\_main.cc:427:10

previously allocated by thread T0 (chrome) here:  

#0 0x558736054c2d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x55874c16d6a6 in make\_unique<views::WebView, Profile \*&> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x55874c16d6a6 in NearbyShareAction::LaunchAction(sharesheet::SharesheetController\*, views::View\*, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);)) ././../../chrome/browser/nearby\_sharing/sharesheet/nearby\_share\_action.cc:148:15  

#3 0x55874bf0a42d in sharesheet::SharesheetService::OnTargetSelected(aura::Window\*, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, sharesheet::TargetType, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), views::View\*) ././../../chrome/browser/sharesheet/sharesheet\_service.cc:149:19  

#4 0x55874bf13dc4 in sharesheet::SharesheetServiceDelegator::OnTargetSelected(std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, sharesheet::TargetType, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), views::View\*) ././../../chrome/browser/sharesheet/sharesheet\_service\_delegator.cc:111:24  

#5 0x5587505d12e5 in ash::sharesheet::SharesheetBubbleView::TargetButtonPressed(sharesheet::TargetInfo) ././../../chrome/browser/ui/ash/sharesheet/sharesheet\_bubble\_view.cc:685:15  

#6 0x5587505d3f4e in void base::internal::FunctorTraits<void (ash::sharesheet::SharesheetBubbleView::\*)(sharesheet::TargetInfo), void>::Invoke<void (ash::sharesheet::SharesheetBubbleView::\*)(sharesheet::TargetInfo), ash::sharesheet::SharesheetBubbleView\*, sharesheet::TargetInfo const&>(void (ash::sharesheet::SharesheetBubbleView::\*)(sharesheet::TargetInfo), ash::sharesheet::SharesheetBubbleView\*&&, sharesheet::TargetInfo const&) ./../../base/bind\_internal.h:542:12  

#7 0x5587505d3d10 in MakeItSo<void (ash::sharesheet::SharesheetBubbleView::\*const &)(sharesheet::TargetInfo), ash::sharesheet::SharesheetBubbleView \*, const sharesheet::TargetInfo &> ./../../base/bind\_internal.h:706:12  

#8 0x5587505d3d10 in RunImpl<void (ash::sharesheet::SharesheetBubbleView::\*const &)(sharesheet::TargetInfo), const std::\_\_1::tuple<base::internal::UnretainedWrapper[ash::sharesheet::SharesheetBubbleView](javascript:void(0);), sharesheet::TargetInfo> &, 0UL, 1UL> ./../../base/bind\_internal.h:779:12  

#9 0x5587505d3d10 in base::internal::Invoker<base::internal::BindState<void (ash::sharesheet::SharesheetBubbleView::\*)(sharesheet::TargetInfo), base::internal::UnretainedWrapper[ash::sharesheet::SharesheetBubbleView](javascript:void(0);), sharesheet::TargetInfo>, void ()>::Run(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:761:12  

#10 0x558749c1f818 in Run ./../../base/callback.h:241:12  

#11 0x558749c1f818 in operator() ././../../ui/views/controls/button/button.cc:112:68  

#12 0x558749c1f818 in Invoke<const (lambda at ../../ui/views/controls/button/button.cc:111:31) &, const base::RepeatingCallback<void ()> &, const ui::Event &> ./../../base/bind\_internal.h:423:12  

#13 0x558749c1f818 in MakeItSo<const (lambda at ../../ui/views/controls/button/button.cc:111:31) &, const base::RepeatingCallback<void ()> &, const ui::Event &> ./../../base/bind\_internal.h:706:12  

#14 0x558749c1f818 in RunImpl<const (lambda at ../../ui/views/controls/button/button.cc:111:31) &, const std::\_\_1::tuple<base::RepeatingCallback<void ()> > &, 0UL> ./../../base/bind\_internal.h:779:12  

#15 0x558749c1f818 in base::internal::Invoker<base::internal::BindState<views::Button::PressedCallback::PressedCallback(base::RepeatingCallback<void ()>)::$\_0, base::RepeatingCallback<void ()> >, void (ui::Event const&)>::Run(base::internal::BindStateBase\*, ui::Event const&) ./../../base/bind\_internal.h:761:12  

#16 0x558749c1a1ba in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ././../../ui/views/controls/button/button.cc:67:13  

#17 0x558749c21c46 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ././../../ui/views/controls/button/button\_controller.cc:0:34  

#18 0x558749bef0a5 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ././../../ui/events/scoped\_target\_handler.cc:28:24  

#19 0x558745fc0e9b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:190:12  

#20 0x558745fc0460 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:139:5  

#21 0x558745fbff34 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:83:14  

#22 0x558745fbfca0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:55:15  

#23 0x558749d88b4f in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ././../../ui/views/widget/root\_view.cc:485:9  

#24 0x558749d9dd9c in views::Widget::OnMouseEvent(ui::MouseEvent\*) ././../../ui/views/widget/widget.cc:1538:20  

#25 0x558745fc0e9b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:190:12  

#26 0x558745fc0460 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:139:5  

#27 0x558745fbff34 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:83:14  

#28 0x558745fbfca0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ././../../ui/events/event\_dispatcher.cc:55:15  

#29 0x55874997231f in ui::EventProcessor::OnEventFromSource(ui::Event\*) ././../../ui/events/event\_processor.cc:49:17  

#30 0x558745fc443e in ui::EventSource::DeliverEventToSink(ui::Event\*) ././../../ui/events/event\_source.cc:118:16  

#31 0x558745fc4936 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ././../../ui/events/event\_source.cc:66:14  

#32 0x558745fc305b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ././../../ui/events/event\_rewriter.cc:88:39  

#33 0x558739fe39e5 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ././../../ui/chromeos/events/event\_rewriter\_chromeos.cc:1274:12  

#34 0x558739fe3f25 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ././../../ui/chromeos/events/event\_rewriter\_chromeos.cc:758:12  

#35 0x558745fc48e6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ././../../ui/events/event\_source.cc:67:32  

#36 0x558745fc305b in ui::EventRewriter::SendEvent(base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);), ui::Event const\*) ././../../ui/events/event\_rewriter.cc:88:39  

#37 0x55874a013ef0 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ././../../ash/events/keyboard\_driven\_event\_rewriter.cc:31:12

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-966389/chrome+0x2197f6d1) (BuildId: fd415d5d367e074f)  

Shadow bytes around the buggy address:  

0x0c3080008a40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008a50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008a60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008a70: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3080008a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c3080008a90:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008aa0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008ab0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008ac0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008ad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3080008ae0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==67126==ABORTING

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 256 B)
- [Screen.webm](attachments/Screen.webm) (video/webm, 2.7 MB)
- screen.webm (video/webm, 601.7 KB)

## Timeline

### [Deleted User] (2022-02-04)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-02-04)

Thanks for the report! I don't have a ChromeOS device, but the crash looks legit from the screencast. Adding Windows as potentially affected since WebShare is enabled on both platforms (according to https://crbug.com/770595). Marking severity as high since it requires multiple user gestures to trigger the UAF. Marking FoundIn to 97 since the code is landed in 2020.

hansenmichael@, could you take a look? Thanks!

[Monorail components: Blink>WebShare]

### xi...@chromium.org (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-02-08)

[Empty comment from Monorail migration]

### ha...@google.com (2022-02-08)

I can repro in 100.0.4867.0. The UAF occurs when we call a method on |web_view_| here:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/nearby_sharing/sharesheet/nearby_share_action.cc;l=257-258;drc=501d5b2f06743f606a0734d4e34f9f1bc3960cf0

You can reproduce this with the following:

1) Open a sharesheet and select "Nearby" in window A.
2) Open a sharesheet and select "Nearby" in window B.
3) Click "Cancel" to close the sharesheet in window B.
4) Click on the sharesheet UI in window A to focus it.
5) Hit any key, such as "Enter".

NearbyShareAction does not properly handle the scenario where multiple sharesheets are opened simultaneously, and we lose the reference to the WebView for window A when we open window B. I'm preparing a fix in which we will handle keyboard events in NearbyShareDialogUI instead.


### ha...@google.com (2022-02-08)

Fix is in review at crrev.com/c/3449337

### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d9e826b165b03da422727cc0905b05780b1a66d

commit 2d9e826b165b03da422727cc0905b05780b1a66d
Author: Michael Hansen <hansenmichael@google.com>
Date: Wed Feb 09 21:33:14 2022

[Nearby] Handle keyboard events in NearbyShareDialogUI

This moves the responsibility for handling keyboard events from
NearbyShareAction to NearbyShareDialogUI.

Only one instance of NearbyShareAction is created and reused by the
SharesheetService. We previously stored a reference to a WebView in
NearbyShareAction so that we could use its FocusManager in the handling
of keyboard events. But opening and closing multiple sharesheets in a
specific sequence could lead to a UAF as in crbug.com/1294097.

Shifting this responsibility to NearbyShareDialogUI allows multiple
sharesheets to exist safely at the same time.

Manually verified by testing various sequences with multiple sharesheets
on-device.

Bug: 1294097
Change-Id: I7c737057ee70e31e5221ef6ac6e97d47735db798
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449337
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Cr-Commit-Position: refs/heads/main@{#969113}

[modify] https://crrev.com/2d9e826b165b03da422727cc0905b05780b1a66d/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.cc
[modify] https://crrev.com/2d9e826b165b03da422727cc0905b05780b1a66d/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.cc
[modify] https://crrev.com/2d9e826b165b03da422727cc0905b05780b1a66d/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.h
[modify] https://crrev.com/2d9e826b165b03da422727cc0905b05780b1a66d/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.h


### ha...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### ha...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### ha...@google.com (2022-02-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-02-10)

I'm not able to repro this crash in linux-release-chromeos_asan-linux-release-969124

Thanks for the quick fix! 


### am...@chromium.org (2022-02-10)

Based on the CL and merge request, updating this issue as Fixed. In the future, please simply updated issue status to Fixed as soon as resolving commits are landed, as this will allow the bot to add the appropriate security and merge review labels. :) Thank you! 
This issue was foundin-97, so it will need a merge review to M98 as well. Since it's been <24 hours since the fix CL landed, it preferable that this get a bit more bake time on canary before we merge to beta or stable. 

### [Deleted User] (2022-02-10)

Merge review required: M99 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-16)

Merge approved for M99, please merge to branch 4844 at your earliest convenience. 
Merge approved for M98; please merge to branch 4758 so this fix can be included in M98 as it goes into Extended Stable support. Thank you 

### sr...@google.com (2022-02-17)

For M98 pls merge after next tuesday ( Feb 22) 

### pb...@google.com (2022-02-17)

[Bulk update] Your change has been approved for M99 branch please refer to go/chrome-branches for branch info and merge the CL's to M99 branch manually asap so that they would be part of next week's M99 Beta release.

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thanks for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### ha...@google.com (2022-02-18)

Merges are in review at crrev.com/c/3475473 and crrev.com/c/3474339. These should land early next week in time for the next Release of M-99 Beta.

### [Deleted User] (2022-02-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a9824a8bff47b9699bf2df1d59cf30d1ef3b9201

commit a9824a8bff47b9699bf2df1d59cf30d1ef3b9201
Author: Michael Hansen <hansenmichael@google.com>
Date: Tue Feb 22 17:56:05 2022

[Nearby] Handle keyboard events in NearbyShareDialogUI

This moves the responsibility for handling keyboard events from
NearbyShareAction to NearbyShareDialogUI.

Only one instance of NearbyShareAction is created and reused by the
SharesheetService. We previously stored a reference to a WebView in
NearbyShareAction so that we could use its FocusManager in the handling
of keyboard events. But opening and closing multiple sharesheets in a
specific sequence could lead to a UAF as in crbug.com/1294097.

Shifting this responsibility to NearbyShareDialogUI allows multiple
sharesheets to exist safely at the same time.

Manually verified by testing various sequences with multiple sharesheets
on-device.

(cherry picked from commit 2d9e826b165b03da422727cc0905b05780b1a66d)

Bug: 1294097
Change-Id: I7c737057ee70e31e5221ef6ac6e97d47735db798
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449337
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#969113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3474339
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#767}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/a9824a8bff47b9699bf2df1d59cf30d1ef3b9201/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.cc
[modify] https://crrev.com/a9824a8bff47b9699bf2df1d59cf30d1ef3b9201/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.cc
[modify] https://crrev.com/a9824a8bff47b9699bf2df1d59cf30d1ef3b9201/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.h
[modify] https://crrev.com/a9824a8bff47b9699bf2df1d59cf30d1ef3b9201/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.h


### [Deleted User] (2022-02-22)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e30c255bcafdeb25ec1f634dba8540c8e93db5df

commit e30c255bcafdeb25ec1f634dba8540c8e93db5df
Author: Michael Hansen <hansenmichael@google.com>
Date: Tue Feb 22 18:18:12 2022

[Nearby] Handle keyboard events in NearbyShareDialogUI

This moves the responsibility for handling keyboard events from
NearbyShareAction to NearbyShareDialogUI.

Only one instance of NearbyShareAction is created and reused by the
SharesheetService. We previously stored a reference to a WebView in
NearbyShareAction so that we could use its FocusManager in the handling
of keyboard events. But opening and closing multiple sharesheets in a
specific sequence could lead to a UAF as in crbug.com/1294097.

Shifting this responsibility to NearbyShareDialogUI allows multiple
sharesheets to exist safely at the same time.

Manually verified by testing various sequences with multiple sharesheets
on-device.

(cherry picked from commit 2d9e826b165b03da422727cc0905b05780b1a66d)

Bug: 1294097
Change-Id: I7c737057ee70e31e5221ef6ac6e97d47735db798
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449337
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#969113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3475473
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4758@{#1190}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/e30c255bcafdeb25ec1f634dba8540c8e93db5df/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.cc
[modify] https://crrev.com/e30c255bcafdeb25ec1f634dba8540c8e93db5df/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.cc
[modify] https://crrev.com/e30c255bcafdeb25ec1f634dba8540c8e93db5df/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.h
[modify] https://crrev.com/e30c255bcafdeb25ec1f634dba8540c8e93db5df/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.h


### rz...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-23)

1. Just https://crrev.com/c/3483656
2. Low, no conflicts
3. 98, 99
4. Yes

### gm...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8649511cc77ce6dbe6194480e4afd10eab4a127c

commit 8649511cc77ce6dbe6194480e4afd10eab4a127c
Author: Michael Hansen <hansenmichael@google.com>
Date: Thu Feb 24 15:44:53 2022

[M96-LTS][Nearby] Handle keyboard events in NearbyShareDialogUI

This moves the responsibility for handling keyboard events from
NearbyShareAction to NearbyShareDialogUI.

Only one instance of NearbyShareAction is created and reused by the
SharesheetService. We previously stored a reference to a WebView in
NearbyShareAction so that we could use its FocusManager in the handling
of keyboard events. But opening and closing multiple sharesheets in a
specific sequence could lead to a UAF as in crbug.com/1294097.

Shifting this responsibility to NearbyShareDialogUI allows multiple
sharesheets to exist safely at the same time.

Manually verified by testing various sequences with multiple sharesheets
on-device.

(cherry picked from commit 2d9e826b165b03da422727cc0905b05780b1a66d)

Bug: 1294097
Change-Id: I7c737057ee70e31e5221ef6ac6e97d47735db798
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449337
Commit-Queue: Michael Hansen <hansenmichael@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#969113}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3483656
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1506}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/8649511cc77ce6dbe6194480e4afd10eab4a127c/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.cc
[modify] https://crrev.com/8649511cc77ce6dbe6194480e4afd10eab4a127c/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.cc
[modify] https://crrev.com/8649511cc77ce6dbe6194480e4afd10eab4a127c/chrome/browser/nearby_sharing/sharesheet/nearby_share_action.h
[modify] https://crrev.com/8649511cc77ce6dbe6194480e4afd10eab4a127c/chrome/browser/ui/webui/nearby_share/nearby_share_dialog_ui.h


### rz...@google.com (2022-02-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1294097?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1295073]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058679)*
