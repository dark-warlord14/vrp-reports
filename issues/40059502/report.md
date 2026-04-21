# Security: Heap-use-after-free in sharing_hub::SharingHubBubbleController::OnBubbleClosed

| Field | Value |
|-------|-------|
| **Issue ID** | [40059502](https://issues.chromium.org/issues/40059502) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-04-28 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-mac-release-995881.zip and unzip
2. start a server at poc.html: python -m SimpleHTTPServer 8605
3. ./Chromium <http://127.0.0.1:8605/poc.html>
4. After open chromium, click sharing hub icon, then choose `show QR code`
5. Then move the window down to let the QR code bubble shown on the top, and click sharing hub icon again
6. Clikc the back button in QR code bubble, and you will get two sharing hub bubble shown at the same time
7. wait until crash. See video for more infomations.

**Problem Description:**  

This is similar to <https://crbug.com/chromium/1302949>, so I think you can patch it with similar method

In class `SharingHubBubbleViewImpl`, change the raw ptr `controller_` to a weak ptr  

chrome/browser/ui/views/sharing\_hub/sharing\_hub\_bubble\_view\_impl.cc

- controller\_(controller) {

- controller\_(controller->AsWeakPtr()) {

# **Additional Comments:**

==39475==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000156660 at pc 0x000165c9e61f bp 0x00030cfb5fe0 sp 0x00030cfb5fd8  

WRITE of size 8 at 0x60b000156660 thread T0  

#0 0x165c9e61e in sharing\_hub::SharingHubBubbleController::OnBubbleClosed() sharing\_hub\_bubble\_controller.cc:240  

#1 0x1664e9786 in non-virtual thunk to sharing\_hub::SharingHubBubbleViewImpl::WindowClosing() sharing\_hub\_bubble\_view\_impl.cc:73  

#2 0x164972a83 in views::Widget::OnNativeWidgetDestroying() widget.cc:1418  

#3 0x164a1b818 in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnWindowWillClose() native\_widget\_mac\_ns\_window\_host.mm:1171  

#4 0x160ac8fcd in remote\_cocoa::NativeWidgetNSWindowBridge::OnWindowWillClose() native\_widget\_ns\_window\_bridge.mm:929  

#5 0x160ad910b in -[ViewsNSWindowDelegate windowWillClose:] views\_nswindow\_delegate.mm:182  

#6 0x7ff80123e1be in **CFNOTIFICATIONCENTER\_IS\_CALLING\_OUT\_TO\_AN\_OBSERVER**+0xb (CoreFoundation:x86\_64+0x751be) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#7 0x7ff8012dabd4 in \_\_\_CFXRegistrationPost\_block\_invoke+0x30 (CoreFoundation:x86\_64+0x111bd4) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#8 0x7ff8012dab45 in \_CFXRegistrationPost+0x1ef (CoreFoundation:x86\_64+0x111b45) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#9 0x7ff80120fe99 in \_CFXNotificationPost+0x322 (CoreFoundation:x86\_64+0x46e99) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#10 0x7ff801f7e1bd in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x51 (Foundation:x86\_64+0x91bd) (BuildId: bf00b016c6453574b74f4386750fb00932000000200000000100000000020c00)  

#11 0x7ff80442a02e in -[NSWindow \_finishClosingWindow]+0x77 (AppKit:x86\_64+0x8cc02e) (BuildId: 9d3ab20448583120b0025c38b02edec432000000200000000100000000020c00)  

#12 0x7ff803eb648e in -[NSWindow \_close]+0x14f (AppKit:x86\_64+0x35848e) (BuildId: 9d3ab20448583120b0025c38b02edec432000000200000000100000000020c00)  

#13 0x15e5fcbf0 in base::internal::Invoker<base::internal::BindState<base::ScopedTypeRef<void () block\_pointer, base::mac::internal::ScopedBlockTraits<void () block\_pointer> > >, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:748  

#14 0x15a73c09f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) task\_annotator.cc:135  

#15 0x15a7825b7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:386  

#16 0x15a781c65 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:291  

#17 0x15a783381 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc  

#18 0x15a86d388 in base::MessagePumpCFRunLoopBase::RunWork() message\_pump\_mac.mm:399  

#19 0x15a85a989 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe538989) (BuildId: 4c4c440955553144a1c9f2bec99bd4c52400000010000000000b0a0000030c00)  

#20 0x15a86bca5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:375  

#21 0x7ff801248c07 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0x7fc07) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#22 0x7ff801248b6f in \_\_CFRunLoopDoSource0+0xb3 (CoreFoundation:x86\_64+0x7fb6f) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#23 0x7ff8012488e2 in \_\_CFRunLoopDoSources0+0xf1 (CoreFoundation:x86\_64+0x7f8e2) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#24 0x7ff8012472fe in \_\_CFRunLoopRun+0x380 (CoreFoundation:x86\_64+0x7e2fe) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#25 0x7ff8012468a8 in CFRunLoopRunSpecific+0x236 (CoreFoundation:x86\_64+0x7d8a8) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#26 0x7ff80a2d24f0 in RunCurrentEventLoopInMode+0x123 (HIToolbox:x86\_64+0x324f0) (BuildId: c538aa787afd3f8a8fdb1fc2acde6b3f32000000200000000100000000020c00)  

#27 0x7ff80a2d2246 in ReceiveNextEventCommon+0x24a (HIToolbox:x86\_64+0x32246) (BuildId: c538aa787afd3f8a8fdb1fc2acde6b3f32000000200000000100000000020c00)  

#28 0x7ff80a2d1fe4 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x45 (HIToolbox:x86\_64+0x31fe4) (BuildId: c538aa787afd3f8a8fdb1fc2acde6b3f32000000200000000100000000020c00)  

#29 0x7ff803b9cd87 in \_DPSNextEvent+0x375 (AppKit:x86\_64+0x3ed87) (BuildId: 9d3ab20448583120b0025c38b02edec432000000200000000100000000020c00)  

#30 0x7ff803b9b3f3 in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0x582 (AppKit:x86\_64+0x3d3f3) (BuildId: 9d3ab20448583120b0025c38b02edec432000000200000000100000000020c00)  

#31 0x159533f02 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke chrome\_browser\_application\_mac.mm:239  

#32 0x15a85a989 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe538989) (BuildId: 4c4c440955553144a1c9f2bec99bd4c52400000010000000000b0a0000030c00)  

#33 0x159533a9a in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome\_browser\_application\_mac.mm:238  

#34 0x7ff803b8d918 in -[NSApplication run]+0x249 (AppKit:x86\_64+0x2f918) (BuildId: 9d3ab20448583120b0025c38b02edec432000000200000000100000000020c00)  

#35 0x15a86ed4a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:744  

#36 0x15a86aa57 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:160  

#37 0x15a783a65 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:498  

#38 0x15a6aa1b6 in base::RunLoop::Run(base::Location const&) run\_loop.cc:141  

#39 0x151534ad2 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:1067  

#40 0x1515391c1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:157  

#41 0x15152e315 in content::BrowserMain(content::MainFunctionParams) browser\_main.cc:30  

#42 0x1593874fa in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:659  

#43 0x15938a315 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content\_main\_runner\_impl.cc:1166  

#44 0x1593895e4 in content::ContentMainRunnerImpl::Run() content\_main\_runner\_impl.cc:1038  

#45 0x159385e3d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content\_main.cc:407  

#46 0x1593865ad in content::ContentMain(content::ContentMainParams) content\_main.cc:435  

#47 0x14c326a9c in ChromeMain chrome\_main.cc:177  

#48 0x10454cb65 in main chrome\_exe\_main\_mac.cc:208  

#49 0x2049bb4fd in start+0x1cd (dyld:x86\_64+0x54fd) (BuildId: 7de33963bbc53996ba6ef1d562c17c9532000000200000000100000000020c00)  

#50 0x2049b5fff (<unknown module>)

0x60b000156660 is located 32 bytes inside of 104-byte region [0x60b000156640,0x60b0001566a8)  

freed by thread T0 here:  

#0 0x10cf7e6d9 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x476d9) (BuildId: 07c0453048843a5c89338b25b4878b73240000001000000000070a0000010b00)  

#1 0x15a72f3c5 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1801  

#2 0x15a72f37c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1799  

#3 0x15a72f37c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1799  

#4 0x15a72f37c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1799  

#5 0x15a72f35d in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1798  

#6 0x15a72f37c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1799  

#7 0x15a72f37c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) \_\_tree:1799  

#8 0x15a72ec07 in base::SupportsUserData::~SupportsUserData() supports\_user\_data.cc:71  

#9 0x15284bdf3 in content::WebContentsImpl::~WebContentsImpl() web\_contents\_impl.cc:1115  

#10 0x15284e18d in content::WebContentsImpl::~WebContentsImpl() web\_contents\_impl.cc:1017  

#11 0x1657078b9 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) tab\_strip\_model.cc:569  

#12 0x165710d15 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) tab\_strip\_model.cc:1927  

#13 0x16571237e in TabStripModel::CloseWebContentsAt(int, unsigned int) tab\_strip\_model.cc:787  

#14 0x1528d7454 in content::WebContentsImpl::Close(content::RenderViewHost\*) web\_contents\_impl.cc:7318  

#15 0x14f8ed7c4 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost\*, mojo::Message\*) frame.mojom.cc  

#16 0x15acb91a0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:922  

#17 0x15acc896a in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:48  

#18 0x15acbdd14 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) interface\_endpoint\_client.cc:664  

#19 0x15ce0704d in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc\_mojo\_bootstrap.cc:1010  

#20 0x15ce00d3c in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:748  

#21 0x15a73c09f in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) task\_annotator.cc:135  

#22 0x15a7825b7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:386  

#23 0x15a781c65 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:291  

#24 0x15a783381 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc  

#25 0x15a86d388 in base::MessagePumpCFRunLoopBase::RunWork() message\_pump\_mac.mm:399  

#26 0x15a85a989 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe538989) (BuildId: 4c4c440955553144a1c9f2bec99bd4c52400000010000000000b0a0000030c00)  

#27 0x15a86bca5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:375  

#28 0x7ff801248c07 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0x7fc07) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)  

#29 0x7ff801248b6f in \_\_CFRunLoopDoSource0+0xb3 (CoreFoundation:x86\_64+0x7fb6f) (BuildId: 1d1db08b810c316eb9d9eecdff8ee6e332000000200000000100000000020c00)

previously allocated by thread T0 here:  

#0 0x10cf7e590 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x47590) (BuildId: 07c0453048843a5c89338b25b4878b73240000001000000000070a0000010b00)  

#1 0x1594b2c07 in operator new(unsigned long) new.cpp:67  

#2 0x165c9c4d1 in void content::WebContentsUserData<sharing\_hub::SharingHubBubbleController>::CreateForWebContents<>(content::WebContents\*) web\_contents\_user\_data.h:51  

#3 0x165c9c44d in sharing\_hub::SharingHubBubbleController::CreateOrGetFromWebContents(content::WebContents\*) sharing\_hub\_bubble\_controller.cc:102  

#4 0x1664ebd76 in sharing\_hub::SharingHubIconView::UpdateImpl() sharing\_hub\_icon\_view.cc:80  

#5 0x1662a85c3 in PageActionIconController::UpdateAll() page\_action\_icon\_controller.cc:271  

#6 0x166126d02 in LocationBarView::Update(content::WebContents\*) location\_bar\_view.cc:797  

#7 0x1667786ad in ToolbarView::Update(content::WebContents\*) toolbar\_view.cc:434  

#8 0x1655352cd in Browser::OnActiveTabChanged(content::WebContents\*, content::WebContents\*, int, int) browser.cc:2426  

#9 0x165534307 in Browser::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser.cc:1196  

#10 0x1657039cc in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, absl::optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1896  

#11 0x1657175f9 in TabStripModel::AddWebContents(std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, absl::optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1059  

#12 0x16559e3e1 in Navigate(NavigateParams\*) browser\_navigator.cc:770  

#13 0x1656d88e2 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser\*, chrome::startup::IsProcessStartup, std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&) startup\_browser\_creator\_impl.cc:299  

#14 0x1656db12d in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, chrome::startup::IsProcessStartup, bool) startup\_browser\_creator\_impl.cc:630  

#15 0x1656d78ca in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(chrome::startup::IsProcessStartup) startup\_browser\_creator\_impl.cc:433  

#16 0x1656d6cee in StartupBrowserCreatorImpl::Launch(Profile\*, chrome::startup::IsProcessStartup, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator\_impl.cc:169  

#17 0x1656ce0e1 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile\*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator.cc:673  

#18 0x1656cf0fb in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, StartupProfileInfo, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:738  

#19 0x1656cda48 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc  

#20 0x1656cbe97 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:630  

#21 0x15956ba86 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome\_browser\_main.cc:1744  

#22 0x15956a1fd in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome\_browser\_main.cc:1159  

#23 0x151532602 in content::BrowserMainLoop::PreMainMessageLoopRun() browser\_main\_loop.cc:983  

#24 0x1527a4c1f in content::StartupTaskRunner::RunAllTasksNow() startup\_task\_runner.cc:43  

#25 0x151531adf in content::BrowserMainLoop::CreateStartupTasks() browser\_main\_loop.cc:894  

#26 0x15153883e in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) browser\_main\_runner\_impl.cc:136  

#27 0x15152e2c7 in content::BrowserMain(content::MainFunctionParams) browser\_main.cc:26  

#28 0x1593874fa in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:659  

#29 0x15938a315 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content\_main\_runner\_impl.cc:1166

SUMMARY: AddressSanitizer: heap-use-after-free sharing\_hub\_bubble\_controller.cc:240 in sharing\_hub::SharingHubBubbleController::OnBubbleClosed()  

Shadow bytes around the buggy address:  

0x1c160002ac70: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x1c160002ac80: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x1c160002ac90: 00 00 00 00 fa fa fa fa fa fa fa fa 00 00 00 00  

0x1c160002aca0: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa  

0x1c160002acb0: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x1c160002acc0: fa fa fa fa fa fa fa fa fd fd fd fd[fd]fd fd fd  

0x1c160002acd0: fd fd fd fd fd fa fa fa fa fa fa fa fa fa 00 00  

0x1c160002ace0: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x1c160002acf0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c160002ad00: fd fd fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x1c160002ad10: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

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

==39475==ABORTING  

Received signal 6  

[0x00015a834e49]  

[0x00015a5c7f23]  

[0x00015a834bcb]  

[0x7ff801197e2d]  

[0x203e203e61746144]  

[0x7ff8010ced10]  

[0x00010cfa37a6]  

[0x00010cfa2f04]  

[0x00010cf86a17]  

[0x00010cf85cbc]  

[0x00010cf8732b]  

[0x000165c9e61f]  

[0x0001664e9787]  

[0x000164972a84]  

[0x000164a1b819]  

[0x000160ac8fce]  

[0x000160ad910c]  

[0x7ff80123e1bf]  

[0x7ff8012dabd5]  

[0x7ff8012dab46]  

[0x7ff80120fe9a]  

[0x7ff801f7e1be]  

[0x7ff80442a02f]  

[0x7ff803eb648f]  

[0x00015e5fcbf1]  

[0x00015a73c0a0]  

[0x00015a7825b8]  

[0x00015a781c66]  

[0x00015a783382]  

[0x00015a86d389]  

[0x00015a85a98a]  

[0x00015a86bca6]  

[0x7ff801248c08]  

[0x7ff801248b70]  

[0x7ff8012488e3]  

[0x7ff8012472ff]  

[0x7ff8012468a9]  

[0x7ff80a2d24f1]  

[0x7ff80a2d2247]  

[0x7ff80a2d1fe5]  

[0x7ff803b9cd88]  

[0x7ff803b9b3f4]  

[0x000159533f03]  

[0x00015a85a98a]  

[0x000159533a9b]  

[0x7ff803b8d919]  

[0x00015a86ed4b]  

[0x00015a86aa58]  

[0x00015a783a66]  

[0x00015a6aa1b7]  

[0x000151534ad3]  

[0x0001515391c2]  

[0x00015152e316]  

[0x0001593874fb]  

[0x00015938a316]  

[0x0001593895e5]  

[0x000159385e3e]  

[0x0001593865ae]  

[0x00014c326a9d]  

[0x00010454cb66]  

[0x0002049bb4fe]  

[0x0002049b6000]  

[end of stack trace]

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 173 B)
- [video.mov](attachments/video.mov) (video/quicktime, 3.8 MB)

## Timeline

### dt...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-29)

+ellyjones, do you mind taking a look? Thanks!

[Monorail components: UI>Browser>Sharing]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-04-29)

Yep, sigh. :( This is basically the same bug as https://crbug.com/chromium/1302949 but on a different class. I will do a similar fix.

### el...@chromium.org (2022-04-29)

I have a fix in progress.

Hm, I wonder why the use of raw_ptr<> for that field didn't cause this to be a CHECK instead of an actual UaF... +cc danakj@

### da...@chromium.org (2022-04-29)

1) raw_ptr doesn't do anything yet
2) it won't CHECK when it does do something. it will write junk into the freed memory and hold it from being reallocated while the raw_ptr exists.

