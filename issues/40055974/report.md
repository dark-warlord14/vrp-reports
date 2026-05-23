# Security: UAF after user clicks help link in enhanced spell check dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40055974](https://issues.chromium.org/issues/40055974) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Language>Spellcheck |
| **Platforms** | Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2021-05-23 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The enhanced spell check dialog includes a help link in the bottom left. That link is opened via the WebContents used to show the dialog. If that WebContents has been destroyed (e.g. because the tab has been closed) and the user clicks the help link, a UAF will occur in the browser process.

**VERSION**  

Chrome Version: Tested on 93.0.4520.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Ensure enhanced spell check isn't already on.
2. Install the attached extension.
3. Once installed, the extension will open page.html in a new tab.
4. In the input field on the page, right-click, then select "Spell check" > "Use enhanced spell check" from the context menu.
5. page.html will wait for the contextmenu event, followed by a blur event (which will be triggered when the enhanced spell check dialog is opened). Once it detects those events, it will send a message to the background page requesting it to close the tab.
6. Once the tab has been closed, click the help link shown in the dialog. That will result in a UAF in the browser process. You can verify that by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_885837.txt](attachments/asan_output_885837.txt) (text/plain, 17.7 KB)
- [background.js](attachments/background.js) (text/plain, 228 B)
- [manifest.json](attachments/manifest.json) (text/plain, 160 B)
- [page.html](attachments/page.html) (text/plain, 168 B)
- [page.js](attachments/page.js) (text/plain, 903 B)

## Timeline

### [Deleted User] (2021-05-23)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-05-23)

The SpellingBubbleModel class holds a pointer to the WebContents that was used to host the context menu:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/spelling_bubble_model.h;l=40;drc=dec9912407fc5946125799ec62b996a04d08c4f0

When the help page link is clicked, the stored WebContents will be used to open the help page:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/spelling_bubble_model.cc;l=67;drc=dec9912407fc5946125799ec62b996a04d08c4f0

If the WebContents has been destroyed since the menu was shown, that will result in a UAF.

I think the extension attached in the initial message demonstrates that it's at least plausible that a page could indirectly detect that the enhanced spell check dialog has been opened, and then close the tab in response to that.

A regular webpage could do the same thing, though using an extension is a little easier, as there are restrictions on when window.close can be called:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/dom_window.cc;l=344;drc=d2047b5fbf1da5e49ea1b6009eed130b357ac3e1

### va...@chromium.org (2021-05-25)

avi@ tentatively assigning this to you as one of the OWNERs for chrome/browser/renderer_context_menu/

I'm able to reproduce it on 90.0.4430.212 on Windows.

Assigning Security_Severity-High since it requires installing an extension and some specific, non-obvious user interactions.

### va...@chromium.org (2021-05-25)

==146385==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e000107480 at pc 0x55fc7ad41b64 bp 0x7fff758cad30 sp 0x7fff758cad28
READ of size 8 at 0x61e000107480 thread T0 (chrome)
    #0 0x55fc7ad41b63 in SpellingBubbleModel::OpenHelpPage() chrome/browser/renderer_context_menu/spelling_bubble_model.cc:67:18
    #1 0x55fc7a3486b3 in operator() chrome/browser/ui/views/confirm_bubble_views.cc:45:33
    #2 0x55fc7a3486b3 in Invoke<const (lambda at ../../chrome/browser/ui/views/confirm_bubble_views.cc:44:15) &, ConfirmBubbleViews *> base/bind_internal
.h:379:12
    #3 0x55fc7a3486b3 in MakeItSo<const (lambda at ../../chrome/browser/ui/views/confirm_bubble_views.cc:44:15) &, ConfirmBubbleViews *> base/bind_intern
al.h:637:12
    #4 0x55fc7a3486b3 in RunImpl<const (lambda at ../../chrome/browser/ui/views/confirm_bubble_views.cc:44:15) &, const std::tuple<base::internal::Unreta
