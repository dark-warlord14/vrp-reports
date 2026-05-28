# UAF in in Tab::OnMouseReleased(class ui::MouseEvent const &) in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [401393576](https://issues.chromium.org/issues/401393576) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2025-03-07 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
The core issue occurs in the Tab::OnMouseReleased method where the code attempts to access an object after it has been freed.

VERSION
Chromium	136.0.7054.0 (Developer Build) (64-bit) 
OS	Windows 11 Version 24H2 (Build 26120.3360)

REPRODUCTION CASE
1. visit an windows 11/10 via RDP(mstsc.exe) （Affected by the network)
2. triggers a preview tab and click in the preview tab
3. close the activated preview tab with mouse wheel button(Sometimes click x in the tabs also will trigger this issue).
See the poc.gif.

PS: I first catch this crash via the initiatePreview(url.mojom.Url) method in the mojo blink.mojom.SpeculationHostPtr() interface to visit a unknown webpage however it cannot be reproduced.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [ browser.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]
=================================================================
==31108==ERROR: AddressSanitizer: heap-use-after-free on address 0x120457eba8ef at pc 0x7fff0700ebf6 bp 0x00be21bf9960 sp 0x00be21bf99a8
WRITE of size 1 at 0x120457eba8ef thread T0
    #0 0x7fff0700ebf5 in Tab::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:606:1
    #1 0x7ffef1951c04 in views::View::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1660:9
    #2 0x7ffef5b1ad26 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #3 0x7ffef5b19845 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #4 0x7ffef5b18c8c in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #5 0x7ffef5b1861a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #6 0x7ffef191f852 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:626:9
    #7 0x7ffef190da7b in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2082:20
    #8 0x7ffef1833a57 in views::DesktopNativeWidgetAura::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1400:30
    #9 0x7ffef5b1ad26 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #10 0x7ffef5b19845 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #11 0x7ffef5b18c8c in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #12 0x7ffef5b1861a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #13 0x7ffef5b13b74 in ui::EventProcessor::OnEventFromSource(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:72:19
    #14 0x7ffef5b12de0 in ui::EventSource::DeliverEventToSink(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:119:16
    #15 0x7ffef5b126af in ui::EventSource::SendEventToSinkFromRewriter(class ui::Event const *, class ui::EventRewriter const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:134:12
    #16 0x7ffef5b1229f in ui::EventSource::SendEventToSink(class ui::Event const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113:10
    #17 0x7ffef1823344 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1186:3
    #18 0x7ffef18a4ba0 in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned __int64, __int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3302:26
    #19 0x7ffef189e028 in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:2156
    #20 0x7ffef189e028 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:390:5
    #21 0x7ffef189d77d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1111:7
    #22 0x7ffef570993c in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:311:18
    #23 0x7ffef570842e in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #24 0x7fffd8edb642  (C:\WINDOWS\System32\USER32.dll+0x18000b642)
    #25 0x7fffd8ed91cc  (C:\WINDOWS\System32\USER32.dll+0x1800091cc)
    #26 0x7ffef2fcea87 in base::MessagePumpForUI::ProcessMessageHelper(struct tagMSG const &) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:629:3
    #27 0x7ffef2fcc8f2 in base::MessagePumpForUI::ProcessNextWindowsMessage(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:591:31
    #28 0x7ffef2fcbde6 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:251:33
    #29 0x7ffef2fc96f8 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:88:3
    #30 0x7ffef311e9c1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #31 0x7ffef31aa42e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #32 0x7ffee9fe45dd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1089:18
    #33 0x7ffee9febdc9 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15
    #34 0x7ffee9fdb07c in content::BrowserMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32:28
    #35 0x7ffeefdefbc9 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:716:10
    #36 0x7ffeefdf2b7c in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1296:10
    #37 0x7ffeefdf2399 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1151:12
    #38 0x7ffeefde6535 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #39 0x7ffeefde70dd in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #40 0x7ffee0b016b4 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #41 0x7ff7be14472d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #42 0x7ff7be141fda in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #43 0x7ff7be7b628b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #44 0x7ff7be7b628b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #45 0x7fffd915e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #46 0x7fffda33197b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800b197b)