### [Deleted User] (2022-04-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/da4e27e68b2b394a764fcbd7b1bb5cca120bb45f

commit da4e27e68b2b394a764fcbd7b1bb5cca120bb45f
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Fri Apr 29 17:19:06 2022

sharing hub: don't UaF during window close

Since window closure is asynchronous, SharingHubBubbleViewImpl's window
close hook can run after SharingHubBubbleController has already been
destroyed as part of WebContents teardown. To avoid that, hold the
Controller as a WeakPtr, not a raw_ptr.

Fixed: 1320592
Change-Id: If194bfe5a1b3930b9c2e1f5e90e09f0b94b2492e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3616864
Commit-Queue: Kristi Park <kristipark@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Kristi Park <kristipark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#997770}

[modify] https://crrev.com/da4e27e68b2b394a764fcbd7b1bb5cca120bb45f/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/da4e27e68b2b394a764fcbd7b1bb5cca120bb45f/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h
[modify] https://crrev.com/da4e27e68b2b394a764fcbd7b1bb5cca120bb45f/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.cc
[modify] https://crrev.com/da4e27e68b2b394a764fcbd7b1bb5cca120bb45f/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.h


### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

Requesting merge to extended stable M100 because latest trunk commit (997770) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (997770) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (997770) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-30)

