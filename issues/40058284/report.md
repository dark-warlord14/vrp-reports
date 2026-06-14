# Security: heap-use-after-free in TabStripLayoutHelper::SlotIsCollapsedTab

| Field | Value |
|-------|-------|
| **Issue ID** | [40058284](https://issues.chromium.org/issues/40058284) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-12-18 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

Dragging a tab group while a new tab in the tab group is opened results in the group being opened across multiple windows, which causes unexpected behaviour.

**VERSION**  

Chrome Version: 99.0.4774.0  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Launch chromium with poc.html and a NTP
2. Add poc.html to a tab group
3. Click the button
4. Drag the tab group
5. Now, drag the tab groups into the same window

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==15844==ERROR: AddressSanitizer: heap-use-after-free on address 0x11afc4237728 at pc 0x7ffbc5a5f9a0 bp 0x0015ef5fc380 sp 0x0015ef5fc3c8  

READ of size 1 at 0x11afc4237728 thread T0  

==15844==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffbc5a5f99f in TabStripLayoutHelper::SlotIsCollapsedTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip\_layout\_helper.cc:443  

#1 0x7ffbc5a5c941 in TabStripLayoutHelper::CalculateIdealBounds C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip\_layout\_helper.cc:299  

#2 0x7ffbc5a5e9dc in TabStripLayoutHelper::CalculateMinimumWidth C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip\_layout\_helper.cc:230  

#3 0x7ffbc2934a9a in TabStrip::GetMinimumSize C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:2169  

#4 0x7ffbbe0a6c74 in views::`anonymous namespace'::GetPreferredSize C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex\_layout\_types.cc:202  

#5 0x7ffbbe0a8404 in base::internal::Invoker<base::internal::BindState<gfx::Size (\*)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, const views::View \*, const views::SizeBounds &),views::MinimumFlexSizeRule,views::MaximumFlexSizeRule,views::MinimumFlexSizeRule,views::MaximumFlexSizeRule,bool>,gfx::Size (const views::View \*, const views::SizeBounds &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#6 0x7ffbbd2ee037 in views::FlexLayout::GetPreferredSizeForRule C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex\_layout.cc:483  

#7 0x7ffbbd2e9ab0 in views::FlexLayout::InitializeChildData C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex\_layout.cc:548  

#8 0x7ffbbd2e8277 in views::FlexLayout::CalculateProposedLayout C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex\_layout.cc:421  

#9 0x7ffbc01735e7 in views::LayoutManagerBase::GetProposedLayout C:\b\s\w\ir\cache\builder\src\ui\views\layout\layout\_manager\_base.cc:104  

#10 0x7ffbc0172d63 in views::LayoutManagerBase::GetAvailableSize C:\b\s\w\ir\cache\builder\src\ui\views\layout\layout\_manager\_base.cc:68  

#11 0x7ffbb8714b99 in views::View::GetAvailableSize C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:563  

#12 0x7ffbc292609e in TabStrip::GetAvailableWidthForTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3183  

#13 0x7ffbc292791a in TabStrip::UpdateIdealBounds C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3169  

#14 0x7ffbc2928b9c in TabStrip::OnGroupVisualsChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:1276  

#15 0x7ffbc291d6e9 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser\_tab\_strip\_controller.cc:718  

#16 0x7ffbbad2795e in TabStripModel::ChangeTabGroupVisuals C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1228  

#17 0x7ffbbd2d54a6 in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_group.cc:68  

#18 0x7ffbbad250a9 in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2245  

#19 0x7ffbbad12737 in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1758  

#20 0x7ffbbad11a34 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:366  

#21 0x7ffbc5a3cec9 in TabDragController::Attach C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1175  

#22 0x7ffbc5a45af6 in TabDragController::DetachAndAttachToNewContext C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1058  

#23 0x7ffbc5a414ef in TabDragController::RunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1415  

#24 0x7ffbc5a4570d in TabDragController::DetachIntoNewBrowserAndRunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1352  

#25 0x7ffbc5a43839 in TabDragController::DragBrowserToNewTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:866  

#26 0x7ffbc5a41c83 in TabDragController::ContinueDragging C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:836  

#27 0x7ffbc5a3bef7 in TabDragController::Drag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:600  

#28 0x7ffbc2930ced in TabStrip::TabDragContextImpl::ContinueDrag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:395  

#29 0x7ffbc293aaf2 in TabStrip::OnMouseDragged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3256  

#30 0x7ffbb8720827 in views::View::ProcessMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3051  

#31 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#32 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#33 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#34 0x7ffbb9655ed0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#35 0x7ffbbb169967 in views::internal::RootView::OnMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:463  

#36 0x7ffbb87483fb in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1550  

#37 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#38 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#39 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#40 0x7ffbb9655ed0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#41 0x7ffbbe0ee5dc in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#42 0x7ffbbb15c50f in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#43 0x7ffbbb15c169 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#44 0x7ffbbb15bc6b in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#45 0x7ffbbe0ebfb9 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1023  

#46 0x7ffbc206da5f in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3145  

#47 0x7ffbc2066ec3 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:358  

#48 0x7ffbc2066562 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1019  

#49 0x7ffbbb89f456 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#50 0x7ffbbb89dd71 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#51 0x7ffc5cdee7e7 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e7e7)  

#52 0x7ffc5cdee228 in DispatchMessageW+0x258 (C:\WINDOWS\System32\user32.dll+0x18000e228)  

#53 0x7ffbb8a8217a in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542  

#54 0x7ffbb8a801a9 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:504  

#55 0x7ffbb8a7faa3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:215  

#56 0x7ffbb8a7ddd8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#57 0x7ffbbb53ecd1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#58 0x7ffbb8958403 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#59 0x7ffbb1b25037 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#60 0x7ffbb1b2a479 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#61 0x7ffbb1b1e602 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#62 0x7ffbb45bfe2f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#63 0x7ffbb45c2eff in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#64 0x7ffbb45c2032 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#65 0x7ffbb45be1ed in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#66 0x7ffbb45bf278 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#67 0x7ffbaddf148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#68 0x7ff607675b65 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#69 0x7ff607672c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#70 0x7ff607a7969f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#71 0x7ffc5ca67033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#72 0x7ffc5e9c2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x11afc4237728 is located 680 bytes inside of 832-byte region [0x11afc4237480,0x11afc42377c0)  

freed by thread T0 here:  

#0 0x7ff6077227bb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffbc570e605 in TabGroupHeader::~TabGroupHeader C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_group\_header.cc:126  

#2 0x7ffbc5a63dbf in TabGroupViews::~TabGroupViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_group\_views.cc:35  

#3 0x7ffbc2942fc7 in std::\_\_1::unique\_ptr<TabGroupViews,std::\_\_1::default\_delete<TabGroupViews> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#4 0x7ffbc2926f89 in TabStrip::OnGroupCreated C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:1244  

#5 0x7ffbc291d170 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser\_tab\_strip\_controller.cc:677  

#6 0x7ffbbad26a73 in TabStripModel::CreateTabGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1207  

#7 0x7ffbbd2d541d in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_group.cc:65  

#8 0x7ffbbad250a9 in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2245  

#9 0x7ffbbad12737 in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1758  

#10 0x7ffbbad11a34 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:366  

#11 0x7ffbc5a3cec9 in TabDragController::Attach C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1175  

#12 0x7ffbc5a45af6 in TabDragController::DetachAndAttachToNewContext C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1058  

#13 0x7ffbc5a414ef in TabDragController::RunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1415  

#14 0x7ffbc5a4570d in TabDragController::DetachIntoNewBrowserAndRunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1352  

#15 0x7ffbc5a43839 in TabDragController::DragBrowserToNewTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:866  

#16 0x7ffbc5a41c83 in TabDragController::ContinueDragging C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:836  

#17 0x7ffbc5a3bef7 in TabDragController::Drag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:600  

#18 0x7ffbc2930ced in TabStrip::TabDragContextImpl::ContinueDrag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:395  

#19 0x7ffbc293aaf2 in TabStrip::OnMouseDragged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3256  

#20 0x7ffbb8720827 in views::View::ProcessMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3051  

#21 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#22 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#23 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#24 0x7ffbb9655ed0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#25 0x7ffbbb169967 in views::internal::RootView::OnMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:463  

#26 0x7ffbb87483fb in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1550  

#27 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190

previously allocated by thread T0 here:  

#0 0x7ff6077228bb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffbcb397bfe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffbc5a63ac1 in TabGroupViews::TabGroupViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_group\_views.cc:27  

#3 0x7ffbc2926e7a in TabStrip::OnGroupCreated C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:1242  

#4 0x7ffbc291d170 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser\_tab\_strip\_controller.cc:677  

#5 0x7ffbbad26a73 in TabStripModel::CreateTabGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1207  

#6 0x7ffbbd2d541d in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_group.cc:65  

#7 0x7ffbbad250a9 in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2245  

#8 0x7ffbbad12737 in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1758  

#9 0x7ffbbad11a34 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:366  

#10 0x7ffbc5a3cec9 in TabDragController::Attach C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1175  

#11 0x7ffbc5a45af6 in TabDragController::DetachAndAttachToNewContext C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1058  

#12 0x7ffbc5a455be in TabDragController::DetachIntoNewBrowserAndRunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:1338  

#13 0x7ffbc5a43839 in TabDragController::DragBrowserToNewTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:866  

#14 0x7ffbc5a41c83 in TabDragController::ContinueDragging C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:836  

#15 0x7ffbc5a3bef7 in TabDragController::Drag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_drag\_controller.cc:600  

#16 0x7ffbc2930ced in TabStrip::TabDragContextImpl::ContinueDrag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:395  

#17 0x7ffbc293aaf2 in TabStrip::OnMouseDragged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:3256  

#18 0x7ffbb8720827 in views::View::ProcessMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3051  

#19 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#20 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#21 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#22 0x7ffbb9655ed0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#23 0x7ffbbb169967 in views::internal::RootView::OnMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:463  

#24 0x7ffbb87483fb in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1550  

#25 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#26 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#27 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip\_layout\_helper.cc:443 in TabStripLayoutHelper::SlotIsCollapsedTab  

Shadow bytes around the buggy address:  

0x03b5bc846e90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846ea0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846eb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846ec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846ed0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x03b5bc846ee0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846ef0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x03b5bc846f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x03b5bc846f10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846f20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x03b5bc846f30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==15844==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 91 B)
- [uaf.mp4](attachments/uaf.mp4) (video/mp4, 764.1 KB)
- [drag-detach.mp4](attachments/drag-detach.mp4) (video/mp4, 1.7 MB)
- [detach-drag.mp4](attachments/detach-drag.mp4) (video/mp4, 1.2 MB)

