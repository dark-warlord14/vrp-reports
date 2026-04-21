# Security: Browser process heap-use-after-free in the portal element

| Field | Value |
|-------|-------|
| **Issue ID** | [40054168](https://issues.chromium.org/issues/40054168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | lf...@chromium.org |
| **Created** | 2020-12-14 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in the content::RenderWidgetHostImpl::RejectMouseLockOrUnlockIfNecessary in the browser process(escape the sandbox)

The portal element + url jump in the pdf plugin + requestPointerLock will cause the UAF.

**VERSION**  

Chrome Version: The latest chromium, asan-win32-release\_x64-836542  

Operating System: Windows 10

**REPRODUCTION CASE**

chrome://flags/#enable-portals

C:\chromium\_version\asan-win32-release\_x64-836542>chrome.exe --enable-features=Portals,PortalsCrossOrigin --user-data-dir=c:/tmp/ppp <http://127.0.0.1/poc/portal.html>

1. open the portal.html >> acitvate and open the url.pdf
2. click anywhere in the pdf document >> jump to the pointerlock.html
3. click "ClickMe" button in the pointerlock.html
4. close the tab or click the back navigation in the upper right corner will both triger the UAF stably.

See the gif

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

# C:\chromium\_version\asan-win32-release\_x64-836542>chrome.exe --enable-features=Portals,PortalsCrossOrigin --user-data-dir=c:/tmp/pp [15320:20080:1214/160741.200:ERROR:device\_event\_log\_impl.cc(214)] [16:07:41.200] USB: usb\_device\_handle\_win.cc:1049 [15320:20080:1214/160741.252:ERROR:device\_event\_log\_impl.cc(214)] [16:07:41.251] USB: usb\_device\_handle\_win.cc:1049 [15320:20080:1214/160741.383:ERROR:device\_event\_log\_impl.cc(214)] [16:07:41.383] Bluetooth: bluetooth\_adapter\_winrt.cc:1072 Getting Default Adapter failed.

==15320==ERROR: AddressSanitizer: heap-use-after-free on address 0x1233097b40c9 at pc 0x7ffbf1e7175f bp 0x00f8559fe400 sp 0x00f8559fe448  

READ of size 1 at 0x1233097b40c9 thread T0  

#0 0x7ffbf1e7175e in content::RenderWidgetHostImpl::RejectMouseLockOrUnlockIfNecessary(enum blink::mojom::PointerLockResult) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2118:7  

#1 0x7ffbf22259f8 in content::WebContentsImpl::~WebContentsImpl(void) C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:899:25  

#2 0x7ffbf22cb9c3 in content::WebContentsImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.h:869 #3 0x7ffbf1ac548f in content::Portal::WebContentsHolder::~WebContentsHolder C:\b\s\w\ir\cache\builder\src\content\browser\portal\portal.cc:650 #4 0x7ffbf1ac548f in content::Portal::~Portal(void) C:\b\s\w\ir\cache\builder\src\content\browser\portal\portal.cc:60:1 #5 0x7ffbf1acbe3f in content::Portal::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\portal\portal.h:56  

#6 0x7ffbf1d3443b in std::default\_delete C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2378  

#7 0x7ffbf1d3443b in std::unique\_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2499  

#8 0x7ffbf1d3443b in std::unique\_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2495  

#9 0x7ffbf1d3443b in content::RenderFrameHostImpl::DestroyPortal(class content::Portal \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:1487:1  

#10 0x7ffbf22a92e5 in content::WebContentsImpl::Close(class content::RenderViewHost \*) C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:6999:16  

#11 0x7ffbeff9744f in base::OnceCallback C:\b\s\w\ir\cache\builder\src\base\callback.h:84  

#12 0x7ffbeff9744f in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\frame\frame.mojom.cc:14289:26  

#13 0x7ffbf77ddb23 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:549:23  

#14 0x7ffbf9edd042 in mojo::MessageDispatcher::Accept(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:41:19  

#15 0x7ffbfa6d2cc5 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnProxyThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:945:24  

#16 0x7ffbfa6ccdb9 in base::internal::FunctorTraits C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:498  

#17 0x7ffbfa6ccdb9 in base::internal::InvokeHelper C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:637  

#18 0x7ffbfa6ccdb9 in base::internal::Invoker C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:710  

#19 0x7ffbfa6ccdb9 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#20 0x7ffbf73a825f in base::OnceCallback C:\b\s\w\ir\cache\builder\src\base\callback.h:102  

#21 0x7ffbf73a825f in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:163:33  

#22 0x7ffbf9a7c8ae in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#23 0x7ffbf9a7be79 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#24 0x7ffbf7457950 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:224:63  

#25 0x7ffbf745542a in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:80:3  

#26 0x7ffbf9a7edaf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#27 0x7ffbf735c2b5 in base::RunLoop::Run(void) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:131:14  

#28 0x7ffbf9ba5ebd in ChromeBrowserMainParts::MainMessageLoopRun(int \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1733:15  

#29 0x7ffbf12eeaab in content::BrowserMainLoop::RunMainMessageLoopParts(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1013:29  

#30 0x7ffbf12f47ef in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:150:15  

#31 0x7ffbf12e724e in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47:28  

#32 0x7ffbf7117b8d in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:535:10  

#33 0x7ffbf711a3b3 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1031:10  

#34 0x7ffbf711975b in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:900:12  

#35 0x7ffbf7116a4f in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372:36  

#36 0x7ffbf7117023 in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398:10  

#37 0x7ffbedae145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:130:12  

#38 0x7ff62b395b9f in MainDllLoader::Launch(struct HINSTANCE\_\_\*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169:12  

#39 0x7ff62b3929b7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:345:20  

#40 0x7ff62b76771f in invoke\_main d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#41 0x7ff62b76771f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#42 0x7ffca40f7033 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#43 0x7ffca593d0d0 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004d0d0)

0x1233097b40c9 is located 585 bytes inside of 1960-byte region [0x1233097b3e80,0x1233097b4628)  

freed by thread T0 here:  

#0 0x7ff62b4344db in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffbf1e90803 in content::RenderWidgetHostImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_impl.h:429 #2 0x7ffbf1e5ec4f in std::default_delete C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2378 #3 0x7ffbf1e5ec4f in std::unique_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2722 #4 0x7ffbf1e5ec4f in std::unique_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2718 #5 0x7ffbf1e5ec4f in content::RenderViewHostImpl::~RenderViewHostImpl(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_view_host_impl.cc:381:1 #6 0x7ffbf1e655a5 in content::RenderViewHostImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_view\_host\_impl.h:341  

#7 0x7ffbf1d2e093 in scoped\_refptr C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:208  

#8 0x7ffbf1d2e093 in scoped\_refptr C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:214  

#9 0x7ffbf1d2e093 in scoped\_refptr C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:207  

#10 0x7ffbf1d2e093 in content::RenderFrameHostImpl::~RenderFrameHostImpl(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:1281:21  

#11 0x7ffbf1d9dd25 in content::RenderFrameHostImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.h:1149 #12 0x7ffbf1dcaa2d in std::default_delete C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2378 #13 0x7ffbf1dcaa2d in std::unique_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2499 #14 0x7ffbf1dcaa2d in std::unique_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2495 #15 0x7ffbf1dcaa2d in content::RenderFrameHostManager::~RenderFrameHostManager(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:216:3 #16 0x7ffbf1b560ec in content::FrameTreeNode::~FrameTreeNode(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:224:1 #17 0x7ffbf1b50806 in content::FrameTree::~FrameTree(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree.cc:123:3 #18 0x7ffbf22271fa in content::WebContentsImpl::~WebContentsImpl(void) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:991:1 #19 0x7ffbf22cb9c3 in content::WebContentsImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:869  

#20 0x7ffbf2223a02 in std::default\_delete C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2378  

#21 0x7ffbf2223a02 in std::unique\_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2499  

#22 0x7ffbf2223a02 in std::unique\_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2495  

#23 0x7ffbf2223a02 in content::WebContentsImpl::WebContentsTreeNode::OnFrameTreeNodeDestroyed(class content::FrameTreeNode \*) C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:748:3  

#24 0x7ffbf1b55bae in content::FrameTreeNode::~FrameTreeNode(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:178:14  

#25 0x7ffbf1d4a40a in std::default\_delete C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2378  

#26 0x7ffbf1d4a40a in std::unique\_ptr C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2499  

#27 0x7ffbf1d4a40a in content::RenderFrameHostImpl::RemoveChild(class content::FrameTreeNode \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:2953:22  

#28 0x7ffbf1d4b27d in content::RenderFrameHostImpl::PendingDeletionCheckCompletedOnSubtree(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:6114:5  

#29 0x7ffbf1d4b22e in content::RenderFrameHostImpl::PendingDeletionCheckCompletedOnSubtree(void) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:6125:16  

#30 0x7ffbf1d51de6 in content::RenderFrameHostImpl::Unload(class content::RenderFrameProxyHost \*, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3329:3  

#31 0x7ffbf1dd11d1 in content::RenderFrameHostManager::UnloadOldFrame(class std::\_\_1::unique\_ptr<class content::RenderFrameHostImpl, struct std::\_\_1::default\_delete<class content::RenderFrameHostImpl>>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:603:23  

#32 0x7ffbf1dce774 in content::RenderFrameHostManager::CommitPending(class std::\_\_1::unique\_ptr<class content::RenderFrameHostImpl, struct std::\_\_1::default\_delete<class content::RenderFrameHostImpl>>, class std::\_\_1::unique\_ptr<struct content::BackForwardCacheImpl::Entry, struct std::\_\_1::default\_delete<struct content::BackForwardCacheImpl::Entry>>, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:3148:3  

#33 0x7ffbf1dcd35b in content::RenderFrameHostManager::CommitPendingIfNecessary(class content::RenderFrameHostImpl \*, bool, bool, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:380:5  

#34 0x7ffbf1dcd032 in content::RenderFrameHostManager::DidNavigateFrame(class content::RenderFrameHostImpl \*, bool, bool, bool, struct blink::FramePolicy const &) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:349:3  

#35 0x7ffbf1d13bc8 in content::Navigator::DidNavigate(class content::RenderFrameHostImpl \*, class content::mojom::DidCommitProvisionalLoadParams const &, class std::\_\_1::unique\_ptr<class content::NavigationRequest, struct std::\_\_1::default\_delete<class content::NavigationRequest>>, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:303:38  

#36 0x7ffbf1d4f39c in content::RenderFrameHostImpl::DidCommitNavigationInternal(class std::\_\_1::unique\_ptr<class content::NavigationRequest, struct std::\_\_1::default\_delete<class content::NavigationRequest>>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::InlinedStructPtr<class content::mojom::DidCommitSameDocumentNavigationParams>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:8802:34  

#37 0x7ffbf1d4d38c in content::RenderFrameHostImpl::DidCommitNavigation(class std::\_\_1::unique\_ptr<class content::NavigationRequest, struct std::\_\_1::default\_delete<class content::NavigationRequest>>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:9247:8  

#38 0x7ffbf1d4fef3 in content::RenderFrameHostImpl::DidCommitPerNavigationMojoInterfaceNavigation(class content::NavigationRequest \*, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3177:3  

#39 0x7ffbf1dc928c in base::internal::FunctorTraits C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:395  

#40 0x7ffbf1dc928c in base::internal::InvokeHelper C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:637  

#41 0x7ffbf1dc928c in base::internal::Invoker C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:710  

#42 0x7ffbf1dc928c in base::internal::Invoker<struct base::internal::BindState<void (\_\_cdecl content::RenderFrameHostImpl::\*)(class content::NavigationRequest \*, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>), class base::internal::UnretainedWrapper<class content::RenderFrameHostImpl>, class content::NavigationRequest \*>, (class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce(class base::internal::BindStateBase \*, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams> &&, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams> &&) C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#43 0x7ffbf058ec07 in base::OnceCallback<(class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::Run(class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadParams>, class mojo::StructPtr<class content::mojom::DidCommitProvisionalLoadInterfaceParams>) && C:\b\s\w\ir\cache\builder\src\base\callback.h:101:12  

#44 0x7ffbf058e911 in content::mojom::NavigationClient\_CommitNavigation\_ForwardToCallback::Accept(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\navigation\_client.mojom.cc:652:26  

#45 0x7ffbf77ddb23 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:549:23

previously allocated by thread T0 here:  

#0 0x7ff62b4345db in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc08ce581a in operator new(unsigned \_\_int64) d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffbf1e689cb in content::RenderWidgetHostImpl::Create(class content::RenderWidgetHostDelegate \*, class content::AgentSchedulingGroupHost &, int, bool, class std::\_\_1::unique\_ptr<class content::FrameTokenMessageQueue, struct std::\_\_1::default\_delete<class content::FrameTokenMessageQueue>>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:337:27  

#3 0x7ffbf1e68882 in content::RenderWidgetHostFactory::Create(class content::RenderWidgetHostDelegate \*, class content::AgentSchedulingGroupHost &, int, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_factory.cc:25:10  

#4 0x7ffbf1e5c35b in content::RenderViewHostFactory::Create(class content::SiteInstance \*, class content::RenderViewHostDelegate \*, class content::RenderWidgetHostDelegate \*, int, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_view\_host\_factory.cc:41:7  

#5 0x7ffbf1b52d03 in content::FrameTree::CreateRenderViewHost(class content::SiteInstance \*, int, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree.cc:400:40  

#6 0x7ffbf1ddf4ec in content::RenderFrameHostManager::CreateRenderFrameProxy(class content::SiteInstance \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:2581:58  

#7 0x7ffbf1b51d2f in content::FrameTree::CreateProxiesForSiteInstance(class content::FrameTreeNode \*, class content::SiteInstance \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree.cc:335:31  

#8 0x7ffbf1ddece3 in content::RenderFrameHostManager::CreateOpenerProxiesForFrameTree C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:3370  

#9 0x7ffbf1ddece3 in content::RenderFrameHostManager::CreateOpenerProxies(class content::SiteInstance \*, class content::FrameTreeNode \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:3329:37  

#10 0x7ffbf1dde859 in content::RenderFrameHostManager::CreateProxiesForNewRenderFrameHost(class content::SiteInstance \*, class content::SiteInstance \*, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:2313:5  

#11 0x7ffbf1dd74a9 in content::RenderFrameHostManager::CreateSpeculativeRenderFrameHost(class content::SiteInstance \*, class content::SiteInstance \*, bool) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:2454:3  

#12 0x7ffbf1dd3b54 in content::RenderFrameHostManager::GetFrameHostForNavigation(class content::NavigationRequest \*, class std::\_\_1::basic\_string<char, struct std::\_\_1::char\_traits<char>, class std::\_\_1::allocator<char>> \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:919:22  

#13 0x7ffbf1dd31c8 in content::RenderFrameHostManager::DidCreateNavigationRequest(class content::NavigationRequest \*) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:732:37  

#14 0x7ffbf1b59175 in content::FrameTreeNode::CreatedNavigationRequest(class std::\_\_1::unique\_ptr<class content::NavigationRequest, struct std::\_\_1::default\_delete<class content::NavigationRequest>>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:517:21  

#15 0x7ffbf1d1791c in content::Navigator::OnBeginNavigation(class content::FrameTreeNode \*, class mojo::StructPtr<class content::mojom::CommonNavigationParams>, class mojo::StructPtr<class content::mojom::BeginNavigationParams>, class scoped\_refptr<class network::SharedURLLoaderFactory>, class mojo::PendingAssociatedRemote<class content::mojom::NavigationClient>, class mojo::PendingRemote<class blink::mojom::NavigationInitiator>, class scoped\_refptr<class content::PrefetchedSignedExchangeCache>, class std::\_\_1::unique\_ptr<class content::WebBundleHandleTracker, struct std::\_\_1::default\_delete<class content::WebBundleHandleTracker>>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:738:20  

#16 0x7ffbf1d694eb in content::RenderFrameHostImpl::BeginNavigation(class mojo::StructPtr<class content::mojom::CommonNavigationParams>, class mojo::StructPtr<class content::mojom::BeginNavigationParams>, class mojo::PendingRemote<class blink::mojom::BlobURLToken>, class mojo::PendingAssociatedRemote<class content::mojom::NavigationClient>, class mojo::PendingRemote<class blink::mojom::NavigationInitiator>) C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:5620:34  

#17 0x7ffbf05434cc in content::mojom::FrameHostStubDispatch::Accept(class content::mojom::FrameHost \*, class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:5925:13  

#18 0x7ffbf77ddc8e in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:554:54  

#19 0x7ffbf9edcf4d in mojo::MessageDispatcher::Accept(class mojo::Message \*) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:46:24  

#20 0x7ffbfa6d2cc5 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnProxyThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:945:24  

#21 0x7ffbfa6ccdb9 in base::internal::FunctorTraits C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:498  

#22 0x7ffbfa6ccdb9 in base::internal::InvokeHelper C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:637  

#23 0x7ffbfa6ccdb9 in base::internal::Invoker C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:710  

#24 0x7ffbfa6ccdb9 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#25 0x7ffbf73a825f in base::OnceCallback C:\b\s\w\ir\cache\builder\src\base\callback.h:102  

#26 0x7ffbf73a825f in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:163:33  

#27 0x7ffbf9a7c8ae in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#28 0x7ffbf9a7be79 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#29 0x7ffbf7457950 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:224:63  

#30 0x7ffbf745542a in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:80:3  

#31 0x7ffbf9a7edaf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#32 0x7ffbf735c2b5 in base::RunLoop::Run(void) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:131:14  

#33 0x7ffbf9ba5ebd in ChromeBrowserMainParts::MainMessageLoopRun(int \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1733:15

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:2118:7 in content::RenderWidgetHostImpl::RejectMouseLockOrUnlockIfNecessary(enum blink::mojom::PointerLockResult)  

Shadow bytes around the buggy address:  

0x043f6a5f67c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x043f6a5f67d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f67e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f67f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f6800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x043f6a5f6810: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd  

0x043f6a5f6820: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f6830: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f6840: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f6850: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x043f6a5f6860: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc  

==15320==ABORTING

C:\chromium\_version\asan-win32-release\_x64-836542>

## Attachments

- [navigator.gif](attachments/navigator.gif) (image/gif, 4.2 MB)
- [close.gif](attachments/close.gif) (image/gif, 2.1 MB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 1013 B)
- [pointerlock.html](attachments/pointerlock.html) (text/plain, 411 B)
- [portal.html](attachments/portal.html) (text/plain, 64 B)
- [url.pdf](attachments/url.pdf) (application/pdf, 692 B)

## Timeline

### [Deleted User] (2020-12-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-14)

See also 1158381.

Portals folks, can you take a look at this issue. Despite needing a feature being enabled, I believe this is behind origin trial so exposed on the web (Triage: Severity High).

[Monorail components: Blink>Portals]

### [Deleted User] (2020-12-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-17)

lfg@ says " the portals origin trial has already ended, so this bug should not affect any shipping configuration." - adjusting labels appropriately.

### lf...@chromium.org (2020-12-17)

To update this -- the portals origin trial ended in M86. The only way to test portals right now is through a command-line flag.


### lf...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2021-01-16)

The https://crbug.com/chromium/1158381 don't allow MimeHandlerViews to navigate away from their handling extension.
Maybe the https://crbug.com/chromium/1158381 submitted code also fixed this issue.
This issue also exploits the pdf navigate to cause the UAF in the browser process.
Will these two issues count as the same vulnerability?

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/17040c563e8c5d2e433ebb0e29b3b1eb3854b002

commit 17040c563e8c5d2e433ebb0e29b3b1eb3854b002
Author: Lucas Gadani <lfg@chromium.org>
Date: Mon Jan 25 22:42:09 2021

Provide a default implementation that auto-rejects requests for pointer and keyboard locks.

Bug: 1158376
Change-Id: Iff036459443ff61cf985c34a29e20d1b2f800825
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2638107
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#846926}

[modify] https://crrev.com/17040c563e8c5d2e433ebb0e29b3b1eb3854b002/content/public/browser/web_contents_delegate.cc
[modify] https://crrev.com/17040c563e8c5d2e433ebb0e29b3b1eb3854b002/content/public/browser/web_contents_delegate.h
[modify] https://crrev.com/17040c563e8c5d2e433ebb0e29b3b1eb3854b002/extensions/browser/guest_view/mime_handler_view/mime_handler_view_browsertest.cc


### lf...@chromium.org (2021-01-25)

Just to also update this bug (I've mentioned in https://crbug.com/chromium/1158381): Kevin's CL already fixed the issue, but the CL I just landed should prevent a UaF from pointer lock in case there's another bug that allows loading content inside a MimeHandlerView.


### lf...@chromium.org (2021-01-25)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1c22ada7d65f4546078fb648765702d39ee13198

commit 1c22ada7d65f4546078fb648765702d39ee13198
Author: Findit <findit-for-me@appspot.gserviceaccount.com>
Date: Tue Jan 26 02:24:30 2021

Revert "Provide a default implementation that auto-rejects requests for pointer and keyboard locks."

This reverts commit 17040c563e8c5d2e433ebb0e29b3b1eb3854b002.

Reason for revert:

Findit (https://goo.gl/kROfz5) identified CL at revision 846926 as the
culprit for flakes in the build cycles as shown on:
https://analysis.chromium.org/p/chromium/flake-portal/analysis/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyQwsSDEZsYWtlQ3VscHJpdCIxY2hyb21pdW0vMTcwNDBjNTYzZThjNWQyZTQzM2ViYjBlMjliM2IxZWIzODU0YjAwMgw

Sample Failed Build: https://ci.chromium.org/b/8857085597648469200

Sample Failed Step: bf_cache_browser_tests

Sample Flaky Test: MimeHandlerViewTest.RejectPointLock

Original change's description:
> Provide a default implementation that auto-rejects requests for pointer and keyboard locks.
> 
> Bug: 1158376
> Change-Id: Iff036459443ff61cf985c34a29e20d1b2f800825
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2638107
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Lucas Gadani <lfg@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#846926}


Change-Id: I294daaa7d2105706c23ba41520c77cdb77b64b4d
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 1158376
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2649386
Cr-Commit-Position: refs/heads/master@{#847009}

[modify] https://crrev.com/1c22ada7d65f4546078fb648765702d39ee13198/content/public/browser/web_contents_delegate.cc
[modify] https://crrev.com/1c22ada7d65f4546078fb648765702d39ee13198/content/public/browser/web_contents_delegate.h
[modify] https://crrev.com/1c22ada7d65f4546078fb648765702d39ee13198/extensions/browser/guest_view/mime_handler_view/mime_handler_view_browsertest.cc


### lf...@chromium.org (2021-01-26)

Reopening since there was a revert.

### lf...@chromium.org (2021-01-26)

The flaky test seems to be happening because WaitForLoadStop is failing (from https://ci.chromium.org/ui/p/chromium/builders/ci/linux-bfcache-rel/13747/overview):

../../extensions/browser/guest_view/mime_handler_view/mime_handler_view_browsertest.cc:584: Failure
Value of: WaitForLoadStop(guest_contents)
  Actual: false
Expected: true


### lf...@chromium.org (2021-01-26)

My guess is that we can get to that point before the guest has started to navigate.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a933b8702b9d94cf5c028b61f31498229d335ac7

commit a933b8702b9d94cf5c028b61f31498229d335ac7
Author: Lucas Gadani <lfg@chromium.org>
Date: Tue Jan 26 20:10:27 2021

Reland "Provide a default implementation that auto-rejects requests for pointer and keyboard locks."

This is a reland of 17040c563e8c5d2e433ebb0e29b3b1eb3854b002

Original change's description:
> Provide a default implementation that auto-rejects requests for pointer and keyboard locks.
>
> Bug: 1158376
> Change-Id: Iff036459443ff61cf985c34a29e20d1b2f800825
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2638107
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Lucas Gadani <lfg@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#846926}

Bug: 1158376
Change-Id: I611c6a2891578e872122c5b35e2162aea1663115
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2649276
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#847286}

[modify] https://crrev.com/a933b8702b9d94cf5c028b61f31498229d335ac7/content/public/browser/web_contents_delegate.cc
[modify] https://crrev.com/a933b8702b9d94cf5c028b61f31498229d335ac7/content/public/browser/web_contents_delegate.h
[modify] https://crrev.com/a933b8702b9d94cf5c028b61f31498229d335ac7/extensions/browser/guest_view/mime_handler_view/mime_handler_view_browsertest.cc


### lf...@chromium.org (2021-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Congratulations! The VRP Panel has decided to reward you $15,000 for this report. Nice work. 

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1158376?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054168)*
