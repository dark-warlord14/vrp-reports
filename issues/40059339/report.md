# Security: Heap-use-after-free in remote_cocoa::NativeWidgetNSWindowBridge::SetVisibilityState

| Field | Value |
|-------|-------|
| **Issue ID** | [40059339](https://issues.chromium.org/issues/40059339) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | lg...@chromium.org |
| **Created** | 2022-04-09 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 102.0.4992.0 (Official Build) canary (arm64) and stable  

Operating System: macOS 11.3

**REPRODUCTION CASE**

1. Open Two windows (full enter screen)
2. Try to minimize window A by dragging it and close it
3. On window B, right-click on the top of tab >> Move Tab to Another Window >> untitled and -1 Other tabs
4. UaF occurs

==1044==ERROR: AddressSanitizer: heap-use-after-free on address 0x613000195c00 at pc 0x00011fa90744 bp 0x000305dbf690 sp 0x000305dbf688  

READ of size 4 at 0x613000195c00 thread T0  

#0 0x11fa90743 in remote\_cocoa::NativeWidgetNSWindowBridge::SetVisibilityState(remote\_cocoa::mojom::WindowVisibilityState) native\_widget\_ns\_window\_bridge.mm:775  

#1 0x1239cd482 in views::NativeWidgetMac::Show(ui::WindowShowState, gfx::Rect const&) native\_widget\_mac.mm:571  

#2 0x1238ef8e6 in views::Widget::Show() widget.cc:725  

#3 0x124fd5757 in BrowserView::Show() browser\_view.cc:1210  

#4 0x12451bb75 in chrome::MoveTabsToExistingWindow(Browser\*, Browser\*, std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&) browser\_commands.cc:1000  

#5 0x1245426e2 in chrome::BrowserTabStripModelDelegate::MoveToExistingWindow(std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&, int) browser\_tab\_strip\_model\_delegate.cc:134  

#6 0x1246c60d4 in TabStripModel::ExecuteAddToExistingWindowCommand(int, int) tab\_strip\_model.cc:1640  

#7 0x125539d7c in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) existing\_base\_sub\_menu\_model.cc:45  

#8 0x11a6fffeb in -[MenuControllerCocoa itemSelected:] menu\_controller.mm:327  

#9 0x7fff22e30b0a in -[NSApplication(NSResponder) sendAction:to:from:]+0x11f (AppKit:x86\_64+0x25fb0a) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#10 0x11884514c in \_\_43-[BrowserCrApplication sendAction:to:from:]\_block\_invoke chrome\_browser\_application\_mac.mm:297  

#11 0x119b319a9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe61f9a9) (BuildId: 4c4c44b055553144a1acc4a683c035942400000010000000000b0a0000030c00)  

#12 0x118844ba7 in -[BrowserCrApplication sendAction:to:from:] chrome\_browser\_application\_mac.mm:296  

#13 0x7fff22f33b00 in -[NSMenuItem \_corePerformAction]+0x19c (AppKit:x86\_64+0x362b00) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#14 0x7fff22f3381f in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x5e (AppKit:x86\_64+0x36281f) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#15 0x7fff22f7fdff in -[NSMenu performActionForItemAtIndex:]+0x70 (AppKit:x86\_64+0x3aedff) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#16 0x7fff22f7fd85 in -[NSMenu \_internalPerformActionForItemAtIndex:]+0x51 (AppKit:x86\_64+0x3aed85) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#17 0x7fff22f7fbcc in -[NSCarbonMenuImpl \_carbonCommandProcessEvent:handlerCallRef:]+0x64 (AppKit:x86\_64+0x3aebcc) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#18 0x7fff22f16450 in NSSLMMenuEventHandler+0x435 (AppKit:x86\_64+0x345450) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#19 0x7fff28945dc0 in DispatchEventToHandlers(EventTargetRec\*, OpaqueEventRef\*, HandlerCallRec\*)+0x551 (HIToolbox:x86\_64+0x9dc0) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#20 0x7fff289451e2 in SendEventToEventTargetInternal(OpaqueEventRef\*, OpaqueEventTargetRef\*, HandlerCallRec\*)+0x14a (HIToolbox:x86\_64+0x91e2) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#21 0x7fff2895aa91 in SendEventToEventTarget+0x26 (HIToolbox:x86\_64+0x1ea91) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#22 0x7fff289ba6f6 in SendHICommandEvent(unsigned int, HICommand const\*, unsigned int, unsigned int, unsigned char, void const\*, OpaqueEventTargetRef\*, OpaqueEventTargetRef\*, OpaqueEventRef\*\*)+0x16f (HIToolbox:x86\_64+0x7e6f6) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#23 0x7fff289e02d0 in SendMenuCommandWithContextAndModifiers+0x2c (HIToolbox:x86\_64+0xa42d0) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#24 0x7fff289e027b in SendMenuItemSelectedEvent+0x15b (HIToolbox:x86\_64+0xa427b) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#25 0x7fff289e00ca in FinishMenuSelection(SelectionData\*, MenuResult\*, MenuResult\*)+0x5f (HIToolbox:x86\_64+0xa40ca) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#26 0x7fff28aee2b0 in PopUpMenuSelectCore(MenuData\*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const\*, unsigned short, unsigned int, Rect const\*, Rect const\*, \_\_CFDictionary const\*, \_\_CFString const\*, OpaqueMenuRef\*\*, unsigned short\*)+0x5c3 (HIToolbox:x86\_64+0x1b22b0) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#27 0x7fff28aed7f2 in \_HandlePopUpMenuSelection8(OpaqueMenuRef\*, OpaqueEventRef\*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const\*, unsigned short, Rect const\*, Rect const\*, \_\_CFDictionary const\*, \_\_CFString const\*, OpaqueMenuRef\*\*, unsigned short\*)+0x199 (HIToolbox:x86\_64+0x1b17f2) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#28 0x7fff289c2444 in \_HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86\_64+0x86444) (BuildId: 65d66ff8f36131fd99701798b9d43dbb32000000200000000100000000030b00)  

#29 0x7fff230dd768 in SLMPerformPopUpCarbonMenu+0x8b2 (AppKit:x86\_64+0x50c768) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#30 0x7fff22f79130 in \_NSSLMPopUpCarbonMenu3+0x447 (AppKit:x86\_64+0x3a8130) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#31 0x7fff2301aed4 in -[NSCarbonMenuImpl \_popUpContextMenu:withEvent:forView:withFont:]+0xcf (AppKit:x86\_64+0x449ed4) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#32 0x7fff2301ad5f in -[NSMenu \_popUpContextMenu:withEvent:forView:withFont:]+0xd0 (AppKit:x86\_64+0x449d5f) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#33 0x12367efbc in views::internal::MenuRunnerImplCocoa::RunMenuAt(views::Widget\*, views::MenuButtonController\*, gfx::Rect const&, views::MenuAnchorPosition, int, gfx::NativeView) menu\_runner\_impl\_cocoa.mm:554  

#34 0x12554e816 in BrowserTabStripController::ShowContextMenuForTab(Tab\*, gfx::Point const&, ui::MenuSourceType) browser\_tab\_strip\_controller.cc:420  

#35 0x1236997be in views::ContextMenuController::ShowContextMenuForView(views::View\*, gfx::Point const&, ui::MenuSourceType) context\_menu\_controller.cc:29  

#36 0x1238a2917 in views::View::ProcessMousePressed(ui::MouseEvent const&) view.cc:3062  

#37 0x1238a22b9 in views::View::OnMouseEvent(ui::MouseEvent\*) view.cc:1436  

#38 0x11bee9092 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:139  

#39 0x11bee8942 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:55  

#40 0x1238db6f1 in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) root\_view.cc:418  

#41 0x1238fb657 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1544  

#42 0x12399c9bc in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:912  

#43 0x11fa799db in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:616  

#44 0x7fff22d9aee7 in -[NSWindow(NSEventRouting) \_reallySendEvent:isDelayedEvent:]+0x1951 (AppKit:x86\_64+0x1c9ee7) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#45 0x7fff22d99375 in -[NSWindow(NSEventRouting) sendEvent:]+0x15a (AppKit:x86\_64+0x1c8375) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#46 0x11fa853d4 in -[NativeWidgetMacNSWindow sendEvent:] native\_widget\_mac\_nswindow.mm:298  

#47 0x7fff22d981b4 in -[NSApplication(NSEvent) sendEvent:]+0xb90 (AppKit:x86\_64+0x1c71b4) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#48 0x118846f0c in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:344  

#49 0x119b319a9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe61f9a9) (BuildId: 4c4c44b055553144a1acc4a683c035942400000010000000000b0a0000030c00)  

#50 0x118845f1c in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:321  

#51 0x7fff23070978 in -[NSApplication \_handleEvent:]+0x40 (AppKit:x86\_64+0x49f978) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#52 0x7fff22c0069d in -[NSApplication run]+0x26e (AppKit:x86\_64+0x2f69d) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#53 0x119b45daa in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:744  

#54 0x119b41ab7 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:160  

#55 0x119a5bac5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:498  

#56 0x11998b8dc in base::RunLoop::Run(base::Location const&) run\_loop.cc:141  

#57 0x1103c1762 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:1067  

#58 0x1103c5e31 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:155  

#59 0x1103bafa5 in content::BrowserMain(content::MainFunctionParams) browser\_main.cc:30  

#60 0x118698c7a in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:640  

#61 0x11869ba95 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content\_main\_runner\_impl.cc:1147  

#62 0x11869ad64 in content::ContentMainRunnerImpl::Run() content\_main\_runner\_impl.cc:1019  

#63 0x1186975bd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content\_main.cc:407  

#64 0x118697d2d in content::ContentMain(content::ContentMainParams) content\_main.cc:435  

#65 0x10b516aa1 in ChromeMain chrome\_main.cc:176  

#66 0x100d62b65 in main chrome\_exe\_main\_mac.cc:208  

#67 0x7fff2040df3c in start+0x0 (libdyld.dylib:x86\_64+0x15f3c) (BuildId: 9f95c644d1bd38d996126188fe9ea53c32000000200000000100000000030b00)

0x613000195c00 is located 256 bytes inside of 360-byte region [0x613000195b00,0x613000195c68)  

freed by thread T0 here:  

#0 0x1092b33c9 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x473c9) (BuildId: a8c3db167e2a3af8ac596829a392139a240000001000000000070a0000010b00)  

#1 0x123992145 in views::NativeWidgetMacNSWindowHost::~NativeWidgetMacNSWindowHost() native\_widget\_mac\_ns\_window\_host.mm:287  

#2 0x12399354d in views::NativeWidgetMacNSWindowHost::~NativeWidgetMacNSWindowHost() native\_widget\_mac\_ns\_window\_host.mm:258  

#3 0x1239c9590 in views::NativeWidgetMac::WindowDestroyed() native\_widget\_mac.mm:140  

#4 0x11faa22ab in -[ViewsNSWindowDelegate windowWillClose:] views\_nswindow\_delegate.mm:182  

#5 0x7fff204e0e88 in **CFNOTIFICATIONCENTER\_IS\_CALLING\_OUT\_TO\_AN\_OBSERVER**+0xb (CoreFoundation:x86\_64+0x76e88) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#6 0x7fff2057c847 in \_\_\_CFXRegistrationPost\_block\_invoke+0x30 (CoreFoundation:x86\_64+0x112847) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#7 0x7fff2057c7c4 in \_CFXRegistrationPost+0x1c5 (CoreFoundation:x86\_64+0x1127c4) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#8 0x7fff204b1f23 in \_CFXNotificationPost+0x31a (CoreFoundation:x86\_64+0x47f23) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#9 0x7fff211472c7 in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x3a (Foundation:x86\_64+0x92c7) (BuildId: 5b112edb35c131a7bfdae185d1b49d9332000000200000000100000000030b00)  

#10 0x7fff234c2e5a in -[NSWindow \_finishClosingWindow]+0x7b (AppKit:x86\_64+0x8f1e5a) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#11 0x7fff22f5415f in -[NSWindow \_close]+0x15a (AppKit:x86\_64+0x38315f) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#12 0x11fab0766 in remote\_cocoa::NativeWidgetNSWindowFullscreenController::HandleDeferredClose() native\_widget\_ns\_window\_fullscreen\_controller.mm:319  

#13 0x11fab0351 in remote\_cocoa::NativeWidgetNSWindowFullscreenController::OnWindowDidEnterFullscreen() native\_widget\_ns\_window\_fullscreen\_controller.mm:198  

#14 0x7fff204e0e88 in **CFNOTIFICATIONCENTER\_IS\_CALLING\_OUT\_TO\_AN\_OBSERVER**+0xb (CoreFoundation:x86\_64+0x76e88) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#15 0x7fff2057c847 in \_\_\_CFXRegistrationPost\_block\_invoke+0x30 (CoreFoundation:x86\_64+0x112847) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#16 0x7fff2057c7c4 in \_CFXRegistrationPost+0x1c5 (CoreFoundation:x86\_64+0x1127c4) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#17 0x7fff204b1f23 in \_CFXNotificationPost+0x31a (CoreFoundation:x86\_64+0x47f23) (BuildId: 00f47b8fa02b37bfb57f129cf787f38b32000000200000000100000000030b00)  

#18 0x7fff211472c7 in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x3a (Foundation:x86\_64+0x92c7) (BuildId: 5b112edb35c131a7bfdae185d1b49d9332000000200000000100000000030b00)  

#19 0x7fff237386df in -[NSWindow(NSFullScreen) \_didEnterFullScreen]+0x75 (AppKit:x86\_64+0xb676df) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#20 0x7fff2311b84a in -[\_NSWindowEnterFullScreenTransitionController doAfterEnterFullScreen]+0x109 (AppKit:x86\_64+0x54a84a) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#21 0x7fff23588d0b in -[\_NSEnterFullScreenTransitionController \_performFinalTransitionCleanup]+0x31 (AppKit:x86\_64+0x9b7d0b) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#22 0x7fff23589310 in -[\_NSEnterFullScreenTransitionController \_doSucceededToEnterFullScreen]+0x2db (AppKit:x86\_64+0x9b8310) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#23 0x7fff23589d86 in \_\_65-[\_NSEnterFullScreenTransitionController \_performEnterFullScreen]\_block\_invoke.175+0x17d (AppKit:x86\_64+0x9b8d86) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#24 0x7fff2303ca78 in \_\_NSFullScreenDockConnectionSendCreateForSpace\_block\_invoke+0x54 (AppKit:x86\_64+0x46ba78) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#25 0x7fff2353c1f8 in -[NSDockConnection sendMessage:synchronous:replyHandler:]+0x109 (AppKit:x86\_64+0x96b1f8) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#26 0x7fff2303ca0c in NSFullScreenDockConnectionSendCreateForSpace+0xeb (AppKit:x86\_64+0x46ba0c) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#27 0x7fff2358990e in -[\_NSEnterFullScreenTransitionController \_performEnterFullScreen]+0x406 (AppKit:x86\_64+0x9b890e) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#28 0x7fff2358aa26 in -[\_NSEnterFullScreenTransitionController start]+0x2a1 (AppKit:x86\_64+0x9b9a26) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#29 0x7fff2311c53f in -[\_NSWindowEnterFullScreenTransitionController start]+0x16e (AppKit:x86\_64+0x54b53f) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)

previously allocated by thread T0 here:  

#0 0x1092b3280 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x47280) (BuildId: a8c3db167e2a3af8ac596829a392139a240000001000000000070a0000010b00)  

#1 0x1187c2e57 in operator new(unsigned long) new.cpp:67  

#2 0x123993916 in views::NativeWidgetMacNSWindowHost::CreateInProcessNSWindowBridge(base::scoped\_nsobject<NativeWidgetMacNSWindow>) native\_widget\_mac\_ns\_window\_host.mm:323  

#3 0x1239ca150 in views::NativeWidgetMac::InitNativeWidget(views::Widget::InitParams) native\_widget\_mac.mm:218  

#4 0x1238e7497 in views::Widget::Init(views::Widget::InitParams) widget.cc:391  

#5 0x124e399cc in BrowserFrame::InitBrowserFrame() browser\_frame.cc:124  

#6 0x125005b17 in BrowserWindow::CreateBrowserWindow(std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >, bool, bool) browser\_window\_factory.cc:55  

#7 0x1244c575b in Browser::Browser(Browser::CreateParams const&) browser.cc:535  

#8 0x1244c404b in Browser::Create(Browser::CreateParams const&) browser.cc:449  

#9 0x12558dd6d in TabDragController::CreateBrowserForDrag(TabDragContext\*, gfx::Point const&, gfx::Vector2d\*, std::\_\_1::vector<gfx::Rect, std::\_\_1::allocator[gfx::Rect](javascript:void(0);) >\*) tab\_drag\_controller.cc:2297  

#10 0x125589e84 in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) tab\_drag\_controller.cc:1486  

#11 0x12558920c in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) tab\_drag\_controller.cc:992  

#12 0x125585476 in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:962  

#13 0x12557cfda in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:676  

#14 0x125612ecd in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:225  

#15 0x125617e8b in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:2025  

#16 0x1238a2edd in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:3091  

#17 0x11bee9092 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:139  

#18 0x11bee8942 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:55  

#19 0x1238dc3e4 in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) root\_view.cc:463  

#20 0x1238fb3d9 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1583  

#21 0x12399c9bc in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:912  

#22 0x11fa799db in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:616  

#23 0x11fa76bed in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:298  

#24 0x11fa98506 in non-virtual thunk to remote\_cocoa::NativeWidgetNSWindowBridge::PostCapturedEvent(NSEvent\*) native\_widget\_ns\_window\_bridge.mm:1372  

#25 0x11faac88f in invocation function for block in remote\_cocoa::CocoaMouseCapture::ActiveEventTap::Init() mouse\_capture.mm:93  

#26 0x7fff22d98b5c in \_NSSendEventToObservers+0x14f (AppKit:x86\_64+0x1c7b5c) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#27 0x7fff22d97675 in -[NSApplication(NSEvent) sendEvent:]+0x51 (AppKit:x86\_64+0x1c6675) (BuildId: 10afbc3ae9a43e62b9f597df579b7a8432000000200000000100000000030b00)  

#28 0x118846f0c in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:344  

#29 0x119b319a9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe61f9a9) (BuildId: 4c4c44b055553144a1acc4a683c035942400000010000000000b0a0000030c00)

SUMMARY: AddressSanitizer: heap-use-after-free native\_widget\_ns\_window\_bridge.mm:775 in remote\_cocoa::NativeWidgetNSWindowBridge::SetVisibilityState(remote\_cocoa::mojom::WindowVisibilityState)  

Shadow bytes around the buggy address:  

0x1c2600032b30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032b40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032b60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c2600032b70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x1c2600032b80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x1c2600032b90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032ba0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032bb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032bc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2600032bd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

- [Screen Recording 2022-04-09 at 05.03.33.mp4](attachments/Screen Recording 2022-04-09 at 05.03.33.mp4) (video/mp4, 2.5 MB)
- [Screen Recording 2022-04-09 at 20.35.33.mp4](attachments/Screen Recording 2022-04-09 at 20.35.33.mp4) (video/mp4, 1.2 MB)

## Timeline

### [Deleted User] (2022-04-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-04-09)

This is a little fiddly to reproduce; on macOS 12.3.1 I can’t always get the window into the state that is seen at 0:09 in the video.

Labeling as Sev-High because I do not think web content can cause this series of interactions. If it could, this would be Sev-Critical.

[Monorail components: UI>Browser]

### [Deleted User] (2022-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2022-04-09)

There is another way to get the window into the state that is seen at 0:09 - Drag window A (full enter screen) and at the same time press F3 then drop it.



### cc...@chromium.org (2022-04-22)

lgrey, can you try debugging this?

### rs...@chromium.org (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-23)

lgrey: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b84548853b4695104647f52228918561ca1e0a76

commit b84548853b4695104647f52228918561ca1e0a76
Author: Leonard Grey <lgrey@chromium.org>
Date: Tue Apr 26 18:46:14 2022

Mac: don't make dragged fullscreen tabs re-fullscreen on complete

Most other platforms have opted out of this (but Lacros intends to
return so I'm not just deleting the code), and it's unclear if it was
even intended to work this way on Mac (due to fullscreen/maximize
confusion).

More importantly, some interactions (including Expose) can interact
badly with this behavior and leave phantom Browsers behind when
an affected window closes.

Bug: 727051, 1314908
Change-Id: I0956b0dbc3e6f13c912cf268c970a9b97acb97f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3606650
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996301}

[modify] https://crrev.com/b84548853b4695104647f52228918561ca1e0a76/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### ch...@gmail.com (2022-04-27)

Fixed on 103.0.5028.0 canary.

### lg...@chromium.org (2022-04-27)

Thanks for verifying (and reporting!) :)

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

