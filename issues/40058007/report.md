# Security: Heap-buffer-overflow in tabgroup

| Field | Value |
|-------|-------|
| **Issue ID** | [40058007](https://issues.chromium.org/issues/40058007) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-11-24 |
| **Bounty** | $7,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

Steps to reproduce the problem:
1. Install extension
2. It will open three tabs and group them separately. 
3. Right click the third tab strip, after the second tab is ungrouped, move third tab to the second tab's origin group (see poc.webm for more info)
4. overflow

What is the expected behavior?

What went wrong?
This is similar to https://crbug.com/chromium/1197875.
Test with asan-linux-release-944423.

=================================================================
==3485473==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000d52460 at pc 0x55a88eb5ed47 bp 0x7ffecb9dd610 sp 0x7ffecb9dd608
READ of size 8 at 0x602000d52460 thread T0 (chrome)
    #0 0x55a88eb5ed46 in operator()<std::__1::tuple<const unsigned long &, const unsigned long &>, std::__1::tuple<const unsigned long &, const unsigned long &> > buildtools/third_party/libc++/trunk/include/tuple:1314:38
    #1 0x55a88eb5ed46 in operator<<const unsigned long &, const unsigned long &, const unsigned long &, const unsigned long &> buildtools/third_party/libc++/trunk/include/tuple:1339:12
    #2 0x55a88eb5ed46 in operator< base/token.h:62:43
    #3 0x55a88eb5ed46 in tab_groups::TabGroupId::operator<(tab_groups::TabGroupId const&) const components/tab_groups/tab_group_id.cc:37:17
    #4 0x55a890a7be5b in operator() buildtools/third_party/libc++/trunk/include/__functional_base:54:21
    #5 0x55a890a7be5b in operator() buildtools/third_party/libc++/trunk/include/map:529:17
    #6 0x55a890a7be5b in __lower_bound<tab_groups::TabGroupId> buildtools/third_party/libc++/trunk/include/__tree:2557:14
    #7 0x55a890a7be5b in find<tab_groups::TabGroupId> buildtools/third_party/libc++/trunk/include/__tree:2477:26
    #8 0x55a890a7be5b in find buildtools/third_party/libc++/trunk/include/map:1393:68
    #9 0x55a890a7be5b in ContainsImpl<std::__1::map<tab_groups::TabGroupId, std::__1::unique_ptr<TabGroup, std::__1::default_delete<TabGroup> >, std::__1::less<tab_groups::TabGroupId>, std::__1::allocator<std::__1::pair<const tab_groups::TabGroupId, std::__1::unique_ptr<TabGroup, std::__1::default_delete<TabGroup> > > > >, tab_groups::TabGroupId> base/containers/contains.h:46:20
    #10 0x55a890a7be5b in Contains<std::__1::map<tab_groups::TabGroupId, std::__1::unique_ptr<TabGroup, std::__1::default_delete<TabGroup> >, std::__1::less<tab_groups::TabGroupId>, std::__1::allocator<std::__1::pair<const tab_groups::TabGroupId, std::__1::unique_ptr<TabGroup, std::__1::default_delete<TabGroup> > > > >, tab_groups::TabGroupId> base/containers/contains.h:82:10
    #11 0x55a890a7be5b in TabGroupModel::ContainsTabGroup(tab_groups::TabGroupId const&) const chrome/browser/ui/tabs/tab_group_model.cc:38:10
    #12 0x55a890a96048 in TabStripModel::AddToExistingGroupImpl(std::__1::vector<int, std::__1::allocator<int> > const&, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:2123:22
    #13 0x55a890a95e21 in TabStripModel::AddToExistingGroup(std::__1::vector<int, std::__1::allocator<int> > const&, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:1103:3
    #14 0x55a890aa3016 in TabStripModel::ExecuteAddToExistingGroupCommand(int, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:1495:3
    #15 0x55a891767abd in ExistingTabGroupSubMenuModel::ExecuteExistingCommand(int) chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc:100:12
    #16 0x55a891768d3d in ExecuteCommand chrome/browser/ui/tabs/existing_base_sub_menu_model.cc:52:3
    #17 0x55a891768d3d in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) chrome/browser/ui/tabs/existing_base_sub_menu_model.cc
    #18 0x55a88fc46448 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:170:12
    #19 0x55a88fbeb19b in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:233:29
    #20 0x55a88fbee954 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3175:13
    #21 0x55a88fbf32f2 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:825:7
    #22 0x55a88fdcba74 in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1544:20
    #23 0x55a888aaa405 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #24 0x55a888aaa405 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #25 0x55a888aa9cbc in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #26 0x55a888aa9cbc in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #27 0x55a88b5d35bd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #28 0x55a88b5f2dff in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:117:16
    #29 0x55a88b5f2aa3 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:142:12
    #30 0x55a88fea2a17 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:230:38
    #31 0x55a88fe9ce30 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:284:29
    #32 0x55a888ab703d in Run base/callback.h:142:12
    #33 0x55a888ab703d in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:36:25
    #34 0x55a889d5e99f in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #35 0x55a889d5e857 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1294:36
    #36 0x55a889d5dd4f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #37 0x55a889d5ebac in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #38 0x55a888a87784 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:98:29
    #39 0x55a889bc08c4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #40 0x55a8799ad6aa in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #41 0x55a8799ac711 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #42 0x55a8799ac711 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #43 0x55a889bce964 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #44 0x7f7663e5304d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5204d)

0x602000d52460 is located 0 bytes to the right of 16-byte region [0x602000d52450,0x602000d52460)
allocated by thread T0 (chrome) here:
    #0 0x55a8783b6e7d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55a890a7d00c in __libcpp_operator_new<unsigned long> buildtools/third_party/libc++/trunk/include/new:235:10
    #2 0x55a890a7d00c in __libcpp_allocate buildtools/third_party/libc++/trunk/include/new:261:10
    #3 0x55a890a7d00c in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82:38
    #4 0x55a890a7d00c in allocate buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261:20
    #5 0x55a890a7d00c in __split_buffer buildtools/third_party/libc++/trunk/include/__split_buffer:314:29
    #6 0x55a890a7d00c in void std::__1::vector<tab_groups::TabGroupId, std::__1::allocator<tab_groups::TabGroupId> >::__push_back_slow_path<tab_groups::TabGroupId const&>(tab_groups::TabGroupId const&) buildtools/third_party/libc++/trunk/include/vector:1625:49
    #7 0x55a891766cd6 in push_back buildtools/third_party/libc++/trunk/include/vector:1642:9
    #8 0x55a891766cd6 in ExistingTabGroupSubMenuModel::GetOrderedTabGroupsInSubMenu() chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc:69:22
    #9 0x55a891767a91 in ExistingTabGroupSubMenuModel::ExecuteExistingCommand(int) chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc:101:26
    #10 0x55a891768d3d in ExecuteCommand chrome/browser/ui/tabs/existing_base_sub_menu_model.cc:52:3
    #11 0x55a891768d3d in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) chrome/browser/ui/tabs/existing_base_sub_menu_model.cc
    #12 0x55a88fc46448 in views::MenuModelAdapter::ExecuteCommand(int, int) ui/views/controls/menu/menu_model_adapter.cc:170:12
    #13 0x55a88fbeb19b in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView*, int) ui/views/controls/menu/menu_runner_impl.cc:233:29
    #14 0x55a88fbee954 in views::MenuController::ExitMenu() ui/views/controls/menu/menu_controller.cc:3175:13
    #15 0x55a88fbf32f2 in views::MenuController::OnMouseReleased(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:825:7
    #16 0x55a88fdcba74 in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1544:20
    #17 0x55a888aaa405 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #18 0x55a888aaa405 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #19 0x55a888aa9cbc in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #20 0x55a888aa9cbc in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #21 0x55a88b5d35bd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x55a88b5f2dff in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:117:16
    #23 0x55a88b5f2aa3 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:142:12
    #24 0x55a88fea2a17 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:230:38
    #25 0x55a88fe9ce30 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:284:29
    #26 0x55a888ab703d in Run base/callback.h:142:12
    #27 0x55a888ab703d in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:36:25
    #28 0x55a889d5e99f in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #29 0x55a889d5e857 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1294:36
    #30 0x55a889d5dd4f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #31 0x55a889d5ebac in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #32 0x55a888a87784 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:98:29
    #33 0x55a889bc08c4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #34 0x55a8799ad6aa in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #35 0x55a8799ac711 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #36 0x55a8799ac711 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #37 0x55a889bce964 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #38 0x7f7663e5304d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5204d)

SUMMARY: AddressSanitizer: heap-buffer-overflow buildtools/third_party/libc++/trunk/include/tuple:1314:38 in operator()<std::__1::tuple<const unsigned long &, const unsigned long &>, std::__1::tuple<const unsigned long &, const unsigned long &> >
Shadow bytes around the buggy address:
  0x0c04801a2430: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x0c04801a2440: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x0c04801a2450: fa fa fd fa fa fa 00 fa fa fa fd fa fa fa fd fa
  0x0c04801a2460: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c04801a2470: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
=>0x0c04801a2480: fa fa fd fa fa fa fd fd fa fa 00 00[fa]fa 04 fa
  0x0c04801a2490: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c04801a24a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c04801a24b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c04801a24c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c04801a24d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==3485473==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4606.81  Channel: n/a
OS Version:

## Attachments

- [background.js](attachments/background.js) (text/plain, 641 B)
- [manifest.json](attachments/manifest.json) (text/plain, 210 B)
- [poc.webm](attachments/poc.webm) (video/webm, 499.2 KB)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 842 B)

