# Security: Heap-use-after-free in constrained_window::CreateWebModalDialogViews

| Field | Value |
|-------|-------|
| **Issue ID** | [40055448](https://issues.chromium.org/issues/40055448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2021-04-04 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version: 91.0.4466.0 (Official Build) canary (x86\_64)  

Operating System: All

**REPRODUCTION CASE**

- Enable #enable-experimental-web-platform-features flag.

1. Open two tabs "about:blank" and "<https://rsolomakhin.github.io/pr/spc-enroll/>"
2. Click on "Open window to enroll credential" button.
3. Click on "Enroll"
4. Detach <https://rsolomakhin.github.io/pr/spc-enroll> tab then close "about:blank" page
5. Click on "Enroll" >> UaF crash

==7529==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070001e2ae0 at pc 0x00011e40e9f0 bp 0x7fff5e08c110 sp 0x7fff5e08c108  

READ of size 8 at 0x6070001e2ae0 thread T0  

#0 0x11e40e9ef in constrained\_window::CreateWebModalDialogViews(views::WidgetDelegate\*, content::WebContents\*) constrained\_window\_views.cc:191  

#1 0x11e40e79f in constrained\_window::ShowWebModalDialogViews(views::WidgetDelegate\*, content::WebContents\*) constrained\_window\_views.cc:178  

#2 0x11dde11ff in payments::PaymentCredentialEnrollmentDialogView::ShowDialog(content::WebContents\*, base::WeakPtr[payments::PaymentCredentialEnrollmentModel](javascript:void(0);), base::OnceCallback<void ()>, base::OnceCallback<void ()>) payment\_credential\_enrollment\_dialog\_view.cc:75  

#3 0x11e4a1c4a in payments::PaymentCredentialEnrollmentController::ShowDialog(content::GlobalFrameRoutingId, std::\_\_1::unique\_ptr<SkBitmap, std::\_\_1::default\_delete<SkBitmap> >, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&, base::OnceCallback<void (bool)>) payment\_credential\_enrollment\_controller.cc:87  

#4 0x11e49e575 in payments::PaymentCredential::DidDownloadIcon(base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&) payment\_credential.cc:207  

#5 0x11e4a067d in void base::internal::FunctorTraits<void (payments::PaymentCredential::\*)(base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), void>::Invoke<void (payments::PaymentCredential::\*)(base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[payments::PaymentCredential](javascript:void(0);), base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&>(void (payments::PaymentCredential::\*)(base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[payments::PaymentCredential](javascript:void(0);)&&, base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>&&, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >&&, int&&, int&&, GURL const&&&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&&&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&&&) bind\_internal.h:498  

#6 0x11e4a0389 in base::internal::Invoker<base::internal::BindState<void (payments::PaymentCredential::\*)(base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> >, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[payments::PaymentCredential](javascript:void(0);), base::OnceCallback<void (payments::mojom::PaymentCredentialUserPromptStatus)>, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > >, void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>::RunOnce(base::internal::BindStateBase\*, int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&) bind\_internal.h:657  

#7 0x10b18b3d0 in content::WebContentsImpl::OnDidDownloadImage(base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL const&, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&) callback.h:101  

#8 0x10b1e3c56 in void base::internal::FunctorTraits<void (content::WebContentsImpl::\*)(base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL const&, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), void>::Invoke<void (content::WebContentsImpl::\*)(base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL const&, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[content::WebContentsImpl](javascript:void(0);), base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&>(void (content::WebContentsImpl::\*)(base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL const&, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[content::WebContentsImpl](javascript:void(0);)&&, base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>&&, int&&, GURL&&, int&&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&&&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&&&) bind\_internal.h:498  

#9 0x10b1e39c6 in base::internal::Invoker<base::internal::BindState<void (content::WebContentsImpl::\*)(base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL const&, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&), base::WeakPtr[content::WebContentsImpl](javascript:void(0);), base::OnceCallback<void (int, int, GURL const&, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>, int, GURL>, void (int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&)>::RunOnce(base::internal::BindStateBase\*, int, std::\_\_1::vector<SkBitmap, std::\_\_1::allocator<SkBitmap> > const&, std::\_\_1::vector<gfx::Size, std::\_\_1::allocator[gfx::Size](javascript:void(0);) > const&) bind\_internal.h:657  

#10 0x1084c14b7 in blink::mojom::ImageDownloader\_DownloadImage\_ForwardToCallback::Accept(mojo::Message\*) callback.h:101  

#11 0x112b64393 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:549  

#12 0x112b6c4c5 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:43  

#13 0x112b77ef7 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) multiplex\_router.cc:955  

#14 0x112b764b7 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) multiplex\_router.cc:622  

#15 0x112b6c4c5 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:43  

#16 0x112b59589 in mojo::Connector::DispatchMessage(mojo::Message) connector.cc:508  

#17 0x112b5b0a8 in mojo::Connector::ReadAllAvailableMessages() connector.cc:566  

#18 0x112bc2db4 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) callback.h:168  

#19 0x112bc40ba in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:498  

#20 0x1113d214f in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#21 0x11140d81a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#22 0x11140d037 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#23 0x1114fae03 in base::MessagePumpCFRunLoopBase::RunWork() message\_pump\_mac.mm:358  

#24 0x1114e8299 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbae8299)  

#25 0x1114f97d5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#26 0x7fffa5396e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#27 0x7fffa53780cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#28 0x7fffa53775b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)  

#29 0x7fffa5376fb3 in CFRunLoopRunSpecific+0x1a3 (CoreFoundation:x86\_64+0x84fb3)  

#30 0x7fffa48d5ebb in RunCurrentEventLoopInMode+0xef (HIToolbox:x86\_64+0x30ebb)  

#31 0x7fffa48d5cf0 in ReceiveNextEventCommon+0x1af (HIToolbox:x86\_64+0x30cf0)  

#32 0x7fffa48d5b25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (HIToolbox:x86\_64+0x30b25)  

#33 0x7fffa2e6aa03 in \_DPSNextEvent+0x45f (AppKit:x86\_64+0x46a03)  

#34 0x7fffa35e67ed in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0xaeb (AppKit:x86\_64+0x7c27ed)  

#35 0x1126abdc2 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke chrome\_browser\_application\_mac.mm:237  

#36 0x1114e8299 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbae8299)  

#37 0x1126ab95a in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome\_browser\_application\_mac.mm:236  

#38 0x7fffa2e5f38a in -[NSApplication run]+0x39d (AppKit:x86\_64+0x3b38a)  

#39 0x1114fc6fa in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:691  

#40 0x1114f8818 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:149  

#41 0x11140ea3b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:460  

#42 0x11134c25e in base::RunLoop::Run(base::Location const&) run\_loop.cc:133  

#43 0x1119fd823 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) chrome\_browser\_main.cc:1732  

#44 0x10a054467 in content::BrowserMainLoop::RunMainMessageLoopParts() browser\_main\_loop.cc:970  

#45 0x10a058b51 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#46 0x10a04d9fc in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#47 0x1111287c4 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:581  

#48 0x111127af4 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:944  

#49 0x111124ce6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#50 0x1111252fc in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#51 0x105a081d5 in ChromeMain chrome\_main.cc:141  

#52 0x101b7040f in main chrome\_exe\_main\_mac.cc:114  

#53 0x7fffbafbf234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x6070001e2ae0 is located 0 bytes inside of 72-byte region [0x6070001e2ae0,0x6070001e2b28)  

freed by thread T0 here:  

#0 0x101eaafc9 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44fc9)  

#1 0x11db361c8 in BrowserViewLayout::~BrowserViewLayout() memory:1335  

#2 0x11cb766c7 in views::View::~View() memory:1335  

#3 0x11db11f46 in BrowserView::~BrowserView() browser\_view.cc:692  

#4 0x11db12567 in non-virtual thunk to BrowserView::~BrowserView() browser\_view.cc:657  

#5 0x11cb76826 in views::View::~View() view.cc:237  

#6 0x11cc0b45a in views::NonClientView::~NonClientView() non\_client\_view.cc:164  

#7 0x11cb79f3b in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) memory:1335  

#8 0x11cb7a2fb in views::View::RemoveAllChildViews(bool) view.cc:306  

#9 0x11cbd4bf6 in views::Widget::~Widget() widget.cc:1553  

#10 0x11db043ad in BrowserFrame::~BrowserFrame() browser\_frame.cc:78  

#11 0x11cc489cd in views::NativeWidgetMac::~NativeWidgetMac() native\_widget\_mac.mm:123  

#12 0x11d89f719 in BrowserFrameMac::~BrowserFrameMac() browser\_frame\_mac.mm:112  

#13 0x118edf1bb in -[ViewsNSWindowDelegate windowWillClose:] views\_nswindow\_delegate.mm:182  

#14 0x7fffa538cfbb in **CFNOTIFICATIONCENTER\_IS\_CALLING\_OUT\_TO\_AN\_OBSERVER**+0xb (CoreFoundation:x86\_64+0x9afbb)  

#15 0x7fffa538ceba in \_CFXRegistrationPost+0x1aa (CoreFoundation:x86\_64+0x9aeba)  

#16 0x7fffa538cc21 in \_\_\_CFXNotificationPost\_block\_invoke+0x31 (CoreFoundation:x86\_64+0x9ac21)  

#17 0x7fffa534b1b1 in -[\_CFXNotificationRegistrar find:object:observer:enumerator:]+0x7e1 (CoreFoundation:x86\_64+0x591b1)  

#18 0x7fffa534a19a in \_CFXNotificationPost+0x29a (CoreFoundation:x86\_64+0x5819a)  

#19 0x7fffa6d8ee86 in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x41 (Foundation:x86\_64+0x6e86)  

#20 0x7fffa3101da3 in \_\_18-[NSWindow \_close]\_block\_invoke+0xcc (AppKit:x86\_64+0x2ddda3)  

#21 0x7fffa3101c87 in -[NSWindow \_close]+0x16c (AppKit:x86\_64+0x2ddc87)  

#22 0x1126f9dd0 in base::internal::Invoker<base::internal::BindState<base::ScopedTypeRef<void () block\_pointer, base::mac::internal::ScopedBlockTraits<void () block\_pointer> > >, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:479  

#23 0x1113d214f in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#24 0x11140d81a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#25 0x11140d037 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#26 0x1114fae03 in base::MessagePumpCFRunLoopBase::RunWork() message\_pump\_mac.mm:358  

#27 0x1114e8299 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbae8299)  

#28 0x1114f97d5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#29 0x7fffa5396e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)

previously allocated by thread T0 here:  

#0 0x101eaae80 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44e80)  

#1 0x11124c067 in operator new(unsigned long) new.cpp:67  

#2 0x11db35e74 in BrowserViewLayout::BrowserViewLayout(std::\_\_1::unique\_ptr<BrowserViewLayoutDelegate, std::\_\_1::default\_delete<BrowserViewLayoutDelegate> >, gfx::NativeView, BrowserView\*, views::View\*, TabStripRegionView\*, TabStrip\*, views::View\*, InfoBarContainerView\*, views::View\*, views::View\*, ImmersiveModeController\*, views::View\*, views::View\*) memory:2006  

#3 0x11db264b9 in BrowserView::AddedToWidget() memory:2006  

#4 0x11cba2b67 in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) view.cc:2624  

#5 0x11cba05fe in views::View::AddChildViewAtImpl(views::View\*, int) view.cc:2510  

#6 0x11cc0dab9 in views::NonClientView::ViewHierarchyChanged(views::ViewHierarchyChangedDetails const&) non\_client\_view.cc:306  

#7 0x11cba23b1 in views::View::ViewHierarchyChangedImpl(views::ViewHierarchyChangedDetails const&) view.cc:2641  

#8 0x11cba2b1a in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) view.cc:2622  

#9 0x11cba05fe in views::View::AddChildViewAtImpl(views::View\*, int) view.cc:2510  

#10 0x11cbd39e4 in views::Widget::Init(views::Widget::InitParams) widget.cc:375  

#11 0x11db04a6e in BrowserFrame::InitBrowserFrame() browser\_frame.cc:113  

#12 0x11db3c6a7 in BrowserWindow::CreateBrowserWindow(std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >, bool, bool) browser\_window\_factory.cc:46  

#13 0x11d232ff3 in Browser::Browser(Browser::CreateParams const&) browser.cc:512  

#14 0x11d23190b in Browser::Create(Browser::CreateParams const&) browser.cc:432  

#15 0x11d3f15bd in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser\*, bool, std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&) startup\_browser\_creator\_impl.cc:238  

#16 0x11d3f400b in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) startup\_browser\_creator\_impl.cc:521  

#17 0x11d3f093c in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool, std::\_\_1::vector<GURL, std::\_\_1::allocator<GURL> > const&) startup\_browser\_creator\_impl.cc:385  

#18 0x11d3efc94 in StartupBrowserCreatorImpl::Launch(Profile\*, std::\_\_1::vector<GURL, std::\_\_1::allocator<GURL> > const&, bool, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator\_impl.cc:186  

#19 0x11d3e35d9 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile\*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator.cc:519  

#20 0x11d3eb0b8 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:993  

#21 0x11d3e2c5c in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:921  

#22 0x11d3e114c in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:471  

#23 0x1119fafbc in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome\_browser\_main.cc:1638  

#24 0x1119f93ad in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome\_browser\_main.cc:1042  

#25 0x10a0540f7 in content::BrowserMainLoop::PreMainMessageLoopRun() browser\_main\_loop.cc:944  

#26 0x10b09413f in content::StartupTaskRunner::RunAllTasksNow() callback.h:101  

#27 0x10a0512d0 in content::BrowserMainLoop::CreateStartupTasks() browser\_main\_loop.cc:854  

#28 0x10a058285 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) browser\_main\_runner\_impl.cc:129  

#29 0x10a04d9b7 in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:43

SUMMARY: AddressSanitizer: heap-use-after-free constrained\_window\_views.cc:191 in constrained\_window::CreateWebModalDialogViews(views::WidgetDelegate\*, content::WebContents\*)  

Shadow bytes around the buggy address:  

0x1c0e0003c500: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x1c0e0003c510: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x1c0e0003c520: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa  

0x1c0e0003c530: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x1c0e0003c540: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd  

=>0x1c0e0003c550: fd fd fd fd fd fd fd fa fa fa fa fa[fd]fd fd fd  

0x1c0e0003c560: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

0x1c0e0003c570: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x1c0e0003c580: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x1c0e0003c590: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa  

0x1c0e0003c5a0: fa fa 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

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

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 9.2 MB)
- [testcase.html](attachments/testcase.html) (text/plain, 1.2 KB)
- [confirm.js](attachments/confirm.js) (text/plain, 1.2 KB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 12.0 MB)