## Timeline

### [Deleted User] (2021-12-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-20)

Thanks for the report. I can also repro in M98 but not 97 or 96.

connily: Could you PTAL? This is split from https://crbug.com/chromium/1278789.

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-01)

connily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2022-01-06)

Passing along another security bug, let me know if we should do a round of group triage?

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### sr...@google.com (2022-01-10)

This issue is marked as RBS for M98, we promoted M98 to beta and doing weekly releases on wednesday every week. Please review this bug and if it is indeed RBS for M98 please help get a fix landed on trunk asap and verify and request merge to m98 by tuesday so we can get the change beta coverage. 

### dp...@chromium.org (2022-01-13)

in order to address this issue, im going to force the tabGroupId to be updated to a new Id for the attached context when in header drag. this should address this issue by creating a new tab group visually since from the user perspective they already 2 separate tab groups. we can follow up later to figure out what a fix looks like to prevent the tab from being added into the wrong tabstrip during the drag, but that will require substantial work on the TabDrag code.

### dp...@chromium.org (2022-01-13)

after talking with a couple people about switching to new tab_group_ids it seems like we would break assumptions for the ExtensionsAPI if we did update the tab group ID. the other solution I looked at was merging the tab groups (see https://chromium-review.googlesource.com/c/chromium/src/+/3387988)

### st...@gmail.com (2022-01-16)

When a tab group header is dragged, `drag_data_` contains the dragged tabs from when the drag started. The issue is that tabs that were added to the tab group since the drag started are not added to `drag_data_`.


Different things happen depending on the order of actions ([drag, detach] vs [detach, drag]):

When a tab group (header) is being dragged while attached to the tab strip and a new tab in the group opens, the new tab will be left behind in the tab strip as it's not set as being dragged. When the dragged tab group is detached into a new tab strip (in a new window), the new tab will still stay in the original tab strip and keep its group ID. This results in one group being in multiple tab strips.

In case the new tab is opened after the tab group is detached, it causes the drag to be canceled. 
`TabDragController::RevertDrag` attaches back the tabs (except tabs that were closed), but since `drag_data_` does not contain newly created tabs, they are not attached back and this results in one tab group in multiple tab strips.


Both are caused by stale `drag_data_`. So, in a tab group header drag, adding new tabs opened in the tab group to `drag_data_` should fix this. Not sure how complicated this would be.
A quicker fix (to just fix the UAF) might be: when a new tab is to be added, if it has a group ID set and this group ID is currently being dragged, do not add it to the group.

### dp...@chromium.org (2022-01-18)

Im removing release blocker from this issue since it has been in effect since the introduction of the Tab Group Feature, we will follow with a fix, but it shouldnt block stable release.

### dp...@chromium.org (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2022-01-18)

Apparently Sheriffbot really wants this to block stable, perhaps ReleaseBlock-NA will stop it?

### do...@chromium.org (2022-01-18)

High severity security issues should be fixed by the current stable milestone per[1] - regardless of how long they have existed. That is why Sheriffbot is reapplying RBS. Please try and address this as soon as possible, or alternatively, please indicate why this bug is lower than High severity. Note that in general, memory corruption in the browser process triggerable by user interaction is always High severity unless the user interaction is particularly unusual or involved.

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-High-severity

### st...@gmail.com (2022-01-19)

I'm uploading screen recordings of the issue as described in https://crbug.com/chromium/1281079#c12 showing it more clearly.

### dp...@chromium.org (2022-01-20)

I have a fix for this behavior which is in early stages of review now.

### sr...@google.com (2022-01-21)

while it is true we should fix security bugs asap, if this is not a regression in M98, should this be RBS? ( Amy thougths?)

Also we are cutting M98 stable RC next tuesday so pls help expedite the land of fix so we can verify and merge to M98 before RC cut 

### am...@chromium.org (2022-01-21)

This does not appear to be a regression and should not be considered a release blocker.
It's great that dpenning@ has a fix in flight, if that can be landed soon, we can potentially get it into m98 stable cut, but is not a release blocker. 

### am...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-01-24)

out for review as https://chromium-review.googlesource.com/c/chromium/src/+/3404696

### dp...@chromium.org (2022-01-24)

de-duping these tabgroupheader drag issues

### st...@gmail.com (2022-01-24)

dpenning@, could you also add me to the referenced issue?

### am...@chromium.org (2022-03-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-16)

Upon review it appears you reported https://crbug.com/chromium/1278789 as a single report on 10 December, which you opened as two new reports later on 18 December - this one and 1281078. As this issue was merged into https://crbug.com/chromium/1280205 (reported on 15 December) without knowledge that this issue was reported prior since this individual report was open later, on 18 December. The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and for letting us know about the original report! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1281079?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1280205]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058284)*