## Timeline

### [Deleted User] (2021-11-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-24)

Thanks for the report. I can confirm this on Chrome 96 on Mac. The issue is that the context menu does not get updated when it is open after the extension manipulates the tab group.

=================================================================
==18972==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000275d40 at pc 0x00015f4236a2 bp 0x7ff7b110c840 sp 0x7ff7b110c838
READ of size 8 at 0x602000275d40 thread T0
    #0 0x15f4236a1 in tab_groups::TabGroupId::operator<(tab_groups::TabGroupId const&) const tab_group_id.cc:37
    #1 0x1612c82bb in TabGroupModel::ContainsTabGroup(tab_groups::TabGroupId const&) const tab_group_model.cc:38
    #2 0x1612e31c8 in TabStripModel::AddToExistingGroupImpl(std::__1::vector<int, std::__1::allocator<int> > const&, tab_groups::TabGroupId const&) tab_strip_model.cc:2142
    #3 0x1612e2fb0 in TabStripModel::AddToExistingGroup(std::__1::vector<int, std::__1::allocator<int> > const&, tab_groups::TabGroupId const&) tab_strip_model.cc:1118
    #4 0x1612f0916 in TabStripModel::ExecuteAddToExistingGroupCommand(int, tab_groups::TabGroupId const&) tab_strip_model.cc:1510
    #5 0x16207d830 in ExistingTabGroupSubMenuModel::ExecuteExistingCommand(int) existing_tab_group_sub_menu_model.cc:100
    #6 0x16206e1ac in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) existing_base_sub_menu_model.cc:52
    #7 0x1580fcb3b in -[MenuControllerCocoa itemSelected:] menu_controller.mm:327
    #8 0x7ff8075fb64c in -[NSApplication(NSResponder) sendAction:to:from:]+0x11f (AppKit:x86_64+0x24364c)
    #9 0x1562bb2fc in __43-[BrowserCrApplication sendAction:to:from:]_block_invoke chrome_browser_application_mac.mm:295
    #10 0x15753de19 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd5d4e19)
    #11 0x1562bad61 in -[BrowserCrApplication sendAction:to:from:] chrome_browser_application_mac.mm:294
    #12 0x7ff8076f09dd in -[NSMenuItem _corePerformAction]+0x19c (AppKit:x86_64+0x3389dd)
    #13 0x7ff8076f06fd in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x5e (AppKit:x86_64+0x3386fd)
    #14 0x7ff80773b518 in -[NSMenu performActionForItemAtIndex:]+0x70 (AppKit:x86_64+0x383518)
    #15 0x7ff80773b49e in -[NSMenu _internalPerformActionForItemAtIndex:]+0x51 (AppKit:x86_64+0x38349e)
    #16 0x7ff80773b2e7 in -[NSCarbonMenuImpl _carbonCommandProcessEvent:handlerCallRef:]+0x64 (AppKit:x86_64+0x3832e7)
    #17 0x7ff8076d4eb2 in NSSLMMenuEventHandler+0x435 (AppKit:x86_64+0x31ceb2)
    #18 0x7ff80d5c2bac in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x56e (HIToolbox:x86_64+0x8bac)
    #19 0x7ff80d5c1fdd in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x14c (HIToolbox:x86_64+0x7fdd)
    #20 0x7ff80d5d6e0a in SendEventToEventTarget+0x26 (HIToolbox:x86_64+0x1ce0a)
    #21 0x7ff80d6372ee in SendHICommandEvent(unsigned int, HICommand const*, unsigned int, unsigned int, unsigned char, void const*, OpaqueEventTargetRef*, OpaqueEventTargetRef*, OpaqueEventRef**)+0x16c (HIToolbox:x86_64+0x7d2ee)
    #22 0x7ff80d65c75d in SendMenuCommandWithContextAndModifiers+0x2d (HIToolbox:x86_64+0xa275d)
    #23 0x7ff80d65c707 in SendMenuItemSelectedEvent+0x15b (HIToolbox:x86_64+0xa2707)
    #24 0x7ff80d65c559 in FinishMenuSelection(SelectionData*, MenuResult*, MenuResult*)+0x5f (HIToolbox:x86_64+0xa2559)
    #25 0x7ff80d76b4db in PopUpMenuSelectCore(MenuData*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, unsigned int, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x5a9 (HIToolbox:x86_64+0x1b14db)
    #26 0x7ff80d76aa4f in _HandlePopUpMenuSelection8(OpaqueMenuRef*, OpaqueEventRef*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x199 (HIToolbox:x86_64+0x1b0a4f)
    #27 0x7ff80d63eecc in _HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86_64+0x84ecc)
    #28 0x7ff80788edcb in SLMPerformPopUpCarbonMenu+0x8b7 (AppKit:x86_64+0x4d6dcb)
    #29 0x7ff807734c40 in _NSSLMPopUpCarbonMenu3+0x464 (AppKit:x86_64+0x37cc40)
    #30 0x7ff8077cbf94 in -[NSCarbonMenuImpl _popUpContextMenu:withEvent:forView:withFont:]+0xdd (AppKit:x86_64+0x413f94)
    #31 0x7ff8077cbe08 in -[NSMenu _popUpContextMenu:withEvent:forView:withFont:]+0xe1 (AppKit:x86_64+0x413e08)
    #32 0x160443e5d in views::internal::MenuRunnerImplCocoa::RunMenuAt(views::Widget*, views::MenuButtonController*, gfx::Rect const&, views::MenuAnchorPosition, int, gfx::NativeView) menu_runner_impl_cocoa.mm:554
    #33 0x162082a99 in BrowserTabStripController::ShowContextMenuForTab(Tab*, gfx::Point const&, ui::MenuSourceType) browser_tab_strip_controller.cc:454
    #34 0x16045e289 in views::ContextMenuController::ShowContextMenuForView(views::View*, gfx::Point const&, ui::MenuSourceType) context_menu_controller.cc:29
    #35 0x160645302 in views::View::ProcessMousePressed(ui::MouseEvent const&) view.cc:3016
    #36 0x160644caa in views::View::OnMouseEvent(ui::MouseEvent*) view.cc:1430
    #37 0x15973abbe in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:140
    #38 0x15973a46b in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:56
    #39 0x160679dde in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) root_view.cc:413
    #40 0x160699cc8 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1519
    #41 0x16073cc9c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >) native_widget_mac_ns_window_host.mm:854
    #42 0x15cbf083b in -[BridgedContentView mouseEvent:] bridged_content_view.mm:595
    #43 0x7ff80756a27b in -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:]+0x1bed (AppKit:x86_64+0x1b227b)
    #44 0x7ff80756846d in -[NSWindow(NSEventRouting) sendEvent:]+0x15f (AppKit:x86_64+0x1b046d)
    #45 0x15cbfbfad in -[NativeWidgetMacNSWindow sendEvent:] native_widget_mac_nswindow.mm:298
    #46 0x7ff80756726d in -[NSApplication(NSEvent) sendEvent:]+0xb91 (AppKit:x86_64+0x1af26d)
    #47 0x1562bcd44 in __34-[BrowserCrApplication sendEvent:]_block_invoke chrome_browser_application_mac.mm:335
    #48 0x15753de19 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd5d4e19)
    #49 0x1562bc0be in -[BrowserCrApplication sendEvent:] chrome_browser_application_mac.mm:319
    #50 0x7ff80781f80a in -[NSApplication _handleEvent:]+0x40 (AppKit:x86_64+0x46780a)
    #51 0x7ff8073e737d in -[NSApplication run]+0x26e (AppKit:x86_64+0x2f37d)
    #52 0x15755295a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) message_pump_mac.mm:743
    #53 0x15754e698 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) message_pump_mac.mm:161
    #54 0x15746f4ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:462
    #55 0x1573aabcc in base::RunLoop::Run(base::Location const&) run_loop.cc:140
    #56 0x14e7970e5 in content::BrowserMainLoop::RunMainMessageLoop() browser_main_loop.cc:989
    #57 0x14e79b571 in content::BrowserMainRunnerImpl::Run() browser_main_runner_impl.cc:152
    #58 0x14e790e73 in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:49
    #59 0x1561020c0 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content_main_runner_impl.cc:1116
    #60 0x156101198 in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:983
    #61 0x1560fcf4d in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content_main.cc:390
    #62 0x1560fee31 in content::ContentMain(content::ContentMainParams const&) content_main.cc:418
    #63 0x149f6db1c in ChromeMain chrome_main.cc:172
    #64 0x10edeebff in main chrome_exe_main_mac.cc:115
    #65 0x10ff944fd in start+0x1cd (dyld:x86_64+0x54fd)