Requesting merge to extended stable M100 because latest trunk commit (996301) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (996301) appears to be after stable branch point (982481).

Requesting merge to dev M102 because latest trunk commit (996301) appears to be after dev branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-28)

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

### [Deleted User] (2022-04-28)

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

### [Deleted User] (2022-04-28)

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

### lg...@chromium.org (2022-04-28)

1. Why does your merge fit within the merge criteria for these milestones?
"include fixes for important security issues (medium severity or higher)"
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3606650
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Manual verification couldn't hurt. Repro instructions in c#0, made more reliable by replacing step 2 with instructions in c#5

### sr...@google.com (2022-05-02)

Merge approved for M102 branch: pls refer to go/chrome-branches for more info

### am...@chromium.org (2022-05-03)

M101 and M100 merge approved; please merge this this fix to branch 4951 and 4896 NLT EOD Friday, 6 may so this fix can be included in the next Stable and Extended respins. 

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/72b858db22e2353f2c59bb0dcd26aa22582e8dd0

commit 72b858db22e2353f2c59bb0dcd26aa22582e8dd0
Author: Leonard Grey <lgrey@chromium.org>
Date: Tue May 03 14:37:17 2022

[Merge 102] Mac: don't make dragged fullscreen tabs re-fullscreen on complete