## Timeline

### [Deleted User] (2021-04-04)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report. I'm having trouble reproducing this as-is. I'm fairly certain you missed a step to install the "credential enrollment payment handler", based on your test page, but even doing that doesn't reliably reproduce the crash.

Can you make a self-contained PoC for this problem? Because there seem to be a lot of remote resources involved in this crash, and I suspect some of them are interfering with reliable reproduction.

### ch...@gmail.com (2021-04-05)

[Comment Deleted]

### [Deleted User] (2021-04-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2021-04-05)

Sorry I missed that step!

Unfortunately I cannot now make a standalone PoC.

1. Open a new tab (about:blank)
2. Open another tab and go to https://skilful-reserve-239412.appspot.com/static/apps/max-nonbasiccard/ and install the Max-Pay thing.
3. Click on "Test it out"
4. Click on "Buy" 
5. Change the URL to https://lbstyle.github.io/testcase.html then click on "Go!"
6. Detach the tab and try to close "about:blank" window >> UaF crash!

### jd...@chromium.org (2021-04-07)

I still can't repro this, but I'm going to give it the benefit of the doubt here.

sahel@: you took crbug.com/1114556. Can you take a look at this one, too?

[Monorail components: Blink>Payments]

### ch...@gmail.com (2021-04-07)

