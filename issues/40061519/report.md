# Security: heap-use-after-free browser\renderer_host\render_process_host_impl.cc:2068 in content::RenderProcessHostImpl::CreateNotificationService

| Field | Value |
|-------|-------|
| **Issue ID** | [40061519](https://issues.chromium.org/issues/40061519) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation>BFCache, UI>Notifications |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2022-10-29 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

commit 4f54ba6adfa8f619fd7f6993649bdc68e1b3a167 (HEAD, origin/main, origin/HEAD)  

Author: Peter Kasting [pkasting@chromium.org](mailto:pkasting@chromium.org)  

Date: Sat Oct 29 01:45:01 2022 +0000

target\_cpu = "x64"  

dcheck\_always\_on = false  

is\_asan = true  

is\_component\_build = true  

is\_debug = false  

enable\_nacl = false  

symbol\_level=2

**REPRODUCTION CASE**  

coming soon

Type of crash: [browser]

RCA  

coming soon

# ASAN

==3028==ERROR: AddressSanitizer: heap-use-after-free on address 0x12521fde5100 at pc 0x7fff938dc22d bp 0x005a9fdf66e0 sp 0x005a9fdf6728  

READ of size 8 at 0x12521fde5100 thread T0  

fuzz->url newPage:<http://localhost/fuzz1/1667028608581_814280/fuzz-00011.html> tick->0 since-> 267.593 headless:0  

#0 0x7fff938dc22c in content::RenderProcessHostImpl::CreateNotificationService D:\chromium\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:2068  

#1 0x7fff9288e73d in base::internal::Invoker<base::internal::BindState<`lambda at ../../content/browser/browser_interface_binders.cc:359:7',base::internal::UnretainedWrapper<content::DedicatedWorkerHost,base::RawPtrBanDanglingIfSupported>,base::internal::UnretainedWrapper<content::RenderFrameHost,base::RawPtrBanDanglingIfSupported>,content::RenderProcessHost::NotificationServiceCreatorType>,void (const url::Origin &, mojo::PendingReceiver<blink::mojom::NotificationService>)>::Run D:\chromium\src\base\functional\bind_internal.h:883 #2 0x7fff9288ee51 in base::RepeatingCallback<void (const url::Origin &, mojo::PendingReceiver<blink::mojom::NotificationService>)>::Run D:\chromium\src\base\functional\callback.h:309 #3 0x7fff9288eaf2 in mojo::internal::BinderContextTraits<const url::Origin &>::BindGenericReceiver<blink::mojom::NotificationService> D:\chromium\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:39 #4 0x7fff9288ecfa in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (const url::Origin &, mojo::PendingReceiver<blink::mojom::NotificationService>)> &, const url::Origin &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>),base::RepeatingCallback<void (const url::Origin &, mojo::PendingReceiver<blink::mojom::NotificationService>)> >,void (const url::Origin &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>)>::Run D:\chromium\src\base\functional\bind_internal.h:883 #5 0x7fff93f1e897 in base::RepeatingCallback<void (const url::Origin &, mojo::ScopedHandleBase<mojo::MessagePipeHandle>)>::Run D:\chromium\src\base\functional\callback.h:309 #6 0x7fff93f1e41b in mojo::internal::GenericCallbackBinderWithContext<const url::Origin &>::RunCallbackWithContext D:\chromium\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:120 #7 0x7fff93f1dfb7 in mojo::internal::GenericCallbackBinderWithContext<const url::Origin &>::BindInterface D:\chromium\src\mojo\public\cpp\bindings\lib\binder_map_internal.h:101 #8 0x7fff93f1db70 in mojo::BinderMapWithContext<const url::Origin &>::TryBind D:\chromium\src\mojo\public\cpp\bindings\binder_map.h:111 #9 0x7fff93f1d8bb in content::BrowserInterfaceBrokerImpl<content::DedicatedWorkerHost,const url::Origin &>::BindInterface D:\chromium\src\content\browser\browser_interface_broker_impl.h:90 #10 0x7fff93f1d495 in content::BrowserInterfaceBrokerImpl<content::DedicatedWorkerHost,const url::Origin &>::GetInterface D:\chromium\src\content\browser\browser_interface_broker_impl.h:60 #11 0x7fff8cde441c in blink::mojom::BrowserInterfaceBrokerStubDispatch::Accept D:\chromium\src\out\asan\gen\third_party\blink\public\mojom\browser_interface_broker.mojom.cc:186 #12 0x7fffd11dd6a1 in mojo::InterfaceEndpointClient::HandleValidatedMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:989 #13 0x7fffd11f0fb0 in mojo::MessageDispatcher::Accept D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #14 0x7fffd11e1a12 in mojo::InterfaceEndpointClient::HandleIncomingMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:689 #15 0x7fffd11fdc1f in mojo::internal::MultiplexRouter::ProcessIncomingMessage D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096 #16 0x7fffd11fcabf in mojo::internal::MultiplexRouter::Accept D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:716 #17 0x7fffd11f0fb0 in mojo::MessageDispatcher::Accept D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #18 0x7fffd11cad94 in mojo::Connector::DispatchMessageW D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:561 #19 0x7fffd11cc85b in mojo::Connector::ReadAllAvailableMessages D:\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:618 #20 0x7fffd11cfe3d in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::RawPtrBanDanglingIfSupported> >,void (unsigned int)>::Run D:\chromium\src\base\functional\bind_internal.h:883 #21 0x7fffd11cdd7f in base::RepeatingCallback<void (unsigned int)>::Run D:\chromium\src\base\functional\callback.h:309 #22 0x7fffd11cdc53 in base::internal::Invoker<base::internal::BindState<void (\*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run D:\chromium\src\base\functional\bind_internal.h:883 #23 0x7fffdc2f5239 in base::RepeatingCallback<void (unsigned int, const mojo::HandleSignalsState &)>::Run D:\chromium\src\base\functional\callback.h:309 #24 0x7fffdc2f4e0d in mojo::SimpleWatcher::OnHandleReady D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:278 #25 0x7fffdc2f5fae in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int,mojo::HandleSignalsState>,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:870 #26 0x7fffca1585b9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:134 #27 0x7fffca1b5363 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:448 #28 0x7fffca1b40fd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:299 #29 0x7fffca2cd862 in base::MessagePumpForUI::DoRunLoop D:\chromium\src\base\message_loop\message_pump_win.cc:214 #30 0x7fffca2cb81b in base::MessagePumpWin::Run D:\chromium\src\base\message_loop\message_pump_win.cc:78 #31 0x7fffca1b7715 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:608 #32 0x7fffca0c21de in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:141 #33 0x7fff928a4f17 in content::BrowserMainLoop::RunMainMessageLoop D:\chromium\src\content\browser\browser_main_loop.cc:1048 #34 0x7fff928ac291 in content::BrowserMainRunnerImpl::Run D:\chromium\src\content\browser\browser_main_runner_impl.cc:162 #35 0x7fff6ad46750 in headless::HeadlessContentMainDelegate::RunProcess D:\chromium\src\headless\lib\headless_content_main_delegate.cc:392 #36 0x7fff94e6e63c in content::RunBrowserProcessMain D:\chromium\src\content\app\content_main_runner_impl.cc:705 #37 0x7fff94e72060 in content::ContentMainRunnerImpl::RunBrowser D:\chromium\src\content\app\content_main_runner_impl.cc:1242 #38 0x7fff94e71826 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1102 #39 0x7fff94e6c348 in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:342 #40 0x7fff94e6d172 in content::ContentMain D:\chromium\src\content\app\content_main.cc:370 #41 0x7fff9c7519b0 in headless::`anonymous namespace'::RunContentMain D:\chromium\src\headless\app\headless\_shell.cc:150  

#42 0x7fff9c751533 in headless::HeadlessBrowserMain D:\chromium\src\headless\app\headless\_shell.cc:868  

#43 0x7fff9c7504c5 in headless::HeadlessShellMain D:\chromium\src\headless\app\headless\_shell.cc:807  

#44 0x7fff98271490 in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:160  

#45 0x7ff78b145d3a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#46 0x7ff78b142ae4 in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#47 0x7ff78b407167 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#48 0x7ff8027a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#49 0x7ff8033e26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

0x12521fde5100 is located 0 bytes inside of 5624-byte region [0x12521fde5100,0x12521fde66f8)  

freed by thread T0 here:  

#0 0x7fffc950e18d in operator delete+0x8d (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004e18d)  

#1 0x7fff9384118f in content::RenderFrameHostImpl::~RenderFrameHostImpl D:\chromium\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:1823  

#2 0x7fff9388f340 in content::RenderFrameHostManager::~RenderFrameHostManager D:\chromium\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:359  

#3 0x7fff9352a3ab in content::FrameTreeNode::~FrameTreeNode D:\chromium\src\content\browser\renderer\_host\frame\_tree\_node.cc:331  

#4 0x7fff9351c04d in content::FrameTree::~FrameTree D:\chromium\src\content\browser\renderer\_host\frame\_tree.cc:229  

#5 0x7fff93d4081e in content::WebContentsImpl::~WebContentsImpl D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:1088  

#6 0x7fff93dcf415 in content::WebContentsImpl::~WebContentsImpl D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:978  

#7 0x7fff6ad132d0 in headless::HeadlessWebContentsImpl::~HeadlessWebContentsImpl D:\chromium\src\headless\lib\browser\headless\_web\_contents\_impl.cc:348  

#8 0x7fff6ad174fb in headless::HeadlessWebContentsImpl::~HeadlessWebContentsImpl D:\chromium\src\headless\lib\browser\headless\_web\_contents\_impl.cc:338  

#9 0x7fff6ace687c in std::Cr::\_\_destroy\_at<std::Cr::pair<const std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,0> D:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\construct\_at.h:64  

#10 0x7fff6acec749 in std::Cr::unique\_ptr<std::Cr::\_\_hash\_node<std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,void \*>,std::Cr::\_\_hash\_node\_destructor<std::Cr::allocator<std::Cr::\_\_hash\_node<std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,void \*> > > >::reset D:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:281  

#11 0x7fff6acecc56 in std::Cr::\_\_hash\_table<std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,std::Cr::\_\_unordered\_map\_hasher<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,std::Cr::hash<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,std::Cr::equal\_to<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,1>,std::Cr::\_\_unordered\_map\_equal<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > >,std::Cr::equal\_to<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,std::Cr::hash<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,1>,std::Cr::allocator<std::Cr::\_\_hash\_value\_type<std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >,std::Cr::unique\_ptr<headless::HeadlessWebContents,std::Cr::default\_delete[headless::HeadlessWebContents](javascript:void(0);) > > > >::erase D:\chromium\src\buildtools\third\_party\libc++\trunk\include\_\_hash\_table:2408  

#12 0x7fff6ace4cb3 in headless::HeadlessBrowserContextImpl::DestroyWebContents D:\chromium\src\headless\lib\browser\headless\_browser\_context\_impl.cc:346  

#13 0x7fff6ad297ee in headless::protocol::TargetHandler::CloseTarget D:\chromium\src\headless\lib\browser\protocol\target\_handler.cc:84  

#14 0x7fff6bbe0cc9 in headless::protocol::Target::DomainDispatcherImpl::closeTarget D:\chromium\src\out\asan\gen\headless\lib\browser\protocol\target.cc:122  

#15 0x7fffb581aea9 in crdtp::UberDispatcher::DispatchResult::Run D:\chromium\src\third\_party\inspector\_protocol\crdtp\dispatch.cc:511  

#16 0x7fff6ad1da90 in headless::protocol::HeadlessDevToolsSession::HandleCommand D:\chromium\src\headless\lib\browser\protocol\headless\_devtools\_session.cc:63  

#17 0x7fff6ad061c7 in headless::HeadlessDevToolsManagerDelegate::HandleCommand D:\chromium\src\headless\lib\browser\headless\_devtools\_manager\_delegate.cc:31  

#18 0x7fff92ac4f5c in content::DevToolsSession::DispatchProtocolMessageInternal D:\chromium\src\content\browser\devtools\devtools\_session.cc:345  

#19 0x7fff92ac440e in content::DevToolsSession::DispatchProtocolMessage D:\chromium\src\content\browser\devtools\devtools\_session.cc:313  

#20 0x7fff92a7067b in content::DevToolsAgentHostImpl::DispatchProtocolMessage D:\chromium\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:251  

#21 0x7fff92a8c748 in content::DevToolsHttpHandler::OnWebSocketMessage D:\chromium\src\content\browser\devtools\devtools\_http\_handler.cc:796  

#22 0x7fff92a969d5 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int, std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:870  

#23 0x7fffca1585b9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:134  

#24 0x7fffca1b5363 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:448  

#25 0x7fffca1b40fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:299  

#26 0x7fffca2cd862 in base::MessagePumpForUI::DoRunLoop D:\chromium\src\base\message\_loop\message\_pump\_win.cc:214  

#27 0x7fffca2cb81b in base::MessagePumpWin::Run D:\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#28 0x7fffca1b7715 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:608  

#29 0x7fffca0c21de in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#30 0x7fff928a4f17 in content::BrowserMainLoop::RunMainMessageLoop D:\chromium\src\content\browser\browser\_main\_loop.cc:1048  

#31 0x7fff928ac291 in content::BrowserMainRunnerImpl::Run D:\chromium\src\content\browser\browser\_main\_runner\_impl.cc:162  

#32 0x7fff6ad46750 in headless::HeadlessContentMainDelegate::RunProcess D:\chromium\src\headless\lib\headless\_content\_main\_delegate.cc:392  

#33 0x7fff94e6e63c in content::RunBrowserProcessMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:705  

#34 0x7fff94e72060 in content::ContentMainRunnerImpl::RunBrowser D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1242  

#35 0x7fff94e71826 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1102  

#36 0x7fff94e6c348 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#37 0x7fff94e6d172 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#38 0x7fff9c7519b0 in headless::`anonymous namespace'::RunContentMain D:\chromium\src\headless\app\headless\_shell.cc:150  

#39 0x7fff9c751533 in headless::HeadlessBrowserMain D:\chromium\src\headless\app\headless\_shell.cc:868  

#40 0x7fff9c7504c5 in headless::HeadlessShellMain D:\chromium\src\headless\app\headless\_shell.cc:807  

#41 0x7fff98271490 in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:160  

#42 0x7ff78b145d3a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#43 0x7ff78b142ae4 in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#44 0x7ff78b407167 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#45 0x7ff8027a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)

previously allocated by thread T0 here:  

#0 0x7fffc950d96d in operator new+0x8d (D:\chromium\src\out\asan\clang\_rt.asan\_dynamic-x86\_64.dll+0x18004d96d)  

#1 0x7fff937a46dd in content::RenderFrameHostFactory::Create D:\chromium\src\content\browser\renderer\_host\render\_frame\_host\_factory.cc:38  

#2 0x7fff93890d94 in content::RenderFrameHostManager::CreateRenderFrameHost D:\chromium\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:2849  

#3 0x7fff93890275 in content::RenderFrameHostManager::InitRoot D:\chromium\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:388  

#4 0x7fff93522b60 in content::FrameTree::Init D:\chromium\src\content\browser\renderer\_host\frame\_tree.cc:797  

#5 0x7fff93d60a25 in content::WebContentsImpl::Init D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:3084  

#6 0x7fff93d38a1d in content::WebContentsImpl::CreateWithOpener D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:1141  

#7 0x7fff93d383f2 in content::WebContentsImpl::Create D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:557  

#8 0x7fff93d382ff in content::WebContents::Create D:\chromium\src\content\browser\web\_contents\web\_contents\_impl.cc:552  

#9 0x7fff6ad10fae in headless::HeadlessWebContentsImpl::Create D:\chromium\src\headless\lib\browser\headless\_web\_contents\_impl.cc:255  

#10 0x7fff6ace4653 in headless::HeadlessBrowserContextImpl::CreateWebContents D:\chromium\src\headless\lib\browser\headless\_browser\_context\_impl.cc:322  

#11 0x7fff6ad2924a in headless::protocol::TargetHandler::CreateTarget D:\chromium\src\headless\lib\browser\protocol\target\_handler.cc:72  

#12 0x7fff6bbe1c03 in headless::protocol::Target::DomainDispatcherImpl::createTarget D:\chromium\src\out\asan\gen\headless\lib\browser\protocol\target.cc:179  

#13 0x7fffb581aea9 in crdtp::UberDispatcher::DispatchResult::Run D:\chromium\src\third\_party\inspector\_protocol\crdtp\dispatch.cc:511  

#14 0x7fff6ad1da90 in headless::protocol::HeadlessDevToolsSession::HandleCommand D:\chromium\src\headless\lib\browser\protocol\headless\_devtools\_session.cc:63  

#15 0x7fff6ad061c7 in headless::HeadlessDevToolsManagerDelegate::HandleCommand D:\chromium\src\headless\lib\browser\headless\_devtools\_manager\_delegate.cc:31  

#16 0x7fff92ac4f5c in content::DevToolsSession::DispatchProtocolMessageInternal D:\chromium\src\content\browser\devtools\devtools\_session.cc:345  

#17 0x7fff92ac440e in content::DevToolsSession::DispatchProtocolMessage D:\chromium\src\content\browser\devtools\devtools\_session.cc:313  

#18 0x7fff92a7067b in content::DevToolsAgentHostImpl::DispatchProtocolMessage D:\chromium\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:251  

#19 0x7fff92a8c748 in content::DevToolsHttpHandler::OnWebSocketMessage D:\chromium\src\content\browser\devtools\devtools\_http\_handler.cc:796  

#20 0x7fff92a969d5 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int, std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:870  

#21 0x7fffca1585b9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:134  

#22 0x7fffca1b5363 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:448  

#23 0x7fffca1b40fd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:299  

#24 0x7fffca2cd862 in base::MessagePumpForUI::DoRunLoop D:\chromium\src\base\message\_loop\message\_pump\_win.cc:214  

#25 0x7fffca2cb81b in base::MessagePumpWin::Run D:\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#26 0x7fffca1b7715 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:608  

#27 0x7fffca0c21de in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#28 0x7fff928a4f17 in content::BrowserMainLoop::RunMainMessageLoop D:\chromium\src\content\browser\browser\_main\_loop.cc:1048  

#29 0x7fff928ac291 in content::BrowserMainRunnerImpl::Run D:\chromium\src\content\browser\browser\_main\_runner\_impl.cc:162  

#30 0x7fff6ad46750 in headless::HeadlessContentMainDelegate::RunProcess D:\chromium\src\headless\lib\headless\_content\_main\_delegate.cc:392  

#31 0x7fff94e6e63c in content::RunBrowserProcessMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:705  

#32 0x7fff94e72060 in content::ContentMainRunnerImpl::RunBrowser D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1242  

#33 0x7fff94e71826 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1102  

#34 0x7fff94e6c348 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#35 0x7fff94e6d172 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#36 0x7fff9c7519b0 in headless::`anonymous namespace'::RunContentMain D:\chromium\src\headless\app\headless\_shell.cc:150  

#37 0x7fff9c751533 in headless::HeadlessBrowserMain D:\chromium\src\headless\app\headless\_shell.cc:868  

#38 0x7fff9c7504c5 in headless::HeadlessShellMain D:\chromium\src\headless\app\headless\_shell.cc:807  

#39 0x7fff98271490 in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:160  

#40 0x7ff78b145d3a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#41 0x7ff78b142ae4 in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#42 0x7ff78b407167 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#43 0x7ff8027a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#44 0x7ff8033e26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free D:\chromium\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:2068 in content::RenderProcessHostImpl::CreateNotificationService  

Shadow bytes around the buggy address:  

0x12521fde4e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x12521fde4f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x12521fde4f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x12521fde5000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x12521fde5080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

=>0x12521fde5100:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12521fde5180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12521fde5200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12521fde5280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12521fde5300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x12521fde5380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

MiraclePtr Status: PROTECTED  

This crash occurred inside a callback where a raw\_ptr<T> pointing to the same region was bound to one of the arguments.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==3028==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 25.1 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 162.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 241.0 KB)
- [ch.test.js](attachments/ch.test.js) (text/plain, 5.3 KB)

