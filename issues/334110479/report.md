# Security: SidePanelContentSwappingContainer Heap-Use-After-Free Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [334110479](https://issues.chromium.org/issues/334110479) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Windows |
| **Chrome Version** | 123.0.0.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2024-04-13 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Download Chrome asan
2. Open chrome.exe --no-sandbox --enable-features=DataCollectionModeForScreen2x
3. Close Chrome

# Problem Description

```
=================================================================
==9564==ERROR: AddressSanitizer: heap-use-after-free on address 0x1291b8ada980 at pc 0x7ffba943ff79 bp 0x00e2049fd0e0 sp 0x00e2049fd128
READ of size 1 at 0x1291b8ada980 thread T0
==9564==WARNING: Failed to use and restart external symbolizer!
[9316:13680:0413/235831.137:ERROR:shared_image_manager.cc(225)] SharedImageManager::ProduceSkia: Trying to Produce a Skia representation from a non-existent mailbox.
[9316:13680:0413/235831.139:ERROR:shared_image_manager.cc(225)] SharedImageManager::ProduceSkia: Trying to Produce a Skia representation from a non-existent mailbox.
    #0 0x7ffba943ff78 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:53
    #1 0x7ffba943fb98 in base::internal::`anonymous namespace'::SafelyUnwrapForDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:76
    #2 0x7ffbace91356 in `anonymous namespace'::SidePanelContentSwappingContainer::ResetLoadingEntryIfNecessary C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_coordinator.cc:244
    #3 0x7ffbace9d325 in `anonymous namespace'::SidePanelContentSwappingContainer::~SidePanelContentSwappingContainer C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_coordinator.cc:220
    #4 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #5 0x7ffba4a1fc4f in views::FlexLayoutView::~FlexLayoutView C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout_view.cc:29
    #6 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #7 0x7ffbace82034 in SidePanel::~SidePanel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel.cc:267
    #8 0x7ffbace8524f in SidePanel::~SidePanel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel.cc:267
    #9 0x7ffba13274aa in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3214
    #10 0x7ffba13278e6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:354
    #11 0x7ffba8049fdf in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:1059
    #12 0x7ffba8073d09 in BrowserView::`vector deleting destructor'+0x19 (C:\fuzz\win32-release_x64_asan-win32-release_x64-1286748\chrome.dll+0x194ec3d09)
    #13 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #14 0x7ffbb24a8653 in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #15 0x7ffbb24b1c5f in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #16 0x7ffba12e1f5c in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:179
    #17 0x7ffba12e403f in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:175
    #18 0x7ffba13274aa in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3214
    #19 0x7ffba13278e6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:354
    #20 0x7ffba12f61da in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2128
    #21 0x7ffba12f5737 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:242
    #22 0x7ffba8e8cdcf in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:128
    #23 0x7ffbad7b0309 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:317
    #24 0x7ffbb4bfbeaf in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #25 0x7ffbad7b163b in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:392
    #26 0x7ffbad786b6e in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1102
    #27 0x7ffba5e376bc in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:310
    #28 0x7ffba5e362fe in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #29 0x7ffc76fdef74 in CallWindowProcW+0x614 (C:\Windows\System32\USER32.dll+0x18000ef74)
    #30 0x7ffc76fde8db in DispatchMessageW+0x6eb (C:\Windows\System32\USER32.dll+0x18000e8db)
    #31 0x7ffc76ff76e7 in GetLastInputInfo+0x77 (C:\Windows\System32\USER32.dll+0x1800276e7)
    #32 0x7ffc78cd0e63 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x180

