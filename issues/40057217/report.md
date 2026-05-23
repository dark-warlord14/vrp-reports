# Security:  heap-use-after-free in the views::Widget::GetNativeTheme in the browser process 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057217](https://issues.chromium.org/issues/40057217) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2021-09-09 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in the views::Widget::GetNativeTheme in the browser process which will excape the sandbox.

**VERSION**  

Chrome Version: 95.0.4626.0 (Developer Build) (64-bit)  

Operating System: Windows 10 && Ubuntu

**REPRODUCTION CASE**

In the previous submission, it seems that the owner did not successfully reproduce in the initial report  

It can be reproduced stably in windows and linux.

Steps:

1. Enable chrome://flags/#omnibox-webui-omnibox-popup
2. open the chrome with the command : chrome.exe --user-data-dir=c:/tmp/any <https://test.com/poc.html> about:blank
3. input any strings in the omnibox
4. Mouse right click in the popup windows(chrome://omnibox/omnibox\_popup.html)
5. That will cause the UAF when the tab closes

You can also reproduce this issue with the window.open api.  

See the new comment in the <https://crbug.com/chromium/1244304>.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 91 B)
- [windows.gif](attachments/windows.gif) (image/gif, 7.5 MB)

## Timeline

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-09)

Reproduced with a custom x64 Linux build of 95.0.4626.0, using exactly the steps described.

gn args
dcheck_always_on = false
enable_ipc_fuzzer = true
is_asan = true
is_component_build = false
is_debug = false
is_lsan = true
use_goma = true
v8_enable_verify_heap = true


=================================================================
==1013412==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160001f2f80 at pc 0x564ce0b4c08f bp 0x7ffc1d86ccf0 sp 0x7ffc1d86cce8
READ of size 8 at 0x6160001f2f80 thread T0 (chrome)
    #0 0x564ce0b4c08e in GetNativeTheme ui/views/widget/widget.h:739:43
    #1 0x564ce0b4c08e in views::Widget::GetNativeTheme() const ui/views/widget/widget.cc:1781:21
    #2 0x564ce09ea0e7 in GetNativeTheme ui/views/view.h:916:63
    #3 0x564ce09ea0e7 in views::MenuScrollViewContainer::OnPaintBackground(gfx::Canvas*) ui/views/controls/menu/menu_scroll_view_container.cc:290:3
    #4 0x564ce0ad9414 in views::View::OnPaint(gfx::Canvas*) ui/views/view.cc:1948:3
    #5 0x564ce0acf93d in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1185:5
    #6 0x564ce0ad9056 in RecursivePaintHelper ui/views/view.cc:2443:7
    #7 0x564ce0ad9056 in views::View::PaintChildren(views::PaintInfo const&) ui/views/view.cc:1943:3
    #8 0x564ce0acfaab in views::View::Paint(views::PaintInfo const&) ui/views/view.cc:1191:3
    #9 0x564ce0adc53c in views::View::PaintFromPaintRoot(ui::PaintContext const&) ui/views/view.cc:2450:3
    #10 0x564cdc5d4d0d in ui::Layer::PaintContentsToDisplayList() ui/compositor/layer.cc:1327:16
    #11 0x564cdb866e2a in cc::PictureLayer::Update() cc/layers/picture_layer.cc:145:41
    #12 0x564cdb953fcf in PaintContent cc/trees/layer_tree_host.cc:1550:33
    #13 0x564cdb953fcf in cc::LayerTreeHost::DoUpdateLayers() cc/trees/layer_tree_host.cc:921:28
    #14 0x564cdb9537be in cc::LayerTreeHost::UpdateLayers() cc/trees/layer_tree_host.cc:774:17
    #15 0x564cdbb9a9fe in cc::SingleThreadProxy::DoPainting() cc/trees/single_thread_proxy.cc:911:21
    #16 0x564cdbb9c0b4 in cc::SingleThreadProxy::BeginMainFrame(viz::BeginFrameArgs const&) cc/trees/single_thread_proxy.cc:888:3
    #17 0x564cdbb9dc36 in Invoke<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:509:12
    #18 0x564cdbb9dc36 in MakeItSo<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs> base/bind_internal.h:668:5
    #19 0x564cdbb9dc36 in RunImpl<void (cc::SingleThreadProxy::*)(const viz::BeginFrameArgs &), std::__1::tuple<base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, 0UL, 1UL> base/bind_internal.h:721:12
    #20 0x564cdbb9dc36 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::*)(viz::BeginFrameArgs const&), base::WeakPtr<cc::SingleThreadProxy>, viz::BeginFrameArgs>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #21 0x564cd7632670 in Run base/callback.h:99:12
    #22 0x564cd7632670 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #23 0x564cd766ac99 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #24 0x564cd766a428 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #25 0x564cd766b641 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #26 0x564cd752c8ea in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #27 0x564cd766bd0b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #28 0x564cd75ae381 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #29 0x564cce5c7dd5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:988:18
    #30 0x564cce5cc915 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #31 0x564cce5c1ccf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #32 0x564cd6432d9d in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #33 0x564cd6432d9d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #34 0x564cd6431ea5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #35 0x564cd642b457 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #36 0x564cd642d072 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #37 0x564cc9870935 in ChromeMain chrome/app/chrome_main.cc:172:12
    #38 0x7f712ff70d09 in __libc_start_main csu/../csu/libc-start.c:308:16