Oh it was my mistake, you need to enable #enable-experimental-web-platform-features not #enable-experimental-webassembly-features flag.

### ma...@chromium.org (2021-04-07)

[Description Changed]

### ma...@chromium.org (2021-04-07)

https://crbug.com/chromium/1195686#c7, thanks, I've edited the bug description.

### sa...@chromium.org (2021-04-07)

Based on the stack trace and https://lbstyle.github.io/testcase.html  looks like the issue is related to SPC, handing it off to Nick since he is the main domain expert.


### np...@chromium.org (2021-04-08)

Thanks for the report! Can repro. The root issue, as shown in the video in https://crbug.com/chromium/1195686#c5, is that the dialog is attached to the wrong webcontents when the new window is split. This is only an issue when SPC is invoked from the modal window web contents. Still investigating the fix. This issue is only in M91 as the feature was completely disabled prior.

### np...@chromium.org (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2021-04-08)

I'm still investigating the fix but I don't think we need to revert anything, this is only enabled in M91 so I'll make sure the fix is landed and merged before beta

### np...@chromium.org (2021-04-14)

I've got a fix ready. The problem is that we're displaying a secondary modal dialog (SPC) on top of a modal dialog (Payment Handler), and the way this was originally implemented is that the secondary dialog uses the browser's dialog host[1]. So this UAF works by pulling the SPC/payment handler tab out to a new browser window, while the PaymentHandlerModalDialogManagerDelegate still holds a pointer to the old browser's dialog host.

