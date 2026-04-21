# Security: UAF in NavigationPredictor

| Field | Value |
|-------|-------|
| **Issue ID** | [40055517](https://issues.chromium.org/issues/40055517) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader, Internals>Network>DataProxy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-04-11 |
| **Bounty** | $27,000.00 |

## Description

**VULNERABILITY DETAILS**  

NavigationPredictor holds a raw pointer to `BrowserContext \*browser_context_` [1]. NavigationPredictor can continue receiving Mojo calls after BrowserContext is freed, resulting in a use after free on a virtual function pointer [2].

Note: This feature is "disabled" on desktop but is still reachable because it is only protected by a DCHECK on the browser process side [3]. On android this vulnerability is reachable through blink [4] (without mojoJS bindings).

[1] -<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/navigation_predictor/navigation_predictor.cc;l=116;drc=9b4c3eeaeed2c0cf9b3911c69417cdbde5105778>  

[2] -<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/navigation_predictor/navigation_predictor.cc;l=509;drc=9b4c3eeaeed2c0cf9b3911c69417cdbde5105778>  

[3] - <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/navigation_predictor/navigation_predictor.cc;l=507;drc=7a353f20acd7f7973d3e5113247afe7109f3f58e>  

[4] - <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/common/features.cc;l=122;drc=7a353f20acd7f7973d3e5113247afe7109f3f58e>

**VERSION**  

89.0.4389.114 [Stable]

**REPRODUCTION CASE**  

No user interaction (extension) - cooler

1. Install the attached extension (ext) and allow in incognito <https://stackoverflow.com/questions/60842000/how-to-get-windowid-from-chrome-incognito-window-with-chrome-api>
2. Host child.html with a web server
3. python copy\_mojo\_bindings.py /path/to/chrome/src/out/x64.asan mojo
4. run ./out/x64.asan/chrome --enable-blink-features=MojoJS --ignore-certificate-errors --load-extension=/path/to/ext

Note: Allow incognito is just needed because I'm using the chrome.windows api to simulate closing a browser window.

User interaction (exit browser)

1. Host child.html with a web server
2. Open incognito browser (can be another chrome instance, guest view, etc - we just need two BrowserContext instances)
3. Navigate to to <https://localhost:8080/child.html>
4. Close the browser

=================================================================  

==16466==ERROR: AddressSanitizer: heap-use-after-free on address 0x6120032bc240 at pc 0x55ece85af113 bp 0x7ffc7ef62950 sp 0x7ffc7ef62948  

READ of size 8 at 0x6120032bc240 thread T0 (chrome)  

#0 0x55ece85af112 in NavigationPredictor::ReportAnchorElementMetricsOnClick(mojo::StructPtr[blink::mojom::AnchorElementMetrics](javascript:void(0);)) ./../../chrome/browser/navigation\_predictor/navigation\_predictor.cc:509:25  

#1 0x55ecdf49c129 in blink::mojom::AnchorElementMetricsHostStubDispatch::Accept(blink::mojom::AnchorElementMetricsHost\*, mojo::Message\*) ./gen/third\_party/blink/public/mojom/loader/navigation\_predictor.mojom.cc:277:13  

#2 0x55ece9381ed4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:554:54  

#3 0x55ece938f466 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:41:19  

#4 0x55ece939b05e in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:955:42  

#5 0x55ece939978a in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:622:38  

#6 0x55ece938f466 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:41:19  

#7 0x55ece937aad5 in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:508:49  

#8 0x55ece937cf33 in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:566:14  

#9 0x55ece937dd64 in void base::internal::FunctorTraits<void (mojo::Connector::\*)(), void>::Invoke<void (mojo::Connector::\*)(), base::WeakPtr[mojo::Connector](javascript:void(0);) >(void (mojo::Connector::\*)(), base::WeakPtr[mojo::Connector](javascript:void(0);)&&) ./../../base/bind\_internal.h:498:12  

#10 0x55ece937dd64 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (mojo::Connector::\*)(), base::WeakPtr[mojo::Connector](javascript:void(0);) >(void (mojo::Connector::\*&&)(), base::WeakPtr[mojo::Connector](javascript:void(0);)&&) ./../../base/bind\_internal.h:657:5  

#11 0x55ece937dd64 in void base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(), base::WeakPtr[mojo::Connector](javascript:void(0);) >, void ()>::RunImpl<void (mojo::Connector::\*)(), std::\_\_1::tuple<base::WeakPtr[mojo::Connector](javascript:void(0);) >, 0ul>(void (mojo::Connector::\*&&)(), std::\_\_1::tuple<base::WeakPtr[mojo::Connector](javascript:void(0);) >&&, std::\_\_1::integer\_sequence<unsigned long, 0ul>) ./../../base/bind\_internal.h:710:12  

#12 0x55ece937dd64 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(), base::WeakPtr[mojo::Connector](javascript:void(0);) >, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:679:12  

#13 0x55ece78fd967 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:101:12  

#14 0x55ece78fd967 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:163:33  

#15 0x55ece793b7f0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#16 0x55ece793af24 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#17 0x55ece77fd7b0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:404:48  

#18 0x55ece793d806 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#19 0x55ece78848d0 in base::RunLoop::Run() ./../../base/run\_loop.cc:131:14  

#20 0x55ece83b0da0 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) ./../../chrome/browser/chrome\_browser\_main.cc:1736:15  

#21 0x55ece0a49e98 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser\_main\_loop.cc:974:29  

#22 0x55ece0a4fa85 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:150:15  

#23 0x55ece0a42005 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser\_main.cc:47:28  

#24 0x55ece7600eed in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:557:10  

#25 0x55ece7600eed in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content\_main\_runner\_impl.cc:1068:10  

#26 0x55ece7600182 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:935:12  

#27 0x55ece75f9fce in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:372:36  

#28 0x55ece75fa5cc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:398:10  

#29 0x55ecdc94bd97 in ChromeMain ./../../chrome/app/chrome\_main.cc:141:12  

#30 0x7f9c31fcbbf6 in \_\_libc\_start\_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310:0

0x6120032bc240 is located 0 bytes inside of 288-byte region [0x6120032bc240,0x6120032bc360)  

freed by thread T0 (chrome) here:  

#0 0x55ecdc949add in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160:3  

#1 0x55ece89612f8 in std::\_\_1::default\_delete<Profile>::operator()(Profile\*) const ./../../buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#2 0x55ece89612f8 in std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> >::reset(Profile\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#3 0x55ece89612f8 in std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> >::~unique\_ptr() ./../../buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#4 0x55ece89612f8 in std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >::~pair() ./../../buildtools/third\_party/libc++/trunk/include/utility:297:29  

#5 0x55ece89612f8 in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*> > >::\_\_destroy<std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > >(std::\_\_1::integral\_constant<bool, false>, std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*> >&, std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:1787:23  

#6 0x55ece89612f8 in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*> > >::destroy<std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > >(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*> >&, std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:1619:14  

#7 0x55ece89612f8 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::\_\_map\_value\_compare<Profile::OTRProfileID, std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::less[Profile::OTRProfileID](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > > >::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, void\*>\*, long>) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2519:5  

#8 0x55ece89596e9 in unsigned long std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::\_\_map\_value\_compare<Profile::OTRProfileID, std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > >, std::\_\_1::less[Profile::OTRProfileID](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > > >::\_\_erase\_unique[Profile::OTRProfileID](javascript:void(0);)(Profile::OTRProfileID const&) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2542:5  

#9 0x55ece89596e9 in std::\_\_1::map<Profile::OTRProfileID, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> >, std::\_\_1::less[Profile::OTRProfileID](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<Profile::OTRProfileID const, std::\_\_1::unique\_ptr<Profile, std::\_\_1::default\_delete<Profile> > > > >::erase(Profile::OTRProfileID const&) ./../../buildtools/third\_party/libc++/trunk/include/map:1304:25  

#10 0x55ece89596e9 in ProfileImpl::DestroyOffTheRecordProfile(Profile\*) ./../../chrome/browser/profiles/profile\_impl.cc:989:17  

#11 0x55ece89662d4 in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile\*) ./../../chrome/browser/profiles/profile\_destroyer.cc:85:34  

#12 0x55ece8964850 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile\*) ./../../chrome/browser/profiles/profile\_destroyer.cc:62:5  

#13 0x55ecf1f8f258 in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:627:7  

#14 0x55ecf1f906ad in Browser::~Browser() ./../../chrome/browser/ui/browser.cc:548:21  

#15 0x55ecf26d46cb in std::\_\_1::default\_delete<Browser>::operator()(Browser\*) const ./../../buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#16 0x55ecf26d46cb in std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >::reset(Browser\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#17 0x55ecf26d46cb in std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >::~unique\_ptr() ./../../buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#18 0x55ecf26d46cb in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:670:1  

#19 0x55ecf26d4fd7 in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:635:29  

#20 0x55ecf26d4fd7 in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:0:0  

#21 0x55ecf19ab109 in views::View::~View() ./../../ui/views/view.cc:237:9  

#22 0x55ecf1a74019 in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:164:1  

#23 0x55ecf1a74019 in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:160:33  

#24 0x55ecf19ae733 in std::\_\_1::default\_delete[views::View](javascript:void(0);)::operator()(views::View\*) const ./../../buildtools/third\_party/libc++/trunk/include/memory:2378:5  

#25 0x55ecf19ae733 in std::\_\_1::unique\_ptr<views::View, std::\_\_1::default\_delete[views::View](javascript:void(0);) >::reset(views::View\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:2633:7  

#26 0x55ecf19ae733 in std::\_\_1::unique\_ptr<views::View, std::\_\_1::default\_delete[views::View](javascript:void(0);) >::~unique\_ptr() ./../../buildtools/third\_party/libc++/trunk/include/memory:2587:19  

#27 0x55ecf19ae733 in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) ./../../ui/views/view.cc:2563:1  

#28 0x55ecf19aea65 in views::View::RemoveAllChildViews(bool) ./../../ui/views/view.cc:304:5  

#29 0x55ecf1a1db6e in views::Widget::DestroyRootView() ./../../ui/views/widget/widget.cc:1538:15  

#30 0x55ecf1a1db6e in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:178:3  

#31 0x55ecf271587d in BrowserFrame::~BrowserFrame() ./../../chrome/browser/ui/views/frame/browser\_frame.cc:79:31  

#32 0x55ecf1adabef in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:0:0  

#33 0x55ecf281db76 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() ./../../chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:29:64  

#34 0x55ecf281db76 in DesktopBrowserFrameAuraLinux::~DesktopBrowserFrameAuraLinux() ./../../chrome/browser/ui/views/frame/desktop\_browser\_frame\_aura\_linux.cc:29:63  

#35 0x55ecf1b1af31 in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:696:32  

#36 0x55ecf1ac6fe8 in views::DesktopWindowTreeHostLinux::OnClosed() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:248:34  

#37 0x55ecf1b113a6 in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:287:22  

#38 0x55ecf1b1cf84 in void base::internal::FunctorTraits<void (views::DesktopWindowTreeHostPlatform::\*)(), void>::Invoke<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >(void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);)&&) ./../../base/bind\_internal.h:498:12  

#39 0x55ecf1b1cf84 in void base::internal::InvokeHelper<true, void>::MakeItSo<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >(void (views::DesktopWindowTreeHostPlatform::\*&&)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);)&&) ./../../base/bind\_internal.h:657:5  

#40 0x55ecf1b1cf84 in void base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, void ()>::RunImpl<void (views::DesktopWindowTreeHostPlatform::\*)(), std::\_\_1::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, 0ul>(void (views::DesktopWindowTreeHostPlatform::\*&&)(), std::\_\_1::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >&&, std::\_\_1::integer\_sequence<unsigned long, 0ul>) ./../../base/bind\_internal.h:710:12  

#41 0x55ecf1b1cf84 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:679:12  

#42 0x55ece78fd967 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:101:12  

#43 0x55ece78fd967 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:163:33  

#44 0x55ece793b7f0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#45 0x55ece793af24 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#46 0x55ece77fd7b0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:404:48  

#47 0x55ece793d806 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#48 0x55ece78848d0 in base::RunLoop::Run() ./../../base/run\_loop.cc:131:14  

#49 0x55ece83b0da0 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) ./../../chrome/browser/chrome\_browser\_main.cc:1736:15  

#50 0x55ece0a49e98 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser\_main\_loop.cc:974:29  

#51 0x55ece0a4fa85 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:150:15

previously allocated by thread T0 (chrome) here:  

#0 0x55ecdc94927d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x55ece898a0cd in Profile::CreateOffTheRecordProfile(Profile\*, Profile::OTRProfileID const&) ./../../chrome/browser/profiles/off\_the\_record\_profile\_impl.cc:635:19  

#2 0x55ece8958b61 in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&) ./../../chrome/browser/profiles/profile\_impl.cc:963:7  

#3 0x55ece89204fa in Profile::GetPrimaryOTRProfile() ./../../chrome/browser/profiles/profile.cc:492:10  

#4 0x55ecf050db7b in extensions::WindowsCreateFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs\_api.cc:570:52  

#5 0x55ece27f255d in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension\_function.cc:448:10  

#6 0x55ece27fa03f in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg\_Request\_Params const&, content::RenderFrameHost\*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)> const&) ./../../extensions/browser/extension\_function\_dispatcher.cc:383:15  

#7 0x55ece27f919a in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg\_Request\_Params const&, content::RenderFrameHost\*, int) ./../../extensions/browser/extension\_function\_dispatcher.cc:253:5  

#8 0x55ece286f0a7 in void IPC::DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::\*)(content::RenderFrameHost\*, ExtensionHostMsg\_Request\_Params const&), content::RenderFrameHost, std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params>, 0ul>(extensions::ExtensionWebContentsObserver\*, void (extensions::ExtensionWebContentsObserver::\*)(content::RenderFrameHost\*, ExtensionHostMsg\_Request\_Params const&), content::RenderFrameHost\*, std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params>&&, std::\_\_1::integer\_sequence<unsigned long, 0ul>) ./../../ipc/ipc\_message\_templates.h:65:3  

#9 0x55ece286f0a7 in std::\_\_1::enable\_if<(sizeof...(ExtensionHostMsg\_Request\_Params const&)) == (std::tuple\_size<std::\_\_1::decay<std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params> >::type>::value), void>::type IPC::DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, ExtensionHostMsg\_Request\_Params const&, std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params> >(extensions::ExtensionWebContentsObserver\*, void (extensions::ExtensionWebContentsObserver::\*)(content::RenderFrameHost\*, ExtensionHostMsg\_Request\_Params const&), content::RenderFrameHost\*, std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params>&&) ./../../ipc/ipc\_message\_templates.h:77:3  

#10 0x55ece286f0a7 in bool IPC::MessageT<ExtensionHostMsg\_Request\_Meta, std::\_\_1::tuple<ExtensionHostMsg\_Request\_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::\*)(content::RenderFrameHost\*, ExtensionHostMsg\_Request\_Params const&)>(IPC::Message const\*, extensions::ExtensionWebContentsObserver\*, extensions::ExtensionWebContentsObserver\*, content::RenderFrameHost\*, void (extensions::ExtensionWebContentsObserver::\*)(content::RenderFrameHost\*, ExtensionHostMsg\_Request\_Params const&)) ./../../ipc/ipc\_message\_templates.h:140:7  

#11 0x55ece286ee20 in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) ./../../extensions/browser/extension\_web\_contents\_observer.cc:235:5  

#12 0x55ecf079a587 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) ./../../chrome/browser/extensions/chrome\_extension\_web\_contents\_observer.cc:94:37  

#13 0x55ece1c6db10 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl\*, IPC::Message const&) ./../../content/browser/web\_contents/web\_contents\_impl.cc:1142:18  

#14 0x55ece168abb6 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:1894:18  

#15 0x55ecead44e47 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc\_channel\_proxy.cc:325:14  

#16 0x55ece78fd967 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:101:12  

#17 0x55ece78fd967 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:163:33  

#18 0x55ece793b7f0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#19 0x55ece793af24 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#20 0x55ece77fe529 in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:374:46  

#21 0x55ece77fe529 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:124:43  

#22 0x7f9c38bc0536 in g\_main\_context\_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/n/chromes/89.0.4389.114/src/out/x64.asan/chrome+0x15ba6112)  

Shadow bytes around the buggy address:  

0x0c248064f7f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c248064f800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c248064f810: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c248064f820: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c248064f830: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

=>0x0c248064f840: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x0c248064f850: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c248064f860: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c248064f870: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c248064f880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c248064f890: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

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

==16466==ABORTING

## Attachments

- [12_navigation_predictor.tar.gz](attachments/12_navigation_predictor.tar.gz) (application/octet-stream, 6.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 24.0 KB)

## Timeline

### [Deleted User] (2021-04-11)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-04-12)

Here is a second ASAN crash that results from the manual user exit path (not the extension exit path). 

### bt...@gmail.com (2021-04-12)

Uploaded a fix here https://chromium-review.googlesource.com/c/chromium/src/+/2821639

### lu...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>DataProxy]

### lu...@chromium.org (2021-04-12)

AFAIK we treat UaF as high severity (the example given by https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#TOC-High-severity for "Memory corruption in the browser process that can only be triggered from a compromised renderer, leading to a sandbox escape" was also a UaF)

### ry...@chromium.org (2021-04-12)

Spelchat is making some sizeable changes to this code right now, which probably fixes this by moving to frame service base, etc. 

### lu...@chromium.org (2021-04-12)

AFAIU NavigationPredictor has been shipping to the Stable release channel for a while.

### lu...@chromium.org (2021-04-13)

+robertogden@ who authored r734090 which added some of the existing

    if (!web_contents())
      return;

checks in the code (this is also the approach taken by the fix proposed in https://crbug.com/chromium/1197904#c3).

### lu...@chromium.org (2021-04-13)

RE: https://crbug.com/chromium/1197904#c6: ryansturm@:

Migrating to FrameServiceBase sounds like the right long-term strategy here, but a smaller fix is probably still desirable in the short-term (I assume that the FrameServiceBase migration is too complicated to merge to Beta and/or Stable).

### bt...@gmail.com (2021-04-13)

Yup this can be triggered in stable 89.0.4389.114 and head.

### ry...@chromium.org (2021-04-13)

Agreed. Let's take the https://crbug.com/chromium/1197904#c3 cl (already +1'd), so we can take an easy merge. 

### ct...@chromium.org (2021-04-13)

Thank you for the report!

Assigning to tbansal@ and CC'ing sofiyase@ based on https://chromium-review.googlesource.com/c/chromium/src/+/1691705.

The current POC requires MojoJS, which would make us consider this a Severity-High sandbox escape. I think the interaction requirement is very small (especially on Android where IIRC application exit can occur at anytime when the app is in the background). 

I've uploaded the POC to clusterfuzz to see if it can repro there (not 100% sure). I'll do more investigation tomorrow.

Reporter: You mentioned that this may be exploitable on Android without MojoJS. Besides the feature being enabled by default, do you have ideas for how you would actually exploit this? This would raise this to a Severity-Critical, which we would be very interested in knowing about. Any help here would be greatly appreciated.

tbansal@ or others: Do you have any intuition on whether this could be exploitable via standard web APIs as well?

[Monorail components: Blink>Loader]

### cl...@chromium.org (2021-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5738265089736704.

### bt...@gmail.com (2021-04-13)

[Comment Deleted]

### bt...@gmail.com (2021-04-13)

re https://crbug.com/chromium/1197904#c12: I'm not sure how feasible it is to trigger without mojo bindings. The path is reachable programatically by calling `window.open("/foo.html")` if foo has `<a href="">` tags in it [1]. However I'm not sure if it is possible to send enough window.open calls to cause a race between BrowserContext being freed and `NavigationPredictor::ReportAnchorElementMetricsOnLoad` being called before an android device slows down because too many windows or open.

[1] https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/html/anchor_element_metrics_sender.cc;l=78;drc=d5e1999ef5ebc2308f8710dc9eb4d069c3452308

### ct...@chromium.org (2021-04-13)

Thanks! That seems _possible_ but challenging to figure out how to pull it off, so keeping this as Severity-High for now seems reasonable. Let us know if you think about this more and you think there's evidence that it is feasible without mojojs bindings.

### bt...@gmail.com (2021-04-13)

No problem! I completely agree with that assessment :)

### [Deleted User] (2021-04-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7313a810ae0b1361cbe8453bc5496654dee24c76

commit 7313a810ae0b1361cbe8453bc5496654dee24c76
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Tue Apr 13 18:11:13 2021

Ensure that BrowserContext is not used after it has been freed

Previously, it was possible for the BrowserContext to be destroyed
before ReportAnchorElementMetricsOnClick attempted to access it.

The fix uses the fact that NavigationPredictor extends
WebContentsObserver and checks that web_contents is still alive
before dereferencing BrowserContext. WebContents will always
outlive BrowserContext.

R=lukasza@chromium.org, ryansturm@chromium.org

Bug: 1197904
Change-Id: Iee4f126e92670a84d57c7a4ec7d6f702fb975c7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821639
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/master@{#872021}

[modify] https://crrev.com/7313a810ae0b1361cbe8453bc5496654dee24c76/AUTHORS
[modify] https://crrev.com/7313a810ae0b1361cbe8453bc5496654dee24c76/chrome/browser/navigation_predictor/navigation_predictor.cc


### ro...@chromium.org (2021-04-13)

tbansal is OOO, so I'll request the merge for him now.

M90 releases to stable tomorrow, so I'll skip asking to merge to M89.

### [Deleted User] (2021-04-13)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2021-04-13)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2821639

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes, all currently released channels

5. Why are these changes required in this milestone after branch?
Security UAF bug

6. Is this a new feature?
No, but is gated by Finch

7. If it is a new feature, is it behind a flag using finch?

### [Deleted User] (2021-04-14)

Your change meets the bar and is auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f782a440339fa19a44422ca5e7165cddd1cffcc9

commit f782a440339fa19a44422ca5e7165cddd1cffcc9
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Wed Apr 14 21:28:53 2021

Ensure that BrowserContext is not used after it has been freed

Previously, it was possible for the BrowserContext to be destroyed
before ReportAnchorElementMetricsOnClick attempted to access it.

The fix uses the fact that NavigationPredictor extends
WebContentsObserver and checks that web_contents is still alive
before dereferencing BrowserContext. WebContents will always
outlive BrowserContext.

R=​lukasza@chromium.org, ryansturm@chromium.org

(cherry picked from commit 7313a810ae0b1361cbe8453bc5496654dee24c76)

Bug: 1197904
Change-Id: Iee4f126e92670a84d57c7a4ec7d6f702fb975c7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821639
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#872021}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827043
Auto-Submit: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Ryan Sturm <ryansturm@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#77}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f782a440339fa19a44422ca5e7165cddd1cffcc9/AUTHORS
[modify] https://crrev.com/f782a440339fa19a44422ca5e7165cddd1cffcc9/chrome/browser/navigation_predictor/navigation_predictor.cc


### ad...@google.com (2021-04-15)

tbansal/robertogden: Is this deemed a complete fix? If so please could you mark the bug Fixed: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels

### ad...@google.com (2021-04-15)

Approving merge to M90, branch 4430, but please wait until the change has been in Canary for a solid 24 hours. It looks like a very safe change.

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-04-15)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-04-15)

