# Security: Heap-use-after-free in ash::WizardController::HandleAccelerator

| Field | Value |
|-------|-------|
| **Issue ID** | [40063005](https://issues.chromium.org/issues/40063005) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dk...@google.com |
| **Created** | 2023-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 112.0.5585.0  

Operating System: chromeOS

**REPRODUCTION CASE**

Similar to <https://crbug.com/chromium/1283609>

1. ./chrome --isolation-by-default --login-manager
2. Click on ESC key

=================================================================  

==17439==ERROR: AddressSanitizer: heap-use-after-free on address 0x60e0001145a0 at pc 0x561afdd322f9 bp 0x7fff0947e4c0 sp 0x7fff0947e4b8  

READ of size 8 at 0x60e0001145a0 thread T0 (chrome)  

==17439==WARNING: invalid path to external symbolizer!  

==17439==WARNING: Failed to use and restart external symbolizer!  

#0 0x561afdd322f8 in ash::WizardController::HandleAccelerator(ash::LoginAcceleratorAction) ./../../chrome/browser/ash/login/wizard\_controller.cc:2418:26  

#1 0x561afdc7dc03 in ash::LoginDisplayHostCommon::HandleAccelerator(ash::LoginAcceleratorAction) ./../../chrome/browser/ash/login/ui/login\_display\_host\_common.cc:451:30  

#2 0x561b0296e2d4 in TryProcess ./../../ui/base/accelerators/accelerator\_manager.cc:153:17  

#3 0x561b0296e2d4 in ui::AcceleratorManager::Process(ui::Accelerator const&) ./../../ui/base/accelerators/accelerator\_manager.cc:83:27  

#4 0x561b0757feff in views::FocusManager::ProcessAccelerator(ui::Accelerator const&) ./../../ui/views/focus/focus\_manager.cc:524:28  

#5 0x561b1460dd8b in views::UnhandledKeyboardEventHandler::HandleKeyboardEvent(content::NativeWebKeyboardEvent const&, views::FocusManager\*) ./../../ui/views/controls/webview/unhandled\_keyboard\_event\_handler.cc:46:24  

#6 0x561afdcb6026 in ash::WebUILoginView::HandleKeyboardEvent(content::WebContents\*, content::NativeWebKeyboardEvent const&) ./../../chrome/browser/ash/login/ui/webui\_login\_view.cc:334:49  

#7 0x561af8fe9617 in content::RenderWidgetHostImpl::OnKeyboardEventAck(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState) ./../../content/browser/renderer\_host/render\_widget\_host\_impl.cc:2481:16  

#8 0x561af8c1fb07 in Run ./../../base/functional/callback.h:152:12  

#9 0x561af8c1fb07 in content::InputRouterImpl::KeyboardEventHandled(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)) ./../../content/browser/renderer\_host/input/input\_router\_impl.cc:677:36  

#10 0x561af8c28e48 in void base::internal::FunctorTraits<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), void>::Invoke<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);) >(void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);)&&, content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);)&&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>&&, blink::mojom::InputEventResultSource&&, ui::LatencyInfo const&, blink::mojom::InputEventResultState&&, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:745:12  

#11 0x561af8c28a86 in MakeItSo<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), std::Cr::tuple<base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);) > ./../../base/functional/bind\_internal.h:947:5  

#12 0x561af8c28a86 in RunImpl<void (content::InputRouterImpl::\*)(const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), std::Cr::tuple<base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (const content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) &, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1019:12  

#13 0x561af8c28a86 in base::internal::Invoker<base::internal::BindState<void (content::InputRouterImpl::\*)(content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)), base::WeakPtr[content::InputRouterImpl](javascript:void(0);), content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);), base::OnceCallback<void (content::EventWithLatencyInfo[content::NativeWebKeyboardEvent](javascript:void(0);) const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)> >, void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:970:12  

#14 0x561af8c2e654 in Run ./../../base/functional/callback.h:152:12  

#15 0x561af8c2e654 in operator() ./../../content/browser/renderer\_host/input/input\_router\_impl.cc:638:35  

#16 0x561af8c2e654 in Invoke<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:622:13), base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);), blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);) > ./../../base/functional/bind\_internal.h:620:12  

#17 0x561af8c2e654 in MakeItSo<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:622:13), std::Cr::tuple<base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >, blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);) > ./../../base/functional/bind\_internal.h:924:12  

#18 0x561af8c2e654 in RunImpl<(lambda at ../../content/browser/renderer\_host/input/input\_router\_impl.cc:622:13), std::Cr::tuple<base::OnceCallback<void (blink::mojom::InputEventResultSource, const ui::LatencyInfo &, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1019:12  

#19 0x561af8c2e654 in base::internal::Invoker<base::internal::BindState<content::InputRouterImpl::FilterAndSendWebInputEvent(blink::WebInputEvent const&, ui::LatencyInfo const&, base::OnceCallback<void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>)::$\_1, base::OnceCallback<void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>, base::WeakPtr[content::InputRouterImpl](javascript:void(0);) >, void (blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);), mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);), mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);))>::RunOnce(base::internal::BindStateBase\*, blink::mojom::InputEventResultSource, ui::LatencyInfo const&, blink::mojom::InputEventResultState, mojo::StructPtr[blink::mojom::DidOverscrollParams](javascript:void(0);)&&, mojo::InlinedStructPtr[blink::mojom::TouchActionOptional](javascript:void(0);)&&, mojo::StructPtr[blink::mojom::ScrollResultData](javascript:void(0);)&&) ./../../base/functional/bind\_internal.h:970:12  

#20 0x561af398fbac in Run ./../../base/functional/callback.h:152:12  

#21 0x561af398fbac in blink::mojom::WidgetInputHandler\_DispatchEvent\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/input/input\_handler.mojom.cc:6622:26  

#22 0x561b02654643 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1002:41  

#23 0x561b0266c2e0 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#24 0x561b02658bdb in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:694:20  

#25 0x561b02675e3c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1096:42  

#26 0x561b02674ce3 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:710:7  

#27 0x561b0266c2e0 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#28 0x561b0264c1a4 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase[mojo::MessageHandle](javascript:void(0);)) ./../../mojo/public/cpp/bindings/lib/connector.cc:550:49  

#29 0x561b0264d6ec in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:607:14  

#30 0x561af3d2438f in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/functional/callback.h:333:12  

#31 0x561b026cbc59 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/functional/callback.h:333:12  

#32 0x561b026cb7df in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#33 0x561b00270e46 in Run ./../../base/functional/callback.h:152:12  

#34 0x561b00270e46 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:165:32  

#35 0x561b002c03e9 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:491:11)> ./../../base/task/common/task\_annotator.h:87:5  

#36 0x561b002c03e9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:489:23  

#37 0x561b002bf41f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:340:30  

#38 0x561b002c1724 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#39 0x561b003e4bd6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#40 0x561b002c21c9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:649:12  

#41 0x561b001f1ef1 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#42 0x561af8045f0a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1066:18  

#43 0x561af804b622 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15  

#44 0x561af803f7a3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#45 0x561afe963910 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:715:10  

#46 0x561afe965edb in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1266:10  

#47 0x561afe9658e5 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1120:12  

#48 0x561afe95f2e1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:335:36  

#49 0x561afe960119 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:363:10  

#50 0x561aef8c3ba7 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#51 0x7f9f518c00b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60e0001145a0 is located 0 bytes inside of 160-byte region [0x60e0001145a0,0x60e000114640)  

freed by thread T0 (chrome) here:  

#0 0x561aef8c1a9d in operator delete(void\*) *asan\_rtl*:3  

#1 0x561afdb6cf37 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#2 0x561afdb6cf37 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#3 0x561afdb6cf37 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#4 0x561afdb6cf37 in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:63:29  

#5 0x561afdb6cf37 in void std::Cr::\_\_destroy\_at[abi:v170000]<std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > >, 0>(std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > >\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#6 0x561afdb6f7ad in destroy\_at<std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:91:5  

#7 0x561afdb6f7ad in destroy<std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#8 0x561afdb6f7ad in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:836:9  

#9 0x561afdb6f7ad in \_\_clear ./../../buildtools/third\_party/libc++/trunk/include/vector:830:29  

#10 0x561afdb6f7ad in std::Cr::vector<std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > >, std::Cr::allocator<std::Cr::pair<ash::OobeScreenId, std::Cr::unique\_ptr<ash::BaseScreen, std::Cr::default\_delete[ash::BaseScreen](javascript:void(0);) > > > >::clearabi:v170000 ./../../buildtools/third\_party/libc++/trunk/include/vector:643:9  

#11 0x561afdd1016e in ash::WizardController::OnDestroyingOobeUI() ./../../chrome/browser/ash/login/wizard\_controller.cc:498:20  

#12 0x561b139c656a in ash::OobeUI::~OobeUI() ./../../chrome/browser/ui/webui/ash/login/oobe\_ui.cc:590:14  

#13 0x561b139c6e63 in ash::OobeUI::~OobeUI() ./../../chrome/browser/ui/webui/ash/login/oobe\_ui.cc:588:19  

#14 0x561af953c682 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#15 0x561af953c682 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#16 0x561af953c682 in content::WebUIImpl::~WebUIImpl() ./../../content/browser/webui/web\_ui\_impl.cc:87:15  

#17 0x561af953cba1 in content::WebUIImpl::~WebUIImpl() ./../../content/browser/webui/web\_ui\_impl.cc:81:25  

#18 0x561af8e60868 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#19 0x561af8e60868 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#20 0x561af8e60868 in ClearWebUI ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:9783:11  

#21 0x561af8e60868 in content::RenderFrameHostImpl::OnUnloaded() ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:5172:3  

#22 0x561af8e8ad42 in content::RenderFrameHostImpl::OnUnloadACK() ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:5159:3  

#23 0x561af7a3b604 in content::mojom::AgentSchedulingGroupHostStubDispatch::Accept(content::mojom::AgentSchedulingGroupHost\*, mojo::Message\*) ./gen/content/common/agent\_scheduling\_group.mojom.cc:182:13  

#24 0x561b02654300 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1007:54  

#25 0x561b0266c2e0 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#26 0x561b02658bdb in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:694:20  

#27 0x561b038a1eef in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1075:24  

#28 0x561b0389a991 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind\_internal.h:745:12  

#29 0x561b0389a991 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind\_internal.h:924:12  

#30 0x561b0389a991 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1019:12  

#31 0x561b0389a991 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:970:12  

#32 0x561b00270e46 in Run ./../../base/functional/callback.h:152:12  

#33 0x561b00270e46 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:165:32  

#34 0x561b002c03e9 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:491:11)> ./../../base/task/common/task\_annotator.h:87:5  

#35 0x561b002c03e9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:489:23  

#36 0x561b002bf41f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:340:30  

#37 0x561b002c1724 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#38 0x561b003e4bd6 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:290:55  

#39 0x561b002c21c9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:649:12  

#40 0x561b001f1ef1 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#41 0x561af8045f0a in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1066:18  

#42 0x561af804b622 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15  

#43 0x561af803f7a3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#44 0x561afe963910 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:715:10  

#45 0x561afe965edb in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1266:10  

#46 0x561afe9658e5 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1120:12  

#47 0x561afe95f2e1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:335:36

previously allocated by thread T0 (chrome) here:  

#0 0x561aef8c123d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x561afdd070e0 in make\_unique<ash::UserCreationScreen, base::WeakPtr[ash::UserCreationView](javascript:void(0);), ash::ErrorScreen \*, base::RepeatingCallback<void (ash::UserCreationScreen::Result)> > ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:26  

#2 0x561afdd070e0 in ash::WizardController::CreateScreens() ./../../chrome/browser/ash/login/wizard\_controller.cc:789:10  

#3 0x561afdcfbbc6 in ash::WizardController::WizardController(ash::WizardContext\*) ./../../chrome/browser/ash/login/wizard\_controller.cc:420:27  

#4 0x561afdc90bcd in make\_unique<ash::WizardController, ash::WizardContext \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#5 0x561afdc90bcd in ash::LoginDisplayHostWebUI::StartWizard(ash::OobeScreenId) ./../../chrome/browser/ash/login/ui/login\_display\_host\_webui.cc:558:26  

#6 0x561afdc99e9f in ash::(anonymous namespace)::ShowLoginWizardFinish(ash::OobeScreenId, ash::StartupCustomizationDocument const\*) ./../../chrome/browser/ash/login/ui/login\_display\_host\_webui.cc:261:19  

#7 0x561afdc989e4 in ash::(anonymous namespace)::TriggerShowLoginWizardFinish(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> >, std::Cr::unique\_ptr<ash::(anonymous namespace)::ShowLoginWizardSwitchLanguageCallbackData, std::Cr::default\_delete<ash::(anonymous namespace)::ShowLoginWizardSwitchLanguageCallbackData> >) ./../../chrome/browser/ash/login/ui/login\_display\_host\_webui.cc:320:5  

#8 0x561afdc97566 in ash::ShowLoginWizard(ash::OobeScreenId) ./../../chrome/browser/ash/login/ui/login\_display\_host\_webui.cc:1197:5  

#9 0x561afdc2e7c3 in ash::(anonymous namespace)::StartLoginOobeSession() ./../../chrome/browser/ash/login/session/chrome\_session\_manager.cc:83:3  

#10 0x561afdc2dde5 in ash::ChromeSessionManager::Initialize(base::CommandLine const&, Profile\*, bool) ./../../chrome/browser/ash/login/session/chrome\_session\_manager.cc:385:5  

#11 0x561afd4d4d66 in ash::ChromeBrowserMainPartsAsh::PostProfileInit(Profile\*, bool) ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1239:60  

#12 0x561b08314820 in CallPostProfileInit ./../../chrome/browser/chrome\_browser\_main.cc:1201:3  

#13 0x561b08314820 in ChromeBrowserMainParts::ProfileInitManager::ProfileInitManager(ChromeBrowserMainParts\*, Profile\*) ./../../chrome/browser/chrome\_browser\_main.cc:539:20  

#14 0x561b08318cd7 in make\_unique<ChromeBrowserMainParts::ProfileInitManager, ChromeBrowserMainParts \*, Profile \*&> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#15 0x561b08318cd7 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome\_browser\_main.cc:1606:27  

#16 0x561b08318185 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1142:18  

#17 0x561afd4d0e20 in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:834:39  

#18 0x561af8043b36 in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser\_main\_loop.cc:980:28  

#19 0x561af92f9fe7 in Run ./../../base/functional/callback.h:152:12  

#20 0x561af92f9fe7 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup\_task\_runner.cc:44:29  

#21 0x561af804300b in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser\_main\_loop.cc:890:25  

#22 0x561af804ad63 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser\_main\_runner\_impl.cc:141:15  

#23 0x561af803f764 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:28:32  

#24 0x561afe963910 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:715:10  

#25 0x561afe965edb in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1266:10  

#26 0x561afe9658e5 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1120:12  

#27 0x561afe95f2e1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:335:36  

#28 0x561afe960119 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:363:10  

#29 0x561aef8c3ba7 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#30 0x7f9f518c00b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1102945/chrome+0x1ee692f8) (BuildId: b229b6ac918d058c)  

Shadow bytes around the buggy address:  

0x60e000114300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000114380: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd  

0x60e000114400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000114480: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x60e000114500: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x60e000114580: fa fa fa fa[fd]fd fd fd fd fd fd fd fd fd fd fd  

0x60e000114600: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x60e000114680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000114700: fd fd fd fd fa fa fa fa fa fa fa fa fd fd fd fd  

0x60e000114780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60e000114800: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

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

- [Screencast from 10 فبراير, 2023 +01 00:42:12.webm](attachments/Screencast from 10 فبراير, 2023 +01 00_42_12.webm) (video/webm, 1.2 MB)

## Timeline

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-10)