inedWrapper<ConfirmBubbleViews> > &, 0> base/bind_internal.h:710:12
    #5 0x55fc7a3486b3 in base::internal::Invoker<base::internal::BindState<ConfirmBubbleViews::ConfirmBubbleViews(std::__1::unique_ptr<ConfirmBubbleModel
, std::__1::default_delete<ConfirmBubbleModel> >)::$_0, base::internal::UnretainedWrapper<ConfirmBubbleViews> >, void ()>::Run(base::internal::BindStateB
ase*) base/bind_internal.h:692:12
    #6 0x55fc791ab01b in Run base/callback.h:168:12
    #7 0x55fc791ab01b in operator() ui/views/controls/button/button.cc:102:68
    #8 0x55fc791ab01b in Invoke<const (lambda at ../../ui/views/controls/button/button.cc:101:31) &, const base::RepeatingCallback<void ()> &, const ui::
Event &> base/bind_internal.h:379:12
    #9 0x55fc791ab01b in MakeItSo<const (lambda at ../../ui/views/controls/button/button.cc:101:31) &, const base::RepeatingCallback<void ()> &, const ui
::Event &> base/bind_internal.h:637:12
    #10 0x55fc791ab01b in RunImpl<const (lambda at ../../ui/views/controls/button/button.cc:101:31) &, const std::tuple<base::RepeatingCallback<void ()>
> &, 0> base/bind_internal.h:710:12
    #11 0x55fc791ab01b in base::internal::Invoker<base::internal::BindState<views::Button::PressedCallback::PressedCallback(base::RepeatingCallback<void
()>)::$_0, base::RepeatingCallback<void ()> >, void (ui::Event const&)>::Run(base::internal::BindStateBase*, ui::Event const&) base/bind_internal.h:692:1
2
    #12 0x55fc791af21d in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc
    #13 0x55fc721f9e80 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #14 0x55fc7918c939 in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:28:24
    #15 0x55fc721f771e in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #16 0x55fc721f771e in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #17 0x55fc721f6f1f in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #18 0x55fc721f6c5a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #19 0x55fc793d4c6a in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:480:9
    #20 0x55fc793f32a0 in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1318:20
    #21 0x55fc721f9e80 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc
    #22 0x55fc721f771e in DispatchEvent ui/events/event_dispatcher.cc:191:12
    #23 0x55fc721f771e in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #24 0x55fc721f6f1f in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #25 0x55fc721f6c5a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #26 0x55fc74727a3d in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #27 0x55fc7474479f in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #28 0x55fc74744443 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #29 0x55fc794b2977 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:238:38
    #30 0x55fc794adc27 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:242
:29
    #31 0x55fc7327b32d in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/platform_window/x11/x11_window.cc:638:34
    #32 0x55fc7327a670 in ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc:583:3
    #33 0x55fc7327b54f in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event* const&) ui/platform_window/x11/x11_window.cc
    #34 0x55fc71e7466b in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:100:29
    #35 0x55fc7234de64 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:299:5
    #36 0x55fc63aefd9c in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:459:14
    #37 0x55fc63aeee21 in ProcessNextEvent ui/gfx/x/connection.cc:510:3
    #38 0x55fc63aeee21 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:436:5
    #39 0x55fc7234c405 in ui::X11EventSource::DispatchXEvents() ui/events/platform/x11/x11_event_source.cc:156:25
    #40 0x55fc7235c08b in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:4
2:15
    #41 0x7fe4aa6c9d6e in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x51d6e)

0x61e000107480 is located 0 bytes inside of 2480-byte region [0x61e000107480,0x61e000107e30)
freed by thread T0 (chrome) here:
    #0 0x55fc626a08bd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55fc79e47db4 in operator() buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x55fc79e47db4 in reset buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x55fc79e47db4 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc
:533:21
    #4 0x55fc79e4e8e8 in TabStripModel::InternalCloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/u
i/tabs/tab_strip_model.cc:1763:5
    #5 0x55fc79e4f0a1 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:727:10
    #6 0x55fc68622cf9 in content::WebContentsImpl::Close(content::RenderViewHost*) content/browser/web_contents/web_contents_impl.cc:6889:16
    #7 0x55fc685ec6e1 in content::WebContentsImpl::Close() content/browser/web_contents/web_contents_impl.cc:4710:3
    #8 0x55fc784b06a7 in extensions::TabsRemoveFunction::RemoveTab(int, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<cha
