# Security: Use-After-Free in PasswordManagerPorter::FileSelectionCanceled

| Field | Value |
|-------|-------|
| **Issue ID** | [40071324](https://issues.chromium.org/issues/40071324) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Mac |
| **Reporter** | pw...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2023-09-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-After-Free in PasswordManagerPorter closing

==24125==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000a94728 at pc 0x00011ef66168 bp 0x00016f93fbd0 sp 0x00016f93fbc8  

READ of size 8 at 0x606000a94728 thread T0  

==24125==WARNING: invalid path to external symbolizer!  

==24125==WARNING: Failed to use and restart external symbolizer!  

#0 0x11ef66164 in PasswordManagerPorter::FileSelectionCanceled(void\*)+0x3b0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b12164)  

#1 0x1380cb114 in ui::SelectFileDialogImpl::~SelectFileDialogImpl()+0x114 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libui\_shell\_dialogs.dylib:arm64+0xb114)  

#2 0x1380cb210 in ui::SelectFileDialogImpl::~SelectFileDialogImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libui\_shell\_dialogs.dylib:arm64+0xb210)  

#3 0x11ef63608 in PasswordManagerPorter::~PasswordManagerPorter()+0x15c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b0f608)  

#4 0x11ef63760 in PasswordManagerPorter::~PasswordManagerPorter()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b0f760)  

#5 0x11d658268 in extensions::PasswordsPrivateDelegateImpl::~PasswordsPrivateDelegateImpl()+0x498 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x6204268)  

#6 0x11d65850c in extensions::PasswordsPrivateDelegateImpl::~PasswordsPrivateDelegateImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x620450c)  

#7 0x11f55bc34 in PasswordManagerUI::~PasswordManagerUI()+0x12c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x8107c34)  

#8 0x10f6520c4 in content::WebUIImpl::~WebUIImpl()+0x140 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x29760c4)  

#9 0x10f6524f8 in content::WebUIImpl::~WebUIImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x29764f8)  

#10 0x10eec0d38 in content::RenderFrameHostManager::ClearWebUIInstances()+0x30 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x21e4d38)  

#11 0x10eaa952c in content::FrameTree::Shutdown()+0x2a8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1dcd52c)  

#12 0x10f4817ac in content::WebContentsImpl::~WebContentsImpl()+0x99c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a57ac)  

#13 0x10f484768 in content::WebContentsImpl::~WebContentsImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a8768)  

#14 0x11f386624 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*)+0x744 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f32624)  

#15 0x11f38f558 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int)+0xba8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3b558)  

#16 0x11f38e614 in TabStripModel::CloseAllTabs()+0x3a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3a614)  

#17 0x11f3f9ab8 in UnloadController::ProcessPendingTabs(bool)+0x620 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa5ab8)  

#18 0x11f3f80d8 in UnloadController::ClearUnloadState(content::WebContents\*, bool)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa40d8)  

#19 0x11f3f7e18 in UnloadController::CanCloseContents(content::WebContents\*)+0x5c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa3e18)  

#20 0x11f1ab768 in non-virtual thunk to Browser::CloseContents(content::WebContents\*)+0x18 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7d57768)  

#21 0x10f504f84 in content::WebContentsImpl::Close()+0x1a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2828f84)  

#22 0x10ee85aec in void base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, void ()>::RunImpl<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, 0ul, 1ul>(void (content::RenderFrameHostImpl::\*&&)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>)+0x1a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x21a9aec)  

#23 0x13306557c in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*)+0x12c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libblink\_common.dylib:arm64+0x58557c)  

#24 0x101e82aa8 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xae4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x22aa8)  

#25 0x101e97884 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x370 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x37884)  

#26 0x101e87200 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x158 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x27200)  

#27 0x103a4be94 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x374 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x3fe94)  

#28 0x103a43a20 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x37a20)  

#29 0x102325ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#30 0x102385c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)  

#31 0x102384fc8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x224fc8)  

#32 0x1024ee514 in base::MessagePumpCFRunLoopBase::RunWork()+0x1f8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38e514)  

#33 0x1024daef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#34 0x1024ec328 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38c328)  

#35 0x19eff6638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638)  

#36 0x222d80019eff65cc (<unknown module>)  

#37 0x163d80019eff633c (<unknown module>)  

#38 0x937380019eff4f44 (<unknown module>)  

#39 0xff6c80019eff44b4 (<unknown module>)  

#40 0x5a2d8001a883ec3c (<unknown module>)  

#41 0xee070001a883ea78 (<unknown module>)  

#42 0xf53b8001a883e7d0 (<unknown module>)  

#43 0x907b0001a2215d40 (<unknown module>)  

#44 0x68678001a2214edc (<unknown module>)  

#45 0xc76e800119c59f9c (<unknown module>)  

#46 0x1024daef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#47 0x119c59b1c in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x2b8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x2805b1c)  

#48 0x1a2209340 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2c340)  

#49 0xc62d8001024f0914 (<unknown module>)  

#50 0x1024eae20 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*)+0x2a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38ae20)  

#51 0x102387a50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x36c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x227a50)  

#52 0x1022a4ad4 in base::RunLoop::Run(base::Location const&)+0x4cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x144ad4)  

#53 0x10db398d4 in content::BrowserMainLoop::RunMainMessageLoop()+0x264 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe5d8d4)  

#54 0x10db401d0 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe641d0)  

#55 0x10db3240c in content::BrowserMain(content::MainFunctionParams)+0x1c8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0xe5640c)  

#56 0x110373678 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*)+0x210 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3697678)  

#57 0x1103763e4 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x3a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x369a3e4)  

#58 0x110375d34 in content::ContentMainRunnerImpl::Run()+0x624 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3699d34)  

#59 0x110370f54 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*)+0x6a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3694f54)  

#60 0x110371ba0 in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x3695ba0)  

#61 0x11745e55c in ChromeMain+0x34c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xa55c)  

#62 0x1004bcbb4 in main+0x22c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb4)  

#63 0x19ebbff24 (<unknown module>)  

#64 0x982c7ffffffffffc (<unknown module>)

0x606000a94728 is located 8 bytes inside of 56-byte region [0x606000a94720,0x606000a94758)  

freed by thread T0 here:  

#0 0x100ce2a70 in \_\_sanitizer\_finish\_switch\_fiber+0xb4c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5ea70)  

#1 0x1021a8950 in base::internal::BindStateHolder::~BindStateHolder()+0x7c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x48950)  

#2 0x11ef63510 in PasswordManagerPorter::~PasswordManagerPorter()+0x64 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b0f510)  

#3 0x11ef63760 in PasswordManagerPorter::~PasswordManagerPorter()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b0f760)  

#4 0x11d658268 in extensions::PasswordsPrivateDelegateImpl::~PasswordsPrivateDelegateImpl()+0x498 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x6204268)  

#5 0x11d65850c in extensions::PasswordsPrivateDelegateImpl::~PasswordsPrivateDelegateImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x620450c)  

#6 0x11f55bc34 in PasswordManagerUI::~PasswordManagerUI()+0x12c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x8107c34)  

#7 0x10f6520c4 in content::WebUIImpl::~WebUIImpl()+0x140 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x29760c4)  

#8 0x10f6524f8 in content::WebUIImpl::~WebUIImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x29764f8)  

#9 0x10eec0d38 in content::RenderFrameHostManager::ClearWebUIInstances()+0x30 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x21e4d38)  

#10 0x10eaa952c in content::FrameTree::Shutdown()+0x2a8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x1dcd52c)  

#11 0x10f4817ac in content::WebContentsImpl::~WebContentsImpl()+0x99c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a57ac)  

#12 0x10f484768 in content::WebContentsImpl::~WebContentsImpl()+0x8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x27a8768)  

#13 0x11f386624 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*)+0x744 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f32624)  

#14 0x11f38f558 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int)+0xba8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3b558)  

#15 0x11f38e614 in TabStripModel::CloseAllTabs()+0x3a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7f3a614)  

#16 0x11f3f9ab8 in UnloadController::ProcessPendingTabs(bool)+0x620 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa5ab8)  

#17 0x11f3f80d8 in UnloadController::ClearUnloadState(content::WebContents\*, bool)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa40d8)  

#18 0x11f3f7e18 in UnloadController::CanCloseContents(content::WebContents\*)+0x5c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7fa3e18)  

#19 0x11f1ab768 in non-virtual thunk to Browser::CloseContents(content::WebContents\*)+0x18 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7d57768)  

#20 0x10f504f84 in content::WebContentsImpl::Close()+0x1a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x2828f84)  

#21 0x10ee85aec in void base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, void ()>::RunImpl<void (content::RenderFrameHostImpl::\*)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>, 0ul, 1ul>(void (content::RenderFrameHostImpl::\*&&)(content::RenderFrameHostImpl::ClosePageSource), std::\_\_Cr::tuple<base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), content::RenderFrameHostImpl::ClosePageSource>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul>)+0x1a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libcontent.dylib:arm64+0x21a9aec)  

#22 0x13306557c in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*)+0x12c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libblink\_common.dylib:arm64+0x58557c)  

#23 0x101e82aa8 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0xae4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x22aa8)  

#24 0x101e97884 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x370 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x37884)  

#25 0x101e87200 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x158 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x27200)  

#26 0x103a4be94 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x374 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x3fe94)  

#27 0x103a43a20 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x37a20)  

#28 0x102325ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#29 0x102385c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)

previously allocated by thread T0 here:  

#0 0x100ce2650 in \_\_sanitizer\_finish\_switch\_fiber+0x72c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/Chromium.app/Contents/MacOS/libclang\_rt.asan\_osx\_dynamic.dylib:arm64+0x5e650)  

#1 0x11d662d40 in base::OnceCallback<void (password\_manager::ImportResults const&)> base::OnceCallback<extensions::api::passwords\_private::ImportResults (password\_manager::ImportResults const&)>::Then<void, extensions::api::passwords\_private::ImportResults const&>(base::OnceCallback<void (extensions::api::passwords\_private::ImportResults const&)>) &&+0x10c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x620ed40)  

#2 0x11d6623f0 in extensions::PasswordsPrivateDelegateImpl::ImportPasswords(extensions::api::passwords\_private::PasswordStoreSet, base::OnceCallback<void (extensions::api::passwords\_private::ImportResults const&)>, content::WebContents\*)+0x2f0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x620e3f0)  

#3 0x11db48114 in extensions::PasswordsPrivateImportPasswordsFunction::Run()+0x350 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x66f4114)  

#4 0x1181d7554 in ExtensionFunction::RunWithValidation()+0x1a0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xd83554)  

#5 0x1181e650c in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0xd48 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xd9250c)  

#6 0x1181e4738 in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), content::RenderFrameHost&, base::OnceCallback<void (bool, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0x640 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xd90738)  

#7 0x1181d38d8 in extensions::ExtensionFrameHost::Request(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), base::OnceCallback<void (bool, base::Value::List, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, mojo::StructPtr[extensions::mojom::ExtraResponseData](javascript:void(0);))>)+0x210 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0xd7f8d8)  

#8 0x1176d5684 in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost\*, mojo::Message\*, std::\_\_Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>)+0x7c0 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x281684)  

#9 0x101e827c0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)+0x7fc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x227c0)  

#10 0x101e977a0 in mojo::MessageDispatcher::Accept(mojo::Message\*)+0x28c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x377a0)  

#11 0x101e87200 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*)+0x158 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_cpp\_bindings.dylib:arm64+0x27200)  

#12 0x103a4be94 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x374 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x3fe94)  

#13 0x103a43a20 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*)+0x16c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x37a20)  

#14 0x102325ff8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x398 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x1c5ff8)  

#15 0x102385c50 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*)+0x8a4 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x225c50)  

#16 0x102384fc8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x154 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x224fc8)  

#17 0x1024ee514 in base::MessagePumpCFRunLoopBase::RunWork()+0x1f8 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38e514)  

#18 0x1024daef0 in base::apple::CallWithEHFrame(void () block\_pointer)+0xc (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x37aef0)  

#19 0x1024ec328 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*)+0x13c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libbase.dylib:arm64+0x38c328)  

#20 0x19eff6638 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7f638)  

#21 0x222d80019eff65cc (<unknown module>)  

#22 0x163d80019eff633c (<unknown module>)  

#23 0x937380019eff4f44 (<unknown module>)  

#24 0xff6c80019eff44b4 (<unknown module>)  

#25 0x5a2d8001a883ec3c (<unknown module>)  

#26 0xee070001a883ea78 (<unknown module>)  

#27 0xf53b8001a883e7d0 (<unknown module>)  

#28 0x907b0001a2215d40 (<unknown module>)  

#29 0x68678001a2214edc (<unknown module>)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libchrome\_dll.dylib:arm64+0x7b12164) in PasswordManagerPorter::FileSelectionCanceled(void\*)+0x3b0  

Shadow bytes around the buggy address:  

0x606000a94480: fa fa fa fa fa fa fa fa fa fa f7 fa fa fa fa fa  

0x606000a94500: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x606000a94580: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa  

0x606000a94600: fd fd fd fd fd fd fd fd fa fa f7 fa fa fa fa fa  

0x606000a94680: fa fa fa fa fa fa f7 fa fa fa fa fa fa fa fa fa  

=>0x606000a94700: fa fa f7 fa fd[fd]fd fd fd fd fd fa fa fa f7 fa  

0x606000a94780: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd  

0x606000a94800: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x606000a94880: fa fa f7 fa fa fa fa fa fa fa fa fa fa fa f7 fa  

0x606000a94900: fd fd fd fd fd fd fd fa fa fa f7 fa fa fa fa fa  

0x606000a94980: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00  

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

==24125==ADDITIONAL INFO

==24125==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x103a41e88 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*)+0xc60 (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libipc.dylib:arm64+0x35e88)  