Merge review required: M102 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-30)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-30)

Merge review required: M100 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-02)

Merge review data:

1. This is a high-severity security issue, so it meets the merge bar for stable as requested by the security team.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3616864
3. Yes, it has been tested on canary
4. No, it is not a new feature
5. I do not know who the applicable eng prod representative would be
6. It fixes a security bug, but there is no convenient way to test for the presence of that security bug, so no manual verification is needed.

### sr...@google.com (2022-05-02)

Merge approved for M102 branch: pls refer to go/chrome-branches for more info

### am...@chromium.org (2022-05-03)

M102 merge approved - please merge to branch 5005 
M101 merge approved - please merge to branch 4951 
M100 merge approved - please merge to branch 4896

Please complete merges NLT EOD Friday, 6 May

### sr...@google.com (2022-05-04)

Please complete the merge to M100 before Thursday May 5th 2022, as we trigger RC build on Friday morning

### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bffe15fac553356274613aafe3c04c9dbe7e2cd3

commit bffe15fac553356274613aafe3c04c9dbe7e2cd3
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Thu May 05 07:31:51 2022

[M100] sharing hub: don't UaF during window close

Since window closure is asynchronous, SharingHubBubbleViewImpl's window
close hook can run after SharingHubBubbleController has already been
destroyed as part of WebContents teardown. To avoid that, hold the
Controller as a WeakPtr, not a raw_ptr.