```
# Summary

Security: SidePanelContentSwappingContainer Heap-Use-After-Free Vulnerability

# Custom Questions

#### Type of crash:

Browser

#### Crash state:

```
=================================================================
==9564==ERROR: AddressSanitizer: heap-use-after-free on address 0x1291b8ada980 at pc 0x7ffba943ff79 bp 0x00e2049fd0e0 sp 0x00e2049fd128
READ of size 1 at 0x1291b8ada980 thread T0
==9564==WARNING: Failed to use and restart external symbolizer!
[9316:13680:0413/235831.137:ERROR:shared_image_manager.cc(225)] SharedImageManager::ProduceSkia: Trying to Produce a Skia representation from a non-existent mailbox.
[9316:13680:0413/235831.139:ERROR:shared_image_manager.cc(225)] SharedImageManager::ProduceSkia: Trying to Produce a Skia representation from a non-existent mailbox.
    #0 0x7ffba943ff78 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:53
    #1 0x7ffba943fb98 in base::internal::`anonymous namespace'::SafelyUnwrapForDereference C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:76
    #2 0x7ffbace91356 in `anonymous namespace'::SidePanelContentSwappingContainer::ResetLoadingEntryIfNecessary C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_coordinator.cc:244
    #3 0x7ffbace9d325 in `anonymous namespace'::SidePanelContentSwappingContainer::~SidePanelContentSwappingContainer C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_coordinator.cc:220
    #4 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #5 0x7ffba4a1fc4f in views::FlexLayoutView::~FlexLayoutView C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout_view.cc:29
    #6 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #7 0x7ffbace82034 in SidePanel::~SidePanel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel.cc:267
    #8 0x7ffbace8524f in SidePanel::~SidePanel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel.cc:267
    #9 0x7ffba13274aa in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3214
    #10 0x7ffba13278e6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:354
    #11 0x7ffba8049fdf in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:1059
    #12 0x7ffba8073d09 in BrowserView::`vector deleting destructor'+0x19 (C:\fuzz\win32-release_x64_asan-win32-release_x64-1286748\chrome.dll+0x194ec3d09)
    #13 0x7ffba1322ea4 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:274
    #14 0x7ffbb24a8653 in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #15 0x7ffbb24b1c5f in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:122
    #16 0x7ffba12e1f5c in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:179
    #17 0x7ffba12e403f in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:175
    #18 0x7ffba13274aa in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3214
    #19 0x7ffba13278e6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:354
    #20 0x7ffba12f61da in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2128
    #21 0x7ffba12f5737 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:242
    #22 0x7ffba8e8cdcf in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:128
    #23 0x7ffbad7b0309 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:317
    #24 0x7ffbb4bfbeaf in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #25 0x7ffbad7b163b in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:392
    #26 0x7ffbad786b6e in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1102
    #27 0x7ffba5e376bc in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:310
    #28 0x7ffba5e362fe in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #29 0x7ffc76fdef74 in CallWindowProcW+0x614 (C:\Windows\System32\USER32.dll+0x18000ef74)
    #30 0x7ffc76fde8db in DispatchMessageW+0x6eb (C:\Windows\System32\USER32.dll+0x18000e8db)
    #31 0x7ffc76ff76e7 in GetLastInputInfo+0x77 (C:\Windows\System32\USER32.dll+0x1800276e7)
    #32 0x7ffc78cd0e63 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a0e63)
    #33 0x7ffc76732383 in NtUserDestroyWindow+0x13 (C:\Windows\System32\win32u.dll+0x180002383)
    #34 0x7ffbad7a1ef1 in base::internal::Invoker<base::internal::FunctorTraits<void (views::HWNDMessageHandler::*&&)(),base::WeakPtr<views::HWNDMessageHandler> &&>,base::internal::BindState<1,1,0,void (views::HWNDMessageHandler::*)(),base::WeakPtr<views::HWNDMessageHandler> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #35 0x7ffba17531a0 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:203
    #36 0x7ffba505def6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:473
    #37 0x7ffba505ce19 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:338
    #38 0x7ffba16b153f in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:255
    #39 0x7ffba16af154 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:82
    #40 0x7ffba505faac in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:644
    #41 0x7ffba179dfb0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #42 0x7ffb9b173b75 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1104
    #43 0x7ffb9b17ab69 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:159
    #44 0x7ffb9b16a02f in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:34
    #45 0x7ffba006110e in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:707
    #46 0x7ffba006424f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1298
    #47 0x7ffba0063af7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1143
    #48 0x7ffba005f60a in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:329
    #49 0x7ffba005ffcd in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:342
    #50 0x7ffb931b16c3 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:192
    #51 0x7ff66f2b43c6 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:180
    #52 0x7ff66f2b1dc0 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #53 0x7ff66f692e53 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #54 0x7ffc789a7343 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017343)
    #55 0x7ffc78c826b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