Ideally we just shouldn't use the browser's dialog host (this doesn't fix the weirdness where the SPC dialog is stuck to the old browser window when the tab is detached), but the web contents' dialog host doesn't allow stacking the SPC dialog on top of the Payment Handler dialog. So I'll land+merge the simpler fix to ensure PaymentHandlerModalDialogManagerDelegate returns the current browser dialog host, and take a follow-up task to improve this edge case.

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc;l=213-216;drc=57544c227ec492b8574ec8163def47ff57d36511

### gi...@appspot.gserviceaccount.com (2021-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0681f72f48cfd31fb6e6599cc87ca20a517484e1

commit 0681f72f48cfd31fb6e6599cc87ca20a517484e1
Author: Nick Burris <nburris@chromium.org>
Date: Thu Apr 15 14:31:20 2021

Make PaymentHandlerModalDialogManagerDelegate return the active host

The PaymentHandlerModalDialogManagerDelegate provides the browser's
dialog host for showing additional modal dialogs such as Secure Payment
Confirmation. This patch ensures the current browser's dialog host is
returned, which may be a different browser than when the delegate was
created.

Bug: 1195686
Change-Id: I1c8247dd77cd855e0b089e4f331c820c6441fb64
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2824374
Commit-Queue: Nick Burris <nburris@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#872821}

[modify] https://crrev.com/0681f72f48cfd31fb6e6599cc87ca20a517484e1/chrome/browser/ui/views/payments/payment_handler_modal_dialog_manager_delegate.cc
[modify] https://crrev.com/0681f72f48cfd31fb6e6599cc87ca20a517484e1/chrome/browser/ui/views/payments/payment_handler_modal_dialog_manager_delegate.h
[modify] https://crrev.com/0681f72f48cfd31fb6e6599cc87ca20a517484e1/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### np...@chromium.org (2021-04-15)

Requesting merge to M91: https://chromium-review.googlesource.com/c/chromium/src/+/2827211

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-16)