re https://crbug.com/chromium/1197904#c25 yes, this should be a complete band-aid fix. I've filed https://crbug.com/chromium/1199367 to clean it up and make the class more robust to these kinds of issues. I want to keep the bug open until it is merged to M90 tomorrow morning though, is that ok?

re https://crbug.com/chromium/1197904#c26, setting next action to tomorrow and I'll merge then

### ad...@google.com (2021-04-16)

Re https://crbug.com/chromium/1197904#c29 thanks! Yes you can keep this bug open until it's merged if you like, but please don't do that as a matter of course - it prevents Sheriffbot from automating the right merges - see https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e4abe032f3ad1921f38ce255699968608bca9494

commit e4abe032f3ad1921f38ce255699968608bca9494
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Fri Apr 16 18:14:13 2021

Ensure that BrowserContext is not used after it has been freed

Previously, it was possible for the BrowserContext to be destroyed
before ReportAnchorElementMetricsOnClick attempted to access it.

The fix uses the fact that NavigationPredictor extends
WebContentsObserver and checks that web_contents is still alive
before dereferencing BrowserContext. WebContents will always
outlive BrowserContext.

R=​​lukasza@chromium.org, ryansturm@chromium.org

(cherry picked from commit 7313a810ae0b1361cbe8453bc5496654dee24c76)