0x1291b8ada980 is located 0 bytes inside of 224-byte region [0x1291b8ada980,0x1291b8adaa60)
freed by thread T0 here:
    #0 0x7ff66f38f03d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffbade860c9 in std::__Cr::vector<std::__Cr::unique_ptr<SidePanelEntry,std::__Cr::default_delete<SidePanelEntry> >,std::__Cr::allocator<std::__Cr::unique_ptr<SidePanelEntry,std::__Cr::default_delete<SidePanelEntry> > > >::__destroy_vector::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\vector:491
    #2 0x7ffbade81d7e in SidePanelRegistry::~SidePanelRegistry C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_registry.cc:23
    #3 0x7ffbade85faf in SidePanelRegistry::~SidePanelRegistry C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\side_panel_registry.cc:19
    #4 0x7ffba1766dfc in base::SupportsUserData::~SupportsUserData C:\b\s\w\ir\cache\builder\src\base\supports_user_data.cc:108
    #5 0x7ffb9c8161d8 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:1330
    #6 0x7ffb9c8ac5ef in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:1214
    #7 0x7ffba80eb93a in tabs::TabModel::~TabModel C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_model.cc:26
    #8 0x7ffba46971c2 in TabStripModel::SendDetachWebContentsNotifications C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:622
    #9 0x7ffba46a2a6a in TabStripModel::CloseTabs C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2113
    #10 0x7ffba46a1727 in TabStripModel::CloseAllTabs C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:793
    #11 0x7ffba806a7c2 in BrowserView::OnWindowCloseRequested C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:4283
    #12 0x7ffba12fea07 in views::Widget::CloseWithReason C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:778
    #13 0x7ffbb24c5de7 in base::internal::Invoker<base::internal::FunctorTraits<void (views::Widget::*const &)(views::Widget::ClosedReason),BrowserFrame *,const views::Widget::ClosedReason &>,base::internal::BindState<1,1,0,void (views::Widget::*)(views::Widget::ClosedReason),base::internal::UnretainedWrapper<BrowserFrame,base::unretained_traits::MayNotDangle,0>,views::Widget::ClosedReason>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:987
    #14 0x7ffb9358b923 in base::RepeatingCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344
    #15 0x7ffba1424c36 in views::Button::PressedCallback::Run C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:131
    #16 0x7ffba142a5c2 in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:737
    #17 0x7ffba4a966ee in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button_controller.cc
    #18 0x7ffba133e4ee in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3724
    #19 0x7ffba86bc84c in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped_target_handler.cc:28
    #20 0x7ffba2946227 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187
    #21 0x7ffba2944f28 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:136
    #22 0x7ffba294438d in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:82
    #23 0x7ffba2943e1b in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:54
    #24 0x7ffba49d3a34 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:555
    #25 0x7ffba1314d23 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1833
    #26 0x7ffbad7bbd48 in views::DesktopNativeWidgetAura::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1324
    #27 0x7ffba2946227 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187

previously allocated by thread T0 here:
    #0 0x7ff66f38f13d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffbb7e4d3ee in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ffbae4ca17b in ReadAnythingSidePanelController::CreateAndRegisterEntry C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\read_anything\read_anything_side_panel_controller.cc:128
    #3 0x7ffba8bbfdc5 in ReadAnythingTabHelper::CreateAndRegisterEntry C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\side_panel\read_anything\read_anything_tab_helper.cc:18
    #4 0x7ffbacfd1cb4 in ReadAnythingCoordinator::CreateAndRegisterEntryForWebContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\read_anything\read_anything_coordinator.cc:215
    #5 0x7ffbacfd4cdf in ReadAnythingCoordinator::OnTabStripModelChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\side_panel\read_anything\read_anything_coordinator.cc:337
    #6 0x7ffba4693d05 in TabStripModel::OnChange C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:502
    #7 0x7ffba4691d55 in TabStripModel::InsertTabAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2061
    #8 0x7ffba46aaf73 in TabStripModel::AddWebContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1110
    #9 0x7ffba46d9b3f in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:943
    #10 0x7ffbad8d0f1d in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:350
    #11 0x7ffbad8d396e in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:683
    #12 0x7ffbad8cfb92 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:476
    #13 0x7ffbad8cec12 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:194
    #14 0x7ffba87ecac8 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:720
    #15 0x7ffba87edd99 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:800
    #16 0x7ffba87ec1ef in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1317
    #17 0x7ffba87e9f7a in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:671
    #18 0x7ffba4bba30e in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1770
    #19 0x7ffba4bb9283 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1223
    #20 0x7ffb9b170708 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1014
    #21 0x7ffb9b177ab8 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(),content::BrowserMainLoop *>,base::internal::BindState<1,1,0,int (content::BrowserMainLoop::*)(),base::internal::UnretainedWrapper<content::BrowserMainLoop,base::unretained_traits::MayNotDangle,0> >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980
    #22 0x7ffb9c703a88 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:42
    #23 0x7ffb9b16f65d in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:917
    #24 0x7ffb9b17a115 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:140
    #25 0x7ffb9b169fdc in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #26 0x7ffba006110e in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:707
    #27 0x7ffba006424f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1298

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\raw_ptr_asan_hooks.cc:53 in base::internal::`anonymous namespace'::CrashImmediatelyOnUseAfterFree
Shadow bytes around the buggy address:
  0x1291b8ada700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1291b8ada780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1291b8ada800: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x1291b8ada880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1291b8ada900: fd fd fd fd fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x1291b8ada980:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1291b8adaa00: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x1291b8adaa80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x1291b8adab00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1291b8adab80: fd fd fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x1291b8adac00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==9564==ADDITIONAL INFO

==9564==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffbad77fbb0 in views::HWNDMessageHandler::Close C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:487

MiraclePtr Status: PROTECTED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==9564==END OF ADDITIONAL INFO
==9564==ABORTING
[7920:14192:0413/235832.548:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.

```
#### Reporter credit:

