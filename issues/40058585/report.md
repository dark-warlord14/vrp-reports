# Uaf in OmniboxPopup

| Field | Value |
|-------|-------|
| **Issue ID** | [40058585](https://issues.chromium.org/issues/40058585) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tt...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2022-01-25 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0

Steps to reproduce the problem:
1. run chrome with flag: ./asan-linux-release-962399/chrome --enable-features=WebUIOmniboxPopup http://127.0.0.1:8000/test.html about:blank
2.  input anything in the location bar, it will show a popup window, then right click it.
3. after the tab is closed, move mouse to the right click menu

What is the expected behavior?

What went wrong?
=================================================================
==7683==ERROR: AddressSanitizer: heap-use-after-free on address 0x616000213980 at pc 0x5594af0931f2 bp 0x7ffc321acab0 sp 0x7ffc321acaa8
READ of size 8 at 0x616000213980 thread T0 (chrome)
    #0 0x5594af0931f1 in GetNativeTheme ui/views/widget/widget.h:763:43
    #1 0x5594af0931f1 in views::Widget::GetNativeTheme() const ui/views/widget/widget.cc:1788:21
    #2 0x5594af092eb0 in views::Widget::GetColorProvider() const ui/views/widget/widget.cc:1754:7
    #3 0x5594af013fa3 in views::TypographyProvider::GetColor(views::View const&, int, int) const ui/views/style/typography_provider.cc:142:15
    #4 0x5594aeed903b in CalculateColors ui/views/controls/menu/menu_item_view.cc:1180:27
    #5 0x5594aeed903b in views::MenuItemView::UpdateSelectionBasedState(bool) ui/views/controls/menu/menu_item_view.cc:1487:25
    #6 0x5594aeee5346 in views::MenuItemView::SetSelected(bool) ui/views/controls/menu/menu_item_view.cc:518:3
    #7 0x5594aeeb0c8e in views::MenuController::SetSelection(views::MenuItemView*, int) ui/views/controls/menu/menu_controller.cc:1382:18
    #8 0x5594aeeb7d05 in views::MenuController::HandleMouseLocation(views::SubmenuView*, gfx::Point const&) ui/views/controls/menu/menu_controller.cc
    #9 0x5594aeeb76d0 in views::MenuController::OnMouseMoved(views::SubmenuView*, ui::MouseEvent const&) ui/views/controls/menu/menu_controller.cc:870:3
    #10 0x5594af09147b in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc
    #11 0x5594a7c52dd9 in DispatchEvent ui/events/event_dispatcher.cc:190:12
    #12 0x5594a7c52dd9 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #13 0x5594a7c526a3 in DispatchEventToTarget ui/events/event_dispatcher.cc:83:14
    #14 0x5594a7c526a3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #15 0x5594aa818abd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #16 0x5594aa837ccf in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #17 0x5594aa8378c9 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:143:12
    #18 0x5594af15d377 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:231:38
    #19 0x5594af1575cd in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:297:29
    #20 0x5594a7c5f9fa in Run base/callback.h:142:12
    #21 0x5594a7c5f9fa in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:36:25
    #22 0x5594a9166672 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #23 0x5594a9165a1f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #24 0x5594a916685c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #25 0x5594a7c31384 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:100:29
    #26 0x5594a8fc9394 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:287:5
    #27 0x55949892531a in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:469:14
    #28 0x559498924381 in ProcessNextEvent ui/gfx/x/connection.cc:520:3
    #29 0x559498924381 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:446:5
    #30 0x5594a8fd6f64 in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:55:15
    #31 0x7fd75008904d in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5204d) (BuildId: 2c1d2f9d4a08c71a36797aeb246ab7ae377934ea)

0x616000213980 is located 0 bytes inside of 600-byte region [0x616000213980,0x616000213bd8)
freed by thread T0 (chrome) here:
    #0 0x55949731c87d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5594af133023 in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc
    #2 0x5594af1332dd in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc:1132:39
    #3 0x5594aa7dcf1a in aura::Window::~Window() ui/aura/window.cc:228:16
    #4 0x5594aa7de85d in aura::Window::~Window() ui/aura/window.cc:183:19
    #5 0x5594af134a90 in Invoke<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura> > base/bind_internal.h:535:12
    #6 0x5594af134a90 in MakeItSo<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura> > base/bind_internal.h:719:5
    #7 0x5594af134a90 in RunImpl<void (views::NativeWidgetAura::*)(), std::__1::tuple<base::WeakPtr<views::NativeWidgetAura> >, 0UL> base/bind_internal.h:772:12
    #8 0x5594af134a90 in base::internal::Invoker<base::internal::BindState<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:741:12
    #9 0x5594a572fcc3 in Run base/callback.h:142:12
    #10 0x5594a572fcc3 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #11 0x5594a5771353 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #12 0x5594a5771353 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #13 0x5594a5770b67 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #14 0x5594a5771f21 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #15 0x5594a562857a in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:406:48
    #16 0x5594a57725e7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #17 0x5594a56aa1e9 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #18 0x55949c23d3f0 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1053:18
    #19 0x55949c241de5 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #20 0x55949c237337 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #21 0x5594a4502730 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:637:10
    #22 0x5594a45057ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1152:10
    #23 0x5594a45048d2 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1018:12
    #24 0x5594a44fd42c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #25 0x5594a44ff094 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #26 0x55949731e8be in ChromeMain chrome/app/chrome_main.cc:176:12
    #27 0x7fd74eb430b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x55949731c01d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5594b0779237 in OmniboxPopupContentsView::UpdatePopupAppearance() chrome/browser/ui/views/omnibox/omnibox_popup_contents_view.cc:337:15
    #2 0x5594afcfdce2 in OmniboxEditModel::OnPopupResultChanged() components/omnibox/browser/omnibox_edit_model.cc:2088:18
    #3 0x5594afcfa062 in OmniboxEditModel::OnCurrentMatchChanged() components/omnibox/browser/omnibox_edit_model.cc:1589:3
    #4 0x5594afd034be in OmniboxController::OnResultChanged(AutocompleteController*, bool) components/omnibox/browser/omnibox_controller.cc:55:28
    #5 0x5594ae82d891 in AutocompleteController::NotifyChanged(bool) components/omnibox/browser/autocomplete_controller.cc:965:9
    #6 0x5594ae827bd8 in AutocompleteController::UpdateResult(bool, bool) components/omnibox/browser/autocomplete_controller.cc:803:3
    #7 0x5594ae825653 in AutocompleteController::Start(AutocompleteInput const&) components/omnibox/browser/autocomplete_controller.cc:472:3
    #8 0x5594afce4041 in OmniboxEditModel::StartAutocomplete(bool, bool) components/omnibox/browser/omnibox_edit_model.cc:602:24
    #9 0x5594afce2b9b in OmniboxEditModel::UpdateInput(bool, bool) components/omnibox/browser/omnibox_edit_model.cc:528:5
    #10 0x5594b076180f in OmniboxViewViews::UpdatePopup() chrome/browser/ui/views/omnibox/omnibox_view_views.cc:745:12
    #11 0x5594afcf8682 in OmniboxEditModel::OnAfterPossibleChange(OmniboxView::StateChanges const&, bool) components/omnibox/browser/omnibox_edit_model.cc:1542:10
    #12 0x5594b0764e0b in OmniboxViewViews::OnAfterPossibleChange(bool) chrome/browser/ui/views/omnibox/omnibox_view_views.cc:940:37
    #13 0x5594aef3c3cb in OnAfterUserAction ui/views/controls/textfield/textfield.cc:2479:18
    #14 0x5594aef3c3cb in views::Textfield::DoInsertChar(char16_t) ui/views/controls/textfield/textfield.cc:1811:3
    #15 0x5594aef385bb in views::Textfield::InsertChar(ui::KeyEvent const&) ui/views/controls/textfield/textfield.cc:1425:3
    #16 0x5594a90142e9 in ui::InputMethodAuraLinux::MaybeCommitResult(bool, ui::KeyEvent const&) ui/base/ime/linux/input_method_auralinux.cc:299:15
    #17 0x5594a901327d in ui::InputMethodAuraLinux::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/linux/input_method_auralinux.cc:200:30
    #18 0x5594aa810d63 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1058:54
    #19 0x5594aa80eaff in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:546:15
    #20 0x5594a7c5259c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:51:34
    #21 0x5594aa818abd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x5594aa837ccf in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #23 0x5594aa8378c9 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:143:12
    #24 0x5594af15d377 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:231:38
    #25 0x5594af1575cd in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:297:29
    #26 0x5594a7c5f8fa in Run base/callback.h:142:12
    #27 0x5594a7c5f8fa in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:28:25
    #28 0x5594a9166672 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1304:3
    #29 0x5594a9165a1f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1257:3
    #30 0x5594a916685c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #31 0x5594a7c31384 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:100:29

SUMMARY: AddressSanitizer: heap-use-after-free ui/views/widget/widget.h:763:43 in GetNativeTheme
Shadow bytes around the buggy address:
  0x0c2c8003a6e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c8003a6f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c8003a700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c2c8003a710: 00 00 04 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2c8003a720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2c8003a730:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c8003a740: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c8003a750: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c8003a760: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2c8003a770: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c2c8003a780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==7683==ABORTING

Did this work before? N/A 

Chrome version:   Channel: n/a
OS Version:

## Attachments

- [test.html](attachments/test.html) (text/plain, 74 B)
- [test.mp4](attachments/test.mp4) (video/mp4, 1.9 MB)

## Timeline

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-01-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5095868524724224.

### ca...@chromium.org (2022-01-27)

tommycli: Can you help further triage this? CF doesn't reproduce, but I was able to reproduce in M97

Triageing as severity high since this is in the browser process but requires significant user interaction. Setting Impact-None since this is behind a default off flag.

[Monorail components: UI>Browser>Omnibox]

### to...@chromium.org (2022-01-27)

To be honest, it's not worth much further effort on at this point.

Future work on this feature will likely rewrite most of this code.

The best remediation would be to remove the existing code entirely, if it's bothersome that there's a UAF behind this feature flag...

I can leave this as a P3.

### ad...@google.com (2022-03-25)

tommycli@ could you update us on the status here? Even if this is Security_Impact-None, at some point we need to declare this Fixed (either once the code is rewritten or is removed). If nothing else, that will cause this bug to go to the VRP panel and the reporter may get a reward.

And of course we still like to keep an eye on Security_Impact-None bugs just in case the code becomes enabled!

### to...@chromium.org (2022-03-25)

adetaylor: I added a CL here to remove the code entirely: https://chromium-review.googlesource.com/c/chromium/src/+/3553242

I guess we can always re-add it once someone wants to maintain/develop this feature on a more full time basis.

### to...@chromium.org (2022-03-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09741e01852614ad9722c5c495f5970f95ea459e

commit 09741e01852614ad9722c5c495f5970f95ea459e
Author: Tommy C. Li <tommycli@chromium.org>
Date: Mon Mar 28 09:28:45 2022

[omnibox] Delete the WebUI Omnibox popup code

It has a UAF that you can trigger when you turn on the flag.

The code is untested and unmaintained at this point.

This CL removes the code to put this to rest.

Bug: 1290713, 1046561
Change-Id: I86896b06003007ea406c11d9b51c8d9337f6fcac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3553242
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Auto-Submit: Tommy Li <tommycli@chromium.org>
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Cr-Commit-Position: refs/heads/main@{#985890}

[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/ui/views/omnibox/webui_omnibox_popup_view.h
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/ui/views/omnibox/webui_omnibox_popup_view.cc
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/ui/webui/resources/cr_components/BUILD.gn
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/ui/webui/resources/cr_components/omnibox/BUILD.gn
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/ui/webui/resources/cr_components/omnibox/DIR_METADATA
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/ui/webui/omnibox/omnibox_popup_handler.cc
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/ui/webui/resources/cr_components/omnibox/OWNERS
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/resources/omnibox/omnibox_popup.html
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/components/omnibox/common/omnibox_features.h
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/components/omnibox/common/omnibox_features.cc
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/resources/omnibox/BUILD.gn
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/ui/BUILD.gn
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/resources/omnibox/omnibox_popup.js
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/ui/webui/omnibox/omnibox_ui.h
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/ui/webui/resources/cr_components/omnibox/cr_autocomplete_match_list.js
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/ui/webui/omnibox/omnibox_ui.cc
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/ui/views/omnibox/omnibox_popup_contents_view.h
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/ui/webui/resources/cr_components/omnibox/cr_autocomplete_match_list.html
[modify] https://crrev.com/09741e01852614ad9722c5c495f5970f95ea459e/chrome/browser/ui/views/omnibox/omnibox_popup_contents_view.cc
[delete] https://crrev.com/d47cd4ac21da135fb61f10846ed7601d473e7e11/chrome/browser/ui/webui/omnibox/omnibox_popup_handler.h


### tt...@gmail.com (2022-04-08)

Hi, is this eligible for a bounty or CVE?

### do...@chromium.org (2022-04-28)

tommycli: is this issue addressed now by deleting the code? If so, please mark as Fixed and the rest of the security process will automatically kick in.

### an...@chromium.org (2022-05-05)

tommycli@: Friendly marshal ping to update this issue. Thanks!

### to...@chromium.org (2022-05-05)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-05-05)

Thanks!

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Thank you for this report! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-08-18)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. Thank you! 

### is...@google.com (2022-08-18)

This issue was migrated from crbug.com/chromium/1290713?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058585)*