0x120457eba8ef is located 1391 bytes inside of 1456-byte region [0x120457eba380,0x120457eba930)
freed by thread T0 here:
    #0 0x7fff36d8ae5d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005ae5d)
    #1 0x7fff0701344b in views::View::operator delete C:\b\s\w\ir\cache\builder\src\ui\views\view.h:296
    #2 0x7fff0701344b in Tab::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:290:13
    #3 0x7ffef1feb621 in std::__Cr::unique_ptr<gfx::AnimationDelegate,std::__Cr::default_delete<gfx::AnimationDelegate> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:284
    #4 0x7ffef1feb621 in views::BoundsAnimator::CleanupData C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:233
    #5 0x7ffef1feb621 in views::BoundsAnimator::AnimationEndedOrCanceled(class gfx::Animation const *, enum views::BoundsAnimator::AnimationEndType) C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:301:3
    #6 0x7ffef1fe947c in views::BoundsAnimator::AnimateViewTo(class views::View *, class gfx::Rect const &, class std::__Cr::unique_ptr<class gfx::AnimationDelegate, struct std::__Cr::default_delete<class gfx::AnimationDelegate>>) C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:118:19
    #7 0x7fff07064fc0 in TabContainerImpl::AnimateViewTo C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:1158
    #8 0x7fff07064fc0 in TabContainerImpl::StartRemoveTabAnimation(class Tab *, int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:1314:3
    #9 0x7fff07063f29 in TabContainerImpl::RemoveTab(int, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:202:3
    #10 0x7fff07093e7b in TabStrip::RemoveTabAt(class content::WebContents *, int, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1195:19
    #11 0x7fff071383ba in BrowserTabStripController::OnTabStripModelChanged(class TabStripModel *, class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:771:20
    #12 0x7ffeeffc2aa5 in TabStripModel::OnChange(class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:429:14
    #13 0x7ffeeffc4df0 in TabStripModel::SendDetachWebContentsNotifications(struct TabStripModel::DetachNotifications *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:680:5
    #14 0x7ffeeffd3732 in TabStripModel::CloseTabs(class base::span<class content::WebContents *const, -1, class content::WebContents *const *>, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2564:5
    #15 0x7ffeeffd5033 in TabStripModel::CloseWebContentsAt(int, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:960:3
    #16 0x7fff071344f5 in BrowserTabStripController::CloseTab(int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:458:11
    #17 0x7fff0709b7a9 in TabStrip::CloseTabInternal(int, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:2208:16
    #18 0x7fff070aa528 in base::internal::DecayedFunctorTraits<void (TabStrip::*)(int, CloseTabSource),TabStrip *,int &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #19 0x7fff070aa528 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (TabStrip::*&&)(int, CloseTabSource),TabStrip *,int &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #20 0x7fff070aa528 in base::internal::Invoker<base::internal::FunctorTraits<void (TabStrip::*&&)(int, CloseTabSource),TabStrip *,int &&>,base::internal::BindState<1,1,0,void (TabStrip::*)(int, CloseTabSource),base::internal::UnretainedWrapper<TabStrip,base::unretained_traits::MayNotDangle,0>,int>,void (CloseTabSource)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #21 0x7fff070aa528 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl TabStrip::*&&)(int, enum CloseTabSource), class TabStrip *, int &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl TabStrip::*)(int, enum CloseTabSource), class base::internal::UnretainedWrapper<class TabStrip, struct base::unretained_traits::MayNotDangle, 0>, int>, (enum CloseTabSource)>::RunOnce(class base::internal::BindStateBase *, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #22 0x7fff07133d61 in base::OnceCallback<void (CloseTabSource)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #23 0x7fff07133d61 in BrowserTabStripController::OnCloseTab(int, enum CloseTabSource, class base::OnceCallback<(enum CloseTabSource)>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:439:25
    #24 0x7fff0709b02d in TabStrip::CloseTab(class Tab *, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1640:18
    #25 0x7fff0700e8f4 in Tab::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:584:20
    #26 0x7ffef1951c04 in views::View::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1660:9
    #27 0x7ffef5b1ad26 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #28 0x7ffef5b19845 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #29 0x7ffef5b18c8c in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #30 0x7ffef5b1861a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #31 0x7ffef191f852 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:626:9
    #32 0x7ffef190da7b in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2082:20
    #33 0x7ffef1833a57 in views::DesktopNativeWidgetAura::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1400:30
    #34 0x7ffef5b1ad26 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #35 0x7ffef5b19845 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5