#1 0x101f7a984 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x29c (/Users/sprout/Desktop/pwn2car/chromium/src/out/asan-nodcheck/libmojo\_public\_system\_cpp.dylib:arm64+0x1a984)

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==24125==END OF ADDITIONAL INFO  

==24125==ABORTING  

Received signal 6  

[0x0001024c9f38]  

[0x000102482810]  

[0x0001024c99d4]  

[0x00019ef46a24]  

[0x00019ef17c28]  

[0x00019ee25ae8]  

[0x000100cf8a1c]  

[0x000100cf8188]  

[0x000100cdbd10]  

[0x000100cdb05c]  

[0x000100cdc318]  

[0x00011ef66168]  

[0x0001380cb118]  

[0x0001380cb214]  

[0x00011ef6360c]  

[0x00011ef63764]  

[0x00011d65826c]  

[0x00011d658510]  

[0x00011f55bc38]  

[0x00010f6520c8]  

[0x00010f6524fc]  

[0x00010eec0d3c]  

[0x00010eaa9530]  

[0x00010f4817b0]  

[0x00010f48476c]  

[0x00011f386628]  

[0x00011f38f55c]  

[0x00011f38e618]  

[0x00011f3f9abc]  

[0x00011f3f80dc]  

[0x00011f3f7e1c]  