(cherry picked from commit f782a440339fa19a44422ca5e7165cddd1cffcc9)

Bug: 1197904
Change-Id: Iee4f126e92670a84d57c7a4ec7d6f702fb975c7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821639
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#872021}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827043
Auto-Submit: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Ryan Sturm <ryansturm@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#77}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2830308
Reviewed-by: Tarun Bansal <tbansal@chromium.org>
Commit-Queue: Tarun Bansal <tbansal@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1297}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/e4abe032f3ad1921f38ce255699968608bca9494/AUTHORS
[modify] https://crrev.com/e4abe032f3ad1921f38ce255699968608bca9494/chrome/browser/navigation_predictor/navigation_predictor.cc


### ro...@chromium.org (2021-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b84dc72351bd7b01bf7a0987752ad160029c296

commit 6b84dc72351bd7b01bf7a0987752ad160029c296
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Tue Apr 20 15:45:03 2021

M86-LTS: Ensure that BrowserContext is not used after it has been freed

Previously, it was possible for the BrowserContext to be destroyed
before ReportAnchorElementMetricsOnClick attempted to access it.

The fix uses the fact that NavigationPredictor extends
WebContentsObserver and checks that web_contents is still alive
before dereferencing BrowserContext. WebContents will always
outlive BrowserContext.