0x6160001f2f80 is located 0 bytes inside of 536-byte region [0x6160001f2f80,0x6160001f3198)
freed by thread T0 (chrome) here:
    #0 0x564cc986e92d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x564ce0bf034a in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc
    #2 0x564ce0bf05fd in views::NativeWidgetAura::~NativeWidgetAura() ui/views/widget/native_widget_aura.cc:1124:39
    #3 0x564cdc531f2f in aura::Window::~Window() ui/aura/window.cc:226:16
    #4 0x564cdc53387d in aura::Window::~Window() ui/aura/window.cc:181:19
    #5 0x564ce0bf1d74 in Invoke<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura>> base/bind_internal.h:509:12
    #6 0x564ce0bf1d74 in MakeItSo<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura>> base/bind_internal.h:668:5
    #7 0x564ce0bf1d74 in RunImpl<void (views::NativeWidgetAura::*)(), std::__1::tuple<base::WeakPtr<views::NativeWidgetAura> >, 0UL> base/bind_internal.h:721:12
    #8 0x564ce0bf1d74 in base::internal::Invoker<base::internal::BindState<void (views::NativeWidgetAura::*)(), base::WeakPtr<views::NativeWidgetAura> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #9 0x564cd7632670 in Run base/callback.h:99:12
    #10 0x564cd7632670 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #11 0x564cd766ac99 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #12 0x564cd766a428 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #13 0x564cd766b641 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #14 0x564cd752c8ea in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:405:48
    #15 0x564cd766bd0b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #16 0x564cd75ae381 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #17 0x564cce5c7dd5 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:988:18
    #18 0x564cce5cc915 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #19 0x564cce5c1ccf in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #20 0x564cd6432d9d in RunBrowserProcessMain content/app/content_main_runner_impl.cc:608:10
    #21 0x564cd6432d9d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1104:10
    #22 0x564cd6431ea5 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:971:12
    #23 0x564cd642b457 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #24 0x564cd642d072 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #25 0x564cc9870935 in ChromeMain chrome/app/chrome_main.cc:172:12
    #26 0x7f712ff70d09 in __libc_start_main csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x564cc986e0cd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x564ce20a1f19 in OmniboxPopupContentsView::UpdatePopupAppearance() chrome/browser/ui/views/omnibox/omnibox_popup_contents_view.cc:331:15
    #2 0x564ce035203e in OmniboxPopupModel::OnResultChanged() components/omnibox/browser/omnibox_popup_model.cc:229:10
    #3 0x564ce037fd37 in OmniboxEditModel::OnCurrentMatchChanged() components/omnibox/browser/omnibox_edit_model.cc:1567:20
    #4 0x564ce0384893 in OmniboxController::OnResultChanged(AutocompleteController*, bool) components/omnibox/browser/omnibox_controller.cc:56:28
    #5 0x564ce0186c21 in AutocompleteController::NotifyChanged(bool) components/omnibox/browser/autocomplete_controller.cc:963:9
    #6 0x564ce017edce in AutocompleteController::UpdateResult(bool, bool) components/omnibox/browser/autocomplete_controller.cc:781:3
    #7 0x564ce017cc33 in AutocompleteController::Start(AutocompleteInput const&) components/omnibox/browser/autocomplete_controller.cc:478:3
    #8 0x564ce036ade3 in OmniboxEditModel::StartAutocomplete(bool, bool) components/omnibox/browser/omnibox_edit_model.cc:580:24
    #9 0x564ce036990e in OmniboxEditModel::UpdateInput(bool, bool) components/omnibox/browser/omnibox_edit_model.cc:506:5
    #10 0x564ce208b83f in OmniboxViewViews::UpdatePopup() chrome/browser/ui/views/omnibox/omnibox_view_views.cc:732:12
    #11 0x564ce037e362 in OmniboxEditModel::OnAfterPossibleChange(OmniboxView::StateChanges const&, bool) components/omnibox/browser/omnibox_edit_model.cc:1519:10
    #12 0x564ce208ef6b in OmniboxViewViews::OnAfterPossibleChange(bool) chrome/browser/ui/views/omnibox/omnibox_view_views.cc:928:37
    #13 0x564ce0a0b81b in OnAfterUserAction ui/views/controls/textfield/textfield.cc:2501:18
    #14 0x564ce0a0b81b in views::Textfield::DoInsertChar(char16_t) ui/views/controls/textfield/textfield.cc:1832:3
    #15 0x564ce0a07deb in views::Textfield::InsertChar(ui::KeyEvent const&) ui/views/controls/textfield/textfield.cc:1447:3
    #16 0x564cdabe3f7b in ui::InputMethodAuraLinux::MaybeCommitResult(bool, ui::KeyEvent const&) ui/base/ime/linux/input_method_auralinux.cc:299:15
    #17 0x564cdabe2f00 in ui::InputMethodAuraLinux::DispatchKeyEvent(ui::KeyEvent*) ui/base/ime/linux/input_method_auralinux.cc:200:30
    #18 0x564cdc565bf3 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window*, ui::KeyEvent*) ui/aura/window_event_dispatcher.cc:1063:54
    #19 0x564cdc563997 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget*, ui::Event*) ui/aura/window_event_dispatcher.cc:551:15
    #20 0x564cd9b40aa5 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:52:34
    #21 0x564cdc56d9cd in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #22 0x564cdc58c34f in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #23 0x564cdc58bff3 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #24 0x564ce0c1a6f7 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:252:38
    #25 0x564ce0c14a60 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:279:29
    #26 0x564cdad24d22 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:1262:32
    #27 0x564cdad23f9f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:1204:3
    #28 0x564cdad24e7c in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #29 0x564cd978a5a4 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:98:29
    #30 0x564cd9ca46b4 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:291:5