0x602000275d40 is located 0 bytes to the right of 16-byte region [0x602000275d30,0x602000275d40)
allocated by thread T0 here:
    #0 0x10f1ac6e0  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x476e0)
    #1 0x149f6b4a7 in operator new(unsigned long) new.cpp:67
    #2 0x1612c951c in void std::__1::vector<tab_groups::TabGroupId, std::__1::allocator<tab_groups::TabGroupId> >::__push_back_slow_path<tab_groups::TabGroupId const&>(tab_groups::TabGroupId const&) vector:1625
    #3 0x16207ca0e in ExistingTabGroupSubMenuModel::GetOrderedTabGroupsInSubMenu() existing_tab_group_sub_menu_model.cc:69
    #4 0x16207d7fa in ExistingTabGroupSubMenuModel::ExecuteExistingCommand(int) existing_tab_group_sub_menu_model.cc:101
    #5 0x16206e1ac in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) existing_base_sub_menu_model.cc:52
    #6 0x1580fcb3b in -[MenuControllerCocoa itemSelected:] menu_controller.mm:327
    #7 0x7ff8075fb64c in -[NSApplication(NSResponder) sendAction:to:from:]+0x11f (AppKit:x86_64+0x24364c)
    #8 0x1562bb2fc in __43-[BrowserCrApplication sendAction:to:from:]_block_invoke chrome_browser_application_mac.mm:295
    #9 0x15753de19 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd5d4e19)
    #10 0x1562bad61 in -[BrowserCrApplication sendAction:to:from:] chrome_browser_application_mac.mm:294
    #11 0x7ff8076f09dd in -[NSMenuItem _corePerformAction]+0x19c (AppKit:x86_64+0x3389dd)
    #12 0x7ff8076f06fd in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x5e (AppKit:x86_64+0x3386fd)
    #13 0x7ff80773b518 in -[NSMenu performActionForItemAtIndex:]+0x70 (AppKit:x86_64+0x383518)
    #14 0x7ff80773b49e in -[NSMenu _internalPerformActionForItemAtIndex:]+0x51 (AppKit:x86_64+0x38349e)
    #15 0x7ff80773b2e7 in -[NSCarbonMenuImpl _carbonCommandProcessEvent:handlerCallRef:]+0x64 (AppKit:x86_64+0x3832e7)
    #16 0x7ff8076d4eb2 in NSSLMMenuEventHandler+0x435 (AppKit:x86_64+0x31ceb2)
    #17 0x7ff80d5c2bac in DispatchEventToHandlers(EventTargetRec*, OpaqueEventRef*, HandlerCallRec*)+0x56e (HIToolbox:x86_64+0x8bac)
    #18 0x7ff80d5c1fdd in SendEventToEventTargetInternal(OpaqueEventRef*, OpaqueEventTargetRef*, HandlerCallRec*)+0x14c (HIToolbox:x86_64+0x7fdd)
    #19 0x7ff80d5d6e0a in SendEventToEventTarget+0x26 (HIToolbox:x86_64+0x1ce0a)
    #20 0x7ff80d6372ee in SendHICommandEvent(unsigned int, HICommand const*, unsigned int, unsigned int, unsigned char, void const*, OpaqueEventTargetRef*, OpaqueEventTargetRef*, OpaqueEventRef**)+0x16c (HIToolbox:x86_64+0x7d2ee)
    #21 0x7ff80d65c75d in SendMenuCommandWithContextAndModifiers+0x2d (HIToolbox:x86_64+0xa275d)
    #22 0x7ff80d65c707 in SendMenuItemSelectedEvent+0x15b (HIToolbox:x86_64+0xa2707)
    #23 0x7ff80d65c559 in FinishMenuSelection(SelectionData*, MenuResult*, MenuResult*)+0x5f (HIToolbox:x86_64+0xa2559)
    #24 0x7ff80d76b4db in PopUpMenuSelectCore(MenuData*, Point, double, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, unsigned int, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x5a9 (HIToolbox:x86_64+0x1b14db)
    #25 0x7ff80d76aa4f in _HandlePopUpMenuSelection8(OpaqueMenuRef*, OpaqueEventRef*, unsigned int, Point, unsigned short, unsigned int, unsigned int, Rect const*, unsigned short, Rect const*, Rect const*, __CFDictionary const*, __CFString const*, OpaqueMenuRef**, unsigned short*)+0x199 (HIToolbox:x86_64+0x1b0a4f)
    #26 0x7ff80d63eecc in _HandlePopUpMenuSelectionWithDictionary+0x148 (HIToolbox:x86_64+0x84ecc)
    #27 0x7ff80788edcb in SLMPerformPopUpCarbonMenu+0x8b7 (AppKit:x86_64+0x4d6dcb)
    #28 0x7ff807734c40 in _NSSLMPopUpCarbonMenu3+0x464 (AppKit:x86_64+0x37cc40)
    #29 0x7ff8077cbf94 in -[NSCarbonMenuImpl _popUpContextMenu:withEvent:forView:withFont:]+0xdd (AppKit:x86_64+0x413f94)