[0x00011f1ab76c]  

[0x00010f504f88]  

[0x00010ee85af0]  

[0x000133065580]  

[0x000101e82aac]  

[0x000101e97888]  

[0x000101e87204]  

[0x000103a4be98]  

[0x000103a43a24]  

[0x000102325ffc]  

[0x000102385c54]  

[0x000102384fcc]  

[0x0001024ee518]  

[0x0001024daef4]  

[0x0001024ec32c]  

[0x00019eff663c]  

[0x00019eff65d0]  

[0x00019eff6340]  

[0x00019eff4f48]  

[0x00019eff44b8]  

[0x0001a883ec40]  

[0x0001a883ea7c]  

[0x0001a883e7d4]  

[0x0001a2215d44]  

[0x0001a2214ee0]  

[0x000119c59fa0]  

[0x0001024daef4]  

[0x000119c59b20]  

[0x0001a2209344]  

[0x0001024f0918]  

[0x0001024eae24]  

[0x000102387a54]  

[0x0001022a4ad8]  

[0x00010db398d8]  

[0x00010db401d4]  

[0x00010db32410]  

[0x00011037367c]  

[0x0001103763e8]  

[0x000110375d38]  

[0x000110370f58]  

[0x000110371ba4]  

[0x00011745e560]  

[0x0001004bcbb8]  