SUMMARY: AddressSanitizer: heap-use-after-free ui/views/widget/widget.h:739:43 in GetNativeTheme


### ad...@google.com (2021-09-09)

Severity:
Heap use-after-free in browser process => critical
Mitigated by the need for user interaction => high.

[Monorail components: UI>Browser>Omnibox]

### to...@chromium.org (2021-09-09)

Hold on a sec, in order to access this bug, the user needs to turn on a flag in chrome://flags.

My main remediation for this may actually be to remove the flag from chrome://flags. Is this still a high-severity P1?

### ad...@google.com (2021-09-09)

As this requires #omnibox-webui-omnibox-popup, this shouldn't impact normal Chrome users - rating as Security_Impact-None.

### ad...@google.com (2021-09-09)

Re https://crbug.com/chromium/1248059#c4 yep agreed.
It's high _severity_ but it's impact-none which means we in security don't mind what priority you set it to.

### to...@chromium.org (2021-09-09)

Okay thanks!

### to...@chromium.org (2021-09-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/598283686174bca10aa2ce21a406c38cb1085fd5

commit 598283686174bca10aa2ce21a406c38cb1085fd5
Author: Tommy Li <tommycli@chromium.org>
Date: Mon Sep 20 18:03:26 2021

[omnibox] Remove WebUI omnibox popup flag from chrome://flags