SUMMARY: AddressSanitizer: heap-buffer-overflow tab_group_id.cc:37 in tab_groups::TabGroupId::operator<(tab_groups::TabGroupId const&) const
Shadow bytes around the buggy address:
  0x1c040004eb50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c040004eb60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c040004eb70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c040004eb80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c040004eb90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x1c040004eba0: fa fa 04 fa fa fa 00 00[fa]fa fd fa fa fa fd fa
  0x1c040004ebb0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd
  0x1c040004ebc0: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fd
  0x1c040004ebd0: fa fa 00 00 fa fa fd fd fa fa fd fd fa fa fd fa
  0x1c040004ebe0: fa fa fd fa fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x1c040004ebf0: fa fa 00 00 fa fa fd fd fa fa fd fd fa fa 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==18972==ABORTING


[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2021-11-25)

Here are some analysis, if it's wrong, please ignore it :P
I think the root cause of this overflow is located in function ExecuteExistingCommand [1], `target_index` can be equal to or larger than the size of vector which GetOrderedTabGroupsInSubMenu()[2] returns.
In this case, target_index is 1 and the size of vector is also one(vector size is changed form 2 to 1 after we ungroup tabs). The overflow element vector[1] is used as a TabId in  `TabStripModel::AddToExistingGroupImpl`[3]. 
The size of vector[1] is smaller than the size of TabId, when [3] use TabId.token_, it wil read something overflow vector[1].
And I post a possible patch for this problem. But I'm not pretty sure it's correctness.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc;l=101;bpv=1;bpt=0;drc=22556eb9f230f0a9dee66c30c5d91ea6afe374a2
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc;l=62;drc=22556eb9f230f0a9dee66c30c5d91ea6afe374a2;bpv=1;bpt=0
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=2123;drc=25742e247258532cbdfc9378461290c787b1875f;bpv=0;bpt=0