[0x00019ebbff28]  

[end of stack trace]  

[0904/190547.218748:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x100508000, 0x8000): (os/kern) invalid address (1)  

[0904/190547.219551:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x100508000, 0x8000): (os/kern) invalid address (1)  

[0904/190547.222343:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x100508000, 0x8000): (os/kern) invalid address (1)  

[0904/190547.222744:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x100508000, 0x8000): (os/kern) invalid address (1)  

[0904/190547.225962:WARNING:process\_memory\_mac.cc(93)] mach\_vm\_read(0x100508000, 0x8000): (os/kern) invalid address (1)  

[0904/190547.307363:ERROR:bootstrap.cc(65)] bootstrap\_look\_up com.apple.ReportCrash: Unknown service name (1102)

**VERSION**  

Chrome Version: Browser::TryToCloseWindow  

Operating System: MacOS 13.4.1 (c) (22F770820d)

**REPRODUCTION CASE**

1. Launch Chrome
2. Go Password Manager - Settings - Import passwords
3. When dialog opened, Press Command(Ctrl) + Q

**CREDIT INFORMATION**  

Reporter credit: [pwn2car]

## Attachments

- [PW-UAF.asan.log](attachments/PW-UAF.asan.log) (text/plain, 27.8 KB)
- [PW-UAF.mov](attachments/PW-UAF.mov) (video/quicktime, 7.2 MB)