r> >*) chrome/browser/extensions/api/tabs/tabs_api.cc:1721:13
    #9 0x55fc784afe5d in extensions::TabsRemoveFunction::Run() chrome/browser/extensions/api/tabs/tabs_api.cc:1678:10
    #10 0x55fc69803a30 in ExtensionFunction::RunWithValidation() extensions/browser/extension_function.cc:466:10
    #11 0x55fc6980ba7d in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFr
ameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__1::basic_string<char, std::__1::char_traits<
char>, std::__1::allocator<char> > const&)> const&) extensions/browser/extension_function_dispatcher.cc:383:15
    #12 0x55fc6980ab81 in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) exten
sions/browser/extension_function_dispatcher.cc:253:5
    #13 0x55fc6987d36f in OnRequest extensions/browser/extension_web_contents_observer.cc:324:15                                                 [83/268]
    #14 0x55fc6987d36f in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::Rend
erFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::tuple<ExtensionHostMsg_Request_Params>, 0> ipc/ipc_message_templa
tes.h:65:3
    #15 0x55fc6987d36f in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, s
td::tuple<ExtensionHostMsg_Request_Params> > ipc/ipc_message_templates.h:77:3
    #16 0x55fc6987d36f in Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (ex
tensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &)> ipc/ipc_message_templates.h:140:7
    #17 0x55fc6987d36f in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) extensions/browser/
extension_web_contents_observer.cc:235:5
    #18 0x55fc786e2427 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) chrome/browse
r/extensions/chrome_extension_web_contents_observer.cc:94:37
    #19 0x55fc685ab043 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) content/browser/web_contents/we
b_contents_impl.cc:1160:18
    #20 0x55fc6808d919 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_frame_host_impl.cc:19
36:18
    #21 0x55fc7208e1c7 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:325:14
    #22 0x55fc6ed86dd0 in Run base/callback.h:101:12
    #23 0x55fc6ed86dd0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #24 0x55fc6edc1977 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/s
equence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #25 0x55fc6edc11a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_wi
th_message_pump_impl.cc:264:36
    #26 0x55fc6ec856e0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:404:48
    #27 0x55fc6edc2a9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/th
read_controller_with_message_pump_impl.cc:460:12
    #28 0x55fc6ed05101 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #29 0x55fc6f7dc638 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1732:15
    #30 0x55fc674aa5a0 in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:970:29
    #31 0x55fc674af425 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:150:15
    #32 0x55fc674a3955 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #33 0x55fc6ea63245 in RunBrowserProcessMain content/app/content_main_runner_impl.cc:581:10
    #34 0x55fc6ea63245 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1062:10
    #35 0x55fc6ea625b7 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:944:12
    #36 0x55fc6ea5ca76 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:372:36
    #37 0x55fc6ea5cfcc in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:398:10

previously allocated by thread T0 (chrome) here:
    #0 0x55fc626a005d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55fc6859e620 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) content/bro
wser/web_contents/web_contents_impl.cc:1016:7
    #2 0x55fc79d3db58 in CreateTargetContents chrome/browser/ui/browser_navigator.cc:455:7
    #3 0x55fc79d3db58 in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:645:28
    #4 0x55fc788369be in extensions::ExtensionTabUtil::OpenTab(ExtensionFunction*, extensions::ExtensionTabUtil::OpenTabParams const&, bool, std:[40/268]
sic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) chrome/browser/extensions/extension_tab_util.cc:313:3
    #5 0x55fc784a88b7 in extensions::TabsCreateFunction::Run() chrome/browser/extensions/api/tabs/tabs_api.cc:1170:7
    #6 0x55fc69803a30 in ExtensionFunction::RunWithValidation() extensions/browser/extension_function.cc:466:10
    #7 0x55fc6980ba7d in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFra
meHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__1::basic_string<char, std::__1::char_traits<c
har>, std::__1::allocator<char> > const&)> const&) extensions/browser/extension_function_dispatcher.cc:383:15
    #8 0x55fc6980ab81 in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) extens
ions/browser/extension_function_dispatcher.cc:253:5
    #9 0x55fc6987d36f in OnRequest extensions/browser/extension_web_contents_observer.cc:324:15
    #10 0x55fc6987d36f in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::Rend
erFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::tuple<ExtensionHostMsg_Request_Params>, 0> ipc/ipc_message_templa
tes.h:65:3
    #11 0x55fc6987d36f in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, s
td::tuple<ExtensionHostMsg_Request_Params> > ipc/ipc_message_templates.h:77:3
    #12 0x55fc6987d36f in Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (ex
tensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &)> ipc/ipc_message_templates.h:140:7
    #13 0x55fc6987d36f in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) extensions/browser/
extension_web_contents_observer.cc:235:5
    #14 0x55fc786e2427 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) chrome/browse
r/extensions/chrome_extension_web_contents_observer.cc:94:37
    #15 0x55fc685ab043 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) content/browser/web_contents/we
b_contents_impl.cc:1160:18
    #16 0x55fc6808d919 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_frame_host_impl.cc:19
36:18
    #17 0x55fc7208e1c7 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:325:14
    #18 0x55fc6ed86dd0 in Run base/callback.h:101:12
    #19 0x55fc6ed86dd0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:163:33
    #20 0x55fc6edc1977 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/s
equence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #21 0x55fc6edc11a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_wi
th_message_pump_impl.cc:264:36
    #22 0x55fc6ec856e0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:404:48
    #23 0x55fc6edc2a9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/th
read_controller_with_message_pump_impl.cc:460:12
    #24 0x55fc6ed05101 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:133:14
    #25 0x55fc6f7dc638 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1732:15
    #26 0x55fc674aa5a0 in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:970:29
    #27 0x55fc674af425 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:150:15
    #28 0x55fc674a3955 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #29 0x55fc6ea63245 in RunBrowserProcessMain content/app/content_main_runner_impl.cc:581:10
    #30 0x55fc6ea63245 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1062:10
    #31 0x55fc6ea625b7 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:944:12
    #32 0x55fc6ea5ca76 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:372:36
    #33 0x55fc6ea5cfcc in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:398:10
    #34 0x55fc626a2b77 in ChromeMain chrome/app/chrome_main.cc:141:12
    #35 0x7fe4a8ce6d09 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/renderer_context_menu/spelling_bubble_model.cc:67:18 in SpellingBubbleModel::OpenHelpPage()
Shadow bytes around the buggy address:
  0x0c3c80018e40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018e50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018e60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018e70: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c80018e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3c80018e90:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018ea0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018eb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018ec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018ed0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80018ee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
  Shadow gap:              cc
==146385==ABORTING

### va...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Language>Spellcheck]

### [Deleted User] (2021-05-25)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2021-05-25)

+katie who is working on the same thing in https://crbug.com/chromium/1212500.

### va...@chromium.org (2021-05-26)

crash/5a97c3d246daefb9 -- if that's useful.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### av...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4

commit b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4
Author: Avi Drissman <avi@chromium.org>
Date: Thu May 27 18:15:43 2021

Fix UaF for the enhanced spell check bubble

For the enhanced spell check bubble, be sure to use a valid
WebContents for the help page. Adds a browser test.

Note that this is a clone of 427728383657e6ccb06dbfcce0c5118bb557c0af
that was committed to fix the same issue with the accessibility
bubble. Alas, these are the only two subclassers of ConfirmBubbleModel
across the Chromium codebase, and given that ConfirmBubbleModel is in
ui/ and can't know about this specific lifetime issue, this is the
simplest way forward.

Bug: 1212498
Test: As in bug
Change-Id: I365e9721613ea2a89a8fad902ddc137b24de687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920807
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#887244}