Over to ChromeOS security bug triage

### pa...@chromium.org (2023-02-15)

rbock@ and andreydav@: Could you please take a look, or CC/assign to someone who can? Thanks! :)

[Monorail components: UI>Shell]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### an...@google.com (2023-02-16)

Adding Danila from the OOBE team to take a look

### rb...@google.com (2023-02-16)

Hey Danila,

Can you take over as an owner? I am currently neck deep in a P0.

Happy to take a look next week. Feel free to ping me.

Thanks,
Roland

### dk...@google.com (2023-02-16)

Sure, looks like it is happening somewhere in WizardController, I'll take a look. 

### [Deleted User] (2023-02-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dk...@google.com (2023-02-20)

For some reason adding --isolation-by-default switch makes OobeUI to be destroyed after creation, but the first screen of the OOBE flow is already set by WizardController. WizardController::OnDestroyingOobeUI() deletes all of the screens, but doesn't reset the current_screen_. So when the WizardController::HandleAccelerator is called after pressing the ESC button, the current_screen_ pointer points to the memory that was already freed. I have a CL to reset the current_screen_ of the WizardController more carefully on OobeUI destruction.

CL: https://chromium-review.googlesource.com/c/chromium/src/+/4272608

### dk...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46cebedf0e806ca2c24c80ec75eef4c52641096b

