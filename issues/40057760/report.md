# Security: Heap-use-after-free in sharing_hub::SharingHubBubbleController::~SharingHubBubbleController

| Field | Value |
|-------|-------|
| **Issue ID** | [40057760](https://issues.chromium.org/issues/40057760) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2021-10-29 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version: 97.0.4685.0 refs/heads/main@{#936123}  

Operating System: Ozone X11

**REPRODUCTION CASE**

1. Launch Chromium
2. Click on 'Sharesheet' icon and select "Nearby Share"
3. Open a new tab and click on 'Sharesheet' icon
4. Close the first tab
5. Close the second tab

=================================================================  

==37079==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000434ab0 at pc 0x5605252144b0 bp 0x7ffc1407b610 sp 0x7ffc1407b608  

READ of size 8 at 0x602000434ab0 thread T0 (chrome)  

2021-10-29T01:13:41.225085Z ERROR chrome[37079:37155]: [object\_proxy.cc(642)] Failed to call method: org.chromium.debugd.GetPerfOutputFd: object\_path= /org/chromium/debugd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.debugd was not provided by any .service files  

#0 0x5605252144af in sharing\_hub::SharingHubBubbleController::~SharingHubBubbleController() chrome/browser/ui/sharing\_hub/sharing\_hub\_bubble\_controller.cc:81:29  

#1 0x5605252144c5 in sharing\_hub::SharingHubBubbleController::~SharingHubBubbleController() chrome/browser/ui/sharing\_hub/sharing\_hub\_bubble\_controller.cc:73:59  

#2 0x560516d943ad in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#3 0x560516d943ad in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#4 0x560516d943ad in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#5 0x560516d943ad in ~pair buildtools/third\_party/libc++/trunk/include/utility:394:29  

#6 0x560516d943ad in destroy<std::\_\_1::pair<const void \*const, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:318:15  

#7 0x560516d943ad in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1801:9  

#8 0x560516d94361 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:9  

#9 0x560516d94361 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:9  

#10 0x560516d94341 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1798:9  

#11 0x560516d94361 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:9  

#12 0x560516d94361 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:9  

#13 0x560516d94361 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::\_\_map\_value\_compare<void const\*, std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, std::\_\_1::less<void const\*>, true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void const\*, std::\_\_1::unique\_ptr<base::SupportsUserData::Data, std::\_\_1::default\_delete[base::SupportsUserData::Data](javascript:void(0);) > >, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:9  

#14 0x560516d94067 in ~\_\_tree buildtools/third\_party/libc++/trunk/include/\_\_tree:1789:3  

#15 0x560516d94067 in ~map buildtools/third\_party/libc++/trunk/include/map:1103:5  

#16 0x560516d94067 in base::SupportsUserData::~SupportsUserData() base/supports\_user\_data.cc:71:1  

#17 0x56050c60d233 in ~WebContents content/public/browser/web\_contents.h:316:28  

#18 0x56050c60d233 in content::WebContentsImpl::~WebContentsImpl() content/browser/web\_contents/web\_contents\_impl.cc:1066:1  

#19 0x56050c60e7f5 in content::WebContentsImpl::~WebContentsImpl() content/browser/web\_contents/web\_contents\_impl.cc:968:37  

#20 0x5605247520c3 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#21 0x5605247520c3 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#22 0x5605247520c3 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) chrome/browser/ui/tabs/tab\_strip\_model.cc:555:27  

#23 0x560524757ab6 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab\_strip\_model.cc:1797:5  

#24 0x56052475843a in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab\_strip\_model.cc:766:10  

#25 0x560525760803 in BrowserTabStripController::CloseTab(int) chrome/browser/ui/views/tabs/browser\_tab\_strip\_controller.cc:371:11  

#26 0x5605257b7a45 in TabStrip::CloseTabInternal(int, CloseTabSource) chrome/browser/ui/views/tabs/tab\_strip.cc:3069:16  

#27 0x5605257b7587 in TabStrip::CloseTab(Tab\*, CloseTabSource) chrome/browser/ui/views/tabs/tab\_strip.cc:1983:3  

#28 0x56052577387f in Tab::CloseButtonPressed(ui::Event const&) chrome/browser/ui/views/tabs/tab.cc:1073:16  

#29 0x56051f8eb33a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ui/views/controls/button/button.cc:66:13  

#30 0x56051f8f3126 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button\_controller.cc  

#31 0x56051f8ba261 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ui/events/scoped\_target\_handler.cc:28:24  

#32 0x56051a72049b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:191:12  

#33 0x56051a71f684 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#34 0x56051a71f14c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14  

#35 0x56051a71eeb9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#36 0x56051fa81c4f in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root\_view.cc:485:9  

#37 0x56051fa9a504 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc:1541:20  

#38 0x56051faef172 in views::NativeWidgetAura::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/native\_widget\_aura.cc  

#39 0x56051a72049b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:191:12  

#40 0x56051a71f684 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#41 0x56051a71f14c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14  

#42 0x56051a71eeb9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#43 0x56051dd0ead3 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17  

#44 0x56051a724548 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:117:16  

#45 0x56051a724a01 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:65:14  

#46 0x56050e450fe6 in ui::EventRewriterChromeOS::RewriteMouseButtonEvent(ui::MouseEvent const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:1258:12  

#47 0x56050e451498 in ui::EventRewriterChromeOS::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ui/chromeos/events/event\_rewriter\_chromeos.cc:768:12  

#48 0x56051a7249a7 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:32  

#49 0x5605227aed17 in ash::KeyboardDrivenEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/events/keyboard\_driven\_event\_rewriter.cc:31:12  

#50 0x56051a7249a7 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:32  

#51 0x5605227aac25 in ash::AccessibilityEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) base/memory/weak\_ptr.h  

#52 0x56051a7249a7 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:32  

#53 0x56052257fd65 in ash::AutoclickDragEventRewriter::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/autoclick/autoclick\_drag\_event\_rewriter.cc  

#54 0x56051a7249a7 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const\*) ui/events/event\_source.cc:66:32  

#55 0x56052255d523 in ash::FullscreenMagnifierController::RewriteEvent(ui::Event const&, base::WeakPtr[ui::EventRewriterContinuation](javascript:void(0);)) ash/accessibility/magnifier/fullscreen\_magnifier\_controller.cc  

#56 0x56051a724203 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:143:29  

#57 0x5605227ecdef in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:252:38  

#58 0x5605227f44fa in ash::AshWindowTreeHostPlatform::DispatchEvent(ui::Event\*) ash/host/ash\_window\_tree\_host\_platform.cc:184:40  

#59 0x56051a72f497 in base::OnceCallback<void (ui::Event\*)>::Run(ui::Event\*) && base/callback.h:142:12  

#60 0x56051a72ef70 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:36:25  

#61 0x56051bd2ddd3 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/platform\_window/x11/x11\_window.cc:1283:3  

#62 0x56051bd2d592 in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc:1236:3  

#63 0x56051bd2e11e in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/platform\_window/x11/x11\_window.cc  

#64 0x560518a8ac78 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:98:29  

#65 0x56051a86f94f in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:287:5  

#66 0x560506ee05b6 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14  

#67 0x560506ee026c in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:520:3  

#68 0x560506edfb4e in x11::Connection::Dispatch() ui/gfx/x/connection.cc  

#69 0x560506ee03d9 in x11::Connection::DispatchAll() ui/gfx/x/connection.cc:457:12  

#70 0x56051704a3ea in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) base/message\_loop/message\_pump\_libevent.cc  

#71 0x5605173d3cb4 in event\_process\_active base/third\_party/libevent/event.c:381:4  

#72 0x5605173d3cb4 in event\_base\_loop base/third\_party/libevent/event.c:521:4  

#73 0x56051704aeb2 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:251:5  

#74 0x560516e0dde6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#75 0x560516d1a35e in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:140:14  

#76 0x56050b3c1db1 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1005:18  

#77 0x56050b3c7237 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:152:15  

#78 0x56050b3bba1a in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser\_main.cc:49:28  

#79 0x560516a8c8e7 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:641:10  

#80 0x560516a8f171 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content\_main\_runner\_impl.cc:1137:10  

#81 0x560516a8e470 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:1004:12  

#82 0x560516a890bb in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content/app/content\_main.cc:390:36  

#83 0x560516a89577 in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:418:10  

#84 0x560505eda68b in ChromeMain chrome/app/chrome\_main.cc:172:12  

#85 0x7fc0d4e350b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x602000434ab0 is located 0 bytes inside of 16-byte region [0x602000434ab0,0x602000434ac0)  

freed by thread T0 (chrome) here:  

#0 0x560505ed86ed in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x560519509590 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x560519509590 in std::\_\_1::unique\_ptr<sharesheet::SharesheetServiceDelegator, std::\_\_1::default\_delete[sharesheet::SharesheetServiceDelegator](javascript:void(0);) >::reset(sharesheet::SharesheetServiceDelegator\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x5605195094ac in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#4 0x5605195094ac in destroy buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:133:15  

#5 0x5605195094ac in destroy<std::\_\_1::unique\_ptr<sharesheet::SharesheetServiceDelegator, std::\_\_1::default\_delete[sharesheet::SharesheetServiceDelegator](javascript:void(0);) >, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:308:13  

#6 0x5605195094ac in \_\_destruct\_at\_end buildtools/third\_party/libc++/trunk/include/vector:429:9  

#7 0x5605195094ac in std::\_\_1::vector<std::\_\_1::unique\_ptr<sharesheet::SharesheetServiceDelegator, std::\_\_1::default\_delete[sharesheet::SharesheetServiceDelegator](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<sharesheet::SharesheetServiceDelegator, std::\_\_1::default\_delete[sharesheet::SharesheetServiceDelegator](javascript:void(0);) > > >::\_\_destruct\_at\_end(std::\_\_1::unique\_ptr<sharesheet::SharesheetServiceDelegator, std::\_\_1::default\_delete[sharesheet::SharesheetServiceDelegator](javascript:void(0);) >\*) buildtools/third\_party/libc++/trunk/include/vector:836:17  

#8 0x5605195047ee in erase buildtools/third\_party/libc++/trunk/include/vector:1719:11  

#9 0x5605195047ee in sharesheet::SharesheetService::OnBubbleClosed(aura::Window\*, std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&) chrome/browser/sharesheet/sharesheet\_service.cc:125:26  

#10 0x56051950efa9 in sharesheet::SharesheetServiceDelegator::OnBubbleClosed(std::\_\_1::basic\_string<char16\_t, std::\_\_1::char\_traits<char16\_t>, std::\_\_1::allocator<char16\_t> > const&) chrome/browser/sharesheet/sharesheet\_service\_delegator.cc:101:24  

#11 0x560506ee3157 in base::OnceCallback<void ()>::Run() && base/callback.h:142:12  

#12 0x560524d61be9 in ui::ClosureAnimationObserver::OnImplicitAnimationsCompleted() ui/compositor/closure\_animation\_observer.cc:18:23  

#13 0x56051dda2d86 in CheckCompleted ui/compositor/layer\_animation\_observer.cc:128:5  

#14 0x56051dda2d86 in ui::ImplicitAnimationObserver::OnDetachedFromSequence(ui::LayerAnimationSequence\*) ui/compositor/layer\_animation\_observer.cc:122:3  

#15 0x56051dda1ba2 in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence\*, bool) ui/compositor/layer\_animation\_observer.cc:55:5  

#16 0x56051dda21fa in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence\*) ui/compositor/layer\_animation\_observer.cc:89:13  

#17 0x56051dda66d6 in ui::LayerAnimationSequence::NotifyEnded() ui/compositor/layer\_animation\_sequence.cc:289:14  

#18 0x56051dda7468 in ui::LayerAnimationSequence::ProgressToEnd(ui::LayerAnimationDelegate\*) ui/compositor/layer\_animation\_sequence.cc:167:5  

#19 0x56051ddb3a2c in ProgressAnimationToEnd ui/compositor/layer\_animator.cc:472:13  

#20 0x56051ddb3a2c in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence\*, bool) ui/compositor/layer\_animator.cc:624:5  

#21 0x56051ddb6397 in ui::LayerAnimator::Step(base::TimeTicks) ui/compositor/layer\_animator.cc:503:7  

#22 0x56051ddc1967 in ui::LayerAnimatorCollection::OnAnimationStep(base::TimeTicks) ui/compositor/layer\_animator\_collection.cc:52:16  

#23 0x56051dd49a01 in ui::Compositor::BeginMainFrame(viz::BeginFrameArgs const&) ui/compositor/compositor.cc:662:14  

#24 0x56051cb96ca9 in cc::SingleThreadProxy::DoBeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single\_thread\_proxy.cc:910:21  

#25 0x56051cb9897f in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single\_thread\_proxy.cc:875:3  

#26 0x56051cb9b689 in Invoke<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> base/bind\_internal.h:531:12  

#27 0x56051cb9b689 in MakeItSo<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs> base/bind\_internal.h:731:5  

#28 0x56051cb9b689 in RunImpl<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &), std::\_\_1::tuple<base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, 0UL, 1UL> base/bind\_internal.h:784:12  

#29 0x56051cb9b689 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(viz::BeginFrameArgs const&), base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);), viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:753:12  

#30 0x560516da4939 in Run base/callback.h:142:12  

#31 0x560516da4939 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#32 0x560516e0c265 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:23  

#33 0x560516e0af3b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#34 0x560516e0d041 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#35 0x56051704aabc in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:200:55  

#36 0x560516e0dde6 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#37 0x560516d1a35e in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:140:14  

#38 0x56050b3c1db1 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1005:18  

#39 0x56050b3c7237 in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:152:15  

#40 0x56050b3bba1a in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser\_main.cc:49:28  

#41 0x560516a8c8e7 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:641:10

previously allocated by thread T0 (chrome) here:  

#0 0x560505ed7e8d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x56051950df48 in make\_unique<ash::sharesheet::SharesheetBubbleViewDelegate, aura::Window \*&, sharesheet::SharesheetServiceDelegator \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:28  

#2 0x56051950df48 in sharesheet::SharesheetServiceDelegator::SharesheetServiceDelegator(aura::Window\*, sharesheet::SharesheetService\*) chrome/browser/sharesheet/sharesheet\_service\_delegator.cc:24:7  

#3 0x56051950418d in make\_unique<sharesheet::SharesheetServiceDelegator, aura::Window \*&, sharesheet::SharesheetService \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:32  

#4 0x56051950418d in sharesheet::SharesheetService::GetOrCreateDelegator(aura::Window\*) chrome/browser/sharesheet/sharesheet\_service.cc:372:9  

#5 0x5605195066c4 in sharesheet::SharesheetService::OnReadyToShowBubble(aura::Window\*, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >) chrome/browser/sharesheet/sharesheet\_service.cc:328:21  

#6 0x560519507801 in sharesheet::SharesheetService::OnAppIconsLoaded(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >) chrome/browser/sharesheet/sharesheet\_service.cc:317:3  

#7 0x560519509ac8 in void base::internal::FunctorTraits<void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), void>::Invoke<void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), base::WeakPtr[sharesheet::SharesheetService](javascript:void(0);), base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) > >(void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), base::WeakPtr[sharesheet::SharesheetService](javascript:void(0);)&&, base::WeakPtr[content::WebContents](javascript:void(0);)&&, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);)&&, base::OnceCallback<void (sharesheet::SharesheetResult)>&&, base::OnceCallback<void (views::Widget::ClosedReason)>&&, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >&&) base/bind\_internal.h:531:12  

#8 0x5605195097e6 in MakeItSo<void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), base::WeakPtr[sharesheet::SharesheetService](javascript:void(0);), base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) > > base/bind\_internal.h:731:5  

#9 0x5605195097e6 in RunImpl<void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[sharesheet::SharesheetService](javascript:void(0);), base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)> >, 0UL, 1UL, 2UL, 3UL, 4UL> base/bind\_internal.h:784:12  

#10 0x5605195097e6 in base::internal::Invoker<base::internal::BindState<void (sharesheet::SharesheetService::\*)(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >), base::WeakPtr[sharesheet::SharesheetService](javascript:void(0);), base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)> >, void (std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >)>::RunOnce(base::internal::BindStateBase\*, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >&&) base/bind\_internal.h:753:12  

#11 0x560519507b6f in base::OnceCallback<void (std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >)>::Run(std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >) && base/callback.h:142:12  

#12 0x560519507240 in sharesheet::SharesheetService::LoadAppIcons(std::\_\_1::vector<apps::IntentLaunchInfo, std::\_\_1::allocator[apps::IntentLaunchInfo](javascript:void(0);) >, std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >, unsigned long, base::OnceCallback<void (std::\_\_1::vector<sharesheet::TargetInfo, std::\_\_1::allocator[sharesheet::TargetInfo](javascript:void(0);) >)>) chrome/browser/sharesheet/sharesheet\_service.cc:258:25  

#13 0x56051950374f in sharesheet::SharesheetService::PrepareToShowBubble(base::WeakPtr[content::WebContents](javascript:void(0);), mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), bool, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet\_service.cc:228:3  

#14 0x560519503287 in sharesheet::SharesheetService::ShowBubble(content::WebContents\*, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), bool, sharesheet::SharesheetMetrics::LaunchSource, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet\_service.cc:71:3  

#15 0x560519502e84 in sharesheet::SharesheetService::ShowBubble(content::WebContents\*, mojo::StructPtr[apps::mojom::Intent](javascript:void(0);), sharesheet::SharesheetMetrics::LaunchSource, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet\_service.cc:57:3  

#16 0x560525214d4e in sharing\_hub::SharingHubBubbleController::ShowSharesheet(views::Button\*) chrome/browser/ui/sharing\_hub/sharing\_hub\_bubble\_controller.cc:245:23  

#17 0x56052461e277 in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks) chrome/browser/ui/browser\_command\_controller.cc:581:7  

#18 0x5605255db78e in PageActionIconView::NotifyClick(ui::Event const&) chrome/browser/ui/views/page\_action/page\_action\_icon\_view.cc:148:3  

#19 0x56051f8eb33a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ui/views/controls/button/button.cc:66:13  

#20 0x56051f8f3126 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button\_controller.cc  

#21 0x56051f8ba261 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ui/events/scoped\_target\_handler.cc:28:24  

#22 0x56051a72049b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:191:12  

#23 0x56051a71f684 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#24 0x56051a71f14c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14  

#25 0x56051a71eeb9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#26 0x56051fa81c4f in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root\_view.cc:485:9  

#27 0x56051fa9a504 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc:1541:20  

#28 0x56051faef172 in views::NativeWidgetAura::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/native\_widget\_aura.cc  

#29 0x56051a72049b in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:191:12  

#30 0x56051a71f684 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:140:5  

#31 0x56051a71f14c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:84:14  

#32 0x56051a71eeb9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:56:15  

#33 0x56051dd0ead3 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:49:17

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/ui/sharing\_hub/sharing\_hub\_bubble\_controller.cc:81:29 in sharing\_hub::SharingHubBubbleController::~SharingHubBubbleController()  

Shadow bytes around the buggy address:  

0x0c048007e900: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fd  

0x0c048007e910: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd  

0x0c048007e920: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd  

0x0c048007e930: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fa  

0x0c048007e940: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd  

=>0x0c048007e950: fa fa fd fa fa fa[fd]fd fa fa fd fd fa fa fd fa  

0x0c048007e960: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c048007e970: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c048007e980: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c048007e990: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c048007e9a0: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa  

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

==37079==ABORTING

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 917.3 KB)