[modify] https://crrev.com/b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4/chrome/browser/renderer_context_menu/spelling_bubble_model.cc
[modify] https://crrev.com/b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4/chrome/browser/renderer_context_menu/spelling_bubble_model.h
[add] https://crrev.com/b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4/chrome/browser/renderer_context_menu/spelling_bubble_model_browsertest.cc
[modify] https://crrev.com/b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4/chrome/test/BUILD.gn


### av...@chromium.org (2021-05-27)

As in https://crbug.com/chromium/1212500, is this something we want to target for a merge?

### [Deleted User] (2021-05-27)

Requesting merge to stable M91 because latest trunk commit (887244) appears to be after stable branch point (870763).

Requesting merge to beta M91 because latest trunk commit (887244) appears to be after beta branch point (870763).

Requesting merge to future beta M92 because latest trunk commit (887244) appears to be after future beta branch point (56).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2021-05-27)

Coordinating answers with https://crbug.com/chromium/1212500#c30:

1. This has test coverage, though it has not yet baked on Canary. Does a help link in the corner of a dialog qualify as a critical enough issue to merge to stable? This is not web-accessible.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2920807
3. Yes.
4. Yes, M+1, M92
5. Security fix
6. No
7. n/a

### ad...@google.com (2021-05-27)

Approving merge to M92, branch 4515. We'll handle M91 approvals at a later stage.

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb043604930d22d5fb2e88045fd980523c7b5257

commit fb043604930d22d5fb2e88045fd980523c7b5257
Author: Avi Drissman <avi@chromium.org>
Date: Thu May 27 22:29:20 2021

[Merge to M92] Fix UaF for the enhanced spell check bubble

For the enhanced spell check bubble, be sure to use a valid
WebContents for the help page. Adds a browser test.

Note that this is a clone of 427728383657e6ccb06dbfcce0c5118bb557c0af
that was committed to fix the same issue with the accessibility
bubble. Alas, these are the only two subclassers of ConfirmBubbleModel
across the Chromium codebase, and given that ConfirmBubbleModel is in
ui/ and can't know about this specific lifetime issue, this is the
simplest way forward.

(cherry picked from commit b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4)

Bug: 1212498
Test: As in bug
Change-Id: I365e9721613ea2a89a8fad902ddc137b24de687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920807
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2923228
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Katie Dektar <katie@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#133}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/fb043604930d22d5fb2e88045fd980523c7b5257/chrome/browser/renderer_context_menu/spelling_bubble_model.cc
[modify] https://crrev.com/fb043604930d22d5fb2e88045fd980523c7b5257/chrome/browser/renderer_context_menu/spelling_bubble_model.h
[add] https://crrev.com/fb043604930d22d5fb2e88045fd980523c7b5257/chrome/browser/renderer_context_menu/spelling_bubble_model_browsertest.cc
[modify] https://crrev.com/fb043604930d22d5fb2e88045fd980523c7b5257/chrome/test/BUILD.gn


### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-28)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-03)

Approving merge to M91, branch 4472.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f8ca0e35834223cb58ce777c9ccd49e903e7434

commit 9f8ca0e35834223cb58ce777c9ccd49e903e7434
Author: Avi Drissman <avi@chromium.org>
Date: Thu Jun 03 23:33:28 2021

Fix UaF for the enhanced spell check bubble

For the enhanced spell check bubble, be sure to use a valid
WebContents for the help page. Adds a browser test.

Note that this is a clone of 427728383657e6ccb06dbfcce0c5118bb557c0af
that was committed to fix the same issue with the accessibility
bubble. Alas, these are the only two subclassers of ConfirmBubbleModel
across the Chromium codebase, and given that ConfirmBubbleModel is in
ui/ and can't know about this specific lifetime issue, this is the
simplest way forward.

(cherry picked from commit b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4)