### me...@gmail.com (2021-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

connily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-23)

connily: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-01-12)

out for review: https://chromium-review.googlesource.com/c/chromium/src/+/3384389

### me...@gmail.com (2022-01-19)

[Comment Deleted]

### [Deleted User] (2022-01-23)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8e276e73f8390fc4f88a2752527889467bf742bb

commit 8e276e73f8390fc4f88a2752527889467bf742bb
Author: David Pennington <dpenning@chromium.org>
Date: Tue Jan 25 02:58:21 2022

fix adding to group that is deleted from the tab_menu_model

The old way that target index was used to get the groupID for the tab
group to be added to was using the wrong source of truth. the fix is
to have a mapping of index to tabGroupID from when the model was
generated and then check against that mapping to check if the group
model still contains that ID.

Bug: 1273397
Change-Id: I566505dc4267a1224de0dd2de95da8c12f79ed97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384389
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#962822}

[modify] https://crrev.com/8e276e73f8390fc4f88a2752527889467bf742bb/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.h
[modify] https://crrev.com/8e276e73f8390fc4f88a2752527889467bf742bb/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc


### me...@gmail.com (2022-01-28)

Hi, I want to temporarily change my Credit info  to:

Krace

Thank you.

### me...@chromium.org (2022-02-01)

dpenning@chromium.org: Can this be marked as fixed? Thanks.