previously allocated by thread T0 here:
    #0 0x7fff36d8a63d  (C:\chromium_version\latest_asan\clang_rt.asan_dynamic-x86_64.dll+0x18005a63d)
    #1 0x7fff070921e6 in views::View::operator new C:\b\s\w\ir\cache\builder\src\ui\views\view.h:296
    #2 0x7fff070921e6 in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754
    #3 0x7fff070921e6 in TabStrip::AddTabsAt(class std::__Cr::vector<struct std::__Cr::pair<int, struct TabRendererData>, class std::__Cr::allocator<struct std::__Cr::pair<int, struct TabRendererData>>>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1116:9
    #4 0x7fff07132267 in BrowserTabStripController::AddTabs(class std::__Cr::vector<struct std::__Cr::pair<class content::WebContents *, int>, class std::__Cr::allocator<struct std::__Cr::pair<class content::WebContents *, int>>>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:972:14
    #5 0x7fff07138531 in BrowserTabStripController::OnTabStripModelChanged(class TabStripModel *, class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:765:7
    #6 0x7ffeeffc2aa5 in TabStripModel::OnChange(class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:429:14
    #7 0x7ffeefff0cb7 in TabStripModel::InsertTabAtIndexImpl(class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, class std::__Cr::optional<class tab_groups::TabGroupId>, bool, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:3110:3
    #8 0x7ffeeffc13ce in TabStripModel::InsertTabAtImpl(int, class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, class std::__Cr::optional<class tab_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2508:3
    #9 0x7ffeeffdaef8 in TabStripModel::AddTab(class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, enum ui::PageTransition, int, class std::__Cr::optional<class tab_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1289:3
    #10 0x7fff07cf6b5f in Navigate(struct NavigateParams *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:941:41
    #11 0x7fff07cefbdf in chrome::AddWebContents(class Browser *, class content::WebContents *, class std::__Cr::unique_ptr<class content::WebContents, struct std::__Cr::default_delete<class content::WebContents>>, class GURL const &, enum WindowOpenDisposition, class blink::mojom::WindowFeatures const &, enum NavigateParams::WindowAction, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_tabstrip.cc:103:3
    #12 0x7fff07d6c473 in Browser::AddNewContents(class content::WebContents *, class std::__Cr::unique_ptr<class content::WebContents, struct std::__Cr::default_delete<class content::WebContents>>, class GURL const &, enum WindowOpenDisposition, class blink::mojom::WindowFeatures const &, bool, bool *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser.cc:2103:10
    #13 0x7fff07d5152c in PreviewTab::PromoteToNewTab(class content::WebContents &) C:\b\s\w\ir\cache\builder\src\chrome\browser\preloading\preview\preview_tab.cc:196:13
    #14 0x7fff07d54263 in PreviewManager::PromoteToNewTab(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\preloading\preview\preview_manager.cc:65:9
    #15 0x7fff07d5085d in PreviewTab::AuditWebInputEvent(class blink::WebInputEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\preloading\preview\preview_tab.cc:139:23
    #16 0x7fff07d52cc8 in base::internal::DecayedFunctorTraits<bool (PreviewTab::*)(const blink::WebInputEvent &),PreviewTab *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #17 0x7fff07d52cc8 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<bool (PreviewTab::*const &)(const blink::WebInputEvent &),PreviewTab *>,bool,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:923
    #18 0x7fff07d52cc8 in base::internal::Invoker<base::internal::FunctorTraits<bool (PreviewTab::*const &)(const blink::WebInputEvent &),PreviewTab *>,base::internal::BindState<1,1,0,bool (PreviewTab::*)(const blink::WebInputEvent &),base::internal::UnretainedWrapper<PreviewTab,base::unretained_traits::MayNotDangle,0> >,bool (const blink::WebInputEvent &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #19 0x7fff07d52cc8 in base::internal::Invoker<struct base::internal::FunctorTraits<bool (__cdecl PreviewTab::*const &)(class blink::WebInputEvent const &), class PreviewTab *>, struct base::internal::BindState<1, 1, 0, bool (__cdecl PreviewTab::*)(class blink::WebInputEvent const &), class base::internal::UnretainedWrapper<class PreviewTab, struct base::unretained_traits::MayNotDangle, 0>>, (class blink::WebInputEvent const &)>::Run(class base::internal::BindStateBase *, class blink::WebInputEvent const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:980:12
    #20 0x7ffeeba223cd in base::RepeatingCallback<(class blink::WebInputEvent const &)>::Run(class blink::WebInputEvent const &) const & C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:344:12
    #21 0x7ffeeba2217b in content::WebContentsImpl::ShouldIgnoreWebInputEvents(class blink::WebInputEvent const &) C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:9832:26
    #22 0x7ffeeb424c6f in content::RenderWidgetHostImpl::IsIgnoringWebInputEvents(class blink::WebInputEvent const &) const C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_impl.cc:3385:21
    #23 0x7ffeeb407c8d in content::RenderWidgetHostImpl::ForwardMouseEventWithLatencyInfo(class blink::WebMouseEvent const &, class ui::LatencyInfo const &) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_impl.cc:1569:7
    #24 0x7ffeeb4656e0 in content::RenderWidgetHostViewBase::ProcessMouseEvent(class blink::WebMouseEvent const &, class ui::LatencyInfo const &) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_view_base.cc:671:11
    #25 0x7ffefa038223 in input::RenderWidgetHostInputEventRouter::DispatchMouseEvent(class input::RenderWidgetHostViewInput *, class input::RenderWidgetHostViewInput *, class blink::WebMouseEvent const &, class ui::LatencyInfo const &, class std::__Cr::optional<class gfx::PointF> const &) C:\b\s\w\ir\cache\builder\src\components\input\render_widget_host_input_event_router.cc:702:11
    #26 0x7ffefa045b37 in input::RenderWidgetHostInputEventRouter::DispatchEventToTarget(class input::RenderWidgetHostViewInput *, class input::RenderWidgetHostViewInput *, class blink::WebInputEvent *, class ui::LatencyInfo const &, class std::__Cr::optional<class gfx::PointF> const &) C:\b\s\w\ir\cache\builder\src\components\input\render_widget_host_input_event_router.cc:2078:5
    #27 0x7ffefa029eac in input::RenderWidgetTargeter::FoundTarget(class input::RenderWidgetHostViewInput *, class std::__Cr::optional<class gfx::PointF> const &, class input::RenderWidgetTargeter::TargetingRequest *) C:\b\s\w\ir\cache\builder\src\components\input\render_widget_targeter.cc:391:16
    #28 0x7ffefa027c91 in input::RenderWidgetTargeter::ResolveTargetingRequest(class input::RenderWidgetTargeter::TargetingRequest) C:\b\s\w\ir\cache\builder\src\components\input\render_widget_targeter.cc:226:5
    #29 0x7ffefa0271c0 in input::RenderWidgetTargeter::FindTargetAndDispatch(class input::RenderWidgetHostViewInput *, class blink::WebInputEvent const &, class ui::LatencyInfo const &) C:\b\s\w\ir\cache\builder\src\components\input\render_widget_targeter.cc:164:3
    #30 0x7ffeebe1c49f in content::RenderWidgetHostViewEventHandler::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_view_event_handler.cc:370:51
    #31 0x7ffeeb44f80c in content::RenderWidgetHostViewAura::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_widget_host_view_aura.cc:2254:19
    #32 0x7ffef5b1ad26 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:606:1 in Tab::OnMouseReleased(class ui::MouseEvent const &)