## Timeline

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-29)

Similar to 1264282 but a different stack trace.

Please confirm if this is only in M97 or earlier.



[Monorail components: UI>Browser>Sharing]

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-29)

+melzhang fyi

Verifying that this is also present in M96

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-30)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@google.com (2021-11-01)

kristipark@ - Thank you for working on this issue. I have a couple questions

1. RE https://crbug.com/chromium/1264703#c4: Have you confirmed the issue is present in M96 or are you still trying to verify that it is present?
2. Do you know if this is a new regression in M96 or was it also in M94/M95?
3. Do you believe that this issue is bad enough to block M96 Beta targeted for this week?

### jo...@chromium.org (2021-11-01)

Do we know whether this can affect M94? We'd have to merge to M94 in that case. Otherwise we should still try to merge on M96.

### ad...@google.com (2021-11-01)

Our sheriff is OOO today so I'm going to make some adjustments here.

1. OS=Chrome is inaccurate, this clearly affects Linux from the video
2. As this is UI driven and does not include any remote content at all, it definitely isn't critical severity. Bumping down to High. (Some would argue that this isn't exploitable remotely so is type=Bug, but I'll wait for the sheriff to return to discuss that).

Dana, as sheriff, please confirm which versions you reproduced this on (back to M94)

### ad...@google.com (2021-11-01)