Your change meets the bar and is auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2021-04-16)

Fixed on Canary 92.0.4479.0. Thanks Nick for the fix!

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a762314d99e45c4879ee77d41166cbcb167a21c

commit 2a762314d99e45c4879ee77d41166cbcb167a21c
Author: Nick Burris <nburris@chromium.org>
Date: Fri Apr 16 16:19:19 2021

Make PaymentHandlerModalDialogManagerDelegate return the active host

[Merge to M91]
The PaymentHandlerModalDialogManagerDelegate provides the browser's
dialog host for showing additional modal dialogs such as Secure Payment
Confirmation. This patch ensures the current browser's dialog host is
returned, which may be a different browser than when the delegate was
created.

Bug: 1195686
Change-Id: I1c8247dd77cd855e0b089e4f331c820c6441fb64
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827211
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#147}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/2a762314d99e45c4879ee77d41166cbcb167a21c/chrome/browser/ui/views/payments/payment_handler_modal_dialog_manager_delegate.cc
[modify] https://crrev.com/2a762314d99e45c4879ee77d41166cbcb167a21c/chrome/browser/ui/views/payments/payment_handler_modal_dialog_manager_delegate.h
[modify] https://crrev.com/2a762314d99e45c4879ee77d41166cbcb167a21c/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### ro...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### np...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, Khalil - The VRP panel has decided to award you $5000 for this report. Nice work!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195686?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055448)*