## Timeline

### m....@gmail.com (2022-10-29)

Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/3876770

Change-Id: I8475b1e243998e599ebb3208a48f1cfa9df30b95

### [Deleted User] (2022-10-29)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-10-29)

#RCA

In this CL https://chromium-review.googlesource.com/c/chromium/src/+/3876770

PopulateBinderMapWithContext passes the rfh raw pointer to BindNotificationService	[1]
BindNotificationService pass it to BindRepeating(CreateNotificationService)	[2]
finally uses it in CreateNotificationService without observe the rfh life cycle	[3]
resulting in UAF

```
void PopulateBinderMapWithContext(
    DedicatedWorkerHost* host,
    mojo::BinderMapWithContext<const url::Origin&>* map) {
  // RenderProcessHost binders taking an origin
  map->Add<payments::mojom::PaymentManager>(BindWorkerReceiverForOrigin(
      &RenderProcessHostImpl::CreatePaymentManagerForOrigin, host));
  map->Add<blink::mojom::PermissionService>(BindWorkerReceiverForOrigin(
      &RenderProcessHostImpl::CreatePermissionService, host));

  RenderFrameHost* rfh =
      RenderFrameHost::FromID(host->GetAncestorRenderFrameHostId());
  CHECK(rfh);
  map->Add<blink::mojom::NotificationService>(BindNotificationService(
      rfh, RenderProcessHost::NotificationServiceCreatorType::kDedicatedWorker,		<<[1]
      host));
}

// Binds the `RenderFrameHost` pointer and the notification service creator type
// to the notification service creator.
template <typename WorkerHost>
base::RepeatingCallback<
    void(const url::Origin&,
         mojo::PendingReceiver<blink::mojom::NotificationService>)>
BindNotificationService(
    RenderFrameHost* rfh,
    RenderProcessHost::NotificationServiceCreatorType creator_type,
    WorkerHost* host) {
  DCHECK_NE(creator_type,
            RenderProcessHost::NotificationServiceCreatorType::kServiceWorker);
  return base::BindRepeating(
      [](WorkerHost* host, RenderFrameHost* rfh,
         RenderProcessHost::NotificationServiceCreatorType creator_type,
         const url::Origin& origin,
         mojo::PendingReceiver<blink::mojom::NotificationService> receiver) {
        auto* process_host =
            static_cast<RenderProcessHostImpl*>(host->GetProcessHost());
        CHECK(process_host);
        process_host->CreateNotificationService(rfh, creator_type, origin,
                                                std::move(receiver));
      },
      base::Unretained(host), rfh, creator_type);									<<[2]
}

void RenderProcessHostImpl::CreateNotificationService(
    RenderFrameHost* rfh,
    const RenderProcessHost::NotificationServiceCreatorType creator_type,
    const url::Origin& origin,
    mojo::PendingReceiver<blink::mojom::NotificationService> receiver) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);
  auto weak_document_ptr = rfh ? rfh->GetWeakDocumentPtr() : WeakDocumentPtr();		<<[3]
  switch (creator_type) {
    case RenderProcessHost::NotificationServiceCreatorType::kServiceWorker:
    case RenderProcessHost::NotificationServiceCreatorType::kSharedWorker:
    case RenderProcessHost::NotificationServiceCreatorType::kDedicatedWorker: {
      storage_partition_impl_->GetPlatformNotificationContext()->CreateService(
          this, origin, /*document_url=*/GURL(), weak_document_ptr,
          creator_type, std::move(receiver));
      break;
    }
    case RenderProcessHost::NotificationServiceCreatorType::kDocument: {
      CHECK(rfh);

      storage_partition_impl_->GetPlatformNotificationContext()->CreateService(
          this, origin, rfh->GetLastCommittedURL(), weak_document_ptr,
          creator_type, std::move(receiver));
      break;
    }
  }
}
```