(I'm expecting sheriffbot to add ReleaseBlock-Stable here, as this is deemed a regression given the earliest FoundIn is 96)

### ad...@google.com (2021-11-01)

danakj@ please see https://crbug.com/chromium/1264703#c10 when you're back.

### el...@chromium.org (2021-11-01)

#10: This is ChromeOS-specific and doesn't affect Linux; the reporter is showing a repro under an Ozone build on Linux, but Ozone is currently only used on Chrome OS afaik. The crash stack shows ash::sharesheet::SharesheetBubbleViewDelegate, which is the ChromeOS system share sheet.

#8: I believe the revision that introduced this specific UAF was b50dd05347e61c0b5a8d12249fbddeb98191166d which is present in M93+. However, the vulnerable code is gated behind a Finch trial (ChromeOSSharingHub) which we could retarget to later revisions - that may be preferable to doing a 94 merge.

### kr...@chromium.org (2021-11-01)

https://crbug.com/chromium/1264703#c8: I agree with Elly that this is likely present in M93+. Given it's a Finch experiment, this should not be a blocker.

I'll update the Finch config to target M96+ to avoid the M94 merge, and have a fix for this merged to M96.

### kr...@chromium.org (2021-11-01)

[Empty comment from Monorail migration]

### dg...@google.com (2021-11-01)

If this is caused by a finch experiment/trial + we are already in Beta for M96, can we just turn the experiment/trial off in M96 altogether and get the fix into M97? This would seem to be the least dangerous considering we are so close to Stable.

I don't think this would qualify as a release blocker for M96 if the issue has been around since M93 or M94 (see go/chromeos-release-blockers#what-are-not-release-blocking-issues) + is only caused by an experiment/trial that can be turned off. 

Removing Linux per https://crbug.com/chromium/1264703#c13.

### dg...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-11-02)

Thanks everyone. Sounds like the right call is to disable this in M96. Let's keep this bug open until that happens.

### [Deleted User] (2021-11-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-11-02)

Min version has been updated to M97 (http://cl/407169403). Currently working on fix for this issue.

### [Deleted User] (2021-11-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd706ddfd094933611d13c00b722680098b35f6e

commit bd706ddfd094933611d13c00b722680098b35f6e
Author: Kristi Park <kristipark@chromium.org>
Date: Thu Nov 04 20:26:02 2021

[CrOSSharingHub] Close sharesheet when the user swaps to another tab

Cancel the current sharing attempt if the user swaps to a different
tab. Swapping to a different window is permitted since a sharesheet is
tied to a native window.

We track the sharesheet using gfx::NativeWindow, which should outlive
both it and our WebContents.

Bug: 1264703
Change-Id: Ifbfa092aa1f7b007fe2502880e2eee3d1e2f6714
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3260639
Commit-Queue: Kristi Park <kristipark@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938460}

[modify] https://crrev.com/bd706ddfd094933611d13c00b722680098b35f6e/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc
[modify] https://crrev.com/bd706ddfd094933611d13c00b722680098b35f6e/chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.h


### kr...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-07)

Not requesting merge to dev (M97) because latest trunk commit (938460) appears to be prior to dev branch point (938553). If this is incorrect, please replace the Merge-NA-97 label with Merge-Request-97. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations, Khalil! The VRP Panel has decided to award you $5000 for this report. Nice finding! 

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1264703?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057760)*