## Timeline

### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

Thank you for the report. 
Sev-High, for browser process UAF mitigated by user interaction / Pri-1.
I was easily and reliably able to reproduce this on Mac Canary/118 (118.0.5991.0) to Stable/116, setting FoundIn-116. 
I was not able to reproduce this on Linux, so keeping OS set to just Mac for now. 
Assigning to natiahlyi@ based on past and ongoing work in password manager porter interface, cc'ing others from password manager experience team 


[Monorail components: UI>Browser>Passwords]

### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-09-06)

(I am a bot: this is an auto-cc on a security bug)

### ar...@google.com (2023-09-15)

@natiahlyi: Gentle ping from the secondary security shepherd. 

### na...@google.com (2023-09-15)

[Empty comment from Monorail migration]

### na...@google.com (2023-09-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9dea1181c3af5209ba02fadf8e1a229b33b2ca6b

commit 9dea1181c3af5209ba02fadf8e1a229b33b2ca6b
Author: Andrii Natiahlyi <natiahlyi@google.com>
Date: Mon Sep 18 13:41:17 2023

Fix PasswordManagerPorter is called after destruction

Fixed: 1478889
Change-Id: I3acbf5dea56ea16a23a5799c241ca9aeb7ff091a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4872120
Auto-Submit: Andrii Natiahlyi <natiahlyi@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Andrii Natiahlyi <natiahlyi@google.com>
Cr-Commit-Position: refs/heads/main@{#1197799}

[modify] https://crrev.com/9dea1181c3af5209ba02fadf8e1a229b33b2ca6b/chrome/browser/ui/passwords/settings/password_manager_porter.cc


### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

Requesting merge to extended stable M116 because latest trunk commit (1197799) appears to be after extended stable branch point (1160321).

Requesting merge to stable M117 because latest trunk commit (1197799) appears to be after stable branch point (1181205).

Requesting merge to beta M118 because latest trunk commit (1197799) appears to be after beta branch point (1192594).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-19)

Merge review required: M118 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-19)

Merge review required: M117 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-19)

Merge review required: M116 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-20)

M118 merge approved for https://crrev.com/c/4872120, please merge this fix to branch 5993 at your earliest convenience 