Shadow bytes around the buggy address:
  0x120457eba600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x120457eba680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x120457eba700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x120457eba780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x120457eba800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x120457eba880: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd
  0x120457eba900: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x120457eba980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x120457ebaa00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x120457ebaa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x120457ebab00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==31108==ADDITIONAL INFO

==31108==Note: Please include this section with the ASan report.
Task trace:


Command line: `chrome --user-data-dir=c:/tmp/test --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=C:\chromium_version\latest_asan\gen" https://example.com`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==31108==END OF ADDITIONAL INFO
==31108==ABORTING


## Attachments

- [poc.gif](attachments/poc.gif) (image/gif, 7.9 MB)

## Timeline

### ph...@chromium.org (2025-03-07)

I tried a few times on linux M136 ASAN but can't repro. I'll try to get a Windows ASAN and try again.

### ph...@chromium.org (2025-03-07)

I can reproduce on a M136 ASAN on Chrome.

### ph...@chromium.org (2025-03-07)

Setting to Medium severity because this still requires certain user interaction.

### ph...@chromium.org (2025-03-07)

Actually since this is still a UAF in the browser process, setting the priority to High.

### ph...@chromium.org (2025-03-07)

I was not able to repro in M134 but I did repro in M135 just by middle clicking a tab (not opened by preview link).