R=​lukasza@chromium.org, ryansturm@chromium.org

(cherry picked from commit 7313a810ae0b1361cbe8453bc5496654dee24c76)

Bug: 1197904
Change-Id: Iee4f126e92670a84d57c7a4ec7d6f702fb975c7e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821639
Reviewed-by: Ryan Sturm <ryansturm@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#872021}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2838328
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Auto-Submit: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1613}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/6b84dc72351bd7b01bf7a0987752ad160029c296/AUTHORS
[modify] https://crrev.com/6b84dc72351bd7b01bf7a0987752ad160029c296/chrome/browser/navigation_predictor/navigation_predictor.cc


### bt...@gmail.com (2021-04-20)

[Comment Deleted]

### as...@google.com (2021-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, Brendon! The VRP Panel has decided to award you $27,000 for this report. Thanks you for submitting this issue and your excellent work on it. Please confirm you'd also still like this reward donated to the EFF. Nice work!!

### bt...@gmail.com (2021-04-23)

Thank you amyressler@! Yes I would still like this reward donated+ to the EFF :)

### am...@chromium.org (2021-04-23)

[Comment Deleted]

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-27)

VRP rewards have been doubled and processed for donation at the request of btiszka@

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1197904?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Internals>Network>DataProxy]
[Monorail blocking: crbug.com/chromium/1199367]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055517)*