### m....@gmail.com (2022-10-30)

REPRODUCTION CASE
install node
install puppeteer-core
unzip poc.zip;python -m http.server 1337; 
node ch.test.js chrome_bin_path http://localhost:1337/poc.html

NOTE:1337 is hardcode in poc.html,can't change.
ch.test will cycle the test 20 times to ensure that the crash occurs stably



### me...@google.com (2022-11-01)

Thanks for the report.

leimy, could you PTAL? I'm having trouble reproducing the issue because of an import error in the ch.test.js file. Tentatively assigning labels.

[Monorail components: UI>Browser>Navigation>BFCache UI>Notifications]

### me...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### le...@chromium.org (2022-11-01)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-11-01)

re https://crbug.com/chromium/1379579#c05
node -v
v16.15.1

+-- puppeteer-core@18.0.2

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-01)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@google.com (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-11-02)

Please apply appropriate OSs label. 

### am...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6

commit 6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6
Author: Mingyu Lei <leimy@chromium.org>
Date: Thu Nov 03 14:50:08 2022

Use RFH ID instead of pointer during binding to avoid UAF

In https://crrev.com/c/3876770, when creating binder for
`blink::mojom::NotificationService`, the `RenderFrameHost*` is captured
in the `RepeatingCallback` and will be referenced later when the real
mojo call comes in. This introduces a risk of use-after-free if there
are some race condition between the destruction of the `RenderFrameHost`
and the `DedicatedWorkerHost`.