This CL removes access to the WebUI omnibox popup from chrome://flags.

This experiment is not being actively developed.

Bug: 1248059, 1244304, 1174341
Change-Id: I1befa2e49dc542f857c3d78f26baeb5023cc438b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3169427
Auto-Submit: Tommy Li <tommycli@chromium.org>
Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922960}

[modify] https://crrev.com/598283686174bca10aa2ce21a406c38cb1085fd5/chrome/browser/about_flags.cc
[modify] https://crrev.com/598283686174bca10aa2ce21a406c38cb1085fd5/chrome/browser/flag-metadata.json


### to...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-09-29)

[VRP Panel] Hi, this bug doesn't appear to be fixed, the UAF is still present in the code, it's just unreachable without extra command line switches. Can you re-triage and take a look at the underlying UAF? Thanks.

### 0x...@gmail.com (2021-10-21)

Hi, any update to this issue?

### to...@chromium.org (2021-12-07)

We don't plan on fixing the underlying issue right away, since it's on a speculative feature that's still slated for future development.

Should we just leave it Open at a P3 in this situation?

### ad...@google.com (2021-12-07)

That's fine yes. We would like to see this fixed - we don't like UaFs in the code even if they require a command line flag. It would be great if you can land a fix sometime within the next couple of months - hope that's reasonable?

### da...@chromium.org (2022-04-05)

What's the plan for this code? I see a few UAF reported in it. Can we remove it?

### pk...@chromium.org (2022-04-25)

Gone as of https://chromium-review.googlesource.com/c/chromium/src/+/3553242 .

That said, I am investigating if the general issue here (closing a Widget while it has an open menu parented to it) is still a problem, and if so, I'll look into fixing systematically.

### pk...@chromium.org (2022-04-25)

Some detail on what's going on here:

Menus have code to auto-close a menu if its parent widget loses activation.  In practice, this usually means that when a widget is closed, its open menu (if any) is closed too, because you can't generally open a menu on a widget without activating it in the process.

However, the omnibox dropdown doesn't activate when it opens, it leaves the parent widget active (with the omnibox textfield focused).  For normal Chrome builds this doesn't matter, because you can't context-click the omnibox dropdown (it doesn't do anything).  But the webui omnibox dropdown allowed a context menu to open.

Combine these two together and you get an open menu that doesn't auto-close when its parent widget closes.  Somehow, this led to a UAF during menu painting; I'm not quite sure how, since I think that means the MenuHost widget was deleted but there was still a paint queued in the event loop, and I can't step through in a debugger because the code is now gone.

Maybe I'll try and resurrect this code just to debug more.

### 0x...@gmail.com (2022-04-26)

This issue is fixed in https://crbug.com/chromium/1248059#c9 && https://crbug.com/chromium/1248059#c10.
In https://crbug.com/chromium/1248059#c14 the statue is setted as WontFix.
Maybe fixed is the right statue.


### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-04-26)

The correct status for a Fixed security issue is Fixed.

### aj...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Thank you for this report. Since this does not appear to be an issue exploitable from the web and given the sufficient user interaction for this issue, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-02)

This issue was migrated from crbug.com/chromium/1248059?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1244304]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057217)*