### dl...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

Requesting merge to extended stable M96 because latest trunk commit (962822) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (962822) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (962822) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (962822) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Merge review required: M98 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Merge review required: M96 is already shipping to stable.

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

### am...@chromium.org (2022-02-02)

M98 is now stable channel release branch, so merge to M96 and M97 is unnecessary
merge approved to M99, please merge to branch 4844 (go/chrome-branches) at your earliest convenience 

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### pb...@google.com (2022-02-08)

[Bulk Edit] Your change has been approved for M99 branch,please go ahead and merge the CL's to M99 branch(go/chrome-branches) manually asap so that they would be part of tomorrows M99 Beta release.

### am...@chromium.org (2022-02-08)

m98 merge approved, please merge to branch 4758 by EOD Thursday, 10 February so this fix can be included in next week's Stable channel refresh -- thanks! 

### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6921d04d0dadf9d3621cf0491a152f778ae27965

commit 6921d04d0dadf9d3621cf0491a152f778ae27965
Author: David Pennington <dpenning@chromium.org>
Date: Wed Feb 09 17:07:33 2022

fix adding to group that is deleted from the tab_menu_model

The old way that target index was used to get the groupID for the tab
group to be added to was using the wrong source of truth. the fix is
to have a mapping of index to tabGroupID from when the model was
generated and then check against that mapping to check if the group
model still contains that ID.

