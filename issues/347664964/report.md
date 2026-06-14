# Security: heap-use-after-free in GetModalDialogBounds

| Field | Value |
|-------|-------|
| **Issue ID** | [347664964](https://issues.chromium.org/issues/347664964) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | tl...@google.com |
| **Created** | 2024-06-17 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Security: heap-use-after-free in GetModalDialogBounds

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

If the "On-device site data" dialog is in a different browser window to the one the tab was opened in, it will keep referencing the old browser window even if it's been closed and freed from memory.

Reproduction steps:

1. Open two tabs (example.com and NTP, for example) in separate browser windows
2. On example.com, click Site info > Tracking protection > Manage on-device site data
3. Move the example.com tab into the other window
4. Mouseover the dialog

ASAN log:

```
=================================================================
==13620==ERROR: AddressSanitizer: heap-use-after-free on address 0x11b84f348530 at pc 0x7ff87562f772 bp 0x007e0f3fce80 sp 0x007e0f3fcec8
READ of size 8 at 0x11b84f348530 thread T0
==13620==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff87562f771 in constrained_window::`anonymous namespace'::GetModalDialogBounds C:\b\s\w\ir\cache\builder\src\components\constrained_window\constrained_window_views.cc:105
    #1 0x7ff87562fa59 in base::internal::Invoker<base::internal::FunctorTraits<const `lambda at ..\..\components\constrained_window\constrained_window_views.cc:260:7' &,views::Widget *const &,web_modal::ModalDialogHost *const &>,base::internal::BindState<0,0,0,`lambda at ..\..\components\constrained_window\constrained_window_views.cc:260:7',base::internal::UnretainedWrapper<views::Widget,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<web_modal::ModalDialogHost,base::unretained_traits::MayNotDangle,0> >,gfx::Rect ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:987
    #2 0x7ff871b2e7f4 in base::RepeatingCallback<gfx::Rect ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344
    #3 0x7ff871b2e332 in views::WidgetDelegate::GetDesiredWidgetBounds C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget_delegate.cc:518
    #4 0x7ff871b47824 in views::Widget::OnRootViewLayoutInvalidated C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1174
    #5 0x7ff871b66f0a in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:982
    #6 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #7 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #8 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #9 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #10 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #11 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #12 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #13 0x7ff871b66ec4 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #14 0x7ff871b855e7 in views::View::PreferredSizeChanged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2247
    #15 0x7ff879bb5052 in views::LinkFragment::RecalculateFont C:\b\s\w\ir\cache\builder\src\ui\views\controls\link_fragment.cc:74
    #16 0x7ff871b7e1a8 in views::View::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1663
    #17 0x7ff8733300a7 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187
    #18 0x7ff87332edae in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:136
    #19 0x7ff87332e21d in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:82
    #20 0x7ff87332dcab in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:54
    #21 0x7ff8758d31d1 in views::internal::RootView::HandleMouseEnteredOrMoved C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:813
    #22 0x7ff871b5534a in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1888
    #23 0x7ff8758c80f9 in views::NativeWidgetAura::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\native_widget_aura.cc:1208
    #24 0x7ff8733300a7 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187
    #25 0x7ff87332edae in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:136
    #26 0x7ff87332e21d in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:82
    #27 0x7ff87332dcab in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:54
    #28 0x7ff879b840dd in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:72
    #29 0x7ff8758b9730 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:119
    #30 0x7ff8758b8ff8 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:134
    #31 0x7ff8758b8b5f in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113
    #32 0x7ff879b80094 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1060
    #33 0x7ff87ef75b19 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3284
    #34 0x7ff87ef74f8c in views::HWNDMessageHandler::HandleMouseMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1154
    #35 0x7ff86cbebe22 in content::LegacyRenderWidgetHostHWND::OnMouseRange C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.cc:351
    #36 0x7ff86cbee59e in content::LegacyRenderWidgetHostHWND::_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.h:92
    #37 0x7ff86cbed05e in content::LegacyRenderWidgetHostHWND::ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.h:85
    #38 0x7ff86cbef6ba in ATL::CWindowImplBaseT<ATL::CWindow,ATL::CWinTraits<1073741824,0> >::WindowProc C:\b\s\w\ir\cache\builder\src\third_party\depot_tools\win_toolchain\vs_files\7393122652\VC\Tools\MSVC\14.39.33519\atlmfc\include\atlwin.h:3571
    #39 0x7ff997f610f1 in AtlThunk_AllocateData+0xe1 (C:\WINDOWS\SYSTEM32\atlthunk.dll+0x1800010f1)
    #40 0x7ff9a97589a0 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x1800189a0)
    #41 0x7ff9a9758460 in DispatchMessageW+0x200 (C:\WINDOWS\System32\USER32.dll+0x180018460)
    #42 0x7ff8720a19a9 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:614
    #43 0x7ff87209f7e5 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:579
    #44 0x7ff87209ece3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:245
    #45 0x7ff87209ca64 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:83
    #46 0x7ff8761b8dcc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:654
    #47 0x7ff87218cfe0 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #48 0x7ff86b24eaa5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1085
    #49 0x7ff86b255ac9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:159
    #50 0x7ff86b24537f in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:34
    #51 0x7ff87088d2f9 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:721
    #52 0x7ff8708902e1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1302
    #53 0x7ff87088fbb2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154
    #54 0x7ff87088b7b4 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #55 0x7ff87088c1ad in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #56 0x7ff86305166d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:228
    #57 0x7ff794ff4228 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #58 0x7ff794ff1dc3 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #59 0x7ff7953de573 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #60 0x7ff9aa13257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
    #61 0x7ff9ab0caa47 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa47)

0x11b84f348530 is located 0 bytes inside of 72-byte region [0x11b84f348530,0x11b84f348578)
freed by thread T0 here:
    #0 0x7ff7950cca2d in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff87943b01b in BrowserViewLayout::WebContentsModalDialogHostViews::~WebContentsModalDialogHostViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:90
    #2 0x7ff879430816 in BrowserViewLayout::~BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:186
    #3 0x7ff87943afdf in BrowserViewLayout::~BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:186
    #4 0x7ff871b63467 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:267
    #5 0x7ff87544ca30 in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:1064
    #6 0x7ff875475479 in BrowserView::`vector deleting destructor'+0x19 (C:\Files\Chromium\Builds\asan-win32-release_x64-1315554\chrome.dll+0x192425479)
    #7 0x7ff871b63861 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:289
    #8 0x7ff8828c45c3 in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:123
    #9 0x7ff8828cd65f in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:123
    #10 0x7ff871b209cc in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:179
    #11 0x7ff871b2292f in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:175
    #12 0x7ff871b67d6a in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3102
    #13 0x7ff871b681a6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:369
    #14 0x7ff871b3707a in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2169
    #15 0x7ff871b34c75 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:251
    #16 0x7ff87938e81f in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:128
    #17 0x7ff8794a72e9 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:318
    #18 0x7ff884fd9a0f in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #19 0x7ff8794a862b in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:393
    #20 0x7ff87ef6e9de in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1103
    #21 0x7ff876f7216c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:310
    #22 0x7ff876f70d9e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #23 0x7ff9a97589a0 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x1800189a0)
    #24 0x7ff9a975865b in DispatchMessageW+0x3fb (C:\WINDOWS\System32\USER32.dll+0x18001865b)
    #25 0x7ff9a9767681 in Ordinal2613+0x61 (C:\WINDOWS\System32\USER32.dll+0x180027681)
    #26 0x7ff9ab113ac3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a3ac3)
    #27 0x7ff9a8c32753 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002753)

previously allocated by thread T0 here:
    #0 0x7ff7950ccb2d in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff8880ffc6e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ff879430482 in BrowserViewLayout::BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:184
    #3 0x7ff87546e5cd in std::__Cr::make_unique<BrowserViewLayout,std::__Cr::unique_ptr<BrowserViewLayoutDelegateImpl,std::__Cr::default_delete<BrowserViewLayoutDelegateImpl> >,BrowserView *,base::raw_ptr<TopContainerView,1> &,base::raw_ptr<WebAppFrameToolbarView,1> &,base::raw_ptr<views::Label,1> &,base::raw_ptr<TabStripRegionView,1> &,base::raw_ptr<TabStrip,1> &,base::raw_ptr<ToolbarView,1> &,base::raw_ptr<InfoBarContainerView,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<SidePanel,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<views::View,1> &,ImmersiveModeController *,base::raw_ptr<views::View,1> &> C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:620
    #4 0x7ff87546cfc6 in BrowserView::AddedToWidget C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:4445
    #5 0x7ff871b92266 in views::View::PropagateAddNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3153
    #6 0x7ff871b8fc8d in views::View::AddChildViewAtImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3025
    #7 0x7ff871b21fa8 in views::NonClientView::ViewHierarchyChanged C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:328
    #8 0x7ff871b918e9 in views::View::ViewHierarchyChangedImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3172
    #9 0x7ff871b92220 in views::View::PropagateAddNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3151
    #10 0x7ff871b8fc8d in views::View::AddChildViewAtImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3025
    #11 0x7ff871b334ac in views::Widget::Init C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:492
    #12 0x7ff87938b13b in BrowserFrame::InitBrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:185
    #13 0x7ff879702839 in BrowserWindow::CreateBrowserWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_window_factory.cc:70
    #14 0x7ff8755c2038 in Browser::Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:641
    #15 0x7ff8755c0617 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:532
    #16 0x7ff879cb7195 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:249
    #17 0x7ff879cb9d0e in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:631
    #18 0x7ff879cb6327 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:448
    #19 0x7ff879cb5462 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:178
    #20 0x7ff875aa0048 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:722
    #21 0x7ff875aa1d78 in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1403
    #22 0x7ff875aa1348 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:821
    #23 0x7ff875a9f76c in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1320
    #24 0x7ff875a9d48a in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:673
    #25 0x7ff875b5c35d in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1801
    #26 0x7ff875b5b283 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1246
    #27 0x7ff86b24b6e8 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:995

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\components\constrained_window\constrained_window_views.cc:105 in constrained_window::`anonymous namespace'::GetModalDialogBounds
Shadow bytes around the buggy address:
  0x11b84f348280: f7 fa fd fd fd fd fd fd fd fd fd fa fa fa f7 fa
  0x11b84f348300: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd
  0x11b84f348380: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x11b84f348400: fd fd fd fd fd fa fa fa f7 fa fd fd fd fd fd fd
  0x11b84f348480: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
=>0x11b84f348500: fd fa fa fa f7 fa[fd]fd fd fd fd fd fd fd fd fa
  0x11b84f348580: fa fa f7 fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x11b84f348600: f7 fa fd fd fd fd fd fd fd fd fd fa fa fa f7 fa
  0x11b84f348680: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd
  0x11b84f348700: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd
  0x11b84f348780: fd fd fd fd fd fa fa fa f7 fa fd fd fd fd fd fd
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

==13620==ADDITIONAL INFO

==13620==Note: Please include this section with the ASan report.
Task trace:


MiraclePtr Status: PROTECTED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==13620==END OF ADDITIONAL INFO
==13620==ABORTING

```
#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker can abuse this memory corruption to potentially execute untrusted code.

---

### The cause

#### What version of Chrome have you found the security issue in?

128.0.6541.0

#### Is the security issue related to a crash?

Yes

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Thomas Orlita

## Attachments

- [poc.webm](attachments/poc.webm) (video/webm, 2.7 MB)

## Timeline

### [Deleted User] (2024-06-17)

Severity: memory corruption in the browser process is S0, but given the odd user interaction required to trigger, downgrading it to S1.

FoundIn: I was able to repro in 128, but the repro was flaky. I wasn't able to repro in 126 or 127. Once the problem has been identified, if it looks like it was introduced before M128, please update the FoundIn to the version where it was introduced.

### pe...@google.com (2024-06-18)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-06-18)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### st...@gmail.com (2024-06-26)

This seems to affect all dialogs constructed using this class.

An alternative way to reproduce the same issue via the Google Lens dialog:

1. Open two tabs in different windows
2. Right-click > Search with Google Lens
3. Drag the tab with the dialog into the other window
4. Mouseover the dialog (specifically the link)

```
=================================================================
==13636==ERROR: AddressSanitizer: heap-use-after-free on address 0x11cbde13db70 at pc 0x7ff874afce92 bp 0x0013219fce40 sp 0x0013219fce88
READ of size 8 at 0x11cbde13db70 thread T0
==13636==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff874afce91 in constrained_window::`anonymous namespace'::GetModalDialogBounds C:\b\s\w\ir\cache\builder\src\components\constrained_window\constrained_window_views.cc:105
    #1 0x7ff874afd179 in base::internal::Invoker<base::internal::FunctorTraits<const `lambda at ..\..\components\constrained_window\constrained_window_views.cc:260:7' &,views::Widget *const &,web_modal::ModalDialogHost *const &>,base::internal::BindState<0,0,0,`lambda at ..\..\components\constrained_window\constrained_window_views.cc:260:7',base::internal::UnretainedWrapper<views::Widget,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<web_modal::ModalDialogHost,base::unretained_traits::MayNotDangle,0> >,gfx::Rect ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:987
    #2 0x7ff870c652f4 in base::RepeatingCallback<gfx::Rect ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344
    #3 0x7ff870c64e32 in views::WidgetDelegate::GetDesiredWidgetBounds C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget_delegate.cc:518
    #4 0x7ff870c7e564 in views::Widget::OnRootViewLayoutInvalidated C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1174
    #5 0x7ff870c9df03 in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:982
    #6 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #7 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #8 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #9 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #10 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #11 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #12 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #13 0x7ff870c9debd in views::View::InvalidateLayout C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:978
    #14 0x7ff870cbc677 in views::View::PreferredSizeChanged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:2247
    #15 0x7ff879373af2 in views::LinkFragment::RecalculateFont C:\b\s\w\ir\cache\builder\src\ui\views\controls\link_fragment.cc:74
    #16 0x7ff870cb5178 in views::View::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1663
    #17 0x7ff8725dec47 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187
    #18 0x7ff8725dd94e in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:136
    #19 0x7ff8725dcdb5 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:82
    #20 0x7ff8725dc84b in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:54
    #21 0x7ff874dba8e0 in views::internal::RootView::HandleMouseEnteredOrMoved C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:813
    #22 0x7ff870c8c07a in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1888
    #23 0x7ff874daf7c9 in views::NativeWidgetAura::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\native_widget_aura.cc:1208
    #24 0x7ff8725dec47 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:187
    #25 0x7ff8725dd94e in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:136
    #26 0x7ff8725dcdb5 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:82
    #27 0x7ff8725dc84b in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:54
    #28 0x7ff879342b9d in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:72
    #29 0x7ff874da0a40 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:119
    #30 0x7ff874da030a in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:134
    #31 0x7ff874d9fe6f in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113
    #32 0x7ff87933eb44 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1060
    #33 0x7ff87ead6eb9 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3284
    #34 0x7ff87ead632c in views::HWNDMessageHandler::HandleMouseMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1154
    #35 0x7ff86bb20202 in content::LegacyRenderWidgetHostHWND::OnMouseRange C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.cc:351
    #36 0x7ff86bb2297e in content::LegacyRenderWidgetHostHWND::_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.h:92
    #37 0x7ff86bb2143e in content::LegacyRenderWidgetHostHWND::ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\legacy_render_widget_host_win.h:85
    #38 0x7ff86bb23a9a in ATL::CWindowImplBaseT<ATL::CWindow,ATL::CWinTraits<1073741824,0> >::WindowProc C:\b\s\w\ir\cache\builder\src\third_party\depot_tools\win_toolchain\vs_files\7393122652\VC\Tools\MSVC\14.39.33519\atlmfc\include\atlwin.h:3571
    #39 0x7ff9993610f1 in AtlThunk_AllocateData+0xe1 (C:\WINDOWS\SYSTEM32\atlthunk.dll+0x1800010f1)
    #40 0x7ff9a97589a0 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x1800189a0)
    #41 0x7ff9a9758460 in DispatchMessageW+0x200 (C:\WINDOWS\System32\USER32.dll+0x180018460)
    #42 0x7ff8711e2727 in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:614
    #43 0x7ff8711e05e2 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:579
    #44 0x7ff8711dfb23 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:245
    #45 0x7ff8711dd708 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:83
    #46 0x7ff8756fcecf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:654
    #47 0x7ff8712e793e in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #48 0x7ff86a0e01e5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1086
    #49 0x7ff86a0e71e9 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:159
    #50 0x7ff86a0d6a0f in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:34
    #51 0x7ff86f81ecd4 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:735
    #52 0x7ff86f82218d in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1318
    #53 0x7ff86f8219dc in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1170
    #54 0x7ff86f81d0bd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:332
    #55 0x7ff86f81db9d in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:345
    #56 0x7ff8619f167f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:228
    #57 0x7ff651333bc8 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:181
    #58 0x7ff651331bcc in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:350
    #59 0x7ff651754163 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #60 0x7ff9aa13257c in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x18001257c)
    #61 0x7ff9ab0caa47 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005aa47)

0x11cbde13db70 is located 0 bytes inside of 72-byte region [0x11cbde13db70,0x11cbde13dbb8)
freed by thread T0 here:
    #0 0x7ff65140f5dd in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff878badceb in BrowserViewLayout::WebContentsModalDialogHostViews::~WebContentsModalDialogHostViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:90
    #2 0x7ff878ba34e6 in BrowserViewLayout::~BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:186
    #3 0x7ff878badcaf in BrowserViewLayout::~BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:186
    #4 0x7ff870c9a387 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:267
    #5 0x7ff8749052e7 in BrowserView::~BrowserView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:1064
    #6 0x7ff87492e089 in BrowserView::`vector deleting destructor'+0x19 (C:\Files\Chromium\Builds\asan-win32-release_x64-1319721\chrome.dll+0x192f3e089)
    #7 0x7ff870c9a781 in views::View::~View C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:289
    #8 0x7ff8826900c3 in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:123
    #9 0x7ff88269914f in BrowserFrameViewWin::~BrowserFrameViewWin C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame_view_win.cc:123
    #10 0x7ff870c56d6c in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:179
    #11 0x7ff870c58cdf in views::NonClientView::~NonClientView C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:175
    #12 0x7ff870c9ed8a in views::View::DoRemoveChildView C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3102
    #13 0x7ff870c9f1d6 in views::View::RemoveAllChildViews C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:369
    #14 0x7ff870c6ddca in views::Widget::DestroyRootView C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2169
    #15 0x7ff870c6b9c5 in views::Widget::~Widget C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:251
    #16 0x7ff878aff67f in BrowserFrame::~BrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:128
    #17 0x7ff878c1a829 in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:318
    #18 0x7ff884e7e9df in DesktopBrowserFrameAura::~DesktopBrowserFrameAura C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\desktop_browser_frame_aura.cc:39
    #19 0x7ff878c1bb7b in views::DesktopNativeWidgetAura::OnHostClosed C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:393
    #20 0x7ff87eacfd3e in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1103
    #21 0x7ff8765c338c in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:310
    #22 0x7ff8765c1f2e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74
    #23 0x7ff9a97589a0 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x1800189a0)
    #24 0x7ff9a975865b in DispatchMessageW+0x3fb (C:\WINDOWS\System32\USER32.dll+0x18001865b)
    #25 0x7ff9a9767681 in Ordinal2613+0x61 (C:\WINDOWS\System32\USER32.dll+0x180027681)
    #26 0x7ff9ab113ac3 in KiUserCallbackDispatcher+0x23 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800a3ac3)
    #27 0x7ff9a8c32753 in NtUserDestroyWindow+0x13 (C:\WINDOWS\System32\win32u.dll+0x180002753)

previously allocated by thread T0 here:
    #0 0x7ff65140f6dd in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff8880717ee in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:36
    #2 0x7ff878ba3152 in BrowserViewLayout::BrowserViewLayout C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view_layout.cc:184
    #3 0x7ff8749270dd in std::__Cr::make_unique<BrowserViewLayout,std::__Cr::unique_ptr<BrowserViewLayoutDelegateImpl,std::__Cr::default_delete<BrowserViewLayoutDelegateImpl> >,BrowserView *,base::raw_ptr<TopContainerView,1> &,base::raw_ptr<WebAppFrameToolbarView,1> &,base::raw_ptr<views::Label,1> &,base::raw_ptr<TabStripRegionView,1> &,base::raw_ptr<TabStrip,1> &,base::raw_ptr<ToolbarView,1> &,base::raw_ptr<InfoBarContainerView,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<SidePanel,1> &,base::raw_ptr<views::View,1> &,base::raw_ptr<views::View,1> &,ImmersiveModeController *,base::raw_ptr<views::View,1> &> C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:620
    #4 0x7ff8749259c2 in BrowserView::AddedToWidget C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_view.cc:4457
    #5 0x7ff870cc9326 in views::View::PropagateAddNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3153
    #6 0x7ff870cc6d43 in views::View::AddChildViewAtImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3025
    #7 0x7ff870c58348 in views::NonClientView::ViewHierarchyChanged C:\b\s\w\ir\cache\builder\src\ui\views\window\non_client_view.cc:328
    #8 0x7ff870cc89a9 in views::View::ViewHierarchyChangedImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3172
    #9 0x7ff870cc92e0 in views::View::PropagateAddNotifications C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3151
    #10 0x7ff870cc6d43 in views::View::AddChildViewAtImpl C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3025
    #11 0x7ff870c69f25 in views::Widget::Init C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:492
    #12 0x7ff878afc130 in BrowserFrame::InitBrowserFrame C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_frame.cc:185
    #13 0x7ff878e950a9 in BrowserWindow::CreateBrowserWindow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser_window_factory.cc:70
    #14 0x7ff874a8dfe2 in Browser::Browser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:643
    #15 0x7ff874a8c2f7 in Browser::Create C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:532
    #16 0x7ff879483d58 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:249
    #17 0x7ff87948694e in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:631
    #18 0x7ff879482efa in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:448
    #19 0x7ff87948206e in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:178
    #20 0x7ff874fa5748 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:722
    #21 0x7ff874fa7593 in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1403
    #22 0x7ff874fa6a48 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:821
    #23 0x7ff874fa4ec3 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1320
    #24 0x7ff874fa2c7a in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:673
    #25 0x7ff875066328 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1801
    #26 0x7ff875065253 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1246
    #27 0x7ff86a0dcdb8 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:996

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\components\constrained_window\constrained_window_views.cc:105 in constrained_window::`anonymous namespace'::GetModalDialogBounds
Shadow bytes around the buggy address:
  0x11cbde13d880: fd fd fd fd fd fa fa fa f7 fa fd fd fd fd fd fd
  0x11cbde13d900: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11cbde13d980: fd fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fa
  0x11cbde13da00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x11cbde13da80: f7 fa fd fd fd fd fd fd fd fd fd fa fa fa f7 fa
=>0x11cbde13db00: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa[fd]fd
  0x11cbde13db80: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x11cbde13dc00: fd fd fd fd fd fd fa fa f7 fa fd fd fd fd fd fd
  0x11cbde13dc80: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd
  0x11cbde13dd00: fd fd fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
  0x11cbde13dd80: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fa fa
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

==13636==ADDITIONAL INFO

==13636==Note: Please include this section with the ASan report.
Task trace:


Command line: `"C:\Files\Chromium\Builds\asan-win32-release_x64-1319721\chrome.exe" --user-data-dir=C:/Files/Chromium/Profiles/p0011 --no-sandbox --enable-features=PermissionElement --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=C:\Files\Chromium\Builds\asan-win32-release_x64-1319721\gen"`


MiraclePtr Status: PROTECTED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==13636==END OF ADDITIONAL INFO
==13636==ABORTING

```

### pe...@google.com (2024-07-02)

tluk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2024-07-12)

[secondary shepherd] tluk@, could you confirm you intend to take a look at this, or if not, could you help re-triage? (will ping as well)

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: main

commit 9929be76cb873917006f13a16f2dfb6bd331da90
Author: Thomas Lukaszewicz <tluk@chromium.org>
Date:   Mon Jul 15 22:34:01 2024

    Close constrained modal dialogs if their host has been destroyed
    
    This CL addresses an issue where a constrained dialog persists after
    its ModalDialogHost has been destroyed.
    
    This is done via the ModalDialogHostObserverViews, attached to the
    modal dialog's Widget that closes the dialog if the host has been
    destroyed. Currently the modal dialog may persist after its host
    has been destroyed, resulting in potential memory corruption / UAFs.
    
    The current constrained web child modal implementation is tied to
    the initial window of the associated WebContents. This should be
    updated in a follow up to follow the WebContents across windows.
    
    Bug: 347664964, 353174863
    Change-Id: I5dc708a8a7784e511991ac376ec9d6cf8a77015f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5705079
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
    Reviewed-by: Allen Bauer <kylixrd@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1327829}

M       chrome/browser/ui/views/constrained_window_views_browsertest.cc
M       components/constrained_window/constrained_window_views.cc
M       ui/views/widget/widget.h

https://chromium-review.googlesource.com/5705079


### am...@chromium.org (2024-07-18)

this issue is a BRP protected UAF and this issue requires substantial and non-standard user interaction, reducing severity to medium

### pe...@google.com (2024-07-24)

Not requesting merge to dev (M128) because latest trunk commit (1327829) appears to be prior to dev branch point (1331488). If this is incorrect please remove NA-128 from the 'Merge' field and add 128 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
for report of heavily mitigated memory corruption in a non-sandboxed process -- mitigated by BRP and significant user interaction 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Congratulations, Thomas! Generally issues mitigated to this extent would not be eligible for a VRP reward; however, we were very impressed with the reporting quality and the clear and concise repro that allowed to to quickly and efficiently investigate and resolve this issue. Thanks for the nice work here!

### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/347664964)*