In this CL, we pass the ID during the binding, and retrieve the
`RenderFrameHost` during the real creation to ensure that its state
is valid before getting the `WeakDocumentPtr`. This should prevent the
use-after-free crash.

See the bug link for more information of the crash.

Bug: 1379579
Change-Id: I2c4d71bc5a3e228d4d061f57402c50e3e517bbf6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3995828
Reviewed-by: Alexander Timin <altimin@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Mingyu Lei <leimy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067010}

[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/public/browser/render_process_host.h
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/browser/worker_host/dedicated_worker_host.h
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/public/test/mock_render_process_host.h
[modify] https://crrev.com/6d78af3b303c82ad960f4a45ad48a0bcdf6aa2e6/content/browser/renderer_host/render_process_host_impl.h


### le...@chromium.org (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@chromium.org (2022-11-11)

It appears that some user gesture would be required to trigger this issue, severity == High; adjusting accordingly 

### m....@gmail.com (2022-11-11)

re https://crbug.com/chromium/1379579#c22 Thanks for reward.
But I don't understand why user gesture is required, the.
The issue was discovered by fuzz without any user gesture.

### [Deleted User] (2022-11-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

Not requesting merge to dev (M109) because latest trunk commit (1067010) appears to be prior to dev branch point (1070088). If this is incorrect, please replace the Merge-NA-109 label with Merge-Request-109. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-17)

to correct my https://crbug.com/chromium/1379579#c22, this should not have been reduced to to user gesture, but mildly mitigated by race condition

OP, you are correct not sure gesture but race condition. Apologies for my error as I was working across a number of bugs at once. 
Thanks for reaching out so I could correct this. 

### m....@gmail.com (2022-11-17)

Thank you for your explanation.

It seems that the reward amount of "mildly mitigated by race condition" issue is very random, such as this issue(reward:30k) https://bugs.chromium.org/p/chromium/issues/detail?id=1347707
So I think the race condition issue should not be put into the "Moderately mitigated" rule because there isn't any security mitigation here.


### am...@chromium.org (2022-11-17)

The looping to achieve execution was not in the renderer; this issue is not demonstrated as easy to achieve reliable triggering and beating the race. The POC provided and used to achieve this result was also quite large and not at all minimized. Due to these conditions, we feel that the reward is appropriate for this report. 

### m....@gmail.com (2022-11-18)

Sounds reasonable, thanks again for the explanation.

### [Deleted User] (2023-02-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

Hi, can someone restore the files that were deleted in https://crbug.com/chromium/1379579#c4? I can't reproduce this issue without them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1379579?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation>BFCache, UI>Notifications]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061519)*