(cherry picked from commit da4e27e68b2b394a764fcbd7b1bb5cca120bb45f)

Fixed: 1320592
Change-Id: If194bfe5a1b3930b9c2e1f5e90e09f0b94b2492e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3616864
Commit-Queue: Kristi Park <kristipark@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Kristi Park <kristipark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997770}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3628742
Reviewed-by: Travis Skare <skare@chromium.org>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Kristi Park <kristipark@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1230}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/bffe15fac553356274613aafe3c04c9dbe7e2cd3/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/bffe15fac553356274613aafe3c04c9dbe7e2cd3/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h
[modify] https://crrev.com/bffe15fac553356274613aafe3c04c9dbe7e2cd3/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.cc
[modify] https://crrev.com/bffe15fac553356274613aafe3c04c9dbe7e2cd3/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.h


### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41e4d25b6943d3cc436d62369d87e30a39e113ba

commit 41e4d25b6943d3cc436d62369d87e30a39e113ba
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Thu May 05 07:36:47 2022

[M102] sharing hub: don't UaF during window close

Since window closure is asynchronous, SharingHubBubbleViewImpl's window
close hook can run after SharingHubBubbleController has already been
destroyed as part of WebContents teardown. To avoid that, hold the
Controller as a WeakPtr, not a raw_ptr.