Bug: 1212498
Test: As in bug
Change-Id: I365e9721613ea2a89a8fad902ddc137b24de687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920807
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#887244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937516
Commit-Queue: Katie Dektar <katie@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1423}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/9f8ca0e35834223cb58ce777c9ccd49e903e7434/chrome/browser/renderer_context_menu/spelling_bubble_model.cc
[modify] https://crrev.com/9f8ca0e35834223cb58ce777c9ccd49e903e7434/chrome/browser/renderer_context_menu/spelling_bubble_model.h
[add] https://crrev.com/9f8ca0e35834223cb58ce777c9ccd49e903e7434/chrome/browser/renderer_context_menu/spelling_bubble_model_browsertest.cc
[modify] https://crrev.com/9f8ca0e35834223cb58ce777c9ccd49e903e7434/chrome/test/BUILD.gn


### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90e0022e33af99c4e7320774c888af92c876d11b

commit 90e0022e33af99c4e7320774c888af92c876d11b
Author: Avi Drissman <avi@chromium.org>
Date: Thu Jun 10 07:06:47 2021

[M90-LTS] Fix UaF for the enhanced spell check bubble

For the enhanced spell check bubble, be sure to use a valid
WebContents for the help page. Adds a browser test.

Note that this is a clone of 427728383657e6ccb06dbfcce0c5118bb557c0af
that was committed to fix the same issue with the accessibility
bubble. Alas, these are the only two subclassers of ConfirmBubbleModel
across the Chromium codebase, and given that ConfirmBubbleModel is in
ui/ and can't know about this specific lifetime issue, this is the
simplest way forward.

(cherry picked from commit b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4)

(cherry picked from commit 9f8ca0e35834223cb58ce777c9ccd49e903e7434)

Bug: 1212498
Test: As in bug
Change-Id: I365e9721613ea2a89a8fad902ddc137b24de687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920807
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937516
Commit-Queue: Katie Dektar <katie@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1423}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2945788
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1514}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/90e0022e33af99c4e7320774c888af92c876d11b/chrome/browser/renderer_context_menu/spelling_bubble_model.cc
[modify] https://crrev.com/90e0022e33af99c4e7320774c888af92c876d11b/chrome/browser/renderer_context_menu/spelling_bubble_model.h
[add] https://crrev.com/90e0022e33af99c4e7320774c888af92c876d11b/chrome/browser/renderer_context_menu/spelling_bubble_model_browsertest.cc
[modify] https://crrev.com/90e0022e33af99c4e7320774c888af92c876d11b/chrome/test/BUILD.gn


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/536bcb2d708f12decb47d0454da0b95995145974

commit 536bcb2d708f12decb47d0454da0b95995145974
Author: Avi Drissman <avi@chromium.org>
Date: Thu Jun 10 07:20:34 2021

[M86-LTS] Fix UaF for the enhanced spell check bubble

For the enhanced spell check bubble, be sure to use a valid
WebContents for the help page. Adds a browser test.

Note that this is a clone of 427728383657e6ccb06dbfcce0c5118bb557c0af
that was committed to fix the same issue with the accessibility
bubble. Alas, these are the only two subclassers of ConfirmBubbleModel
across the Chromium codebase, and given that ConfirmBubbleModel is in
ui/ and can't know about this specific lifetime issue, this is the
simplest way forward.

(cherry picked from commit b427418352dc5a2e095aaa3f3dcd3c55d91dfbd4)

(cherry picked from commit 9f8ca0e35834223cb58ce777c9ccd49e903e7434)

Bug: 1212498
Test: As in bug
Change-Id: I365e9721613ea2a89a8fad902ddc137b24de687f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2920807
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#887244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2937516
Commit-Queue: Katie Dektar <katie@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1423}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944944
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1664}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/536bcb2d708f12decb47d0454da0b95995145974/chrome/browser/renderer_context_menu/spelling_bubble_model.cc
[modify] https://crrev.com/536bcb2d708f12decb47d0454da0b95995145974/chrome/browser/renderer_context_menu/spelling_bubble_model.h
[add] https://crrev.com/536bcb2d708f12decb47d0454da0b95995145974/chrome/browser/renderer_context_menu/spelling_bubble_model_browsertest.cc
[modify] https://crrev.com/536bcb2d708f12decb47d0454da0b95995145974/chrome/test/BUILD.gn


### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congrats, David on another one! The VRP Panel has decided to award you $10,000 for this report. Nice work. 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### ja...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212498?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055974)*