Most other platforms have opted out of this (but Lacros intends to
return so I'm not just deleting the code), and it's unclear if it was
even intended to work this way on Mac (due to fullscreen/maximize
confusion).

More importantly, some interactions (including Expose) can interact
badly with this behavior and leave phantom Browsers behind when
an affected window closes.

(cherry picked from commit b84548853b4695104647f52228918561ca1e0a76)

Bug: 727051, 1314908
Change-Id: I0956b0dbc3e6f13c912cf268c970a9b97acb97f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3606650
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#996301}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3621341
Cr-Commit-Position: refs/branch-heads/5005@{#384}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/72b858db22e2353f2c59bb0dcd26aa22582e8dd0/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e216e57e25c531c05ee223d78f190fb88009d669

commit e216e57e25c531c05ee223d78f190fb88009d669
Author: Leonard Grey <lgrey@chromium.org>
Date: Tue May 03 16:42:39 2022

[Merge 100] Mac: don't make dragged fullscreen tabs re-fullscreen on complete

Most other platforms have opted out of this (but Lacros intends to
return so I'm not just deleting the code), and it's unclear if it was
even intended to work this way on Mac (due to fullscreen/maximize
confusion).

More importantly, some interactions (including Expose) can interact
badly with this behavior and leave phantom Browsers behind when
an affected window closes.

(cherry picked from commit b84548853b4695104647f52228918561ca1e0a76)

Bug: 727051, 1314908
Change-Id: I0956b0dbc3e6f13c912cf268c970a9b97acb97f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3606650
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#996301}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3624099
Cr-Commit-Position: refs/branch-heads/4896@{#1218}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/e216e57e25c531c05ee223d78f190fb88009d669/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3df22f945cd065a8de597ebb8a8364b2b3b46d6

commit e3df22f945cd065a8de597ebb8a8364b2b3b46d6
Author: Leonard Grey <lgrey@chromium.org>
Date: Tue May 03 16:43:02 2022

[Merge 101] Mac: don't make dragged fullscreen tabs re-fullscreen on complete

Most other platforms have opted out of this (but Lacros intends to
return so I'm not just deleting the code), and it's unclear if it was
even intended to work this way on Mac (due to fullscreen/maximize
confusion).

More importantly, some interactions (including Expose) can interact
badly with this behavior and leave phantom Browsers behind when
an affected window closes.

(cherry picked from commit b84548853b4695104647f52228918561ca1e0a76)

Bug: 727051, 1314908
Change-Id: I0956b0dbc3e6f13c912cf268c970a9b97acb97f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3606650
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#996301}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3624059
Cr-Commit-Position: refs/branch-heads/4951@{#1153}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/e3df22f945cd065a8de597ebb8a8364b2b3b46d6/chrome/browser/ui/views/tabs/tab_drag_controller.cc


### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Thank you for this report, Khalil. Given that this issue does not appear to be exploitable from the web and the sufficient amount of user interaction required to trigger this issue, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-13)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1314908?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059339)*