(cherry picked from commit da4e27e68b2b394a764fcbd7b1bb5cca120bb45f)

Fixed: 1320592
Change-Id: If194bfe5a1b3930b9c2e1f5e90e09f0b94b2492e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3616864
Commit-Queue: Kristi Park <kristipark@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Kristi Park <kristipark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997770}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3628743
Reviewed-by: Travis Skare <skare@chromium.org>
Commit-Queue: Travis Skare <skare@chromium.org>
Auto-Submit: Kristi Park <kristipark@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#443}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/41e4d25b6943d3cc436d62369d87e30a39e113ba/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/41e4d25b6943d3cc436d62369d87e30a39e113ba/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h
[modify] https://crrev.com/41e4d25b6943d3cc436d62369d87e30a39e113ba/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.cc
[modify] https://crrev.com/41e4d25b6943d3cc436d62369d87e30a39e113ba/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.h


### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b74d01a7b3efa63382ee8f8d463d8ce2a34be62f

commit b74d01a7b3efa63382ee8f8d463d8ce2a34be62f
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Thu May 05 07:42:32 2022

[M101] sharing hub: don't UaF during window close

Since window closure is asynchronous, SharingHubBubbleViewImpl's window
close hook can run after SharingHubBubbleController has already been
destroyed as part of WebContents teardown. To avoid that, hold the
Controller as a WeakPtr, not a raw_ptr.

(cherry picked from commit da4e27e68b2b394a764fcbd7b1bb5cca120bb45f)

Fixed: 1320592
Change-Id: If194bfe5a1b3930b9c2e1f5e90e09f0b94b2492e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3616864
Commit-Queue: Kristi Park <kristipark@chromium.org>
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Kristi Park <kristipark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997770}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3628546
Reviewed-by: Travis Skare <skare@chromium.org>
Auto-Submit: Kristi Park <kristipark@chromium.org>
Commit-Queue: Travis Skare <skare@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#1173}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/b74d01a7b3efa63382ee8f8d463d8ce2a34be62f/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/b74d01a7b3efa63382ee8f8d463d8ce2a34be62f/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h
[modify] https://crrev.com/b74d01a7b3efa63382ee8f8d463d8ce2a34be62f/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.cc
[modify] https://crrev.com/b74d01a7b3efa63382ee8f8d463d8ce2a34be62f/chrome/browser/ui/views/sharing_hub/sharing_hub_bubble_view_impl.h


### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

And another one! Thank you for reporting this issue as well. Due to the substantial amount of user interaction required to trigger this issue, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us. 

### me...@gmail.com (2022-05-17)

[Comment Deleted]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1320592?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059502)*