Pwn2car

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: Yes

## Timeline

### bb...@google.com (2024-04-15)

DataCollectionModeForScreen2x is effectively a test-only feature and not enabled by default. We do not normally consider issues in test only code security bugs. Do you have a reproducer without this feature enabled?

Failing that I believe this is a regular bug..

### ma...@google.com (2024-04-17)

The duplicate [issue 335328453](https://issues.chromium.org/issues/335328453) has a detailed RCA and bisect information. Assigning to @corising per information on that issue.

@corising, could you help us understand if this bug might be reachable by any stable channel population users/without custom flags? Thank you.

### co...@chromium.org (2024-04-18)

If the comments in issue 335328453 are correct, this is caused by a change that landed two weeks ago so it wouldn't be in stable. I will look into this more and get a fix out for it today.

### ap...@google.com (2024-04-18)

Project: chromium/src
Branch: main

commit bbb87a89210fcc7d585dee3d66da8b086883988d
Author: Caroline Rising <corising@chromium.org>
Date:   Thu Apr 18 17:19:44 2024

    Make the side panel loading entry pointer a weak pointer.
    
    The loading entry could be destroyed if it is contextual and the tab it
    is associated with is deleted. Making the pointer a weak pointer will
    prevent against trying to use the loading entry if it has been deleted.
    
    Bug: 334110479
    Change-Id: Ic2f736d3fc47739683af49bb8d6a603c633a5f33
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5464066
    Commit-Queue: Caroline Rising <corising@chromium.org>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1289406}

M       chrome/browser/ui/views/side_panel/side_panel_coordinator.cc

https://chromium-review.googlesource.com/5464066


### ma...@google.com (2024-04-19)

> If the comments in [issue 335328453](https://issues.chromium.org/issues/335328453) are correct, this is caused by a change that landed two weeks ago so it wouldn't be in stable.

Sorry, I shouldn't have referred to the Stable channel. But for triage purposes we are interested whether this could affect users by default (i.e. without setting commandline flags or manually turning on feature flags).

Also at least this report seems to contradict that bisection information, possibly because it was a reland?

@Reporter: You were able to reproduce this in 123, correct?

### ad...@google.com (2024-04-19)

@corising thanks for the very quick fix here.

We need to tweak the metadata on this bug in order to make the right merge decisions. Please could you:

- confirm whether or not this bug is reachable without `--enable-features=DataCollectionModeForScreen2x`. (If not, we'll add a special hotlist which prevents emergency merges)
- let us know the earliest version of Chrome where users might have hit this (123? 125?) and please update the `FoundIn` custom field with your answer
- mark the bug as Fixed.

This will then kick off all the right merge procedures to get this fix out to users with the right level of urgency. Thanks!

### co...@chromium.org (2024-04-19)

I tried this out locally on my remote linux build and am not able to reproduce this without `--enable-features=DataCollectionModeForScreen2x`

### ad...@google.com (2024-04-19)

OK thank you, and I assume that this feature is not enabled for any part of the normal stable population via 1% experiments or anything? I assume not, and so I've labeled this Security\_Impact-None.

### pw...@gmail.com (2024-04-22)

Any Reward?

### am...@chromium.org (2024-04-22)

Hello, this bug was only closed as fixed on Friday so it has not been assessed for a potential reward in a VRP Panel session yet. Once that has been done, the reward decision will be communicated directly on bug as per usual.

### pe...@google.com (2024-04-24)

The NextAction date has arrived: 2024-04-24 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### wf...@chromium.org (2024-04-25)

I'm curious how this bug was not found through testing, I see `DataCollectionModeForScreen2x` is enabled in a unit test, but would it be possible to add a browser test for it too?

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations pwn2car! The Chrome VRP Pane has decided to award you $1,000 for this report of a heavily mitigated security bug, mitigated by BRP protection and shutdown. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-07-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/334110479)*