```
C:\Users\phao\Downloads\chromium-135.0.7049.3-win64-asan> ./chrome --user-data-dir=c:/tmp/test --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=C:\chromium_version\latest_asan\gen" https://example.com
[16328:13816:0307/111213.609:ERROR:sandbox_win.cc(762)] Sandbox cannot access executable. Check filesystem permissions are valid. See https://bit.ly/31yqMJR.: Access is denied. (0x5)
[16328:18292:0307/111216.079:ERROR:network_service_instance_impl.cc(612)] Network service crashed, restarting service.
[16328:18292:0307/111222.587:ERROR:fm_registration_token_uploader.cc(179)] Client is missing for kUser scope
[16328:18292:0307/111222.587:ERROR:fm_registration_token_uploader.cc(179)] Client is missing for kUser scope
[16328:12108:0307/111250.476:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT
[16328:12108:0307/111315.175:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==16328==ERROR: AddressSanitizer: heap-use-after-free on address 0x12f45473acef at pc 0x7ffef84d6c36 bp 0x00cd945f9d80 sp 0x00cd945f9dc8
WRITE of size 1 at 0x12f45473acef thread T0
    #0 0x7ffef84d6c35 in Tab::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:606:1
    #1 0x7ffee2f56584 in views::View::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1660:9
    #2 0x7ffee7065376 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #3 0x7ffee7063e95 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #4 0x7ffee70632dc in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #5 0x7ffee7062c6a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #6 0x7ffee2f241d2 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:626:9
    #7 0x7ffee2f123fb in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2082:20
    #8 0x7ffee2e38427 in views::DesktopNativeWidgetAura::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1400:30
    #9 0x7ffee7065376 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #10 0x7ffee7063e95 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #11 0x7ffee70632dc in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #12 0x7ffee7062c6a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #13 0x7ffee705e1c4 in ui::EventProcessor::OnEventFromSource(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_processor.cc:72:19
    #14 0x7ffee705d430 in ui::EventSource::DeliverEventToSink(class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:119:16
    #15 0x7ffee705ccff in ui::EventSource::SendEventToSinkFromRewriter(class ui::Event const *, class ui::EventRewriter const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:134:12
    #16 0x7ffee705c8ef in ui::EventSource::SendEventToSink(class ui::Event const *) C:\b\s\w\ir\cache\builder\src\ui\events\event_source.cc:113:10
    #17 0x7ffee2e27d14 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:1186:3
    #18 0x7ffee2ea9550 in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned __int64, __int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:3302:26
    #19 0x7ffee2ea29d8 in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:2156
    #20 0x7ffee2ea29d8 in views::HWNDMessageHandler::_ProcessWindowMessage(struct HWND__*, unsigned int, unsigned __int64, __int64, __int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.h:390:5
    #21 0x7ffee2ea212d in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd_message_handler.cc:1111:7
    #22 0x7ffee6c369bc in gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window_impl.cc:311:18
    #23 0x7ffee6c354ae in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND__*, unsigned int, unsigned __int64, __int64)>(struct HWND__*, unsigned int, unsigned __int64, __int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped_window_proc.h:74:10
    #24 0x7fff8315ef5b  (C:\Windows\System32\USER32.dll+0x18000ef5b)
    #25 0x7fff8315e683  (C:\Windows\System32\USER32.dll+0x18000e683)
    #26 0x7ffee45d0ed7 in base::MessagePumpForUI::ProcessMessageHelper(struct tagMSG const &) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:629:3
    #27 0x7ffee45ced42 in base::MessagePumpForUI::ProcessNextWindowsMessage(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:591:31
    #28 0x7ffee45ce236 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:251:33
    #29 0x7ffee45cbb48 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:88:3
    #30 0x7ffee4720be1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #31 0x7ffee47ac61e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #32 0x7ffedb61c2bd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1089:18
    #33 0x7ffedb623aa9 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:156:15
    #34 0x7ffedb612d5c in content::BrowserMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:32:28
    #35 0x7ffee140a909 in content::RunBrowserProcessMain(struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:716:10
    #36 0x7ffee140d8bc in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams, bool) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1296:10
    #37 0x7ffee140d0d9 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1151:12
    #38 0x7ffee1401275 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #39 0x7ffee1401e1d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #40 0x7ffed21816b4 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #41 0x7ff656f9472d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #42 0x7ff656f91fda in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #43 0x7ff65760380b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #44 0x7ff65760380b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #45 0x7fff83f27373  (C:\Windows\System32\KERNEL32.DLL+0x180017373)
    #46 0x7fff8503cc90  (C:\Windows\SYSTEM32\ntdll.dll+0x18004cc90)

0x12f45473acef is located 1391 bytes inside of 1456-byte region [0x12f45473a780,0x12f45473ad30)
freed by thread T0 here:
    #0 0x7fff3ad5ae5d  (C:\Users\phao\Downloads\chromium-135.0.7049.3-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005ae5d)
    #1 0x7ffef84db48b in views::View::operator delete C:\b\s\w\ir\cache\builder\src\ui\views\view.h:296
    #2 0x7ffef84db48b in Tab::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:290:13
    #3 0x7ffee35efa41 in std::__Cr::unique_ptr<gfx::AnimationDelegate,std::__Cr::default_delete<gfx::AnimationDelegate> >::reset C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:284
    #4 0x7ffee35efa41 in views::BoundsAnimator::CleanupData C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:233
    #5 0x7ffee35efa41 in views::BoundsAnimator::AnimationEndedOrCanceled(class gfx::Animation const *, enum views::BoundsAnimator::AnimationEndType) C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:301:3
    #6 0x7ffee35ed89c in views::BoundsAnimator::AnimateViewTo(class views::View *, class gfx::Rect const &, class std::__Cr::unique_ptr<class gfx::AnimationDelegate, struct std::__Cr::default_delete<class gfx::AnimationDelegate>>) C:\b\s\w\ir\cache\builder\src\ui\views\animation\bounds_animator.cc:118:19
    #7 0x7ffef852cdf0 in TabContainerImpl::AnimateViewTo C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:1158
    #8 0x7ffef852cdf0 in TabContainerImpl::StartRemoveTabAnimation(class Tab *, int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:1314:3
    #9 0x7ffef852bd59 in TabContainerImpl::RemoveTab(int, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_container_impl.cc:202:3
    #10 0x7ffef855bcab in TabStrip::RemoveTabAt(class content::WebContents *, int, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1195:19
    #11 0x7ffef85ffc4a in BrowserTabStripController::OnTabStripModelChanged(class TabStripModel *, class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:771:20
    #12 0x7ffee15d9f55 in TabStripModel::OnChange(class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:429:14
    #13 0x7ffee15dc2a0 in TabStripModel::SendDetachWebContentsNotifications(struct TabStripModel::DetachNotifications *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:680:5
    #14 0x7ffee15eabe2 in TabStripModel::CloseTabs(class base::span<class content::WebContents *const, -1, class content::WebContents *const *>, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2560:5
    #15 0x7ffee15ec4e3 in TabStripModel::CloseWebContentsAt(int, unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:960:3
    #16 0x7ffef85fbd85 in BrowserTabStripController::CloseTab(int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:458:11
    #17 0x7ffef8563559 in TabStrip::CloseTabInternal(int, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:2203:16
    #18 0x7ffef85722d8 in base::internal::DecayedFunctorTraits<void (TabStrip::*)(int, CloseTabSource),TabStrip *,int &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:728
    #19 0x7ffef85722d8 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (TabStrip::*&&)(int, CloseTabSource),TabStrip *,int &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
    #20 0x7ffef85722d8 in base::internal::Invoker<base::internal::FunctorTraits<void (TabStrip::*&&)(int, CloseTabSource),TabStrip *,int &&>,base::internal::BindState<1,1,0,void (TabStrip::*)(int, CloseTabSource),base::internal::UnretainedWrapper<TabStrip,base::unretained_traits::MayNotDangle,0>,int>,void (CloseTabSource)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
    #21 0x7ffef85722d8 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl TabStrip::*&&)(int, enum CloseTabSource), class TabStrip *, int &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl TabStrip::*)(int, enum CloseTabSource), class base::internal::UnretainedWrapper<class TabStrip, struct base::unretained_traits::MayNotDangle, 0>, int>, (enum CloseTabSource)>::RunOnce(class base::internal::BindStateBase *, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
    #22 0x7ffef85fb5f1 in base::OnceCallback<void (CloseTabSource)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #23 0x7ffef85fb5f1 in BrowserTabStripController::OnCloseTab(int, enum CloseTabSource, class base::OnceCallback<(enum CloseTabSource)>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:439:25
    #24 0x7ffef8562ddd in TabStrip::CloseTab(class Tab *, enum CloseTabSource) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1635:18
    #25 0x7ffef84d6934 in Tab::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:584:20
    #26 0x7ffee2f56584 in views::View::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:1660:9
    #27 0x7ffee7065376 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #28 0x7ffee7063e95 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5
    #29 0x7ffee70632dc in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:84:14
    #30 0x7ffee7062c6a in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:56:15
    #31 0x7ffee2f241d2 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:626:9
    #32 0x7ffee2f123fb in views::Widget::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:2082:20
    #33 0x7ffee2e38427 in views::DesktopNativeWidgetAura::OnMouseEvent(class ui::MouseEvent *) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop_aura\desktop_native_widget_aura.cc:1400:30
    #34 0x7ffee7065376 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:189:12
    #35 0x7ffee7063e95 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget *, class ui::Event *) C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:138:5

previously allocated by thread T0 here:
    #0 0x7fff3ad5a63d  (C:\Users\phao\Downloads\chromium-135.0.7049.3-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005a63d)
    #1 0x7ffef855a016 in views::View::operator new C:\b\s\w\ir\cache\builder\src\ui\views\view.h:296
    #2 0x7ffef855a016 in std::__Cr::make_unique C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\unique_ptr.h:754
    #3 0x7ffef855a016 in TabStrip::AddTabsAt(class std::__Cr::vector<struct std::__Cr::pair<int, struct TabRendererData>, class std::__Cr::allocator<struct std::__Cr::pair<int, struct TabRendererData>>>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1116:9
    #4 0x7ffef85f9af7 in BrowserTabStripController::AddTabs(class std::__Cr::vector<struct std::__Cr::pair<class content::WebContents *, int>, class std::__Cr::allocator<struct std::__Cr::pair<class content::WebContents *, int>>>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:964:14
    #5 0x7ffef85ffdc1 in BrowserTabStripController::OnTabStripModelChanged(class TabStripModel *, class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:765:7
    #6 0x7ffee15d9f55 in TabStripModel::OnChange(class TabStripModelChange const &, struct TabStripSelectionChange const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:429:14
    #7 0x7ffee1608127 in TabStripModel::InsertTabAtIndexImpl(class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, class std::__Cr::optional<class tab_groups::TabGroupId>, bool, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:3106:3
    #8 0x7ffee15d887e in TabStripModel::InsertTabAtImpl(int, class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, class std::__Cr::optional<class tab_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2504:3
    #9 0x7ffee15f23a8 in TabStripModel::AddTab(class std::__Cr::unique_ptr<class tabs::TabModel, struct std::__Cr::default_delete<class tabs::TabModel>>, int, enum ui::PageTransition, int, class std::__Cr::optional<class tab_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1289:3
    #10 0x7ffef91b9d2f in Navigate(struct NavigateParams *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:941:41
    #11 0x7ffef90eb5c6 in StartupBrowserCreatorImpl::OpenTabsInBrowser(class Browser *, enum chrome::startup::IsProcessStartup, class std::__Cr::vector<struct StartupTab, class std::__Cr::allocator<struct StartupTab>> const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:299:5
    #12 0x7ffef90ede5c in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(class std::__Cr::vector<struct StartupTab, class std::__Cr::allocator<struct StartupTab>> const &, enum StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, enum chrome::startup::IsProcessStartup, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:611:13
    #13 0x7ffef90ea48b in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(enum chrome::startup::IsProcessStartup, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:423:22
    #14 0x7ffef90e974d in StartupBrowserCreatorImpl::Launch(class Profile *, enum chrome::startup::IsProcessStartup, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:155:3
    #15 0x7ffef90f8efd in StartupBrowserCreator::LaunchBrowser(class base::CommandLine const &, class Profile *, class base::FilePath const &, enum chrome::startup::IsProcessStartup, enum chrome::startup::IsFirstRun, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:739:9
    #16 0x7ffef90fa07b in StartupBrowserCreator::LaunchBrowserForLastProfiles(class base::CommandLine const &, class base::FilePath const &, enum chrome::startup::IsProcessStartup, enum chrome::startup::IsFirstRun, struct StartupProfileInfo, class std::__Cr::vector<class Profile *, class std::__Cr::allocator<class Profile *>> const &, bool) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:820:7
    #17 0x7ffef90f85e6 in StartupBrowserCreator::ProcessCmdLineImpl(class base::CommandLine const &, class base::FilePath const &, enum chrome::startup::IsProcessStartup, struct StartupProfileInfo, class std::__Cr::vector<class Profile *, class std::__Cr::allocator<class Profile *>> const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1330:5
    #18 0x7ffef90fd628 in StartupBrowserCreator::ProcessCommandLineWithProfile(class base::CommandLine const &, class base::FilePath const &, enum StartupProfileMode, class Profile *) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1498:27
    #19 0x7ffef90fd8a3 in StartupBrowserCreator::ProcessCommandLineAlreadyRunning(class base::CommandLine const &, class base::FilePath const &, struct StartupProfilePathInfo const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1528:3
    #20 0x7ffee427fd87 in `anonymous namespace'::ProcessSingletonNotificationCallbackImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:463:3
    #21 0x7ffee4282468 in base::internal::DecayedFunctorTraits<void (*)(base::CommandLine, const base::FilePath &),base::CommandLine &&,base::FilePath &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:661
    #22 0x7ffee4282468 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(base::CommandLine, const base::FilePath &),base::CommandLine &&,base::FilePath &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:920
    #23 0x7ffee4282468 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::CommandLine, const base::FilePath &),base::CommandLine &&,base::FilePath &&>,base::internal::BindState<0,1,0,void (*)(base::CommandLine, const base::FilePath &),base::CommandLine,base::FilePath>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1057
    #24 0x7ffee4282468 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *&&)(class base::CommandLine, class base::FilePath const &), class base::CommandLine &&, class base::FilePath &&>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(class base::CommandLine, class base::FilePath const &), class base::CommandLine, class base::FilePath>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:970:12
    #25 0x7ffee474a143 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #26 0x7ffee474a143 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #27 0x7ffee471eef4 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #28 0x7ffee471eef4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #29 0x7ffee471dd6f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #30 0x7ffee45ce390 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:261:67
    #31 0x7ffee45cbb48 in base::MessagePumpWin::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:88:3
    #32 0x7ffee4720be1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #33 0x7ffee47ac61e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #34 0x7ffedb61c2bd in content::BrowserMainLoop::RunMainMessageLoop(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1089:18

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab.cc:606:1 in Tab::OnMouseReleased(class ui::MouseEvent const &)
Shadow bytes around the buggy address:
  0x12f45473aa00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12f45473aa80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12f45473ab00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12f45473ab80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12f45473ac00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x12f45473ac80: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd
  0x12f45473ad00: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x12f45473ad80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x12f45473ae00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x12f45473ae80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x12f45473af00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==16328==ADDITIONAL INFO