(cherry picked from commit 8e276e73f8390fc4f88a2752527889467bf742bb)

Bug: 1273397
Change-Id: I566505dc4267a1224de0dd2de95da8c12f79ed97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384389
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962822}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3448672
Reviewed-by: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#385}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/6921d04d0dadf9d3621cf0491a152f778ae27965/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/6921d04d0dadf9d3621cf0491a152f778ae27965/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.h


### [Deleted User] (2022-02-09)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@google.com (2022-02-09)

Cherrypicked to 99 in https://chromium-review.googlesource.com/c/chromium/src/+/3448672
Cherrypicked to 98 in https://chromium-review.googlesource.com/c/chromium/src/+/3449665

### gi...@appspot.gserviceaccount.com (2022-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2b608b95e2534312a86105be25578a20a5fac6e7

commit 2b608b95e2534312a86105be25578a20a5fac6e7
Author: David Pennington <dpenning@chromium.org>
Date: Wed Feb 09 19:14:19 2022

fix adding to group that is deleted from the tab_menu_model

The old way that target index was used to get the groupID for the tab
group to be added to was using the wrong source of truth. the fix is
to have a mapping of index to tabGroupID from when the model was
generated and then check against that mapping to check if the group
model still contains that ID.

(cherry picked from commit 8e276e73f8390fc4f88a2752527889467bf742bb)

