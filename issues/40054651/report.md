# Security: Heap buffer overflow in Tab Groups

| Field | Value |
|-------|-------|
| **Issue ID** | [40054651](https://issues.chromium.org/issues/40054651) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-02-02 |
| **Bounty** | $7,500.00 |

## Description

Chrome Version: 90.0.4406.0 (Official Build) canary (x86\_64) and stable  

Operating System: MacOS

**REPRODUCTION CASE**

Similar to <https://crbug.com/chromium/1163845>

1. python -m SimpleHTTPServer
2. out/asan/chrome --user-data-dir=/tmp/xxxx "about:blank" "<http://localhost:8000/poc.html>"
3. Add <http://localhost:8000/poc.html> to a new group.
4. Click on the button then click on the button
5. Now hold the mouse over the grey point and keep dragging the tab from the right to the left

==1399==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6100002d0d28 at pc 0x00012e902fb9 bp 0x7fff53494d10 sp 0x7fff53494d08  

READ of size 8 at 0x6100002d0d28 thread T0  

#0 0x12e902fb8 in TabStrip::SetSelection(ui::ListSelectionModel const&) view\_model.h:81  

#1 0x12e865f4a in BrowserTabStripController::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser\_tab\_strip\_controller.cc:689  

#2 0x12dd72a0b in TabStripModel::SetSelection(ui::ListSelectionModel, TabStripModelObserver::ChangeReason, bool) tab\_strip\_model.cc:1884  

#3 0x12dd7aa92 in TabStripModel::SetSelectionFromModel(ui::ListSelectionModel) tab\_strip\_model.cc:915  

#4 0x12e8bcea5 in TabDragController::CompleteDrag() tab\_drag\_controller.cc:1794  

#5 0x12e8b0290 in TabDragController::EndDragImpl(TabDragController::EndDragType) tab\_drag\_controller.cc:1531  

#6 0x12e8a7147 in TabDragController::EndDrag(EndDragReason) tab\_drag\_controller.cc:646  

#7 0x12e909363 in TabStrip::EndDrag(EndDragReason) tab\_strip.cc:477  

#8 0x12e8fbc5c in TabStrip::RemoveTabAt(content::WebContents\*, int, bool) tab\_strip.cc:1390  

#9 0x12e865d0d in BrowserTabStripController::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser\_tab\_strip\_controller.cc:647  

#10 0x12dd702bb in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) tab\_strip\_model.cc:526  

#11 0x12dd7703f in TabStripModel::InternalCloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) tab\_strip\_model.cc:1754  

#12 0x12dd77850 in TabStripModel::CloseWebContentsAt(int, unsigned int) tab\_strip\_model.cc:731  

#13 0x11c3189ae in content::WebContentsImpl::Close(content::RenderViewHost\*) web\_contents\_impl.cc:6993  

#14 0x11be105c1 in content::RenderViewHostImpl::ClosePage() render\_view\_host\_impl.cc:665  

#15 0x11bd5f07e in content::RenderFrameHostManager::BeforeUnloadCompleted(bool, base::TimeTicks const&) render\_frame\_host\_manager.cc:341  

#16 0x11bd3e671 in base::internal::Invoker<base::internal::BindState<content::RenderFrameHostImpl::ProcessBeforeUnloadCompletedFromFrame(bool, bool, content::RenderFrameHostImpl\*, bool, base::TimeTicks const&, base::TimeTicks const&)::$\_5, base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), base::TimeTicks, bool, bool>, void ()>::RunOnce(base::internal::BindStateBase\*) render\_frame\_host\_impl.cc:3557  

#17 0x11bca9b89 in content::RenderFrameHostImpl::ProcessBeforeUnloadCompletedFromFrame(bool, bool, content::RenderFrameHostImpl\*, bool, base::TimeTicks const&, base::TimeTicks const&) callback.h:101  

#18 0x11bcd2c65 in content::RenderFrameHostImpl::ProcessBeforeUnloadCompleted(bool, bool, base::TimeTicks const&, base::TimeTicks const&) render\_frame\_host\_impl.cc:3458  

#19 0x11bd57929 in base::internal::Invoker<base::internal::BindState<content::RenderFrameHostImpl::SendBeforeUnload(bool, base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);))::$\_23, base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);) >, void (bool, base::TimeTicks, base::TimeTicks)>::RunOnce(base::internal::BindStateBase\*, bool, base::TimeTicks&&, base::TimeTicks&&) render\_frame\_host\_impl.cc:9465  

#20 0x11929905f in blink::mojom::LocalFrame\_BeforeUnload\_ForwardToCallback::Accept(mojo::Message\*) callback.h:101  

#21 0x1233247ee in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:549  

#22 0x12332d238 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:41  

#23 0x1251aa16d in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ipc\_mojo\_bootstrap.cc:945  

#24 0x1251a313c in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:498  

#25 0x121b21b15 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#26 0x121b5fe30 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#27 0x121b5f5d7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#28 0x121c4fc18 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:358  

#29 0x121c3d1b9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xb4221b9)  

#30 0x121c4e365 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#31 0x7fffa8ac6e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#32 0x7fffa8aa80cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#33 0x7fffa8aa75b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)  

#34 0x7fffa8aa6fb3 in CFRunLoopRunSpecific+0x1a3 (CoreFoundation:x86\_64+0x84fb3)  

#35 0x7fffa8005ebb in RunCurrentEventLoopInMode+0xef (HIToolbox:x86\_64+0x30ebb)  

#36 0x7fffa8005bf8 in ReceiveNextEventCommon+0xb7 (HIToolbox:x86\_64+0x30bf8)  

#37 0x7fffa8005b25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (HIToolbox:x86\_64+0x30b25)  

#38 0x7fffa659aa03 in \_DPSNextEvent+0x45f (AppKit:x86\_64+0x46a03)  

#39 0x7fffa6d167ed in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0xaeb (AppKit:x86\_64+0x7c27ed)  

#40 0x122e4d842 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke chrome\_browser\_application\_mac.mm:229  

#41 0x121c3d1b9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xb4221b9)  

#42 0x122e4d3da in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome\_browser\_application\_mac.mm:228  

#43 0x7fffa658f38a in -[NSApplication run]+0x39d (AppKit:x86\_64+0x3b38a)  

#44 0x121c515da in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:691  

#45 0x121c4d1b8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:149  

#46 0x121b6181b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:460  

#47 0x121aa788b in base::RunLoop::Run() run\_loop.cc:131  

#48 0x122173261 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) chrome\_browser\_main.cc:1736  

#49 0x11b04aef9 in content::BrowserMainLoop::RunMainMessageLoopParts() browser\_main\_loop.cc:970  

#50 0x11b0504c1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#51 0x11b04276c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#52 0x121884175 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:555  

#53 0x1218834c3 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:926  

#54 0x12188025b in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#55 0x12188091c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#56 0x116820a35 in ChromeMain chrome\_main.cc:141  

#57 0x10c765eff in main chrome\_exe\_main\_mac.cc:114  

#58 0x7fffbe6ef234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x6100002d0d28 is located 24 bytes to the left of 192-byte region [0x6100002d0d40,0x6100002d0e00)  

allocated by thread T0 here:  

#0 0x10c949d30 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x45d30)  

#1 0x1219a5387 in operator new(unsigned long) new.cpp:67  

#2 0x12d84a6f6 in std::\_\_1::vector<views::ViewModelBase::Entry, std::\_\_1::allocator[views::ViewModelBase::Entry](javascript:void(0);) >::insert(std::\_\_1::\_\_wrap\_iter<views::ViewModelBase::Entry const\*>, views::ViewModelBase::Entry const&) \_\_split\_buffer:318  

#3 0x12d84b032 in views::ViewModelBase::AddUnsafe(views::View\*, int) view\_model.cc:74  

#4 0x12e8f7c82 in TabStrip::AddTabAt(int, TabRendererData, bool) tab\_strip.cc:1271  

#5 0x12e860e4d in BrowserTabStripController::AddTab(content::WebContents\*, int, bool) browser\_tab\_strip\_controller.cc:775  

#6 0x12e865a40 in BrowserTabStripController::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser\_tab\_strip\_controller.cc:639  

#7 0x12dd6d30e in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1726  

#8 0x12dd6c6bb in TabStripModel::InsertWebContentsAt(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:379  

#9 0x12dbc17b9 in chrome::AddRestoredTab(Browser\*, std::\_\_1::vector<sessions::SerializedNavigationEntry, std::\_\_1::allocator[sessions::SerializedNavigationEntry](javascript:void(0);) > const&, int, int, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::Optional<tab\_groups::TabGroupId>, bool, bool, base::TimeTicks, content::SessionStorageNamespace\*, sessions::SerializedUserAgentOverride const&, bool) browser\_tabrestore.cc:160  

#10 0x12321d0a5 in SessionRestoreImpl::RestoreTab(sessions::SessionTab const&, Browser\*, std::\_\_1::vector<SessionRestoreDelegate::RestoredTab, std::\_\_1::allocator[SessionRestoreDelegate::RestoredTab](javascript:void(0);) >\*, int, bool, base::TimeTicks) session\_restore.cc:624  

#11 0x1232194a9 in SessionRestoreImpl::RestoreTabsToBrowser(sessions::SessionWindow const&, Browser\*, int, std::\_\_1::vector<SessionRestoreDelegate::RestoredTab, std::\_\_1::allocator[SessionRestoreDelegate::RestoredTab](javascript:void(0);) >\*) session\_restore.cc:587  

#12 0x12321721e in SessionRestoreImpl::ProcessSessionWindows(std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >\*, SessionID, std::\_\_1::vector<SessionRestoreDelegate::RestoredTab, std::\_\_1::allocator[SessionRestoreDelegate::RestoredTab](javascript:void(0);) >\*) session\_restore.cc:448  

#13 0x123216457 in SessionRestoreImpl::OnGotSession(std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID) session\_restore.cc:349  

#14 0x1232169b9 in void base::internal::FunctorTraits<void (SessionRestoreImpl::\*)(std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID), void>::Invoke<void (SessionRestoreImpl::\*)(std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID), base::WeakPtr<SessionRestoreImpl>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID>(void (SessionRestoreImpl::\*)(std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID), base::WeakPtr<SessionRestoreImpl>&&, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >&&, SessionID&&) bind\_internal.h:498  

#15 0x12322c87d in SessionService::OnGotSessionCommands(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >) callback.h:101  

#16 0x123230dfe in void base::internal::FunctorTraits<void (SessionService::\*)(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >), void>::Invoke<void (SessionService::\*)(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >), base::WeakPtr<SessionService>, base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > >(void (SessionService::\*)(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >), base::WeakPtr<SessionService>&&, base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionWindow, std::\_\_1::default\_delete[sessions::SessionWindow](javascript:void(0);) > > >, SessionID)>&&, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >&&) bind\_internal.h:498  

#17 0x11ce1d1dd in void base::internal::ReplyAdapter<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >, std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > >(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >)>, std::\_\_1::unique\_ptr<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >, std::\_\_1::default\_delete<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > > >\*) callback.h:101  

#18 0x11ce1d769 in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >)>, std::\_\_1::unique\_ptr<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >, std::\_\_1::default\_delete<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > > >\*), base::OnceCallback<void (std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >)>, base::internal::OwnedWrapper<std::\_\_1::unique\_ptr<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >, std::\_\_1::default\_delete<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > > >, std::\_\_1::default\_delete<std::\_\_1::unique\_ptr<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > >, std::\_\_1::default\_delete<std::\_\_1::vector<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sessions::SessionCommand, std::\_\_1::default\_delete[sessions::SessionCommand](javascript:void(0);) > > > > > > > >, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:393  

#19 0x121bb8316 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) callback.h:101  

#20 0x121bb8558 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:393  

#21 0x121b21b15 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#22 0x121b5fe30 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#23 0x121b5f5d7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#24 0x121c4fc18 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:358  

#25 0x121c3d1b9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xb4221b9)  

#26 0x121c4e365 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:334  

#27 0x7fffa8ac6e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#28 0x7fffa8aa80cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#29 0x7fffa8aa75b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)

SUMMARY: AddressSanitizer: heap-buffer-overflow view\_model.h:81 in TabStrip::SetSelection(ui::ListSelectionModel const&)  

Shadow bytes around the buggy address:  

0x1c200005a150: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a160: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a170: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a180: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x1c200005a190: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

=>0x1c200005a1a0: fa fa fa fa fa[fa]fa fa 00 00 00 00 00 00 fc fc  

0x1c200005a1b0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x1c200005a1c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a1d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a1e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c200005a1f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

- [poc.html](attachments/poc.html) (text/plain, 176 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 2.6 MB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 2.7 MB)

## Timeline

### [Deleted User] (2021-02-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-02)

Perhaps similar to https://crbug.com/1173269 but a different stack trace. Per the other bug, setting sev-high (not sev-critical) due to interaction required.


[Monorail components: UI>Browser>TabStrip]

### [Deleted User] (2021-02-03)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-02-03)

+Taylor has kindly agreed to help take a look here, as I'm not sure I can address these in a reasonable timeframe.

Taylor, these all look pretty similar to each other and to https://bugs.chromium.org/p/chromium/issues/detail?id=1151799, but with slightly different repros and stack traces. Please feel free to grab some time with me to go over them, or just chat asynchronously.

Thank you!!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb3dde3e0e96f738f88a7a219c716b259baa83be

commit cb3dde3e0e96f738f88a7a219c716b259baa83be
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Feb 04 01:36:46 2021

Fix crash trying to select an already closed tab on header drag completion.

Bug: 1173702
Change-Id: I9a7a668f89f16a89580fb7de61d19d0ae65ec9e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2673164
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/master@{#850395}

[modify] https://crrev.com/cb3dde3e0e96f738f88a7a219c716b259baa83be/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### ch...@gmail.com (2021-02-04)

I verified the fix on Chromium 90.0.4408.0 refs/heads/master@{#850437} on MacOS.

Taylor, thanks for the quick fix!

### tb...@chromium.org (2021-02-05)

Excellent! Glad it all worked out in the end

### [Deleted User] (2021-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-02-16)

Does this change need a merge to stable M88?

### tb...@google.com (2021-02-17)

I believe it does affect stable, and 89. I think these are the labels to add to get security input on whether a merge is needed?

### ch...@gmail.com (2021-02-17)

I think you should add Merge-Request-89 and Merge-Request-88 labels to get the security team's attention. (Please remove Security_Impact-Head label as this bug affects stable).

### ad...@google.com (2021-02-17)

Sheriffbot would add the merge requests automatically now that https://crbug.com/chromium/1173702#c12 has been done - thanks! However, to expedite matters, I'll just go ahead and approve merge to M89 - branch 4389.

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Hi, Khalil. The VRP Panel has decided to award you $7,500 for this report as the vulnerability does not give the attacker great control, but also the user interaction/gesture required is quite high. Thank you for your submission and nice work! 


### ch...@gmail.com (2021-02-18)

Great! It's a nice reward! - Thank you so much!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6308a43c518dcb3c5eb1b0ff4c618c342a510b55

commit 6308a43c518dcb3c5eb1b0ff4c618c342a510b55
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Feb 18 00:58:55 2021

Fix crash trying to select an already closed tab on header drag completion.

(cherry picked from commit cb3dde3e0e96f738f88a7a219c716b259baa83be)

Bug: 1173702
Change-Id: I9a7a668f89f16a89580fb7de61d19d0ae65ec9e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2673164
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#850395}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2702758
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4389@{#1162}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/6308a43c518dcb3c5eb1b0ff4c618c342a510b55/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

Not merging to M88 - no further releases planned.

### as...@google.com (2021-03-01)

Marking as not applicable for LTS since introducing code landed after M86 (same as https://crbug.com/1163845).

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1173702?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054651)*