==16328==Note: Please include this section with the ASan report.
Task trace:


Command line: `"C:\Users\phao\Downloads\chromium-135.0.7049.3-win64-asan\chrome.exe" --user-data-dir=c:/tmp/test --flag-switches-begin --flag-switches-end --file-url-path-alias="/gen=C:\chromium_version\latest_asan\gen" --flag-switches-begin --flag-switches-end https://example.com`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==16328==END OF ADDITIONAL INFO
==16328==ABORTING

```

### ph...@chromium.org (2025-03-07)

CC'ed a few people who last touched the OnMouseReleased function and some related owners.

emshack@: Could you please help find the right person to take a look at this high severity security bug?

### em...@chromium.org (2025-03-07)

I'm not able to reproduce this by middle clicking a tab header (tried on Mac and Windows), and this issue doesn't look related to my change. Tentatively reassigning to tbergquist@, whose similarly recent change was more extensive and did touch the middle click code path (though the changes to that file don't seem related).

### ke...@chromium.org (2025-03-07)

This is a UaF in tabs.cc, `Tab::OnMouseReleased()`. The tab object (i.e. `this` pointer) is destroyed by `CloseTab()` and after returning from the call, it touches `shift_pressed_on_mouse_down_` member variable.

```
void Tab::OnMouseReleased(const ui::MouseEvent& event) {

  ... 
  if (event.IsOnlyMiddleMouseButton()) {
    if (HitTestPoint(event.location())) {
      // CloseTabs() deletes Tab on animation finishes. If the animation is disabled, 
      // Tab is deleted immediately.
      controller_->CloseTab(this, CloseTabSource::kFromMouse);
      ... 
  }
  // BOOM, `this` could be already dead.
  shift_pressed_on_mouse_down_ = false;
}

```

I think the key to reproduce is to disable the animation. There does not seem to have a command line for this. This is controlled by `Animation::ShouldRenderRichAnimationImpl()` where RDP is detected. The quickest way to hack will be to override the function in a local build.

### em...@chromium.org (2025-03-07)

Ok, reassigning to myself in that case, I can take a look

### ap...@google.com (2025-03-07)

Project: chromium/src  

Branch: main  

Author: Emily Shack <[emshack@chromium.org](mailto:emshack@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6336893>

Fix UAF on tab mouse release

---


Expand for full commit details
```
Fix UAF on tab mouse release 
 
Bug: 401393576 
Change-Id: I03df46dd83ca1c792fe419f9cc8c4ec01a2575ab 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6336893 
Reviewed-by: Keren Zhu <kerenzhu@chromium.org> 
Commit-Queue: Emily Shack <emshack@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1429754}