M117 and M116 merges approved for https://crrev.com/c/4872120, please merge this fix to M117 Stable/branch 5938 and M116 Extended / branch 5845 by EOD tomorrow (Thursday 21 September) so this fix can be included in the next M117 Stable and M116 Extended Stable security updates next week. 

### gi...@appspot.gserviceaccount.com (2023-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9184e015c41be2faca84ef412d727abd618142fa

commit 9184e015c41be2faca84ef412d727abd618142fa
Author: Andrii Natiahlyi <natiahlyi@google.com>
Date: Thu Sep 21 11:08:27 2023

[M118] Fix PasswordManagerPorter is called after destruction

(cherry picked from commit 9dea1181c3af5209ba02fadf8e1a229b33b2ca6b)

Fixed: 1478889
Change-Id: I3acbf5dea56ea16a23a5799c241ca9aeb7ff091a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4872120
Auto-Submit: Andrii Natiahlyi <natiahlyi@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Andrii Natiahlyi <natiahlyi@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1197799}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4882458
Cr-Commit-Position: refs/branch-heads/5993@{#614}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/9184e015c41be2faca84ef412d727abd618142fa/chrome/browser/ui/passwords/settings/password_manager_porter.cc


### gi...@appspot.gserviceaccount.com (2023-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca326311c5d7f45b71a416364e15d3655204cf29

commit ca326311c5d7f45b71a416364e15d3655204cf29
Author: Andrii Natiahlyi <natiahlyi@google.com>
Date: Thu Sep 21 11:09:36 2023

[M117] Fix PasswordManagerPorter is called after destruction

(cherry picked from commit 9dea1181c3af5209ba02fadf8e1a229b33b2ca6b)

Fixed: 1478889
Change-Id: I3acbf5dea56ea16a23a5799c241ca9aeb7ff091a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4872120
Auto-Submit: Andrii Natiahlyi <natiahlyi@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Andrii Natiahlyi <natiahlyi@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1197799}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4882598
Cr-Commit-Position: refs/branch-heads/5938@{#1364}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/ca326311c5d7f45b71a416364e15d3655204cf29/chrome/browser/ui/passwords/settings/password_manager_porter.cc


### gi...@appspot.gserviceaccount.com (2023-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9998ceadc93a8e75c57fee448c485f36f65e8404

commit 9998ceadc93a8e75c57fee448c485f36f65e8404
Author: Andrii Natiahlyi <natiahlyi@google.com>
Date: Thu Sep 21 12:26:26 2023

[M116] Fix PasswordManagerPorter is called after destruction

(cherry picked from commit 9dea1181c3af5209ba02fadf8e1a229b33b2ca6b)

Fixed: 1478889
Change-Id: I3acbf5dea56ea16a23a5799c241ca9aeb7ff091a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4872120
Auto-Submit: Andrii Natiahlyi <natiahlyi@google.com>
Commit-Queue: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Commit-Queue: Andrii Natiahlyi <natiahlyi@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1197799}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4882617
Cr-Commit-Position: refs/branch-heads/5845@{#1834}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/9998ceadc93a8e75c57fee448c485f36f65e8404/chrome/browser/ui/passwords/settings/password_manager_porter.cc


### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-26)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-09-28)

FYI, I applied the same fix to other file dialog users in https://crrev.com/c/4900261

### pg...@google.com (2023-09-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations pwn2car! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug in the browser process. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### na...@google.com (2023-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### pw...@gmail.com (2024-01-17)

Hello,

When can I expect to receive the reward?

### am...@chromium.org (2024-01-18)

Hello, payments are handled by the p2p-vrp finance team. According to https://crbug.com/chromium/1478889#c26, the reward information was forwarded to them for processing on 29 September and should have been long since paid out by now. According to our automation, you were rewarded for this issue and https://crbug.com/chromium/1483194, so this would have been processed together as a $4000 payment for both issues. If you have not received this payment back in October 2023, please reach out to p2p-vrp@google.com as soon as possible for an update or to have this issue rectified. 

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1478889?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1483678]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071324)*