Bug: 1273397
Change-Id: I566505dc4267a1224de0dd2de95da8c12f79ed97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384389
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962822}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3449665
Cr-Commit-Position: refs/branch-heads/4758@{#1123}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/2b608b95e2534312a86105be25578a20a5fac6e7/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/2b608b95e2534312a86105be25578a20a5fac6e7/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.h


### rz...@google.com (2022-02-10)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-11)

1. just https://crrev.com/c/3452262
2. Low, no conflicts
3. 98, 99
4. Yes

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP has decided to award you $7000 for this report. Thank you for this report and your efforts!  

### me...@gmail.com (2022-02-12)

[Comment Deleted]

### am...@chromium.org (2022-02-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-12)

Re: https://crbug.com/chromium/1273397#c38: differences in reward amounts are primarily based on report quality, pocs, exploits, analysis or follow-up provided by the researcher, and bonuses, such as patch bonus which was rewarded for https://crbug.com/chromium/1197875. 
We have also shifted reward amounts for reports requiring a high degree of user interaction, especially unusual user interaction, and less exploitation through remote content. If you provide a new POC or reproduction with reduced interaction and can still demonstrate exploitability, we would be glad to reassess for a potential change in reward amount. 

### gm...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b613ed5f67476cc532ebf9e2accd889283c1ebb6

commit b613ed5f67476cc532ebf9e2accd889283c1ebb6
Author: David Pennington <dpenning@chromium.org>
Date: Mon Feb 14 18:18:38 2022

[M96-LTS] fix adding to group that is deleted from the tab_menu_model

The old way that target index was used to get the groupID for the tab
group to be added to was using the wrong source of truth. the fix is
to have a mapping of index to tabGroupID from when the model was
generated and then check against that mapping to check if the group
model still contains that ID.

(cherry picked from commit 8e276e73f8390fc4f88a2752527889467bf742bb)

Bug: 1273397
Change-Id: I566505dc4267a1224de0dd2de95da8c12f79ed97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384389
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#962822}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3452262
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1471}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/b613ed5f67476cc532ebf9e2accd889283c1ebb6/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/b613ed5f67476cc532ebf9e2accd889283c1ebb6/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.h


### am...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1273397?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058007)*