```

---

Files:

- M `chrome/browser/ui/views/tabs/tab.cc`

---

Hash: d2a73990438a84199f658a671c2a2c93e360d7a7  

Date:  Fri Mar 07 14:18:29 2025


---

### ch...@google.com (2025-03-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-08)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-03-08)

**Merge approved:** your change passed merge requirements and is auto-approved for M135. Please go ahead and merge the CL to branch 7049 (refs/branch-heads/7049) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ap...@google.com (2025-03-10)

Project: chromium/src  

Branch: refs/branch-heads/7049  

Author: Emily Shack <[emshack@chromium.org](mailto:emshack@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6339490>

[M135] Fix UAF on tab mouse release

---


Expand for full commit details
```
[M135] Fix UAF on tab mouse release 
 
(cherry picked from commit d2a73990438a84199f658a671c2a2c93e360d7a7) 
 
Bug: 401393576 
Change-Id: I03df46dd83ca1c792fe419f9cc8c4ec01a2575ab 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6336893 
Reviewed-by: Keren Zhu <kerenzhu@chromium.org> 
Commit-Queue: Emily Shack <emshack@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1429754} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6339490 
Auto-Submit: Emily Shack <emshack@chromium.org> 
Commit-Queue: Keren Zhu <kerenzhu@chromium.org> 
Cr-Commit-Position: refs/branch-heads/7049@{#407} 
Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}

```

---

Files:

- M `chrome/browser/ui/views/tabs/tab.cc`

---

Hash: 87feda2c4be7e9e376c40d13b539e9e8a5d320b9  

Date:  Mon Mar 10 10:24:12 2025


---

### sp...@google.com (2025-03-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-13)

Congratulations asnine! Thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-06-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-06-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-08-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/401393576)*