commit 46cebedf0e806ca2c24c80ec75eef4c52641096b
Author: Danila Kuzmin <dkuzmin@google.com>
Date: Wed Feb 22 10:53:42 2023

[OOBE]: Reset curren_screen_ of WizardController on OobeUI destruction

Bug: 1414581
Change-Id: If94f5cb470f1a2d675349a0e0713b00092dfab09
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4272608
Commit-Queue: Danila Kuzmin <dkuzmin@google.com>
Reviewed-by: Renato Silva <rrsilva@google.com>
Cr-Commit-Position: refs/heads/main@{#1108250}

[modify] https://crrev.com/46cebedf0e806ca2c24c80ec75eef4c52641096b/chrome/browser/ash/login/wizard_controller.cc


### dk...@google.com (2023-02-22)

Should be fixed 

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

Not requesting merge to dev (M112) because latest trunk commit (1108250) appears to be prior to dev branch point (1109224). If this is incorrect, please replace the Merge-NA-112 label with Merge-Request-112. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M112 is already shipping to stable.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Khalil! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### ob...@google.com (2023-03-27)

Hello dkuzmin@google.com amyressler@google.com for this is there any review you want considered by the Release team?

### am...@chromium.org (2023-03-27)

hi obenedict@, it looks like this issue was foundin- / impacts only as far back as 112 and the fix was landed in 112, so no merge would be needed here. 
It also appears that this is a ChromeOS issue;  I am on the Chrome browser security team, so merge review conversations for issues that impact ChromeOS should probably be deferred to someone on the ChromeOS security team, such as palmer@, roxabee@, &| chmiel@ in the future. Thanks! 

### ob...@google.com (2023-03-28)

Thank you. With the 'Merge-Review-112' it caught my attention.

I will remove the `Merge-Review-112` label.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414581?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1414579]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063005)*
